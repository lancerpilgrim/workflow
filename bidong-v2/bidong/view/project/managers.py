from bidong.view.project import CollectionsHandler, IndividualsHandler
from bidong.service.executor import (
    ManagersService,
    ManagerService,
)
from bidong.service.project import ProjectAuthsService
from bidong.service.auth import ManagerAuthsService
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

    def get(self, project_id, *args, **kwargs):
        # TODO rpoject_id
        service = ManagersService()
        payload = service.get_details(self.page, self.per_page)
        payload = ManagersOutputSchema().dump(payload).data
        return self.response(payload=payload)

    def post(self, project_id, *args, **kwargs):
        parameters = validate_with_schema(ManagerInputSchema, self.request_body_dict)
        service = ManagersService()
        payload = service.integrated_create(overviews=parameters.overviews,
                                            authorizations=parameters.authorizations)
        payload = ManagerOutputSchema().dump(payload).data
        return self.response(payload=payload)


class ManagerHandler(IndividualsHandler):

    def get(self, project_id, manager_id, **kwargs):
        service = ManagerService(manager_id)
        payload = service.get_details()
        payload = ManagerOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, project_id, manager_id):
        parameters = validate_with_schema(ManagerInputSchema, self.request_body_dict)
        service = ManagerService(manager_id)
        payload = service.integrated_update(parameters.overviews, parameters.authorizations)
        payload = ManagerOutputSchema().dump(payload).data
        self.response(payload=payload)

    def delete(self, project_id, manager_id, *args, **kwargs):
        service = ManagerService(manager_id)
        service.delete()
        self.response()


class ManagerAuthorizationsHandler(CollectionsHandler):

    def get(self, project_id, manager_id):
        service = ManagerService(manager_id)
        payload = service.get_authorizations()
        payload = ManagerAuthorizationsOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, project_id, manager_id):
        self.request_body_dict.update({"id": manager_id})
        parameters = validate_with_schema(ManagerAuthorizationsInputSchema,
                                          self.request_body_dict)
        service = ManagerService(manager_id)
        payload = service.update_authorizations(parameters)
        payload = ManagerAuthorizationsOutputSchema().dump(payload).data
        self.response(payload=payload)


class ManagerOverviewsHandler(IndividualsHandler):

    def get(self, project_id, manager_id):
        service = ManagerService(manager_id)
        payload = service.get_overviews()
        payload = ManagerOverviewsOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, project_id, manager_id):
        parameters = validate_with_schema(ManagerOverviewsInputSchema, self.request_body_dict)
        service = ManagerService(manager_id)
        payload = service.update_overviews(parameters)
        payload = ManagerOverviewsOutputSchema().dump(payload).data
        self.response(payload=payload)


class ManagerProjectsHandler(IndividualsHandler):

    def get(self, manager_id):
        payload = ManagerAuthsService(manager_id).list_all_managed_projects()
        self.response(payload=payload)
