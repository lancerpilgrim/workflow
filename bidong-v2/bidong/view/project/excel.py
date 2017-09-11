from io import BytesIO
from datetime import datetime

import xlrd
import xlsxwriter
from tornado import gen
from tornado.web import asynchronous

from bidong.core.exceptions import LogicError
from bidong.service.billing import OrderService
from bidong.service.account import ProjectAccountService
from bidong.view.project import Resource


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


class ExcelTemplateApi(ExcelApi):
    @asynchronous
    @gen.engine
    def get(self, project_id):
        """获取导入模版
        ---
        summary: 导出导入数据模版
        description: 导出导入数据模版（如用户模版)
        tags:
            - excel
        produces:
            - application/vnd.ms-excel
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: query
              name: type
              type: string
              required: true
              description: 模版类型，支持类型 account
        responses:
            200:
                description: OK
            500:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("用户管理", project_id)

        template_type = self.smart_query_get(
            'type', validate=lambda x: x in ('account',))

        if template_type == "account":
            self.genfunc = ProjectAccountService(
                project_id).get_template_headers
            filename = 'user-template.xls'

        yield gen.Task(self.excel_response, filename)


class AccountExcelApi(ExcelApi):
    """导出和导出项目用户资料列表
    """

    @asynchronous
    @gen.engine
    def get(self, project_id):
        """获取导入模版
        ---
        summary: 导出项目用户数据数据
        description: 导出项目用户数据数据
        tags:
            - excel
        produces:
            - application/vnd.ms-excel
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
        responses:
            200:
                description: OK
            500:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("用户管理", project_id)

        online = self.smart_query_get("online", datatype=int, allow_none=True)
        tag_id = self.smart_query_get("tag", datatype=int, allow_none=True)
        keyword = self.smart_query_get("keyword", allow_none=True)

        filename = "users.xls"
        self.genfunc = ProjectAccountService(project_id).gen_export_data
        self.args = (online, tag_id, keyword)

        yield gen.Task(self.excel_response, filename)


class OrderExcelApi(ExcelApi):

    @asynchronous
    @gen.engine
    def get(self, project_id):
        """
        ---
        summary: 导出项目项目收款数据
        description: 导出项目收款数据
        tags:
            - excel
        produces:
            - application/vnd.ms-excel
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
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
        responses:
            200:
                description: OK
            500:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("计费管理", project_id)

        begin = self.smart_query_get(
            "begin", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        end = self.smart_query_get(
            "end", datatype=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        keyword = self.smart_query_get("keyword", allow_none=True)

        filename = "orders.xls"
        self.genfunc = OrderService(project_id).gen_project_order_data
        self.args = (begin, end, keyword)

        yield gen.Task(self.excel_response, filename)


class ImportAccountApi(ExcelApi):

    def post(self, project_id):
        """
        ---
        summary: 导入项目用户数据
        description: 导入项目用户数据
        tags:
            - excel
        consumes:
            - multipart/form-data
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 当前项目id
            - in: formData
              name: files
              type: file
              required: true
              description: 要导入的用户excel文件
        responses:
            200:
                description: OK
            400:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        self.check_permision("用户管理", project_id)

        binary = self.request.files['files'][0]['body']
        book = xlrd.open_workbook(file_contents=binary)
        sheet = book.sheet_by_index(0)
        row_size = sheet.nrows
        if not row_size:
            raise LogicError(400, "请按模版填写数据再导入")

        headers = sheet.row_values(0)
        content = [sheet.row_values(n) for n in range(1, row_size)]
        errors = ProjectAccountService(project_id).load_import_data(
            headers, content
        )
        self.response(payload={"errors": errors})
