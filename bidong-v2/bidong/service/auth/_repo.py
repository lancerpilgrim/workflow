#    一九二七年春，帕斯捷尔纳克致茨维塔耶娃:
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
import time
from bidong.storage.models import (
    ResourceRegistry,
    ResourceTree,
    AdministratorsAuthorization,
    ManagersAuthorization,
    ProjectsAuthorization
)
from bidong.common.utils import generate_random_id, ObjectDict, dictize
from bidong.core.repo import BaseRepo
from bidong.core.database import session


################
# 管理员权限相关 #
################


class AdministratorAuthRepo(BaseRepo):
    def __init__(self, administrator_id, resource):
        self._id = administrator_id
        self.resource = resource
        self.r = None

    def _instantiate(self, *args, **kwargs):
        return self.r.one()

    def locate(self):
        # 只通过联合索引获取记录，其余交给业务逻辑，提高性能
        self.r = session.query(AdministratorsAuthorization).filter(
            AdministratorsAuthorization.authorization_holder == self._id,
            AdministratorsAuthorization.resource_name == self.resource.name,
            AdministratorsAuthorization.resource_locator == self.resource.locator,
        )
        return self

    def integrated_update(self, auth, resource):
        self.r.update(authorization_holder=auth.holder,
                      holder_type=auth.holder_type,
                      resource_id=resource.id,
                      resource_name=resource.name,
                      resource_locator=resource.locator,
                      allow_method=auth.allow_method,
                      status=auth.status,
                      synchronize_session=False)
        return self

    def update(self, **kwargs):
        self.r.update(kwargs, synchronize_session=False)
        session.flush()
        return self

    def enable(self):
        self.update(status=AdministratorsAuthorization.ENABLED)
        session.flush()
        return self

    def disable(self):
        self.update(status=AdministratorsAuthorization.DISABLED)
        session.flush()
        return self

    def delete(self):
        self.update(status=AdministratorsAuthorization.DELETE)
        session.flush()
        return self


class ManagerAuthRepo(BaseRepo):
    def __init__(self, manager_id, resource):
        self._id = manager_id
        self.resource = resource
        self.r = None

    def _instantiate(self, *args, **kwargs):
        return self.r.one()

    def locate(self):
        # 只通过联合索引获取记录，其余交给业务逻辑，提高性能
        self.r = session.query(ManagersAuthorization).filter(
            ManagersAuthorization.authorization_holder == self._id,
            ManagersAuthorization.resource_name == self.resource.name,
            ManagersAuthorization.resource_locator == self.resource.locator,
        )
        return self

    def integrated_update(self, auth, resource):
        self.r.update(authorization_holder=auth.holder,
                      holder_type=auth.holder_type,
                      resource_id=resource.id,
                      resource_name=resource.name,
                      resource_locator=resource.locator,
                      allow_method=auth.allow_method,
                      status=auth.status,
                      synchronize_session=False)
        return self

    def update(self, **kwargs):
        self.r.update(kwargs, synchronize_session=False)
        session.flush()
        return self

    def enable(self):
        self.update(status=ManagersAuthorization.ENABLED)
        session.flush()
        return self

    def disable(self):
        self.update(status=ManagersAuthorization.DISABLED)
        session.flush()
        return self

    def delete(self):
        self.update(status=ManagersAuthorization.DELETE)
        session.flush()
        return self


