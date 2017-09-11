from datetime import datetime

from marshmallow import Schema, fields
from marshmallow import post_load

from bidong.core.exceptions import LogicError
from bidong.common.validator import check_mobile, check_mac_address


class DyncolSchema(Schema):
    id = fields.Integer(description="动态列id")
    label = fields.String(description="动态列标题")
    col = fields.String(description="动态列字段名")


class DyncolListSchema(Schema):
    default = fields.Nested(DyncolSchema, many=True, description="平台默认字段")
    setted = fields.Nested(DyncolSchema, many=True, description="项目已选自定义字段")


class DyncolIdListSchema(Schema):
    cols = fields.List(fields.Integer(), required=True)


class UserItemSchema(Schema):
    id = fields.Integer(description="用户ID")
    name = fields.String()
    mobile = fields.String()
    address = fields.String()
    tags = fields.String()
    online = fields.Integer(description="在线状态 1 - 在线, 0 - 离线")


class UserListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(UserItemSchema, many=True)


class AttrDictSchema(Schema):
    col = fields.Integer(required=True, validate=lambda x: x > 0,
                         description="用户自定义属性id")
    value = fields.String(required=True, description="属性值")


class UserSchema(Schema):
    name = fields.String(required=True, validate=lambda x: bool(x.strip()))
    mobile = fields.String(required=True, validate=check_mobile)
    attrs = fields.Nested(AttrDictSchema, many=True, required=True,
                          description="用户自定义属性")
    tags = fields.List(fields.Integer(), required=True, description="标签ID列表")


class UserAttrSchema(Schema):
    id = fields.Integer(description="自定义属性id")
    label = fields.String(description="字段标题")
    col = fields.String(description="字段名，图片类会以_image结尾")
    value = fields.String(description="字段值")


class UserTagSchema(Schema):
    id = fields.Integer(description="标签id")
    name = fields.String(description="标签名")


class UserDetailSchema(Schema):
    nickname = fields.String()
    mobile = fields.String()
    name = fields.String()
    attrs = fields.Nested(
        UserAttrSchema, many=True, description="用户自定义属性字典列表")
    tags = fields.Nested(
        UserTagSchema, many=True, description="用户标签列表"
    )


class VisitorUserSchema(Schema):
    userid = fields.Integer(description="用户ID")
    user = fields.String(description="手机号码或微信昵称")
    address = fields.String(description="当前位置")
    connect_at = fields.LocalDateTime(format="%Y-%m-%d %H:%M")
    auth_type = fields.Integer(
        description="认证方式, 0 - 账号, 1 - 手机号, 2 - 微信, 4 - App")
    traffic = fields.Integer()


class VisitorUserListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(VisitorUserSchema, many=True)


class AttachedTagSchema(Schema):
    users = fields.List(fields.Integer, description="用户id列表")
    tags = fields.List(fields.Integer, description="标签id列表")


class PackageItemSchema(Schema):
    id = fields.Integer(description="套餐ID")
    name = fields.String(description="套餐名")
    time_length = fields.String(description="时长数")
    price = fields.Decimal(description="金额")
    ends = fields.Integer(description="终端数")
    until = fields.LocalDateTime(format="%Y-%m-%d", description="套餐有效期")
    tags = fields.String(description="投放范围")
    amount = fields.Decimal(description="营收")
    created_at = fields.LocalDateTime(format="%Y-%m-%d", description="创建日期")


class PackageListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(PackageItemSchema, many=True)


class PackageSchema(Schema):
    name = fields.String(required=True, validate=lambda x: bool(x.strip()))
    time = fields.Integer(description="天数", validate=lambda x: x > 0)
    expired = fields.LocalDateTime(
        format="%Y-%m-%d", description="指定日期, 天数和指定日期二选其一")
    price = fields.Decimal(required=True, validate=lambda x: x > 0,
                           description="金额")
    ends = fields.Integer(description="终端", default=1)
    until = fields.LocalDateTime(format="%Y-%m-%d",
                                 description="套餐有效期, 日期格式YYYY-mm-dd")
    tags = fields.String(description="投放标签（仅在展示有）", dump_only=True)
    tag_list = fields.List(fields.Int,
                           description="标签ID列表(在展示是与tags一一对应)")

    @post_load
    def check_time_expired(self, data):
        time = data.get('time')
        expired = data.get('expired')
        if time is None and expired is None:
            raise LogicError(400, "天数和指定日期不能同时为空")
        if time:
            data['time'] *= 24
        if expired:
            if expired < datetime.now():
                raise LogicError(400, "指定日期不能早于当天")


class PackageUpdateSchema(Schema):
    until = fields.LocalDateTime(format="%Y-%m-%d", description="套餐过期时间")
    tag_list = fields.List(fields.Integer, description="标签ID列表")


