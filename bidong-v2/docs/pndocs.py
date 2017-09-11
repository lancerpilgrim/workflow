import inspect
from importlib import import_module

from apispec import APISpec

from bidong.router.project import routers


tags = [
    {"name": "project", "description": "项目管理"},
    {"name": "user", "description": "用户管理"},
    {"name": "tag", "description": "标签管理"},
    {"name": "excel", "description": "报表"},
    {"name": "billing", "description": "计费管理"},
    {"name": "operations", "description": "运营管理"},
    {"name": "message", "description": "站内信"},
    {"name": "tool", "description": "工具"},
]

pnspec = APISpec(
    title="壁咚项目管理后台API",
    version="1.0.0",
    basePath="/v1.0",
    info=dict(
        description="壁咚项目管理后台API"
    ),
    tags=tags,
    plugins=[
        "apispec.ext.tornado",
        "apispec.ext.marshmallow"
    ]
)

# define schema
pnspec.definition("ErrorMsg", properties={
    "field": {"type": "string", "description": "字段出错信息"}
})
pnspec.definition("Error", properties={
    "field": {"type": "array", "$ref": "#definitions/ErrorMsg"}
})
pnspec.definition("Api400Error", properties={
    "status_code": {"type": "integer", "description": "状态码, 参见HTTP常见状态码"},
    "message": {"type": "string", "description": "出错信息"},
    "errors": {"type": "array", "$ref": "#definitions/Error",
               "description": "字段出错信息，仅在HTTP状态码为400有这个字段"}
})
pnspec.definition("ApiError", properties={
    "status_code": {"type": "integer", "description": "状态码, 参见HTTP常见状态码"},
    "message": {"type": "string", "description": "出错信息"}
})
pnspec.definition("ApiSuccess", properties={
    "status_code": {"type": "integer", "default": 200},
    "message": {"type": "string", "default": "OK"}
})


def load_schemas(path):
    """从指定Python module初始化shcemas
    """
    module = import_module(path)
    for name, _object in inspect.getmembers(module):
        if inspect.isclass(_object) and name.endswith('Schema'):
            name = name.replace('Schema', '')
            if name:
                pnspec.definition(name, schema=_object)

# load schemas
load_schemas('bidong.view.sharedschemas')
load_schemas('bidong.view.project.schemas')

# url-spec settings
for r in routers:
    try:
        url = r[0].replace('/v1.0', ''), r[1]
        pnspec.add_path(urlspec=url)
    except Exception as err:
        print(err)
