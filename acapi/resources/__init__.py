"""
I lifted from stackoverflow and hacked it
import os
import glob
files = glob.glob(os.path.dirname(__file__)+"/*.py")
modules = []
for f in files:
    if os.path.isfile(f) and not f.endswith('__init__.py'):
        modules[] = os.path.basename(f)[:-3]
__all__ = modules
del files
del modules
"""

import os
import re
import time

from ..imports import httplib2, json

from ..response import Response
from ..util import make_acapi_request

class AcquiaData(object):

    def __init__(self, uri, auth, data=None):
        self.uri = uri
        self.auth = auth
        self.data = data

    def request(self, uri=None, method='GET', data=None, params=None):
        if None == uri:
            uri = self.uri

        return make_acapi_request(method, uri, auth=self.auth, data=data, params=params)

    def task_uri(self, task_data):
        """
        This is a horrible hack, but it is needed for now
        """
        task_id = int(task_data['id'])

        p = re.compile('/sites/(.*)/envs.*')
        task_uri = ('%s/%d' % (p.sub('/sites/\g<1>/tasks', self.uri), task_id))

        return task_uri

    def wait_for_task(self, task_data, uri=None):
        """
        FIXME: Move this some where elese
        """
        if None == uri:
            uri = self.uri

        task_uri = self.task_uri(task_data)
        task = Task(task_uri, self.auth)

        while task.pending():
            # This seems like a reasonable trade off between being polite and 
            # hammering the API.
            time.sleep(3)

        return task.get()


class AcquiaResource(AcquiaData):

    def get(self):
        if None == self.data:
          response = self.request()
          self.data = response.content

        return self.data

class AcquiaList(AcquiaData, dict):

    def __init__(self, uri, auth, *args, **kwargs):
        AcquiaData.__init__(self, uri, auth)
        dict.__init__(self, *args, **kwargs)

class Backup(AcquiaResource):

    def delete(self):
        response = self.request(method='DELETE')
        return response.ok     
    
    def download(self, target_file):
        """
        Download a database backup file from the Acquia Cloud API.
        """

        response = self.request()
        backup = response.content

        # We do this as make_acapi_request() assumes response is a json string.
        http = httplib2.Http(
                proxy_info=Connection.proxy_info(),
                )
        resp, content = http.request(backup['link'].encode('ascii', 'ignore'), 'GET')

        file = open(target_file, 'wb')
        file.write(content)
        file.close()

        return True

class BackupList(AcquiaList):

    def create(self):
        response = self.request(method='POST')
        task_data = response.content

        task = self.wait_for_task(task_data)
        if None == task['completed']:
            raise Exception('Unable to request backup')

        id = int(json.loads(task['result'])['backupid'])
        uri = ('%s/%d' % (self.uri, id))
        backup = Backup(uri, self.auth)

        self.__setitem__(id, backup)

        return backup


class Database(AcquiaResource):

    def backup(self, id):
        uri = ('%s/backups/%d' % (self.uri, id))
        return Backup(uri, self.auth)

    def backups(self):
        uri = ('%s/backups' % (self.uri))

        backups = BackupList(uri, self.auth)

        response = self.request(uri=uri)
        for backup in response.content:
            id = int(backup['id'])
            backup_uri = ('%s/%d' % (uri, id))
            backups[id] = Backup(uri, self.auth, data=backup)

        return backups
    
    def copy(self, target):
        # More regex hacks to work around the limitations of the ACAPI.
        p = re.compile('/envs/(.*)/dbs/(.*)')
        m = p.search(self.uri)
        current_env = m.group(1)
        db = m.group(2)

        move_uri = ('%s/%s' % (p.sub('/dbs/\g<2>/db-copy/\g<1>', self.uri), target))

        response = self.request(uri=move_uri, method='POST')
        if response.ok:
            # Another hack, this time to get the URI for the domain.
            new_uri = self.uri.replace(('/%s/' % (current_env)), ('/%s/' % (target)))
            return Database(new_uri, self.auth)

        return False

