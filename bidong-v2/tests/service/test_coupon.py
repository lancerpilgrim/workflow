from time import time
from datetime import datetime, timedelta

from bidong.core.database import session
from bidong.storage.models import CouponCode, CouponSerial
from bidong.service.coupon import CouponService, CouponAdminService

from tests.service import ServiceTestCase


class TestCouponService(ServiceTestCase):
    models = []

    def test_service(self):
        serial = int(str(int(time()))[:6])
        codes = CouponService.generate(serial, 10)
        print('codes => ', codes)
        self.assertEqual(len(codes), 10)

        code = ''
        self.assertFalse(CouponService.is_valid_code(code))
        code = codes[0]
        self.assertTrue(CouponService.is_valid_code(code))
        code = code.lower()
        self.assertTrue(CouponService.is_valid_code(code))
        code = code[len(code)-2:]
        self.assertFalse(CouponService.is_valid_code(code))


class TestAdminService(ServiceTestCase):
    models = [CouponCode, CouponSerial]

    def setUp(self):
        super().setUp()
        self.managerid = 12
        self.service = CouponAdminService(self.managerid)
        self.service_copy = CouponAdminService(self.managerid+100)

    def tearDown(self):
        super().tearDown()

    def timestamp(self, offset=0):
        current = datetime.now()
        return (current + timedelta(days=offset)).date()

    def test_curd(self):
        serial1 = self.service.generate(2, 20, self.timestamp(5))
        count = session.query(CouponCode).count()
        self.assertEqual(count, 20)
        count = session.query(CouponSerial).count()
        self.assertEqual(count, 1)

        codes = self.service.list_by_serial(serial1)
        self.assertEqual(len(codes), 20)
        paginator = self.service.list_by_serial(serial1, page=2, page_size=5)
        self.assertEqual(paginator['total_items'], 20)
        self.assertEqual(len(paginator['objects']), 5)
        for rv in paginator['objects']:
            print('list_by_serial => ', rv)

        paginator = self.service.list(1, 10)
        self.assertEqual(paginator['total_items'], 20)
        self.assertEqual(len(paginator['objects']), 10)
        for rv in paginator['objects']:
            print('list => ', rv)

        paginator = self.service.list(1, 10, 1)
        self.assertEqual(paginator['total_items'], 0)

        serial2 = self.service_copy.generate(2, 20, self.timestamp(-5))
        codes = self.service_copy.list_by_serial(serial2)[:5]
        code_id_list = [c.id for c in codes]
        session.query(CouponCode).filter(
            CouponCode.id.in_(code_id_list)
        ).update({"is_used": 1}, synchronize_session=False)
        session.commit()

        begin, end = self.timestamp(-6), self.timestamp(6)
        paginator = self.service.aggregate(begin, end, 1, 20)
        self.assertEqual(paginator['total_items'], 2)
        self.assertEqual(len(paginator['objects']), 2)
        for rv in paginator['objects']:
            print('aggregate => ', rv)
