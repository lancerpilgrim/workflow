from bidong.core.response import Context
from bidong.core.response import CONFLICT, NOT_FOUND, BAD_REQUEST
from bidong.core.response import UNAUTHORIZED, FORBIDDEN


class Error(Exception):
    pass


class DuplicateError(Error, Context):
    def __init__(self, message):
        Exception.__init__(self, message)
        Context.__init__(self, CONFLICT, message)


class NotFoundError(Error, Context):
    def __init__(self, message):
        Exception.__init__(self, message)
        Context.__init__(self, NOT_FOUND, message)


class LogicError(Error, Context):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        Context.__init__(self, code, message)


class APIException(Error, Context):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self)
        Context.__init__(self, *args, **kwargs)


class LoginError(Error, Context):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self)
        Context.__init__(self, *args, **kwargs)


class NeedLoginException(LoginError):
    def __init__(self, *args, **kwargs):
        super(NeedLoginException, self).__init__(*args, **kwargs)


class SignatureExpiredError(LoginError):

    def __init__(self, *args, **kwargs):
        super(SignatureExpiredError, self).__init__(*args, **kwargs)


class InvalidParametersError(Error, Context):
    def __init__(self, message):
        Exception.__init__(self, message)
        Context.__init__(self, BAD_REQUEST, message)


class UnAuthorizedError(Error, Context):
    def __init__(self, message):
        Exception.__init__(self, message)
        Context.__init__(self, UNAUTHORIZED, message)


class NoPermissionError(Error, Context):
    def __init__(self, message):
        Exception.__init__(self, message)
        Context.__init__(self, FORBIDDEN, message)
