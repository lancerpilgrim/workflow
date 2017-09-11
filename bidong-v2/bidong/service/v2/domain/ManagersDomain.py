from bidong.common.utils import ObjectDict, get_dict_attribute
from bidong.service.v2.repo.AdministratorsRepository import (
    AdministratorAuthsRepository,
    AdministratorsAuthsQuery
)
from bidong.service.v2.repo import ResourcesQuery
from bidong.service.v2.domain.ValueObjects import Resource, Auth
from bidong.service.v2.domain.DomainTools import *

DEFAULT_METHOD_LIST = ["DELETE", "PUT", "POST", "GET"]


class ManagerAuthsDomain(object):
    """
    平台管理员的权限聚合
    """
    def __init__(self, administrator_id):
        self.id = administrator_id
        self.auth_entities_map = {}
        self.auth_entities = []
        # 实际上, auth_entity的真正的实体id是它在auth_entities中的key, 因为这个key被设计成独一无二
        # 在仓储中, id已经存在的实体会执行更新操作, id不存在的则执行新建操作, 这不需要被Domain感知到
        # Repository只包含Command, 实际只需要GetByEntityId和Save即可, Query由专门的Query类承担.

    def reset(self, resources_auths):
        """
        :brief 完整地重新定义所有权限，不在auths列表中的原有权限都将被置为DELETE状态, 已经存在的将被更新, 
               新增的权限将被创建. 权限设置的逻辑是这样的: 对于前端来说实现patch式的更新是相对繁琐的操作,
               所以在实现上, 每次都会重新定义一个用户的权限, 即Reset. 这种情况下新建和更新是同一的.
        :param resources_auths: a nested list [(resource, auth), ....]
               resource: a instance of Resource,
               auth: a instance of Auth
        :return: 更新后的权限列表
        """
        # 构建现有权限实体
        self.construct_current_entities()

        # 计算得到新的权限实体
        existing = {key: value.auth.allow_method for key, value in self.auth_entities_map.items()}
        pending = {(self.id, resource.name, str(resource.locator)): ensure_method_as_int(auth.allow_method)
                   for (resource, auth) in resources_auths}
        union = set(pending).union(existing)
        to_delete = set(union).difference(pending)
        to_update = set(pending).intersection(existing)
        to_create = set(union).difference(existing)
        for key in to_delete:
            self.auth_entities_map[key](
                self.AdministratorAuthEntity(self.id,
                                             Resource(*key),
                                             Auth(self.id, status=Auth.DELETE)))
        for key in to_update:
            self.auth_entities_map[key](
                self.AdministratorAuthEntity(self.id,
                                             Resource(*key),
                                             Auth(self.id,
                                                  status=Auth.ENABLED,
                                                  allow_method=pending[key])))
        for key in to_create:
            self.auth_entities_map[key](
                self.AdministratorAuthEntity(self.id,
                                             Resource(*key),
                                             Auth(self.id,
                                                  status=Auth.ENABLED,
                                                  allow_method=pending[key])))
        # 在生命周期的某个时候持久化本聚合中的实体
        return self

    def construct_current_entities(self):
        query = AdministratorsAuthsQuery().list_user_features(self.id).all()
        for q in query:
            auth_entity = self.AdministratorAuthEntity(self.id,
                                                       Resource(q.resouce_name, q.resource_locator),
                                                       Auth(self.id,
                                                            status=q.status,
                                                            allow_method=q.allow_method))
            self.auth_entities_map[(self.id, q.resouce_name, q.resource_locator)] = auth_entity
        return self

    def save(self):
        self.auth_entities = AdministratorAuthsRepository().persist(self.auth_entities_map)
        return self

    def get_entities(self):
        # 返回实体列表
        return self.auth_entities

    def disable_one_auth(self, resource):
        self._add_entities(resource, Auth(self.id, status=Auth.DISABLED))
        return self

    def enable_one_auth(self, resource):
        self._add_entities(resource, Auth(self.id, status=Auth.ENABLED))
        return self

    def delete_one_auth(self, resource):
        self._add_entities(resource, Auth(self.id, status=Auth.DELETE))
        return self

    def _add_entities(self, resource, auth):
        auth_entity = self.AdministratorAuthEntity(self.id, resource, auth)
        self.auth_entities_map[(self.id, resource.name, resource.locator)] = auth_entity

    class AdministratorAuthEntity(object):
        def __init__(self, administrator_id, resource, auth):
            """
            :param administrator_id: 
            :param resource: a instance of Resource 
            """
            self.id = administrator_id
            self.resource = resource
            self.auth = auth
            self.validate()

        def validate(self):
            self._ensure_resource()
            self._ensure_auth()

        def _ensure_auth(self):
            self.auth.allow_method = ensure_method_as_int(self.auth.allow_method)

        def _ensure_resource(self):
            self.resource.id = ResourcesQuery().locate_by_name(self.resource.name).one().id


