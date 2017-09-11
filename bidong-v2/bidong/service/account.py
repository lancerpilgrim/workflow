"""
account.py
~~~
用户管理相关逻辑
"""
from datetime import datetime
from numbers import Number
from collections import defaultdict

import user_agents
from tornado import gen
from sqlalchemy import text, func, or_, and_, distinct
from sqlalchemy.sql import select

from bidong.core.auth import salt_password
from bidong.core.database import session
from bidong.core.exceptions import NotFoundError, DuplicateError
from bidong.core.paginator import Paginator
from bidong.common.validator import check_mobile
from bidong.common.utils import set_bit
from bidong.storage.models import Account, AccountProfile
from bidong.storage.models import PNField, Dyncol, Tag
from bidong.storage.models import Online, AP, Projects
from bidong.storage.models import account_tag_table
# from bidong.task.workers import offline_user


def user_had_registered(mobile):
    """
    去统一用户平台查询用户是否已经注册
    """
    return False


def fetch_user_info(mobile):
    """获取统一用户平台用户信息
    """
    return {}


def create_account(mobile, password, name, coin=0, ends=3):
    """创建平台站号，一个用户有一个唯一的账号
    """
    # mask & 1 > 0 标示激活
    mask = 1 if user_had_registered(mobile) else 0

    _password = salt_password(password)

    account = Account(
        user=mobile, password=_password, name=name,
        mask=mask, coin=coin, ends=ends, mobile=mobile
    )
    session.add(account)
    session.flush()
    account.user = account.id
    session.commit()
    return account.id


def update_account(account_id, **kwargs):
    """更新平台账号
    """
    valids = ('user', 'password', 'name', 'mask', 'coin', 'ends', 'mobile')
    if 'password' in kwargs:
        kwargs['password'] = salt_password(kwargs['password'])

    # only update those could update
    to_update = {k: kwargs[k] for k in valids if k in kwargs}
    session.query(Account).filter(Account.id == account_id).update(
        to_update, synchronize_session=False
    )
    session.commit()


def disable_account(account_id=None, mobile=None):
    if account_id is not None:
        account = session.query(
            Account).filter_by(id=account_id).one_or_none()
    else:
        account = session.query(Account).filter_by(
            mobile=mobile).one_or_none()
    account.mask = set_bit(account.mask, 30, 1)
    session.commit()


def get_account(account_id=None, user=None, mobile=None):
    query = session.query(Account)
    if account_id is not None:
        query = query.filter(Account.id == account_id)
    elif user is not None:
        query = query.filter(Account.user == user)
    elif mobile is not None:
        query = query.filter(Account.mobile == mobile)
    else:
        return None
    return query.one_or_none()


def base_profile(account_id):
    """获取平台用户基本信息
    """
    account = get_account(account_id)
    if not account:
        raise NotFoundError("用户不存在")

    profile = {"nickname": "", "mobile": account.mobile, "name": account.name}
    tags = [{"id": t.id, "name": t.name} for t in account.tags if t.pn == 0]
    profile["tags"] = tags
    return profile


def project_profiles(account_id):
    """获取平台用户在各个项目的详细资料
    """
    account = get_account(account_id)
    if not account:
        raise NotFoundError("用户不存在")

    records = session.query(AccountProfile).filter(
        AccountProfile.account_id == account_id
    ).all()

    profiles = []
    for r in records:
        project = session.query(Projects.name).filter(
            Projects.id == r.pn
        ).first()
        profile = {'project': project.name if project else ""}

        attrs = []
        dyncols = session.query(Dyncol.col, Dyncol.label).filter(
            Dyncol.id == PNField.dyncol_id, PNField.pn == r.pn
        ).all()
        for c in dyncols:
            attrs.append(
                {"label": c.label, "value": r.dynattr(c.col), "col": c.col})
        profile['attrs'] = attrs

        tags = ", ".join([t.name for t in account.tags if t.pn == r.pn])
        profile['tags'] = tags
        profiles.append(profile)

    return profiles


def get_default_dyncol():
    return session.query(Dyncol).all()


def account_overview():
    """获取总用户量等信息
    """
    rv = {}
    today = datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0)
    rv['total_user'] = session.query(Account).count()
    rv['online_user'] = session.query(Online).distinct(Online.user).count()
    rv['today_register'] = session.query(
            Account).filter(Account.created_at >= today).count()
    return rv


