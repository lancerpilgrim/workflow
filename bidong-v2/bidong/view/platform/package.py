from bidong.core.validates import validate_with_schema
from bidong.core.exceptions import DuplicateError

from bidong.service.package import PackageService
from bidong.view.platform import schemas
from bidong.view.platform import Resource


class PackageListApi(Resource):

    def get(self):
        """
        ---
        summary: 获取套餐列表
        description: 获取套餐列表
        tags:
            - billing
        parameters:
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
        self.check_permision("财务管理")

        page = self.smart_query_get('page', datatype=int, default=1)
        page_size = self.smart_query_get('page_size', datatype=int, default=20)
        keyword = self.smart_query_get('keyword', allow_none=True)

        paginator = PackageService(is_platform=True).list(
            keyword, page, page_size)
        payload = schemas.PackageListSchema().dump(paginator).data
        self.response(payload=payload)

    def post(self):
        """
        ---
        summary: 新增套餐
        description: 新增套餐
        tags:
            - billing
        consumes:
            - application/json
        parameters:
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
        self.check_permision("财务管理")

        data = validate_with_schema(
            schemas.PackageSchema, self.request_body_dict)

        created = PackageService(is_platform=True).create(
            data.name, data.price, data.ends,
            mask=data.mask, time=data.time, available_until=data.until,
            tags=data.tag_list, apply_projects=data.project_list
        )
        if not created:
            raise DuplicateError("已存在同名套餐")

        self.response()


class PackageApi(Resource):

    def get(self, package_id):
        """
        ---
        summary: 获取套餐详情
        description: 获取套餐详情
        tags:
            - billing
        parameters:
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
        self.check_permision("财务管理")

        p = PackageService(is_platform=True).get(package_id)
        payload = schemas.PackageSchema().dump(p).data

        self.response(payload=payload)

    def put(self, package_id):
        """
        ---
        summary: 编辑套餐
        description: 更新套餐有效期和投放标签和投放项目
        tags:
            - billing
        consumes:
            - application/json
        parameters:
            - in: path
              name: package_id
              type: integer
              required: true
              description: 用户ID
            - in: body
              name: package
              required: true
              description: 更新套餐到期时间，投放标签和项目
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
        self.check_permision("财务管理")

        data = validate_with_schema(
            schemas.PackageUpdateSchema, self.request_body_dict
        )

        PackageService(is_platform=True).update(
            package_id, data.until, data.tag_list, data.project_list)
        self.response()

    def delete(self, package_id):
        """
        ---
        summary: 删除套餐
        description: 删除套餐
        tags:
            - billing
        parameters:
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
        self.check_permision("财务管理")

        PackageService(is_platform=True).delete(package_id)
        self.response()
