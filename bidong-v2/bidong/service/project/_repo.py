#    我想和你一起生活
#    在某个小镇，
# 　　共享无尽的黄昏
# 　　和绵绵不绝的钟声。
# 　　在这个小镇的旅店里
# 　　古老时钟敲出的
# 　　微弱响声
# 　　像时间轻轻滴落。
import time
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError
from bidong.core.exceptions import DuplicateError
from bidong.storage.models import Projects, AdministratorsAuthorization, ResourceRegistry
from bidong.common.utils import generate_random_id, dictize, ObjectDict
from bidong.core.repo import BaseRepo
from bidong.core.paginator import Paginator
from bidong.core.database import session


class ProjectsRepo(BaseRepo):

    # 简单系统暂不考虑Specification和规约模式
    # 大多数方法返回self，即集合本身，通过self.all()方法获取实例化的对象集合

    def __init__(self):
        self.r = session.query(Projects)

    def create(self, param_dict):
        _id = self._generate_id()
        param_dict.update({"id": _id})
        if "create_time" not in param_dict:
            param_dict["create_time"] = int(time.time())
        project = Projects(**param_dict)
        session.add(project)
        session.flush()
        return ObjectDict(dictize(project))

    def order_by_create_time(self, desc=False):
        if desc:
            self.r = self.r.order_by(Projects.create_time.desc())
        self.r = self.r.order_by(Projects.create_time)

    def filter_by_mobile(self, mobile):
        self.r = self.r.filter(Projects.contact_number.like("%{0}%".format(mobile)))
        return self

    def filter_by_id(self, _id_list):
        self.r = self.r.filter(Projects.id._in(_id_list))

    def filter_by_name(self, name):
        self.r = self.r.filter(Projects.name.like("%{0}%".format(name)))
        return self

    def filter_by_contact_name(self, name):
        self.r = self.r.filter(Projects.contact.like("%{0}%".format(name)))
        return self

    def filter_enabled(self):
        self.r = self.r.filter(Projects.status == Projects.ENABLED)
        return self

    def filter_disabled(self):
        self.r = self.r.filter(Projects.status == Projects.DISABLED)
        return self

    def exclude_deleted(self):
        self.r = self.r.filter(Projects.status.in_((Projects.DISABLED, Projects.ENABLED)))
        return self

    def filter_by_administrator_id(self, administrator_id):
        r = session.query(AdministratorsAuthorization.resource_locator).filter(
            AdministratorsAuthorization.authorization_holder == administrator_id).filter(
            AdministratorsAuthorization.resource_name == "platform_project_data"
        )
        self.r = self.r.filter(Projects.id.in_(r))
        return self

    def _generate_id(self, max_retry=3):
        while max_retry > 0:
            while 1:
                _id = "1" + generate_random_id(9)
                if len(_id) == 10:
                    break
            if self._primary_key_conflicted(_id):
                max_retry -= 1
            else:
                return _id
        raise Exception("_id Max Retries")

    @staticmethod
    def _primary_key_conflicted(_id):
        q = session.query(Projects).filter(Projects.id == _id)
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


class ProjectRepo(BaseRepo):
    """
    单个project的仓储操作
    """

    def __init__(self, _id):
        self._id = _id
        self.r = None

    def get_by_pk(self):
        self.r = session.query(Projects).filter(Projects.id == self._id)
        return self

    def update(self, param_dict):
        self.r.update(param_dict, synchronize_session=False)
        return self

    def delete(self):
        self.r.update({"status":Projects.DELETE}, synchronize_session=False)

    def disable(self):
        self.r.update({"status": Projects.DISABLED}, synchronize_session=False)

    def enable(self):
        self.r.update({"status": Projects.ENABLED}, synchronize_session=False)

    def _instantiate(self):
        res = self.r.one_or_none()
        if res is None:
            raise NoResultFound
        if res.status == Projects.DELETE:
            raise NoResultFound
        return ObjectDict(dictize(self.r.one()))
