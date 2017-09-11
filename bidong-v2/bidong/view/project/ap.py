from bidong.core.validates import validate_with_schema

from bidong.service.ap import APService
from bidong.view.project import schemas
from bidong.view.project import Resource


class APListApi(Resource):

    def get(self, project_id):
        """
        ---
        summary: 获取项目AP列表
        description: 获取项目AP列表
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
              description: 每页大小
            - in: query
              name: online
              type: integer
              description: 是否在线, 0 - 离线, 1 - 在线
            - in: query
              name: vendor
              type: string
              description: 品牌
            - in: query
              name: tag
              type: integer
              description: 标签id
            - in: query
              name: keyword
              type: string
              description: 名字、位置或者mac搜索
        responses:
            200:
                description: 项目用户列表
                schema:
                    $ref: '#definitions/APList'
            400:
                description: Server Error
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("项目管理", project_id)

        page = self.smart_query_get("page", datatype=int, default=1)
        page_size = self.smart_query_get("page_size", datatype=int, default=20)
        tag_id = self.smart_query_get("tag", datatype=int, allow_none=True)
        online = self.smart_query_get("online", datatype=int, allow_none=True)
        vendor = self.smart_query_get('vendor', allow_none=True)
        keyword = self.smart_query_get("keyword", allow_none=True)

        paginator = APService(project_id).list(
            page, page_size, online, vendor, tag_id, keyword
        )
        payload = schemas.APListSchema().dump(paginator).data
        self.response(payload=payload)

    def post(self, project_id):
        """
        ---
        summary: 新增AP
        description: 新增AP
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
              name: ap
              required: true
              description: AP信息
              schema:
                $ref: '#definitions/AP'
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
            schemas.APSchema, self.request_body_dict
        )
        apid = APService(project_id).create(
            datas.name, datas.mac.upper(), datas.address,
            datas.vendor, datas.tags
        )
        self.response(payload={"id": apid})


class APApi(Resource):

    def get(self, project_id, ap_id):
        """
        ---
        summary: AP详情
        description: 获取项目AP详情
        tags:
            - project
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: ap_id
              type: integer
              description: AP ID
        responses:
            200:
                description: 项目AP详情
                schema:
                    $ref: '#definitions/AP'
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("项目管理", project_id)

        detail = APService(project_id).get(ap_id)
        payload = schemas.APSchema().dump(detail).data
        self.response(payload=payload)

    def put(self, project_id, ap_id):
        """
        ---
        summary: 更新AP
        description: 更新AP
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
              name: ap_id
              type: integer
              required: true
              description: AP ID
            - in: body
              name: ap
              required: true
              description: AP信息
              schema:
                $ref: '#definitions/AP'
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
            schemas.APSchema, self.request_body_dict
        )
        APService(project_id).update(
            ap_id,
            datas.name, datas.mac.upper(), datas.address,
            datas.vendor, datas.tags
        )
        self.response()

    def delete(self, project_id, ap_id):
        """
        ---
        summary: 删除AP
        description: 删除AP
        tags:
            - project
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: ap_id
              required: true
              type: integer
              description: AP ID
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """
        self.check_permision("项目管理", project_id)

        APService(project_id).delete(ap_id)
        self.response()


class APOverviewApi(Resource):

    def get(self, project_id):
        """
        ---
        summary: 获取项目AP数据
        description: 获取项目AP数据
        tags:
            - project
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
        responses:
            200:
                description: 项目AP数据统计
                schema:
                    type: object
                    properties:
                        total:
                            type: integer
                            description: 总AP数
                        online:
                            type: integer
                            description: 在线AP数
                        alert:
                            type: integer
                            description: AP警报数
                        rate:
                            type: number
                            description: 授权使用率
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("项目管理", project_id)

        payload = APService(project_id).overview()
        self.response(payload=payload)
