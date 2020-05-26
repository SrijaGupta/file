import unittest2 as unittest
from mock import patch, MagicMock
from jnpr.toby.hldcl.trafficgen.ixia.IxRestApi import Connection, WebObject
#from jnpr.toby.hldcl.trafficgen.ixia import IxRestApi as IxRestUtils

#/jnpr/toby/hldcl/trafficgen/ixia

# import sys
# print(sys.executable)
# print("\n".join(sys.path))

class test_IxRestApi(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.rest = Connection(siteUrl="dummy",apiVersion="dummy")
    
    @classmethod
    def tearDownClass(self):
        print ("ixload")
        #self.rest.log("teardown class")
    
    def test_http_get(self):
        url = "http://dummy/ixload/stats/dummy/values'"
        jmock = MagicMock(return_value={"test": "test"})
        mk = MagicMock(status_code='200', json=jmock)
        self.rest.http_request= MagicMock(return_value=mk)
        connret = self.rest.http_get(url=url)
        self.assertIsInstance(connret, WebObject)

if __name__ == '__main__':
    unittest.main()

