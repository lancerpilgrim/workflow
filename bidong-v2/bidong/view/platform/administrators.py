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


class AdministratorsHandler(CollectionsHandler):

    def get(self, *args, **kwargs):
        # 搜索
        if self.q:
            service = AdministratorsSearchService(self.q, self.page, self.per_page)
            payload = service.search()
            return self.response(payload=payload)

        service = AdministratorsService()
        if self.fields:
            payload = service.get_fields(self.fields)
        else:
            payload = service.get_details(self.page, self.per_page)
            payload = AdministratorsOutputSchema().dump(payload).data
        return self.response(payload=payload)

    def post(self, *args, **kwargs):
        parameters = validate_with_schema(AdministratorInputSchema, self.request_body_dict)
        service = AdministratorsService()
        payload = service.integrated_create(overviews=parameters.overviews,
                                            authorizations=parameters.authorizations)
        payload = AdministratorOutputSchema().dump(payload).data
        return self.response(payload=payload)


class AdministratorHandler(IndividualsHandler):

    def get(self, administrator_id, **kwargs):
        service = AdministratorService(administrator_id)
        payload = service.get_details()
        payload = AdministratorOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, administrator_id):
        parameters = validate_with_schema(AdministratorInputSchema, self.request_body_dict)
        service = AdministratorService(administrator_id)
        payload = service.integrated_update(parameters.overviews, parameters.authorizations)
        payload = AdministratorOutputSchema().dump(payload).data
        self.response(payload=payload)

    def delete(self, administrator_id, *args, **kwargs):
        service = AdministratorService(administrator_id)
        service.delete()
        self.response()


class AdministratorAuthorizationsHandler(CollectionsHandler):

    def get(self, administrator_id):
        service = AdministratorService(administrator_id)
        payload = service.get_authorizations()
        payload = AdministratorAuthorizationsOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, administrator_id):
        self.request_body_dict.update({"id": administrator_id})
        parameters = validate_with_schema(AdministratorAuthorizationsInputSchema,
                                          self.request_body_dict)
        service = AdministratorService(administrator_id)
        payload = service.update_authorizations(parameters)
        payload = AdministratorAuthorizationsOutputSchema().dump(payload).data
        self.response(payload=payload)


class AdministratorOverviewsHandler(IndividualsHandler):

    def get(self, administrator_id):
        service = AdministratorService(administrator_id)
        payload = service.get_overviews()
        payload = AdministratorOverviewsOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, administrator_id):
        parameters = validate_with_schema(AdministratorOverviewsInputSchema, self.request_body_dict)
        service = AdministratorService(administrator_id)
        payload = service.update_overviews(parameters)
        payload = AdministratorOverviewsOutputSchema().dump(payload).data
        self.response(payload=payload)


class AdministratorsFeaturesHandler(IndividualsHandler):

    def get(self):
        payload = AdministratorAuthsService.list_all_alternative_features()
        self.response(payload=payload)
