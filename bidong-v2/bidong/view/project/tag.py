from bidong.core.validates import validate_with_schema
from bidong.service import tag as tag_service
from bidong.view import sharedschemas
from bidong.view.project import Resource


class TagListApi(Resource):

    def get(self, project_id):
        """
        ---
        summary: 获取标签列表
        description: 获取标签列表
        tags:
            - tag
        parameters:
            - in: query
              name: type
              type: string
              required: true
              description: 标签类型, 选项 [account, ap]
            - in: path
              name: project_id
              type: integer
              required: true
              description: 项目ID
        responses:
            200:
                description: 标签列表
                schema:
                    $ref: '#definitions/TagList'
            500:
                description: 出错信息
                schema:
                    $ref: '#definitions/ApiError'
        """
        tag_type = self.smart_query_get('type')
        rvs = tag_service.list_tag(tag_type, project_id)
        payload = sharedschemas.TagListSchema().dump(
            {"tags": rvs}).data

        self.response(payload=payload)

    def post(self, project_id):
        """
        ---
        description: 创建标签
        summary: 创建新标签
        tags:
            - tag
        consumes:
            - application/json
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 项目ID
            - in: body
              name: name
              description: 标签名
              schema:
                $ref: '#definitions/Tag'
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
        data = validate_with_schema(
            sharedschemas.TagSchema, self.request_body_dict)
        tag_id = tag_service.create_tag(data.tag_type, data.name, project_id)
        self.response(payload={"id": tag_id})


class TagApi(Resource):

    def delete(self, project_id, tag_id):
        """
        ---
        description: 删除标签
        summary: 删除标签
        tags:
            - tag
        parameters:
            - in: path
              name: project_id
              type: integer
              required: true
              description: 项目ID
            - in: path
              name: tag_id
              required: true
              type: integer
              description: 标签id
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """
        tag_service.delete_tag(int(tag_id), int(project_id))
        self.response()
