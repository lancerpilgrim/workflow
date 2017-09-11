from datetime import datetime

from bidong.core.validates import validate_with_schema
from bidong.service.message import LetterService
from bidong.service.coupon import CouponAdminService
from bidong.view.platform import schemas
from bidong.view.platform import Resource


class LetterListApi(Resource):

    def get(self):
        """获取平台站内信列表
        ---
        summary: 获取站内信列表
        description: 获取站内信列表
        tags:
            - operation
        parameters:
            - in: query
              name: page
              type: integer
              description: 当前页数
            - in: query
              name: page_size
              type: integer
              description: 每页大小
            - in: query
              name: status
              type: integer
              required: true
              description: 站内信状态, 0 - 草稿， 1 - 已发
        responses:
            200:
                description: 站内信列表
                schema:
                    $ref: '#definitions/LetterList'
            500:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("运营管理")

        page = self.smart_query_get("page", datatype=int, default=1)
        page_size = self.smart_query_get("page_size", datatype=int, default=20)
        status = self.smart_query_get(
            "status", datatype=int, default=1, validate=lambda x: x in (0, 1))

        paginator = LetterService.list(page, page_size, status)
        rvs, _ = schemas.LetterListSchema().dump(paginator)

        self.response(payload=rvs)

    def post(self):
        """
        ---
        summary: 创建站内信
        description: 创建站内信
        tags:
            - operation
        consumes:
            - application/json
        parameters:
            - in: body
              name: letter
              description: 站内信内容
              schema:
                $ref: '#definitions/Letter'
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

        data = validate_with_schema(
            schemas.LetterSchema, self.request_body_dict)
        letter_id = LetterService.generate(
            self.get_current_user_id(),
            data.title, data.content, data.status
        )

        self.response(payload={"id": letter_id})


class LetterApi(Resource):

    def get(self, letter_id):
        """
        ---
        summary: 获取站内信详情
        description: 获取站内信详情
        tags:
            - operation
        parameters:
            - in: path
              name: letter_id
              required: true
              type: integer
              description: 站内信id
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/Letter'
            404:
                description: NOT FOUND
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("运营管理")

        record = LetterService.detail(letter_id)
        rvs, _ = schemas.LetterSchema().dump(record)

        self.response(payload=rvs)

    def put(self, letter_id):
        """
        ---
        summary: 修改站内信草稿
        description: 修改站内信草稿
        tags:
            - operation
        consumes:
            - application/json
        parameters:
            - in: path
              name: letter_id
              required: true
              type: integer
              description: 站内信id

            - in: body
              name: letter
              description: 站内信内容
              schema:
                $ref: '#definitions/Letter'
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
            400:
                description: BAD REQUEST
                schema:
                    $ref: '#definitions/Api400Error'
            404:
                description: NOT FOUND
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("运营管理")

        data = validate_with_schema(
            schemas.LetterSchema, self.request_body_dict)
        letter_id = LetterService.update(
            letter_id, data.title, data.content, data.status)

        self.response(payload={"id": letter_id})

    def delete(self, letter_id):
        """
        ---
        summary: 删除站内信
        description: 删除站内信
        tags:
            - operation
        parameters:
            - in: path
              name: letter_id
              required: true
              type: integer
              description: 站内信id
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """
        self.check_permision("运营管理")

        LetterService.delete(letter_id)
        self.response()


