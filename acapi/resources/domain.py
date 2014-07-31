""" Acquia Cloud API domain resource. """

import re
from .acquiaresource import AcquiaResource
from .task import Task


class Domain(AcquiaResource):

    """ Domain record associated with an environment. """

    def cache_purge(self):
        """Purge the varnish cache for the domain.

        Returns
        -------
        bool
            Was the cache cleared?
        """
        uri = '{}/cache'.format(self.uri)
        response = self.request(uri=uri, method='DELETE')
        return response.ok

    def delete(self):
        """Delete the domain record.

        Returns
        -------
        bool
            Was the domain record deleted?
        """
        response = self.request(method='DELETE')
        return response.ok

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
        p = re.compile('/envs/(.*)/domains/(.*)')
        m = p.search(self.uri)
        current_env = m.group(1)
        domain = m.group(2)

        move_uri = ('%s/%s' % (p.sub('/domain-move/\g<1>', self.uri), target))
        data = {'domains': [domain]}

        response = self.request(uri=move_uri, method='POST', data=data)
        task_data = response.content

        task = Task(self.uri, self.auth, data=task_data).wait()
        if None == task['completed']:
            raise Exception('Unable to move domian.')

        # Another hack, this time to get the URI for the domain.
        env_search = '/{}/'.format(current_env)
        env_target = '/{}/'.format(target)
        new_uri = self.uri.replace(env_search, env_target)
        return Domain(new_uri, self.auth)
