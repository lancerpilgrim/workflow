from sqlalchemy import or_

from bidong.core.database import session
from bidong.core.paginator import Paginator
from bidong.core.exceptions import DuplicateError, NotFoundError
from bidong.storage.models import NetworkConfig


class NetworkService:

    def __init__(self, pn):
        self.pn = int(pn)

    def create(self, ssid, portal_id, duration, session_timeout, is_public,
               is_free, mask, wechat_account_id):
        """新建WiFi网络配置
        Args:
            mask: 标志位, 前三位为认证方式
        """
        exist = session.query(NetworkConfig).filter_by(
            pn=self.pn, ssid=ssid).count()
        if exist:
            raise DuplicateError("项目内SSID不能重复")

        config = NetworkConfig(
            pn=self.pn, ssid=ssid, portal_id=portal_id, is_public=is_public,
            is_free=is_free, mask=mask, session_timeout=session_timeout,
            duration=duration, wechat_account_id=wechat_account_id
        )
        session.add(config)
        session.commit()
        return config.id

    def get(self, network_id):
        config = session.query(NetworkConfig).filter(
            NetworkConfig.id == network_id, NetworkConfig.pn == self.pn
        ).first()
        if not config:
            raise NotFoundError("网络配置不存在")
        return config

    def update(self, network_id, ssid, portal_id, duration, session_timeout,
               is_public, is_free, mask, wechat_account_id):
        config = session.query(NetworkConfig).filter(
            NetworkConfig.id == network_id, NetworkConfig.pn == self.pn
        ).first()
        if not config:
            raise NotFoundError("网络配置不存在")

        ssid_exists = session.query(NetworkConfig).filter(
            NetworkConfig.id != network_id, NetworkConfig.ssid == ssid,
            NetworkConfig.pn == self.pn
        ).count()
        if ssid_exists:
            raise DuplicateError("项目内ssid不能重复")

        config.ssid = ssid
        config.portal_id = portal_id
        config.duration = duration
        config.session_timeout = session_timeout
        config.is_public = is_public
        config.is_free = is_free
        config.mask = mask
        config.wechat_account_id = wechat_account_id
        session.commit()

    def list(self, page, page_size,  keyword=None):
        query = session.query(NetworkConfig).filter(
            NetworkConfig.pn == self.pn
        )
        if keyword is not None:
            if keyword.isdigit():
                query = query.filter(
                    or_(
                        NetworkConfig.ssid.contains(keyword),
                        NetworkConfig.id == int(keyword)
                    )
                )
            else:
                query = query.filter(NetworkConfig.ssid.contains(keyword))

        paginator = Paginator(query, page, page_size)
        return paginator.to_dict()

    def delete(self, network_id):
        rv = session.query(NetworkConfig).filter(
            NetworkConfig.id == network_id
        ).delete(synchronize_session=False)

        session.commit()
        return bool(rv)