def attach_tags(account_id, tag_id_list, pn=0, reset=False):
    """贴标签
    Args:
        account_id: 账号id
        tag_id_list: 标签ID列表
    """
    account = session.query(Account).filter_by(id=account_id).first()
    attached = [t.id for t in account.tags if t.pn == pn]

    if tag_id_list:
        allow_tags = session.query(Tag.id).filter(
            Tag.pn == pn, Tag.id.in_(tag_id_list)
        ).all()
        tag_id_list = [rv.id for rv in allow_tags]

    to_attach = list(set(tag_id_list) - set(attached))
    if to_attach:
        tags = session.query(Tag).filter(Tag.id.in_(to_attach)).all()
        for tag in tags:
            account.tags.append(tag)

    if reset:
        to_remove = list(set(attached) - set(tag_id_list))
        if to_remove:
            tags = session.query(Tag).filter(Tag.id.in_(to_remove)).all()
            for tag in tags:
                account.tags.remove(tag)

    session.commit()


def account_list(page=None, page_size=None,
                 project_id=None, online=None, tag_id=None, keyword=None):
    """
    """
    filters = []
    choiced_account_list = []
    is_in_filter_trigger = False
    if page is not None and page_size is not None:
        to_paginate = True
    else:
        to_paginate = False

    if project_id is not None:
        rvs = session.query(AccountProfile.account_id).filter_by(
            pn=project_id).all()
        choiced_account_list.extend([rv.account_id for rv in rvs])
        is_in_filter_trigger = True

    if online == 0:
        filters.append(Online.user.is_(None))
    elif online == 1:
        filters.append(Online.user.isnot(None))

    # 要考虑项目和标签同时过滤
    if tag_id is not None:
        tag = session.query(Tag).filter_by(id=tag_id, pn=0).one_or_none()
        if tag:
            tagged_account_list = [a.id for a in tag.accounts.all()]
            if choiced_account_list:
                choiced_account_list = list(
                    set(choiced_account_list) & set(tagged_account_list)
                )
            else:
                choiced_account_list = tagged_account_list
        is_in_filter_trigger = True

    choiced_account_list = list(set(choiced_account_list))
    if choiced_account_list:
        filters.append(Account.id.in_(choiced_account_list))
    elif is_in_filter_trigger:
        filters.append(Account.id.in_([0]))

    if keyword is not None:
        filters.append(Account.has_keyword(keyword))

    query = session.query(
        Account.id, Account.mobile,
        Account.name, AP.address,
        func.IF(Online.user.is_(None), 0, 1).label("online"),
        func.IF(AP.address.is_(None), "", AP.address).label("address"),
        func.IF(AP.pn.is_(None), 0, AP.pn).label("pn"),
    ).outerjoin(
        Online, Online.user == Account.user
    ).outerjoin(
        AP, AP.mac == Online.ap_mac
    )

    if filters:
        query = query.filter(*filters)

    if to_paginate:
        paginator = Paginator(query, page, page_size)
        query = paginator.Query
        paginator_dict = paginator.to_dict()

    # TODO: 消灭这段重复的代码
    account_id_list = [rv.id for rv in query.all()]
    tags_dict = defaultdict(list)
    account_proejct_dict = defaultdict(list)
    if account_id_list:
        account_tags_query = select(
            [account_tag_table.c.account_id, Tag.name]
        ).where(
            (account_tag_table.c.account_id.in_(account_id_list)) &
            (Tag.id == account_tag_table.c.tag_id) &
            (Tag.pn == 0)
        )
        results = session.execute(account_tags_query).fetchall()
        for rv in results:
            tags_dict[rv[0]].append(rv[1])

        rvs = session.query(
            AccountProfile.account_id, AccountProfile.pn,
            Projects.name
        ).filter(
            Projects.id == AccountProfile.pn,
            AccountProfile.account_id.in_(account_id_list),
        ).all()
        for rv in rvs:
            account_proejct_dict[rv.account_id].append(rv.name)

    # TODO: duplicate code, reduces it
    project_dict = {}
    projects = session.query(Projects.id, Projects.name).all()
    for p in projects:
        project_dict[p.id] = p.name

    if to_paginate:
        objects = paginator_dict.pop("objects")
    else:
        objects = query.all()
    account_list = []
    for rv in objects:
        tag = ", ".join(tags_dict.get(rv.id, []))
        if rv.address:
            address = "{}, {}".format(
                project_dict.get(rv.pn, ""), rv.address
            )
        else:
            address = ""

        if rv.id not in account_proejct_dict:
            belong = "平台"
        else:
            belong = ", ".join(account_proejct_dict[rv.id])
        a_dict = {
            "id": rv.id, "name": rv.name, "mobile": rv.mobile,
            "belong": belong, "online": rv.online, "address": address,
            "tags": tag
        }
        account_list.append(a_dict)

    if to_paginate:
        paginator_dict["objects"] = account_list
        return paginator_dict

    return account_list


