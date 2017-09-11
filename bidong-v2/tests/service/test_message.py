from bidong.core.database import session
from bidong.core.exceptions import NotFoundError
from bidong.storage.models import Letter, Mailbox
from bidong.service.message import LetterService
from tests.service import ServiceTestCase


class TestLetterService(ServiceTestCase):
    models = [Letter, Mailbox]

    def setUp(self):
        super(TestLetterService, self).setUp()

    def tearDown(self):
        super(TestLetterService, self).tearDown()

    def test_gererate_draft(self):
        kwargs = {
            "manager_id": 1, "title": "站内信草稿", "content": "这是站内信内容",
            "status": 0
        }
        rv = LetterService.generate(**kwargs)
        self.assertIsNotNone(rv)

        l = session.query(Letter).filter_by(id=rv).first()
        self.assertEqual(l.title, kwargs['title'])
        self.assertEqual(l.status, kwargs['status'])

    def test_gererate_public(self):
        kwargs = {
            "manager_id": 1, "title": "站内正式内容", "content": "这是站内信内容",
            "status": 1, "receivers": [11, 12, 13]
        }
        rv = LetterService.generate(**kwargs)
        self.assertIsNotNone(rv)

        mails = session.query(Mailbox).all()
        self.assertEqual(len(mails), len(kwargs['receivers']))
        self.assertEqual(mails[0].letter_id, rv)

    def test_detail(self):
        kwargs = {
            "manager_id": 1, "title": "站内信草稿", "content": "这是站内信内容",
            "status": 0
        }
        letter_id = LetterService.generate(**kwargs)
        self.assertIsNotNone(letter_id)

        letter = LetterService.detail(letter_id)
        self.assertEqual(letter.title, kwargs['title'])

        with self.assertRaises(NotFoundError) as context:
            LetterService.detail(63557)
        self.assertTrue("不存在" in context.exception.message)

    def test_list(self):
        kwargs = {"manager_id": 1, "status": 0}
        for n in range(20):
            kwargs['title'] = 'title-{}'.format(n)
            kwargs['content'] = 'content-{}'.format(n)
            LetterService.generate(**kwargs)

        count = session.query(Letter).count()
        self.assertEqual(count, 20)

        p = LetterService.list(1, 6, 0)
        self.assertEqual(p.total_items, 20)
        self.assertEqual(p.total_pages, 4)
        self.assertEqual(len(p.objects), 6)

    def test_update(self):
        kwargs = {
            "manager_id": 1, "title": "站内信草稿", "content": "这是站内信内容",
            "status": 0
        }
        letter_id = LetterService.generate(**kwargs)
        self.assertIsNotNone(letter_id)

        kwargs.update({"title": "修改标题", "status": 1,
                       "letter_id": letter_id, "receivers": [11, 12]})
        kwargs.pop('manager_id', None)
        LetterService.update(**kwargs)

        letter = session.query(Letter).filter_by(id=letter_id).first()
        self.assertEqual(letter.title, kwargs['title'])

        count = session.query(Mailbox).count()
        self.assertEqual(count, 2)

    def test_delete(self):
        kwargs = {
            "manager_id": 1, "title": "站内正式内容", "content": "这是站内信内容",
            "status": 1, "receivers": [11, 12, 13]
        }
        letter_id = LetterService.generate(**kwargs)
        self.assertIsNotNone(letter_id)

        LetterService.delete(letter_id)

        count = session.query(Letter).filter_by(status=Letter.DELETED).count()
        self.assertEqual(count, 1)

        count = session.query(Mailbox).filter_by(
            status=Mailbox.DELETED).count()
        self.assertEqual(count, 3)
