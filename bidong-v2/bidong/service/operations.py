"""
operations.py
~~~
项目运营相关逻辑
"""
from bidong.core.database import session
from bidong.core.exceptions import NotFoundError, DuplicateError, LogicError
from bidong.core.paginator import Paginator
from bidong.storage.models import WechatOfficialAccount, NetworkConfig


class WechatOfficialAccountService:

    def __init__(self, pn):
        self.pn = int(pn)

    def create(self, name, appid, shopid, secret, note):
        record = session.query(WechatOfficialAccount).filter_by(
            appid=appid, is_deleted=0, pn=self.pn).first()

        if record:
            raise DuplicateError("相同appid公众号已存在")

        account = WechatOfficialAccount(
            pn=self.pn, name=name, appid=appid, shopid=shopid,
            secret=secret, note=note
        )
        session.add(account)
        session.commit()
        return account.id

    def list(self, page, page_size, keyword=None):
        query = session.query(WechatOfficialAccount).filter(
            WechatOfficialAccount.pn == self.pn,
            WechatOfficialAccount.is_deleted == 0
        )
        if keyword is not None:
            query = query.filter(WechatOfficialAccount.has_keyword(keyword))

        paginator = Paginator(query, page, page_size)
        return paginator.to_dict()

    def update(self, wechat_id, name, appid, shopid, secret, note):
        record = session.query(WechatOfficialAccount).filter_by(
            appid=appid, is_deleted=0, pn=self.pn).first()

        if record and record.id != wechat_id:
            raise DuplicateError("相同appid公众号已存在")

        updated = session.query(WechatOfficialAccount).filter(
            WechatOfficialAccount.id == wechat_id,
            WechatOfficialAccount.pn == self.pn
        ).update(
            {"name": name, "appid": appid, "shopid": shopid,
             "secret": secret, "note": note},
            synchronize_session=False
        )
        session.commit()

        if not updated:
            raise NotFoundError("公众号不存在")
        return True

    def delete(self, wechat_id):
        using = session.query(NetworkConfig.id).filter_by(
            wechat_account_id=wechat_id, pn=self.pn
        ).count()
        if using:
            raise LogicError(409, "删除失败，公众号使用中")

        session.query(WechatOfficialAccount).filter(
            WechatOfficialAccount.id == wechat_id,
            WechatOfficialAccount.pn == self.pn
        ).update(
            {"is_deleted": 1},
            synchronize_session=False
        )
        session.commit()

    def list_select_fields(self, fields):
        fields = fields.split(',')
        selected = [
            rv for rv in fields if hasattr(WechatOfficialAccount, rv)]

        if not selected:
            return []
        columns = [getattr(WechatOfficialAccount, rv) for rv in selected]
        items = session.query(*columns).filter(
            WechatOfficialAccount.pn == self.pn,
            WechatOfficialAccount.is_deleted == 0
        ).all()

        select_dict_list = []
        for record in items:
            rv = {col: getattr(record, col) for col in selected}
            select_dict_list.append(rv)

        return select_dict_list
