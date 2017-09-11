from bidong.core import response
from bidong.core.exceptions import APIException
from bidong.common.utils import ObjectDict


def is_valid(schema, context):
    """校验web请求参数
    Args:
        schema: marhsmallow schema class
        context: request params dict
    Return:
        bool, True or raise APIException
    Raise:
        APIException
    """
    errors = schema().validate(context)
    if errors:
        raise APIException(payload={"errors": errors},
                           status_code=response.BAD_REQUEST)
    return True


def validate_with_schema(schema, context):
    """校验web请求参数并返回清洗后的数据
    Args:
        schema: marshmallow schema class
        context: request params dict
    Return:
        dict, clean data
    Raise:
        APIException
    """
    data, errors = schema().load(context)
    if errors:
        raise APIException(payload={"errors": errors},
                           status_code=response.BAD_REQUEST)
    return ObjectDict(data)
