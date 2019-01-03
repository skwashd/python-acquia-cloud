"""Generic Acquia Cloud API resource."""

from acapi.resources.acquiadata import AcquiaData


class AcquiaResource(AcquiaData):
    """Acquia Cloud API resource."""

    #: Valid properties for this resource object
    valid_keys = None

    def __getitem__(self, key):
        """Get the value of an object property."""
        if self.data is None:
            self.get()

        if self.valid_keys is not None and key in self.valid_keys:
            return self.data[key]

    def get(self):
        """Return the resource from the Acquia Cloud API."""
        if self.data is None:
            response = self.request()
            self.data = response

        return self.data
