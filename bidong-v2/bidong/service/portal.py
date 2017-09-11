from bidong.core.database import session
from bidong.core.exceptions import NotFoundError, DuplicateError, LogicError
from bidong.storage.models import Portal, NetworkConfig


class PortalService:

    def __init__(self, pn=0, is_platform=False):
        self.pn = int(pn)
        self.is_platform = is_platform

    def create(self, name, note, mobile_title, mobile_banner_url,
               pc_title, pc_banner_url):

        exists = session.query(Portal).filter_by(
            name=name, pn=self.pn).count()
        if exists:
            raise DuplicateError("同名portal配置已存在")

        portal = Portal(
            pn=self.pn, name=name, note=note,
            mobile_title=mobile_title,
            mobile_banner_url=mobile_banner_url,
            pc_title=pc_title,
            pc_banner_url=pc_banner_url
        )
        session.add(portal)
        session.commit()
        return portal.id

    def list(self, page=None, page_size=None):
        query = session.query(
            Portal.id, Portal.name, Portal.note, Portal.on_using,
            Portal.created_at, Portal.updated_at
        )

        portal_list = []
        if not self.is_platform:
            portal_used = query.filter(
                Portal.pn == 0, Portal.on_using == 1).first()
            if portal_used:
                rv = dict(zip(portal_used.keys(), portal_used))
                rv['is_platform'] = 1
                portal_list.append(rv)

        portals = query.filter(Portal.pn == self.pn).all()
        portals = [dict(zip(p.keys(), p)) for p in portals]
        portal_list.extend(portals)
        return portal_list

    def get(self, portal_id):
        # 如果是项目的可以查看平台默认模版
        if not self.is_platform:
            portal = session.query(Portal).filter(
                Portal.pn == 0, Portal.id == portal_id, Portal.on_using == 1
            ).first()
            if portal:
                return portal

        portal = session.query(Portal).filter(
            Portal.pn == self.pn, Portal.id == portal_id
        ).first()
        if not portal:
            raise NotFoundError("Portal页配置不存在")

        return portal

    def update(self, portal_id, name, note, mobile_title, mobile_banner_url,
               pc_title, pc_banner_url):

        portal = session.query(Portal).filter(
            Portal.pn == self.pn, Portal.id == portal_id
        ).first()
        if not portal:
            raise NotFoundError("Portal页配置不存在")

        exist = session.query(Portal.id).filter(
            Portal.id != portal_id, Portal.name == name
        ).count()
        if exist:
            raise DuplicateError("同名portal配置已存在")

        portal.name = name
        portal.note = note
        portal.mobile_title = mobile_title
        portal.mobile_banner_url = mobile_banner_url
        portal.pc_title = pc_title
        portal.pc_banner_url = pc_banner_url
        session.commit()

    def using(self, portal_id):
        """将平台某个模版设置为默认模版
        """
        portal_id = int(portal_id)
        portal = session.query(Portal).filter_by(
            on_using=1, pn=self.pn).first()

        if portal and portal.id == portal_id:
            return False

        if portal:
            portal.on_using = 0

        updated_success = session.query(Portal).filter(
            Portal.id == portal_id, Portal.pn == self.pn
        ).update(
            {"on_using": 1}, synchronize_session=False
        )
        session.commit()

        if portal and updated_success:
            session.query(NetworkConfig).filter(
                NetworkConfig.portal_id == portal.id
            ).update(
                {"portal_id": portal_id}, synchronize_session=False
            )
        return True

    def delete(self, portal_id):
        using = session.query(NetworkConfig.id).filter(
            # NetworkConfig.portal_id == portal_id, NetworkConfig.pn == self.pn
            NetworkConfig.portal_id == portal_id
        ).count()
        if using:
            raise LogicError(409, "Potal模版使用中，不能删除")

        rv = session.query(Portal).filter(
            Portal.pn == self.pn, Portal.id == portal_id
        ).delete(synchronize_session=False)
        session.commit()
        return rv == 1
