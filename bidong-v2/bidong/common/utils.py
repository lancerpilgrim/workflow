import json
import time
import uuid
import decimal
import logging
import datetime
from functools import wraps
import random

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class SmartJSONEncoder(json.JSONEncoder):
    '''
        serial datetime date
    '''

    def default(self, obj):
        '''
            serialize datetime & date & decimal.Deciaml
        '''
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime(DATE_FORMAT)
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            raise TypeError("Object of type '%s' is not JSON serializable" %
                            obj.__class__.__name__)


json_encoder = SmartJSONEncoder(indent=4).encode
json_decoder = json.JSONDecoder().decode


def extract_param(d):
    """
    To extract logger format for a param dict
    :param d: dict
    :return:  str
    >>> extract_param({"a": 1})
    '[a=1]'
    """
    param_list = list()
    for k, v in d.items():
        param_list.append("[{0}={1}]".format(k, v))
    return " ".join(param_list)


class ObjectDict(dict):
    """
    make dict behaves like object, if key missing, return None
    >>> o = ObjectDict({"a": 1})
    >>> o.a
    >>> 1
    >>> o.b
    """

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


def dictize(item, exclude_attrs=None):
    """
    serialize object to dict, use it to dictize sqlalchemy query result,
    if item is None, then return empty dict
    Args:
        item: object
        exclude_attrs: list, attrs not include in return dict
    Returns:
        dict
    """
    if item is None:
        return {}

    excludes = set(exclude_attrs) if exclude_attrs else set()
    rvs = {}
    for attr, value in item.__dict__.items():
        if attr.startswith("_") or attr.startswith("__"):
            continue
        if attr in excludes:
            continue
        rvs[attr] = value

    return rvs


def shortuuid():
    return str(uuid.uuid4())[:8]


def ensure_bytes(value, encoding='utf-8'):
    if isinstance(value, bytes):
        return value
    elif isinstance(value, str):
        return value.encode(encoding)
    return str(value).encode(encoding)


def ensure_unicode(value, encoding='utf-8'):
    if isinstance(value, bytes):
        return value.decode(encoding)
    return str(value)


def set_bit(v, index, bit):
    """set  integer x the index bit to 0 or 1
    Args:
        v: integer
        index: the N bit
        bit: 0 or 1
    """
    mask = 1 << index
    v &= ~mask
    if bit:
        v |= mask
    return v


def get_bit(v, index):
    """ check integer v the index bit 0 or 1
    """
    mask = v & (1 << index)
    return 1 if mask else 0


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        interval = time.time() - start
        logging.info("Interval: %r (%r, %r) ==> %2.2f sec" % (
            func.__name__, args, kwargs, interval
        ))
        return result

    return wrapper


def generate_random_number(l=9):
    strings = []
    for x in range(l):
        strings.append(str(random.randint(0, 10)))
    return "".join(strings)[:l]


class ObjectContainer:
    pass


def get_dict_attribute(resource_dict, attr):
    """
    :brief: 根據attr獲取字典resource_dict的value，attr是帶有層次結構的key
            舉例而言如果resource_dict = {"key1": {"key2": value2}, "key3": value3}, 
            如果attr="key3", 則返回("key3", value3), 
            如果attr="key1.key2", 則返回("key1.key2", value2),
            如果attr="key2", 拋出KeyError異常
    :param resource_dict: 源字典 
    :param attr: 形如'key1.key2'的帶有層次結構的key值 
    :return: (attr, value)
    """

    class G(object):

        def __init__(self, _resource_dict, _attribute_hierarchy):
            self.__dict = _resource_dict
            self.__index = 0
            self.__attr = _attribute_hierarchy

        def __next__(self):
            res = self.__dict[self.__attr[self.__index]]
            self.__dict = res
            self.__index += 1
            return res

        def __iter__(self):
            return self

    attr_hierarchy = attr.split(".")
    _item = G(resource_dict, attr_hierarchy)
    value = None
    for j in range(len(attr_hierarchy)):
        value = next(_item)
    return attr_hierarchy[-1], value
