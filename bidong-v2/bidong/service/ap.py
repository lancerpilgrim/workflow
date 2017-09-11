from sqlalchemy import func
from sqlalchemy.sql import select

from bidong.core.database import session
from bidong.core.paginator import Paginator
from bidong.core.exceptions import DuplicateError, NotFoundError, LogicError
from bidong.storage.models import AP, Tag, Projects, ap_tag_table


class APService:

    def __init__(self, pn=0, is_platform=False):
        self.pn = int(pn)
        self.is_platform = is_platform

    def attach_tags(self, ap, tag_id_list):
        sql = ap_tag_table.delete().where(ap_tag_table.c.ap_id == ap.id)
        session.execute(sql)
        session.commit()

        if tag_id_list:
            tags = session.query(Tag).filter(Tag.id.in_(tag_id_list)).all()
            for tag in tags:
                ap.tags.append(tag)
            session.commit()

    def get_project_auth_ap_count(self):
        count = session.query(Projects.auth_ap_amount).filter(
            Projects.id == self.pn
        ).scalar()
        return count if count else 0

    def create(self, name, mac, address, vendor, tags):
        installed_count = session.query(AP.id).filter(AP.pn == self.pn).count()
        auth_count = self.get_project_auth_ap_count()
        if installed_count >= auth_count:
            raise LogicError(409, "AP数量已超过授权AP数")

        apexist = session.query(AP.id).filter_by(mac=mac).count()
        if apexist:
            raise DuplicateError("mac地址重复")

        ap = AP(pn=self.pn, name=name, mac=mac, address=address, vendor=vendor)
        session.add(ap)
        session.commit()

        self.attach_tags(ap, tags)
        return ap.id

    def update(self, ap_id, name, mac, address, vendor, tags):
        ap = session.query(AP).filter(AP.id == ap_id, AP.pn == self.pn).first()
        if not ap:
            raise NotFoundError("AP不存在")

        exists = session.query(
            AP.id).filter(AP.id != ap_id, AP.mac == mac).count()
        if exists:
            raise DuplicateError("mac地址重复")

        ap.name = name
        ap.mac = mac
        ap.address = address
        ap.vendor = vendor
        session.commit()

        self.attach_tags(ap, tags)

    def get(self, ap_id):
        ap = session.query(AP).filter(AP.id == ap_id, AP.pn == self.pn).first()
        if not ap:
            raise NotFoundError("AP不存在")

        tags = []
        for tag in ap.tags:
            tags.append(tag.id)
        detail = {"name": ap.name, "mac": ap.mac, "vendor": ap.vendor,
                  "address": ap.address, "tags": tags}
        return detail

    def list(self, page, page_size, online=None, vendor=None, tagid=None,
             keyword=None):
        filters = []
        if online is not None:
            filters.append(AP.is_online == online)
        if vendor is not None:
            filters.append(AP.vendor == vendor)
        if tagid is not None:
            sql = select(
                [ap_tag_table.c.ap_id]).where(ap_tag_table.c.tag_id == tagid)
            results = session.execute(sql).fetchall()
            ap_id_list = [rv[0] for rv in results]
            if ap_id_list:
                filters.append(AP.id.in_(ap_id_list))
            else:
                filters.append(AP.id.in_([0]))
        if keyword is not None:
            filters.append(AP.has_keyword(keyword))

        query = session.query(AP).filter(AP.pn == self.pn)
        if filters:
            query = query.filter(*filters)

        paginator = Paginator(query, page, page_size)
        paginator_dict = paginator.to_dict()

        ap_list = []
        objects = paginator_dict.pop('objects')
        for ap in objects:
            tags = ", ".join([t.name for t in ap.tags])
            detail = {"id": ap.id, "name": ap.name, "mac": ap.mac,
                      "vendor": ap.vendor, "online": ap.is_online,
                      "address": ap.address, "tags": tags,
                      "conns": ap.connections}
            ap_list.append(detail)

        paginator_dict['objects'] = ap_list
        return paginator_dict

    def delete(self, ap_id):
        session.query(AP).filter(AP.pn == self.pn, AP.id == ap_id).delete(
            synchronize_session=False
        )
        session.commit()

    def overview(self):
        auth_count = self.get_project_auth_ap_count()
        total_count = session.query(AP.id).filter(AP.pn == self.pn).count()
        online_count = session.query(AP.id).filter(
            AP.pn == self.pn, AP.is_online == 1
        ).count()

        if auth_count:
            rate = round(total_count / auth_count * 100, 2)
        else:
            rate = 100
        info = {
            "total": total_count,
            "online": online_count,
            "alert": 0,
            "rate": rate
        }
        return info


def get_projects_ap_count(project_id_list=None):
    """获取项目对应的AP数
    Args:
        project_id_list: list, 项目ID列表
    Returns:
        dict, {"project1_id": "ap_count", "project2_id": "ap_count"}
    """
    query = session.query(AP.pn, func.count(AP.id).label('ap_count'))
    if project_id_list:
        query = query.filter(AP.pn.in_(project_id_list))

    rvs = query.group_by(AP.pn).all()
    ap_count_dict = {rv.pn: rv.ap_count for rv in rvs}
    return ap_count_dict


def get_ap_alert_count_by_project(project_id):
    """获取项目AP警报数
    Args:
        project_id: 项目ID
    Returns:
        integer, AP警报数
    """
    return 0


def get_project_ap_count(project_id, status=None):
    """获取项目AP数
    Args:
        project_id: 项目ID
        status: int, 0 - 下线(即故障), 1 - 在线, None - 获取全部AP数
    Returns:
        integer: 项目AP数
    """
    query = session.query(AP.id).filter(AP.pn == project_id)
    if status is not None and status in (0, 1):
        query = query.filter(AP.is_online == status)

    return query.count()