class ManagersService(object):

    def __init__(self):
        self.repo = ManagersRepo()

    def get_by_mobile(self, mobile):
        return self.repo.get_by_mobile(mobile)

    def integrated_create(self, overviews=None, authorizations=None):
        item = ObjectDict({})
        item.overviews = self.create_overviews(overviews)
        item.authorizations = self.create_authorizations(item.overviews.id, authorizations)
        item.id = item.overviews.id

        # 初始化手机号密码登录
        from bidong.service.login import ManagerPasswordLoginService
        ps = ManagerPasswordLoginService(item.overviews.mobile)
        ps.init_user_login_info(item.id)

        return item

    def create_overviews(self, overviews):
        overviews = self.repo.create(overviews)
        return overviews

    @staticmethod
    def create_authorizations(manager_id, authorizations):
        auth_service = ManagerAuthsService(manager_id)
        projects = authorizations["contents"]
        authorizations_parameters = []
        for project in projects:
            locator = project["project_id"]
            for feature in project["features"]:
                if "allow_method" not in feature.keys():
                    feature["allow_method"] = ["DELETE", "PUT", "POST", "GET"]
                p = (Resource(feature["name"], locator), Auth(manager_id, feature["allow_method"]))
                authorizations_parameters.append(p)
        authorizations = auth_service._integrated_create_or_update(authorizations_parameters).list()
        return authorizations

    def get_details(self, page, per_page, sort="", order=""):
        payload = ObjectDict({})
        overviews = self.get_overviews(page, per_page, sort, order)
        content = []
        # 添加授权信息
        for overview in overviews.objects:
            item = ObjectDict({})
            item.authorizations = ManagerService(overview.id).get_authorizations()
            item.overviews = overview
            item.id = item.overviews.id
            content.append(item)
        payload.update(overviews)
        payload.objects = content
        return payload

    def get_fields(self, fields):
        payload = ObjectDict({"objects": []})
        overviews = self.get_overviews(0, 0)
        # 添加授权信息
        for overview in overviews.objects:
            item = ObjectDict({})
            item.authorizations = ManagerService(overview.id).get_authorizations()
            item.overviews = overview
            item.id = item.overviews.id
            downsized_item = {}
            for field in fields.split(","):
                try:
                    key, value = get_dict_attribute(item, field)
                    downsized_item[key] = value
                except Exception:
                    raise InvalidParametersError(message="`fields`參數有誤")
            payload.objects.append(downsized_item)
        print(payload)
        return payload

    def get_overviews(self, page, per_page, sort="", order=""):
        return self.repo.filter_enabled().all(page, per_page, sort, order)


class ManagerService(object):

    def __init__(self, _id):
        self._id = _id
        self.repo = ManagerRepo(_id)

    def get_details(self):
        item = ObjectDict({})
        item.overviews = self.get_overviews()
        item.authorizations = self.get_authorizations()
        item.id = self._id
        return item

    def get_authorizations(self):
        auth_service = ManagerAuthsService(self._id)
        authorizations = auth_service.list()
        return authorizations

    def get_overviews(self):
        self.repo.get_by_pk()
        return self.repo.one()

    def exists(self):
        try:
            self.get_overviews()
        except Exception:
            return False
        else:
            return True

    def check_enable(self):
        try:
            assert self.get_overviews().status == self.repo.ENABLED
        except Exception:
            return False
        else:
            return True

    def integrated_update(self, overviews=None, authorizations=None):
        item = ObjectDict({})
        item.overviews = self.update_overviews(overviews)
        item.authorizations = self.update_authorizations(authorizations)
        item.id = item.overviews.id
        return item

    def update_overviews(self, overviews=None):
        self.repo.get_by_pk()
        overviews = self.repo.update(overviews).one()
        return overviews

    def update_authorizations(self, authorizations=None):
        auth_service = ManagerAuthsService(self._id)
        projects = authorizations["contents"]
        authorizations_parameters = []
        for project in projects:
            locator = project["project_id"]
            for feature in project["features"]:
                if "allow_method" not in feature.keys():
                    feature["allow_method"] = ["DELETE", "PUT", "POST", "GET"]
                p = (Resource(feature["name"], locator), Auth(self._id, feature["allow_method"]))
                authorizations_parameters.append(p)
        authorizations = auth_service._integrated_create_or_update(authorizations_parameters).list()

        return authorizations

    def disable(self):
        self.repo.get_by_pk()
        self.repo.disable()

    def enable(self):
        self.repo.get_by_pk()
        self.repo.enable()

    def delete(self):
        self.repo.get_by_pk()
        self.repo.delete()