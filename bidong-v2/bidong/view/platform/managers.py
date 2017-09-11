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


class ManagersHandler(CollectionsHandler):

    def get(self, *args, **kwargs):
        # 搜索
        if self.q:
            service = ManagersSearchService(self.q, self.page, self.per_page)
            payload = service.search()
            return self.response(payload=payload)

        service = ManagersService()
        if self.fields:
            payload = service.get_fields(self.fields)
        else:
            payload = service.get_details(self.page, self.per_page)
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
