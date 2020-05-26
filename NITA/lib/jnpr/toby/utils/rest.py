"""
REST API UTILITY
"""
import requests


#from jnpr.toby.init.init import init
#init(initialize_t=True)


class RESTClient(object):
    """
    The RESTClient service utility
    """

    def __init__(self, host, user=None, password=None, **kwargs):
        """
        """
        self.host = host
        self.user = user
        self.password = password
        self.protocol = kwargs.get('protocol', 'https')
        self._kwargs = kwargs
        self.session = requests.Session()
        if self.user is not None:
            self.session.auth = (self.user, self.password)
        self.session.verify = False
        self.session.headers.update(kwargs.get('headers', {}))
        self.urlprefix = self.protocol + '://' + self.host + '/'

    def get(self, url, **kwargs):
        """
        Read a specific resource (by an identifier) or a collection of resources.
        """
        response = self.session.get(self.urlprefix + url, **kwargs)
        return response

    def post(self, url, **kwargs):
        """
        used to post a New resource, Non-idempotent.
        """
        response = self.session.post(self.urlprefix + url, **kwargs)
        return response

    def put(self, url, **kwargs):
        """
        Update a specific resource (by an identifier) or a collection of resources.
        Can also be used to post a specific resource if the resource identifier is know before-hand.
        """
        response = self.session.put(self.urlprefix + url, **kwargs)
        return response

    def delete(self, url, **kwargs):
        """
        Remove/delete a specific resource by an identifier.
        """
        response = self.session.delete(self.urlprefix + url, **kwargs)
        return response

def create_rest_client(host, user=None, password=None, **kwargs):
    """

    :param host:
    *MANDATORY* host required for API call
    :param username:
    *OPTIONAL* Username for Authentication
,    :param password:
    *PASSWORD* Password for Authentication
    :param protocol:
    *MANDATORY* Protocol used
    :param timeout:
    *OPTIONAL* Timeout
    :return: RestClient handle
    """
    return RESTClient(host, user, password, **kwargs)

def rest_get(restclient, url=None, headers=None):
    """
       :param restclient:
       *MANDATORY* RestClient handle on which REST Methods
       are invoked
       :param url:
       *MANDATORY* URL to be invoked
       :param headers:
       *OPTIONAL* Headers based on User content negotiation.
       :param timeout:
       *OPTIONAL* timeout
       :return: Response for Particular resource
       or Collection of resource.
       """

    t.log(level="INFO", message="Entering Rest GET")
    t.log(level="INFO", message="URL for Rest GET: " + str(restclient.urlprefix) + str(url))
    response = restclient.get(url, headers=headers)
    t.log(level="INFO", message="Response from REST GET: " + str(response))
    return response

def rest_post(restclient, url=None, headers=None, data=None):
    """
    :param restclient:
    *MANDATORY* RestClient handle on which REST Methods
    are invoked
    :param url:
    *MANDATORY* URL to be invoked
    :param headers:
    *OPTIONAL* Headers based on User content negotiation.
    :param data:
    *MANDATORY* form-encoded data to identify particular
    resource
    :param timeout:
    *OPTIONAL* timeout
    :return: Response object.
    """

    t.log(level="INFO", message="Entering Rest CREATE")
    t.log(level="INFO", message="URL for Rest CREATE: " + str(restclient.urlprefix) + str(url))
    response = restclient.post(url, data=data, headers=headers)
    t.log(level="INFO", message="Response from REST CREATE: " + str(response))
    return response



def rest_put(restclient, url=None, headers=None, data=None):
    """
    :param restclient:
    *MANDATORY* RestClient handle on which REST Methods
    are invoked
    :param url:
    *MANDATORY* URL to be invoked. Should contain resource Id in Path parameter.
    :param headers:
    *OPTIONAL* Headers based on User content negotiation.
    :param data:
    *MANDATORY* form-encoded data to identify particular
    resource
    :param timeout:
    *OPTIONAL* timeout
    :return: Response object.
    """
    t.log(level="INFO", message="Entering Rest PUT")
    t.log(level="INFO", message="URL for Rest UPDATE: " + str(restclient.urlprefix) + str(url))
    response = restclient.put(url, data=data, headers=headers)
    t.log(level="INFO", message="Response from REST PUT: " + str(response))
    return response

def rest_delete(restclient, url=None, headers=None, data=None):
    """
    :param restclient:
    *MANDATORY* RestClient handle on which REST Methods
    are invoked
    :param url:
    *MANDATORY* URL to be invoked. Should contain resource Id in Path parameter.
    :param headers:
    *OPTIONAL* Headers based on User content negotiation.
    :param data:
    *OPTIONAL* form-encoded data to identify particular
    resource
    :param timeout:
    *OPTIONAL* timeout
    :return: Response object.
    """
    t.log(level="INFO", message="Entering Rest DELETE")
    t.log(level="INFO", message="URL for Rest DELETE: " + str(restclient.urlprefix) + str(url))
    response = restclient.delete(url, data=data, headers=headers)
    t.log(level="INFO", message="Response from REST DELETE: " + str(response))
    return response
