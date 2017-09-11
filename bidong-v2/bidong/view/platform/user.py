from bidong.core.validates import validate_with_schema
from bidong.service import account
from bidong.view.platform import schemas
from bidong.view.platform import Resource


class UserOverviewApi(Resource):
    def get(self):
        """
        ---
        summary: 获取项目用户数据
        description: 获取项目用户数据
        tags:
            - user
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
                        today_register:
                            type: integer
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("用户管理")

        rvs = account.account_overview()
        self.response(payload=rvs)


class UserListApi(Resource):

    def get(self):
        """
        ---
        summary: 获取平台用户列表
        description: 获取平台用户列表
        tags:
            - user
        parameters:
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
              name: project
              type: integer
              required: false
              description: 项目id
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
            default:
                description: Error
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("用户管理")

        page = self.smart_query_get("page", datatype=int, default=1)
        page_size = self.smart_query_get("page_size", datatype=int, default=20)
        project = self.smart_query_get(
            "project", datatype=int, allow_none=True)
        online = self.smart_query_get("online", datatype=int, allow_none=True)
        tag = self.smart_query_get("tag", datatype=int, allow_none=True)
        keyword = self.smart_query_get("keyword", allow_none=True)

        paginator = account.account_list(
            page, page_size, project, online, tag, keyword)
        rvs = schemas.UserListSchema().dump(paginator).data
        self.response(payload=rvs)


class UserDetailApi(Resource):

    def get(self, account_id):
        """
        ---
        summary: 获取平台用户详情
        description: 获取项目用户详情
        tags:
            - user
        parameters:
            - in: path
              name: account_id
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
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("用户管理")

        detail = account.base_profile(account_id)
        payload = schemas.UserDetailSchema().dump(detail).data
        self.response(payload=payload)

    def put(self, account_id):
        """
        ---
        summary: 更新平台用户标签
        description: 更新平台用户标签
        tags:
            - user
        consumes:
            - application/json
        parameters:
            - in: path
              name: account_id
              type: integer
              required: true
              description: 用户ID
            - in: body
              name: tags
              required: true
              description: 用户tag id
              schema:
                $ref: '#definitions/UserTagList'
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
        self.check_permision("用户管理")

        data = validate_with_schema(
            schemas.UserTagListSchema, self.request_body_dict
        )
        account.attach_tags(account_id, data['tags'], reset=True)
        self.response()


class UserTagApi(Resource):

    def post(self):
        """
        ---
        summary: 批量贴标签
        description: 给用户批量贴标签
        tags:
            - user
        consumes:
            - application/json
        parameters:
            - in: body
              name: attached_tags
              required: true
              description: 用户id和标签id
              schema:
                $ref: '#definitions/AttachedTag'
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
        self.check_permision("用户管理")

        data = validate_with_schema(
            schemas.AttachedTagSchema, self.request_body_dict
        )
        account_id_list = data['accounts']
        for aid in account_id_list:
            account.attach_tags(aid, data["tags"])

        self.response()


class UserProjectProfileApi(Resource):

    def get(self, account_id):
        """
        ---
        summary: 获取用户项目资料
        description: 获取用户项目资料
        tags:
            - user
        parameters:
            - in: path
              name: account_id
              type: integer
              description: 用户ID
        responses:
            200:
                description: 项目用户项目资料
                schema:
                    $ref: '#definitions/Profiles'
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("用户管理")

        profiles = account.project_profiles(account_id)
        payload = schemas.ProfilesSchema().dump(
            {"objects": profiles}
        ).data

        self.response(payload=payload)
