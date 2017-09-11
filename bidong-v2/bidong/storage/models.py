import json

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import func, text
from sqlalchemy import Integer, SmallInteger, String, DateTime, Text, Float
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from sqlalchemy.ext.declarative import declarative_base

from bidong.core.database import engines

Base = declarative_base()

account_tag_table = Table(
    "bd_account_tag", Base.metadata,
    Column("account_id", Integer, ForeignKey("bd_account.id")),
    Column("tag_id", Integer, ForeignKey("bd_tag.id"))
)

package_tag_table = Table(
    "bd_package_tag", Base.metadata,
    Column("package_id", Integer, ForeignKey("bd_package.id")),
    Column("tag_id", Integer, ForeignKey("bd_tag.id"))
)

ap_tag_table = Table(
    "bd_ap_tag", Base.metadata,
    Column("ap_id", Integer, ForeignKey("bd_ap.id")),
    Column("tag_id", Integer, ForeignKey("bd_tag.id"))
)

ticket_table = Table(
    "bd_ticket", Base.metadata, autoload=True,
    autoload_with=engines["slave"]
)


class Letter(Base):
    __tablename__ = "bd_letter"

    DRAFT = 0
    PUBLIC = 1
    DELETED = 2

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128))
    content = Column(Text)
    status = Column(SmallInteger, default=0)
    created_by = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())


class Mailbox(Base):
    __tablename__ = "bd_mailbox"

    UNREAD = 0
    READ = 1
    DELETED = 2

    id = Column(Integer, primary_key=True, autoincrement=True)
    letter_id = Column(Integer)
    receiver_id = Column(Integer)
    title = Column(String(128))
    content = Column(Text)
    is_broadcast = Column(SmallInteger, default=1)
    status = Column(SmallInteger, default=0)
    created_at = Column(DateTime, server_default=func.now())


class Dyncol(Base):
    __tablename__ = "bd_dyncol"

    id = Column(Integer, primary_key=True, autoincrement=True)
    col = Column(String(32))
    label = Column(String(32))
    created_at = Column(DateTime, server_default=func.now())


class PNField(Base):
    __tablename__ = "bd_pn_field"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pn = Column(Integer)
    dyncol_id = Column(Integer)


class Tag(Base):
    __tablename__ = "bd_tag"

    ACCOUNT_TAG = 'account'
    PACKAGE_TAG = 'package'
    AP_TAG = 'ap'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pn = Column(Integer, default=0)
    tag_type = Column(String(64))
    name = Column(String(32))
    created_at = Column(DateTime, server_default=func.now())

    accounts = relationship(
        "Account", secondary=account_tag_table,
        back_populates="tags", lazy="dynamic"
    )
    packages = relationship(
        "Package", secondary=package_tag_table,
        back_populates="tags", lazy="dynamic"
    )
    aps = relationship(
        "AP", secondary=ap_tag_table,
        back_populates="tags", lazy="dynamic"
    )

    @hybrid_property
    def tagged_count(self):
        if self.tag_type == self.ACCOUNT_TAG:
            return self.accounts.count()
        elif self.tag_type == self.AP_TAG:
            return self.aps.count()
        else:
            return 0


class Online(Base):
    __tablename__ = "bd_online"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(32))
    nas_addr = Column(String(32), default="")
    acct_session_id = Column(String(32), default="")
    acct_start_time = Column(DateTime, server_default=func.now())
    framed_ipaddr = Column(String(32), default="")
    mac_addr = Column(String(32), default="")
    billing_times = Column(Integer, default=0)
    input_total = Column(Integer, default=0)
    output_total = Column(Integer, default=0)
    start_source = Column(SmallInteger, default=0)
    pn = Column(Integer, default=0)
    ssid = Column(String(32), default="")
    ap_mac = Column(String(24))
    is_auto = Column(SmallInteger, default=0)
    auth_type = Column(SmallInteger, default=0)


