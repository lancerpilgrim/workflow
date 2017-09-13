from bidong.core.exceptions import NotFoundError
from bidong.common.utils import ObjectDict, dictize, get_current_timestamp
from bidong.service.v2.repo import ResourceQuery
from bidong.service.v2.repo.ManagersRepository import (
    ManagerAuthsRepository,
    ManagersAuthsQuery,
    ManagerOverviewsRepository, ManagerOverviewsQuery)
from bidong.service.v2.domain.ValueObjects import Resource, Auth
from bidong.service.v2.domain.DomainTools import *
from bidong.service.v2.domain import REVERSED_CLIENT_RESOURCES_MAP

DEFAULT_METHOD_LIST = ["DELETE", "PUT", "POST", "GET"]


class ManagerAuthsDomain(object):
    """
    平台管理员的权限聚合
    """

    def __init__(self, manager_id, resources_auths=None, project_id=None):
        # 初始化参数包括了manager权限几个维度:
        # 作为实体id的manager_id, 资源值对象resourceVO, 针对该资源值对象的授权值对象authVO,
        # resourceVO和authVO构成了一个完整权限值对象, 它从属于某个由project_id标识的project
        # 由此构建出manager的权限领域模型.
        # 无论构建方式是查询已有数据库还是根据输入参数, 持久化时调用者不能作出区分, 请注意这一点
        self.id = manager_id
        self._resources_auths = resources_auths
        self._project_id = project_id
        self.auth_entities_map = {}
        self.auth_entities_list = None

    def construct_entities(self):
        if self._resources_auths:
            self.reset(self._resources_auths)
        else:
            self._construct_current_entities()
        return self

    def _construct_current_entities(self):
        # 功能性资源, 一条feature-auth从属于某一个project
        fquery = ManagersAuthsQuery().list_user_features(self.id)
        if self._project_id:
            fquery = fquery.filter_by_project(self._project_id)
        query_set, p = fquery.all()
        for q in query_set:
            auth_entity = self.ManagerAuthEntity(self.id,
                                                 Resource(q.resource_name,
                                                          q.resource_locator,
                                                          resource_type=Resource.FEATURE),
                                                 Auth(self.id,
                                                      status=q.status,
                                                      allow_method=q.allow_method))
            self.auth_entities_map[(self.id, q.resource_name, q.resource_locator)] = auth_entity

        # 数据性资源
        dquery = ManagersAuthsQuery().list_user_data(self.id)
        if self._project_id:
            dquery = dquery.filter_by_project(self._project_id)
        query_set, p = dquery.all()
        for q in query_set:
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
            if each.resource.resource_type == Resource.DATA:
                # todo 这个分支暂时不会被运行
                avo = self.ManagerAuthDataVO(each.resource, each.auth).struct
                data_id = each.resource.locator
                if data_id in authorizations.contents:
                    if hasattr(authorizations.contents[data_id], "data"):
                        authorizations.contents[data_id].data.append(avo)
                    else:
                        authorizations.contents[data_id].data = [avo]
                else:
                    item = ObjectDict()
                    item.data = [avo]
                    item.project_id = each.resource.locator
                    authorizations.contents[data_id] = item
            if each.resource.resource_type == Resource.FEATURE:
                fvo = self.ManagerAuthFeatureVO(each.resource, each.auth).struct
                project_id = each.resource.locator
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
               新增的权限将被创建. 权限设置的逻辑是这样的: 不支持patch式的更新
               所以在实现上, 每次更新实质上是重新定义一遍用户的权限, 即Reset. 这种情况下新建和更新是同一的.
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
            r = ResourceQuery().locate_by_name(self.resource.name)
            self.resource.id = r.id
            self.resource.resource_type = r.resource_type

    class ManagerAuthDataVO(object):

        def __init__(self, resource, auth):
            self._resource = resource
            self._auth = auth
            self.name = self._resource.name
            self.description = self._get_description()
            self.allow_method = ensure_method_as_list(self._auth.allow_method)
            self.data_id = self._resource.locator

        @property
        def struct(self):
            item = ObjectDict()
            item.name = self.name
            item.allow_method = self.allow_method
            item.description = self.description
            item.data_id = self.data_id
            return item

        def _get_description(self):
            # TODO 获取名字
            if self.name == "platform_project_data":
                return "测试项目"
            return "测试项目"

    class ManagerAuthFeatureVO(object):
        def __init__(self, resource, auth):
            self._resource = resource
            self._auth = auth
            self.name = self._resource.name
            self.description = REVERSED_CLIENT_RESOURCES_MAP[self.name]
            self.allow_method = ensure_method_as_list(self._auth.allow_method)

        @property
        def struct(self):
            item = ObjectDict()
            item.name = self.name
            item.description = self.description
            item.allow_method = self.allow_method
            return item


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
    def __init__(self, manager_id=None, overviews=None,
                 resources_auths=None, project_id=None):
        self.overviews = None
        self.authorizations = None
        self.id = None
        self.od = None
        self.ad = None
        self._id = manager_id
        self._overviews = overviews
        self._resources_auths = resources_auths
        self._project_id = project_id

    def construct_entities(self):
        t1 = get_current_timestamp(integer=False)
        self.od = ManagerOverviewsDomain(self._id, self._overviews)
        self.overviews = self.od.construct_entities().struct
        t2 = get_current_timestamp(integer=False)
        print("ov construct cost:{0}".format(t2-t1))
        self.id = self.overviews.id
        self.ad = ManagerAuthsDomain(self.id, self._resources_auths, self._project_id)
        self.authorizations = self.ad.construct_entities().struct
        t3 = get_current_timestamp(integer=False)
        print("au construct cost:{0}".format(t3 - t2))
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
