from bidong.core.exceptions import NotFoundError
from bidong.common.utils import ObjectDict, dictize, get_current_timestamp
from bidong.service.v2.repo.ManagersRepository import (
    ManagerAuthsRepository,
    ManagersAuthsQuery,
    ManagerOverviewsRepository, ManagerOverviewsQuery)
from bidong.service.v2.repo import ResourcesQuery
from bidong.service.v2.domain.ValueObjects import Resource, Auth
from bidong.service.v2.domain.DomainTools import *
from bidong.service.v2.domain import REVERSED_CLIENT_RESOURCES_MAP, REVERSED_PLATFORM_RESOURCES_MAP, \
    PLATFORM_RESOURCES_MAP, CLIENT_RESOURCES_MAP
from pprint import pprint

DEFAULT_METHOD_LIST = ["DELETE", "PUT", "POST", "GET"]


class ManagerAuthsDomain(object):
    """
    平台管理员的权限聚合
    """

    def __init__(self, manager_id, resources_auths=None):
        self.id = manager_id
        self._resources_auths = resources_auths
        self.auth_entities_map = {}
        self.auth_entities_list = None
        # 实际上, auth_entity的真正的实体id是它在auth_entities中的key, 因为这个key被设计成独一无二
        # 在仓储中, id已经存在的实体会执行更新操作, id不存在的则执行新建操作, 这不需要被Domain感知到
        # Repository只包含Command, 实际只需要GetByEntityId和Save即可, Query由专门的Query类承担.

    def construct_entities(self):
        if self._resources_auths:
            self.reset(self._resources_auths)
        else:
            self._construct_current_entities()
        return self

    def _construct_current_entities(self):
        # 功能性资源
        query, p = ManagersAuthsQuery().list_user_features(self.id).all()
        for q in query:
            auth_entity = self.ManagerAuthEntity(self.id,
                                                 Resource(q.resource_name,
                                                          q.resource_locator,
                                                          resource_type=Resource.FEATURE),
                                                 Auth(self.id,
                                                      status=q.status,
                                                      allow_method=q.allow_method))
            self.auth_entities_map[(self.id, q.resource_name, q.resource_locator)] = auth_entity
        # 数据性资源
        query, p = ManagersAuthsQuery().list_user_data(self.id).all()
        for q in query:
            auth_entity = self.ManagerAuthEntity(self.id,
                                                 Resource(q.resource_name,
                                                          q.resource_locator,
                                                          resource_type=Resource.DATA),
                                                 Auth(self.id,
                                                      status=q.status,
                                                      allow_method=q.allow_method))
            self.auth_entities_map[(self.id, q.resource_name, q.resource_locator)] = auth_entity
        return self

    def save(self):
        ManagerAuthsRepository().persist(self.auth_entities_map)
        return self

    def ensure_existence(self):
        # 校验用户存在性
        a = ManagerOverviewsQuery().get_by_id(self.id).one()
        if a and a.status == ManagerOverviewsDomain.ManagerOverviewsEntity.DELETE:
            raise NotFoundError("用户不存在")
        return self

    @property
    def struct(self):
        # 返回结构化的授权信息
        authorizations = ObjectDict()
        authorizations.id = self.id
        authorizations.contents = ObjectDict()

        for each in self.auth_entities_map.values():
            if each.auth.status != Auth.ENABLED:
                continue
            locator = each.resource.locator
            project_id = locator
            if each.resource.resource_type == Resource.DATA:
                # todo 这里暂时是没有的
                avo = ObjectDict(dictize(self.ManagerAuthDataVO(each.resource, each.auth)))
                if project_id in authorizations.contents:
                    if hasattr(authorizations.contents[project_id], "data"):
                        authorizations.contents[project_id].data.append(avo)
                    else:
                        authorizations.contents[project_id].data = [avo]
                else:
                    item = ObjectDict()
                    item.data = [avo]
                    item.project_id = each.resource.locator
                    authorizations.contents[project_id] = item
            if each.resource.resource_type == Resource.FEATURE:
                fvo = ObjectDict(dictize(self.ManagerAuthFeatureVO(each.resource, each.auth)))
                if project_id in authorizations.contents:
                    if hasattr(authorizations.contents[project_id], "features"):
                        authorizations.contents[project_id].features.append(fvo)
                    else:
                        authorizations.contents[project_id].features = [fvo]
                else:
                    item = ObjectDict()
                    item.features = [fvo]
                    item.project_id = each.resource.locator
                    item.project_name = "-"
                    authorizations.contents[project_id] = item
        authorizations.contents = list(authorizations.contents.values())
        return authorizations

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
        self._construct_current_entities()

        # 计算得到新的权限实体
        existing = {key: value for key, value in self.auth_entities_map.items()}
        pending = {(self.id, resource.name, str(resource.locator)): ensure_method_as_int(auth.allow_method)
                   for (resource, auth) in resources_auths}
        union = set(pending).union(existing)
        to_delete = set(union).difference(pending)
        to_update = set(pending).intersection(existing)
        to_create = set(union).difference(existing)
        for key in to_delete:
            self.auth_entities_map[key] = self.ManagerAuthEntity(self.id,
                                                                 Resource(*key[1:]),
                                                                 Auth(self.id, status=Auth.DELETE))
        for key in to_update:
            self.auth_entities_map[key] = self.ManagerAuthEntity(self.id,
                                                                 Resource(*key[1:]),
                                                                 Auth(self.id,
                                                                      status=Auth.ENABLED,
                                                                      allow_method=pending[key]))
        for key in to_create:
            self.auth_entities_map[key] = self.ManagerAuthEntity(self.id,
                                                                 Resource(*key[1:]),
                                                                 Auth(self.id,
                                                                      status=Auth.ENABLED,
                                                                      allow_method=pending[key]))
        # 在生命周期的某个时候持久化本聚合中的实体
        return self

    def disable_one_auth(self, resource):
        self._add_entities_to_map(resource, Auth(self.id, status=Auth.DISABLED))
        return self

    def enable_one_auth(self, resource):
        self._add_entities_to_map(resource, Auth(self.id, status=Auth.ENABLED))
        return self

    def delete_one_auth(self, resource):
        self._add_entities_to_map(resource, Auth(self.id, status=Auth.DELETE))
        return self

    def _add_entities_to_map(self, resource, auth):
        auth_entity = self.ManagerAuthEntity(self.id, resource, auth)
        self.auth_entities_map[(self.id, resource.name, resource.locator)] = auth_entity

    class ManagerAuthEntity(object):
        def __init__(self, manager_id, resource, auth):
            """
            :param manager_id:
            :param resource: a instance of Resource
            """
            self.id = manager_id
            self.resource = resource
            self.auth = auth
            self.validate()

        def validate(self):
            self._ensure_resource()
            self._ensure_auth()

        def _ensure_auth(self):
            self.auth.allow_method = ensure_method_as_int(self.auth.allow_method)

        def _ensure_resource(self):
            r = ResourcesQuery().locate_by_name(self.resource.name).one()
            self.resource.id = r.id
            self.resource.resource_type = r.resource_type

    class ManagerAuthDataVO(object):

        def __init__(self, resource, auth):
            self._resource = resource
            self._auth = auth
            self.name = None
            self.description = None
            self.allow_method = None
            self.data_id = None
            self.struct()

        def struct(self):
            self.name = self._resource.name
            self.allow_method = ensure_method_as_list(self._auth.allow_method)
            self.description = self._get_description()
            self.data_id = self._resource.locator

        def _get_description(self):
            # TODO 获取名字
            if self.name == "platform_project_data":
                return "测试项目"
            return "测试项目"

    class ManagerAuthFeatureVO(object):
        def __init__(self, resource, auth):
            self._resource = resource
            self._auth = auth
            self.name = None
            self.description = None
            self.allow_method = None
            self.struct()

        def struct(self):
            self.name = self._resource.name
            self.allow_method = ensure_method_as_list(self._auth.allow_method)
            self.description = REVERSED_CLIENT_RESOURCES_MAP[self.name]


