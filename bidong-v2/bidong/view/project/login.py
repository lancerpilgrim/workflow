from bidong.service.login import ManagerPasswordLoginService
from bidong.service.executor import ManagerService
from bidong.view.project import IndividualsHandler
from bidong.view.schemas.login import LoginInputSchema, LoginUpdateSchema
from bidong.core.validates import validate_with_schema


class LoginHandler(IndividualsHandler):

    def get(self):
        project_id = self.smart_query_get("project_id")
        payload = ManagerService(self.get_current_user_id()).get_authorizations_by_project_id(project_id)
        # ps = ManagerPasswordLoginService(ss.mobile)
        # ps.init_user_login_info(ss.id)
        self.response(payload=payload)

    def put(self, *args, **kwargs):
        parameters = validate_with_schema(LoginUpdateSchema, self.request_body_dict)
        s = ManagerPasswordLoginService(parameters.identifier)
        token, payload = s.reset_password(parameters)
        self.set_secure_cookie("token", token)
        self.response(payload=payload)

    def post(self, *args, **kwargs):
        parameters = validate_with_schema(LoginInputSchema, self.request_body_dict)
        s = ManagerPasswordLoginService(parameters.identifier)
        token, payload = s.login(parameters.password)
        self.set_secure_cookie("token", token)
        self.response(payload=payload)

    def delete(self, *args, **kwargs):
        self.clear_cookie("token")
        self.response()




