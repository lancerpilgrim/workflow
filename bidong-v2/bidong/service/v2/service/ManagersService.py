from bidong.common.utils import ObjectDict
from bidong.service.v2 import BaseEvent


class ManagersEvent(BaseEvent):

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
