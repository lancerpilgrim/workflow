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