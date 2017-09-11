import jwt
from bidong.core.auth import gen_auth_token, decode_auth_token
from bidong.core.exceptions import SignatureExpiredError, NeedLoginException, LoginError
from ._repo import ManagerLoginRepo, AdministratorLoginRepo
from bidong.common.utils import ObjectDict
from bidong.core.log import logger
from settings import version
from bidong.service.executor import AdministratorService, ManagerService

URI_WHITE_LIST = ObjectDict({"uri": "/{version}/sessions".format(version=version),
                             "method": {"post", "put"}})


class BaseTokenService(object):
    def __init__(self, aud, user_role):
        self.aud = aud
        self.user_role = user_role

    def token_auth(self, token):
        try:
            payload = decode_auth_token(token, self.aud)
        except jwt.exceptions.ExpiredSignatureError as e:
            logger.error(e)
            raise SignatureExpiredError(status_code=401, message="登录已过期")
        except jwt.exceptions.InvalidTokenError as e:
            logger.error(e)
            raise LoginError(status_code=401, message="认证失败")
        else:
            rv = ObjectDict({})
            rv.update(payload)
            rv.token = token
            return rv

    def generate_token(self, user_id):
        payload = {"user_id": user_id, "user_role": self.user_role}
        return gen_auth_token(payload=payload, aud=self.aud)


class PlatformTokenService(BaseTokenService):
    def __init__(self):
        super(PlatformTokenService, self).__init__("platform", "administrator")


class ClientTokenService(BaseTokenService):
    def __init__(self):
        super(ClientTokenService, self).__init__("client", "manager")


class ManagerPasswordLoginService(object):
    def __init__(self, identifier, method="mobile"):
        self.repo = ManagerLoginRepo(identifier)
        self.method = method

    def login(self, password):
        # TODO 第一步只支持手機號登錄然後重置密碼
        user = self.repo.get(method=self.method).one()
        if user is None:
            raise LoginError(status_code=401, message="用戶不存在")
        ms = ManagerService(user.id)
        if not ms.check_enable():
            raise LoginError(status_code=401, message="用户已禁用")
        else:
            rs = self.repo.check_password(password)
            if not rs:
                raise LoginError(status_code=401, message="密码错误")
            # if user.status == self.repo.NEED_RESET:
            #     raise LoginError(status_code=307, message="請重置密碼")
            # 簽發token
            token = ClientTokenService().generate_token(user.id)
            payload = {"sessions": {"user_id": user.id,
                                    "name": ms.get_overviews().name}}
            return token, payload

    def init_user_login_info(self, manager_id):
        # 根據手機號和管理員id初始化一個登錄賬號密碼。
        default_password = "bidongwifi"
        user = self.repo.create(manager_id, default_password)

    def reset_password(self, parameters):
        previous_password = parameters.previous_password
        new_password = parameters.new_password
        user = self.repo.get(method=self.method).one()
        if user is None:
            raise LoginError(status=401, message="用户不存在")
        rs = self.repo.check_password(previous_password)
        if not rs:
            raise LoginError(status_code=401, message="密码错误")
        self.repo.update_password(new_password)
        token = ClientTokenService().generate_token(user.id)
        payload = {"sessions": {"user_id": user.id}}
        return token, payload


class AdministratorPasswordLoginService(object):
    def __init__(self, identifier, method="mobile"):
        self.repo = AdministratorLoginRepo(identifier)
        self.method = method

    def login(self, password):
        # TODO 第一步只支持手機號登錄然後重置密碼
        user = self.repo.get(method=self.method).one()
        if user is None:
            raise LoginError(status_code=401, message="用户不存在")
        s = AdministratorService(user.id)
        if not s.check_enable():
            raise LoginError(status_code=401, message="用户已封禁")
        # elif user.status == self.repo.NEED_RESET:
        #     raise LoginError(status_code=307, message="請重置密碼")
        else:
            rs = self.repo.check_password(password)
            if not rs:
                raise LoginError(status_code=401, message="密码错误")
            # 簽發token
            token = PlatformTokenService().generate_token(user.id)
            payload = {"sessions": {"user_id": user.id,
                                    "name": s.get_overviews().name}}
            return token, payload

    def init_user_login_info(self, administrator_id):
        # 根據手機號和管理員id初始化一個登錄賬號密碼。
        default_password = "bidongwifi"
        user = self.repo.create_or_update(administrator_id, default_password)

    def reset_password(self, parameters):
        previous_password = parameters.previous_password
        new_password = parameters.new_password
        user = self.repo.get(method=self.method).one()
        rs = self.repo.check_password(previous_password)
        if not rs:
            raise LoginError(status_code=401, message="密码错误")
        self.repo.update_password(new_password)
        token = PlatformTokenService().generate_token(user.id)
        return token
