"""Acquia Cloud API server resource. """

from acapi.resources.acquiaresource import AcquiaResource


class Server(AcquiaResource):
    """Acquia Cloud API Server."""

    valid_keys = ['name', 'fqdn', 'services', 'status', 'ami_type',
                  'ec2_region', 'ec2_availability_zone']
