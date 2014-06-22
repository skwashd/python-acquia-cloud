from .imports import json

class Response(object):
    """
    Take a httplib2 response and turn it into a response object

    Borrowed from twilio-python.
    """
    def __init__(self, httplib_resp, content, url):
        self.headers = httplib_resp
        self.content = json.loads(content)
        self.cached = False
        self.status_code = int(httplib_resp.status)
        self.ok = self.status_code < 400
        self.url = url
