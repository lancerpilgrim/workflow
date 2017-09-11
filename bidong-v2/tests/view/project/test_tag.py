from bidong.core.database import session
from bidong.storage.models import Tag

from tests.view import ApiTestCase


class TagApiTestCase(ApiTestCase):
    api = "project"
    url_pattern = '/v1.0/projects/{pid}/tags'
    related_models = [Tag]

    def setUp(self):
        super(TagApiTestCase, self).setUp()
        self.pn = 12
        self.url = self.url_pattern.format(pid=self.pn)

    def tearDown(self):
        super(TagApiTestCase, self).tearDown()

    def test_get(self):
        kwargs = [
            {"pn": 0, "tag_type": "account", "name": "用户标签1"},
            {"pn": 0, "tag_type": "ap", "name": "套餐标签1"},
            {"pn": 1, "tag_type": "account", "name": "用户标签2"},
            {"pn": 1, "tag_type": "ap", "name": "套餐标签2"},
            {"pn": 1, "tag_type": "account", "name": "用户标签3"},
            {"pn": 1, "tag_type": "ap", "name": "套餐标签3"},
            {"pn": 2, "tag_type": "account", "name": "用户标签4"},
            {"pn": 2, "tag_type": "ap", "name": "套餐标签4"},
        ]
        tags = [Tag(**kw) for kw in kwargs]
        session.add_all(tags)
        session.commit()

        resp = self.get(self.url_pattern.format(pid=0))
        self.assertEqual(resp.code, 400)

        url = self.url_pattern.format(pid=0)
        resp = self.get(url, query={"type": "account"})
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['tags']), 1)

        url = self.url_pattern.format(pid=1)
        resp = self.get(url, query={"type": "account"})
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['tags']), 2)

    def test_post(self):
        kwargs = [
            {"pn": 1, "tag_type": "account", "name": "用户标签1"},
            {"pn": 1, "tag_type": "ap", "name": "套餐标签1"},
            {"pn": 2, "tag_type": "account", "name": "用户标签2"},
            {"pn": 2, "tag_type": "ap", "name": "套餐标签2"}
        ]
        for kw in kwargs:
            pn = kw.pop("pn")
            url = self.url.format(pid=pn)
            resp = self.json_post(url, kw)
            self.assertEqual(resp.code, 200)
            print(resp.json)

        resp = self.json_post(self.url.format(pid=0), payload={})
        print(resp.json)
        self.assertEqual(resp.code, 400)

    def test_delete(self):
        kwargs = [
            {"pn": 1, "tag_type": "account", "name": "用户标签1"},
            {"pn": 2, "tag_type": "account", "name": "用户标签2"},
        ]
        tags_id = []
        for kw in kwargs:
            tag = Tag(**kw)
            session.add(tag)
            session.commit()
            tags_id.append(tag.id)

        count = session.query(Tag).count()
        url = self.url_pattern + '/{tid}'
        self.delete(url.format(pid=kwargs[0]['pn'], tid=tags_id[0]))

        count = session.query(Tag).count()
        self.assertEqual(count, 1)

        self.delete(url.format(pid=kwargs[0]['pn'], tid=tags_id[1]))
        count = session.query(Tag).count()
        self.assertEqual(count, 1)
