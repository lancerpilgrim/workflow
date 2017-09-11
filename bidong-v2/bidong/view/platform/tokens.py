from bidong.service.uploader import QiniuService
from bidong.view.platform import Resource


class QiniuUploadTokenApi(Resource):

    def get(self):
        """
        ---
        summary: 获取七牛上传token
        description: 获取七牛上传token
        tags:
            - tool
        responses:
            200:
                description: 七牛前端上传token
                schema:
                    type: object
                    properties:
                        uptoken:
                            type: string
                            description: 前端上传所需的uptoken
        """
        uptoken = QiniuService().gen_upload_token()
        self.response(payload={"uptoken": uptoken})
