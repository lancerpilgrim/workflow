from bidong.service.login import AdministratorPasswordLoginService
from bidong.service.executor import AdministratorService
from bidong.view.platform import IndividualsHandler
from bidong.view.schemas.login import LoginInputSchema, LoginUpdateSchema
from bidong.core.validates import validate_with_schema


class LoginHandler(IndividualsHandler):

    def get(self):
        # sessions的GET方法通常会返回根目录，我们这里处理成返回本次会话的权限信息。
        payload = AdministratorService(self.get_current_user_id()).get_authorizations()
        self.response(payload=payload)

    def put(self, *args, **kwargs):
        parameters = validate_with_schema(LoginUpdateSchema, self.request_body_dict)
        s = AdministratorPasswordLoginService(parameters.identifier)
        token = s.reset_password(parameters)
        self.set_secure_cookie("token", token)
        self.response()

    def post(self, *args, **kwargs):
        parameters = validate_with_schema(LoginInputSchema, self.request_body_dict)
        s = AdministratorPasswordLoginService(parameters.identifier)
        token, payload = s.login(parameters.password)
        self.set_secure_cookie("token", token)
        self.response(payload=payload)

    def delete(self, *args, **kwargs):
        self.clear_cookie("token")
        self.response()




