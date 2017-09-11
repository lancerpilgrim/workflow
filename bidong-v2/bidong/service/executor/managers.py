from ._repo import (
    ManagerRepo,
    ManagersRepo
)
from bidong.service.auth import (
    ManagerAuthsService,
    Resource,
    Auth
)
from bidong.common.utils import ObjectDict, get_dict_attribute, dictize
from bidong.core.exceptions import InvalidParametersError
from bidong.core.paginator import Paginator


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
        authorizations = auth_service.integrated_create_or_update(authorizations_parameters).list()
        return authorizations

    def get_details(self, page, per_page, sort="", order=""):
        payload = ObjectDict({})
        overviews = self.get_overviews(page, per_page, sort, order)
        content = []
        # 添加授权信息
        for overview in overviews.objects:
            item = ObjectDict({})
            try:
                item.authorizations = ManagerService(overview.id).get_authorizations()
            except Exception as e:
                print(overview)
                print(e)
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
        return payload

    def get_overviews(self, page, per_page, sort="", order=""):
        return self.repo.exclude_deleted().all(page, per_page, sort, order)


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

    def get_authorizations_by_project_id(self, project_id):
        payload = ManagerAuthsService(self._id).get(project_id)
        return payload

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


class ManagersSearchService(object):

    def __init__(self, q, page, per_page):
        self.q = q.strip()
        self.page = page
        self.per_page = per_page

    def search(self):
        if self.q.isdigit():
            r = self.search_by_mobile()
        else:
            r = self.search_by_name()

        res = ObjectDict(Paginator(r, self.page, self.per_page).to_dict())
        res.objects = [ObjectDict(dictize(each)) for each in res.objects]

        payload = ObjectDict({})
        content = []
        # 添加授权信息
        for overview in res.objects:
            item = ObjectDict({})
            item.authorizations = ManagerService(overview.id).get_authorizations()
            item.overviews = overview
            item.id = item.overviews.id
            content.append(item)
        payload.update(res)
        payload.objects = content
        return payload

    def search_by_mobile(self):
        repo = ManagersRepo()
        return repo.filter_by_mobile(int(self.q)).r

    def search_by_name(self):
        repo = ManagersRepo()
        return repo.filter_by_name(str(self.q)).r


