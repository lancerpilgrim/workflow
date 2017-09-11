from bidong.core.database import session
from bidong.core.exceptions import DuplicateError, NotFoundError
from bidong.storage.models import AC


class ACService:

    def check_duplicate(self, *filters):
        exists = session.query(AC.id).filter(*filters).count()
        if exists:
            raise DuplicateError("IP地址重复")

    def one_or_raise(self, *filters):
        ac = session.query(AC).filter(*filters).one_or_none()
        if ac is None:
            raise NotFoundError("AC不存在")
        return ac

    def create(self, name, vendor, ip, secret):
        self.check_duplicate(AC.ip == ip)
        ac = AC(name=name, vendor=vendor, ip=ip, secret=secret)
        session.add(ac)
        session.commit()
        return ac.id

    def update(self, ac_id, name, vendor, ip, secret):
        self.check_duplicate(AC.ip == ip, AC.id != ac_id)

        ac = self.one_or_raise(AC.id == ac_id)
        ac.name = name
        ac.vendor = vendor
        ac.ip = ip
        ac.secret = secret
        session.commit()

    def get(self, ac_id):
        return self.one_or_raise(AC.id == ac_id)

    def list(self, keyword=None):
        query = session.query(AC)
        if keyword is not None:
            query = query.filter(AC.has_keyword(keyword))
        return query.all()

    def delete(self, ac_id):
        count = session.query(AC).filter(AC.id == ac_id).delete(
            synchronize_session=False
        )
        session.commit()
        return count
