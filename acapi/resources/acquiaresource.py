"""Generic Acquia Cloud API resource."""

from .acquiadata import AcquiaData


class AcquiaResource(AcquiaData):

    """Acquia Cloud API resource."""

    def get(self):
        """Return the resource from the Acquia Cloud API."""
        if None == self.data:
            response = self.request()
            self.data = response.content

        return self.data
