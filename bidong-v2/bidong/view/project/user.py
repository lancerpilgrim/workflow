from bidong.core.validates import validate_with_schema
from bidong.core.exceptions import DuplicateError

from bidong.service import account
from bidong.service.account import ProjectAccountService
from bidong.view.project import schemas
from bidong.view.project import Resource


class UserCustomAttrApi(Resource):

    def get(self, project_id):
        """
        ---
        summary: 获取项目用户自定义属性
        description: 获取项目用户自定义属性
        tags:
            - user
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
        responses:
            200:
                description: 用户自定义属性
                schema:
                    $ref: '#definitions/DyncolList'
            500:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("用户管理", project_id)

        default = account.get_default_dyncol()
        setted = ProjectAccountService(project_id).get_dyncol()

        rvs = schemas.DyncolListSchema().dump(
            {"default": default, "setted": setted}
        ).data
        self.response(payload=rvs)

    def post(self, project_id):
        """
        ---
        summary: 设置用户自定义属性
        description: 设置用户自定义属性
        tags:
            - user
        consumes:
            - application/json
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: body
              name: letter
              required: true
              description: 自定义属性id 列表
              schema:
                $ref: '#definitions/DyncolIdList'
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
            400:
                description: BAD REQUEST
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("用户管理", project_id)

        data = validate_with_schema(
            schemas.DyncolIdListSchema, self.request_body_dict)

        ProjectAccountService(project_id).set_dyncol(data["cols"])
        self.response()


class UserProfileListApi(Resource):

    def get(self, project_id):
        """
        ---
        summary: 获取项目用户列表
        description: 获取项目用户列表
        tags:
            - user
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: query
              name: page
              type: integer
              description: 当前页
            - in: query
              name: online
              type: integer
              required: false
              description: 是否在线, 0 - 离线, 1 - 在线
            - in: query
              name: tag
              type: integer
              required: false
              description: 标签id
            - in: query
              name: keyword
              type: string
              required: false
              description: 姓名或者手机号搜索
        responses:
            200:
                description: 项目用户列表
                schema:
                    $ref: '#definitions/UserList'
            400:
                description: Bad Request
                schema:
                    $ref: '#definitions/Api400Error'
            500:
                description: Server Error
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("用户管理", project_id)

        page = self.smart_query_get("page", datatype=int, default=1)
        page_size = self.smart_query_get("page_size", datatype=int, default=20)
        tag_id = self.smart_query_get("tag", datatype=int, allow_none=True)
        online = self.smart_query_get("online", datatype=int, allow_none=True)
        keyword = self.smart_query_get(
            "keyword", datatype=str, allow_none=True)

        paginator = ProjectAccountService(project_id).fetch(
           online, tag_id, keyword, page, page_size
        )
        rvs = schemas.UserListSchema().dump(paginator).data
        self.response(payload=rvs)

    def post(self, project_id):
        """
        ---
        summary: 新增用户
        description: 创建项目用户
        tags:
            - user
        consumes:
            - application/json
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: body
              name: user
              required: true
              description: 用户信息
              schema:
                $ref: '#definitions/User'
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
            400:
                description: BAD REQUEST
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("用户管理", project_id)

        data = validate_with_schema(
            schemas.UserSchema, self.request_body_dict)

        created = ProjectAccountService(project_id).create(
            data.name, data.mobile, data.attrs, data.tags
        )
        if not created:
            raise DuplicateError("用户已经存在")

        self.response()

    def delete(self, project_id):
        """
        ---
        summary: 批量删除用户
        description: 批量删除项目用户
        tags:
            - user
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: query
              name: choice
              required: true
              type: string
              description: 要删除的用户ID列表，ID直接用逗号隔开, choice=1,2,3,4
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """
        self.check_permision("用户管理", project_id)

        choice = self.smart_query_get("choice", datatype=str)

        ids = [int(rv) for rv in choice.split(',') if rv.strip().isdigit()]
        ProjectAccountService(project_id).delete_profile(batch_delete=ids)
        self.response()


class UserProfileApi(Resource):
    def get(self, project_id, profile_id):
        """
        ---
        summary: 用户详情
        description: 获取项目用户详情
        tags:
            - user
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: profile_id
              type: integer
              description: 用户ID
        responses:
            200:
                description: 项目用户详情
                schema:
                    $ref: '#definitions/UserDetail'
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("用户管理", project_id)

        profile = ProjectAccountService(project_id).get_profile(profile_id)

        rvs = schemas.UserDetailSchema().dump(profile).data
        self.response(payload=rvs)

    def put(self, project_id, profile_id):
        """
        ---
        summary: 编辑用户
        description: 更新项目用户
        tags:
            - user
        consumes:
            - application/json
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: profile_id
              type: integer
              required: true
              description: 用户ID
            - in: body
              name: user
              required: true
              description: 项目用户信息
              schema:
                $ref: '#definitions/User'
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
            400:
                description: BAD REQUEST
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("用户管理", project_id)

        data = validate_with_schema(
            schemas.UserSchema, self.request_body_dict
        )
        ProjectAccountService(project_id).update(
            profile_id, data.mobile, data.name, data.attrs, data.tags
        )
        self.response()

    def delete(self, project_id, profile_id):
        """
        ---
        summary: 删除用户
        description: 删除项目用户
        tags:
            - user
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: profile_id
              required: true
              type: integer
              description: 用户ID
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """
        self.check_permision("用户管理", project_id)

        ProjectAccountService(project_id).delete_profile(profile_id=profile_id)
        self.response()


class UserOverviewApi(Resource):
    def get(self, project_id):
        """
        ---
        summary: 获取项目用户数据
        description: 获取项目用户数据
        tags:
            - user
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
        responses:
            200:
                description: 项目用户统计
                schema:
                    type: object
                    properties:
                        total_user:
                            type: integer
                        online_user:
                            type: integer
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("用户管理", project_id)

        rvs = ProjectAccountService(project_id).overview()
        self.response(payload=rvs)


class VisitorUserListApi(Resource):
    def get(self, project_id):
        """
        ---
        summary: 在线访客
        description: 获取项目在线访客
        tags:
            - user
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: query
              name: page
              type: integer
              description: 当前页
            - in: query
              name: keyword
              type: string
              required: false
              description: 姓名或者手机号搜索
        responses:
            200:
                description: 项目用户列表
                schema:
                    $ref: '#definitions/VisitorUserList'
            400:
                description: Bad Request
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("用户管理", project_id)

        page = self.smart_query_get('page', datatype=int, default=1)
        page_size = self.smart_query_get('page_size', datatype=int, default=20)
        keyword = self.smart_query_get('keyword', allow_none=True)

        vistor_list = ProjectAccountService(project_id).list_visitors(
            keyword, page, page_size)
        payload = schemas.VisitorUserListSchema().dump(vistor_list).data
        self.response(payload=payload)

    def put(self, project_id):
        """
        ---
        summary: 下线在线访客
        description: 更新项目用户
        tags:
            - user
        consumes:
            - application/json
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: query
              name: userid
              type: integer
              required: true
              description: 在线访客id
            - in: query
              name: action
              type: string
              required: true
              description: 将游客下线, action=offline
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
            400:
                description: BAD REQUEST
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("用户管理", project_id)

        userid = self.smart_query_get('userid', datatype=int)
        action = self.smart_query_get('action', allow_none=True)

        if action == 'offline':
            ProjectAccountService(project_id).kick_out_visitor(userid)
        self.response()