class Domain(AcquiaResource):

    def cache_purge(self):
        uri = ('%s/cache' % (self.uri))
        response = self.request(uri=uri, method='DELETE')
        return response.ok

    def delete(self):
        response = self.request(method='DELETE')
        return response.ok

    def move(self, target):

        # These regex hacks are needed because Acquia doesn't keep this function
        # with domains, which sucks.
        p = re.compile('/envs/(.*)/domains/(.*)')
        m = p.search(self.uri)
        current_env = m.group(1)
        domain = m.group(2)

        move_uri = ('%s/%s' % (p.sub('/domain-move/\g<1>', self.uri), target))

        data = {'domains': [domain]}

        response = self.request(uri=move_uri, method='POST', data=data)
        if response.ok:
            # Another hack, this time to get the URI for the domain.
            new_uri = self.uri.replace(('/%s/' % (current_env)), ('/%s/' % (target)))
            return Domain(new_uri, self.auth)

        return False


class DomainList(AcquiaList):

    def create(self, name):
        uri = ('%s/%s' % (self.uri, name))
        response = self.request(method='POST', uri=uri)
        task_data = response.content

        task = self.wait_for_task(task_data, uri)
        if None == task['completed']:
            raise Exception('Failed to create domain')

        domain = Domain(uri, self.auth)

        self.__setitem__(name, domain)

        return domain


class Environment(AcquiaResource):
    
    def db(self, name):
        uri = ('%s/dbs/%s' % (self.uri, name))
        return Database(uri, self.auth)

    def dbs(self):
        dbs = {}
        uri = ('%s/dbs' % (self.uri))
        response = self.request(uri=uri)
        for db in response.content:
            name = db['name'].encode('ascii', 'ignore')
            db_uri = ('%s/%s' % (uri, name))
            dbs[name] = Database(db_uri, self.auth, data=db)

        return dbs

    def deploy_code(self, path):
        uri = ('%s/code-deploy' % (self.uri))
        params = {'path': path}
        response = self.request(uri=uri, method='POST', params=params)
        if response.ok:
            index = self.uri.find('/envs/')
            base_uri = self.uri[:index]
            task_uri = ('%s/tasks/%d' % (base_uri, int(response.content['id'])))
            return Task(task_uri, self.auth)
        
        return False


    def domain(self, name):
        uri = ('%s/domains/%s' % (self.uri, name))
        return Domain(uri, self.auth)

    def domains(self):
        uri = ('%s/domains' % (self.uri))

        domains = DomainList(uri, self.auth)

        response = self.request(uri=uri)
        for domain in response.content:
            name = domain['name'].encode('ascii','ignore')
            domain_uri = ('%s/%s' % (uri, name))
            domains[name] = Domain(domain_uri, self.auth, data=domain)

        return domains

    def server(self, name):
        uri = ('%s/servers/%s', (self.uri, name))
        return Server(uri, self.auth)

    def servers(self):
        uri = ('%s/servers' % (self.uri))

        servers = ServerList(uri, self.auth)

        response = self.request(uri=uri)
        for server in response.content:
            name = server['name'].encode('ascii', 'ignore')
            server_uri = ('%s/%s' % (uri, name))
            servers[name] = Server(server_uri, self.auth, data=server)

        return servers

class Server(AcquiaResource):
    pass

class ServerList(AcquiaList):
    pass


class Site(AcquiaResource):

    def environment(self, name):
        uri = ('%s/envs/%s' % (self.uri, name))
        return Environment(uri, self.auth)
        
    def environments(self):
        envs = {}
        uri = ('%s/envs' % (self.uri))
        response = self.request(uri=uri)
        for env in response.content:
            name = env['name'].encode('ascii', 'ignore')
            env_uri = ('%s/%s' % (uri, name))
            envs[name] = Environment(env_uri, self.auth, data=env)

        return envs
     
    def task(self, id):
        uri = ('%s/tasks/%d' % (self.uri, id))
        return Task(uri, self.auth)

    def tasks(self):
        tasks = {}
        uri = ('%s/tasks' % (self.uri))
        response = self.request(uri=uri)
        for task in response.content:
            id = int(task[u'id'])
            task_uri = ('%s/%d', (uri, id))
            tasks[id] = Task(task_uri, self.auth, data=task)

        return tasks


class Task(AcquiaResource):
    
    def pending(self):
        # Ensure we don't have stale data
        self.data = None

        task = self.get()
        state = task['state'].encode('ascii', 'ignore')
        return state not in ['done', 'error']

class User(AcquiaResource):

    def drushrc(self):
        """
        The json+PHP output of this isn't very useful in python.
        """
        uri =  ('%s/drushrc' % (self.uri))
        response = make_acapi_request('GET', uri, auth=self.auth)
        return response.content

