from . import *


class InvalidUsage(Exception):
    status_code = STATUS_BAD_REQUEST

    def __init__(self, message, status_code=None, payload=None, reason=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.reason = reason

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['return_code'] = self.status_code
        rv['message'] = self.message
        rv['reason'] = self.reason
        return rv


class ConflictException(InvalidUsage):
    # Indicates that the request could not be processed because of conflict in the request
    def __init__(self, message, status_code=STATUS_CONFLICT, payload=None, reason=None):
        InvalidUsage.__init__(self, 'Conflict Request: ' + message, status_code, payload, reason)


class NoContentException(InvalidUsage):
    # The server successfully processed the request, but is not returning any content.
    def __init__(self, message, status_code=STATUS_NO_CONTENT, payload=None, reason=None):
        InvalidUsage.__init__(self, 'Not Found Record: ' + message, status_code, payload, reason)


class BadRequestException(InvalidUsage):
    # The request could not be understood by the server due to malformed syntax.
    def __init__(self, message, status_code=STATUS_BAD_REQUEST, payload=None, reason=None):
        InvalidUsage.__init__(self, 'Bad Request: ' + message, status_code, payload, reason)


class NotAcceptableException(InvalidUsage):
    # The request could not be understood by the server due to malformed syntax.
    def __init__(self, message, status_code=STATUS_NOT_ACCEPTABLE, payload=None, reason=None):
        InvalidUsage.__init__(self, 'Not Acceptable: ' + message, status_code, payload, reason)


class PreconditionRequiredException(InvalidUsage):
    def __init__(self, message, status_code=STATUS_PRECONDITION_REQUIRED, payload=None, reason=None):
        InvalidUsage.__init__(self, 'Precondition Required: ' + message, status_code, payload, reason)


class UnauthorizedException(InvalidUsage):
    # The request could not be understood by the server due to malformed syntax.
    def __init__(self, message, status_code=STATUS_UNAUTHORIZED, payload=None, reason=None):
        InvalidUsage.__init__(self, 'Unauthorized: ' + message, status_code, payload, reason)


class InternalServerErrorException(InvalidUsage):
    # A generic error message, given when an unexpected condition was encountered and no more specific message is suitable.
    def __init__(self, message, status_code=STATUS_INTERNAL_SERVER_ERROR, payload=None, reason=None):
        InvalidUsage.__init__(self, 'Internal Server Error: ' + message, status_code, payload, reason)
