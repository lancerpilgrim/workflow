from bidong.service.v2.repo import ResourcesQuery


def __map_resource_name():
    _ = {}
    __ = {}
    r = ResourcesQuery()
    all_resources = r.get_all_resources().all()
    for each in all_resources:
        if each.ascription == 1:
            _[each.private_name] = each.public_name
        elif each.ascription == 2:
            __[each.private_name] = each.public_name
    return _, __


PLATFORM_RESOURCES_MAP, CLIENT_RESOURCES_MAP = __map_resource_name()
REVERSED_PLATFORM_RESOURCES_MAP = {v: k for k, v in PLATFORM_RESOURCES_MAP.items()}
REVERSED_CLIENT_RESOURCES_MAP = {v: k for k, v in CLIENT_RESOURCES_MAP.items()}


# ###################################################################################

# # 权限和状态变动的业务规则
#
# ## Projects
#
# 0.
# 只有administrator可以操作项目权限
#
# 1.
# project的overviews.status
# 发生变更，整个项目状态改变:
#
# 1.1
# project_authorization ：auth的状态只有可用和不可用这两种 ，
# 这些权限作为一个整体的可用性由overviews去维护和校验，auth只管在整体能用时某个功能和数据能不能用，
# 管理员的权限也是同理，所以project_authorization不改变；
#
# 1.2
# manager_authorization
# 根据resource_locator = project_id
# 的所有权限同步变更状态;
#
# 2.
# project_authorization的某条记录status发生变更（一般是进行删除操作）：
#
# 2.1
# manager_authorization, 根据resource_locator = project_id,
# resource_name = resource_name
# 的记录同步变更，因为manager的auth是project的auth的子集;
#
# ## Managers
#
# 3.
# 在platform上由administrator操作新建manager时，
#
# 3.1
# 可选项目范围不能列出已经被删除的项目和已经被禁用的项目功能，只能列出可用项目的可用功能。
# 3.2
# 检查输入的resource和auth是否为对应的project下可用资源的counterpart的子集
#
# 4.
# 在client上由manager操作新建manager时，
#
# 4.1
# 可分配的权限范围是这个manager自身权限的子集。由3
# .1
# 的约束，自然也应该是project的权限子集。
#
# 5.
# manager的overviews.status变更时，不再改变对应的auth表。
#
# 6.
# manager登录之后显示的项目列表只能列出权限为可用的project。
#
# ## Administrators
#
# 6.
# administrator
# 新建时，
#
# 6.1
# 可选范围应该列出所有项目，包括已经删除的，因为可能会要求恢复
# 6.2
# 超级administrator应该能够豁免于这个机制，可以看到所有。
#
# 7.
# projects列表应该提供筛选功能，默认显示未被删除的，需要能筛选出被删除的项目
#
# ## 综合
#
# 8.
# managers和administrators
# 同6
#
# 9.
# 功能点将来很可能细分，资源将建立层级概念，每一个资源的权限都能查到一个它资源树的层级。
#
#
# 10.
# 随时根据业务需要补充
#
