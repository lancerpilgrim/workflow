import time

from bidong.common.utils import ObjectDict, get_dict_attribute, dictize, generate_random_number
from bidong.service.v2.repo.AdministratorsRepository import (
    AdministratorAuthsRepository,
    AdministratorsAuthsQuery,
    AdministratorOverviewsRepository, AdministratorOverviewsQuery)
from bidong.service.v2.repo import ResourcesQuery
from bidong.service.v2.domain.ValueObjects import Resource, Auth
from bidong.service.v2.domain.DomainTools import *
from bidong.service.v2.domain import REVERSED_CLIENT_RESOURCES_MAP, REVERSED_PLATFORM_RESOURCES_MAP, \
    PLATFORM_RESOURCES_MAP, CLIENT_RESOURCES_MAP
from pprint import pprint

DEFAULT_METHOD_LIST = ["DELETE", "PUT", "POST", "GET"]


class AdministratorAuthsDomain(object):
    """
    平台管理员的权限聚合
    """

    def __init__(self, administrator_id, resources_auths=None):
        self.id = administrator_id
        self._resources_auths = resources_auths
        self.auth_entities_map = {}
        self.auth_entities_list = None
        # 实际上, auth_entity的真正的实体id是它在auth_entities中的key, 因为这个key被设计成独一无二
        # 在仓储中, id已经存在的实体会执行更新操作, id不存在的则执行新建操作, 这不需要被Domain感知到
        # Repository只包含Command, 实际只需要GetByEntityId和Save即可, Query由专门的Query类承担.

    def construct_entities(self):
        if self._resources_auths:
            print("-")
            pprint(self._resources_auths)
            print("-")
            self.reset(self._resources_auths)
        else:
            self._construct_current_entities()
        return self

    def _construct_current_entities(self):
        # 功能性资源
        query, p = AdministratorsAuthsQuery().list_user_features(self.id).all()
        for q in query:
            auth_entity = self.AdministratorAuthEntity(self.id,
                                                       Resource(q.resource_name,
                                                                q.resource_locator,
                                                                resource_type=Resource.FEATURE),
                                                       Auth(self.id,
                                                            status=q.status,
                                                            allow_method=q.allow_method))
            self.auth_entities_map[(self.id, q.resource_name, q.resource_locator)] = auth_entity
        # 数据性资源
        query, p = AdministratorsAuthsQuery().list_user_data(self.id).all()
        for q in query:
            auth_entity = self.AdministratorAuthEntity(self.id,
                                                       Resource(q.resource_name,
                                                                q.resource_locator,
                                                                resource_type=Resource.DATA),
                                                       Auth(self.id,
                                                            status=q.status,
                                                            allow_method=q.allow_method))
            self.auth_entities_map[(self.id, q.resource_name, q.resource_locator)] = auth_entity
        return self

    def save(self):
        AdministratorAuthsRepository().persist(self.auth_entities_map)
        return self

    @property
    def struct(self):
        # 返回结构化的授权信息

        authorizations = ObjectDict()
        authorizations.id = self.id
        authorizations.features = []
        authorizations.data = []

        for each in self.auth_entities_map.values():
            if each.auth.status != Auth.ENABLED:
                continue
            if each.resource.resource_type == Resource.DATA:
                item = ObjectDict(dictize(self.AdministratorAuthDataVO(each.resource, each.auth)))
                authorizations.data.append(item)
            if each.resource.resource_type == Resource.FEATURE:
                item = ObjectDict(dictize(self.AdministratorAuthFeatureVO(each.resource, each.auth)))
                authorizations.features.append(item)

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
            self.auth_entities_map[key] = self.AdministratorAuthEntity(self.id,
                                                                       Resource(*key[1:]),
                                                                       Auth(self.id, status=Auth.DELETE))
        for key in to_update:
            self.auth_entities_map[key] = self.AdministratorAuthEntity(self.id,
                                                                       Resource(*key[1:]),
                                                                       Auth(self.id,
                                                                            status=Auth.ENABLED,
                                                                            allow_method=pending[key]))
            pprint(self.auth_entities_map[key].__dict__)
        for key in to_create:
            self.auth_entities_map[key] = self.AdministratorAuthEntity(self.id,
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
            r = ResourcesQuery().locate_by_name(self.resource.name).one()
            self.resource.id = r.id
            self.resource.resource_type = r.resource_type

    class AdministratorAuthDataVO(object):

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

    class AdministratorAuthFeatureVO(object):
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
            self.description = REVERSED_PLATFORM_RESOURCES_MAP[self.name]


class AdministratorOverviewsDomain(object):
    """
    平台管理员的基础信息聚合,　可以根据id构建出聚合的结构, 也可以根据输入参数来决定.
    """

    def __init__(self, administrator_id=None, overviews=None):
        self._overviews = overviews
        self._administrator_id = administrator_id
        self.administrator_entity = None
        self.id = None

    def construct_entities(self):
        if self._overviews is None and self._administrator_id is None:
            raise Exception()
        if self._overviews and self._administrator_id is None:
            self.administrator_entity = self.AdministratorOverviewsEntity(self._overviews)
        if self._overviews and self._administrator_id:
            self._overviews.update(id=self._administrator_id)
            self.administrator_entity = self.AdministratorOverviewsEntity(self._overviews)
        if not self._overviews and self._administrator_id:
            q = AdministratorOverviewsQuery().get_by_id(self._administrator_id).one()
            self.administrator_entity = self.AdministratorOverviewsEntity(q)
        self.id = self.administrator_entity.id
        return self

    @property
    def struct(self):
        return ObjectDict(dictize(self.administrator_entity))

    def save(self):
        AdministratorOverviewsRepository().persist(self.administrator_entity)
        return self

    def disable(self):
        self.administrator_entity.status = self.AdministratorOverviewsEntity.DISABLED
        return self

    def enable(self):
        self.administrator_entity.status = self.AdministratorOverviewsEntity.ENABLED
        return self

    def delete(self):
        self.administrator_entity.status = self.AdministratorOverviewsEntity.DELETE
        return self

    class AdministratorOverviewsEntity(object):
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
            self.status = overviews.get("status")
            self.validate()

        def validate(self):
            if self.id and not self.create_time:
                _overviews = AdministratorOverviewsQuery().get_by_id(self.id).one()
                self.create_time = _overviews.create_time
            if not self.id:
                self.id = generate_id(duplicate_checker=self.id_exists)
                self.create_time = int(time.time())
            if not self.status:
                self.status = self.ENABLED

        @staticmethod
        def id_exists(_id):
            return AdministratorOverviewsQuery().get_by_id(_id).exists()


class AdministratorDomain(object):
    def __init__(self, administrator_id=None, overviews=None, resources_auths=None):
        self.overviews = None
        self.authorizations = None
        self.id = None
        self.od = None
        self.ad = None
        self._id = administrator_id
        self._overviews = overviews
        self._resources_auths = resources_auths

    def construct_entities(self):
        self.od = AdministratorOverviewsDomain(self._id, self._overviews)
        self.overviews = self.od.construct_entities().struct
        self.id = self.overviews.id
        self.ad = AdministratorAuthsDomain(self.id, self._resources_auths)
        self.authorizations = self.ad.construct_entities().struct
        return self

    @property
    def struct(self):
        administrator = ObjectDict()
        administrator.overviews = self.overviews
        administrator.authorizations = self.authorizations
        administrator.id = self.id
        return administrator

    def save(self):
        self.od = self.od.save()
        self.ad = self.ad.save()
        return self
