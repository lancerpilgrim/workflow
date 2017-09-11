import xlsxwriter
from io import BytesIO
from datetime import datetime

from tornado import gen
from tornado.web import asynchronous

from bidong.service.billing import OrderService
from bidong.service.coupon import CouponAdminService
from bidong.service.account import gen_account_export_data
from bidong.view.platform import Resource


class ExcelApi(Resource):
    genfunc = None
    args = None
    kwargs = None

    @gen.coroutine
    def create_excel(self, headers, content):
        """生成excel文件
        Args:
            filename: excel文件名
            headers: excel表头部, 列表
            content: excel内容，二维矩阵
        """
        output = BytesIO()
        wb = xlsxwriter.Workbook(output, {"in_memory": True})
        ws = wb.add_worksheet("sheet 1")

        for idx, col in enumerate(headers):
            ws.write(0, idx, col)

        for row_num, line in enumerate(content):
            for col_num, col in enumerate(line):
                ws.write(row_num + 1, col_num, col)

        wb.close()
        output.seek(0)
        return output.read()

    @gen.coroutine
    def excel_response(self, filename):
        """返回excel binary data
        Args:
            context: dict, {"filename": "", "headers": [], "content": []}
        """
        self.args = self.args if self.args else []
        self.kwargs = self.kwargs if self.kwargs else {}
        future = self.genfunc(*self.args, **self.kwargs)
        headers, content = future.result()

        future = self.create_excel(headers, content)
        output = future.result()

        self.set_header(
            'Content-Type',
            'application/vnd.ms-excel; charset="utf-8"'
        )
        self.set_header(
            'Content-Disposition',
            'attachment; filename={}'.format(filename))
        self.set_header(
            'Content-Length', len(output))
        self.write(output)
        self.finish()


class OrderExcelApi(ExcelApi):

    @asynchronous
    @gen.engine
    def get(self):
        """
        ---
        summary: 导出平台收款记录
        description: 导出平台收款记录
        tags:
            - excel
        produces:
            - application/vnd.ms-excel
        parameters:
            - in: query
              name: begin
              type: string
              required: true
              description: 开始日期, 日期格式YYYY-mm-dd
            - in: query
              name: end
              type: string
              required: true
              description: 结束日期, 日期格式YYYY-mm-dd
            - in: query
              name: keyword
              type: string
              description: 套餐名
            - in: query
              name: project_id
              type: string
              description: 项目ID，为0是导出属于平台的收款记录
        responses:
            200:
                description: OK
            500:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("财务管理")

        begin = self.smart_query_get(
            "begin", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        end = self.smart_query_get(
            "end", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        project_id = self.smart_query_get("project_id", datatype=int,
                                          allow_none=True)
        keyword = self.smart_query_get("keyword", allow_none=True)

        filename = "orders.xls"
        self.genfunc = OrderService(is_platform=True).gen_platform_order_data
        self.args = (begin, end, keyword, project_id)

        yield gen.Task(self.excel_response, filename)


class CouponExcelApi(ExcelApi):

    @asynchronous
    @gen.engine
    def get(self):
        """
        ---
        summary: 导出新创建的兑换码列表
        description: 导出新创建的兑换码列表
        tags:
            - excel
        produces:
            - application/vnd.ms-excel
        parameters:
            - in: query
              name: serial
              type: integer
              required: true
              description: 序列号名
        responses:
            200:
                description: OK
            500:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("财务管理")

        managerid = self.get_current_user_id()
        serial = self.smart_query_get('serial', datatype=int)

        filename = 'coupons.xls'
        self.genfunc = CouponAdminService(managerid).gen_serial_coupons_data
        self.args = (serial,)

        yield gen.Task(self.excel_response, filename)


class AccountExcelApi(ExcelApi):

    @asynchronous
    @gen.engine
    def get(self):
        """
        ---
        summary: 导出平台用户
        description: 导出平台用户
        tags:
            - excel
        produces:
            - application/vnd.ms-excel
        parameters:
            - in: query
              name: project
              type: integer
              description: 项目ID
            - in: query
              name: online
              type: integer
              description: 是否在线，0 -离线, 1 - 在线
            - in: query
              name: tag
              type: integer
              description: 标签 id
            - in: query
              name: keyword
              type: string
              description: 用户姓名或手机号
        responses:
            200:
                description: OK
            500:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("用户管理")

        project = self.smart_query_get(
            "project", datatype=int, allow_none=True)
        online = self.smart_query_get("online", datatype=int, allow_none=True)
        tag = self.smart_query_get("tag", datatype=int, allow_none=True)
        keyword = self.smart_query_get("keyword", allow_none=True)

        filename = 'users.xls'
        self.genfunc = gen_account_export_data
        self.args = (project, online, tag, keyword)

        yield gen.Task(self.excel_response, filename)
