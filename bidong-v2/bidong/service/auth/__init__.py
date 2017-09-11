# 类命名规则：复数表示对多条记录集合的操作，主要包括查询集，新建一个集合元素，乃至批量更新等；
#           单数表示对单条记录的操作，主要用于校验单个资源的权限，检验存在性，更新单个元素等等操作。

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from bidong.common.utils import ObjectDict
from bidong.service.account import get_online_user_count_by_project
from bidong.service.ap import get_project_ap_count
from ._repo import (
    ManagerAuthRepo,
    AdministratorAuthRepo,
    ManagerAuthsRepo,
    AdministratorAuthsRepo,
    ProjectAuthRepo,
    ProjectAuthsRepo,
    ResourceRepo,
    ResourcesRepo,
    Resource,
    Auth
)

#######################################################
# 资源名称对照表, 可以用中文名称去得到public_name, 反之亦然 #
#######################################################


def __map_resource_name():
    _ = {}
    __ = {}
    r = ResourcesRepo()
    all_resources = r.get_all_resources().all()
    for each in all_resources:
        if each.ascription == 1:
            _[each.private_name] = each.public_name
        elif each.ascription == 2:
            __[each.private_name] = each.public_name
    return _, __

PLATFORM_RESOURCES_MAP, CLIENT_RESOURCES_MAP = __map_resource_name()
REVERSED_PLATFORM_RESOURCES_MAP = {v: k for k, v in PLATFORM_RESOURCES_MAP.items()}
REVERSED_CLIENT_RESOURCES_MAP = {v: k for k, v in CLIENT_RESOURCES_MAP.items()}


###############
# 项目权限相关 #
###############


class ProjectAuthService(object):
    def __init__(self, project_id, resource):
        """
        :param project_id: 
        :param resource: a instance of resource 
        """
        self.project_id = project_id
        self.resource = resource
        self.repo = ProjectAuthRepo(project_id, self.resource)

    def check(self, method="GET"):
        try:
            auth = Auth(self.project_id, method)
            self.repo.locate()
            _ = self.repo.one()
        except (NoResultFound, MultipleResultsFound):
            return False
        else:
            method = _ensure_method_as_int(auth.allow_method)
            if method is None:
                raise Exception("Parameter Error")
            if method & _ensure_method_as_int(auth.allow_method) == method and auth.status:
                return True
            return False

    def get(self):
        self.repo.locate()
        return self.repo.one()

    def alter_allow_method(self, allow_method=None):
        """
        更新单条记录的可用方法
        :param allow_method: ["GET", "POST", "PUT", "DELETE"]的一个子集 或者int类型 
        :return: 
        """
        self.repo.locate()
        if not isinstance(allow_method, list):
            allow_method = _ensure_method_as_int(allow_method)
        return self.repo.update(allow_method=allow_method).one()

    def disable(self):
        self.repo.locate()
        return self.repo.disable().one()

    def enable(self):
        self.repo.locate()
        return self.repo.enable().one()

    def delete(self):
        self.repo.locate()
        return self.repo.delete().one()


class ProjectAuthsService(object):
    @classmethod
    def list_all_alternative_features(cls):
        repo = ResourcesRepo()
        payload = ObjectDict({})
        resources = repo.get_all_resources().filter_client().all()
        payload.features = []
        for each in resources:
            item = ObjectDict({})
            item.name = each.public_name
            item.description = each.description
            payload.features.append(item)
        return payload

    def __init__(self, project_id):
        self.project_id = project_id
        self.repo = ProjectAuthsRepo(project_id)

    def separate_create(self, resource, auth):
        """
        :param auth: instance of Auth
        :param resource: instance of Resource
        :return: 
        """
        resource_repo = ResourceRepo(resource.name)
        resource_repo.locate()
        r = resource_repo.one()
        # 组装资源对象
        resource = Resource(r.public_name, resource.locator, r.id)
        # 组装授权对象
        auth = Auth(self.project_id, allow_method=auth.method)
        # 创建新授权
        created_auth = self.repo.create(auth, resource)
        created_auth.id = self.project_id
        return created_auth

    def list(self):
        result = self.repo.list().filter_enabled().all()
        payload = self._assemble_payload(result)
        return payload

    def _assemble_payload(self, raw_auths_list):
        payload = ObjectDict({})
        payload.id = self.project_id
        payload.features = []

        for auth in raw_auths_list:
            feature = ObjectDict({})
            feature.name = auth.resource_name
            feature.description = REVERSED_CLIENT_RESOURCES_MAP[feature.name]
            feature.allow_method = _ensure_method_as_list(auth.allow_method)
            payload.features.append(feature)

        return payload

    def integrated_create_or_update(self, auths):
        """
        :brief 完整地重新定义项目的所有权限，不在auths列表中的原有权限都将被置为DELETE状态, 
               已经存在的将被更新，auths新增的权限将被创建
        :param auths: a nested list [(resource, auth), ....]
                      resource: a instance of Resource,
                      auth: a instance of Auth
        :return: 更新后的权限列表
        """
        result = self.repo.list().all()
        existing = {(r.resource_name, str(r.resource_locator)): r.allow_method for r in result}
        new = {(resource.name, str(resource.locator)): _ensure_method_as_int(auth.allow_method)
               for (resource, auth) in auths}
        union = set(new).union(existing)
        to_delete = set(union).difference(new)
        to_update = set(new).intersection(existing)
        to_create = set(union).difference(existing)
        for key in to_delete:
            service = ProjectAuthService(self.project_id, Resource(*key))
            service.delete()
        for key in to_update:
            service = ProjectAuthService(self.project_id, Resource(*key))
            service.alter_allow_method(new[key])
            service.enable()
        for key in to_create:
            self.separate_create(Resource(key[0], key[1]), Auth(self.project_id, allow_method=new[key]))
        return self


