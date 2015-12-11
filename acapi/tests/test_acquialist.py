""" Tests the Acquia list class. """
import requests_mock

from . import BaseTest
from ..resources import DatabaseList
from ..exceptions import AcquiaCloudNoDataException

@requests_mock.Mocker()
class TestAcquiaList(BaseTest):
    """Tests the Acquia Cloud API db list class."""

    dblist = None

    def test_delitem(self, mocker):
        """ Test del item call. """
        json = [
            {
                "db_cluster": "4",
                "host": "srv-4",
                "instance_name": "mysitedev",
                "name": "mysite",
                "password": "UeytUwwZxpfqutH",
                "username": "mysitedev"
            }
        ]

        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/dbs.json',
            json=json
        )
        
        dblist = self.client.site('mysite').environment('dev').dbs()
        del(dblist['mysite'])


    def test_first_no_data(self, mocker):
        """ Test calling first with an empty oject. """
        dblist = self.get_empty_list(mocker)

        with self.assertRaises(AcquiaCloudNoDataException):
            dblist.first()


    def test_last_no_data(self, mocker):
        """ Test calling last with no data in object. """
        dblist = self.get_empty_list(mocker)

        with self.assertRaises(AcquiaCloudNoDataException):
            dblist.last()


    def test_set_base_uri(self, mocker):
        """ Test setting the base uri. """
        dblist = self.get_empty_list(mocker)

        uri = 'https://google.com'
        self.assertNotEquals(dblist.uri, uri)

        dblist.set_base_uri(uri)
        # FIXME This doesn't seem right.
        self.assertEquals(dblist.uri, uri + '/dbs')


    def get_empty_list(self, mocker):
        """ Fetches an empty acquia list derived object. """

        json = []

        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/dbs.json',
            json=json
        )
        
        return self.client.site('mysite').environment('dev').dbs()
