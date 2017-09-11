from copy import copy

from bidong.core.database import session
from bidong.storage.models import WechatOfficialAccount
from tests.view import ApiTestCase


class PortalTestCase(ApiTestCase):
    api = "project"
    url_pattern = "/v1.0/projects/{pid}/wechat-accounts"
    related_models = [WechatOfficialAccount]

    def setUp(self):
        super().setUp()
        self.pn = 12
        self.url = self.url_pattern.format(pid=self.pn)

    def tearDown(self):
        super().tearDown()

    def test_scenario(self):
        template = {
            "name": "account-{}", "appid": "appid-{}", "shopid": "shopid-{}",
            "secret": "secret-{}", "note": "note-{}"
        }

        for n in range(10):
            kwargs = copy(template)
            for key in kwargs:
                kwargs[key] = kwargs[key].format(n)
            resp = self.json_post(self.url, payload=kwargs)
            self.assertEqual(resp.code, 200)

        count = session.query(WechatOfficialAccount).count()
        self.assertEqual(count, 10)

        # test list
        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 10)
        self.assertEqual(len(resp.json['objects']), 10)

        url = '{}/{}'.format(self.url, 'fields')
        resp = self.get(url, query={"select": "id,name,amount"})
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['objects']), 10)
        self.assertEqual(len(resp.json['objects'][0].keys()), 2)

        resp = self.get(self.url, query={"keyword": "account-0"})
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 1)

        wechat_id = resp.json['objects'][0]['id']
        url = '{}/{}'.format(self.url, wechat_id)
        payload = copy(template)
        for key in payload:
            payload[key] = payload[key].format(100)
        resp = self.json_put(url, payload=payload)
        self.assertEqual(resp.code, 200)
        resp = self.get(self.url, query={"keyword": "account-100"})
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 1)

        resp = self.delete(url)
        self.assertEqual(resp.code, 200)
        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 9)
        resp = self.get(self.url, query={"keyword": "account-100"})
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 0)
