from bidong.view.project import IndividualsHandler
from bidong.service.project import ProjectService
from bidong.view.schemas.project import (
    ProjectOverviewsSchema,
    ProjectOverviewsInputSchema,
    ProjectAuthorizationSchema,
    ProjectInputSchema,
    ProjectOutputSchema
)
from bidong.core.validates import validate_with_schema


class ProjectHandler(IndividualsHandler):
    def get(self, project_id, **kwargs):
        service = ProjectService(project_id)
        payload = service.get_details()
        payload = ProjectOutputSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, project_id):
        parameters = validate_with_schema(ProjectInputSchema, self.request_body_dict)
        service = ProjectService(project_id)
        payload = service.integrated_update(parameters.overviews, parameters.authorizations)
        self.response(payload=payload)

    def delete(self, project_id, *args, **kwargs):
        service = ProjectService(project_id)
        service.delete()
        self.response()


class ProjectAuthorizationHandler(IndividualsHandler):

    def get(self, project_id):
        service = ProjectService(project_id)
        payload = service.get_authorizations()
        payload = ProjectAuthorizationSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, project_id):
        self.request_body_dict.update({"id": project_id})
        parameters = validate_with_schema(ProjectAuthorizationSchema,
                                          self.request_body_dict)
        service = ProjectService(project_id)
        payload = service.update_authorizations(parameters)
        payload = ProjectAuthorizationSchema().dump(payload).data
        self.response(payload=payload)


class ProjectOverviewHandler(IndividualsHandler):

    def get(self, project_id):
        service = ProjectService(project_id)
        payload = service.get_overviews()
        payload = ProjectOverviewsSchema().dump(payload).data
        self.response(payload=payload)

    def put(self, project_id):
        parameters = validate_with_schema(ProjectOverviewsInputSchema, self.request_body_dict)
        service = ProjectService(project_id)
        payload = service.update_overviews(parameters)
        payload = ProjectOverviewsSchema().dump(payload).data
        self.response(payload=payload)


class ProjectBriefHandler(IndividualsHandler):

    def get(self, project_id):
        service = ProjectService(project_id)
        payload = service.get_brief()
        # payload = ProjectOverviewsSchema().dump(payload).data
        self.response(payload=payload)
