from datetime import datetime

from bidong.service.billing import OrderService
from bidong.view.platform import schemas
from bidong.view.platform import Resource


class OrderListApi(Resource):

    def get(self):
        """
        ---
        summary: 获取收款记录
        description: 获取收款记录
        tags:
            - billing
        parameters:
            - in: query
              name: begin
              type: string
              required: true
              description: 开始日期，格式示例 2017-08-01
            - in: query
              name: end
              type: string
              required: true
              description: 截止日期，格式示例 2017-08-30
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
            - in: query
              name: project_id
              type: integer
              description: 项目id
        responses:
            200:
                description: 收款记录
                schema:
                    $ref: '#definitions/OrderList'
            400:
                description: 出错信息
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("财务管理")

        begin = self.smart_query_get(
            "begin", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        end = self.smart_query_get(
            "end", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        page = self.smart_query_get("page", datatype=int, default=1)
        page_size = self.smart_query_get("page_size", datatype=int, default=20)
        keyword = self.smart_query_get("keyword", allow_none=True)
        project_id = self.smart_query_get(
            "project_id", datatype=int, allow_none=True)

        paginator = OrderService(is_platform=True).list(
            begin, end, page, page_size, keyword, project_id
        )
        payload = schemas.OrderListSchema().dump(paginator).data

        self.response(payload=payload)


class OrderOverviewApi(Resource):

    def get(self):
        """
        ---
        summary: 获取收款统计
        description: 获取收款统计
        tags:
            - billing
        responses:
            200:
                description: 平台总收款统计
                schema:
                    type: object
                    properties:
                        today_amount:
                            type: number
                        total_amount:
                            type: number
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("财务管理")

        payload = OrderService(is_platform=True).overview()
        self.response(payload=payload)


class OrderChartApi(Resource):

    def get(self):
        """
        ---
        summary: 获取收款日统计数据
        description: 获取收款日统计数据
        tags:
            - billing
        parameters:
            - in: query
              name: begin
              type: string
              required: true
              description: 开始日期，格式示例 2017-08-01
            - in: query
              name: end
              type: string
              required: true
              description: 截止日期，格式示例 2017-08-30
            - in: query
              name: project_id
              type: integer
              description: 项目ID
        responses:
            200:
                description: 收款日统计
                schema:
                    $ref: '#definitions/OrderChart'
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/Api400Error'
        """
        self.check_permision("财务管理")

        begin = self.smart_query_get(
            "begin", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        end = self.smart_query_get(
            "end", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        project_id = self.smart_query_get(
            "project_id", datatype=int, allow_none=True)

        data = OrderService(is_platform=True).chart(begin, end, project_id)
        payload = schemas.OrderChartSchema().dump(data).data

        self.response(payload=payload)
