from copy import copy

from bidong.core.database import session
from bidong.storage.models import Portal, NetworkConfig
from tests.view import ApiTestCase


class PortalTestCase(ApiTestCase):
    api = "project"
    url_pattern = "/v1.0/projects/{pid}/portals"
    related_models = [Portal]

    def setUp(self):
        super().setUp()
        self.pn = 12
        self.url = self.url_pattern.format(pid=self.pn)

    def tearDown(self):
        super().tearDown()

    def test_scenario(self):
        portal = Portal(
            pn=0, name="Bidong", note="官方认证页",
            mobile_title="壁咚WiFi", mobile_banner_url="http://www.zhizhang.com",
            pc_title="PC壁咚", pc_banner_url="http://pc.com",
            on_using=1
        )
        session.add(portal)
        session.commit()

        resp = self.json_post(self.url, payload={})
        self.assertEqual(resp.code, 400)

        template = {
            "name": "name-{}", "note": "note-{}",
            "mobile_title": "mobile-title-{}",
            "mobile_banner_url": "mobile-banner-url-{}",
            "pc_title": "pc-title-{}",
            "pc_banner_url": "pc-banner-url-{}"
        }

        for n in range(1, 21):
            kwargs = copy(template)
            for key in kwargs:
                kwargs[key] = kwargs[key].format(n)
            resp = self.json_post(self.url, payload=kwargs)
            self.assertEqual(resp.code, 200)

        count = session.query(Portal).count()
        self.assertEqual(count, 21)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertEqual(len(resp.json['objects']), 21)

        default = resp.json['objects'][0]
        self.assertEqual(default['is_platform'], 1)

        portal2_id = resp.json['objects'][1]['id']
        portal3_id = resp.json['objects'][2]['id']
        url = '{}/{}'.format(self.url, portal2_id)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        for key in template:
            self.assertEqual(resp.json[key], template[key].format(1))

        kwargs = copy(template)
        for key in kwargs:
            kwargs[key] = kwargs[key].format(100)
        resp = self.json_put(url, payload=kwargs)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        for key in template:
            self.assertEqual(resp.json[key], template[key].format(100))

        resp = self.delete(url)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertEqual(len(resp.json['objects']), 20)

        session.query(Portal).filter_by(pn=0, on_using=1).delete(
            synchronize_session=False
        )
        session.commit()

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertEqual(len(resp.json['objects']), 19)

        config = NetworkConfig(
            pn=self.pn, ssid='bidong', portal_id=portal3_id,
            mask=7
        )
        session.add(config)
        session.commit()

        url = '{}/{}'.format(self.url, portal3_id)
        resp = self.delete(url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 409)
