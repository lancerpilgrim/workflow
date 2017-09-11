from bidong.view.project import (
    ap,
    tag,
    user,
    login,
    excel,
    tokens,
    portal,
    network,
    package,
    billing,
    message,
    projects,
    managers,
    operations
)


routers = [
    (r'^/v1.0/projects/(\d+)/tags$', tag.TagListApi),
    (r'^/v1.0/projects/(\d+)/tags/(\d+)$', tag.TagApi),

    (r'^/v1.0/projects/(\d+)/networks$', network.NetworkListApi),
    (r'^/v1.0/projects/(\d+)/networks/(\d+)$', network.NetworkApi),

    (r'^/v1.0/projects/(\d+)/aps$', ap.APListApi),
    (r'^/v1.0/projects/(\d+)/aps/overview$', ap.APOverviewApi),
    (r'^/v1.0/projects/(\d+)/aps/(\d+)$', ap.APApi),

    (r'^/v1.0/projects/(\d+)/users/overview$', user.UserOverviewApi),
    (r'^/v1.0/projects/(\d+)/users/profiles$', user.UserProfileListApi),
    (r'^/v1.0/projects/(\d+)/users/profiles/(\d+)$', user.UserProfileApi),
    (r'^/v1.0/projects/(\d+)/users/custom-attr$', user.UserCustomAttrApi),
    (r'^/v1.0/projects/(\d+)/users/visitors$', user.VisitorUserListApi),

    (r'^/v1.0/projects/(\d+)/packages$', package.PackageListApi),
    (r'^/v1.0/projects/(\d+)/packages/(\d+)$', package.PackageApi),

    (r'^/v1.0/projects/(\d+)/orders$', billing.OrderListApi),
    (r'^/v1.0/projects/(\d+)/orders/overview$', billing.OrderOverviewApi),
    (r'^/v1.0/projects/(\d+)/orders/chart$', billing.OrderChartApi),

    (r'^/v1.0/projects/(\d+)/portals$', portal.PortalListApi),
    (r'^/v1.0/projects/(\d+)/portals/(\d+)$', portal.PortalApi),

    (r'^/v1.0/projects/(\d+)/wechat-accounts$',
     operations.WechatAccountListApi),
    (r'^/v1.0/projects/(\d+)/wechat-accounts/fields$',
     operations.WechatAccountFieldsApi),
    (r'^/v1.0/projects/(\d+)/wechat-accounts/(\d+)$',
     operations.WechatAccountApi),

    (r'^/v1.0/messages$', message.MessageListApi),
    (r'^/v1.0/messages/notify$', message.MessageNotifyApi),
    (r'^/v1.0/messages/(\d+)$', message.MessageApi),

    (r'^/v1.0/projects/(\d+)/import/users', excel.ImportAccountApi),
    (r'^/v1.0/projects/(\d+)/files/template.xls$', excel.ExcelTemplateApi),
    (r'^/v1.0/projects/(\d+)/files/orders.xls$', excel.OrderExcelApi),
    (r'^/v1.0/projects/(\d+)/files/users.xls$', excel.AccountExcelApi),

    (r'^/v1.0/token/qiniu-uptoken$', tokens.QiniuUploadTokenApi),

    (r'/v1.0/projects/(?P<project_id>\d+)$', projects.ProjectHandler),
    (r'/v1.0/projects/(?P<project_id>\d+)/authorizations$', projects.ProjectAuthorizationHandler),
    (r'/v1.0/projects/(?P<project_id>\d+)/overviews$', projects.ProjectOverviewHandler),
    (r'/v1.0/projects/(?P<project_id>\d+)/brief$', projects.ProjectBriefHandler),

    (r'/v1.0/projects/(?P<project_id>\d+)/managers$', managers.ManagersHandler),
    (r'/v1.0/projects/(?P<project_id>\d+)/managers/(?P<manager_id>\d+)$', managers.ManagerHandler),
    (r'/v1.0/projects/(?P<project_id>\d+)/managers/(?P<manager_id>\d+)/overviews$', managers.ManagerOverviewsHandler),
    (r'/v1.0/projects/(?P<project_id>\d+)/managers/(?P<manager_id>\d+)/authorizations',
     managers.ManagerAuthorizationsHandler),

    (r'/v1.0/managers/(?P<manager_id>\d+)/projects', managers.ManagerProjectsHandler),

    (r'/v1.0/sessions$', login.LoginHandler)
]
