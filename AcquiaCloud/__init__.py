import urllib2
import re
import json

from six import u

# Backwards compatibility.
from .version import __version__, __version_info__

from .base import Response, make_acapi_request

class CloudObject(object):

    def __init__(self, uri, auth):
        self.uri = uri
        self.auth = auth

    def get(self):
        response = make_acapi_request('GET', self.uri, auth=self.auth)
        return response.content


class Domain(CloudObject):

    def add(self):
        response = make_acapi_request('POST', self.uri, auth=self.auth)
        if response.ok:
            return Domain(self.uri, self.auth)

        return False

    def cache_purge(self):
        uri = ('%s/cache' % (self.uri))
        response = make_acapi_request('DELETE', uri, auth=self.auth)
        return response.ok

    def delete(self):
        response = make_acapi_request('DELETE', self.uri, auth=self.auth)
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

        response = make_acapi_request('POST', move_uri, auth=self.auth, data=data)
        if response.ok:
            # Another hack, this time to get the URI for the domain.
            new_uri = self.uri.replace(('/%s/' % (current_env)), ('/%s/' % (target)))
            return Domain(new_uri, self.auth)

        return False


class Environment(CloudObject):

    def deploy_code(self, path):
        uri = ('%s/code-deploy' % (self.uri))
        params = {'path': path}
        response = make_acapi_request('POST', uri, auth=self.auth, params=params)
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
        domains = {}
        uri = ('%s/domains' % (self.uri))
        response = make_acapi_request('GET', uri, auth=self.auth)
        for domain in response.content:
            name = domain['name'].encode('ascii','ignore')
            domain_uri = ('%s/%s' % (uri, name))
            domains[name] = Domain(domain_uri, self.auth)

        return domains


class Site(CloudObject):

    def environment(self, name):
        uri = ('%s/envs/%s' % (self.uri, name))
        return Environment(uri, self.auth)
        
    def environments(self):
        envs = {}
        uri = ('%s/envs' % (self.uri))
        response = make_acapi_request('GET', uri, auth=self.auth)
        for env in response.content:
            name = env['name'].encode('ascii','ignore')
            env_uri = ('%s/%s' % (uri, name))
            envs[name] = Environment(env_uri, self.auth)

        return envs
     
    def task(self, id):
        uri = ('%s/tasks/%d' % (self.uri, id))
        return Task(uri, self.auth)

    def tasks(self):
        tasks = {}
        uri = ('%s/tasks' % (self.uri))
        response = make_acapi_request('GET', uri, auth=self.auth)
        for task in response.content:
            id = int(task[u'id'])
            tasks[id] = task

        return tasks



class Task(CloudObject):
    pass

class User(CloudObject):

    def drushrc(self):
        uri =  ('%s/drushrc' % (self.uri))
        response = make_acapi_request('GET', uri, auth=self.auth)
        return response.content

class Client(object):
    '''
    A Client for accessing the Acquia Cloud API.

    :param str user: Acquia Cloud API username.

    :param str token: Acquia Cloud API user token.

    :param str realm: Acquia Cloud API realm (defaults to 'prod').

    :param str endpoint: Acquia Cloud API endpoint.
    '''

    def __init__(self, user=None, token=None, realm='prod', endpoint='https://cloudapi.acquia.com/v1'):

        '''
        Create an Acquia Cloud API REST client.
        '''

        self.auth = (user, token)
        self.realm = realm
        self.endpoint = endpoint

        # User endpoints
        self.user = User(self.generate_uri('me'), self.auth)

    def generate_uri(self, path):
        uri = ('%s/%s' % (self.endpoint, path))
        return uri
    
    def site(self, name):
        namespace = ('sites/%s:%s' % (self.realm, name))
        uri = self.generate_uri(namespace)
        site = Site(uri, self.auth)
        return site

    def sites(self):
        sites = {}

        uri = self.generate_uri('sites')
        response = make_acapi_request('GET', uri, auth=self.auth)

        for site in response.content:
            realm, name = site.encode('ascii','ignore').split(':')
            site_uri = self.generate_uri('sites/%s' % (name))
            sites[name] = Site(site_uri, self.auth)

        return sites
