""" Imports all the resources. """

# Base classes
from acapi.resources.acquiadata import AcquiaData
from acapi.resources.acquialist import AcquiaList
from acapi.resources.acquiaresource import AcquiaResource

# Databases can be backed up
from acapi.resources.backup import Backup
from acapi.resources.backuplist import BackupList

# Environments have databases
from acapi.resources.database import Database
from acapi.resources.databaselist import DatabaseList

# Environments have domains
from acapi.resources.domain import Domain
from acapi.resources.domainlist import DomainList

# Sites reference environments
from acapi.resources.environment import Environment
from acapi.resources.environmentlist import EnvironmentList

# Sites have servers
from acapi.resources.server import Server
from acapi.resources.serverlist import ServerList

# Sites have tasks
from acapi.resources.task import Task
from acapi.resources.tasklist import TaskList

# Site is our top level
from acapi.resources.site import Site
from acapi.resources.sitelist import SiteList

# Users are top level
from acapi.resources.user import User

__all__ = [
    'AcquiaData',
    'AcquiaList',
    'AcquiaResource',
    'Backup',
    'BackupList',
    'Database',
    'DatabaseList',
    'Domain',
    'DomainList',
    'Environment',
    'EnvironmentList',
    'Server',
    'ServerList',
    'Task',
    'TaskList',
    'Site',
    'SiteList',
    'User',
]
