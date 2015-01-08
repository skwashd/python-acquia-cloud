""" Acquia API task queue resource. """

import re
import time

from .acquiaresource import AcquiaResource
from ..exceptions import AcquiaCloudTaskFailedException

class Task(AcquiaResource):

    """ Task queue resource. """

    """ Task polling interval """
    POLL_INTERVAL = 3

    def __init__(self, uri, auth, data=None, hack_uri=True):
        """ Constructor.

        Parameters
        ----------
        uri : str
            The base URI for the resource.
        auth : tuple
             The authentication credentials to use for the request.
        data : dict
            Raw data from ACAPI.
        hack_uri : bool
            Hack the URI so it is valid?
        """
        if hack_uri:
            uri = self.mangle_uri(uri, data)

        AcquiaResource.__init__(self, uri, auth, data)

    def mangle_uri(self, uri, task_data):
        """Generate a URI for a task based on JSON task object.

        FIXME This belongs on Task, not AcquiaData.

        Paramters
        ---------
        task_data : dict
            Raw task data from ACAPI.

        Returns
        -------
        Task
            Task object.
        """
        task_id = int(task_data['id'])

        p = re.compile('/sites/([a-z\:0-9]+)(/.*)?')
        task_uri = p.sub('/sites/\g<1>/tasks/{}'.format(task_id), uri)

        return task_uri

    def pending(self):
        """ Check if a task is still pending.

        Returns
        -------
        bool
            Is the task still pending completion?
        """
        # Ensure we don't have stale data
        self.data = None

        task = self.get()
        state = task['state'].encode('ascii', 'ignore')
        return state not in ['done', 'error']

    def wait(self):
        """Wait for a task to finish executing.

        Returns
        -------
        Task
            Task object.
        """
        while self.pending():
            # TODO Make this an property so users can override it.
            # This seems like a reasonable trade off between being polite and
            # hammering the API.
            time.sleep(self.POLL_INTERVAL)

        task = self.get()
        if 'done' != task['state']:
            raise AcquiaCloudTaskFailedException('Task {task_id} failed'.format(task_id=task['id']), task)

        return task