class ManagerOverviewsDomain(object):
    """
    平台管理员的基础信息聚合,　可以根据id构建出聚合的结构, 也可以根据输入参数来决定.
    """

    def __init__(self, manager_id=None, overviews=None):
        self._overviews = overviews
        self._manager_id = manager_id
        self.manager_entity = None
        self.id = None

    def construct_entities(self):
        if self._overviews is None and self._manager_id is None:
            raise Exception()
        if self._overviews and self._manager_id is None:
            self.manager_entity = self.ManagerOverviewsEntity(self._overviews)
        if self._overviews and self._manager_id:
            self._overviews.update(id=self._manager_id)
            self.manager_entity = self.ManagerOverviewsEntity(self._overviews)
        if not self._overviews and self._manager_id:
            q = ManagerOverviewsQuery().get_by_id(self._manager_id).one()
            self.manager_entity = self.ManagerOverviewsEntity(q)
        self.id = self.manager_entity.id
        return self

    @property
    def struct(self):
        return ObjectDict(dictize(self.manager_entity))

    def save(self):
        ManagerOverviewsRepository().persist(self.manager_entity)
        return self

    def ensure_existence(self):
        if self.manager_entity.status == self.ManagerOverviewsEntity.DELETE:
            raise NotFoundError("用户不存在")
        return self

    def disable(self):
        self.manager_entity.status = self.ManagerOverviewsEntity.DISABLED
        return self

    def enable(self):
        self.manager_entity.status = self.ManagerOverviewsEntity.ENABLED
        return self

    def delete(self):
        self.manager_entity.status = self.ManagerOverviewsEntity.DELETE
        return self

    class ManagerOverviewsEntity(object):
        ENABLED = 1
        DISABLED = 0
        DELETE = 2

        def __init__(self, overviews):
            """
            :param overviews: a instance of Dict?
            """
            self.id = overviews.get("id")
            self.name = overviews.get("name", "")
            self.mobile = overviews.get("mobile")
            self.create_time = overviews.get("create_time")
            self.description = overviews.get("description")
            self.status = overviews.get("status", None)
            self.validate()

        def validate(self):
            if self.id and not self.create_time:
                _overviews = ManagerOverviewsQuery().get_by_id(self.id).one()
                self.create_time = _overviews.create_time
            if not self.id:
                self.id = generate_id(duplicate_checker=self.id_exists)
                self.create_time = get_current_timestamp()
            if self.status is None:
                self.status = self.ENABLED

        @staticmethod
        def id_exists(_id):
            return ManagerOverviewsQuery().get_by_id(_id).exists()


class ManagerDomain(object):
    def __init__(self, manager_id=None, overviews=None, resources_auths=None):
        self.overviews = None
        self.authorizations = None
        self.id = None
        self.od = None
        self.ad = None
        self._id = manager_id
        self._overviews = overviews
        self._resources_auths = resources_auths

    def construct_entities(self):
        self.od = ManagerOverviewsDomain(self._id, self._overviews)
        self.overviews = self.od.construct_entities().struct
        self.id = self.overviews.id
        self.ad = ManagerAuthsDomain(self.id, self._resources_auths)
        self.authorizations = self.ad.construct_entities().struct
        return self

    @property
    def struct(self):
        manager = ObjectDict()
        manager.overviews = self.overviews
        manager.authorizations = self.authorizations
        manager.id = self.id
        return manager

    def save(self):
        self.od = self.od.save()
        self.ad = self.ad.save()
        return self

    def ensure_existence(self):
        self.od.ensure_existence()
        return self