@gen.coroutine
def gen_account_export_data(
        project_id=None, online=None, tag_id=None, keyword=None):
    account_dict_list = account_list(
        None, None, project_id, online, tag_id, keyword
    )
    headers = [
        "id,用户ID", "name,用户姓名", "mobile,手机号码", "belong,所属项目",
        "address,当前位置", "tags,标签", "online,状态"
    ]

    contents = []
    for rv in account_dict_list:
        row = []
        for header in headers:
            key = header.split(',')[0]
            if key == 'online':
                status = '在线' if rv[key] else '离线'
                row.append(status)
            else:
                row.append(rv[key])
        contents.append(row)

    headers = [h.split(',')[1] for h in headers]
    return headers, contents


class ProjectAccountService:
    """项目用户管理
    """

    def __init__(self, pn):
        """
        Args:
            project_id: 项目ID
        """
        self.pn = int(pn)

    def set_dyncol(self, col_id_list):
        rvs = session.query(Dyncol.id).all()
        sys_colids = [rv.id for rv in rvs]
        # 清理掉不存在的列id
        col_id_list = list(set(col_id_list) & set(sys_colids))

        rvs = session.query(PNField.dyncol_id).filter(
            PNField.pn == self.pn
        ).all()
        existed_ids = [rv.dyncol_id for rv in rvs]

        to_add = list(set(col_id_list) - set(existed_ids))
        to_remove = list(set(existed_ids) - set(col_id_list))

        for cid in to_add:
            pnfiled = PNField(pn=self.pn, dyncol_id=cid)
            session.add(pnfiled)

        if to_remove:
            session.query(PNField).filter(
                PNField.dyncol_id.in_(to_remove)
            ).delete(
                synchronize_session=False
            )

        session.commit()

    def get_dyncol(self):
        rvs = session.query(
            Dyncol.id.label("id"), Dyncol.col.label("col"),
            Dyncol.label.label("label")
        ).join(
            PNField, Dyncol.id == PNField.dyncol_id
        ).filter(
            PNField.pn == self.pn
        ).all()
        return rvs

    def create_profile(self, account_id, name, mobile, attr_dict):
        """创建项目用户信息
        Args:
            pn: 归属项目
            account_id: 项目id
            attr_dict: 自定义属性 {"school": "", ...}
        """
        attrs = []
        for k, v in attr_dict.items():
            attrs.extend([k, v])

        if attrs:
            dyncol_text = str(tuple(attrs))
            dyncol = text("COLUMN_CREATE" + dyncol_text)
        else:
            dyncol = None

        profile = AccountProfile(
            account_id=account_id, pn=self.pn, name=name,
            mobile=mobile, dyncol=dyncol
        )
        session.add(profile)
        session.commit()

        return profile.id

    def update_profile(self, profile_id,
                       name=None, mobile=None, attr_dict=None):
        """更新项目用户信息
        """
        to_update = {}
        if name is not None:
            to_update['name'] = name
        if mobile is not None:
            to_update['mobile'] = mobile

        if attr_dict is not None:
            attrs = []
            for k, v in attr_dict.items():
                attrs.extend([k, v])

            dyncol_text = str(tuple(attrs))[1:]
            dyncol = text("COLUMN_ADD(dyncol, " + dyncol_text)
            to_update['dyncol'] = dyncol

        session.query(AccountProfile).filter(
            AccountProfile.id == profile_id
        ).update(
            to_update, synchronize_session=False
        )
        session.commit()

    def get_profile(self, profile_id):
        """获取项目用户信息
        """
        profile = session.query(AccountProfile).filter_by(
            pn=self.pn, id=profile_id
        ).first()
        if not profile:
            raise NotFoundError("用户不存在")

        dyncols = session.query(Dyncol).filter(
            Dyncol.id == PNField.dyncol_id, PNField.pn == self.pn
        ).all()

        attrs = []
        for c in dyncols:
            attr = {"id": c.id, "label": c.label,
                    "value": profile.dynattr(c.col), "col": c.col}
            attrs.append(attr)

        account = session.query(
            Account).filter_by(id=profile.account_id).first()
        tags = []
        if account:
            for rv in account.tags:
                if rv.pn == self.pn:
                    tag = {"id": rv.id, "name": rv.name}
                    tags.append(tag)

        profile_dict = {
            "nickname": "",
            "mobile": profile.mobile,
            "name": profile.name,
            "attrs": attrs,
            "tags": tags
        }
        return profile_dict

    def delete_profile(self, profile_id=None, batch_delete=None):
        if profile_id is not None:
            ids = [profile_id]
        elif batch_delete is not None:
            ids = batch_delete
        else:
            ids = [0]

        accounts = session.query(AccountProfile.account_id).filter(
            AccountProfile.pn == self.pn,
            AccountProfile.id.in_(ids)
        ).all()
        account_id_list = [rv.account_id for rv in accounts]

        tags = session.query(Tag.id).filter(
            Tag.pn == self.pn,
            Tag.tag_type == Tag.ACCOUNT_TAG
        ).all()
        tag_id_list = [rv.id for rv in tags]

        # 删项目用户顺便删标签
        if account_id_list and tag_id_list:
            sql = account_tag_table.delete().where(
                and_(
                    account_tag_table.c.account_id.in_(account_id_list),
                    account_tag_table.c.tag_id.in_(tag_id_list)
                )
            )
            session.execute(sql)

        session.query(AccountProfile).filter(
            AccountProfile.pn == self.pn,
            AccountProfile.id.in_(ids)
        ).delete(
            synchronize_session=False
        )
        session.commit()

    def _clean_dyncol_attr(self, attrs):
        """将动态列id 和 字段值清洗成自由在系统中设置过才行
        Args:
            pn: 项目id
            attrs: [{"col": 字段id, "value": 字段值}, ...]
        Returns:
            dict, {"col": value, ...}
        """
        dyncols = self.get_dyncol()
        dyncol_dict = {rv.id: rv.col for rv in dyncols}

        attr_dict = {}
        for attr in attrs:
            col_id = attr['col']
            if col_id in dyncol_dict:
                attr_dict[dyncol_dict[col_id]] = attr['value']

        return attr_dict

    def create(self, name, mobile, attrs, tags):
        """创建项目账号
        Args:
            name: 姓名
            mobile: 手机号码
            attrs: 自定义属性字段[{"col": 字段id, "value": 字段值}, ...]
            tags: 标签列表
        Return:
            bool, True - create success, False - other
        """
        account = session.query(
            Account.id).filter_by(mobile=mobile).first()
        if not account:
            account_id = create_account(mobile, '', name)
        else:
            account_id = account.id

        profile_exists = session.query(AccountProfile).filter_by(
            account_id=account_id, pn=self.pn).count()
        if profile_exists:
            return False

        attr_dict = self._clean_dyncol_attr(attrs)
        self.create_profile(account_id, name, mobile, attr_dict)
        if tags:
            attach_tags(account_id, tags, pn=self.pn)
        return True

    def update(self, profile_id, mobile, name, attrs, tags):
        profile = session.query(AccountProfile.id).filter(
            AccountProfile.mobile == mobile, AccountProfile.id != profile_id
        ).first()
        if profile:
            raise DuplicateError("手机号码重复")

        profile = session.query(AccountProfile.account_id).filter_by(
            id=profile_id, pn=self.pn).first()
        if not profile:
            raise NotFoundError("用户不存在")

        # Warning:修改用户信息，用户基础表是否跟着改变, 目前是
        update_account(profile.account_id, name=name, mobile=mobile)

        attr_dict = self._clean_dyncol_attr(attrs)
        self.update_profile(profile_id, name=name,
                            mobile=mobile, attr_dict=attr_dict)
        if tags:
            attach_tags(profile.account_id, tags, pn=self.pn, reset=True)

    def fetch(
            self, online=None, tag_id=None, keyword=None,
            page=None, page_size=None):
        """获取项目用户列表, 这个鬼东西不知道需求怎么提的
        Args:
            pn: 项目编号
            online: 是否在线, 0 - 否，1 - 是, None - 全部
            tag_id: tag id, None - 全部
        Return:
            - with page and page_size: paginator_dict
            - without page and page_size: list of dict
        """
        to_paginate = False
        filters = []

        if online == 0:
            filters.append(Online.user.is_(None))
        elif online == 1:
            filters.append(Online.user.isnot(None))

        if tag_id is not None:
            tag = session.query(Tag).filter_by(
                id=tag_id, pn=self.pn).one_or_none()
            if tag:
                accounts_id = [a.id for a in tag.accounts.all()]
                if accounts_id:
                    filters.append(Account.id.in_(accounts_id))
                else:
                    filters.append(Account.id.in_([0]))
            else:
                filters.append(Account.id.in_([0]))

        if keyword is not None:
            filters.append(AccountProfile.has_keyword(keyword))

        if page and page_size:
            to_paginate = True

        query = session.query(
            AccountProfile.id, AccountProfile.name,
            AccountProfile.mobile, Account.id.label("account_id"),
            func.IF(Online.user.is_(None), 0, 1).label("online"),
            func.IF(AP.address.is_(None), "", AP.address).label("address")
        ).join(
            Account, AccountProfile.account_id == Account.id
        ).outerjoin(
            Online, Online.user == Account.user
        ).outerjoin(
            AP, AP.mac == Online.ap_mac
        ).filter(
            AccountProfile.pn == self.pn
        )

        if filters:
            query = query.filter(*filters)

        if to_paginate:
            paginator_dict = {}
            paginator = Paginator(query, page, page_size)
            paginator_dict.update(paginator.to_dict())
            paginator_dict.pop("objects")
            query = paginator.Query

        account_id_list = [rv.account_id for rv in query.all()]
        tags_dict = defaultdict(list)
        if account_id_list:
            account_tags_query = select(
                [account_tag_table.c.account_id, Tag.name]
            ).where(
                (account_tag_table.c.account_id.in_(account_id_list)) &
                (Tag.id == account_tag_table.c.tag_id) &
                (Tag.pn == self.pn)
            )
            results = session.execute(account_tags_query).fetchall()
            for rv in results:
                tags_dict[rv[0]].append(rv[1])

        profile_list = []
        for rv in query.all():
            tag = ", ".join(tags_dict.get(rv.account_id, []))
            p = {
                "id": rv.id, "name": rv.name, "mobile": rv.mobile,
                "online": rv.online, "address": rv.address, "tags": tag
            }
            profile_list.append(p)

        if to_paginate:
            paginator_dict['objects'] = profile_list
            return paginator_dict

        return profile_list

    def overview(self):
        """获取项目用户数量，在线用户数等
        """
        rv = {}
        rv['total_user'] = session.query(
            AccountProfile).filter_by(pn=self.pn).count()
        rv['online_user'] = session.query(AccountProfile).filter(
            AccountProfile.account_id == Account.id,
            Online.user == Account.user
        ).count()
        return rv

    def _parse_agents(self, platform):
        """获取用户客户端即上网方式，后期应该优化
        """
        if not platform:
            return "未知", "未知"
        if "micromessenger" in platform or "WeChat" in platform:
            return "微信", "微信"

        agent = user_agents.parse(platform)
        os_family = agent.os.family
        return os_family, "APP"

    def list_visitors(self, keyword=None, page=None, page_size=None):
        """获取项目在线访客
        """
        query = session.query(
            Account.mobile, Account.nickname, Account.id.label("account_id"),
            AP.address, Online.acct_start_time,
            Online.auth_type, AccountProfile.id
        ).outerjoin(
            AccountProfile, AccountProfile.account_id == Account.id
        ).filter(
            Online.pn == self.pn,
            Online.user == Account.user,
            Online.ap_mac == AP.mac,
            or_(
                AccountProfile.id.is_(None),
                AccountProfile.pn != self.pn
            )
        )
        if keyword is not None:
            query = query.filter(Account.has_keyword(keyword))

        # 流量先返回0，从ticket计算性能有问题
        paginator = Paginator(query, page, page_size)
        paginator_dict = paginator.to_dict()
        rvs = paginator_dict.pop("objects")
        objects = []
        for rv in rvs:
            p = {
                "userid": rv.account_id,
                "user": rv.mobile if rv.mobile else rv.nickname,
                "address": rv.address, "connect_at": rv.acct_start_time,
                "auth_type": rv.auth_type,
                "traffic": 0
            }
            objects.append(p)

        paginator_dict["objects"] = objects
        return paginator_dict

    def kick_out_visitor(self, userid):
        """将游客下线, #TODO: 这里有一个异步任务，下线时通知portal进行下线
        """
        account = session.query(Account).filter(Account.id == userid).first()
        if not account:
            return False

        success = session.query(Online).filter(
            Online.pn == self.pn, Online.user == account.user
        ).delete(synchronize_session=False)
        session.commit()
        # if success:
        #     offline_user.apply_async((self.pn, account.id, account.user))
        return success

    @gen.coroutine
    def gen_export_data(self, online=None, tag_id=None, keyword=None):
        """生成导出文件
        Args:
            online: 是否在线
            tag_id: tag标签id
            keyword: 关键词
        Returns:
            headers: list, [], 标题
            content: list of list, [[], [], ...] 标题对应的内容
        """
        fixed_attrs = self.fetch(online, tag_id, keyword)
        headers = ['id,用户ID', 'name,姓名', 'mobile,手机号码',
                   'address,当前位置', 'tags,标签', 'online,状态']
        choiced_profile_list = [rv['id'] for rv in fixed_attrs]

        # 动态列
        dyncol_dict = {rv.col: rv.label for rv in self.get_dyncol()}
        # id,列标题
        headers.extend(['{},{}'.format(k, v) for k, v in dyncol_dict.items()])

        profiles = session.query(AccountProfile).filter(
            AccountProfile.pn == self.pn,
            AccountProfile.id.in_(choiced_profile_list)
        ).all()
        customed_attrs = [rv.dyndatautf8 for rv in profiles]

        content = []
        for fix, custom in zip(fixed_attrs, customed_attrs):
            items = []
            for header in headers:
                key = header.split(',')[0]
                if key == 'online':
                    value = '在线' if fix.get(key) else '离线'
                else:
                    value = (fix.get(key) if fix.get(key)
                             else custom.get(key, ''))
                items.append(value)
            content.append(items)

        headers = [header.split(',')[-1] for header in headers]
        return headers, content

    @gen.coroutine
    def get_template_headers(self):
        """导入模版标头
        """
        headers = ['姓名', '手机号码']
        dyncols = self.get_dyncol()
        for rv in dyncols:
            if rv.col.endswith('_image'):
                continue
            headers.append(rv.label)

        headers.append('标签')
        return headers, []

    def load_import_data(self, headers, content):
        """从excel表导入数据
        Args:
            headers: 表头
            content: 二维矩阵形式excel的内容
        """
        errors = []

        dyncols = self.get_dyncol()
        dyncol_dict = {rv.label: rv.id for rv in dyncols}
        tags = session.query(Tag.id, Tag.name).filter_by(
            pn=self.pn, tag_type=Tag.ACCOUNT_TAG
        ).all()
        tag_dict = {rv.name: rv.id for rv in tags}

        for idx, items in enumerate(content):
            skip = False
            kwargs = {'attrs': []}
            for key, value in zip(headers, items):
                if isinstance(value, Number):
                    value = str(int(value))

                if key == '姓名':
                    if value:
                        kwargs['name'] = value
                    else:
                        msg = "{}行姓名不能为空".format(idx+1)
                        errors.append(msg)
                elif key == '手机号码':
                    if check_mobile(value):
                        kwargs['mobile'] = value
                    else:
                        msg = "{}行手机格式错误".format(idx+1)
                        errors.append(msg)
                        skip = True
                        continue
                elif key == '标签':
                    tags = value.split(',')
                    tags = [tag_dict.get(t) for t in tags if t in tag_dict]
                    kwargs['tags'] = tags
                else:
                    if key in dyncol_dict:
                        rv = {"col": dyncol_dict[key], "value": value}
                        kwargs['attrs'].append(rv)

            if not skip:
                success = self.create(**kwargs)
                if not success:
                    errors.append("{}重复录入".format(idx+1))
        return errors


def get_projects_user_count(project_id_list=None):
    """获取项目对应的专网用户数
    Args:
        project_id_list: list, 项目ID列表
    Returns:
        dict, {"project1_id": user_count1, "proejct1_id": user_count2}
    """
    query = session.query(
        AccountProfile.pn, func.count(AccountProfile.id).label("count"))
    if project_id_list:
        query = query.filter(AccountProfile.pn.in_(project_id_list))

    rvs = query.group_by(AccountProfile.pn)
    project_user_count = {rv.pn: rv.count for rv in rvs}
    return project_user_count


def get_user_count_by_project(project_id):
    """获取项目的专网用户数
    Args:
        project_id: integer, 项目ID
    Returns:
        integer, 专网用户数
    """
    count = session.query(func.count(AccountProfile.id)).filter(
        AccountProfile.pn == project_id
    ).scalar()
    return count if count else 0


def get_online_user_count_by_project(project_id):
    """获取项目在线用户数
    Args:
        project_id: integer, 项目ID
    Returns:
        integer, 在线用户数
    """
    count = session.query(func.count(distinct(Online.user))).filter(
        Online.pn == project_id
    ).scalar()
    return count if count else 0
