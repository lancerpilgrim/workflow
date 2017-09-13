import time
from marshmallow import Schema, fields, post_dump
from datetime import datetime
from marshmallow import post_load, post_dump

from bidong.view.schemas import CollectionBaseSchema, IndividualBaseSchema
from bidong.view.schemas.project import AuthorizationFeatureSchema, ProjectOverviewsSchema
from settings import version


class AdministratorOverviewsOutputSchema(IndividualBaseSchema):
    id = fields.Integer()
    name = fields.String()
    mobile = fields.Integer()
    create_time = fields.Integer()
    description = fields.String()
    status = fields.Integer()
    url = fields.String()

    @post_dump()
    def add_url(self, item):
        item["url"] = "/{version}/administrators/{id}/overviews".format(
            version=version,
            id=item["id"]
        )
        return item

    # 系统内部统一使用时间戳，不再处理格式问题
    # @post_dump()
    # def format_time(self, item):
    #     if str(item["create_time"]).isdigit():
    #         item["create_time"] = time.strftime("%Y-%m-%d", time.localtime(int(item["create_time"])))
    #     return item


class AdministratorsOverviewsOutputSchema(CollectionBaseSchema):
    objects = fields.List(fields.Nested(AdministratorOverviewsOutputSchema))


class ManagerOverviewsOutputSchema(IndividualBaseSchema):
    id = fields.Integer()
    name = fields.String()
    mobile = fields.Integer()
    create_time = fields.Integer()
    description = fields.String()
    status = fields.Integer()
    url = fields.String()

    @post_dump()
    def add_url(self, item):
        item["url"] = "/{version}/managers/{id}/overviews".format(
            version=version,
            id=item["id"]
        )
        return item

    # @post_dump()
    # def format_time(self, item):
    #     if str(item["create_time"]).isdigit():
    #         item["create_time"] = time.strftime("%Y-%m-%d", time.localtime(int(item["create_time"])))
    #     return item


class ManagersOverviewsOutputSchema(CollectionBaseSchema):
    objects = fields.List(fields.Nested(ManagerOverviewsOutputSchema))


class AdministratorOverviewsInputSchema(IndividualBaseSchema):
    id = fields.Integer()
    name = fields.String()
    mobile = fields.Integer()
    create_time = fields.Integer()
    description = fields.String()
    status = fields.Integer()


class ManagerOverviewsInputSchema(IndividualBaseSchema):
    id = fields.Integer()
    name = fields.String()
    mobile = fields.Integer()
    description = fields.String()
    status = fields.Integer()


class AdministratorAuthorizationSchema(AuthorizationFeatureSchema):
    pass
    # features = fields.List(fields.Nested(AuthorizationFeatureSchema))


class AdministratorDataAuthorizationSchema(AuthorizationFeatureSchema):
    data_id = fields.Integer()


class ManagerAuthorizationSchema(IndividualBaseSchema):
    project_id = fields.Integer()
    project_name = fields.String()
    features = fields.List(fields.Nested(AuthorizationFeatureSchema))


class AdministratorAuthorizationsOutputSchema(IndividualBaseSchema):
    id = fields.Integer()
    features = fields.List(fields.Nested(AdministratorAuthorizationSchema))
    data = fields.List(fields.Nested(AdministratorDataAuthorizationSchema))
    url = fields.String()

    @post_dump()
    def add_url(self, item):
        item["url"] = "/{version}/administrators/{id}/authorizations".format(
            version=version,
            id=item["id"]
        )
        return item


class ManagerAuthorizationsOutputSchema(IndividualBaseSchema):
    id = fields.Integer()
    contents = fields.List(fields.Nested(ManagerAuthorizationSchema))
    url = fields.String()

    @post_dump()
    def add_url(self, item):
        item["url"] = "/{version}/managers/{id}/authorizations".format(
            version=version,
            id=item["id"]
        )
        return item


class AdministratorAuthorizationsInputSchema(AdministratorAuthorizationsOutputSchema):
    # id = fields.Integer()
    # contents = fields.List(fields.Nested(AdministratorAuthorizationsOutputSchema))
    pass



class ManagerAuthorizationsInputSchema(IndividualBaseSchema):
    id = fields.Integer()
    contents = fields.List(fields.Nested(ManagerAuthorizationSchema))


class AdministratorInputSchema(IndividualBaseSchema):
    id = fields.Integer()
    overviews = fields.Nested(AdministratorOverviewsOutputSchema, exclude=("create_time", "id", "url"))
    authorizations = fields.Nested(AdministratorAuthorizationsOutputSchema, exclude=("id", "url"))


class ManagerInputSchema(IndividualBaseSchema):
    id = fields.Integer()
    overviews = fields.Nested(ManagerOverviewsOutputSchema, exclude=("create_time", "id", "url"))
    authorizations = fields.Nested(ManagerAuthorizationsOutputSchema, exclude=("id", "url"))


class AdministratorOutputSchema(IndividualBaseSchema):
    id = fields.Integer()
    overviews = fields.Nested(AdministratorOverviewsOutputSchema)
    authorizations = fields.Nested(AdministratorAuthorizationsOutputSchema)

    @post_dump()
    def add_url(self, item):
        item["url"] = "/{version}/administrators/{id}".format(
            version=version,
            id=item["id"]
        )
        return item


class ManagerOutputSchema(IndividualBaseSchema):
    id = fields.Integer()
    overviews = fields.Nested(ManagerOverviewsOutputSchema)
    authorizations = fields.Nested(ManagerAuthorizationsOutputSchema)

    @post_dump()
    def add_url(self, item):
        item["url"] = "/{version}/managers/{id}".format(
            version=version,
            id=item["id"]
        )
        return item


class AdministratorsOutputSchema(CollectionBaseSchema):
    objects = fields.List(fields.Nested(AdministratorOutputSchema))


class ManagersOutputSchema(CollectionBaseSchema):
    objects = fields.List(fields.Nested(ManagerOutputSchema))


class ManagerProjectOutputSchema(IndividualBaseSchema):
    projects = fields.List(fields.Nested(ProjectOverviewsSchema, exclude=("status", )))