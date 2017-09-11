from datetime import datetime, timedelta

from bidong.core.database import session
from bidong.storage.models import Package, PackageOrder, Account
from tests.view import ApiTestCase


class OrderTestCase(ApiTestCase):
    api = "project"
    related_models = [PackageOrder, Package, Account]
    url_pattern = "/v1.0/projects/{pid}/orders"

    def setUp(self):
        super().setUp()
        self.pn = 12
        self.url = self.url_pattern.format(pid=self.pn)

    def tearDown(self):
        super().tearDown()

    def timestamp(self, offset=0):
        day = datetime.now() + timedelta(days=offset)
        return day.strftime("%Y-%m-%d")

    def load_account(self):
        rvs = [
            {"user": "1", "name": "用户1", "password": "1",
             "mobile": "13612555229"},
            {"user": "2", "name": "用户2", "password": "1",
             "mobile": "13612555230"},
            {"user": "3", "name": "用户3", "password": "1",
             "mobile": "13612555231"},
        ]
        for kw in rvs:
            a = Account(**kw)
            session.add(a)
            session.commit()
            kw['id'] = a.id

        return rvs

    def load_package(self):
        rvs = [
            {"pn": self.pn, "name": "套餐1", "price": 30, "time": 30},
            {"pn": self.pn, "name": "套餐2", "price": 45, "time": 40},
            {"pn": self.pn, "name": "套餐3", "price": 60, "time": 70}
        ]
        for kw in rvs:
            p = Package(**kw)
            session.add(p)
            session.commit()
            kw['id'] = p.id

        return rvs

    def test_scenario(self):
        accounts = self.load_account()
        packages = self.load_package()

        kwargs = {"pay_with": "微信支付", "pay_from": "APP"}
        for a in accounts:
            for p in packages:
                kwargs['package_id'] = p['id']
                kwargs['account_id'] = a['id']
                kwargs['amount'] = p['price']
                order = PackageOrder(**kwargs)
                session.add(order)
                session.commit()

        count = session.query(PackageOrder).count()
        self.assertEqual(count, 9)

        resp = self.get(self.url, query={"begin": "", "end": ""})
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 400)

        query = {"begin": self.timestamp(), "end": self.timestamp()}
        resp = self.get(self.url, query=query)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertEqual(resp.json['total_items'], 9)
        self.assertEqual(len(resp.json['objects']), 9)
        self.assertEqual(len(resp.json['objects'][0].keys()), 7)

        query = {"begin": self.timestamp(-5), "end": self.timestamp(-1)}
        resp = self.get(self.url, query=query)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['objects']), 0)

        url = self.url + '/overview'
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertEqual(resp.json['today_amount'], 135 * 3)
        self.assertEqual(resp.json['total_amount'], 135 * 3)

        query = {"begin": self.timestamp(), "end": self.timestamp()}
        url = self.url + '/chart'
        resp = self.get(url, query=query)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertIsNotNone(resp.json.get('title'))
        self.assertEqual(len(resp.json['dates']), 1)
        self.assertEqual(len(resp.json['amounts']), 1)
