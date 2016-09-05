"""Acquia Cloud API Exceptions."""

from pprint import pformat


class AcquiaCloudException(Exception):
    """Generic Acquia Cloud API Exception.

    All ACAPI exceptions should extend this class.
    """

    pass


class AcquiaCloudNoDataException(AcquiaCloudException):
    """No data found exception."""

    pass


class AcquiaCloudTaskFailedException(AcquiaCloudException):
    """An Acquia task failure exception."""

    def __init__(self, message, task):
        """Constructor.

        Parameters
        ----------
        message: str
            The error message.
        task: Task
            The Task object for the task that failed.
        """
        super(AcquiaCloudTaskFailedException, self).__init__(message)
        self.message = message
        self.task = task

    def __str__(self):
        """Return the string representation of the exception.

        Returns
        -------
        str
            The error message and pretty printed Task object properties.
        """
        task = pformat(self.task, indent=4)
        return "{msg}\n{task}".format(msg=self.message, task=task)
