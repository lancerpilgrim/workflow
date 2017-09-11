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
from ._repo import ProjectsRepo, ProjectRepo


class ProjectsService(object):
    def __init__(self, administrator_id=None):
        self.repo = ProjectsRepo()
        self.administrator_id = administrator_id

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
        if self.administrator_id:
            rs = self.repo.exclude_deleted().filter_by_administrator_id(
                self.administrator_id).all(page, per_page, sort, order)
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


