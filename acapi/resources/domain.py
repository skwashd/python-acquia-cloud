"""Acquia Cloud API domain resource. """

import re

from acapi.resources.acquiaresource import AcquiaResource


class Domain(AcquiaResource):
    """Domain record associated with an environment."""

    valid_keys = ['name']

    def cache_purge(self):
        """Purge the varnish cache for the domain.

        Returns
        -------
        bool
            Was the cache cleared?
        """
        uri = '{}/cache'.format(self.uri)
        data = self.request(uri=uri, method='DELETE')
        task = self.create_task(uri, data)
        task.wait()

        return True

    def delete(self):
        """Delete the domain record.

        Returns
        -------
        bool
            Was the domain record deleted?
        """
        data = self.request(method='DELETE')
        task = self.create_task(self.uri, data)
        task.wait()
        return True

    def move(self, target):
        """Move a domain from one environment to another.

        Parameters
        ----------
        target : str
            The name of the environment the domain is being moved to.

        Returns
        -------
        Domain
            The new domain object or None is the move fails.
        """
        # These regex hacks are needed because Acquia doesn't keep this
        # function with domains, which sucks.
        pattern = re.compile('/envs/(.*)/domains/(.*)')
        matches = pattern.search(self.uri)
        current_env = matches.group(1)
        domain = matches.group(2)

        move_uri = (
            '%s/%s' % (pattern.sub(r'/domain-move/\g<1>', self.uri), target))
        data = {'domains': [domain]}

        task_data = self.request(uri=move_uri, method='POST', data=data)
        task = self.create_task(move_uri, task_data)
        task.wait()

        # Another hack, this time to get the URI for the domain.
        env_search = '/{}/'.format(current_env)
        env_target = '/{}/'.format(target)
        new_uri = self.uri.replace(env_search, env_target)
        return Domain(new_uri, self.auth)
