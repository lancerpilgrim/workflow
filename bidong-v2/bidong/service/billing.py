from datetime import datetime

from tornado import gen
from sqlalchemy import func

from bidong.core.database import session
from bidong.core.exceptions import NotFoundError
from bidong.core.paginator import Paginator
from bidong.storage.models import PackageOrder, Package
from bidong.storage.models import Account, Projects


class OrderService:

    def __init__(self, pn=0, is_platform=False):
        """
        Args:
            pn: 项目ID，平台订单则为0
            is_platform: 是否为平台
        """
        self.pn = int(pn)
        self.is_platform = is_platform

    def create(self, package_id, account_id, amount, pay_with, pay_from):
        package = session.query(Package).filter(
            Package.id == package_id).first()
        if not package:
            raise NotFoundError("套餐不存在")

        account = session.query(Account).filter(
            Account.id == account_id).first()
        if not account:
            raise NotFoundError("找不到用户")

        order = PackageOrder(
            package_id, account_id, amount, pay_with, pay_from)
        session.add(order)
        session.commit()

        return order.id

    def list(self, begin, end,
             page=None, page_size=None, keyword=None, project_id=None):
        """订单列表
        """

        filters = []
        if self.pn:
            filters.append(Package.pn == self.pn)
        if self.is_platform and project_id is not None:
            filters.append(Package.pn == project_id)
        if keyword is not None:
            filters.append(Package.name.contains(keyword))

        query = session.query(
            PackageOrder.id, Account.mobile, Account.name.label("username"),
            PackageOrder.pay_with, PackageOrder.pay_from,
            Package.name.label("package_name"), Package.pn,
            PackageOrder.amount, PackageOrder.created_at
        ).join(
            Account, PackageOrder.account_id == Account.id
        ).join(
            Package, PackageOrder.package_id == Package.id
        ).filter(
            func.date(PackageOrder.created_at) >= begin.date(),
            func.date(PackageOrder.created_at) <= end.date()
        )
        if filters:
            query = query.filter(*filters)

        if page and page_size:
            paginator = Paginator(query, page, page_size)
            return paginator.to_dict()

        return query.all()

    def overview(self, project_id=None):
        """
        收入概览
        """
        query = session.query(func.sum(PackageOrder.amount))

        if self.pn:
            query = query.filter(
                Package.pn == self.pn,
                PackageOrder.package_id == Package.id
            )
        elif self.is_platform and project_id is not None:
            query = query.filter(
                Package.pn == project_id,
                PackageOrder.package_id == Package.id
            )

        total_amount = query.scalar()
        total_amount = total_amount if total_amount else 0.0

        today = datetime.now().date()
        today_amount = query.filter(
            func.date(PackageOrder.created_at) >= today
        ).scalar()
        today_amount = today_amount if today_amount else 0.0
        return {"today_amount": today_amount, "total_amount": total_amount}

    def chart(self, begin, end, project_id=None):
        """
        订单图表数据
        Args:
            begin: 开始时间
            end: 结束时间
            project_id: 项目ID，仅在平台逻辑中使用
        Returns:
            dict, examples:
            {
                "title": "平台|xx项目"
                "dates": [],
                "amounts": []
            }
        """
        query = session.query(
            func.date(PackageOrder.created_at).label("timestamp"),
            func.sum(PackageOrder.amount).label("total_amount")
        ).filter(
            func.date(PackageOrder.created_at) >= begin,
            func.date(PackageOrder.created_at) <= end,
        )

        if self.pn:
            query = query.filter(
                Package.pn == self.pn,
                PackageOrder.package_id == Package.id
            )
            title = '{}项目'.format(self.pn)
        elif self.is_platform and project_id is not None:
            query = query.filter(
                Package.pn == project_id,
                PackageOrder.package_id == Package.id
            )
            title = '{}项目'.format(project_id)
        else:
            title = '平台'

        dates = []
        amounts = []
        stats = query.group_by(func.date(PackageOrder.created_at)).all()
        for rv in stats:
            dates.append(rv.timestamp.strftime("%m-%d"))
            amounts.append(float(rv.total_amount))

        return {"title": title, "dates": dates, "amounts": amounts}

    @gen.coroutine
    def gen_project_order_data(self, begin, end, keyword):
        records = self.list(begin, end, keyword=keyword)
        heaers = [
            'mobile,手机号', 'username,姓名', 'pay_with,支付方式',
            "pay_from,充值入口", "package_name,套餐", "amount,金额",
            "created_at,日期"
        ]
        content = []
        for item in records:
            values = []
            for rv in heaers:
                col = rv.split(',')[0]
                if col == 'created_at':
                    values.append(getattr(item, col).strftime("%Y-%m-%d"))
                else:
                    values.append(getattr(item, col))
            content.append(values)

        headers = [rv.split(',')[1] for rv in heaers]
        return headers, content

    @gen.coroutine
    def gen_platform_order_data(self, begin, end, keyword, project_id):
        records = self.list(begin, end, keyword=keyword, project_id=project_id)

        project_dict = {0: "平台"}
        projects = session.query(Projects.id, Projects.name).all()
        for p in projects:
            project_dict[p.id] = p.name

        heaers = [
            'mobile,手机号', 'username,姓名', 'pay_with,支付方式',
            "pay_from,充值入口", "package_name,套餐", "pn,来源项目",
            "amount,金额", "created_at,日期"
        ]
        content = []
        for item in records:
            values = []
            for rv in heaers:
                col = rv.split(',')[0]
                if col == 'pn':
                    project_id = getattr(item, col)
                    project_name = project_dict.get(project_id, '')
                    values.append(project_name)
                elif col == 'created_at':
                    values.append(getattr(item, col).strftime("%Y-%m-%d"))
                else:
                    values.append(getattr(item, col))
            content.append(values)

        headers = [rv.split(',')[1] for rv in heaers]
        return headers, content
