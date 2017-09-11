from settings import version
from bidong.view.platform import (
    tag,
    user,
    package,
    billing,
    operations,
    excel,
    portal,
    tokens,
    bas,
    projects,
    managers,
    administrators,
    login,
    test
)


routers = [
    (r'^/v1.0/tags$', tag.TagListApi),
    (r'^/v1.0/tags/(\d+)$', tag.TagApi),

    (r'^/v1.0/portals$', portal.PortalListApi),
    (r'^/v1.0/portals/(\d+)$', portal.PortalApi),

    (r'^/v1.0/acs$', bas.ACListApi),
    (r'^/v1.0/acs/(\d+)$', bas.ACApi),

    (r'^/v1.0/users$', user.UserListApi),
    (r'^/v1.0/users/(\d+)$', user.UserDetailApi),
    (r'^/v1.0/users/(\d+)/profiles$', user.UserProjectProfileApi),
    (r'^/v1.0/users/overview$', user.UserOverviewApi),
    (r'^/v1.0/users/tags$', user.UserTagApi),

    (r'^/v1.0/packages$', package.PackageListApi),
    (r'^/v1.0/packages/(\d+)$', package.PackageApi),

    (r'^/v1.0/orders$', billing.OrderListApi),
    (r'^/v1.0/orders/overview$', billing.OrderOverviewApi),
    (r'^/v1.0/orders/chart$', billing.OrderChartApi),

    (r'^/v1.0/letters$', operations.LetterListApi),
    (r'^/v1.0/letters/(\d+)$', operations.LetterApi),

    (r'^/v1.0/coupons$', operations.CouponListApi),
    (r'^/v1.0/coupons/serials/(\d+)$', operations.CouponSerialListApi),
    (r'^/v1.0/coupons/overview$', operations.CouponOverviewApi),
    (r'^/v1.0/coupons/data-table$', operations.CouponDataTableApi),

    (r'^/v1.0/files/orders.xls$', excel.OrderExcelApi),
    (r'^/v1.0/files/coupons.xls$', excel.CouponExcelApi),
    (r'^/v1.0/files/users.xls$', excel.AccountExcelApi),

    (r'^/v1.0/token/qiniu-uptoken$', tokens.QiniuUploadTokenApi),

    (r'/v1.0/projects$', projects.ProjectsHandler),
    (r'/v1.0/projects/(?P<project_id>\d+)$', projects.ProjectHandler),
    (r'/v1.0/projects/(?P<project_id>\d+)/authorizations$', projects.ProjectAuthorizationHandler),
    (r'/v1.0/projects/(?P<project_id>\d+)/overviews$', projects.ProjectOverviewHandler),
    (r'/v1.0/projects-resources$', projects.ProjectsFeaturesHandler),

    (r'/v1.0/administrators$', administrators.AdministratorsHandler),
    (r'/v1.0/administrators/(?P<administrator_id>\d+)$', administrators.AdministratorHandler),
    (r'/v1.0/administrators/(?P<administrator_id>\d+)/overviews$', administrators.AdministratorOverviewsHandler),
    (r'/v1.0/administrators/(?P<administrator_id>\d+)/authorizations$',
     administrators.AdministratorAuthorizationsHandler),
    (r'/v1.0/administrators-resources$', administrators.AdministratorsFeaturesHandler),

    (r'/v1.0/managers$', managers.ManagersHandler),
    (r'/v1.0/managers/(?P<manager_id>\d+)$', managers.ManagerHandler),
    (r'/v1.0/managers/(?P<manager_id>\d+)/overviews$', managers.ManagerOverviewsHandler),
    (r'/v1.0/managers/(?P<manager_id>\d+)/authorizations$', managers.ManagerAuthorizationsHandler),
    (r'/v1.0/sessions$', login.LoginHandler),

    # 测试链接
    (r'/{version}/test/administrators$'.format(version=version),
     test.AdministratorsHandler),
    (r'/{version}/test/administrators/(?P<administrator_id>\d+)$'.format(version=version),
     test.AdministratorHandler),
    (r'/{version}/test/administrators/(?P<administrator_id>\d+)/overviews$'.format(version=version),
     test.AdministratorOverviewsHandler),
    (r'/{version}/test/administrators/(?P<administrator_id>\d+)/authorizations$'.format(version=version),
     test.AdministratorAuthorizationsHandler),

]
