'''
    DESCRIPTION
    IxRestUtils is a collection of classes that offer a generic wrapper around a raw REST API.
    It handles:
    - Creating a connection;
    - Running HTTP methods for an active connection
    Abstracting the RAW HTTP input / output to tangible objects that will act as an interface to the REST API.
'''
import requests
from urllib.parse import urljoin
import json
import re
try:
    requests.packages.urllib3.disable_warnings()
except Exception:
    pass
# Gets a Connection instance, that will be used to make the HTTP requests to the application
def get_connection(server, port, http_redirect=False):
    '''
        getconnection perform connection to Ixload and returns session Url.
    '''
    transport_type = 'https' if not http_redirect else 'http'
    connection_url = "%s://%s:%s/" % (transport_type, server, port)
    conn = Connection(connection_url, "v0", http_redirect)
    return conn

class Connection(object):
    '''
        Class that executes the HTTP requests to the application instance.
        It handles creating the HTTP session and executing HTTP methods.

    '''
    kHeaderContentType = "content-type"
    kContentJson = "application/json"
    kApiKeyHeader = 'X-Api-Key'
    kApiKey = ''

    def __init__(self, siteUrl, apiVersion, http_redirect=False):
        '''
            Args:
            - siteUrl is the actual url to which the Connection instance will be made.
            - apiVersion is the actual version of the REST API that the Connection instance will use.
            The HTTP session will be created when the first http request is made.
        '''
        self.http_session = None
        self.http_redirect = http_redirect
        self.url = Connection.urljoin(siteUrl, "api")
        self.url = Connection.urljoin(self.url, apiVersion)

    @staticmethod
    def set_api_key(api_key):
        '''
            set_api_key will set connection key for REST calls.
        '''
        Connection.kApiKey = api_key

    def _get_http_session(self):
        '''
            This is a lazy initializer for the HTTP session.
            It does not need to be active until it is required.
        '''
        if self.http_session is None:
            self.http_session = requests.Session()
            if not self.http_redirect:
                from requests.adapters import HTTPAdapter
                from requests.packages.urllib3.poolmanager import PoolManager
                import ssl
                http_adapter = HTTPAdapter()
                http_adapter.poolmanager = PoolManager(ssl_version=ssl.PROTOCOL_TLSv1)
                self.http_session.mount('https://', http_adapter)
        return self.http_session

    @classmethod
    def urljoin(cls, base, end):
        """ Join two URLs. If the second URL is absolute, the base is ignored.
        Use this instead of urlparse.urljoin directly so that we can customize its behavior if necessary.
        Currently differs in that it
            1. appends a / to base if not present.
            2. casts end to a str as a convenience
        """
        if base and not base.endswith("/"):
            base = base + "/"
        return urljoin(base, str(end))

    def http_request(self, method, url="", data="", params=None, headers=None):
        '''
            Args:

            - Method (mandatory) represents the HTTP method that will be executed.
            - url (optional) is the url that will be appended to the application url.
            - data (optional) is the data that needs to be sent along with the HTTP method as the JSON payload
            - params (optional) the payload python dict not necessary if data is used.
            - headers (optional) these are the HTTP headers that will be sent along with the request. If left blank will use default

            Method for making a HTTP request. The method type (GET, POST, PATCH, DELETE) will be sent as a parameter.
            Along with the url and request data. The HTTP response is returned
        '''
        params = {} if params is None else params
        headers = {} if headers is None else headers
        headers[Connection.kHeaderContentType] = Connection.kContentJson
        if Connection.kApiKey != '':
            headers[Connection.kApiKeyHeader] = Connection.kApiKey
        if isinstance(data, dict):
            data = json.dumps(data)
        abs_url = Connection.urljoin(self.url, url)
        result = self._get_http_session().request(method, abs_url, data=str(data), params=params, headers=headers, verify=False)
        return result

    def http_get(self, url="", data="", params=None, headers=None, error_codes=None, option=None):
        '''
            Method for calling HTTP GET. This will return a WebObject that has the fields returned
            in JSON format by the GET operation.
        '''
        params = {} if params is None else params
        headers = {} if headers is None else headers
        error_codes = [] if error_codes is None else error_codes
        reply = self.http_request("GET", url, data, params, headers)
        if reply.status_code in error_codes:
            raise Exception("Error on executing GET request on url %s: %s" % (url, reply.text))
        if option:
            return reply.json()
        else:
            return _format_response(reply.json(), url)

    def http_options(self, url="", data="", params=None, headers=None, error_codes=None):
        '''
            Method for calling HTTP Option. This will return a WebObject that has the fields returned
            in JSON format by the Option operation.
        '''
        params = {} if params is None else params
        headers = {} if headers is None else headers
        error_codes = [] if error_codes is None else error_codes
        reply = self.http_request("OPTIONS", url, data, params, headers)
        if reply.status_code in error_codes:
            raise Exception("Error on executing Options request on url %s: %s" % (url, reply.text))
        return _format_response(reply.json(), url)

    def http_post(self, url="", data="", params=None, headers=None):
        '''
            Method for calling HTTP POST. Will return the HTTP reply.
        '''
        params = {} if params is None else params
        headers = {} if headers is None else headers
        return self.http_request("POST", url, data, params, headers)

    def http_patch(self, url="", data="", params=None, headers=None):
        '''
            Method for calling HTTP PATCH. Will return the HTTP reply.
        '''
        params = {} if params is None else params
        headers = {} if headers is None else headers
        return self.http_request("PATCH", url, data, params, headers)

    def http_delete(self, url="", data="", params=None, headers=None):
        '''
            Method for calling HTTP DELETE. Will return the HTTP reply.
        '''
        params = {} if params is None else params
        headers = {} if headers is None else headers
        return self.http_request("DELETE", url, data, params, headers)