class Account(Base):
    __tablename__ = "bd_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(32))
    password = Column(String(128))
    name = Column(String(64))
    nickname = Column(String(64))
    mask = Column(Integer, default=0)
    coin = Column(Integer, default=0)
    ends = Column(SmallInteger, default=3)
    mobile = Column(String(17), default='')

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    tags = relationship(
        "Tag", secondary=account_tag_table,
        back_populates="accounts"
    )

    @hybrid_property
    def tag_text(self):
        return ", ".join([t.name for t in self.tags])

    @hybrid_method
    def has_keyword(self, keyword):
        return (self.name.contains(keyword) | self.mobile.contains(keyword) |
                self.nickname.contains(keyword))


class AccountPolicy(Base):
    __tablename__ = "bd_account_policy"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer)
    pn = Column(Integer)
    mask = Column(Integer, default=0)
    expired = Column(DateTime)
    ends = Column(Integer)
    uplink = Column(Integer, default=0)
    downlink = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


class AccountProfile(Base):
    __tablename__ = "bd_account_profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer)
    pn = Column(Integer)
    name = Column(String(64))
    mobile = Column(String(17))
    dyncol = Column(MEDIUMBLOB)
    dyndata = column_property(func.column_json(dyncol))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    @hybrid_property
    def dyndatautf8(self):
        try:
            return json.loads(self.dyndata.decode('utf-8'))
        except:
            return {}

    @hybrid_method
    def dynattr(self, key):
        data = self.dyndatautf8
        if key in data:
            return data[key]

    @dynattr.expression
    def dynattr(cls, key):
        return func.column_get(cls.dyncol, text('"{}" as char'.format(key)))

    @hybrid_method
    def has_keyword(self, keyword):
        return self.name.contains(keyword) | self.mobile.contains(keyword)


