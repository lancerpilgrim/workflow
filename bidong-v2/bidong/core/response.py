OK = 200
CREATED = 201
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
CONFLICT = 409
TYPE_UNSUPPORTED = 415
SERVER_ERROR = 500
NOT_IMPLEMENTED = 501

HTTP_STATUS_CODE_MESSAGE = {
    OK: "OK",
    CREATED: "CREATED",
    BAD_REQUEST: "请求参数错误或数据格式错误",
    UNAUTHORIZED: "用户未授权",
    FORBIDDEN: "用户没有权限",
    NOT_FOUND: "请求资源不存在",
    CONFLICT: "资源已存在",
    TYPE_UNSUPPORTED: "请求数据格式错误, 请使用正确的Content-Type",
    SERVER_ERROR: "服务不可用",
    NOT_IMPLEMENTED: "服务端不支持该方法"
}


class Context:

    def __init__(self, status_code=None, message=None, payload=None, **kwargs):
        self.status_code = status_code or OK
        self.message = message or HTTP_STATUS_CODE_MESSAGE[self.status_code]
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())

        if self.message is not None:
            rv["message"] = self.message

        rv["status_code"] = self.status_code

        return rv

    def to_xml(self):
        pass
