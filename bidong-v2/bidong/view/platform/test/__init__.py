from bidong.core.validates import validate_with_schema
from bidong.service.auth import AdministratorAuthsService
from bidong.service.executor import (
    AdministratorsService,
    AdministratorService,
    AdministratorsSearchService
)
from bidong.view.platform import (
    CollectionsHandler,
    IndividualsHandler
)
from bidong.view.schemas.executor import (
    AdministratorOverviewsOutputSchema,
    AdministratorOverviewsInputSchema,
    AdministratorAuthorizationsInputSchema,
    AdministratorAuthorizationsOutputSchema,
    AdministratorInputSchema,
    AdministratorOutputSchema,
    AdministratorsOutputSchema
)
from bidong.service.v2.service.AdministratorsService import (
    AdministratorsQueryService,
    AdministratorQueryService,
    AdministratorCommandService
)

from bidong.view.platform import CollectionsHandler, IndividualsHandler
from bidong.service.executor import (
    ManagersService,
    ManagerService,
    ManagersSearchService
)
from bidong.view.schemas.executor import (
    ManagerOverviewsOutputSchema,
    ManagerOverviewsInputSchema,
    ManagerAuthorizationsInputSchema,
    ManagerAuthorizationsOutputSchema,
    ManagerInputSchema,
    ManagerOutputSchema,
    ManagersOutputSchema
)
from bidong.core.validates import validate_with_schema
from bidong.service.v2.service.ManagersService import (
    ManagersQueryService,
    ManagerQueryService,
    ManagerCommandService
)


class AdministratorsHandler(CollectionsHandler):
    def get(self, *args, **kwargs):
        # 搜索
        if self.q:
            service = AdministratorsSearchService(self.q, self.page, self.per_page)
            payload = service.search()
            return self.response(payload=payload)
        # 获取
        service = AdministratorsQueryService()
        if self.fields:
            payload = service.get_fields(self.fields)
        else:
            service = service.paginate(self.page, self.per_page)
            payload = service.get_combination()
            payload = AdministratorsOutputSchema().dump(payload).data
        return self.response(payload=payload)

    def post(self, *args, **kwargs):
        parameters = validate_with_schema(AdministratorInputSchema, self.request_body_dict)
        service = AdministratorCommandService(overviews=parameters.overviews,
                                              authorizations=parameters.authorizations)
        payload = service.integrated_create()
        payload = AdministratorOutputSchema().dump(payload).data
        return self.response(payload=payload)


class AdministratorHandler(IndividualsHandler):
    def get(self, administrator_id, **kwargs):
        service = AdministratorQueryService(administrator_id)
        payload = service.get_combination()
        payload = AdministratorOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, administrator_id):
        parameters = validate_with_schema(AdministratorInputSchema, self.request_body_dict)
        service = AdministratorCommandService(administrator_id=administrator_id,
                                              overviews=parameters.overviews,
                                              authorizations=parameters.authorizations)
        payload = service.integrated_update()
        payload = AdministratorOutputSchema().dump(payload).data
        self.response(payload=payload)

    def delete(self, administrator_id, *args, **kwargs):
        service = AdministratorCommandService(administrator_id)
        service.delete()
        self.response()


class AdministratorAuthorizationsHandler(CollectionsHandler):
    def get(self, administrator_id):
        service = AdministratorQueryService(administrator_id)
        payload = service.get_authorizations()
        payload = AdministratorAuthorizationsOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, administrator_id):
        self.request_body_dict.update({"id": administrator_id})
        parameters = validate_with_schema(AdministratorAuthorizationsInputSchema,
                                          self.request_body_dict)
        print(parameters)
        service = AdministratorCommandService(administrator_id=administrator_id,
                                              authorizations=parameters)
        payload = service.update_authorizations()
        payload = AdministratorAuthorizationsOutputSchema().dump(payload).data
        self.response(payload=payload)


class AdministratorOverviewsHandler(IndividualsHandler):
    def get(self, administrator_id):
        service = AdministratorQueryService(administrator_id)
        payload = service.get_overviews()
        payload = AdministratorOverviewsOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, administrator_id):
        parameters = validate_with_schema(AdministratorOverviewsInputSchema, self.request_body_dict)
        service = AdministratorCommandService(administrator_id=administrator_id,
                                              overviews=parameters)
        payload = service.update_overviews()
        payload = AdministratorOverviewsOutputSchema().dump(payload).data
        self.response(payload=payload)


class AdministratorsFeaturesHandler(IndividualsHandler):
    def get(self):
        payload = AdministratorAuthsService.list_all_alternative_features()
        self.response(payload=payload)


class ManagersHandler(CollectionsHandler):

    def get(self, *args, **kwargs):
        # 搜索
        if self.q:
            service = ManagersSearchService(self.q, self.page, self.per_page)
            payload = service.search()
            return self.response(payload=payload)

        service = ManagersQueryService()
        if self.fields:
            payload = service.get_fields(self.fields)
        else:
            service = service.paginate(self.page, self.per_page)
            payload = service.get_combination()
            payload = ManagersOutputSchema().dump(payload).data
        return self.response(payload=payload)

    def post(self, *args, **kwargs):
        parameters = validate_with_schema(ManagerInputSchema, self.request_body_dict)
        service = ManagersService()
        payload = service.integrated_create(overviews=parameters.overviews,
                                            authorizations=parameters.authorizations)
        payload = ManagerOutputSchema().dump(payload).data
        return self.response(payload=payload)


class ManagerHandler(IndividualsHandler):

    def get(self, manager_id, **kwargs):
        service = ManagerService(manager_id)
        payload = service.get_details()
        payload = ManagerOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, manager_id):
        parameters = validate_with_schema(ManagerInputSchema, self.request_body_dict)
        service = ManagerService(manager_id)
        payload = service.integrated_update(parameters.overviews, parameters.authorizations)
        payload = ManagerOutputSchema().dump(payload).data
        self.response(payload=payload)

    def delete(self, manager_id, *args, **kwargs):
        service = ManagerService(manager_id)
        service.delete()
        self.response()


class ManagerAuthorizationsHandler(CollectionsHandler):

    def get(self, manager_id):
        service = ManagerService(manager_id)
        payload = service.get_authorizations()
        payload = ManagerAuthorizationsOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, manager_id):
        self.request_body_dict.update({"id": manager_id})
        parameters = validate_with_schema(ManagerAuthorizationsInputSchema,
                                          self.request_body_dict)
        service = ManagerService(manager_id)
        payload = service.update_authorizations(parameters)
        payload = ManagerAuthorizationsOutputSchema().dump(payload).data
        self.response(payload=payload)


class ManagerOverviewsHandler(IndividualsHandler):

    def get(self, manager_id):
        service = ManagerService(manager_id)
        payload = service.get_overviews()
        payload = ManagerOverviewsOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, manager_id):
        parameters = validate_with_schema(ManagerOverviewsInputSchema, self.request_body_dict)
        service = ManagerService(manager_id)
        payload = service.update_overviews(parameters)
        payload = ManagerOverviewsOutputSchema().dump(payload).data
        self.response(payload=payload)