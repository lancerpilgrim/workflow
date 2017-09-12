from bidong.common.utils import generate_random_number


class Operator:
    GET = "8"
    POST = "4"
    PUT = "2"
    DELETE = "1"


def method_int_convert(method_or_int):
    method_or_int = str(method_or_int)
    if method_or_int == Operator.GET:
        return "GET"
    elif method_or_int == Operator.DELETE:
        return "DELETE"
    elif method_or_int == Operator.POST:
        return "POST"
    elif method_or_int == Operator.PUT:
        return "PUT"
    elif method_or_int == "GET":
        return Operator.GET
    elif method_or_int == "POST":
        return Operator.POST
    elif method_or_int == "PUT":
        return Operator.PUT
    elif method_or_int == "DELETE":
        return Operator.DELETE
    else:
        return None


def ensure_method_as_int(methods):
    result = 0
    if isinstance(methods, str):
        return int(method_int_convert(methods))
    elif isinstance(methods, int):
        return methods
    for method in methods:
        result += int(method_int_convert(method))
    return result


def ensure_method_as_list(method):
    result = []
    if isinstance(method, str):
        method = method_int_convert(method)
    for each in [1, 2, 4, 8]:
        if each & method == each:
            result.append(method_int_convert(each))
    return result


def generate_id(max_retry=3, duplicate_checker=None, length=10):
    """
    :param length: 生成id长度
    :param max_retry: 最大重复生成次数,超过将抛出异常
    :param duplicate_checker: 查重方法,如果其返回结果为True, 将再生成一次. 
    :return: 
    """
    while max_retry > 0:
        while 1:
            _id = "1" + generate_random_number(length-1)
            if len(_id) == 10:
                break
        if duplicate_checker:
            if duplicate_checker(_id):
                max_retry -= 1
            else:
                return _id
        else:
            return _id
    raise Exception("_id Max Retries")