################
# 管理员权限相关 #
################


class AdministratorAuthService(object):
    def __init__(self, administrator_id, resource):
        """
        :param administrator_id: 
        :param resource: a instance of Resource 
        """
        self._id = administrator_id
        self.resource = resource
        self.repo = AdministratorAuthRepo(self._id, self.resource)

    def check(self, method="GET"):
        try:
            auth = Auth(self._id, method)
            self.repo.locate()
            _ = self.repo.one()
        except (NoResultFound, MultipleResultsFound):
            return False
        else:
            method = _ensure_method_as_int(auth.allow_method)
            if method is None:
                raise Exception("Parameter Error")
            if method & _ensure_method_as_int(auth.allow_method) == method and auth.status:
                return True
            return False

    def get(self):
        self.repo.locate()
        return self.repo.one()

    def alter_allow_method(self, allow_method=None):
        """
        更新单条记录的可用方法
        :param allow_method: ["GET", "POST", "PUT", "DELETE"]的一个子集 或者int类型 
        :return: 
        """
        self.repo.locate()
        if not isinstance(allow_method, list):
            allow_method = _ensure_method_as_int(allow_method)
        return self.repo.update(allow_method=allow_method).one()

    def disable(self):
        self.repo.locate()
        return self.repo.disable().one()

    def enable(self):
        self.repo.locate()
        return self.repo.enable().one()

    def delete(self):
        self.repo.locate()
        return self.repo.delete().one()


class ManagerAuthService(object):
    def __init__(self, manager_id, resource):
        """
        :param manager_id: 
        :param resource: a instance of Resource 
        """
        self._id = manager_id
        self.resource = resource
        self.repo = ManagerAuthRepo(self._id, self.resource)

    def check(self, method="GET"):
        try:
            auth = Auth(self._id, method)
            self.repo.locate()
            _ = self.repo.one()
        except (NoResultFound, MultipleResultsFound):
            return False
        else:
            method = _ensure_method_as_int(auth.allow_method)
            if method is None:
                raise Exception("Parameter Error")
            if method & _ensure_method_as_int(auth.allow_method) == method and auth.status:
                return True
            return False

    def get(self):
        self.repo.locate()
        return self.repo.one()

    def alter_allow_method(self, allow_method=None):
        """
        更新单条记录的可用方法
        :param allow_method: ["GET", "POST", "PUT", "DELETE"]的一个子集 或者int类型 
        :return: 
        """
        self.repo.locate()
        if not isinstance(allow_method, list):
            allow_method = _ensure_method_as_int(allow_method)
        return self.repo.update(allow_method=allow_method).one()

    def disable(self):
        self.repo.locate()
        return self.repo.disable().one()

    def enable(self):
        self.repo.locate()
        return self.repo.enable().one()

    def delete(self):
        self.repo.locate()
        return self.repo.delete().one()


