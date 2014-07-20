""" Acquia Cloud API user resource. """

from .acquiaresource import AcquiaResource
from ..util import acapi_request


class User(AcquiaResource):

    """ Acquia Cloud API user resource. """

    def drushrc(self):
        """ Fetch all the drush aliases for sites the user has access to.

        The json+PHP output of this isn't very useful in python.

        Returns
        -------
        dict
            Collection of PHP code snippets.
        """
        uri = '{}/drushrc'.format(self.uri)
        response = acapi_request('GET', uri, auth=self.auth)
        return response.content
