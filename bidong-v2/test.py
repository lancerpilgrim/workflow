import random


def generate_random_id(l=9):
    strings = []
    for x in range(l):
        strings.append(str(random.randint(0, 10)))
    return "".join(strings)[:l]


def _generate_id(max_retry=3, duplicate_checker=None):
    while max_retry > 0:
        while 1:
            _id = "1" + generate_random_id(9)
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



from test2 import A


a = A()
print(_generate_id(duplicate_checker=a.checker))
