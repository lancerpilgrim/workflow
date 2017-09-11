from bidong.core.database import session
from bidong.storage.models import Tag

from tests.view import ApiTestCase


class TagApiTestCase(ApiTestCase):
    api = "platform"
    url = '/v1.0/tags'
    related_models = [Tag]

    def setUp(self):
        super(TagApiTestCase, self).setUp()

    def tearDown(self):
        super(TagApiTestCase, self).tearDown()

    def test_get(self):
        kwargs = [
            {"pn": 0, "tag_type": "account", "name": "用户标签1"},
            {"pn": 0, "tag_type": "ap", "name": "套餐标签1"},
            {"pn": 0, "tag_type": "account", "name": "用户标签2"},
            {"pn": 0, "tag_type": "ap", "name": "套餐标签2"}
        ]
        tags = [Tag(**kw) for kw in kwargs]
        session.add_all(tags)
        session.commit()

        resp = self.get(self.url, query={"type": "account"})
        self.assertEqual(resp.code, 200)
        print(resp.json['tags'])
        self.assertEqual(len(resp.json['tags']), 2)

    def test_post(self):
        kwargs = [
            {"tag_type": "account", "name": "用户标签1"},
            {"tag_type": "ap", "name": "套餐标签1"},
            {"tag_type": "account", "name": "用户标签2"},
            {"tag_type": "ap", "name": "套餐标签2"}
        ]
        for kw in kwargs:
            resp = self.json_post(self.url, kw)
            self.assertEqual(resp.code, 200)
            print(resp.json)

        resp = self.json_post(self.url, payload={})
        print(resp.json)
        self.assertEqual(resp.code, 400)

    def test_delete(self):
        kwargs = [
            {"pn": 0, "tag_type": "account", "name": "用户标签1"},
            {"pn": 0, "tag_type": "account", "name": "用户标签2"},
        ]
        tags_id = []
        for kw in kwargs:
            tag = Tag(**kw)
            session.add(tag)
            session.commit()
            tags_id.append(tag.id)

        print(tags_id)
        url = self.url + '/{tid}'
        self.delete(url.format(tid=tags_id[0]))

        count = session.query(Tag).count()
        self.assertEqual(count, 1)
