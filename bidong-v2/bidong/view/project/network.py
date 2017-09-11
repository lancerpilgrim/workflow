from bidong.core.validates import validate_with_schema
from bidong.view.project import schemas
from bidong.view.project import Resource
from bidong.service.network import NetworkService


class NetworkListApi(Resource):

    def get(self, project_id):
        """
        ---
        summary: 获取项目WiFi网络配置列表
        description: 获取项目WiFi网络配置列表
        tags:
            - project
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
              description: 根据ssid或者ID搜索
        responses:
            200:
                description: 当前项目的套餐列表
                schema:
                    $ref: '#definitions/NetworkList'
        """
        self.check_permision("项目管理", project_id)

        page = self.smart_query_get('page', datatype=int, default=1)
        page_size = self.smart_query_get('page_size', datatype=int, default=20)
        keyword = self.smart_query_get('keyword', allow_none=True)

        paginator = NetworkService(project_id).list(page, page_size, keyword)
        payload = schemas.NetworkListSchema().dump(paginator).data
        self.response(payload=payload)

    def post(self, project_id):
        """
        ---
        summary: 新增WiFi网络配置
        description: 新增WiFi网络配置
        tags:
            - project
        consumes:
            - application/json
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: body
              name: package
              required: true
              description: WiFi网络配置信息
              schema:
                $ref: '#definitions/Network'
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
        self.check_permision("项目管理", project_id)

        datas = validate_with_schema(
            schemas.NetworkSchema, self.request_body_dict
        )

        config_id = NetworkService(project_id).create(
            datas.ssid, datas.portal_id, datas.duration, datas.session_timeout,
            datas.is_public, datas.is_free, datas.mask, datas.wechat_account_id
        )
        self.response(payload={"id": config_id})


class NetworkApi(Resource):

    def get(self, project_id, network_id):
        """
        ---
        summary: 获取网络配置详情
        description: 获取套餐详情
        tags:
            - project
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: network_id
              type: integer
              description: 网络配置ID
        responses:
            200:
                description: 网络配置ID
                schema:
                    $ref: '#definitions/Network'
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("项目管理", project_id)

        config = NetworkService(project_id).get(network_id)
        payload = schemas.NetworkSchema().dump(config).data

        self.response(payload=payload)

    def put(self, project_id, network_id):
        """
        ---
        summary: 更新网络配置
        description: 更新网络配置
        tags:
            - project
        consumes:
            - application/json
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: network_id
              type: integer
              required: true
              description: 网络配置ID
            - in: body
              name: package
              required: true
              description: 网络配置
              schema:
                $ref: '#definitions/Network'
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
        self.check_permision("项目管理", project_id)

        datas = validate_with_schema(
            schemas.NetworkSchema, self.request_body_dict
        )

        NetworkService(project_id).update(
            network_id,
            datas.ssid, datas.portal_id, datas.duration, datas.session_timeout,
            datas.is_public, datas.is_free, datas.mask, datas.wechat_account_id
        )
        self.response()

    def delete(self, project_id, network_id):
        """
        ---
        summary: 删除网络配置
        description: 删除网络配置
        tags:
            - project
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: network_id
              required: true
              type: integer
              description: 网络配置ID
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """
        self.check_permision("项目管理", project_id)

        success = NetworkService(project_id).delete(network_id)
        self.response(payload={"success": success})
