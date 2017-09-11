from datetime import datetime, timedelta

from bidong.core.database import session
from bidong.storage.models import CouponCode, CouponSerial
from tests.view import ApiTestCase


class CouponTestCase(ApiTestCase):
    api = "platform"
    related_models = [CouponCode, CouponSerial]
    url = '/v1.0/coupons'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def timestamp(self, offset=0):
        day = datetime.now() + timedelta(days=offset)
        return day.strftime("%Y-%m-%d")

    def test_scenario(self):
        resp = self.json_post(self.url, payload={"count": 200})
        self.assertEqual(resp.code, 400)

        payload = {
            "hours": 5, "count": 200, "expired": self.timestamp(30)
        }

        resp = self.json_post(self.url, payload=payload)
        self.assertEqual(resp.code, 200)
        self.assertIsNotNone(resp.json.get('serial'))
        serial = resp.json['serial']
        print('serial => ', serial)

        url = '{}/serials/{}'.format(self.url, serial)
        resp = self.get(url, query={"page_size": 20})
        print('resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 200)
        self.assertEqual(len(resp.json['objects']), 20)
        self.assertEqual(len(resp.json['objects'][0].keys()), 3)

        payload = {
            "hours": 10, "count": 120, "expired": self.timestamp(-5)
        }
        resp = self.json_post(self.url, payload=payload)
        self.assertEqual(resp.code, 200)
        count = session.query(CouponCode).count()
        self.assertEqual(count, 320)
        print('Total count => ', count)

        resp = self.get(self.url, query={"page_size": 20})
        print('resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 320)
        self.assertEqual(len(resp.json['objects']), 20)
        self.assertEqual(len(resp.json['objects'][0].keys()), 5)

        resp = self.get(self.url, query={"page_size": 20, "status": 2})
        print('expired resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 120)
        resp = self.get(self.url, query={"page_size": 20, "status": 1})
        print('expired resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 0)
        resp = self.get(self.url, query={"page_size": 20, "status": 0})
        print('expired resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 200)

        url = '{}/data-table'.format(self.url)
        resp = self.get(
            url, query={"begin": self.timestamp(-5), "end": self.timestamp(5)})
        print('resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 1)
        self.assertEqual(len(resp.json['objects']), 1)
        self.assertEqual(resp.json['objects'][0]['usable'], 1000)
        self.assertEqual(resp.json['objects'][0]['used'], 0)
        self.assertEqual(resp.json['objects'][0]['expired'], 1200)
        self.assertEqual(resp.json['objects'][0]['total'], 2200)

        url = '{}/overview'.format(self.url)
        resp = self.get(
            url, query={"begin": self.timestamp(-5), "end": self.timestamp(5)})
        print('resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total'], 2200)
        self.assertEqual(resp.json['usable'], 1000)
        self.assertEqual(resp.json['used'], 0)
        self.assertEqual(resp.json['expired'], 1200)
