from bidong.common.utils import ObjectDict


class Resource(ObjectDict):
    DATA = 2
    FEATURE = 1

    def __init__(self, resource_public_name, resource_locator="", _id=None, **kwargs):
        super().__init__(**kwargs)
        self.id = _id
        self.name = resource_public_name
        self.locator = resource_locator


class Auth(ObjectDict):
    DISABLED = 0
    ENABLED = 1
    DELETE = 2

    def __init__(self, holder, allow_method=15, status=1, holder_type=0, _id=None, **kwargs):
        super().__init__(**kwargs)
        self.id = _id
        self.holder = holder
        self.holder_type = holder_type
        self.allow_method = allow_method
        self.status = status
        self.expiration_time = None
        self.effective_time = None
