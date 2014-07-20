""" Acquia Cloud API Exceptions. """


class AcquiaCloudException(Exception):

    """  Generic Acquia Cloud API Exception.

    All ACAPI exceptions should extend this class.
    """

    pass


class AcquiaCloudRestException(AcquiaCloudException):

    """A generic 400 or 500 level exception from the Acquia Cloud API.

    This class was lifted from twilio-python and hacked.
    """

    def __init__(self, status, uri, msg="", method='GET'):
        """ Constructor.

        Params
        ------
        status : int
            The HTTP status that was returned for the exception.
        uri : str
            The URI that caused the exception.
        msg : str
            A human-readable message for the error.
        method : str
            The HTTP method used to make the request
        """
        self.uri = uri
        self.status = status
        self.msg = msg
        self.method = method

    def __str__(self):
        """ Convert exception to string. """
        subs = (self.method, self.uri, self.status, self.msg)
        return ('%s %s resulted in HTTP %s error: "%s"' % subs)
