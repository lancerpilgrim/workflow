from marshmallow import Schema, fields


class CollectionBaseSchema(Schema):
    page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    total_items = fields.Integer(required=True)


class IndividualBaseSchema(Schema):
    pass