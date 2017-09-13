from bidong.common.utils import ObjectDict
from bidong.service.v2.service import BaseCollectionService, BaseIndividualService
from bidong.service.v2.service.ServiceTools import get_downsized_collection, get_downsized_dict
from bidong.service.v2.domain.ManagersDomain import (
    ManagerOverviewsDomain,
    ManagerAuthsDomain,
    ManagerDomain
)
from bidong.service.v2.domain.ValueObjects import Resource, Auth
from bidong.service.v2.repo.ManagersRepository import (
    ManagersOverviewsQuery,
    ManagersQuery
)


class ManagersQueryService(BaseCollectionService):
    def __init__(self, project_id=None):
        super(ManagersQueryService, self).__init__()
        self._project_id = project_id
        self.id_collection = None

    def get_overviews(self):
        payload = ObjectDict()
        # 基础信息与project无关
        rs, pagination = ManagersQuery().exclude_deleted().paginate(self.paginator).all()
        self.id_collection = rs.keys()
        payload.objects = [ManagerOverviewsDomain(manager_id=_id,
                                                  overviews=rs[_id]).construct_entities().struct
                           for _id in self.id_collection]
        payload.update(pagination)
        return payload

    def get_combination(self):
        payload = ObjectDict()
        # 当做一个整体查询时,需要针对project做筛选
        rs, pagination = ManagersQuery().exclude_deleted().\
            filter_by_project(self._project_id).paginate(self.paginator).all()
        self.id_collection = rs.keys()
        payload.objects = [ManagerDomain(manager_id=_id,
                                         overviews=rs[_id],
                                         project_id=self._project_id).construct_entities().struct
                           for _id in self.id_collection]
        payload.update(pagination)
        return payload

    def get_fields(self, fields):
        """
        :brief 根据fields获得相应字段
        :param fields: 各个字段之间用半角逗号','隔开,字段内部用半角'.'隔开,表示层级.
        　　　　　　　　　比如fields="id,authorizations.features" 则返回dict(objects=dict(id=1, features=[]))
        :return: a collection of objects with attrs referred in fields
        """
        payload = ObjectDict()
        payload.objects = get_downsized_collection(self.get_combination().objects, fields)
        return payload


class ManagerQueryService(BaseIndividualService):
    def __init__(self, manager_id):
        super(ManagerQueryService, self).__init__()
        self.id = manager_id

    def get_overviews(self):
        return self.get_domain_payload(ManagerOverviewsDomain)

    def get_authorizations(self):
        return self.get_domain_payload(ManagerAuthsDomain)

    def get_combination(self):
        return self.get_domain_payload(ManagerDomain)

    def get_domain_payload(self, domain):
        return domain(manager_id=self.id).construct_entities().ensure_existence().struct

    def get_fields(self, fields):
        return get_downsized_dict(self.get_combination(), fields)


class ManagerCommandService(object):
    def __init__(self, manager_id=None, overviews=None, authorizations=None):
        self.id = manager_id
        self.overviews = overviews
        self.authorizations = authorizations

    def integrated_create(self):
        resources_auths = self._format_authorizations_parameter()
        domain = ManagerDomain(overviews=self.overviews,
                               resources_auths=resources_auths).construct_entities()
        domain.save()
        payload = domain.struct

        # 初始化手机号密码登录
        from bidong.service.login import ManagerPasswordLoginService
        ps = ManagerPasswordLoginService(payload.overviews.mobile)
        ps.init_user_login_info(payload.id)

        return payload

    def integrated_update(self):
        resources_auths = self._format_authorizations_parameter()
        domain = ManagerDomain(manager_id=self.id,
                               overviews=self.overviews,
                               resources_auths=resources_auths).construct_entities()
        domain.save()
        return domain.struct

    def update_overviews(self):
        domain = ManagerOverviewsDomain(manager_id=self.id,
                                        overviews=self.overviews).construct_entities()
        domain.save()
        return domain.struct

    def update_authorizations(self):
        resources_auths = self._format_authorizations_parameter()
        domain = ManagerAuthsDomain(manager_id=self.id,
                                    resources_auths=resources_auths).construct_entities()
        domain.save()
        return domain.struct

    def delete(self):
        domain = ManagerOverviewsDomain(manager_id=self.id).construct_entities()
        domain.delete()
        domain.save()

    def _format_authorizations_parameter(self):
        parameters = []
        contents = self.authorizations.get("contents")
        for content in contents:
            features = content.get("features", [])
            data = content.get("data", [])
            for feature in features:
                if "allow_method" not in feature.keys():
                    feature["allow_method"] = ["DELETE", "PUT", "POST", "GET"]
            for datum in data:
                if "allow_method" not in datum.keys():
                    datum["allow_method"] = ["DELETE", "PUT", "POST", "GET"]
            feature_parameters = [(Resource(feature["name"], content.get("project_id")),
                                   Auth(self.id, feature["allow_method"]))
                                  for feature in features]
            data_parameters = [(Resource(datum["name"], datum.get("data_id")),
                                Auth(self.id, datum["allow_method"]))
                               for datum in data]
            parameters.extend(feature_parameters)
            parameters.extend(data_parameters)
        print(parameters)
        return parameters
