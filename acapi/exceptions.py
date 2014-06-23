class AcquiaCloudException(Exception):
    pass

class AcquiaCloudRestException(AcquiaCloudException):
    """ A generic 400 or 500 level exception from the Acquia Cloud API

    This class was lifted from twilio-python and hacked.

    :param int status: the HTTP status that was returned for the exception
    :param str uri: The URI that caused the exception
    :param str msg: A human-readable message for the error
    :param str method: The HTTP method used to make the request
    """

    def __init__(self, status, uri, msg="", method='GET'):
        self.uri = uri
        self.status = status
        self.msg = msg
        self.method = method

    def __str__(self):
        subs = (self.method, self.uri, self.status, self.msg)
        return ('%s %s resulted in HTTP %s error: "%s"' % subs)



