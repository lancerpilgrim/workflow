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
    AdministratorsAuthorization,
    Administrators
)
from bidong.common.utils import (
    ObjectDict,
    dictize
)


class AdministratorAuthsRepository(object):
    def __init__(self):
        self.r = None
        # TODO 操作记录

    def persist(self, entities):
        rs = []
        for (admin_id, resource_name, resource_locator), attrs in entities.items():
            rs.append(self._insert_or_update(admin_id, resource_name, resource_locator, attrs))
        return rs

    def _insert_or_update(self, holder_id, resource_name, resource_locator, attrs):
        q = session.query(AdministratorsAuthorization).filter(
            AdministratorsAuthorization.authorization_holder == holder_id,
            AdministratorsAuthorization.resource_name == resource_name,
            AdministratorsAuthorization.resource_locator == resource_locator,
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
        r = AdministratorsAuthorization(authorization_holder=auth.holder,
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
        r = session.query(AdministratorsAuthorization).filter(
            AdministratorsAuthorization.authorization_holder == auth.holder,
            AdministratorsAuthorization.resource_name == resource.name,
            AdministratorsAuthorization.resource_locator == resource.locator,
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


class AdministratorsAuthsQuery(BaseQuerySet):
    DATA = ResourceRegistry.DATA
    FEATURE = ResourceRegistry.FEATURE

    def __init__(self):
        self.r = None
        self.paginator = None

    def paginate(self, paginator):
        self.paginator = paginator

    def list_user_features(self, administrator_id):
        self.r = session.query(AdministratorsAuthorization).filter(
            AdministratorsAuthorization.authorization_holder == administrator_id).join(
            ResourceRegistry, AdministratorsAuthorization.resource_id == ResourceRegistry.id).filter(
            ResourceRegistry.resource_type == ResourceRegistry.FEATURE
        )
        return self

    def list_user_data(self, administrator_id):
        self.r = session.query(AdministratorsAuthorization).filter(
            AdministratorsAuthorization.authorization_holder == administrator_id).join(
            ResourceRegistry, AdministratorsAuthorization.resource_id == ResourceRegistry.id).filter(
            ResourceRegistry.resource_type == ResourceRegistry.DATA
        )
        return self

    def locate_user_auth_by_resource(self, administrator_id, resource):
        # 只通过联合索引获取记录，其余交给业务逻辑，提高性能
        self.r = session.query(AdministratorsAuthorization).filter(
            AdministratorsAuthorization.authorization_holder == administrator_id,
            AdministratorsAuthorization.resource_name == resource.name,
            AdministratorsAuthorization.resource_locator == resource.locator,
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


class AdministratorOverviewsRepository(object):
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
        q = session.query(Administrators).filter(
            Administrators.id == entity.id,
        )
        if not session.query(q.exists()).scalar():
            return self._create(entity)
        else:
            return self._reset(entity)

    @staticmethod
    def _create(entity):
        """
        :param entity: A Administrator object
        :return: created object
        """
        r = Administrators(id=entity.id,
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
        r = session.query(Administrators).filter(
            Administrators.id == entity.id,
        ).update(
            name=entity.name,
            status=entity.status,
            mobile=entity.mobile,
            create_time=entity.create_time,
            description=entity.description,
            synchronize_session=False
        )
        return ObjectDict(dictize(r.one()))


class AdministratorOverviewsQuery(BaseQuerySet):
    def __init__(self):
        self.r = None

    def get_by_id(self, administrator_id):
        self.r = session.query(Administrators).filter(Administrators.id == administrator_id)
        return self

    def get_by_mobile(self, mobile):
        self.r = self.r.filter(Administrators.mobile == mobile)
        return self

    def exists(self):
        return session.query(self.r.exists()).scalar()

    def _instantiate(self, *args, **kwargs):
        r = self.r.one_or_none()
        if r is None:
            return None
        return ObjectDict(dictize(self.r))


class AdministratorsOverviewsQuery(BaseQuerySet):
    def __init__(self):
        self.r = session.query(Administrators)
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
            self.r = self.r.order_by(Administrators.create_time.desc())
        self.r = self.r.order_by(Administrators.create_time)
        return self

    def filter_by_mobile(self, mobile):
        self.r = self.r.filter(Administrators.mobile.like("%{0}%".format(mobile)))
        return self

    def filter_by_name(self, name):
        self.r = self.r.filter(Administrators.name.like("%{0}%".format(name)))
        return self

    def filter_enabled(self):
        self.r = self.r.filter(Administrators.status == Administrators.ENABLED)
        return self

    def filter_disabled(self):
        self.r = self.r.filter(Administrators.status == Administrators.DISABLED)
        return self

    def filter_deleted(self):
        self.r = self.r.filter(Administrators.status == Administrators.DELETE)
        return self

    def exclude_deleted(self):
        self.r = self.r.filter(Administrators.status.in_((Administrators.ENABLED, Administrators.DISABLED)))
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
