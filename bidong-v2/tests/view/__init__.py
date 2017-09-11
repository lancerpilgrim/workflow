import json
import warnings
from urllib.parse import urlencode

import faker
from tornado.testing import AsyncHTTPTestCase

from server import make_app
from bidong.core.database import session

warnings.simplefilter('ignore', ResourceWarning)

fake = faker.Factory.create("zh_CN")


class Response(object):

    def __init__(self, httpclient_response):
        self.body = httpclient_response.body
        self.json = json.loads(httpclient_response.body.decode())
        self.code = httpclient_response.code


class RequestMixin:
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Tornado/Test'
    }

    def get(self, url, query=None, headers=None):
        if query is not None and isinstance(query, dict):
            url = url + "?" + urlencode(query)
        print('GET => ', url)
        headers = headers.update(self.headers) if headers else self.headers
        return Response(self.fetch(url, headers=headers))

    def delete(self, url, headers=None):
        headers = headers.update(self.headers) if headers else self.headers
        return Response(self.fetch(url, method='DELETE', headers=headers))

    def json_post(self, url, payload, headers=None):
        headers = headers.update(self.headers) if headers else self.headers
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        return Response(
            self.fetch(url, method='POST', headers=headers, body=payload))

    def json_put(self, url, payload, headers=None):
        headers = headers.update(self.headers) if headers else self.headers

        if isinstance(payload, dict):
            payload = json.dumps(payload)
        return Response(
            self.fetch(url, method='PUT', headers=headers, body=payload))


class ApiTestCase(AsyncHTTPTestCase, RequestMixin):

    api = ""
    related_models = []

    def _clean_tables(self):
        for model in self.related_models:
            session.query(model).delete()
        session.commit()

    def setUp(self):
        self._clean_tables()
        super(ApiTestCase, self).setUp()

    def tearDown(self):
        self._clean_tables()
        super(ApiTestCase, self).tearDown()

    def get_app(self):
        return make_app(self.api)