class AdministratorAuthsRepo(BaseRepo):
    def __init__(self, administrator_id):
        self._id = administrator_id
        self.r = None

    @staticmethod
    def create(auth, resource):
        """
        :param resource: A Resource object, 至少含有 `id`, `name`, `locator`等属性 
        :param auth: 授权信息, 至少含有 `holder`,`allow_method` 属性
        :return: 
        """
        new = AdministratorsAuthorization(authorization_holder=auth.holder,
                                          holder_type=auth.holder_type,
                                          resource_id=resource.id,
                                          resource_name=resource.name,
                                          resource_locator=resource.locator,
                                          allow_method=auth.allow_method,
                                          status=auth.status
                                          )
        session.add(new)
        session.flush()
        return ObjectDict(dictize(new))

    def list_features(self):
        self.r = session.query(AdministratorsAuthorization).filter(
            AdministratorsAuthorization.authorization_holder == self._id).join(
            ResourceRegistry, AdministratorsAuthorization.resource_id == ResourceRegistry.id).filter(
            ResourceRegistry.resource_type == ResourceRegistry.FEATURE
        )
        return self

    def list_all(self):
        self.r = session.query(AdministratorsAuthorization).filter(AdministratorsAuthorization.authorization_holder == self._id)
        return self

    def filter_enabled(self):
        self.r = self.r.filter(AdministratorsAuthorization.status == AdministratorsAuthorization.ENABLED)
        return self

    def list_data(self):
        self.r = session.query(AdministratorsAuthorization).filter(
            AdministratorsAuthorization.authorization_holder == self._id).join(
            ResourceRegistry, AdministratorsAuthorization.resource_id == ResourceRegistry.id).filter(
            ResourceRegistry.resource_type == ResourceRegistry.DATA
        )
        return self

    def _instantiate(self, *args, **kwargs):
        content = []
        for each in self.r.all():
            content.append(ObjectDict(dictize(each)))
        return content

    @property
    def query_set(self):
        return self.r


class ManagerAuthsRepo(BaseRepo):
    def __init__(self, manager_id):
        self._id = manager_id
        self.r = None

    def create(self, auth, resource):
        """
        :param resource: A Resource object, 至少含有 `id`, `name`, `locator`等属性 
        :param auth: 授权信息, 至少含有 `holder`,`allow_method` 属性
        :return: 
        """
        new = ManagersAuthorization(authorization_holder=auth.holder,
                                    holder_type=auth.holder_type,
                                    resource_id=resource.id,
                                    resource_name=resource.name,
                                    resource_locator=resource.locator,
                                    allow_method=auth.allow_method,
                                    status=auth.status
                                    )

        session.add(new)
        session.flush()
        return ObjectDict(dictize(new))

    def list_features(self):
        self.r = session.query(ManagersAuthorization).filter(
            ManagersAuthorization.authorization_holder == self._id)
        return self

    def filter_enabled(self):
        self.r = self.r.filter(ManagersAuthorization.status == ManagersAuthorization.ENABLED)
        return self

    def filter_project(self, project_id):
        self.r = self.r.filter(ManagersAuthorization.resource_locator == str(project_id))
        return self

    def list_projects(self):
        from bidong.storage.models import Projects
        self.r = session.query(Projects).join(
            ManagersAuthorization, ManagersAuthorization.resource_locator == Projects.id
        ).filter(ManagersAuthorization.status == ManagersAuthorization.ENABLED).filter(
            ManagersAuthorization.authorization_holder == self._id).distinct(
            ManagersAuthorization.resource_locator)
        return self

    def list_data(self):
        return self

    def _instantiate(self, *args, **kwargs):
        content = []
        for each in self.r.all():
            content.append(ObjectDict(dictize(each)))
        return content

    @property
    def query_set(self):
        return self.r


###############
# 项目权限相关 #
###############


class ProjectAuthRepo(BaseRepo):
    def __init__(self, project_id, resource):
        self.project_id = project_id
        self.resource = resource
        self.r = None

    def locate(self):
        # 只通过联合索引获取记录，其余交给业务逻辑，提高性能
        self.r = session.query(ProjectsAuthorization).filter(
            ProjectsAuthorization.authorization_holder == self.project_id,
            ProjectsAuthorization.resource_name == self.resource.name,
            ProjectsAuthorization.resource_locator == self.resource.locator,
        )
        return self

    def integrated_update(self, auth, resource):
        current = int(time.time())
        self.r.update(authorization_holder=auth.holder,
                      holder_type=auth.holder_type,
                      resource_id=resource.id,
                      resource_name=resource.name,
                      resource_locator=resource.locator,
                      allow_method=auth.allow_method,
                      status=auth.status,
                      effective_time=auth.effective_time or current,
                      expiration_time=auth.expiration_time or 0,
                      resource_amount=1 if not hasattr(auth, "resource_amount") else auth.resource_amount,
                      synchronize_session=False)
        return self

    def update(self, **kwargs):
        self.r.update(kwargs, synchronize_session=False)
        session.flush()
        return self

    def enable(self):
        self.update(status=ProjectsAuthorization.ENABLED)
        session.flush()
        return self

    def disable(self):
        self.update(status=ProjectsAuthorization.DISABLED)
        session.flush()
        return self

    def delete(self):
        self.update(status=ProjectsAuthorization.DELETE)
        session.flush()
        return self

    def _instantiate(self, *args, **kwargs):
        return self.r.one()


