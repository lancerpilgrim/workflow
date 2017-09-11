from bidong.core.validates import validate_with_schema
from bidong.service.portal import PortalService
from bidong.view.project import schemas
from bidong.view.project import Resource


class PortalListApi(Resource):

    def get(self, project_id):
        """
        ---
        summary: 获取portal页配置列表
        description: 获取portal配置列表
        tags:
            - operations
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
        responses:
            200:
                description: 当前项目的套餐列表
                schema:
                    $ref: '#definitions/PortalList'
        """
        self.check_permision("认证页管理,项目管理", project_id)

        items = PortalService(project_id).list()

        payload = schemas.PortalListSchema().dump(
            {"objects": items}
        ).data
        self.response(payload=payload)

    def post(self, project_id):
        """
        ---
        summary: 新增portal页配置
        description: 新增portal页配置
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
        self.check_permision("认证页管理", project_id)

        datas = validate_with_schema(
            schemas.PortalSchema, self.request_body_dict
        )
        created = PortalService(project_id).create(
            datas.name, datas.note, datas.mobile_title,
            datas.mobile_banner_url, datas.pc_title, datas.pc_banner_url
        )

        self.response(payload={"id": created})


class PortalApi(Resource):

    def get(self, project_id, portal_id):
        """
        ---
        summary: 获取portal页配置
        description: 获取portal页配置
        tags:
            - operations
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
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
        self.check_permision("认证页管理", project_id)

        item = PortalService(project_id).get(portal_id)

        payload = schemas.PortalSchema().dump(item).data
        self.response(payload=payload)

    def put(self, project_id, portal_id):
        """
        ---
        summary: 更新portal页配置
        description: 更新portal页配置
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
              name: portal_id
              type: integer
              required: true
              description: portal配置ID
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
        self.check_permision("认证页管理", project_id)

        datas = validate_with_schema(
            schemas.PortalSchema, self.request_body_dict
        )
        PortalService(project_id).update(
            portal_id,
            datas.name, datas.note, datas.mobile_title,
            datas.mobile_banner_url, datas.pc_title, datas.pc_banner_url
        )
        self.response()

    def delete(self, project_id, portal_id):
        """
        ---
        summary: 删除portal页配置
        description: 删除portal页配置
        tags:
            - operations
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
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
        self.check_permision("认证页管理", project_id)

        PortalService(project_id).delete(portal_id)
        self.response()
