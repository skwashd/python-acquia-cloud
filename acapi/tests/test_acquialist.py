""" Tests the Acquia list class. """
import requests_mock

from . import BaseTest
from ..resources import AcquiaList, DatabaseList
from ..exceptions import AcquiaCloudNoDataException

@requests_mock.Mocker()
class TestAcquiaList(BaseTest):
    """Tests the Acquia Cloud API db list class."""

    alist = None

    def setUp(self):
        """ Fetches an empty acquia list derived object. """

        self.alist = AcquiaList(None, False, {})

    def test_delitem(self, mocker):
        """ Test del item call. """
        val = 'value'
        alist = AcquiaList(None, False, {'key': val})

        self.assertEquals(alist['key'], val)

        del(alist['key'])
        with self.assertRaises(KeyError):
            my_var = alist['key']


    def test_first_no_data(self, mocker):
        """ Test calling first with an empty oject. """
        with self.assertRaises(AcquiaCloudNoDataException):
            self.alist.first()


    def test_last_no_data(self, mocker):
        """ Test calling last with no data in object. """
        with self.assertRaises(AcquiaCloudNoDataException):
            self.alist.last()


    def test_set_base_uri(self, mocker):
        """ Test setting the base uri. """

        uri = 'https://google.com'
        self.assertNotEquals(self.alist.uri, uri)

        self.alist.set_base_uri(uri)
        self.assertEquals(self.alist.uri, uri)

