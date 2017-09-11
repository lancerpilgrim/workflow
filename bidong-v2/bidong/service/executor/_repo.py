import time
from sqlalchemy.orm.exc import NoResultFound
from bidong.core.exceptions import DuplicateError
from bidong.storage.models import Administrators, Managers
from bidong.common.utils import generate_random_number, ObjectDict, dictize
from bidong.core.repo import BaseRepo
from bidong.core.paginator import Paginator
from bidong.core.database import session


class ExecutorsRepo(BaseRepo):

    def __init__(self, executor):
        self.Executor = executor
        self.r = session.query(self.Executor)

    @property
    def query_set(self):
        return self.r

    def create(self, param_dict):
        mobile = param_dict["mobile"]
        if self.get_by_mobile(mobile) is not None:
            raise DuplicateError(message="手机号已存在")
        if "create_time" not in param_dict:
            param_dict["create_time"] = int(time.time())
        _id = self._generate_id()
        param_dict.update({"id": _id})
        executor = self.Executor(**param_dict)
        session.add(executor)
        session.flush()
        return ObjectDict(dictize(executor))

    def order_by_id(self, desc=False):
        if desc:
            return self.r.order_by(self.Executor.id.desc())
        return self.r.order_by(self.Executor.id)

    def order_by_create_time(self, desc=False):
        if desc:
            self.r = self.r.order_by(self.Executor.create_time.desc())
        self.r = self.r.order_by(self.Executor.create_time)

    def get_by_mobile(self, mobile):
        self.r = self.r.filter(self.Executor.mobile == mobile)
        return self.r.first()

    def filter_by_mobile(self, mobile):
        self.r = self.r.filter(self.Executor.mobile.like("%{0}%".format(mobile)))
        return self

    def filter_by_name(self, name):
        self.r = self.r.filter(self.Executor.name.like("%{0}%".format(name)))
        return self

    def filter_enabled(self):
        self.r = self.r.filter(self.Executor.status == self.Executor.ENABLED)
        return self

    def exclude_deleted(self):
        self.r = self.r.filter(self.Executor.status.in_((self.Executor.ENABLED, self.Executor.DISABLED)))
        return self

    def filter_disabled(self):
        self.r = self.r.filter(self.Executor.status == self.Executor.DISABLED)
        return self

    def _generate_id(self, max_retry=3):
        while max_retry > 0:
            while 1:
                _id = "1" + generate_random_number(9)
                if len(_id) == 10:
                    break
            print(_id)
            if self._primary_key_conflicted(_id):
                max_retry -= 1
            else:
                return _id
        raise Exception("_id Max Retries")

    def _primary_key_conflicted(self, _id):
        q = session.query(self.Executor).filter(self.Executor.id == _id)
        return session.query(q.exists()).scalar()

    def _instantiate(self, page, per_page, sort, order):
        if sort:
            self.r.order_by(sort)
        if not (page and per_page):
            res = ObjectDict({})
            res.objects = [ObjectDict(dictize(each)) for each in self.r.all()]
        else:
            res = ObjectDict(Paginator(self.r, page, per_page).to_dict())
            res.objects = [ObjectDict(dictize(each)) for each in res.objects]
        return res


class ExecutorRepo(BaseRepo):
    DISABLED = 0
    ENABLED = 1
    DELETE = 2

    def __init__(self, executor, _id):
        self.Executor = executor
        self._id = _id
        self.r = None

    def get_by_pk(self):
        self.r = session.query(self.Executor).filter(self.Executor.id == self._id)
        return self

    def update(self, param_dict):
        self.r.update(param_dict, synchronize_session=False)
        return self

    def delete(self):
        self.r.update({"status": self.Executor.DELETE}, synchronize_session=False)
        return self

    def disable(self):
        self.r.update({"status": self.Executor.DISABLED}, synchronize_session=False)
        return self

    def enable(self):
        self.r.update({"status": self.Executor.ENABLED}, synchronize_session=False)
        return self

    def _instantiate(self):
        res = self.r.one_or_none()
        if res is None:
            raise NoResultFound
        if res.status == self.Executor.DELETE:
            raise NoResultFound
        return ObjectDict(dictize(self.r.one()))


class AdministratorsRepo(ExecutorsRepo):
    def __init__(self):
        super(AdministratorsRepo, self).__init__(Administrators)


class ManagersRepo(ExecutorsRepo):
    def __init__(self):
        super(ManagersRepo, self).__init__(Managers)


class AdministratorRepo(ExecutorRepo):
    def __init__(self, _id):
        super(AdministratorRepo, self).__init__(Administrators, _id)


class ManagerRepo(ExecutorRepo):
    def __init__(self, _id):
        super(ManagerRepo, self).__init__(Managers, _id)
