""" Dictionary of Acquia Cloud API resources. """

from .acquiadata import AcquiaData


class AcquiaList(AcquiaData, dict):

    """ Dictionary of Acquia Cloud API resources. """

    def __init__(self, base_uri, auth, *args, **kwargs):
        """ See :func:AcquiaData.__init__. """
        self.sorted_keys = []

        # Setup the dict
        dict.__init__(self, *args, **kwargs)

        # Setup the list
        self.set_base_uri(base_uri)
        AcquiaData.__init__(self, self.uri, auth)


    def __delitem__(self, key):
        """ See dict.__del_item__(). """
        super(AcquiaList, self).__delitem__(key)
        sorted_keys = []

    def __setitem__(self, key, value):
        """ See dict.__set_item__(). """
        super(AcquiaList, self).__setitem__(key, value)
        sorted_keys = []

    def get_resource_uri(self, id):
        """ Generate the resource URI.

        Parameters
        ----------
        id : int
            The identified of the resource.

        Returns
        -------
        str
            The resource URI.
        """
        return '{base_uri}/{id}'.format(base_uri=self.uri, id=int(id))

    def first(self):
        """ Retrieve the first item in the dictionary.

        Returns
        -------
        AcquiaResource
            The first resource in the dictionary.
        """
        if not len(self):
            # FIXME Raise an exception here.
            return None

        key = self.search_pos(0)
        return self[key]

    def get_sorted_keys(self):
        """ Get a sorted copy of the dictionary keys. """
        if not self.sorted_keys:
            keys = self.keys()
            self.sorted_keys = sorted(keys)

        return self.sorted_keys

    def last(self):
        """ Retrieve the last item in the dictionary.

        Returns
        -------
        AcquiaResource
            The last resource in the dictionary.
        """
        if not len(self):
            # FIXME Raise an exception here.
            return None

        key = self.search_pos(-1)
        return self[key]

    def search_pos(self, pos):
        """ Search for a particular key.

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
