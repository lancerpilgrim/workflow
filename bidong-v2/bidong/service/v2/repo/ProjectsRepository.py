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
from bidong.storage.models import Projects, ProjectsAuthorization, ResourceRegistry
from bidong.common.utils import generate_random_id, dictize, ObjectDict
from bidong.core.repo import BaseRepo
from bidong.core.paginator import Paginator
from bidong.core.database import session
from bidong.service.v2.repo.ManagersRepository import *


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

    def filter_by_Project_id(self, Project_id):
        r = session.query(ProjectsAuthorization.resource_locator).filter(
            ProjectsAuthorization.authorization_holder == Project_id).filter(
            ProjectsAuthorization.resource_name == "platform_project_data"
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
        self.r.update({"status": Projects.DELETE}, synchronize_session=False)

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


# 一九二七年春，帕斯捷尔纳克致茨维塔耶娃:
#
# 　　我们多么草率地成为了孤儿。玛琳娜，
# 　　这是我最后一次呼唤你的名字。
# 　　 大雪落在
# 　　我锈迹斑斑的气管和肺叶上，
# 　　说吧：今夜，我的嗓音是一列被截停的火车，
# 　　你的名字是俄罗斯漫长的国境线。
# 　　
# 　　我想象我们的相遇，在一场隆重的死亡背面
# 　　（玫瑰的矛盾贯穿了他硕大的心）；
# 　　在一九二七年春夜，我们在国境线相遇
# 　　因此错过了
# 　　 这个呼啸着奔向终点的世界。
# 　　而今夜，你是舞曲，世界是错误。
# 　　
# 　　当新年的钟声敲响的时候，百合花盛放
# 　　——他以他的死宣告了世纪的终结，
# 　　而不是我们尴尬的生存。
# 　　 为什么我要对你们沉默？
# 　　当华尔兹舞曲奏起的时候，我在谢幕。
# 　　因为今夜，你是旋转，我是迷失。
# 　　
# 　　当你转换舞伴的时候，我将在世界的留言册上
# 　　抹去我的名字。
# 　　 玛琳娜，国境线的舞会
# 　　停止，大雪落向我们各自孤单的命运。
# 　　我歌唱了这寒冷的春天，我歌唱了我们的废墟
# 　　……然后我又将沉默不语。
# 　　
# 　　
# 　　 1999.4.27


from bidong.core.database import session
from bidong.core.paginator import Paginator
from bidong.service.v2.repo import BaseQuerySet
from bidong.storage.models import (
    ResourceRegistry,
    ProjectsAuthorization,
    Projects,
    ProjectsAuthorization,
    Projects
)
from bidong.common.utils import (
    ObjectDict,
    dictize
)


class ProjectAuthsRepository(object):
    def __init__(self):
        self.r = None
        # TODO 操作记录

    def persist(self, entities):
        rs = []
        for (admin_id, resource_name, resource_locator), attrs in entities.items():
            rs.append(self._insert_or_update(admin_id, resource_name, resource_locator, attrs))
        return rs

    def _insert_or_update(self, holder_id, resource_name, resource_locator, attrs):
        q = session.query(ProjectsAuthorization).filter(
            ProjectsAuthorization.authorization_holder == holder_id,
            ProjectsAuthorization.resource_name == resource_name,
            ProjectsAuthorization.resource_locator == resource_locator,
        )
        if not session.query(q.exists()).scalar():
            return self._create(attrs.auth, attrs.resource)
        else:
            return self._reset(attrs.auth, attrs.resource)

    @staticmethod
    def _create(auth, resource):
        """
        :param resource: A Resource object, 至少含有 `id`, `name`, `locator`等属性 
        :param auth: 授权信息, 至少含有 `holder`,`allow_method` 属性
        :return: 
        """
        r = ProjectsAuthorization(authorization_holder=auth.holder,
                                  holder_type=auth.holder_type,
                                  resource_id=resource.id,
                                  resource_name=resource.name,
                                  resource_locator=resource.locator,
                                  allow_method=auth.allow_method,
                                  status=auth.status
                                  )
        session.add(r)
        session.flush()
        return ObjectDict(dictize(r))

    @staticmethod
    def _reset(auth, resource):
        r = session.query(ProjectsAuthorization).filter(
            ProjectsAuthorization.authorization_holder == auth.holder,
            ProjectsAuthorization.resource_name == resource.name,
            ProjectsAuthorization.resource_locator == resource.locator,
        ).update(
            authorization_holder=auth.holder,
            holder_type=auth.holder_type,
            resource_id=resource.id,
            resource_name=resource.name,
            resource_locator=resource.locator,
            allow_method=auth.allow_method,
            status=auth.status,
            synchronize_session=False)
        return ObjectDict(dictize(r.one()))


class ProjectsAuthsQuery(BaseQuerySet):
    DATA = ResourceRegistry.DATA
    FEATURE = ResourceRegistry.FEATURE

    def __init__(self):
        self.r = None
        self.paginator = None

    def paginate(self, paginator):
        self.paginator = paginator

    def list_project_features(self, project_id):
        self.r = session.query(ProjectsAuthorization).filter(
            ProjectsAuthorization.authorization_holder == project_id).join(
            ResourceRegistry, ProjectsAuthorization.resource_id == ResourceRegistry.id).filter(
            ResourceRegistry.resource_type == ResourceRegistry.FEATURE
        )
        return self

    def list_project_data(self, project_id):
        self.r = session.query(ProjectsAuthorization).filter(
            ProjectsAuthorization.authorization_holder == project_id).join(
            ResourceRegistry, ProjectsAuthorization.resource_id == ResourceRegistry.id).filter(
            ResourceRegistry.resource_type == ResourceRegistry.DATA
        )
        return self

    def locate_project_auth_by_resource(self, project_id, resource):
        # 只通过联合索引获取记录，其余交给业务逻辑，提高性能
        self.r = session.query().filter(
            ProjectsAuthorization.authorization_holder == project_id,
            ProjectsAuthorization.resource_name == resource.name,
            ProjectsAuthorization.resource_locator == resource.locator,
        )
        return self

    def _instantiate(self, *args, **kwargs):
        pagination = ObjectDict({})
        if self.paginator is None:
            rs = [ObjectDict(dictize(each)) for each in self.r.all()]
        else:
            if self.paginator.sort:
                self.r = self.r.order_by(self.paginator.sort)
            p = Paginator(self.r, self.paginator.page, self.paginator.per_page).to_dict()
            rs = [ObjectDict(dictize(each)) for each in p.pop("objects")]
            pagination = p
        return rs, pagination


class ProjectOverviewsRepository(object):
    """
    在现在的设计中，repository仅负责持久化，查询任务交给专门的Query
    """

    def __init__(self):
        self.r = None
        # TODO 操作记录

    def persist(self, entity):
        r = self._insert_or_update(entity)
        return r

    def _insert_or_update(self, entity):
        q = session.query(Projects).filter(
            Projects.id == entity.id,
        )
        if not session.query(q.exists()).scalar():
            return self._create(entity)
        else:
            return self._reset(entity)

    @staticmethod
    def _create(entity):
        """
        :param entity: A Project object
        :return: created object
        """
        r = Projects(id=entity.id,
                     name=entity.name,
                     status=entity.status,
                     mobile=entity.mobile,
                     create_time=entity.create_time,
                     description=entity.description
                     )
        session.add(r)
        session.flush()
        return ObjectDict(dictize(r))

    @staticmethod
    def _reset(entity):
        r = session.query(Projects).filter(
            Projects.id == entity.id,
        ).update(
            name=entity.name,
            status=entity.status,
            mobile=entity.mobile,
            create_time=entity.create_time,
            description=entity.description,
            synchronize_session=False
        )
        return ObjectDict(dictize(r.one()))


class ProjectOverviewsQuery(BaseQuerySet):
    def __init__(self):
        self.r = None

    def get_by_id(self, project_id):
        self.r = session.query(Projects).filter(Projects.id == project_id)
        return self

    def get_by_mobile(self, mobile):
        self.r = self.r.filter(Projects.mobile == mobile)
        return self

    def exists(self):
        return session.query(self.r.exists()).scalar()

    def _instantiate(self, *args, **kwargs):
        r = self.r.one_or_none()
        if r is None:
            return None
        return ObjectDict(dictize(self.r))


class ProjectsOverviewsQuery(BaseQuerySet):
    def __init__(self):
        self.r = session.query(Projects)
        self.paginator = None

    def paginate(self, paginator):
        self.paginator = paginator
        return self

    def order_by_create_time(self, desc=False):
        if desc:
            self.r = self.r.order_by(Projects.create_time.desc())
        self.r = self.r.order_by(Projects.create_time)
        return self

    def filter_by_mobile(self, mobile):
        self.r = self.r.filter(Projects.mobile.like("%{0}%".format(mobile)))
        return self

    def filter_by_name(self, name):
        self.r = self.r.filter(Projects.name.like("%{0}%".format(name)))
        return self

    def filter_enabled(self):
        self.r = self.r.filter(Projects.status == Projects.ENABLED)
        return self

    def filter_disabled(self):
        self.r = self.r.filter(Projects.status == Projects.DISABLED)
        return self

    def filter_deleted(self):
        self.r = self.r.filter(Projects.status == Projects.DELETE)
        return self

    def exclude_deleted(self):
        self.r = self.r.filter(Projects.status.in_((Projects.ENABLED, Projects.DISABLED)))
        return self

    def _instantiate(self):
        rs = ObjectDict()
        pagination = ObjectDict()
        if self.paginator is None:
            rs.update({each.id: ObjectDict(dictize(each)) for each in self.r.all()})
        else:
            if self.paginator.sort:
                self.r = self.r.order_by(self.paginator.sort)
            p = Paginator(self.r, self.paginator.page, self.paginator.per_page).to_dict()
            rs.update({each.id: ObjectDict(dictize(each)) for each in p.pop("objects")})
            pagination = p
        return rs, pagination
