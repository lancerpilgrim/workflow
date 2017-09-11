from marshmallow import fields
from bidong.view.schemas import IndividualBaseSchema


class LoginInputSchema(IndividualBaseSchema):
    identifier = fields.String(required=True)
    password = fields.String(required=True)


class LoginUpdateSchema(IndividualBaseSchema):
    identifier = fields.String(required=True)
    previous_password = fields.String(required=True)
    new_password = fields.String(required=True)