class AdministratorAuthsService(object):

    @classmethod
    def list_all_alternative_features(cls):
        repo = ResourcesRepo()
        payload = ObjectDict({})
        resources = repo.get_all_resources().filter_platform().all()
        payload.features = []
        for each in resources:
            item = ObjectDict({})
            item.name = each.public_name
            item.description = each.private_name
            payload.features.append(item)
        return payload

    def __init__(self, administrator_id):
        self._id = administrator_id
        self.repo = AdministratorAuthsRepo(self._id)

    def integrated_create_or_update(self, auths):
        """
        :brief 完整地重新定义项目的所有权限，不在auths列表中的原有权限都将被置为DELETE状态, 
               已经存在的将被更新，auths新增的权限将被创建
        :param auths: a nested list [(resource, auth), ....]
                      resource: a instance of Resource,
                      auth: a instance of Auth
        :return: 更新后的权限列表
        """
        result = self.repo.list_all().all()
        existing = {(r.resource_name, str(r.resource_locator)): r.allow_method for r in result}
        new = {(resource.name, str(resource.locator)): _ensure_method_as_int(auth.allow_method)
               for (resource, auth) in auths}
        union = set(new).union(existing)
        to_delete = set(union).difference(new)
        to_update = set(new).intersection(existing)
        to_create = set(union).difference(existing)
        for key in to_delete:
            service = AdministratorAuthService(self._id, Resource(*key))
            service.delete()
        for key in to_update:
            service = AdministratorAuthService(self._id, Resource(*key))
            service.alter_allow_method(new[key])
            service.enable()
        for key in to_create:
            self.separate_create(Resource(*key), Auth(self._id, allow_method=new[key]))

        return self

    def separate_create(self, resource, auth):
        """
        :param auth: instance of Auth
        :param resource: instance of Resource
        :return: 
        """
        resource_repo = ResourceRepo(resource.name)
        resource_repo.locate()
        r = resource_repo.one()
        # 组装资源对象
        resource = Resource(r.public_name, resource.locator, r.id)
        # 创建新授权
        created_auth = self.repo.create(auth, resource)
        created_auth.id = self._id
        return created_auth

    def _assemble_payload(self, raw_auths_list):
        payload = ObjectDict({})
        payload.id = self._id
        payload.features = []

        for auth in raw_auths_list:
            feature = ObjectDict({})
            feature.name = auth.resource_name
            feature.allow_method = _ensure_method_as_list(auth.allow_method)
            feature.description = REVERSED_PLATFORM_RESOURCES_MAP[feature.name]
            payload.features.append(feature)

        return payload

    @staticmethod
    def _assemble_features(raw_auths_list):
        features = []
        for auth in raw_auths_list:
            feature = ObjectDict({})
            feature.name = auth.resource_name
            feature.allow_method = _ensure_method_as_list(auth.allow_method)
            feature.description = REVERSED_PLATFORM_RESOURCES_MAP[feature.name]
            features.append(feature)
        return features

    @staticmethod
    def _assemble_data(raw_auths_list):
        data = []
        for auth in raw_auths_list:
            datum = ObjectDict({})
            datum.name = auth.resource_name
            datum.allow_method = _ensure_method_as_list(auth.allow_method)
            datum.description = REVERSED_PLATFORM_RESOURCES_MAP[datum.name]
            datum.data_id = auth.resource_locator
            data.append(datum)
        return data

    def list(self):
        payload = ObjectDict()
        payload.id = self._id
        features = self._assemble_features(self.repo.list_features().filter_enabled().all())
        data = self._assemble_data(self.repo.list_data().filter_enabled().all())
        payload.features = features
        payload.data = data
        return payload


