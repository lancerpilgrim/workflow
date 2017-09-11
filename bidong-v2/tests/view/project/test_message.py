from bidong.core.database import session
from bidong.service.message import LetterService
from bidong.storage.models import Letter, Mailbox
from tests.view import ApiTestCase


class MessageTestCase(ApiTestCase):
    api = "project"
    url = "/v1.0/messages"
    related_models = [Letter, Mailbox]

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().setUp()

    def test_scenario(self):

        messages = [
            {"manager_id": 12, "title": "标题1", "content": "内容1",
             "status": Letter.PUBLIC, "receivers": [1, 2, 3, 4]},
            {"manager_id": 12, "title": "标题2", "content": "内容2",
             "status": Letter.PUBLIC, "receivers": [1, 2, 3, 4]},
            {"manager_id": 12, "title": "标题3", "content": "内容3",
             "status": Letter.PUBLIC, "receivers": [1, 2, 3, 4]},
            {"manager_id": 12, "title": "标题4", "content": "内容4",
             "status": Letter.DRAFT, "receivers": [1, 2, 3, 4]},
        ]
        for kw in messages:
            LetterService.generate(**kw)

        count = session.query(Letter).count()
        self.assertEqual(count, len(messages))

        url = self.url + '/notify'
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['unread'], 3)

        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 3)
        self.assertEqual(len(resp.json['objects']), 3)

        # read one
        messages = resp.json['objects']
        url = '{}/{}'.format(self.url, messages[0]['id'])
        resp = self.get(url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        # still have three message
        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 3)
        # but remain two unread
        resp = self.get(self.url + '/notify')
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['unread'], 2)

        resp = self.delete(url)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 2)
