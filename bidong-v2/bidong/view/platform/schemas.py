from datetime import datetime

from marshmallow import Schema, fields
from marshmallow import post_load, post_dump
from bidong.common.utils import get_bit
from bidong.common.validator import check_ip_address


class LetterListItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(dump_only=True)
    created_at = fields.LocalDateTime(format="%Y-%m-%d")


class LetterListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(LetterListItemSchema, many=True)


class LetterSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=lambda x: bool(x))
    content = fields.String(required=True, validate=lambda x: bool(x))
    status = fields.Integer(
        required=True, validate=lambda x: x in (0, 1),
        description="站内信类型，0 - 草稿, 1 - 发布",
        load_only=True
    )
    created_at = fields.LocalDateTime(dump_only=True, format="%Y-%m-%d %H:%M")


class UserItemSchema(Schema):
    id = fields.Integer(description="用户ID")
    name = fields.String()
    mobile = fields.String()
    address = fields.String(description="当前位置")
    tags = fields.String()
    belong = fields.String(description="所属项目")
    online = fields.Integer(description="在线状态 1 - 在线, 0 - 离线")


class UserListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(UserItemSchema, many=True)


class UserTagSchema(Schema):
    id = fields.Integer(description="标签id")
    name = fields.String(description="标签名")


class UserTagListSchema(Schema):
    tags = fields.List(fields.Integer, description="标签id列表")


class UserDetailSchema(Schema):
    nickname = fields.String(description="昵称", dump_only=True)
    mobile = fields.String(dump_only=True)
    name = fields.String(dump_only=True)
    tags = fields.Nested(
        UserTagSchema, many=True, description="用户标签列表"
    )


class ProfileAttrSchema(Schema):
    col = fields.String(description="字段名称")
    label = fields.String(description="字段展示标签")
    value = fields.String(description="字段值")


class UserProfileSchema(Schema):
    project = fields.String(description="项目名称")
    tags = fields.String(description="项目标签")
    attrs = fields.Nested(ProfileAttrSchema, many=True)


class ProfilesSchema(Schema):
    objects = fields.Nested(UserProfileSchema, many=True)


class AttachedTagSchema(Schema):
    accounts = fields.List(fields.Integer, description="用户ID列表")
    tags = fields.List(fields.Integer, description="平台标签列表")


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
    name = fields.String(required=True, validate=lambda x: bool(x))
    time = fields.Integer(required=True, description="天数",
                          validate=lambda x: x > 0)
    mask = fields.Integer(required=True, description="时长单位, 0 - 天, 1 - 小时",
                          validate=lambda x: x in (0, 1))
    price = fields.Decimal(required=True, description="金额")
    ends = fields.Integer(description="终端", default=1)
    until = fields.LocalDateTime(format="%Y-%m-%d", description="套餐有效期")
    tags = fields.String(description="投放标签（仅在展示有）", dump_only=True)
    projects = fields.String(description="投放项目（仅在展示有）", dump_only=True)
    tag_list = fields.List(fields.Integer, description="标签ID列表(展示时以tag一一对应)")
    project_list = fields.List(fields.Integer,
                               description="项目ID列表（展示时与project一一对应)")

    @post_load
    def united_time(self, data):
        """
        统一将日期转换成小时
        """
        mask = data['mask']
        if not mask:
            data['time'] = data['time'] * 24

    @post_dump
    def hour2day(self, data):
        mask = data['mask']
        if not get_bit(mask, 0):
            data['time'] = (data['time'] // 24)


class PackageUpdateSchema(Schema):
    until = fields.LocalDateTime(format="%Y-%m-%d", description="套餐过期时间")
    tag_list = fields.List(fields.Integer, description="标签ID列表")
    project_list = fields.List(fields.Integer, description="投放项目列表")


class OrderItemSchema(Schema):
    pn = fields.Integer(description="订单所属项目ID, 0为平台订单")
    mobile = fields.String()
    username = fields.String(description="姓名")
    pay_with = fields.String(description="支付方式")
    pay_from = fields.String(description="充值入口")
    package_name = fields.String(description="套餐")
    amount = fields.Decimal(description="金额")
    created_at = fields.LocalDateTime(format="%Y-%m-%d")


class PortalItemSchema(Schema):
    id = fields.Integer(description="id")
    name = fields.String(description="portal名称")
    note = fields.String(description="备注")
    created_at = fields.LocalDateTime(format="%Y-%m-%d", description="创建日期")
    updated_at = fields.LocalDateTime(format="%Y-%m-%d", description="更新日期")
    on_using = fields.Integer(description="是否默认使用中")


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


class OrderListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(OrderItemSchema, many=True)


class OrderChartSchema(Schema):
    title = fields.String(description="图表标题")
    dates = fields.List(fields.String, description="日期列表")
    amounts = fields.List(fields.Float, description="与日期对应数据")


class CouponSchema(Schema):
    hours = fields.Integer(
        required=True, validate=lambda x: x > 0, description="时长")
    count = fields.Integer(
        required=True, validate=lambda x: 0 < x <= 200, description="兑换码数量")
    expired = fields.LocalDateTime(required=True, format="%Y-%m-%d",
                                   description="过期时间")


class CouponItemSchema(Schema):
    code = fields.String(description="兑换码")
    hours = fields.Integer(description="时长")
    expired = fields.LocalDateTime(format="%Y-%m-%d", description="有效期")
    created_at = fields.LocalDateTime(format="%Y-%m-%d", description="创建时间")
    status = fields.Method(
        'get_status', description="状态，0 - 待兑换, 1 - 已兑换, 2 - 过期未兑换")

    def get_status(self, data):
        if data.is_used:
            return 1
        elif data.expired.date() <= datetime.now().date():
            return 0
        else:
            return 2


class CouponListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(CouponItemSchema, many=True)


class SerialCouponItemSchema(Schema):
    code = fields.String(description="兑换码")
    hours = fields.Integer(description="时长")
    expired = fields.LocalDateTime(format="%Y-%m-%d")


class SerialCouponListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(SerialCouponItemSchema, many=True)


class CouponDataSchema(Schema):
    created_by = fields.Integer(description="管理员ID")
    usable = fields.Integer(description="待兑换")
    used = fields.Integer(description="已兑换")
    expired = fields.Integer(description="已过期")
    total = fields.Integer(description="总时长")


class CouponDataListSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)
    objects = fields.Nested(CouponDataSchema, many=True)


class ACSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=lambda x: bool(x.strip()))
    ip = fields.String(required=True, validate=check_ip_address)
    vendor = fields.String(required=True,
                           validate=lambda x: bool(x.strip()),
                           description="品牌")
    secret = fields.String(required=True)


class ACListSchema(Schema):
    objects = fields.Nested(ACSchema, many=True)