class ManagerAuthsService(object):

    @classmethod
    def list_all_alternative_features(cls):
        # TODO 只能選取該管理員所屬項目的權限
        repo = ResourcesRepo()
        payload = ObjectDict({})
        resources = repo.get_all_resources().filter_client().all()
        payload.features = []
        for each in resources:
            item = ObjectDict({})
            item.name = each.public_name
            item.description = each.description
            payload.features.append(item)
        return payload

    def __init__(self, manager_id):
        self._id = manager_id
        self.repo = ManagerAuthsRepo(self._id)

    def list_all_managed_projects(self):
        payload = ObjectDict({})
        result = self.repo.list_projects().all()
        payload.projects = []
        for each in result:
            item = ObjectDict({})
            item.id = each.id
            item.name = each.name
            item.create_time = each.create_time
            item.contact = each.contact
            item.online_user_amount = get_online_user_count_by_project(self._id)
            item.fault_ap_amount = get_project_ap_count(self._id, status=0)
            item.online_ap_amount = get_project_ap_count(self._id, status=1)
            payload.projects.append(item)
        return payload

    def integrated_create_or_update(self, auths):
        """
        :brief 完整地重新定义项目的所有权限，不在auths列表中的原有权限都将被置为DELETE状态, 
               已经存在的将被更新，auths新增的权限将被创建
        :param auths: a nested list [(resource, auth), ....]
                      resource: a instance of Resource,
                      auth: a instance of Auth
        :return: 更新后的权限列表
        """
        result = self.repo.list_features().all()
        existing = {(r.resource_name, str(r.resource_locator)): r.allow_method for r in result}
        new = {(resource.name, str(resource.locator)): _ensure_method_as_int(auth.allow_method)
               for (resource, auth) in auths}
        union = set(new).union(existing)
        to_delete = set(union).difference(new)
        to_update = set(new).intersection(existing)
        to_create = set(union).difference(existing)
        print("create")
        print(to_create)
        print("update")
        print(to_update)
        print("delete")
        print(to_delete)
        for key in to_delete:
            service = ManagerAuthService(self._id, Resource(*key))
            service.delete()
        for key in to_update:
            # 只有发生变更的才执行更新
            service = ManagerAuthService(self._id, Resource(*key))
            # if new[key] != existing[key]:
            service.alter_allow_method(new[key])
            service.enable()
        for key in to_create:
            self.separate_create(Resource(*key), Auth(self._id, allow_method=new[key]))

        return self

    def separate_create(self, resource, auth):
        """
        :param auth: instance of Auth
        :param resource: instance of Resource
        :return: 
        """
        resource_repo = ResourceRepo(resource.name)
        resource_repo.locate()
        r = resource_repo.one()
        # 组装资源对象
        resource = Resource(r.public_name, resource.locator, r.id)
        # 组装授权对象
        auth = Auth(self._id, allow_method=auth.allow_method)
        # 创建新授权
        created_auth = self.repo.create(auth, resource)
        created_auth.id = self._id
        return created_auth

    def _assemble_collection_payload(self, raw_auths_list):
        payload = ObjectDict({})
        payload.contents = []
        payload.id = self._id

        projects = ObjectDict({int(r.resource_locator): ObjectDict({"project_id": int(r.resource_locator),
                                                                    "features": []})
                               for r in raw_auths_list})
        for auth in raw_auths_list:
            feature = ObjectDict({"allow_method": _ensure_method_as_list(auth.allow_method),
                                  "name": auth.resource_name,
                                  "description": REVERSED_CLIENT_RESOURCES_MAP[auth.resource_name]})
            projects[int(auth.resource_locator)].features.append(feature)
        from bidong.service.project import ProjectService
        for each in projects.keys():
            s = ProjectService(projects[each].project_id)
            projects[each].project_name = s.get_overviews().name
            # TODO 調用service查詢項目名, 這裡在現在情形下大約有10ms性能損失，將來可能改進
        payload.contents = list(projects.values())
        return payload

    def _assemble_individual_payload(self, raw_auths):
        payload = ObjectDict({})
        payload.features = []
        for auth in raw_auths:
            feature = ObjectDict({"allow_method": _ensure_method_as_list(auth.allow_method),
                                  "name": auth.resource_name,
                                  "description": REVERSED_CLIENT_RESOURCES_MAP[auth.resource_name]})
            payload.features.append(feature)
        payload.id = self._id
        return payload

    def list(self):
        result = self.repo.list_features().filter_enabled().all()
        payload = self._assemble_collection_payload(result)
        return payload

    def get(self, project_id):
        result = self.repo.list_features().filter_project(project_id).filter_enabled().all()
        payload = self._assemble_individual_payload(result)
        return payload


###############
# 辅助类和方法 #
###############


class Operator:
    GET = "8"
    POST = "4"
    PUT = "2"
    DELETE = "1"


def _method_int_convert(method_or_int):
    method_or_int = str(method_or_int)
    if method_or_int == Operator.GET:
        return "GET"
    elif method_or_int == Operator.DELETE:
        return "DELETE"
    elif method_or_int == Operator.POST:
        return "POST"
    elif method_or_int == Operator.PUT:
        return "PUT"
    elif method_or_int == "GET":
        return Operator.GET
    elif method_or_int == "POST":
        return Operator.POST
    elif method_or_int == "PUT":
        return Operator.PUT
    elif method_or_int == "DELETE":
        return Operator.DELETE
    else:
        return None


def _ensure_method_as_int(methods):
    result = 0
    if isinstance(methods, str):
        return int(_method_int_convert(methods))
    elif isinstance(methods, int):
        return methods
    for method in methods:
        result += int(_method_int_convert(method))
    return result


def _ensure_method_as_list(method):
    result = []
    if isinstance(method, str):
        method = _method_int_convert(method)
    for each in [1, 2, 4, 8]:
        if each & method == each:
            result.append(_method_int_convert(each))
    return result
