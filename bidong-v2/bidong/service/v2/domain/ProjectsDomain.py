import time

from bidong.common.utils import ObjectDict, get_dict_attribute, dictize, generate_random_number
from bidong.service.v2.repo.ProjectsRepository import (
    ProjectAuthsRepository,
    ProjectsAuthsQuery,
    ProjectOverviewsRepository, ProjectOverviewsQuery)
from bidong.service.v2.repo import ResourcesQuery
from bidong.service.v2.domain.ValueObjects import Resource, Auth
from bidong.service.v2.domain.DomainTools import *
from bidong.service.v2.domain import REVERSED_CLIENT_RESOURCES_MAP, REVERSED_PLATFORM_RESOURCES_MAP, \
    PLATFORM_RESOURCES_MAP, CLIENT_RESOURCES_MAP
from bidong.service.v2.repo.ProjectsRepository import ProjectAuthsRepository, ProjectsAuthsQuery

DEFAULT_METHOD_LIST = ["DELETE", "PUT", "POST", "GET"]


class ProjectAuthsDomain(object):
    """
    项目的权限聚合
    """

    def __init__(self, project_id, resources_auths=None):
        self.id = project_id
        self._resources_auths = resources_auths
        self._manager_auth_entity = None
        self._administrator_auth_entity = None
        self.project_auth_entities_map = {}
        self.project_auth_entities_list = None

    def construct_entities(self):
        if self._resources_auths:
            self.reset(self._resources_auths)
            self._construct_related_entities()
        else:
            self._construct_current_entities()
        return self

    def _construct_current_entities(self):
        # 功能性资源
        query, p = ProjectsAuthsQuery().list_project_features(self.id).all()
        for q in query:
            auth_entity = self.ProjectAuthEntity(self.id,
                                                 Resource(q.resource_name,
                                                          q.resource_locator,
                                                          resource_type=ProjectsAuthsQuery.FEATURE),
                                                 Auth(self.id,
                                                      status=q.status,
                                                      allow_method=q.allow_method))
            self.project_auth_entities_map[(self.id, q.resource_name, q.resource_locator)] = auth_entity
        # 数据性资源
        query, p = ProjectsAuthsQuery().list_project_data(self.id).all()
        for q in query:
            auth_entity = self.ProjectAuthEntity(self.id,
                                                 Resource(q.resource_name,
                                                          q.resource_locator,
                                                          resource_type=ProjectsAuthsQuery.DATA),
                                                 Auth(self.id,
                                                      status=q.status,
                                                      allow_method=q.allow_method))
            self.project_auth_entities_map[(self.id, q.resource_name, q.resource_locator)] = auth_entity
        return self

    def _construct_related_entities(self):
        # TODO 项目的权限改变时，需要同步变更对应的管理员记录
        for each in self.project_auth_entities_map.values():
            manager_resource = Resource(each.resource.name, resource_locator=self.id)

        return self

    def save(self):
        ProjectAuthsRepository().persist(self.project_auth_entities_map)
        return self

    @property
    def struct(self):
        # 返回结构化的授权信息
        authorizations = ObjectDict()
        authorizations.id = self.id
        authorizations.features = []
        authorizations.data = []

        for each in self.project_auth_entities_map.values():
            if each.resource.resource_type == ProjectsAuthsQuery.DATA:
                item = ObjectDict(dictize(self.ProjectAuthDataVO(each.resource, each.auth)))
                authorizations.data.append(item)
            if each.resource.resource_type == ProjectsAuthsQuery.FEATURE:
                item = ObjectDict(dictize(self.ProjectAuthFeatureVO(each.resource, each.auth)))
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
        existing = {key: value.auth.allow_method for key, value in self.project_auth_entities_map.items()}
        pending = {(self.id, resource.name, str(resource.locator)): ensure_method_as_int(auth.allow_method)
                   for (resource, auth) in resources_auths}
        union = set(pending).union(existing)
        to_delete = set(union).difference(pending)
        to_update = set(pending).intersection(existing)
        to_create = set(union).difference(existing)
        for key in to_delete:
            self.project_auth_entities_map[key](
                self.ProjectAuthEntity(self.id,
                                       Resource(*key),
                                       Auth(self.id, status=Auth.DELETE)))
        for key in to_update:
            self.project_auth_entities_map[key](
                self.ProjectAuthEntity(self.id,
                                       Resource(*key),
                                       Auth(self.id,
                                            status=Auth.ENABLED,
                                            allow_method=pending[key])))
        for key in to_create:
            self.project_auth_entities_map[key](
                self.ProjectAuthEntity(self.id,
                                       Resource(*key),
                                       Auth(self.id,
                                            status=Auth.ENABLED,
                                            allow_method=pending[key])))
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
        auth_entity = self.ProjectAuthEntity(self.id, resource, auth)
        self.project_auth_entities_map[(self.id, resource.name, resource.locator)] = auth_entity

    class ProjectAuthEntity(object):
        def __init__(self, project_id, resource, auth):
            """
            :param project_id: 
            :param resource: a instance of Resource 
            """
            self.id = project_id
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

    class ProjectAuthDataVO(object):

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

    class ProjectAuthFeatureVO(object):
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


