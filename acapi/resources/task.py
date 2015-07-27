""" Acquia API task queue resource. """

from datetime import datetime
import logging
import re
import requests_cache
import time

from .acquiaresource import AcquiaResource
from ..exceptions import AcquiaCloudTaskFailedException

LOGGER = logging.getLogger('acapi.resources.task')

class Task(AcquiaResource):

    """ Task queue resource. """

    #: Task polling interval in seconds.
    POLL_INTERVAL = 3

    #: Valid task properties
    valid_keys = ['body', 'completed', 'cookie', 'created', 'description', 'hidden',
                  'id', 'percentage', 'queue', 'received', 'recipient', 'result',
                  'sender', 'started', 'state']

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

        self.loops = 0

        AcquiaResource.__init__(self, uri, auth, data)

    def mangle_uri(self, uri, task_data):
        """Generate a URI for a task based on JSON task object.

        Parameters
        ----------
        task_data : dict
            Raw task data from ACAPI.

        Returns
        -------
        Task
            Task object.
        """
        task_id = int(task_data['id'])

        pattern = re.compile(r'/sites/([a-z\:0-9]+)(/.*)?')
        task_uri = pattern.sub(r'/sites/\g<1>/tasks/{}'.format(task_id), uri)

        return task_uri

    def pending(self):
        """ Check if a task is still pending.

        Returns
        -------
        bool
            Is the task still pending completion?
        """
        # Ensure we don't have stale data
        
        # Disable caching so we get the real response
        with requests_cache.disabled():
            task = self.request()
        state = task['state'].encode('ascii', 'ignore')
        self.data = task
        return state not in ['done', 'error']

    def wait(self):
        """Wait for a task to finish executing.

        Returns
        -------
        Task
            Task object.
        """
        # We wait a maximum of 30mins
        max_loops = (60 * 30 / self.POLL_INTERVAL)
        start = datetime.now()

        while self.pending():
            if self.loops >= max_loops:
                break

            self.loops += 1
            time.sleep(self.POLL_INTERVAL)

        # Grab the cached response
        task = self.get()
        if 'done' != task['state'] or None == task['completed']:
            raise AcquiaCloudTaskFailedException('Task {task_id} failed'
                                                 .format(task_id=task['id']), task)

        end = datetime.now()
        delta = end - start
        LOGGER.info("Waited %.2f seconds for task to complete", delta.total_seconds())

        return self
