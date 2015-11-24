""" ACAPI base test class. """

import requests
import requests_mock
import unittest
import time

from .. import Client

@requests_mock.Mocker()
class BaseTest(unittest.TestCase):
    """ Base test class for ACAPI. """

    # ACAPI Client
    client = None

    def generate_task_dictionary(self, tid, state='done', completed=True):
        """ Generates a task dictionary. """

        known_states = ['done', 'error', 'received', 'waiting']

        now = int(time.time())

        completed_ts = None
        if completed:
            completed_ts = now

        # I want know about dodgy states in tests.
        if state not in known_states:
            state = None

        task = {
            "completed": completed_ts,
            "created": now,
            "description": "Copy files from dev to prod",
            "id": tid,
            "logs": "[02:20:58] [02:20:58] Started\n[02:21:00] [02:21:00] Failure\n",
            "queue": "files-migrate",
            "result": "",
            "sender": "cloud_api",
            "started": now,
            "state": state
        }

        return task

    def setUp(self):
        """
        Set up the tests with the mock requests handler.
        """

        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount('mock', adapter)

        self.client = Client('test', 'test', cache=None)