class ProjectOverviewsDomain(object):
    """
    项目的基础信息聚合
    """

    def __init__(self, project_id=None, overviews=None):
        self._overviews = overviews
        self._project_id = project_id
        self.project_entity = None
        self.id = None

    def construct_entities(self):
        if self._overviews is None and self._project_id is None:
            raise Exception()
        if self._overviews and self._project_id is None:
            self.project_entity = self.ProjectOverviewsEntity(self._overviews)
        if self._overviews and self._project_id:
            self._overviews.update(id=self._project_id)
            self.project_entity = self.ProjectOverviewsEntity(self._overviews)
        if not self._overviews and self._project_id:
            q = ProjectOverviewsQuery().get_by_id(self._project_id).one()
            self.project_entity = self.ProjectOverviewsEntity(q)
        self.id = self.project_entity.id
        return self

    @property
    def struct(self):
        return ObjectDict(dictize(self.project_entity))

    def save(self):
        ProjectOverviewsRepository().persist(self.project_entity)
        return self

    def disable(self):
        self.project_entity.status = self.ProjectOverviewsEntity.DISABLED
        return self

    def enable(self):
        self.project_entity.status = self.ProjectOverviewsEntity.ENABLED
        return self

    def delete(self):
        self.project_entity.status = self.ProjectOverviewsEntity.DELETE
        return self

    class ProjectOverviewsEntity(object):
        ENABLED = 1
        DISABLED = 0
        DELETE = 2

        def __init__(self, overviews):
            """
            :param overviews: a instance of ObjectDict? 
            """
            self.id = overviews.get("id")
            self.name = overviews.get("name", "")
            self.mobile = overviews.get("mobile")
            self.create_time = overviews.get("create_time")
            self.description = overviews.get("description")
            self.status = overviews.get("status")
            self.validate()

        def validate(self):
            if not self.id:
                self.id = self._generate_id()
                self.create_time = int(time.time())
            if not self.status:
                self.status = self.ENABLED

        def _generate_id(self, max_retry=3):
            while max_retry > 0:
                while 1:
                    _id = "1" + generate_random_number(9)
                    if len(_id) == 10:
                        break
                if self.id_exists(_id):
                    max_retry -= 1
                else:
                    return _id
            raise Exception("_id Max Retries")

        @staticmethod
        def id_exists(_id):
            return ProjectOverviewsQuery().get_by_id(_id).exists()


class ProjectDomain(object):
    def __init__(self, Project_id=None, overviews=None, resources_auths=None):
        self.overviews = None
        self.authorizations = None
        self.id = None
        self.od = None
        self.ad = None
        self._id = Project_id
        self._overviews = overviews
        self._resources_auths = resources_auths

    def construct_entities(self):
        self.od = ProjectOverviewsDomain(self._id, self._overviews)
        self.overviews = self.od.construct_entities().struct
        self.id = self.overviews.id
        self.ad = ProjectAuthsDomain(self.id, self._resources_auths)
        self.authorizations = self.ad.construct_entities().struct
        return self

    @property
    def struct(self):
        Project = ObjectDict()
        Project.overviews = self.overviews
        Project.authorizations = self.authorizations
        Project.id = self.id
        return Project

    def save(self):
        self.od = self.od.save()
        self.ad = self.ad.save()
        return self


from bidong.common.utils import ObjectDict, get_dict_attribute, dictize
from bidong.core.exceptions import InvalidParametersError
from bidong.core.paginator import Paginator
from bidong.service.auth import (
    ProjectAuthsService,
    Auth,
    Resource
)
from bidong.service.account import (
    get_user_count_by_project,
    get_online_user_count_by_project
)
from bidong.service.ap import (
    get_ap_alert_count_by_project,
    get_project_ap_count
)
from bidong.service.v2.repo.ProjectsRepository import ProjectsRepo, ProjectRepo


