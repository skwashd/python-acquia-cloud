"""Acquia Cloud API user resource."""

from acapi.resources.acquiaresource import AcquiaResource


class User(AcquiaResource):
    """Acquia Cloud API user resource."""

    #: Valid keys for a user.
    valid_keys = ['authenticated_as']

    def drushrc(self):
        """Fetch all the drush aliases for sites the user has access to.

        The json+PHP output of this isn't very useful in python.

        Returns
        -------
        dict
            Collection of PHP code snippets.
        """
        uri = '{}/drushrc'.format(self.uri)
        response = self.request(uri=uri)
        return response
