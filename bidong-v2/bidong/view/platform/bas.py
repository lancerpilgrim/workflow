from bidong.core.validates import validate_with_schema

from bidong.service.bas import ACService
from bidong.view.platform import schemas
from bidong.view.platform import Resource


class ACListApi(Resource):

    def get(self):
        """
        ---
        summary: 获取AC列表
        description: 获取AC列表
        tags:
            - project
        responses:
            200:
                description: AC列表
                schema:
                    $ref: '#definitions/ACList'
        """
        self.check_permision("项目管理")

        keyword = self.smart_query_get('keyword', allow_none=True)
        items = ACService.list(keyword)

        payload = schemas.ACListSchema().dump(
            {"objects": items}
        ).data
        self.response(payload=payload)

    def post(self):
        """
        ---
        summary: 新增AC
        description: 新增AC
        tags:
            - project
        consumes:
            - application/json
        parameters:
            - in: body
              name: ac
              required: true
              description: AC配置
              schema:
                $ref: '#definitions/AC'
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
        self.check_permision("项目管理")

        datas = validate_with_schema(
            schemas.ACSchema, self.request_body_dict
        )

        created = ACService().create(
            datas.name, datas.vendor, datas.ip, datas.secret
        )
        self.response(payload={"id": created})


class ACApi(Resource):

    def get(self, ac_id):
        """
        ---
        summary: 获取AC详情
        description: 获取AC详情
        tags:
            - project
        parameters:
            - in: path
              name: ac_id
              type: integer
              description: AC id
        responses:
            200:
                description: AC详情
                schema:
                    $ref: '#definitions/AC'
        """
        self.check_permision("项目管理")

        ac = ACService().get(ac_id)
        payload = schemas.ACSchema().dump(ac).data

        self.response(payload=payload)

    def put(self, ac_id):
        """
        ---
        summary: 更新AC
        description: 更新AC
        tags:
            - project
        consumes:
            - application/json
        parameters:
            - in: path
              name: ac_id
              type: integer
              required: true
              description: AC ID
            - in: body
              name: ac
              required: true
              description: 更新AC信息
              schema:
                $ref: '#definitions/AC'
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
        self.check_permision("项目管理")

        datas = validate_with_schema(
            schemas.ACSchema, self.request_body_dict
        )

        ACService().update(
            ac_id,
            datas.name, datas.vendor, datas.ip, datas.secret
        )
        self.response()

    def delete(self, ac_id):
        """
        ---
        summary: 删除AC
        description: 删除AC
        tags:
            - project
        parameters:
            - in: path
              name: ac_id
              required: true
              type: integer
              description: AC ID
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """
        self.check_permision("项目管理")

        success = ACService().delete(ac_id)

        self.response(payload={"success": success})
