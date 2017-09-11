from bidong.core.validates import validate_with_schema
from bidong.service.operations import WechatOfficialAccountService
from bidong.view.project import schemas
from bidong.view.project import Resource


class WechatAccountListApi(Resource):

    def get(self, project_id):
        """
        ---
        summary: 获取公众号列表
        description: 获取公众号列表
        tags:
            - operations
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
              name: page_size
              type: integer
              description: 每页条数
            - in: query
              name: keyword
              type: string
              description: 公众号名称等搜索
        responses:
            200:
                description: 公众号列表
                schema:
                    $ref: '#definitions/WechatAccountList'
            400:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("微信公众号管理", project_id)

        page = self.smart_query_get("page", datatype=int, default=1)
        page_size = self.smart_query_get("page_size", datatype=int, default=20)
        keyword = self.smart_query_get('keyword', allow_none=True)

        paginator = WechatOfficialAccountService(project_id).list(
            page, page_size, keyword
        )
        payload = schemas.WechatAccountListSchema().dump(paginator).data
        self.response(payload=payload)

    def post(self, project_id):
        """
        ---
        summary: 新增公众号
        description: 新增公众号
        tags:
            - operations
        consumes:
            - application/json
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: body
              name: wechat_account
              required: true
              description: 套餐信息
              schema:
                $ref: '#definitions/WechatAccount'
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
        self.check_permision("微信公众号管理", project_id)

        datas = validate_with_schema(
            schemas.WechatAccountSchema, self.request_body_dict
        )
        _id = WechatOfficialAccountService(project_id).create(
            datas.name, datas.appid, datas.shopid, datas.secret, datas.note
        )
        self.response(payload={"id": _id})


class WechatAccountFieldsApi(Resource):

    def get(self, project_id):
        """
        ---
        summary: 获取公众号选定字段值
        description: 获取公众号选定字段值, 不分页
        tags:
            - operations
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: query
              name: select
              required: true
              type: string
              description: 用逗号拼接的选定字段, 如id,name
        responses:
            200:
                description: 选定字段的公众号列表
                schema:
                    $ref: '#definitions/WechatAccountFields'
            400:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("项目管理", project_id)

        fields = self.smart_query_get('select')
        datas = WechatOfficialAccountService(project_id).list_select_fields(
            fields
        )
        self.response(payload={"objects": datas})


class WechatAccountApi(Resource):

    def put(self, project_id, wechat_id):
        """
        ---
        summary: 更新公众号
        description: 更新公众号
        tags:
            - operations
        consumes:
            - application/json
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: wechat_id
              type: integer
              required: true
              description: 公众号id
            - in: body
              name: wechat_account
              required: true
              description: 公众号内容
              schema:
                $ref: '#definitions/WechatAccount'
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
        self.check_permision("微信公众号管理", project_id)

        datas = validate_with_schema(
            schemas.WechatAccountSchema, self.request_body_dict
        )

        WechatOfficialAccountService(project_id).update(
            int(wechat_id),
            datas.name, datas.appid, datas.shopid, datas.secret, datas.note
        )
        self.response()

    def delete(self, project_id, wechat_id):
        """
        ---
        summary: 删除公众号
        description: 删除公众号
        tags:
            - operations
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: wechat_id
              required: true
              type: integer
              description: 公众号ID
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """
        self.check_permision("微信公众号管理", project_id)

        WechatOfficialAccountService(project_id).delete(wechat_id)
        self.response()
