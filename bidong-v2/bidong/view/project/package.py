from bidong.core.validates import validate_with_schema
from bidong.core.exceptions import DuplicateError
from bidong.service.package import PackageService
from bidong.view.project import schemas
from bidong.view.project import Resource


class PackageListApi(Resource):

    def get(self, project_id):
        """
        ---
        summary: 获取套餐列表
        description: 获取套餐列表
        tags:
            - billing
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
              description: 套餐名搜索
        responses:
            200:
                description: 当前项目的套餐列表
                schema:
                    $ref: '#definitions/PackageList'
            500:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("计费管理", project_id)

        page = self.smart_query_get('page', datatype=int, default=1)
        page_size = self.smart_query_get('page_size', datatype=int, default=20)
        keyword = self.smart_query_get('keyword', allow_none=True)

        paginator = PackageService(project_id).list(keyword, page, page_size)
        payload = schemas.PackageListSchema().dump(paginator).data

        self.response(payload=payload)

    def post(self, project_id):
        """
        ---
        summary: 新增项目套餐
        description: 新增项目套餐
        tags:
            - billing
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
              description: 套餐信息
              schema:
                $ref: '#definitions/Package'
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
        self.check_permision("计费管理", project_id)

        data = validate_with_schema(
            schemas.PackageSchema, self.request_body_dict)

        created = PackageService(project_id).create(
            data.name, data.price, data.ends,
            time=data.time, expired=data.expired, available_until=data.until,
            tags=data.tag_list
        )
        if not created:
            raise DuplicateError("已存在同名套餐")

        self.response()


class PackageApi(Resource):

    def get(self, project_id, package_id):
        """
        ---
        summary: 获取套餐详情
        description: 获取套餐详情
        tags:
            - billing
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: package_id
              type: integer
              description: 套餐ID
        responses:
            200:
                description: 套餐详情
                schema:
                    $ref: '#definitions/Package'
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("计费管理", project_id)

        p = PackageService(project_id).get(package_id)
        payload = schemas.PackageSchema().dump(p).data

        self.response(payload=payload)

    def put(self, project_id, package_id):
        """
        ---
        summary: 编辑套餐
        description: 更新套餐有效期和投放标签
        tags:
            - billing
        consumes:
            - application/json
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: package_id
              type: integer
              required: true
              description: 用户ID
            - in: body
              name: package
              required: true
              description: 套餐投放标签ID列表或到期时间，可只填一项
              schema:
                $ref: '#definitions/PackageUpdate'
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
        self.check_permision("计费管理", project_id)

        data = validate_with_schema(
            schemas.PackageUpdateSchema, self.request_body_dict
        )

        PackageService(project_id).update(
            package_id, data.until, data.tag_list)
        self.response()

    def delete(self, project_id, package_id):
        """
        ---
        summary: 删除套餐
        description: 删除套餐
        tags:
            - billing
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: path
              name: package_id
              required: true
              type: integer
              description: 套餐ID
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """
        self.check_permision("计费管理", project_id)

        PackageService(project_id).delete(package_id)
        self.response()