class ProjectAuthsRepo(BaseRepo):
    def __init__(self, project_id):
        self.project_id = project_id
        self.r = None

    def _instantiate(self, *args, **kwargs):
        content = []
        for each in self.r.all():
            content.append(ObjectDict(dictize(each)))
        return content

    def create(self, auth, resource):
        """
        :param resource: A Resource object, 至少含有 `id`, `name`, `locator`等属性 
        :param auth: 授权信息, 至少含有 `holder`,`allow_method` 属性
        :return: 
        """
        current = int(time.time())
        new = ProjectsAuthorization(authorization_holder=auth.holder,
                                    holder_type=auth.holder_type,
                                    resource_id=resource.id,
                                    resource_name=resource.name,
                                    resource_locator=resource.locator,
                                    allow_method=auth.allow_method,
                                    status=auth.status,
                                    effective_time=auth.effective_time or current,
                                    expiration_time=auth.expiration_time or 0,
                                    resource_amount=1 if not hasattr(auth, "resource_amount") else auth.resource_amount
                                    )
        session.add(new)
        session.flush()
        return ObjectDict(dictize(new))

    def list(self):
        self.r = session.query(ProjectsAuthorization).filter(
            ProjectsAuthorization.authorization_holder == self.project_id)
        return self

    def filter_enabled(self):
        self.r = self.r.filter(ProjectsAuthorization.status == ProjectsAuthorization.ENABLED)
        return self

    @property
    def query_set(self):
        return self.r


################
# 资源操作和方法 #
################

class ResourceRepo(BaseRepo):
    def __init__(self, resource_name="", resource_id=None):
        self.r = None
        self.resource_name = resource_name
        self.resource_id = resource_id

    def locate(self):
        if self.resource_id:
            self.r = session.query(ResourceRegistry).filter(ResourceRegistry.id == self.resource_id)
        else:
            self.r = session.query(ResourceRegistry).filter(
                ResourceRegistry.public_name == self.resource_name,
            )
        return self

    def _instantiate(self):
        return ObjectDict(dictize(self.r.one()))


class ResourcesRepo(BaseRepo):
    def __init__(self):
        self.r = None

    def generate_tree(self, resources):
        pass

    def expand_tree(self, resource_tree):
        pass

    def filter_client(self):
        self.r = self.r.filter(ResourceRegistry.ascription == ResourceRegistry.CLIENT)
        return self

    def filter_platform(self):
        self.r = self.r.filter(ResourceRegistry.ascription == ResourceRegistry.PLATFORM)
        return self

    def get_all_resources(self):
        self.r = session.query(ResourceRegistry)
        return self

    def _instantiate(self, **kwargs):
        content = []
        for each in self.r.all():
            content.append(ObjectDict(dictize(each)))
        return content


###############
# 辅助类和方法 #
###############

# 以下为值对象，仅用于封装数据

class Resource(ObjectDict):
    def __init__(self, resource_public_name, resource_locator="", _id=None, **kwargs):
        super().__init__(**kwargs)
        self.id = _id
        self.name = resource_public_name
        self.locator = resource_locator


class Auth(ObjectDict):
    DISABLED = 0
    ENABLED = 1
    DELETE = 2

    def __init__(self, holder, allow_method=15, status=1, holder_type=0, _id=None, **kwargs):
        super().__init__(**kwargs)
        self.id = _id
        self.holder = holder
        self.holder_type = holder_type
        self.allow_method = allow_method
        self.status = status
        self.expiration_time = None
        self.effective_time = None
