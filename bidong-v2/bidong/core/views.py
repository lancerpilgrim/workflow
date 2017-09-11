import logging
import traceback

from sqlalchemy.orm.exc import NoResultFound
from tornado import web

import settings
from bidong.common.utils import extract_param, ensure_unicode
from bidong.common.utils import json_encoder, json_decoder
from bidong.core import response
from bidong.core.database import session
from bidong.core.exceptions import APIException, Error

logger = logging.getLogger('mp')


class Api404Handler(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def prepare(self):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.set_status(404)
        rv = {
            "status_code": 404,
            "message": "Error - 404"
        }
        self.finish(json_encoder(rv))


class ApiHandler(web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.session = None
        self.user_id, self.user_role, self.token = None, None, None
        self.log_base = ""

    def data_received(self, chunk):
        pass

    def prepare(self):
        request_log = ("Parameter: [request_method={0}] [response_method={1}]"
                       " [remote_ip={2}] [user_agent={3}] [user_id={4}]")
        response_method = "{0}.{1}".format(
            self.__module__, self.__class__.__name__)
        request_method = "{0} {1}".format(
            self.request.method, self.request.uri)
        # 請求信息應該放在開始，否則報錯時連請求的API都沒有記錄
        self.log_base = request_log.format(
            request_method,
            response_method,
            self.request.remote_ip,
            self.request.headers.get("User-Agent", ""),
            self.user_id
        )
        logger.info("{0} {1}".format(
            self.log_base, extract_param(self.request.arguments)
        ))

    def _handle_request_exception(self, e):
        """
        #TODO: 根据Accept返回对应格式数据
        """
        session.rollback()

        self.set_header("Content-Type", "application/json; charset=utf-8")
        if isinstance(e, Error):
            logger.error(e.to_dict())
            self.set_status(e.status_code)
            self.finish(json_encoder(e.to_dict()))
        elif isinstance(e, NoResultFound):
            rv = {
                "status_code": response.NOT_FOUND,
                "message": response.HTTP_STATUS_CODE_MESSAGE[response.NOT_FOUND]
            }
            self.set_status(response.NOT_FOUND)
            self.finish(json_encoder(rv))
        else:
            code = response.SERVER_ERROR
            message = response.HTTP_STATUS_CODE_MESSAGE[code]
            rv = {
                'status_code': code,
                'message': message,
            }
            if settings.DEBUG:
                rv['traceback'] = traceback.format_exc()

            logger.error(traceback.format_exc())
            self.set_status(code)
            self.finish(json_encoder(rv))

    def write_error(self, status_code, **kwargs):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        rv = {
            "status_code": status_code,
            "message": "Error - {}".format(status_code)
        }
        if settings.DEBUG:
            rv['traceback'] = traceback.format_exc()
        self.write(json_encoder(rv))

    def on_finish(self, *args, **kwargs):
        session.commit()
        session.close()
        logger.info("[Userid={0}] {1} {2} {3:.2f}ms".format(
            self.get_current_user_id(),
            self.request.method,
            self.request.uri,
            self.request.request_time() * 1000
        ))

    def _parse_body_as_dict(self):
        """解析请求，并将请求参数转成dict形式的参数
        """
        content_type = self.request.headers.get('Content-Type', '')
        if self.request.body:
            if content_type.startswith('application/json'):
                return json_decoder(ensure_unicode(self.request.body))
            elif content_type.startswith('multipart/form-data'):
                # 在这可以处理用 form-data处理的数据
                return {}
            else:
                raise APIException(response.TYPE_UNSUPPORTED)
        else:
            return {}

    def set_location_header(self, name):
        url = "{protocol}://{host}{uri}".format(
            protocol=self.request.protocol, host=self.request.host,
            uri=self.request.uri
        )

        self.set_header('Location', url)

    @property
    def request_body_dict(self):
        return self._parse_body_as_dict()

    def response(self, **kwargs):
        """
        #TODO: 根据Accept头部返回相应的格式数据
        """
        # accept = self.request.headers.get('Accept', '')
        self.jsonify(**kwargs)

    def jsonify(self, **kwargs):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        payload = kwargs.pop('payload', {})
        status_code = kwargs.pop("status_code", None)
        message = kwargs.pop("message", None)

        context = response.Context(
            status_code, message, payload, **kwargs
        )

        self.write(json_encoder(context.to_dict()))
        self.finish()

    @staticmethod
    def _raise_400(errors):
        payload = {"errors": errors}
        raise APIException(payload=payload, status_code=response.BAD_REQUEST)

    def smart_query_get(self, key, datatype=str, default=None,
                        allow_none=False, validate=None
                        ):
        """get parameter from url query in smart way
        Args:
            :param key: query key
            :param datatype: required data type, default is str
            :param default: default value
            :param validate: callable func or lambda
            :param allow_none: 
        """
        value = self.get_query_argument(key, None)
        if value is None:
            if default is None and not allow_none:
                errors = {key: ["This field is required."]}
                self._raise_400(errors)
            else:
                return default

        try:
            value = datatype(value)
        except:
            if default is None:
                errors = {key: ["invalid data type."]}
                self._raise_400(errors)
            else:
                return default

        if validate is not None:
            if validate(value):
                return value
            else:
                if default is None:
                    errors = {key: ["invalid data"]}
                    self._raise_400(errors)
                else:
                    return default

        return value

    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        rv = {"status_code": 405, "message": "Not Allowed"}
        self.write(json_encoder(rv))

    def post(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        rv = {"status_code": 405, "message": "Now Allowed"}
        self.write(json_encoder(rv))

    def put(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        rv = {"status_code": 405, "message": "Not Allowed"}
        self.write(json_encoder(rv))

    def delete(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        rv = {"status_code": 405, "message": "Not Allowed"}
        self.write(json_encoder(rv))

    def options(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.set_header("Allow", "GET, POST, PUT, DELETE")
        self.set_status(200)
        self.finish()


if __name__ == "__main__":
    pass
