from bidong.core.validates import validate_with_schema
from bidong.service.portal import PortalService
from bidong.view.platform import schemas
from bidong.view.platform import Resource


class PortalListApi(Resource):

    def get(self):
        """
        ---
        summary: 获取portal页配置列表
        description: 获取portal配置列表
        tags:
            - operation
        responses:
            200:
                description: 平台portal列表
                schema:
                    $ref: '#definitions/PortalList'
        """
        self.check_permision("运营管理")

        items = PortalService(is_platform=True).list()

        payload = schemas.PortalListSchema().dump(
            {"objects": items}
        ).data
        self.response(payload=payload)

    def post(self):
        """
        ---
        summary: 新增portal页配置
        description: 新增portal页配置
        tags:
            - operation
        consumes:
            - application/json
        parameters:
            - in: body
              name: package
              required: true
              description: portal页配置
              schema:
                $ref: '#definitions/Portal'
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
        self.check_permision("运营管理")

        datas = validate_with_schema(
            schemas.PortalSchema, self.request_body_dict
        )
        created = PortalService(is_platform=True).create(
            datas.name, datas.note, datas.mobile_title,
            datas.mobile_banner_url, datas.pc_title, datas.pc_banner_url
        )

        self.response(payload={"id": created})


class PortalApi(Resource):

    def get(self, portal_id):
        """
        ---
        summary: 获取portal页配置
        description: 获取portal页配置
        tags:
            - operation
        parameters:
            - in: path
              name: portal_id
              type: integer
              description: portal配置id
        responses:
            200:
                description: portal配置详情
                schema:
                    $ref: '#definitions/Portal'
        """
        self.check_permision("运营管理")

        item = PortalService(is_platform=True).get(portal_id)

        payload = schemas.PortalSchema().dump(item).data
        self.response(payload=payload)

    def put(self, portal_id):
        """
        ---
        summary: 更新portal页配置
        description: 更新portal页配置
        tags:
            - operation
        consumes:
            - application/json
        parameters:
            - in: path
              name: portal_id
              type: integer
              required: true
              description: portal配置ID
            - in: query
              name: using
              type: integer
              description: 是否设为默认, 1 - 设为默认，当链接中这个参数using=1时会忽略body提交的内容
            - in: body
              name: package
              required: true
              description: portal页配置, 与query参数二选其一
              schema:
                $ref: '#definitions/Portal'
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
        self.check_permision("运营管理")

        using = self.smart_query_get('using', datatype=int, allow_none=True)
        service = PortalService(is_platform=True)
        if using == 1:
            service.using(portal_id)
        else:
            datas = validate_with_schema(
                schemas.PortalSchema, self.request_body_dict
            )
            PortalService(is_platform=True).update(
                portal_id,
                datas.name, datas.note, datas.mobile_title,
                datas.mobile_banner_url, datas.pc_title, datas.pc_banner_url
            )

        self.response()

    def delete(self, portal_id):
        """
        ---
        summary: 删除portal页配置
        description: 删除portal页配置
        tags:
            - operation
        parameters:
            - in: path
              name: portal_id
              required: true
              type: integer
              description: portal配置表
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """
        self.check_permision("运营管理")

        PortalService(is_platform=True).delete(portal_id)
        self.response()
