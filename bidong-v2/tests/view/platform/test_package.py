import time
from copy import deepcopy
from datetime import datetime, timedelta

from bidong.core.database import session
from bidong.storage.models import Package, Tag, Projects
from tests.view import ApiTestCase


class PackageTestCase(ApiTestCase):
    api = "platform"
    url = "/v1.0/packages"
    related_models = [Package, Tag, Projects]

    def setUp(self):
        super().setUp()
        self.pn = 0

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

    def _load_projects(self):
        projects = []
        kwargs = {'name': '项目-{}', 'description': '', 'location': '',
                  'contact': 'Ass', 'contact_number': '18824222212',
                  'email': ''}
        for n in range(4):
            kwargs['id'] = int(time.time()) + n
            kwargs['name'] = '项目 - {}'.format(n)
            p = Projects(**kwargs)
            session.add(p)
            session.commit()
            projects.append(p.id)
        return projects

    def _timestamp(self, offset):
        day = datetime.now() + timedelta(days=offset)
        return day.strftime("%Y-%m-%d")

    def test_package_scenario(self):
        tag_list = self._loat_tags(self.pn)
        project_list = self._load_projects()
        kwargs = {
            "name": "套餐1", "price": 30, "ends": 3
        }
        resp = self.json_post(self.url, payload=kwargs)
        self.assertEqual(resp.code, 400)

        day_kwargs = deepcopy(kwargs)
        day_kwargs['time'] = 30
        day_kwargs['mask'] = 0
        resp = self.json_post(self.url, payload=day_kwargs)
        self.assertEqual(resp.code, 200)
        resp = self.json_post(self.url, payload=day_kwargs)
        self.assertEqual(resp.code, 409)

        day_kwargs['name'] = '套餐2'
        day_kwargs['until'] = self._timestamp(180)
        day_kwargs['tag_list'] = []
        day_kwargs['project_list'] = []
        resp = self.json_post(self.url, payload=day_kwargs)
        self.assertEqual(resp.code, 200)

        hour_kwargs = deepcopy(kwargs)
        hour_kwargs['mask'] = 1
        hour_kwargs['name'] = '套餐3'
        hour_kwargs['time'] = 240
        hour_kwargs['tag_list'] = tag_list
        hour_kwargs['project_list'] = project_list
        resp = self.json_post(self.url, payload=hour_kwargs)
        self.assertEqual(resp.code, 200)

        hour_kwargs['name'] = '套餐4'
        hour_kwargs['until'] = self._timestamp(180)
        resp = self.json_post(self.url, payload=hour_kwargs)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
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

        resp = self.get(self.url, query={"keyword": "套餐"})
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 4)
        self.assertEqual(len(resp.json['objects']), 4)

        package4 = session.query(Package).filter_by(
            name=hour_kwargs['name']).first()
        url = "{}/{}".format(self.url, package4.id)
        resp = self.get(url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['name'], hour_kwargs['name'])
        self.assertEqual(resp.json['until'], hour_kwargs['until'])
        self.assertEqual(resp.json['time'], hour_kwargs['time'])
        self.assertEqual(resp.json['mask'], hour_kwargs['mask'])
        self.assertEqual(len(resp.json['tags'].split(",")), len(tag_list))
        self.assertEqual(len(resp.json['projects'].split(",")),
                         len(project_list))

        package2 = session.query(Package).filter_by(
            name=day_kwargs['name']).first()
        url = "{}/{}".format(self.url, package2.id)

        update_kwargs = {"until": self._timestamp(200)}
        resp = self.json_put(url, payload=update_kwargs)
        self.assertEqual(resp.code, 200)
        resp = self.get(url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['until'], update_kwargs['until'])
        self.assertEqual(resp.json['tags'], "")
        self.assertEqual(resp.json['time'], day_kwargs['time'])
        self.assertEqual(resp.json['tags'], "")
        self.assertEqual(resp.json['projects'], "")

        update_kwargs = {"tag_list": tag_list, "project_list": project_list}
        resp = self.json_put(url, payload=update_kwargs)
        self.assertEqual(resp.code, 200)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['tags'].split(",")), len(tag_list))
        self.assertEqual(len(resp.json['projects'].split(",")),
                         len(project_list))

        update_kwargs = {"tag_list": tag_list[:2]}
        resp = self.json_put(url, payload=update_kwargs)
        self.assertEqual(resp.code, 200)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['tags'].split(",")), 2)

        resp = self.delete(url)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 3)

        count = session.query(Package).filter_by(is_deleted=0).count()
        self.assertEqual(count, 3)
        count = session.query(Package).filter_by(is_deleted=1).count()
        self.assertEqual(count, 1)
