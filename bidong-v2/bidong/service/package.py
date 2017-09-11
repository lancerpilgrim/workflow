"""
package.py
~~~
上网套餐管理
"""
import json

from sqlalchemy import func

from bidong.core.database import session
from bidong.core.paginator import Paginator
from bidong.core.exceptions import NotFoundError
from bidong.common.utils import set_bit
from bidong.storage.models import Package, Tag, PackageOrder, Projects


class PackageService:

    def __init__(self, pn=0, is_platform=False):
        """
        Args:
            pn: 项目ID, 0标示平台
        """
        self.pn = int(pn)
        self.is_platform = is_platform

    def _clean_projects(self, projects):
        project_list = session.query(Projects.id).filter_by(
            status=Projects.ENABLED).all()
        allow_projects = [rv.id for rv in project_list]

        return list(set(projects) & set(allow_projects))

    def create(self, name, price, ends, mask=None, time=None, expired=None,
               available_until=None, tags=None, apply_projects=None):
        """
        Args:
            name: 套餐名称
            price: 套餐金额
            ends: 上网终端
            time: 上网时长，存储单位为小时
            expired: 上网可用到期
            available_until: 套餐有效期
            apply_projects: 平台仅有，投放项目
        """
        if session.query(Package).filter_by(
                name=name, pn=self.pn, is_deleted=0).count():
            return 0

        if self.is_platform:
            apply_projects = apply_projects if apply_projects else []
            apply_projects = json.dumps(self._clean_projects(apply_projects))
            mask = set_bit(0, 0, 1) if mask else set_bit(0, 0, 0)
        else:
            mask = 0
        tag_id_list = tags if tags else []
        if tag_id_list:
            tags = session.query(Tag).filter(
                Tag.pn == self.pn,
                Tag.id.in_(tag_id_list),
                Tag.tag_type == Tag.ACCOUNT_TAG
            ).all()
        else:
            tags = []

        package = Package(
            name=name, price=price, ends=ends, time=time, expired=expired,
            available_until=available_until, pn=self.pn,
            apply_projects=apply_projects, mask=mask
        )
        session.add(package)
        session.commit()
        for tag in tags:
            package.tags.append(tag)
        session.commit()

        return package.id

    def list(self, name=None, page=None, page_size=None):
        query = session.query(Package).filter(
            Package.pn == self.pn, Package.is_deleted == 0)
        if name is not None:
            query = query.filter(Package.name.contains(name))

        query = query.order_by(Package.created_at.desc())
        paginator = Paginator(query, page, page_size)
        paginator_dict = paginator.to_dict()

        objects = paginator_dict.pop("objects")
        package_id_list = [p.id for p in objects]

        if package_id_list:
            orders = session.query(
                PackageOrder.package_id,
                func.sum(PackageOrder.amount).label("amount")
            ).filter(
                PackageOrder.package_id.in_(package_id_list)
            ).group_by(
                PackageOrder.package_id
            ).all()
            package_orders = {o.package_id: o.amount for o in orders}
        else:
            package_orders = {}

        packages = []
        for rv in objects:
            tags = ", ".join([t.name for t in rv.tags])
            package = {
                "id": rv.id, "name": rv.name, "time_length": rv.time_length,
                "price": rv.price, "ends": rv.ends,
                "until": rv.available_until,
                "tags": tags,
                "amount": package_orders.get(rv.id, 0),
                "created_at": rv.created_at
            }
            packages.append(package)

        paginator_dict["objects"] = packages
        return paginator_dict

    def get(self, package_id):
        package = session.query(Package).filter(
            Package.pn == self.pn, Package.id == package_id,
            Package.is_deleted == 0
        ).one_or_none()
        if not package:
            raise NotFoundError("套餐不存在")

        tags = ", ".join([t.name for t in package.tags])
        tag_list = [t.id for t in package.tags]

        package_dict = {
            "id": package.id,
            "name": package.name,
            "price": package.price,
            "ends": package.ends,
            "time": package.time,
            "expired": package.expired,
            "until": package.available_until,
            "mask": package.mask,
            "tags": tags,
            "tag_list": tag_list
        }
        if self.is_platform:
            project_id_list = json.loads(package.apply_projects)
            projects = ", ".join(map(str, project_id_list))
            package_dict["projects"] = projects
            package_dict["project_list"] = project_id_list

        if not self.is_platform and package.time:
            package_dict['time'] = package.time // 24

        return package_dict

    def update(self, package_id,
               available_until=None, tags=None, apply_projects=None):

        package = session.query(Package).filter(
            Package.pn == self.pn, Package.id == package_id,
            Package.is_deleted == 0
        ).one_or_none()
        if not package:
            raise NotFoundError("项目不存在")

        if available_until is not None:
            package.available_until = available_until

        if tags is not None:
            set_tags = [t.id for t in package.tags]
            id_to_add = list(set(tags) - set(set_tags))

            if id_to_add:
                tags_to_add = session.query(Tag).filter(
                    Tag.id.in_(id_to_add)).all()
                for t in tags_to_add:
                    package.tags.append(t)
            id_to_remove = list(set(set_tags) - set(tags))
            if id_to_remove:
                tags_to_remove = session.query(Tag).filter(
                    Tag.id.in_(id_to_remove)).all()
                for t in tags_to_remove:
                    package.tags.remove(t)

        if apply_projects is not None and self.is_platform:
            apply_projects = self._clean_projects(apply_projects)
            package.apply_projects = json.dumps(apply_projects)
        session.commit()

    def delete(self, package_id):
        rv = session.query(Package).filter(
            Package.pn == self.pn, Package.id == package_id
        ).update({"is_deleted": 1}, synchronize_session=False)
        session.commit()
        return rv
