import json
from urllib.parse import urlencode

from tornado.testing import AsyncHTTPTestCase

from server import make_app
from bidong.storage.models import Letter, Mailbox
from bidong.service.message import LetterService
from bidong.core.database import session
from tests.view import RequestMixin


class LetterListApiTestCase(AsyncHTTPTestCase, RequestMixin):

    url = '/v1.0/letters'

    def setUp(self):
        session.query(Letter).delete()
        session.query(Mailbox).delete()
        session.commit()
        super(LetterListApiTestCase, self).setUp()

    def tearDown(self):
        session.query(Letter).delete()
        session.query(Mailbox).delete()
        session.commit()

    def get_app(self):
        return make_app("platform")

    def asssert_succes_get(self, url):
        response = self.get(url)
        self.assertEqual(response.code, 200)
        return response.json

    def assert_post_return(self, url, payload, status_code):
        response = self.json_post(url, payload)
        print(response, type(response))
        self.assertEqual(response.code, status_code)
        content = json.loads(response.body.decode())
        return content

    def test_get(self):
        kwargs = {"manager_id": 1}
        for n in range(50):
            kwargs['title'] = 'title-{}'.format(n)
            kwargs['content'] = 'content-{}'.format(n)
            kwargs['status'] = n % 2
            LetterService.generate(**kwargs)

        content = self.asssert_succes_get(self.url)
        page_size = content['page_size']
        self.assertEqual(content['page'], 1)
        self.assertEqual(len(content['objects']), page_size)

        query = {"page": 2, "status": 0}
        url = self.url + "?" + urlencode(query)
        content = self.asssert_succes_get(url)
        self.assertEqual(len(content['objects']), 5)

        query = {"page": 100, "status": 0}
        url = self.url + "?" + urlencode(query)
        content = self.asssert_succes_get(url)
        self.assertEqual(len(content['objects']), 0)

        query = {"page": 1, "status": 12}
        url = self.url + "?" + urlencode(query)
        content = self.asssert_succes_get(url)
        self.assertEqual(content['page'], 1)

    def test_post_200(self):
        payload = {"title": "站内信测试", "content": "一些内容", "status": 0}
        self.assert_post_return(self.url, payload, 200)

    def test_post_400(self):
        payload = {"title": "站内信测试", "content": "一些内容"}
        content = self.assert_post_return(self.url, payload, 400)
        self.assertTrue('status' in content['errors'])

        payload = {"title": "", "content": "一些内容", "status": 0}
        content = self.assert_post_return(self.url, payload, 400)
        self.assertTrue('title' in content['errors'])

        payload = {"title": "标题", "content": "一些内容", "status": 12}
        content = self.assert_post_return(self.url, payload, 400)
        self.assertTrue('status' in content['errors'])


class LetterApiTestCase(AsyncHTTPTestCase, RequestMixin):

    url_fmt = '/v1.0/letters/{}'

    def setUp(self):
        session.query(Letter).delete()
        session.query(Mailbox).delete()
        session.commit()
        super(LetterApiTestCase, self).setUp()

    def tearDown(self):
        session.query(Letter).delete()
        session.query(Mailbox).delete()
        session.commit()

    def get_app(self):
        return make_app("platform")

    def test_get_200(self):
        kwargs = {
            "manager_id": 1, "title": "站内信草稿", "content": "这是站内信内容",
            "status": 0
        }
        letter_id = LetterService.generate(**kwargs)

        url = self.url_fmt.format(letter_id)
        response = self.get(url)
        self.assertEqual(response.code, 200)
        content = json.loads(response.body.decode())
        self.assertEqual(content['title'], kwargs['title'])

    def test_get_404(self):
        url = self.url_fmt.format(12)
        response = self.get(url)
        self.assertEqual(response.code, 404)
        json.loads(response.body.decode())

        url = self.url_fmt.format('aa')
        response = self.get(url)
        self.assertEqual(response.code, 404)
        json.loads(response.body.decode())

    def test_put(self):
        kwargs = {
            "manager_id": 1, "title": "站内信草稿", "content": "这是站内信内容",
            "status": 0
        }
        letter_id = LetterService.generate(**kwargs)
        url = self.url_fmt.format(letter_id)

        payload = {"title": "信标题", "content": "一个通知", "status": 1}
        response = self.json_put(url, payload)
        self.assertEqual(response.code, 200)
        json.loads(response.body.decode())
        letter = LetterService.detail(letter_id)
        self.assertEqual(letter.title, payload['title'])
        self.assertEqual(letter.status, payload['status'])

    def test_detete(self):
        kwargs = {
            "manager_id": 1, "title": "站内信草稿", "content": "这是站内信内容",
            "status": 0
        }
        letter_id = LetterService.generate(**kwargs)

        url = self.url_fmt.format(letter_id)
        response = self.delete(url)
        self.assertEqual(response.code, 200)
        json.loads(response.body.decode())

        letter = session.query(Letter).filter_by(
            id=letter_id, status=Letter.DELETED).one_or_none()
        self.assertIsNotNone(letter)