def _format_response(value, _url_=None):
    '''
        Method used for creating a wrapper object corresponding to the JSON string received on a GET request.
    '''
    if isinstance(value, dict):
        if _url_ and bool(re.search(r'[\w.-]+/ixload/stats/[\w().-]+/values', _url_)):
            pass#'values' resources only have name and value of the stats, don't need the url
        else:
            value['_url_'] = _url_
        result = WebObject(**value)
        #result = value
    elif isinstance(value, list):
        #result = WebList(entries=value, _url_=_url_)
        result = value
    else:
        result = value
    return result

class WebList(list):
    '''
        Using this class a JSON list will be transformed in a list of WebObject instances.
    '''
    def __init__(self, entries=None, _url_=None):
        '''
            Create a WebList from a list of items that are processed by the _format_response function
        '''
        list.__init__(self)
        entries = [] if entries is None else entries
        self._url_ = _url_
        url = _url_
        filter_syntax = "?filter=" # we need to remove the query param syntax from all chindren of the list.
        if url and filter_syntax in url:
            url = url.split(filter_syntax)[0] # get everything on the left of the filter, removing the query param
        for item in entries:
            item_url = None
            if "objectID" in item:
                item_url = "%s/%s" % (url, item["objectID"])
            self.append(_format_response(item, item_url))

    def copy_data(self, new_obj):
        '''
            copy date and retrun json
        '''
        self[:] = []
        for item in new_obj:
            self.append(item)


class WebObject(object):
    '''
        A WebObject instance will have its fields set to correspond to the JSON format received on a GET request.
        for example: a response in the format: {"caption": "http"} will return an object that has obj.caption="http"
    '''
    def __init__(self, **entries):
        '''
            Create a WebObject instance by providing a dict having a property - value structure.
        '''
        self.json_options = {}
        for key, value in entries.items():
            web_obj = _format_response(value)
            self.json_options[key] = web_obj
            self.__dict__[key] = web_obj

    def copy_data(self, new_obj):
        '''
            copy date and retrun json
        '''
        self.json_options = {}
        for key, obj in new_obj.json_options.items():
            self.json_options[key] = obj
            self.__dict__[key] = obj

    def get_options(self):
        '''
            Get the JSON dictionary which represents the WebObject Instance
        '''
        return self.json_options