class ProjectsService(object):
    def __init__(self, Project_id=None):
        self.repo = ProjectsRepo()
        self.Project_id = Project_id

    def integrated_create(self, overviews=None, authorizations=None):
        item = ObjectDict({})
        item.overviews = self.create_overviews(overviews)
        item.authorizations = self.create_authorizations(item.overviews.id, authorizations)
        item.id = item.overviews.id
        return item

    def create_overviews(self, overviews):
        overviews = self.repo.create(overviews)
        return overviews

    @staticmethod
    def create_authorizations(project_id, authorizations):
        auth_service = ProjectAuthsService(project_id)
        features = authorizations["features"]

        for feature in features:
            if "allow_method" not in feature.keys():
                feature["allow_method"] = ["DELETE", "PUT", "POST", "GET"]

        authorizations_parameters = [(Resource(feature["name"], ""), Auth(project_id, feature["allow_method"]))
                                     for feature in features]
        authorizations = auth_service.integrated_create_or_update(authorizations_parameters).list()
        return authorizations

    def get_details(self, page, per_page, sort="", order=""):
        payload = ObjectDict({})
        overviews = self.get_overviews(page, per_page, sort, order)
        content = []
        # 添加授权信息
        for overview in overviews.objects:
            item = ObjectDict({})
            item.authorizations = ProjectService(overview.id).get_authorizations()
            item.overviews = overview
            statistics = ObjectDict({})
            statistics.project_user_amount = get_user_count_by_project(overview.id)
            statistics.ap_alert_amount = get_ap_alert_count_by_project(overview.id)
            statistics.current_ap_amount = get_project_ap_count(overview.id)
            item.statistics = statistics
            item.id = item.overviews.id
            content.append(item)
        payload.update(overviews)
        payload.objects = content
        return payload

    def get_overviews(self, page, per_page, sort="", order=""):
        # rs = self.repo.exclude_deleted().all(page, per_page, sort, order)
        if self.Project_id:
            rs = self.repo.exclude_deleted().filter_by_Project_id(
                self.Project_id).all(page, per_page, sort, order)
        else:
            rs = self.repo.exclude_deleted().all(page, per_page, sort, order)
        return rs

    def get_fields(self, fields):
        payload = ObjectDict({"objects": []})
        overviews = self.get_overviews(0, 0)
        # 添加授权信息
        for overview in overviews.objects:
            item = ObjectDict({})
            item.authorizations = ProjectService(overview.id).get_authorizations()
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
        return payload


class ProjectService(object):
    def __init__(self, _id):
        self._id = _id
        self.repo = ProjectRepo(_id)

    def get_details(self):
        item = ObjectDict({})
        item.overviews = self.get_overviews()
        item.authorizations = self.get_authorizations()
        item.id = self._id
        return item

    def get_authorizations(self):
        auth_service = ProjectAuthsService(self._id)
        authorizations = auth_service.list()
        return authorizations

    def get_overviews(self):
        self.repo.get_by_pk()
        return self.repo.one()

    def get_brief(self):
        # 项目管理首页的项目概览
        item = self.get_details()
        payload = ObjectDict({})
        payload.update(item)
        payload.online_user_amount = get_online_user_count_by_project(self._id)
        payload.project_user_amount = get_user_count_by_project(self._id)
        payload.ap_alert_amount = get_ap_alert_count_by_project(self._id)
        payload.current_ap_amount = get_project_ap_count(self._id)
        return payload

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
        auth_service = ProjectAuthsService(self._id)
        features = authorizations["features"]

        for feature in features:
            if "allow_method" not in feature.keys():
                feature["allow_method"] = ["DELETE", "PUT", "POST", "GET"]

        authorizations_parameters = [(Resource(feature["name"], ""), Auth(self._id, feature["allow_method"]))
                                     for feature in features]
        authorizations = auth_service.integrated_create_or_update(authorizations_parameters).list()

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
        # TODO 删除项目时项目有关的管理员的权限也相应地删除，恢复时也是一样
        from bidong.service.auth import ManagerAuthsService


class ProjectsSearchService(object):
    def __init__(self, q, page, per_page):
        self.q = q.strip()
        self.page = page
        self.per_page = per_page

    def search(self):
        if self.q.isdigit():
            r = self.search_by_mobile()
        else:
            r = self.search_by_name()
            if not r.all():
                r = self.search_by_contact_name()

        res = ObjectDict(Paginator(r, self.page, self.per_page).to_dict())
        res.objects = [ObjectDict(dictize(each)) for each in res.objects]

        payload = ObjectDict({})
        content = []
        # 添加授权信息
        for overview in res.objects:
            item = ObjectDict({})
            item.authorizations = ProjectService(overview.id).get_authorizations()
            item.overviews = overview
            statistics = ObjectDict({})
            statistics.project_user_amount = get_user_count_by_project(overview.id)
            statistics.ap_alert_amount = get_ap_alert_count_by_project(overview.id)
            statistics.current_ap_amount = get_project_ap_count(overview.id)
            item.statistics = statistics
            item.id = item.overviews.id
            content.append(item)
        payload.update(res)
        payload.objects = content
        return payload

    def search_by_mobile(self):
        repo = ProjectsRepo()
        return repo.filter_by_mobile(int(self.q)).r

    def search_by_name(self):
        repo = ProjectsRepo()
        return repo.filter_by_name(str(self.q)).r

    def search_by_contact_name(self):
        repo = ProjectsRepo()
        return repo.filter_by_contact_name(str(self.q)).r
