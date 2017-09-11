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
from bidong.service.v2.service.ServiceTools import get_downsized_collection


class AdministratorsQueryService(BaseCollectionService):
    def __init__(self):
        super(AdministratorsQueryService, self).__init__()
        self.id_collection = None

    def get_overviews(self):
        return self.get_domain(AdministratorOverviewsDomain)

    def get_combination(self):
        return self.get_domain(AdministratorDomain)

    def get_domain(self, domain):
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
        :return: 
        """
        payload = ObjectDict()
        collection = self.get_combination().objects
        payload.objects = get_downsized_collection(collection, fields)
        return payload


class AdministratorQueryService(BaseIndividualService):
    pass


class AdministratorCommandService(object):
    def __init__(self, administrator_id=None):
        self.id = administrator_id
        self.repo = AdministratorsRepo()

    def integrated_create(self, overviews=None, authorizations=None):
        item = ObjectDict({})
        item.overviews = self._create_overviews(overviews)
        item.authorizations = self._create_authorizations(authorizations)
        item.id = self.id
        # 初始化手机号密码登录
        from bidong.service.login import AdministratorPasswordLoginService
        ps = AdministratorPasswordLoginService(item.overviews.mobile)
        ps.init_user_login_info(item.id)

        return item

    def _create_overviews(self, overviews):
        overviews = self.repo.create(overviews)
        self.id = overviews.id
        return overviews

    def update_overviews(self, overviews=None):
        self.repo.get_by_pk()
        overviews = self.repo.update(overviews).one()
        return overviews

    def _create_authorizations(self, authorizations):
        auth_service = AdministratorAuthsService(self.id)
        authorizations_parameters = self._validate_auth_parameters(authorizations)
        return auth_service.integrated_create_or_update(authorizations_parameters).list()

    def update_authorizations(self, authorizations=None):
        auth_service = AdministratorAuthsService(self.id)
        authorizations_parameters = self._validate_auth_parameters(authorizations)
        return auth_service.integrated_create_or_update(authorizations_parameters).list()

    def integrated_update(self, overviews=None, authorizations=None):
        item = ObjectDict({})
        item.overviews = self.update_overviews(overviews)
        item.authorizations = self.update_authorizations(authorizations)
        item.id = item.overviews.id
        return item

    def _validate_auth_parameters(self, authorizations):
        features = authorizations["features"]
        for feature in features:
            if "allow_method" not in feature.keys():
                feature["allow_method"] = ["DELETE", "PUT", "POST", "GET"]
        authorizations_parameters = [(Resource(feature["name"], ""),
                                      Auth(self.id, feature["allow_method"]))
                                     for feature in features]
        return authorizations_parameters
