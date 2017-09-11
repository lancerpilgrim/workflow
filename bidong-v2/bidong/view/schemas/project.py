from marshmallow import fields, post_dump

from bidong.view.schemas import CollectionBaseSchema, IndividualBaseSchema
from settings import version


class ProjectOverviewsSchema(IndividualBaseSchema):
    id = fields.Integer()
    name = fields.String(description="项目名称")
    description = fields.String(required=True, description="项目简介")
    status = fields.Integer()
    contact = fields.String(description="", required=True)
    contact_number = fields.Integer(description="", required=True)
    email = fields.String(description="")
    create_time = fields.Integer()
    location = fields.String(required=True)
    auth_ap_amount = fields.Integer()
    expiration_time = fields.Integer()
    url = fields.String()

    @post_dump()
    def add_url(self, item):
        item["url"] = "/{version}/projects/{project_id}/overviews".format(
            version=version,
            project_id=item["id"]
        )
        return item


class ProjectOverviewsInputSchema(IndividualBaseSchema):
    name = fields.String(description="项目名称")
    description = fields.String(required=True, description="项目简介")
    status = fields.Integer()
    contact = fields.String(description="", required=True)
    contact_number = fields.Integer(description="", required=True)
    email = fields.String(description="")
    location = fields.String(required=True)
    auth_ap_amount = fields.Integer(required=True)
    expiration_time = fields.Integer(default=0)


class AuthorizationFeatureSchema(IndividualBaseSchema):
    name = fields.String(required=True)
    allow_method = fields.List(fields.String())
    description = fields.String()


class ProjectAuthorizationSchema(IndividualBaseSchema):
    id = fields.Integer()
    features = fields.List(fields.Nested(AuthorizationFeatureSchema))
    url = fields.String()

    @post_dump()
    def add_url(self, item):
        item["url"] = "/{version}/projects/{project_id}/authorizations".format(
            version=version,
            project_id=item["id"]
        )
        return item


class ProjectInputSchema(IndividualBaseSchema):
    id = fields.Integer()
    overviews = fields.Nested(ProjectOverviewsSchema, exclude=("create_time", "id", "url"))
    authorizations = fields.Nested(ProjectAuthorizationSchema, exclude=("id", "url"))


class ProjectOutputSchema(IndividualBaseSchema):
    id = fields.Integer(required=True)
    overviews = fields.Nested(ProjectOverviewsSchema)
    authorizations = fields.Nested(ProjectAuthorizationSchema)
    url = fields.String()

    @post_dump()
    def add_url(self, item):
        item["url"] = "/{version}/projects/{project_id}".format(
            version=version,
            project_id=item["id"]
        )
        return item


class ProjectsOutputSchema(CollectionBaseSchema):
    objects = fields.List(fields.Nested(ProjectOutputSchema))