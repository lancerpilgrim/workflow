from bidong.core.database import session
from bidong.storage.models import NetworkConfig
from tests.view import ApiTestCase


class NetworkTestCase(ApiTestCase):
    api = "project"
    url_pattern = "/v1.0/projects/{pid}/networks"
    related_models = [NetworkConfig]

    def setUp(self):
        super().setUp()
        self.pn = 12
        self.url = self.url_pattern.format(pid=self.pn)

    def tearDown(self):
        super().tearDown()

    def test_package_scenario(self):
        resp = self.json_post(self.url, payload={})
        self.assertEqual(resp.code, 400)

        kwargs = {
            "is_public": 0, "is_free": 0, "mask": 0,
            "portal_id": 1, "ssid": "Bidong1", "duration": 12,
            "session_timeout": 24
        }
        resp = self.json_post(self.url, payload=kwargs)
        self.assertEqual(resp.code, 200)
        resp = self.json_post(self.url, payload=kwargs)
        self.assertEqual(resp.code, 409)

        kwargs = {
            "is_public": 0, "is_free": 0, "mask": 1,
            "portal_id": 1, "ssid": "Bidong2", "duration": 12,
            "session_timeout": 24, "wechat_account_id": 1
        }
        resp = self.json_post(self.url, payload=kwargs)
        self.assertEqual(resp.code, 200)

        kwargs = {
            "is_public": 1, "is_free": 0, "mask": 3,
            "portal_id": 1, "ssid": "Bidong3", "duration": 12,
            "session_timeout": 24, "wechat_account_id": 1
        }
        resp = self.json_post(self.url, payload=kwargs)
        self.assertEqual(resp.code, 200)

        kwargs = {
            "is_public": 1, "is_free": 0, "mask": 7,
            "portal_id": 1, "ssid": "Bidong4", "duration": 12,
            "session_timeout": 24, "wechat_account_id": 1
        }
        resp = self.json_post(self.url, payload=kwargs)
        self.assertEqual(resp.code, 200)

        count = session.query(NetworkConfig).count()
        self.assertEqual(count, 4)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        print('resp => ', resp.json)
        self.assertEqual(resp.json['total_items'], 4)
        self.assertEqual(len(resp.json['objects']), 4)

        resp = self.get(self.url, query={"keyword": "Bidong4"})
        self.assertEqual(resp.code, 200)
        print('resp => ', resp.json)
        self.assertEqual(len(resp.json['objects']), 1)
        config = resp.json['objects'][0]
        self.assertEqual(config['mask'], kwargs['mask'])
        self.assertEqual(config['portal_id'], kwargs['portal_id'])

        _id = config['id']
        url = "{}/{}".format(self.url, _id)
        resp = self.get(url)
        print('resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(config['ssid'], resp.json['ssid'])
        self.assertEqual(config['mask'], resp.json['mask'])

        kwargs = {
            "is_public": 0, "is_free": 1, "mask": 3,
            "portal_id": 12, "ssid": "Bidong5", "duration": 30,
            "session_timeout": 48, "wechat_account_id": 12
        }
        resp = self.json_put(url, payload=kwargs)
        self.assertEqual(resp.code, 200)

        resp = self.get(url)
        print('resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(kwargs['is_public'], resp.json['is_public'])
        self.assertEqual(kwargs['is_free'], resp.json['is_free'])
        self.assertEqual(kwargs['mask'], resp.json['mask'])
        self.assertEqual(kwargs['portal_id'], resp.json['portal_id'])
        self.assertEqual(kwargs['ssid'], resp.json['ssid'])
        self.assertEqual(kwargs['duration'], resp.json['duration'])
        self.assertEqual(kwargs['session_timeout'],
                         resp.json['session_timeout'])
        self.assertEqual(kwargs['wechat_account_id'],
                         resp.json['wechat_account_id'])

        resp = self.delete(url)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        print('resp => ', resp.json)
        self.assertEqual(resp.json['total_items'], 3)
        self.assertEqual(len(resp.json['objects']), 3)
