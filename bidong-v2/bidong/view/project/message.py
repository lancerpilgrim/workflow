from bidong.service.message import MailboxService
from bidong.view.project import Resource
from bidong.view.project import schemas


class MessageNotifyApi(Resource):

    def get(self):
        """
        ---
        summary: 获取未读站内信
        description: 获取未读站内信
        tags:
            - message
        responses:
            200:
                description: 系统提示
                schema:
                    type: object
                    properties:
                        unread:
                            type: integer
                            description: 未读站内信条数
        """
        count = MailboxService(self.get_current_user_id()).unread_count()
        self.response(payload={"unread": count})


class MessageListApi(Resource):

    def get(self):
        """
        ---
        summary: 获取站内信列表
        description: 获取站内信列表
        tags:
            - message
        parameters:
            - in: query
              name: page
              type: integer
              description: 当前页
            - in: query
              name: page_size
              type: integer
              description: 每页条数
        responses:
            200:
                description: 站内信列表
                schema:
                    $ref: '#definitions/MessageList'
        """
        page = self.smart_query_get("page", datatype=int, default=1)
        page_size = self.smart_query_get("page_size", datatype=int, default=20)
        paginator = MailboxService(self.get_current_user_id()).list(
            page, page_size)

        payload = schemas.MessageListSchema().dump(paginator).data
        self.response(payload=payload)


class MessageApi(Resource):

    def get(self, message_id):
        """
        ---
        summary: 获取站内信详情
        description: 获取站内信详情
        tags:
            - message
        parameters:
            - in: path
              name: message_id
              type: integer
              required: true
              description: 消息ID
        responses:
            200:
                description: 消息详情
                schema:
                    $ref: '#definitions/Message'
            404:
                description: Not Found
                schema:
                    $ref: '#definitions/ApiError'
        """
        manager_id = self.get_current_user_id()
        message = MailboxService(manager_id).read(message_id)

        payload = schemas.MessageSchema().dump(message).data
        self.response(payload=payload)

    def delete(self, message_id):
        """
        ---
        summary: 删除站内信
        description: 删除站内信
        tags:
            - message
        parameters:
            - in: path
              name: message_id
              required: true
              type: integer
              description: 站内信ID
        responses:
            200:
                description: OK
                schema:
                    $ref: '#definitions/ApiSuccess'
        """

        manager_id = self.get_current_user_id()
        MailboxService(manager_id).delete(message_id)

        self.response()
