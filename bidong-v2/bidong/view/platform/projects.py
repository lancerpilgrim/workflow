from bidong.view.platform import (
    CollectionsHandler,
    IndividualsHandler
)
from bidong.core.validates import validate_with_schema
from bidong.core.exceptions import UnAuthorizedError
from bidong.service.project import (
    ProjectService,
    ProjectsService,
    ProjectsSearchService
)
from bidong.service.auth import (
    ProjectAuthsService,
    AdministratorAuthService,
    PLATFORM_RESOURCES_MAP,
    Resource as Re
)
from bidong.view.schemas.project import (
    ProjectOverviewsSchema,
    ProjectOverviewsInputSchema,
    ProjectAuthorizationSchema,
    ProjectInputSchema,
    ProjectOutputSchema,
    ProjectsOutputSchema
)


class ProjectsHandler(CollectionsHandler):
    def get(self, *args, **kwargs):
        checker = AdministratorAuthService(self.get_current_user_id(),
                                           Re(PLATFORM_RESOURCES_MAP["项目管理"])).check(method="GET")
        if not checker:
            raise UnAuthorizedError("没有权限")

        # 搜索
        if self.q:
            service = ProjectsSearchService(self.q, self.page, self.per_page)
            payload = service.search()
            return self.response(payload=payload)

        # todo
        service = ProjectsService()#self.get_current_user_id())
        if self.fields:
            payload = service.get_fields(self.fields)
        else:
            payload = service.get_details(self.page, self.per_page)
            # payload = ProjectsOutputSchema().dump(payload).data
        return self.response(payload=payload)

    def post(self, *args, **kwargs):
        parameters = validate_with_schema(ProjectInputSchema, self.request_body_dict)
        service = ProjectsService()
        payload = service.integrated_create(overviews=parameters.overviews,
                                            authorizations=parameters.authorizations)
        payload = ProjectOutputSchema().dump(payload).data
        return self.response(payload=payload)


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


class ProjectsFeaturesHandler(IndividualsHandler):
    def get(self):
        payload = ProjectAuthsService.list_all_alternative_features()
        self.response(payload=payload)
