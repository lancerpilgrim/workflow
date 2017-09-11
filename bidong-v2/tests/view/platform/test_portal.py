from copy import copy

from bidong.core.database import session
from bidong.storage.models import Portal
from tests.view import ApiTestCase


class PortalTestCase(ApiTestCase):
    api = "platform"
    url = "/v1.0/portals"
    related_models = [Portal]

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_scenario(self):

        resp = self.json_post(self.url, payload={})
        self.assertEqual(resp.code, 400)

        template = {
            "name": "name-{}", "note": "note-{}",
            "mobile_title": "mobile-title-{}",
            "mobile_banner_url": "mobile-banner-url-{}",
            "pc_title": "pc-title-{}",
            "pc_banner_url": "pc-banner-url-{}"
        }

        for n in range(0, 20):
            kwargs = copy(template)
            for key in kwargs:
                kwargs[key] = kwargs[key].format(n)
            resp = self.json_post(self.url, payload=kwargs)
            self.assertEqual(resp.code, 200)

        count = session.query(Portal).count()
        self.assertEqual(count, 20)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertEqual(len(resp.json['objects']), 20)

        default = resp.json['objects'][0]
        self.assertEqual(default['on_using'], 0)

        portal2_id = resp.json['objects'][1]['id']
        url = '{}/{}'.format(self.url, portal2_id)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        for key in template:
            self.assertEqual(resp.json[key], template[key].format(1))

        # testing for update
        kwargs = copy(template)
        for key in kwargs:
            kwargs[key] = kwargs[key].format(100)
        resp = self.json_put(url, payload=kwargs)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        for key in template:
            self.assertEqual(resp.json[key], template[key].format(100))

        # testing for using update
        resp = self.json_put('{}?using=1'.format(url), payload={})
        self.assertEqual(resp.code, 200)
        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        rvs = resp.json['objects']
        for rv in rvs:
            if rv['id'] == portal2_id:
                self.assertEqual(rv['on_using'], 1)

        portal_to_using = session.query(Portal.id).filter_by(
            pn=0, on_using=0).first()
        using_url = "{}/{}?using=1".format(self.url, portal_to_using.id)
        resp = self.json_put(using_url, payload={})
        self.assertEqual(resp.code, 200)
        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        rvs = resp.json['objects']
        for rv in rvs:
            if rv['on_using'] == 1:
                self.assertEqual(rv['id'], portal_to_using.id)

        resp = self.delete(url)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        print('Resp => ', resp.json)
        self.assertEqual(len(resp.json['objects']), 19)
