import random
from time import time
from datetime import datetime
from collections import defaultdict

from tornado import gen
from sqlalchemy import desc, func, distinct

from bidong.core.database import session
from bidong.core.paginator import Paginator
from bidong.storage.models import CouponCode, CouponSerial


class CouponService:
    code_prefix = 'M'

    @classmethod
    def gen_check_code(cls, x, y):
        return ((x * y) >> 2) % 10

    @classmethod
    def generate(cls, serial, count):
        total = 0
        subfix_set = set()
        while total < count:
            code = random.randint(1, 99999)
            subfix_set.add(code)
            total = len(subfix_set)

        code_list = []
        for subcode in subfix_set:
            checkcode = cls.gen_check_code(serial, subcode)
            code = '{}{}{:05d}{}'.format(
                cls.code_prefix, serial, subcode, checkcode)
            code_list.append(code)
        return code_list

    @classmethod
    def is_valid_code(cls, code):
        code = code.upper()
        if not code.startswith(cls.code_prefix):
            return False
        try:
            serial = int(code[1:7])
            random_code = int(code[7:12])
            checkcode = int(code[12:])
        except:
            return False

        if cls.gen_check_code(serial, random_code) == checkcode:
            return True
        return False


class CouponAdminService:

    CODE_USABLE = 0
    CODE_USED = 1
    CODE_EXPIRED = 2

    def __init__(self, manager_id):
        self.managerid = manager_id

    def get_serial_number(self):
        serial_record = session.query(CouponSerial.serial).order_by(
            desc(CouponSerial.serial)
        ).first()
        if serial_record is None:
            serial = int(str(int(time()))[:6])
        else:
            serial = serial_record.serial + random.randint(2, 5)
        return serial

    def generate(self, hours, count, expired):
        serial = self.get_serial_number()

        serial_record = CouponSerial(created_by=self.managerid, serial=serial)
        session.add(serial_record)
        session.flush()

        code_list = CouponService.generate(serial, count)
        models = []
        for code in code_list:
            models.append(
                CouponCode(code=code, serial_id=serial_record.id,
                           expired=expired, hours=hours)
            )
        session.add_all(models)
        session.commit()
        return serial

    def list_by_serial(self, serial, page=None, page_size=None):
        query = session.query(
            CouponSerial.serial, CouponCode.id,
            CouponCode.code, CouponCode.hours, CouponCode.expired
        ).filter(
            CouponSerial.created_by == self.managerid,
            CouponSerial.serial == serial,
            CouponCode.serial_id == CouponSerial.id
        )

        if page is not None and page_size is not None:
            return Paginator(query, page, page_size).to_dict()
        return query.all()

    def list(self, page, page_size, status=None):
        # TODO: check current manager is super or not
        is_super = True

        query = session.query(
            CouponCode.code, CouponCode.hours, CouponCode.expired,
            CouponSerial.created_at, CouponCode.is_used
        ).filter(
            CouponCode.serial_id == CouponSerial.id
        )
        if not is_super:
            query = query.filter(CouponSerial.created_by == self.managerid)

        if status is not None:
            if status == CouponCode.USED:
                query = query.filter(CouponCode.is_used == 1)
            elif status == CouponCode.USEABLE:
                query = query.filter(
                    CouponCode.is_used == 0,
                    func.date(CouponCode.expired) >= datetime.now().date()
                )
            else:
                query = query.filter(
                    CouponCode.is_used == 0,
                    func.date(CouponCode.expired) < datetime.now().date()
                )

        paginator = Paginator(query, page, page_size)
        return paginator.to_dict()

    def aggregate(self, begin, end, page, page_size, managerid=None):
        # TODO:
        is_super = True
        limit_managers = []
        if not is_super:
            limit_managers.append(self.managerid)
        if managerid is not None:
            limit_managers.append(managerid)

        query = session.query(
            distinct(CouponSerial.created_by).label("created_by"))
        if limit_managers:
            query = query.filter(
                CouponSerial.created_by.in_(limit_managers))

        paginator = Paginator(query, page, page_size)
        paginator_dict = paginator.to_dict()
        objects = paginator_dict.pop('objects')
        choiced_managers = [rv.created_by for rv in objects]

        query = session.query(
            CouponSerial.created_by,
            func.sum(CouponCode.hours).label("total_hours")
        ).filter(
            CouponCode.serial_id == CouponSerial.id,
            func.date(CouponSerial.created_at) >= begin,
            func.date(CouponSerial.created_at) <= end
        )

        if choiced_managers:
            query = query.filter(CouponSerial.created_by.in_(choiced_managers))
        else:
            paginator_dict['objects'] = []
            return paginator_dict

        manager_dict = {mid: defaultdict(int) for mid in choiced_managers}
        today = datetime.now().date()
        # 这里有三次查询
        filter_dict = {
            CouponCode.USEABLE:
            (CouponCode.is_used == 0, func.date(CouponCode.expired) >= today),
            CouponCode.USED:
            (CouponCode.is_used == 1,),
            CouponCode.EXPIRED:
            (CouponCode.is_used == 0, func.date(CouponCode.expired) < today),
        }

        for status, filters in filter_dict.items():
            rvs = query.filter(
                *filters
            ).group_by(
                CouponSerial.created_by
            ).all()
            for rv in rvs:
                manager_dict[rv.created_by][status] += rv.total_hours

        aggregate_results = []
        for mid, data in manager_dict.items():
            total = sum(data.values()) if data.values() else 0
            rv = {
                "usable": data.get(CouponCode.USEABLE, 0),
                "used": data.get(CouponCode.USED, 0),
                "expired": data.get(CouponCode.EXPIRED, 0),
                "total": total,
                "created_by": mid,
            }
            aggregate_results.append(rv)

        paginator_dict['objects'] = aggregate_results
        return paginator_dict

    def overview(self, begin, end):
        today = datetime.now().date()
        query = session.query(func.sum(CouponCode.hours))
        usable = query.filter(
            CouponCode.is_used == 0, func.date(CouponCode.expired) >= today
        ).scalar()
        used = query.filter(CouponCode.is_used == 1).scalar()
        expired = query.filter(
            CouponCode.is_used == 0, func.date(CouponCode.expired) < today
        ).scalar()

        data = {
            "usable": int(usable) if usable else 0,
            "used": int(used) if used else 0,
            "expired": int(expired) if expired else 0
        }
        total = sum(data.values())
        data['total'] = total

        return data

    def fetch_coupon_managers(self):
        # TODO: 根据权限减少返回用户
        rvs = session.query(
            distinct(CouponSerial.created_by).label('created_by')
        ).all()
        return rvs

    @gen.coroutine
    def gen_serial_coupons_data(self, serial):
        records = self.list_by_serial(serial)
        headers = ['兑换码', '时长', '有效期']

        content = [
            [rv.code, rv.hours, rv.expired.strftime("%Y-%m-%d")]
            for rv in records
        ]
        return headers, content
