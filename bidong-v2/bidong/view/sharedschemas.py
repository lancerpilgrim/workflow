from marshmallow import Schema, fields


class TagSchema(Schema):
    name = fields.String(required=True, validate=lambda x: bool(x))
    id = fields.Integer(dump_only=True)
    tagged_count = fields.Integer(dump_only=True)
    tag_type = fields.String(
        required=True, load_only=True,
        validate=lambda x: x in ('account', 'ap'),
        description="标签类型, 选项[account, ap]"
    )


class TagListSchema(Schema):
    tags = fields.Nested(TagSchema, many=True)


if __name__ == "__main__":
    data = {
        "overviews": {
            "contact_number": 13333333333,
            "location": "nansha",
            "name": "test1",
            "status": 1,
            "email": "aa",
            "contact": "Lancer",
            "description": "test_project_1",
            "id": 1,
            "create_time": "2017-08-23 09:05:09"
        },
        "authorizations": {
            "url": "/projects/1/authorizations",
            "features": [
                {
                    "name": "project_management"
                },
                {
                    "name": "users_management"
                }
            ],
            "auth_ap_amount": 0,
            "id": 1
        },
        "id": 1,
        "message": "OK",
        "status_code": 200
    }