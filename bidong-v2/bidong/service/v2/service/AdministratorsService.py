from bidong.service.v2.domain.AdministratorsDomain import AdministratorAuthsDomain, AdministratorOverviewsDomain
from bidong.service.v2.domain.ValueObjects import Resource, Auth
from bidong.service.auth import AdministratorAuthsService
from bidong.common.utils import ObjectDict
from bidong.service.executor._repo import AdministratorsRepo
from bidong.service.v2.service import BaseCollectionService, BaseIndividualService
from bidong.service.v2.repo.AdministratorsRepository import AdministratorsOverviewsQuery
from bidong.service.v2.domain.AdministratorsDomain import AdministratorAuthsDomain
from bidong.common.utils import get_dict_attribute
from bidong.core.exceptions import InvalidParametersError
from bidong.service.v2.domain.AdministratorsDomain import AdministratorDomain
from bidong.service.v2.service.ServiceTools import get_downsized_collection, get_downsized_dict


class AdministratorsQueryService(BaseCollectionService):
    def __init__(self):
        super(AdministratorsQueryService, self).__init__()
        self.id_collection = None

    def get_overviews(self):
        return self.get_domain_payload(AdministratorOverviewsDomain)

    def get_combination(self):
        return self.get_domain_payload(AdministratorDomain)

    def get_domain_payload(self, domain):
        payload = ObjectDict()
        rs, pagination = AdministratorsOverviewsQuery().exclude_deleted().paginate(self.paginator).all()
        self.id_collection = rs.keys()
        payload.objects = [domain(administrator_id=_id,
                                  overviews=rs[_id]).construct_entities().struct
                           for _id in self.id_collection]
        payload.update(pagination)
        return payload

    def get_fields(self, fields):
        """
        :brief 根据fields获得相应字段
        :param fields: 各个字段之间用半角逗号','隔开,字段内部用半角'.'隔开,表示层级.
        　　　　　　　　　比如fields="id,authorizations.features" 则返回{"objects": {
                                                                                "id": 1,
                                                                                "features": ["features"]    
                                                                                }
                                                                    }
        :return: a collection of objects with attrs referred in fields
        """
        payload = ObjectDict()
        collection, pagination = self.get_combination()
        payload.objects = get_downsized_collection(collection, fields)
        return payload


class AdministratorQueryService(BaseIndividualService):

    def __init__(self, administrator_id):
        super(AdministratorQueryService, self).__init__()
        self.id = administrator_id

    def get_overviews(self):
        return self.get_domain_payload(AdministratorOverviewsDomain)

    def get_authorizations(self):
        return self.get_domain_payload(AdministratorAuthsDomain)

    def get_combination(self):
        return self.get_domain_payload(AdministratorDomain)

    def get_domain_payload(self, domain):
        return domain(administrator_id=self.id).construct_entities().struct

    def get_fields(self, fields):
        return get_downsized_dict(self.get_combination(), fields)


class AdministratorCommandService(object):
    def __init__(self, administrator_id=None, overviews=None, authorizations=None):
        self.id = administrator_id
        self.overviews = overviews
        self.authorizations = authorizations
        print(authorizations)

    def integrated_create(self):
        resources_auths = self._format_authorizations_parameter()
        domain = AdministratorDomain(overviews=self.overviews,
                                     resources_auths=resources_auths).construct_entities()
        domain.save()
        payload = domain.struct

        # 初始化手机号密码登录
        from bidong.service.login import AdministratorPasswordLoginService
        ps = AdministratorPasswordLoginService(payload.overviews.mobile)
        ps.init_user_login_info(payload.id)

        return payload

    def integrated_update(self):
        resources_auths = self._format_authorizations_parameter()
        domain = AdministratorDomain(administrator_id=self.id,
                                     overviews=self.overviews,
                                     resources_auths=resources_auths).construct_entities()
        domain.save()
        return domain.struct

    def update_overviews(self):
        domain = AdministratorOverviewsDomain(administrator_id=self.id,
                                              overviews=self.overviews).construct_entities()
        domain.save()
        return domain.struct

    def update_authorizations(self):
        resources_auths = self._format_authorizations_parameter()
        domain = AdministratorAuthsDomain(administrator_id=self.id,
                                          resources_auths=resources_auths).construct_entities()
        domain.save()
        return domain.struct

    def delete(self):
        domain = AdministratorOverviewsDomain(administrator_id=self.id).construct_entities()
        domain.delete()
        domain.save()

    def _format_authorizations_parameter(self):
        features = self.authorizations.get("features", None)
        data = self.authorizations.get("data", None)
        parameters = []
        for feature in features:
            if "allow_method" not in feature.keys():
                feature["allow_method"] = ["DELETE", "PUT", "POST", "GET"]
        for datum in data:
            if "allow_method" not in datum.keys():
                datum["allow_method"] = ["DELETE", "PUT", "POST", "GET"]
        feature_parameters = [(Resource(feature["name"], ""), Auth(self.id, feature["allow_method"]))
                              for feature in features]
        data_parameters = [(Resource(datum["name"], datum.get("data_id")), Auth(self.id, datum["allow_method"]))
                           for datum in data]
        parameters.extend(feature_parameters)
        parameters.extend(data_parameters)
        return parameters
