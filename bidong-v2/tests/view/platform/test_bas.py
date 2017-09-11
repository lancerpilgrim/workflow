import random

from bidong.core.database import session
from bidong.storage.models import AC
from tests.view import ApiTestCase
from tests.view import fake


class BasTestCase(ApiTestCase):
    api = "platform"
    url = "/v1.0/acs"
    related_models = [AC]

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_scenario(self):
        resp = self.json_post(self.url, payload={})
        self.assertEqual(resp.code, 400)

        resp = self.json_post(self.url, payload={
            "name": "AC", "vendor": "H3C", "ip": "77", "secret": "xx"
        })
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 400)

        for n in range(20):
            vendor = random.choice(['H3C', 'Ruijie', 'Huawei'])
            kwargs = {
                "name": "AC-{}".format(n),
                "vendor": vendor,
                "ip": fake.ipv4(),
                "secret": fake.pystr(max_chars=20)
            }
            resp = self.json_post(self.url, payload=kwargs)
            self.assertEqual(resp.code, 200)

        resp = self.json_post(self.url, payload=kwargs)
        self.assertEqual(resp.code, 409)

        count = session.query(AC).count()
        self.assertEqual(count, 20)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertEqual(len(resp.json['objects']), 20)

        ac_id = resp.json['objects'][0]['id']
        url = '{}/{}'.format(self.url, ac_id)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertEqual(resp.json['name'], 'AC-0')

        kwargs = {
            "name": "AC-100",
            "vendor": "Huawei",
            "ip": fake.ipv4(),
            "secret": fake.pystr(max_chars=20)
        }
        resp = self.json_put(url, payload=kwargs)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        for key in kwargs:
            self.assertEqual(resp.json[key], kwargs[key])

        resp = self.delete(url)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertEqual(len(resp.json['objects']), 19)
