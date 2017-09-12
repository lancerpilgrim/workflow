from bidong.common.utils import ObjectDict, get_dict_attribute
from bidong.core.exceptions import InvalidParametersError


def get_downsized_collection(collection, fields):
    result = []
    for item in collection:
        downsized_item = ObjectDict()
        for field in fields.split(","):
            try:
                key, value = get_dict_attribute(item, field)
                downsized_item[key] = value
            except Exception:
                raise InvalidParametersError(message="`fields`參數有誤")
            else:
                result.append(downsized_item)
    return result


def get_downsized_dict(item, fields):
    downsized_item = ObjectDict()
    for field in fields.split(","):
        try:
            key, value = get_dict_attribute(item, field)
            downsized_item[key] = value
        except Exception:
            raise InvalidParametersError(message="`fields`參數有誤")
    return downsized_item

