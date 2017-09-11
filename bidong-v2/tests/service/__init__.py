import unittest

from bidong.core.database import session
from tests import patch_session, init_database


class ServiceTestCase(unittest.TestCase):

    def setUp(self):
        init_database()
        patch_session()
        self._truncate_tables()

    def _truncate_tables(self):
        for model in self.models:
            session.query(model).delete()
        session.commit()

    def tearDown(self):
        self._truncate_tables()