class Package(Base):
    __tablename__ = "bd_package"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    price = Column(Float(asdecimal=True))
    time = Column(Float)
    ends = Column(SmallInteger, default=3)
    expired = Column(DateTime)
    available_until = Column(DateTime)
    mask = Column(Integer, default=0)
    pn = Column(Integer, default=0)
    is_deleted = Column(SmallInteger, default=0)
    apply_projects = Column(String(256), default='[]')

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    tags = relationship(
        "Tag", secondary=package_tag_table,
        back_populates="packages"
    )

    @hybrid_property
    def time_length(self):
        if self.time:
            if self.mask & 1:
                return "{}小时".format(int(self.time))
            else:
                return "{}天".format(int(self.time // 24))
        else:
            return self.expired.strftime("%Y-%m-%d")


class AC(Base):
    __tablename__ = "bd_ac"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    vendor = Column(String(32))
    ip = Column(String(32))
    secret = Column(String(64))
    coa_port = Column(SmallInteger, default=3799)
    pip = Column(String(15), default='')
    port = Column(SmallInteger, default=0)

    created_at = Column(DateTime, server_default=func.now())

    @hybrid_method
    def has_keyword(self, keyword):
        return (self.name.contains(keyword) | self.ip.contains(keyword))


class AP(Base):
    __tablename__ = "bd_ap"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pn = Column(Integer)
    mac = Column(String(32))
    vendor = Column(String(16))
    name = Column(String(128))
    ip = Column(String(16))
    address = Column(String(64))
    ac_ip = Column(String(16))
    is_online = Column(SmallInteger, default=0)
    mpoi_id = Column(Integer)
    connections = Column(Integer, default=0)
    model = Column(String(32))
    is_sens = Column(SmallInteger, default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    tags = relationship(
        "Tag", secondary=ap_tag_table,
        back_populates="aps"
    )

    @hybrid_method
    def has_keyword(self, keyword):
        return (self.name.contains(keyword) | self.address.contains(keyword) |
                self.mac.contains(keyword))


class MacHistory(Base):
    __tablename__ = "bd_mac_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(32))
    mac = Column(String(17), default="")
    tlogin = Column(DateTime, server_default=func.now())
    platform = Column(String(256), default="")
    expired = Column(DateTime, server_default=func.now())
    ssid = Column(String(32), default="")


class PackageOrder(Base):
    __tablename__ = "bd_package_order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey("bd_package.id"))
    account_id = Column(Integer, ForeignKey("bd_account.id"))
    amount = Column(Float(asdecimal=True))
    pay_with = Column(String(32))
    pay_from = Column(String(32))

    created_at = Column(DateTime, server_default=func.now())


class Portal(Base):
    __tablename__ = "bd_portal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pn = Column(Integer, default=0)
    name = Column(String(32))
    note = Column(String(128))
    mobile_title = Column(String(64))
    mobile_banner_url = Column(String(256))
    pc_title = Column(String(64))
    pc_banner_url = Column(String(256))
    on_using = Column(SmallInteger, default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


class WechatOfficialAccount(Base):
    __tablename__ = "bd_wechat_official_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pn = Column(Integer)
    name = Column(String(32))
    appid = Column(String(32))
    shopid = Column(String(32))
    secret = Column(String(32))
    note = Column(String(128))
    is_deleted = Column(SmallInteger, default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    @hybrid_method
    def has_keyword(self, keyword):
        return (self.name.contains(keyword) | self.appid.contains(keyword) |
                self.shopid.contains(keyword))


class CouponCode(Base):
    __tablename__ = "bd_coupon_code"

    USEABLE = 0
    USED = 1
    EXPIRED = 2

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(32))
    hours = Column(SmallInteger)
    is_used = Column(SmallInteger, default=0)
    serial_id = Column(Integer)
    expired = Column(DateTime)


class CouponSerial(Base):
    __tablename__ = "bd_coupon_serial"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_by = Column(Integer)
    serial = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())


class CouponUsedRecord(Base):
    __tablename__ = "bd_coupon_used_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(32))
    account_id = Column(Integer)
    hours = Column(SmallInteger)
    created_at = Column(DateTime, server_default=func.now())


class NetworkConfig(Base):
    __tablename__ = "bd_network_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pn = Column(Integer)
    ssid = Column(String(32))
    portal_id = Column(Integer, default=0)
    is_public = Column(SmallInteger, default=1)
    is_free = Column(SmallInteger, default=1)
    mask = Column(Integer)
    wechat_account_id = Column(Integer)
    duration = Column(Integer, default=30)
    session_timeout = Column(Integer, default=24)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


class Administrators(Base):

    __tablename__ = 'administrators'

    DISABLED = 0
    ENABLED = 1
    DELETE = 2

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mobile = Column(Integer, unique=True, nullable=False)
    create_time = Column(Integer)
    description = Column(String)
    status = Column(Integer, default=1)

    def __repr__(self):
        return '<Administrators: name={}, mobile={}>'.format(
            self.name, self.mobile)

    @hybrid_property
    def is_enable(self):
        return self.status == self.ENABLED


class Managers(Base):

    __tablename__ = 'managers'

    DISABLED = 0
    ENABLED = 1
    DELETE = 2

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mobile = Column(Integer, unique=True,nullable=False)
    create_time = Column(Integer)
    description = Column(String)
    status = Column(Integer, default=1)

    def __repr__(self):
        return '<Managers: name={}, mobile={}>'.format(
            self.name, self.mobile)

    @hybrid_property
    def is_enable(self):
        return self.status == self.ENABLED


class Projects(Base):
    __tablename__ = 'projects'

    DISABLED = 0
    ENABLED = 1
    DELETE = 2

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    contact_number = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    auth_ap_amount = Column(Integer, nullable=False, default=0)
    create_time = Column(Integer)
    expiration_time = Column(Integer, nullable=False, default=0)
    status = Column(Integer, default=1)

    def __repr__(self):
        return '<Projects: name={}>'.format(
            self.name)


class ResourceRegistry(Base):

    __tablename__ = "resources_registry"

    FEATURE = 1  # 功能性资源
    DATA = 2  # 数据资源

    GLOBAL = 0
    PLATFORM = 1  # 专属于平台的资源
    CLIENT = 2

    id = Column(Integer, primary_key=True)
    resource_type = Column(Integer, nullable=False, default=FEATURE)
    description = Column(String, nullable=False)
    public_name = Column(String, nullable=False)
    private_name = Column(String, nullable=False)
    update_time = Column(Integer, nullable=False)
    ascription = Column(Integer, nullable=False, default=GLOBAL)
    status = Column(Integer, default=1)

    def __repr__(self):
        return '<resource: name={}>'.format(
            self.private_name)


class ResourceTree(Base):

    __tablename__ = 'resources_tree'

    id = Column(Integer, primary_key=True)
    ancestor = Column(Integer, nullable=True)
    descendant = Column(Integer, nullable=True)
    ancestor_name = Column(String, nullable=False)
    descendant_name = Column(String, nullable=False)
    distance = Column(Integer, nullable=False)

    def __repr__(self):
        return '<resource relationship: ancestor name is {}, descendant is {}>'.format(
            self.ancestor_name, self.descendant_name)


class AdministratorsAuthorization(Base):

    __tablename__ = 'administrators_authorization'

    DISABLED = 0
    ENABLED = 1
    DELETE = 2

    id = Column(Integer, primary_key=True)
    authorization_holder = Column(Integer, nullable=False)
    holder_type = Column(Integer, nullable=False)
    resource_id = Column(Integer, nullable=False)
    resource_name = Column(String, nullable=False)
    resource_locator = Column(String, nullable=False)
    allow_method = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

    def __repr__(self):
        return '<admin auth: holder is {}, resource_name is {}, allow_method is {}>'.format(
            self.authorization_holder, self.resource_name, self.allow_method)


class ManagersAuthorization(Base):
    __tablename__ = 'managers_authorization'

    DISABLED = 0
    ENABLED = 1
    DELETE = 2

    id = Column(Integer, primary_key=True)
    authorization_holder = Column(Integer, nullable=False)
    holder_type = Column(Integer, nullable=False, default=0)
    resource_id = Column(Integer, nullable=False)
    resource_name = Column(String, nullable=False)
    resource_locator = Column(String, nullable=False)
    allow_method = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

    def __repr__(self):
        return '<manager auth: holder is {}, resource_name is {}, allow_method is {}>'.format(
            self.authorization_holder, self.resource_name, self.allow_method)


class ProjectsAuthorization(Base):
    __tablename__ = 'projects_authorization'

    DISABLED = 0
    ENABLED = 1
    DELETE = 2

    id = Column(Integer, primary_key=True)
    authorization_holder = Column(Integer, nullable=False)
    holder_type = Column(Integer, nullable=False, default=0)
    resource_id = Column(Integer, nullable=False)
    resource_name = Column(String, nullable=False, default="")
    resource_locator = Column(String, nullable=False, default="")
    allow_method = Column(Integer, nullable=False, default=15)
    status = Column(Integer, nullable=False, default=1)
    resource_amount = Column(Integer, nullable=False, default=1)
    effective_time = Column(Integer, nullable=False)
    expiration_time = Column(Integer, nullable=False)

    def __repr__(self):
        return '<project auth: holder is {}, resource_name is {}, allow_method is {}>'.format(
            self.authorization_holder, self.resource_name, self.allow_method)


class ManagersLogin(Base):

    __tablename__ = "managers_password"

    NEED_RESET = 0
    RESET = 1

    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False, default="")
    email = Column(String, nullable=False, default="")
    mobile = Column(Integer, nullable=False, default=0)
    password = Column(String, nullable=False)
    status = Column(Integer, nullable=False, default=NEED_RESET)


class AdministratorsLogin(Base):

    __tablename__ = "administrators_password"

    NEED_RESET = 0
    RESET = 1

    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False, default="")
    email = Column(String, nullable=False, default="")
    mobile = Column(Integer, nullable=False, default=0)
    password = Column(String, nullable=False)
    status = Column(Integer, nullable=False, default=NEED_RESET)
