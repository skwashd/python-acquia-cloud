"""Acquia API task queue resource."""

import logging
import re
import requests_cache
import time

from datetime import datetime
from datetime import timedelta

from acapi.exceptions import AcquiaCloudTaskFailedException
from acapi.resources.acquiaresource import AcquiaResource

LOGGER = logging.getLogger('acapi.resources.task')


class Task(AcquiaResource):
    """Task queue resource."""

    #: Task polling interval in seconds.
    POLL_INTERVAL = 3

    #: Valid task properties
    valid_keys = ['body', 'completed', 'cookie', 'created', 'description',
                  'hidden', 'id', 'percentage', 'queue', 'received',
                  'recipient', 'result', 'sender', 'started', 'state']

    def __init__(self, uri, auth, data=None, hack_uri=True):
        """Constructor.

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

        super(Task, self).__init__(uri, auth, data)

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
        """Check if a task is still pending.

        Returns
        -------
        bool
            Is the task still pending completion?
        """
        # Ensure we don't have stale data

        # Disable caching so we get the real response
        with requests_cache.disabled():
            task = self.request()

        self.data = task
        return task['completed'] is None

    def wait(self, timeout=1800):
        """Wait for a task to finish executing.

        Parameters
        ----------
        timeout : int
            The maximum number of seconds to wait for the task to complete.


        Returns
        -------
        Task
            Task object.
        """
        start = datetime.now()
        max_time = start + timedelta(seconds=timeout)

        while self.pending():
            # Ensure the timeout hasn't been exceeded.
            if start >= max_time:
                msg = 'Time out exceeded while waiting for {tid}' \
                      .format(tid=self.data['id'])
                raise AcquiaCloudTaskFailedException(msg, self.data)

            time.sleep(self.POLL_INTERVAL)

        # Grab the cached response
        task = self.get()
        if 'done' != task['state']:
            raise AcquiaCloudTaskFailedException('Task {task_id} failed'
                                                 .format(task_id=task['id']),
                                                 task)

        end = datetime.now()
        delta = end - start
        LOGGER.info("Waited %.2f seconds for task to complete",
                    delta.total_seconds())

        return self
