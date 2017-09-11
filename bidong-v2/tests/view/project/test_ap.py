import random

from bidong.core.database import session
from bidong.storage.models import AP, Tag

from tests.view import ApiTestCase, fake


def load_tags(pn):
    tags = [
        {"pn": pn, "tag_type": "ap", "name": "AP标签1"},
        {"pn": pn, "tag_type": "ap", "name": "AP标签2"},
        {"pn": pn, "tag_type": "ap", "name": "AP标签3"},
        {"pn": pn, "tag_type": "ap", "name": "AP标签4"},
    ]
    tag_id_list = []
    for kw in tags:
        t = Tag(**kw)
        session.add(t)
        session.commit()
        tag_id_list.append(t.id)
    return tag_id_list


class APApiTestCase(ApiTestCase):
    api = "project"
    url_pattern = '/v1.0/projects/{}/aps'
    related_models = [AP, Tag]

    def setUp(self):
        super().setUp()
        self.pn = 12
        self.url = self.url_pattern.format(self.pn)
        self.tags = load_tags(self.pn)

    def tearDown(self):
        super().tearDown()

    def test_scenario(self):
        payload = {
            "name": "AP", "address": "address", "mac": "lili", "tags": []}
        resp = self.json_post(self.url, payload=payload)
        self.assertEqual(resp.code, 400)

        expected_total = 20
        for n in range(expected_total):
            vendor = random.choice(['H3C', 'Huawei', 'Hanming'])
            idx = n % len(self.tags)
            payload = {
                "name": "AP-{}".format(n),
                "address": fake.street_name(),
                "mac": fake.mac_address(),
                "vendor": vendor,
                "tags": self.tags[:idx]
            }
            print(payload)
            resp = self.json_post(self.url, payload=payload)
            self.assertEqual(resp.code, 200)

        count = session.query(AP).count()
        self.assertEqual(count, expected_total)

        session.query(AP).filter(AP.name.in_(['AP-1', 'AP-3', 'AP-5'])).update(
            {"is_online": 1}, synchronize_session=False
        )
        session.commit()
        count = session.query(AP.id).filter_by(is_online=1).count()
        self.assertEqual(count, 3)

        url = '{}/overview'.format(self.url)
        resp = self.get(url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total'], expected_total)
        self.assertEqual(resp.json['online'], 3)

        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], expected_total)
        self.assertEqual(len(resp.json['objects']), expected_total)

        resp = self.get(self.url, query={"online": 1})
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 3)

        resp = self.get(self.url, query={"tag": self.tags[0]})
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 15)

        resp = self.get(self.url, query={"keyword": "AP-5"})
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 1)

        ap = resp.json['objects'][0]
        url = '{}/{}'.format(self.url, ap['id'])
        resp = self.get(url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['name'], 'AP-5')
        self.assertEqual(len(resp.json['tags']), 1)

        payload = {"name": "Bidong-AP", "mac": fake.mac_address(),
                   "address": fake.street_name(), "vendor": "Ruijie",
                   "tags": []}
        resp = self.json_put(url, payload=payload)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        resp = self.get(url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['tags']), 0)
        self.assertEqual(resp.json['name'], payload['name'])
        self.assertEqual(resp.json['mac'], payload['mac'].upper())
        self.assertEqual(resp.json['address'], payload['address'])
        self.assertEqual(resp.json['vendor'], payload['vendor'])

        resp = self.delete(url)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], expected_total - 1)
        self.assertEqual(len(resp.json['objects']), expected_total - 1)
