from bidong.core.validates import validate_with_schema
from bidong.service import tag as tag_service
from bidong.view import sharedschemas
from bidong.view.platform import Resource


class TagListApi(Resource):

    def get(self):
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
              description: 标签类型, 选项 [account, ap]
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
        tag_type = self.get_query_argument('type', '')
        rvs = tag_service.list_tag(tag_type)
        payload = sharedschemas.TagListSchema().dump({"tags": rvs}).data

        self.response(payload=payload)

    def post(self):
        """
        ---
        summary: 创建标签
        description: 创建标签
        tags:
            - tag
        consumes:
            - application/json
        parameters:
            - in: body
              name: letter
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
        tag_id = tag_service.create_tag(data.tag_type, data.name)
        self.response(payload={"id": tag_id})


class TagApi(Resource):

    def delete(self, tag_id):
        """
        ---
        summary: 删除标签
        description: 删除标签
        tags:
            - tag
        parameters:
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
        tag_service.delete_tag(tag_id)
        self.response()
