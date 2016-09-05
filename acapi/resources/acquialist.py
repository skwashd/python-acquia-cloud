"""Dictionary of Acquia Cloud API resources."""

from acapi.exceptions import AcquiaCloudNoDataException
from acapi.resources.acquiadata import AcquiaData


class AcquiaList(AcquiaData, dict):
    """Dictionary of Acquia Cloud API resources."""

    def __init__(self, base_uri, auth, *args, **kwargs):
        """See :func:AcquiaData.__init__."""
        self.sorted_keys = []

        # Setup the dict
        dict.__init__(self, *args, **kwargs)

        # Setup the list
        self.set_base_uri(base_uri)
        AcquiaData.__init__(self, self.uri, auth)

    def __delitem__(self, key):
        """See dict.__del_item__()."""
        super(AcquiaList, self).__delitem__(key)
        self.sorted_keys = []

    def __setitem__(self, key, value):
        """See dict.__set_item__()."""
        super(AcquiaList, self).__setitem__(key, value)
        self.sorted_keys = []

    def get_resource_uri(self, res):
        """Generate the resource URI.

        Parameters
        ----------
        res : mixed
            The identifier of the resource.

        Returns
        -------
        str
            The resource URI.
        """
        return '{base_uri}/{res}'.format(base_uri=self.uri, res=res)

    def first(self):
        """Retrieve the first item in the dictionary.

        Returns
        -------
        AcquiaResource
            The first resource in the dictionary.
        """
        if not len(self):
            raise AcquiaCloudNoDataException('No data available')

        key = self.search_pos(0)
        return self[key]

    def get_sorted_keys(self):
        """Get a sorted copy of the dictionary keys."""
        if not self.sorted_keys:
            keys = list(self.keys())
            self.sorted_keys = sorted(keys)

        return self.sorted_keys

    def last(self):
        """Retrieve the last item in the dictionary.

        Returns
        -------
        AcquiaResource
            The last resource in the dictionary.
        """
        if not len(self):
            raise AcquiaCloudNoDataException('No data available')

        key = self.search_pos(-1)
        return self[key]

    def search_pos(self, pos):
        """Search for a particular key.

        Parameters
        ----------
        pos : int
            The position of the key to return

        Returns
        -------
        str
            The key that occupies that position.
        """
        keys = self.get_sorted_keys()
        return keys[pos]

    def set_base_uri(self, base_uri):
        """Set the base URI for the resource.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        self.uri = base_uri
