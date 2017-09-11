from bidong.core.repo import BaseRepo
from bidong.storage.models import ManagersLogin, AdministratorsLogin
from bidong.common.utils import dictize, ObjectDict
from bidong.core.database import session
from bidong.core.auth import generate_password_hash, check_password_hash


class LoginRepo(BaseRepo):
    def __init__(self, identifier):
        self.user_identifier = identifier
        self.r = None

    def get_salted_password(self):
        pass

    def _instantiate(self, *args, **kwargs):
        r = self.r.one_or_none()
        if r is None:
            return None
        return ObjectDict(dictize(self.r.one()))


class ManagerLoginRepo(LoginRepo):
    NEED_RESET = ManagersLogin.NEED_RESET
    RESET = ManagersLogin.RESET

    def __init__(self, identifier):
        super(ManagerLoginRepo, self).__init__(identifier)

    def get(self, method="mobile"):
        if method == "mobile":
            return self.get_by_mobile()
        elif method == "user_name":
            return self.get_by_user_name()
        elif method == "email":
            return self.get_by_email()
        else:
            return None

    def get_by_id(self):
        self.r = session.query(ManagersLogin).filter(ManagersLogin.id == self.user_identifier)
        return self

    def get_by_user_name(self):
        self.r = session.query(ManagersLogin).filter(ManagersLogin.user_name == self.user_identifier)
        return self

    def get_by_email(self):
        self.r = session.query(ManagersLogin).filter(ManagersLogin.email == self.user_identifier)
        return self

    def get_by_mobile(self):
        self.r = session.query(ManagersLogin).filter(ManagersLogin.mobile == self.user_identifier)
        return self

    def create(self, manager_id, password):
        salted_password = generate_password_hash(password)
        new = ManagersLogin(id=manager_id,
                            mobile=self.user_identifier,
                            password=salted_password,
                            status=ManagersLogin.NEED_RESET)
        session.add(new)
        session.flush()
        return ObjectDict(dictize(new))

    def check_password(self, password):
        user = self.r.one()
        return check_password_hash(user.password, password)

    def update_password(self, password):
        salted_password = generate_password_hash(password)
        self.r.update({"password": salted_password, "status": ManagersLogin.RESET})
        return self.r.one()


class AdministratorLoginRepo(LoginRepo):
    NEED_RESET = AdministratorsLogin.NEED_RESET
    RESET = AdministratorsLogin.RESET

    def __init__(self, identifier):
        super(AdministratorLoginRepo, self).__init__(identifier)

    def get(self, method="mobile"):
        if method == "mobile":
            return self.get_by_mobile()
        elif method == "user_name":
            return self.get_by_user_name()
        elif method == "email":
            return self.get_by_email()
        else:
            return None

    def get_by_id(self):
        self.r = session.query(AdministratorsLogin).filter(AdministratorsLogin.id == self.user_identifier)
        return self

    def get_by_user_name(self):
        self.r = session.query(AdministratorsLogin).filter(AdministratorsLogin.user_name == self.user_identifier)
        return self

    def get_by_email(self):
        self.r = session.query(AdministratorsLogin).filter(AdministratorsLogin.email == self.user_identifier)
        return self

    def get_by_mobile(self):
        self.r = session.query(AdministratorsLogin).filter(AdministratorsLogin.mobile == self.user_identifier)
        return self

    def create_or_update(self, administrator_id, password):
        salted_password = generate_password_hash(password)
        r = session.query(AdministratorsLogin).filter(AdministratorsLogin.id == administrator_id,
                                                      AdministratorsLogin.mobile == self.user_identifier)
        if session.query(r.exists()).scalar():
            r.update({"password": salted_password, "status": AdministratorsLogin.RESET}, synchronize_session=False)
            new = r.one()
        else:
            new = AdministratorsLogin(id=administrator_id,
                                      mobile=self.user_identifier,
                                      password=salted_password,
                                      status=AdministratorsLogin.NEED_RESET)
            session.add(new)
            session.flush()
        return ObjectDict(dictize(new))

    def check_password(self, password):
        user = self.r.one()
        return check_password_hash(user.password, password)

    def update_password(self, password):
        salted_password = generate_password_hash(password)
        self.r.update({"password": salted_password, "status": AdministratorsLogin.RESET})
        return self.r.one()
