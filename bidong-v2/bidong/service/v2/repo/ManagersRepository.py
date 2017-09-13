# 一九二七年春，帕斯捷尔纳克致茨维塔耶娃

from bidong.core.database import session
from bidong.core.paginator import Paginator
from bidong.service.v2.repo import BaseQuerySet
from bidong.storage.models import (
    ResourceRegistry,
    ManagersAuthorization,
    Managers
)
from bidong.common.utils import (
    ObjectDict,
    dictize
)


class ManagerAuthsRepository(object):
    def __init__(self):
        self.r = None
        # TODO 操作记录

    def persist(self, entities):
        rs = []
        for (admin_id, resource_name, resource_locator), attrs in entities.items():
            rs.append(self._insert_or_update(admin_id, resource_name, resource_locator, attrs))
        return rs

    def _insert_or_update(self, holder_id, resource_name, resource_locator, attrs):
        q = session.query(ManagersAuthorization).filter(
            ManagersAuthorization.authorization_holder == holder_id,
            ManagersAuthorization.resource_name == resource_name,
            ManagersAuthorization.resource_locator == resource_locator,
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
        r = ManagersAuthorization(authorization_holder=auth.holder,
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
        r = session.query(ManagersAuthorization).filter(
            ManagersAuthorization.authorization_holder == auth.holder,
            ManagersAuthorization.resource_name == resource.name,
            ManagersAuthorization.resource_locator == resource.locator,
        ).update(
            dict(
                authorization_holder=auth.holder,
                holder_type=auth.holder_type,
                resource_id=resource.id,
                resource_name=resource.name,
                resource_locator=resource.locator,
                allow_method=auth.allow_method,
                status=auth.status),
            synchronize_session=False)
        r = session.query(ManagersAuthorization).filter(
            ManagersAuthorization.authorization_holder == auth.holder,
            ManagersAuthorization.resource_name == resource.name,
            ManagersAuthorization.resource_locator == resource.locator,
        )
        return ObjectDict(dictize(r.one()))


class ManagersAuthsQuery(BaseQuerySet):
    def __init__(self):
        self.r = None
        self.paginator = None

    def paginate(self, paginator):
        self.paginator = paginator

    def list_user_features(self, manager_id):
        self.r = session.query(ManagersAuthorization).filter(
            ManagersAuthorization.authorization_holder == manager_id).join(
            ResourceRegistry, ManagersAuthorization.resource_id == ResourceRegistry.id).filter(
            ResourceRegistry.resource_type == ResourceRegistry.FEATURE
        )
        return self

    def list_user_data(self, manager_id):
        self.r = session.query(ManagersAuthorization).filter(
            ManagersAuthorization.authorization_holder == manager_id).join(
            ResourceRegistry, ManagersAuthorization.resource_id == ResourceRegistry.id).filter(
            ResourceRegistry.resource_type == ResourceRegistry.DATA
        )
        return self

    def filter_by_project(self, project_id):
        self.r = self.r.filter(ManagersAuthorization.resource_locator == project_id)
        return self

    def locate_user_auth_by_resource(self, manager_id, resource):
        # 只通过联合索引获取记录，其余交给业务逻辑，提高性能
        self.r = session.query(ManagersAuthorization).filter(
            ManagersAuthorization.authorization_holder == manager_id,
            ManagersAuthorization.resource_name == resource.name,
            ManagersAuthorization.resource_locator == resource.locator,
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


class ManagerOverviewsRepository(object):
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
        q = session.query(Managers).filter(
            Managers.id == entity.id,
        )
        if not session.query(q.exists()).scalar():
            return self._create(entity)
        else:
            return self._reset(entity)

    @staticmethod
    def _create(entity):
        """
        :param entity: A Manager object
        :return: created object
        """
        r = Managers(id=entity.id,
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
        q = session.query(Managers).filter(
            Managers.id == entity.id,
        )
        print(q)
        r = q.update(
            dict(name=entity.name,
                 status=entity.status,
                 mobile=entity.mobile,
                 description=entity.description),
            synchronize_session=False
        )
        session.flush()
        r = session.query(Managers).filter(
            Managers.id == entity.id,
        )
        print(r)
        return ObjectDict(dictize(r.one()))


class ManagerOverviewsQuery(BaseQuerySet):
    def __init__(self):
        self.r = None

    def get_by_id(self, manager_id):
        self.r = session.query(Managers).filter(Managers.id == manager_id)
        return self

    def get_by_mobile(self, mobile):
        self.r = self.r.filter(Managers.mobile == mobile)
        return self

    def exists(self):
        return session.query(self.r.exists()).scalar()

    def _instantiate(self, *args, **kwargs):
        r = self.r.one_or_none()
        if r is None:
            return None
        return ObjectDict(dictize(r))


class ManagersOverviewsQuery(BaseQuerySet):
    def __init__(self):
        self.r = session.query(Managers)
        self.paginator = None

    def paginate(self, paginator):
        self.paginator = paginator
        page = self.paginator.get("page")
        per_page = self.paginator.get("per_page")
        if not page or not per_page:
            self.paginator = None
        return self

    def order_by_create_time(self, desc=False):
        if desc:
            self.r = self.r.order_by(Managers.create_time.desc())
        self.r = self.r.order_by(Managers.create_time)
        return self

    def filter_by_mobile(self, mobile):
        self.r = self.r.filter(Managers.mobile.like("%{0}%".format(mobile)))
        return self

    def filter_by_name(self, name):
        self.r = self.r.filter(Managers.name.like("%{0}%".format(name)))
        return self

    def filter_enabled(self):
        self.r = self.r.filter(Managers.status == Managers.ENABLED)
        return self

    def filter_disabled(self):
        self.r = self.r.filter(Managers.status == Managers.DISABLED)
        return self

    def filter_deleted(self):
        self.r = self.r.filter(Managers.status == Managers.DELETE)
        return self

    def exclude_deleted(self):
        self.r = self.r.filter(Managers.status.in_((Managers.ENABLED, Managers.DISABLED)))
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


class ManagersQuery(BaseQuerySet):
    def __init__(self):
        self.r = session.query(Managers)
        self.paginator = None

    def paginate(self, paginator):
        self.paginator = paginator
        page = self.paginator.get("page")
        per_page = self.paginator.get("per_page")
        if not page or not per_page:
            self.paginator = None
        return self

    def exclude_deleted(self):
        self.r = self.r.filter(Managers.status.in_((Managers.ENABLED, Managers.DISABLED)))
        return self

    def filter_by_project(self, project_id):
        if project_id:
            self.r = self.r.filter(
                ManagersAuthorization.authorization_holder == Managers.id,
                ManagersAuthorization.resource_locator == project_id).distinct()
        return self

    def _instantiate(self, *args, **kwargs):
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
