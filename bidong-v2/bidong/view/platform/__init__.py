import logging

from bidong.core.views import ApiHandler
from bidong.service.login import URI_WHITE_LIST, PlatformTokenService
from bidong.core.exceptions import NeedLoginException, NoPermissionError
from bidong.service.auth import (
    PLATFORM_RESOURCES_MAP,
    Resource as R,
    AdministratorAuthService
)


class Resource(ApiHandler):
    logger = logging.getLogger('platform')

    def prepare(self):
        super(Resource, self).prepare()
        self.session = self.auth()
        if self.session:
            self.set_secure_cookie('token', self.session.token)

    def get_current_user(self):
        return self.session.user_role

    def get_current_user_id(self):
        if self.session:
            return self.session.user_id

    def get_current_userid(self):
        if self.session:
            return self.session.user_id

    def auth(self):
        service = PlatformTokenService()
        uri_condition = self.request.path.rstrip("/") in URI_WHITE_LIST.uri
        method_condition = str(self.request.method).lower() in URI_WHITE_LIST.method
        if uri_condition and method_condition:
            return None
        try:
            token = self.request.headers["Authorization"]
        except (KeyError,) as e:
            token = self.get_secure_cookie("token")
        if not token:
            raise NeedLoginException(status_code=401, message="请登录")
        return service.token_auth(token)

    def check_permision(self, resource_name, action='GET'):
        allow = AdministratorAuthService(
            self.get_current_user_id(),
            R(PLATFORM_RESOURCES_MAP[resource_name])
        ).check(
            method=action
        )
        if not allow:
            raise NoPermissionError("没有权限")


class CollectionsHandler(Resource):
    def data_received(self, chunk):
        pass

    def __init__(self, *args, **kwargs):
        super(CollectionsHandler, self).__init__(*args, **kwargs)
        self.q = self.smart_query_get('q', datatype=str, default="")
        self.per_page = self.smart_query_get('per_page', datatype=int, default=20)
        self.page = self.smart_query_get('page', datatype=int, default=1)
        self.sort = self.smart_query_get('page', datatype=str, default="")
        self.order = self.smart_query_get('page', datatype=str, default="")
        self.fields = self.smart_query_get('fields', datatype=str, default="")

    def response(self, **kwargs):
        return super(CollectionsHandler, self).response(**kwargs)


class IndividualsHandler(Resource):
    def data_received(self, chunk):
        pass

    def __init__(self, *args, **kwargs):
        super(IndividualsHandler, self).__init__(*args, **kwargs)

    def response(self, **kwargs):
        return super(IndividualsHandler, self).response(**kwargs)