class CouponListApi(Resource):

    def get(self):
        """
        ---
        summary: 获取兑换码列表
        description: 获取兑换码列表
        tags:
            - operation
        parameters:
            - in: query
              name: page
              type: integer
              description: 当前页数
            - in: query
              name: page_size
              type: integer
              description: 每页大小
            - in: query
              name: status
              type: integer
              description: 兑换码状态，不填为全部, 0 - 未兑换, 1 - 已兑换, 2 - 已过期
        responses:
            200:
                description: 兑换码列表
                schema:
                    $ref: '#definitions/CouponList'
        """
        self.check_permision("运营管理")

        page = self.smart_query_get('page', datatype=int, default=1)
        page_size = self.smart_query_get('page_size', datatype=int, default=20)
        status = self.smart_query_get('status', datatype=int, allow_none=True)

        managerid = self.get_current_user_id()
        coupons = CouponAdminService(managerid).list(
            page, page_size, status
        )
        payload = schemas.CouponListSchema().dump(coupons).data

        self.response(payload=payload)

    def post(self):
        """
        ---
        summary: 新建兑换码
        description: 新建一批兑换码
        tags:
            - operation
        consumes:
            - application/json
        parameters:
            - in: body
              name: letter
              description: 站内信内容
              schema:
                $ref: '#definitions/Coupon'
        responses:
            200:
                description: OK
                schema:
                    type: object
                    properties:
                        serial:
                            type: integer
                            description: 兑换码序列号
        """
        self.check_permision("运营管理")

        managerid = self.get_current_user_id()
        datas = validate_with_schema(
            schemas.CouponSchema, self.request_body_dict
        )

        serial = CouponAdminService(managerid).generate(
            datas.hours, datas.count, datas.expired
        )

        self.response(payload={"serial": serial})


class CouponSerialListApi(Resource):

    def get(self, serial):
        """
        ---
        summary: 获取新创建兑换码列表
        description: 获取新创建兑换码列表
        tags:
            - operation
        parameters:
            - in: path
              name: serial
              required: true
              type: integer
              description: 新一批兑换码序列号
            - in: query
              name: page
              type: integer
              description: 当前页数
            - in: query
              name: page_size
              type: integer
              description: 每页大小
        responses:
            200:
                description: 新创建兑换码列表
                schema:
                    $ref: '#definitions/SerialCouponList'
        """
        self.check_permision("运营管理")

        managerid = self.get_current_user_id()
        page = self.smart_query_get('page', datatype=int, default=1)
        page_size = self.smart_query_get('page_size', datatype=int, default=20)

        coupons = CouponAdminService(managerid).list_by_serial(
            serial, page, page_size
        )
        payload = schemas.SerialCouponListSchema().dump(coupons).data

        self.response(payload=payload)


class CouponDataTableApi(Resource):

    def get(self):
        """
        ---
        summary: 获取兑换码运营统计数据
        description: 获取兑换码运营统计数据
        tags:
            - operation
        parameters:
            - in: query
              name: begin
              type: string
              required: true
              description: 开始日期, 格式 YYYY-mm-dd
            - in: query
              name: end
              type: string
              required: true
              description: 结束日期, 格式 YYYY-mm-dd
            - in: query
              name: manager
              type: integer
              description: 管理员ID
            - in: query
              name: page
              type: integer
              description: 当前页数
            - in: query
              name: page_size
              type: integer
              description: 每页大小
        responses:
            200:
                description: 新创建兑换码列表
                schema:
                    $ref: '#definitions/CouponDataList'
        """
        self.check_permision("运营管理")

        managerid = self.get_current_user_id()
        begin = self.smart_query_get(
            "begin", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        end = self.smart_query_get(
            "end", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        page = self.smart_query_get('page', datatype=int, default=1)
        page_size = self.smart_query_get('page_size', datatype=int, default=20)
        manager = self.smart_query_get(
            'manager', datatype=int, allow_none=True)

        rvs = CouponAdminService(managerid).aggregate(
            begin, end, page, page_size, manager
        )
        payload = schemas.CouponDataListSchema().dump(rvs).data

        self.response(payload=payload)


class CouponOverviewApi(Resource):

    def get(self):
        """
        ---
        summary: 获取兑换码统计
        description: 获取兑换码统计
        tags:
            - operation
        responses:
            200:
                description: 兑换码总数据
                schema:
                    type: object
                    properties:
                        total:
                            type: integer
                        usable:
                            type: integer
                        used:
                            type: integer
                        expired:
                            type: integer
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("运营管理")

        managerid = self.get_current_user_id()
        begin = self.smart_query_get(
            "begin", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        end = self.smart_query_get(
            "end", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))

        payload = CouponAdminService(managerid).overview(begin, end)
        self.response(payload=payload)
