from copy import deepcopy
from datetime import datetime, timedelta

from bidong.core.database import session
from bidong.storage.models import Package, Tag
from tests.view import ApiTestCase


class PackageTestCase(ApiTestCase):
    api = "project"
    url_pattern = "/v1.0/projects/{pid}/packages"
    related_models = [Package, Tag]

    def setUp(self):
        super().setUp()
        self.pn = 12
        self.url = self.url_pattern.format(pid=self.pn)

    def tearDown(self):
        super().tearDown()

    def _loat_tags(self, pn):
        tags = [
            {"pn": pn, "tag_type": "account", "name": "老师"},
            {"pn": pn, "tag_type": "account", "name": "学生"},
            {"pn": pn, "tag_type": "account", "name": "房东"},
            {"pn": pn, "tag_type": "account", "name": "租客"}
        ]
        for kw in tags:
            tag = Tag(**kw)
            session.add(tag)
        session.commit()
        rvs = session.query(Tag).all()
        self.assertEqual(len(rvs), len(tags))
        return [rv.id for rv in rvs]

    def _timestamp(self, offset):
        day = datetime.now() + timedelta(days=offset)
        return day.strftime("%Y-%m-%d")

    def test_package_scenario(self):
        tag_list = self._loat_tags(self.pn)
        kwargs = {
            "name": "套餐1", "price": 30, "ends": 3
        }
        resp = self.json_post(self.url, payload=kwargs)
        self.assertEqual(resp.code, 400)

        time_kwargs = deepcopy(kwargs)
        time_kwargs['time'] = 30
        resp = self.json_post(self.url, payload=time_kwargs)
        self.assertEqual(resp.code, 200)
        resp = self.json_post(self.url, payload=time_kwargs)
        self.assertEqual(resp.code, 409)

        time_kwargs['name'] = '套餐2'
        time_kwargs['until'] = self._timestamp(180)
        time_kwargs['tag_list'] = []
        resp = self.json_post(self.url, payload=time_kwargs)
        self.assertEqual(resp.code, 200)

        expired_kwargs = deepcopy(kwargs)
        expired_kwargs['name'] = '套餐3'
        expired_kwargs['expired'] = self._timestamp(5)
        expired_kwargs['tag_list'] = tag_list
        resp = self.json_post(self.url, payload=expired_kwargs)
        self.assertEqual(resp.code, 200)

        expired_kwargs['name'] = '套餐4'
        expired_kwargs['until'] = self._timestamp(180)
        resp = self.json_post(self.url, payload=expired_kwargs)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 4)
        self.assertEqual(len(resp.json['objects']), 4)
        self.assertEqual(len(resp.json['objects'][0].keys()), 9)

        resp = self.get(self.url, query={"page": 2, "page_size": 40})
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 4)
        self.assertEqual(len(resp.json['objects']), 0)

        resp = self.get(self.url, query={"keyword": "套餐1"})
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 1)
        self.assertEqual(len(resp.json['objects']), 1)

        package4 = session.query(Package).filter_by(
            name=expired_kwargs['name']).first()
        url = "{}/{}".format(self.url, package4.id)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['name'], expired_kwargs['name'])
        self.assertEqual(resp.json['expired'], expired_kwargs['expired'])
        self.assertEqual(resp.json['until'], expired_kwargs['until'])
        self.assertIsNone(resp.json['time'])

        package2 = session.query(Package).filter_by(
            name=time_kwargs['name']).first()
        url = "{}/{}".format(self.url, package2.id)
        update_kwargs = {"until": self._timestamp(200)}
        resp = self.json_put(url, payload=update_kwargs)
        self.assertEqual(resp.code, 200)
        resp = self.get(url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['until'], update_kwargs['until'])
        self.assertEqual(resp.json['tags'], "")
        self.assertEqual(resp.json['time'], time_kwargs['time'])
        update_kwargs = {"tag_list": tag_list}
        resp = self.json_put(url, payload=update_kwargs)
        self.assertEqual(resp.code, 200)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['tags'].split(",")), len(tag_list))

        resp = self.delete(url)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 3)

        count = session.query(Package).filter_by(is_deleted=0).count()
        self.assertEqual(count, 3)
        count = session.query(Package).filter_by(is_deleted=1).count()
        self.assertEqual(count, 1)