class OrderItemScheam(Schema):
    mobile = fields.String()
    username = fields.String(description="姓名")
    pay_with = fields.String(description="支付方式")
    pay_from = fields.String(description="充值入口")
    package_name = fields.String(description="套餐")
    amount = fields.Decimal(description="金额")
    created_at = fields.LocalDateTime(format="%Y-%m-%d")


class OrderListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(OrderItemScheam, many=True)


class OrderChartSchema(Schema):
    title = fields.String(description="图表标题")
    dates = fields.List(fields.String, description="日期列表")
    amounts = fields.List(fields.Float, description="与日期对应数据")


class MessageItemSchema(Schema):
    id = fields.Integer(description="站内信ID")
    title = fields.String(description="标题")
    created_at = fields.LocalDateTime(format="%Y-%m-%d")
    status = fields.Integer(description="站内信状态, 0 - 未读, 1 - 已读")


class MessageListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(MessageItemSchema, many=True)


class MessageSchema(Schema):
    title = fields.String(description='标题')
    content = fields.String(description='内容')
    status = fields.Integer(
        description="站内信状态，0 - 未读，1 - 已读",
    )
    created_at = fields.LocalDateTime(format="%Y-%m-%d %H:%M")


class PortalItemSchema(Schema):
    id = fields.Integer(description="id")
    name = fields.String(description="portal名称")
    note = fields.String(description="备注")
    created_at = fields.LocalDateTime(format="%Y-%m-%d", description="创建日期")
    updated_at = fields.LocalDateTime(format="%Y-%m-%d", description="更新日期")
    is_platform = fields.Integer(default=0, description="是否为平台模版")


class PortalListSchema(Schema):
    objects = fields.Nested(PortalItemSchema, many=True)


class PortalSchema(Schema):
    name = fields.String(required=True, validate=lambda x: bool(x.strip()),
                         description="portal模版名")
    note = fields.String(description="备注")
    mobile_title = fields.String(
        required=True, validate=lambda x: bool(x.strip()),
        description="移动端文案内容")
    mobile_banner_url = fields.String(
        required=True, validate=lambda x: bool(x.strip()),
        description="移动端banner图片url")
    pc_title = fields.String(
        required=True, validate=lambda x: bool(x.strip()))
    pc_banner_url = fields.String(
        required=True, validate=lambda x: bool(x.strip()))


class WechatAccountSchema(Schema):
    id = fields.Integer(dump_only=True, description="公众号ID")
    name = fields.String(required=True, validate=lambda x: bool(x.strip()))
    appid = fields.String(required=True, validate=lambda x: bool(x.strip()))
    shopid = fields.String(required=True, validate=lambda x: bool(x.strip()))
    secret = fields.String(required=True, validate=lambda x: bool(x.strip()))
    note = fields.String(description="备注")
    created_at = fields.LocalDateTime(format="%Y-%m-%d", dump_only=True)


class WechatAccountListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(WechatAccountSchema, many=True)


class WechatAccountFieldsSchema(Schema):
    objects = fields.List(fields.Dict, description="选择字段字典列表")


class NetworkSchema(Schema):
    id = fields.Integer(dump_only=True, description="配置id，仅展示用")
    ssid = fields.String(required=True, validate=lambda x: bool(x.strip()),
                         description="ssid")
    is_public = fields.Integer(required=True, validate=lambda x: x in (0, 1),
                               description="网络类型，公有 - 1, 私有 - 0")
    is_free = fields.Integer(required=True, validate=lambda x: x in (0, 1),
                             description="计费方式，免费 - 1, 收费- 0")
    mask = fields.Integer(
        required=True,
        description="认证方式, 用前三位表示, 1(001)-手机, 2(010)微信, 4(100)APP"
    )
    portal_id = fields.Integer(required=True, description="portal页配置ID")
    duration = fields.Integer(required=True, description="免认证期限")
    session_timeout = fields.Integer(required=True, description="会话过期时间")
    wechat_account_id = fields.Integer(description="认证公众号ID")


class NetworkListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(NetworkSchema, many=True)


class APTagSchema(Schema):
    id = fields.Integer(description="标签id")
    name = fields.String(description="标签名")


class APSchema(Schema):
    name = fields.String(required=True, validate=lambda x: bool(x.strip()),
                         description="名称")
    mac = fields.String(required=True, validate=check_mac_address,
                        description="MAC地址")
    vendor = fields.String(required=True, description="品牌")
    address = fields.String(required=True, description="位置信息")
    tags = fields.List(fields.Integer(), required=True,
                       description="标签ID列表")


class APItemSchema(Schema):
    id = fields.Integer(description="AP id")
    name = fields.String()
    mac = fields.String()
    vendor = fields.String(description="品牌")
    online = fields.Integer(description="是否在线, 0 - 离线，1 - 在线")
    address = fields.String(description="位置")
    tags = fields.String(description="标签")
    conns = fields.Integer(description="在线人数")


class APListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(APItemSchema, many=True)
