# pylint: disable=invalid-name

"""
grpcConn-test-module
"""


import unittest2 as unittest# pylint: disable=import-error
from mock import patch, MagicMock # pylint: disable=import-error
from jnpr.toby.hldcl.channels.grpcConn import Grpc # pylint: disable=import-error
import os
#import sys

#sys.path.append('/volume/regressions/grpc_lib/19.2')

#from authentication_service_pb2 import *
#import authentication_service_pb2

def testfun():
    """
    DOC
    """
    return True

# class MockImplement(object):
#     """
#     DOC
#     """
#     def __init__(self):
#         pass
#
#     def insecure_channel(self):
#         """
#         DOC
#         """
#         return True

class MockAuthSerPb2(object):
    """
    DOC
    """
    def __init__(self):
        pass

    def LoginStub(self):# pylint: disable=invalid-name
        """
        authentication_service_pb2 LoginStub
        """
        return self

    def LoginCheck(self):# pylint: disable=invalid-name
        """
        authentication_service_pb2 LoginCheck
        """
        return True

class Returnexception(BaseException):
    """
    DOC
    """
    pass

# class MockImplementNeg(object):
#     def __init__(self):
#         pass
#
#     def insecure_channel(self):
#         raise Exception("channel failure")

class MockAuthSerPb2Neg(object):
    """
    DOC
    """
    def __init__(self):
        pass

    def LoginStub(self):# pylint: disable=invalid-name
        """
        DOC
        """
        return self

    @staticmethod
    def LoginCheck(*args): # pylint: disable=invalid-name
        """
        DOC
        """
        args = args
        return False

# Mock prpd_service_pb2
class Mockimportlib(object):
    """
    DOC
    """
    def __init__(self):
        pass

    def BgpRouteStub(self, *args):# pylint: disable=invalid-name
        """
        DOC
        """
        args = args
        return self


    def bgprouteadd(self, *args, **kwargs):
        """
        DOC
        """
        args = args
        kwargs = kwargs
        return True

    def bgprouteinitialize(self, *args, **kwargs):
        """
        DOC
        """
        args = args
        kwargs = kwargs
        return True

    def test_api(self, *args, **kwargs):
        """
        DOC
        """
        args = args
        kwargs = kwargs
        return True

# class Mockeval(object):
#     """
#     DOC
#     """
#     def __init__(self):
#         pass
#
# class Mockgetattr(object):
#     """
#     DOC
#     """
#     def __init__(self):
#         return testfun


class Mydict(dict):
    """
    DOC
    """
    def read(self, var1='aa'):
        """
        DOC
        """
        var1 = var1
        return "{'libraries': ['var1']}"

class MockFileHandle(object):
    """
            Mock Class to emulate Operations on file
    """

    def __init__(self, fname):
        self.name = fname

    def write(self, text):
        """
        DOC
        """
        return text

    def read(self, var1='a'):
        """
        DOC
        """
        if var1 is not 'test_yaml':
            #var2 = Mydict()
            if hasattr(os.environ, 'NO_API_ARGS'):
                return True
            return """
                      Libraries:
                         - bgp_route_service_pb2.py
                         - prpd_common_pb2.py
                         - jnx_addr_pb2.py
                         - prpd_service_pb2.py
                         - test.pm
                      tc0:
                        BgpRoute:
                          bgprouteinitialize:
                            bgprouteinitializerequest_cat_init: {valid: [bgprouteinitializerequest], negative : [], boundary : [], explore : []}        
                    """
        else:
            return "{'libraries': ['bgp_route_service_pb2.py']}"

class MockFileHandleFail(object):
    """
            Mock Class to emulate Operations on file
    """

    def __init__(self, fname):
        """
        DOC
        """
        self.name = fname

    def write(self, text):
        """
        DOC
        """
        return text

    def read(self, var1='a'):
        """
        DOC
        """
        if var1 is not 'test_yaml':
            #var2 = Mydict()
            if hasattr(os.environ, 'NO_API_ARGS'):
                return True
            return """
                      Libraries:
                         - bgp_route_service_pb2.py
                         - prpd_common_pb2.py
                         - jnx_addr_pb2.py
                         - prpd_service_pb2.py
                         - test.pm
                      tc0:
                        BgpRoute:
                          bgprouteinitialize:
                              bgprouteinitializerequest: {valid: [bgprouteinitializerequest], negative : [], boundary : [], explore : []}
                    """
        else:
            return "{'libraries': ['bgp_route_service_pb2.py']}"

class Mypopen(object):
    """
    DOC
    """
    def __init__(self, test_string):
        self.result = [test_string.encode('utf')]
    def communicate(self):
        """
        DOC
        """
        return self.result

class TestGRPCModule(unittest.TestCase):
    """
    DOC
    """
    def setUp(self):# pylint: disable=invalid-name
        """
        DOC
        """
        self.grpc = Grpc(host='1.1.1.1', port='5555', user='test', password='test123', grpc_lib_path='my_path')
        self.grpc.timeout = 1

    def test_grpc_init(self):
        """
        DOC
        """
        mobject = MagicMock(spec=Grpc)
        mobject.user = 'user'
        rhandle = MagicMock()
        rhandle.os = 'IOS'
        try:
            Grpc.__init__(mobject, rhandle=rhandle)
        except: # pylint: disable=bare-except
            pass
        self.assertRaises(Exception, Grpc, mobject, {rhandle:rhandle})

        # Grpc with host
        self.assertEquals(self.grpc.host, '1.1.1.1')
        self.assertEquals(self.grpc.user, 'test')
        self.assertEquals(self.grpc.password, 'test123')
        self.assertEquals(self.grpc.port, 5555)
        self.assertEquals(self.grpc.grpc_lib_path, 'my_path')

        # Grpc with rhandle
        rhandle = MagicMock()
        rhandle.os = 'JUNOS'
        rhandle.name = MagicMock(return_value='1.1.1.1')
        rhandle.USER = MagicMock(return_value='test')
        rhandle.PASSWORD = MagicMock(return_value='test123')
        obj = Grpc(rhandle=rhandle, grpc_lib_path="path1")
        self.assertEquals(obj.port, 50051)
        self.assertIsInstance(obj.host, MagicMock)

    def test_grpc_init_errors(self):
        """
        DOC
        """

        # Exception when host and rhandle is provided
        with self.assertRaises(AttributeError):
            Grpc(host='1.1.1.1', rhandle='1.1.1.1', port='5555')

        # Exception when host and rhandle are not provided
        with self.assertRaises(AttributeError):
            Grpc(port='5555', user='test', password='test')

        # using rhandle and not Junos object
        rhandle = MagicMock(spec=['NAME'])
        rhandle.name = MagicMock(return_value='1.1.1.1')
        with self.assertRaises(AttributeError):
            Grpc(rhandle=rhandle, port='5555')

        # user and password not available
        with self.assertRaises(AttributeError):
            Grpc(host='1.1.1.1', port='5555')

    @patch('authentication_service_pb2_grpc.LoginStub')
    def test_grpc_open(self, test):
        """
        DOC
        """
#         os.environ['LEGO_LIBS_DIR'] = os.getcwd()
#         LEGO_LIBS_DIR = os.getenv('LEGO_LIBS_DIR')

        ## response=true case
        login_response = MagicMock()
        login_response.result = True
        test.return_value.LoginCheck.return_value = login_response

        self.assertEquals(self.grpc.open(), True)

        ## response=false case
        login_response = MagicMock()
        login_response.result = False
        test.return_value.LoginCheck.return_value = login_response

        self.assertEquals(self.grpc.open(), False)
    #@patch('grpc.insecure_channel', return_value=Exception('err'))
    def test_grpc_open_neg(self):
        """
        DOC
        """
        self.assertEquals(self.grpc.open(), False)

    #@patch('authentication_service_pb2.LoginStub', return_value=Returnexception())
    def test_grpc_open_neg1(self):
        """
        DOC
        """
        self.assertEquals(self.grpc.open(), False)

    #@patch('authentication_service_pb2.LoginStub', return_value=Returnexception())
    def test_grpc_open_neg2(self):
        """
        DOC
        """
        self.assertEquals(self.grpc.open(), False)

    @patch('authentication_service_pb2_grpc.LoginStub', return_value=MockAuthSerPb2())
    @patch('builtins.open')
    @patch('importlib.import_module', return_value=Mockimportlib())
    @patch('builtins.eval')
    @patch('jnpr.toby.hldcl.channels.grpcConn.file_util')
    def test_grpc_send_api(self, pone, ptwo, pthree, pfour, pfive):
        """
        DOC
        """
        pone.find_file.return_value = 'ffile1'
        pfour.return_value = MockFileHandle('test')
#         os.environ['LEGO_LIBS_DIR'] = os.getcwd()
#         LEGO_LIBS_DIR = os.getenv('LEGO_LIBS_DIR')
        self.grpc.open()

        # with api
        self.assertEquals(
            self.grpc.send_api(api='test_api', args='some-args', service='BgpRoute'), True)

        # with api_call
        self.assertEquals(
            self.grpc.send_api(api_call='bgprouteinitialize(bgprouteinitializerequest())',
                               service='BgpRoute', library='test_yaml'), True)

        # with api_call, but no 'library'
        self.assertEquals(
            self.grpc.send_api(api_call='bgprouteinitialize(bgprouteinitializerequest())',
                               service='BgpRoute'),
            False)

        # with api_call neg case
        self.assertEquals(
            self.grpc.send_api(api_call='bgprouteadd', service='BgpRoute', library='test_yaml'), False)

        # with id
        self.assertEquals(self.grpc.send_api(id='tc0', yaml_file='test_yaml'), True)
        # with id neg
        self.assertEquals(self.grpc.send_api(id='tc0'), False)
        pone.side_effect = [Exception('err'), Exception('err')]
        self.assertEquals(
            self.grpc.send_api(api_call='bgprouteadd', service='BgpRoute', library='test_yaml'), False)
        self.assertEquals(self.grpc.send_api(id='tc0', yaml_file='test_yaml'), True)

        pone.find_file.return_value = 'file'
        self.grpc.services = {'BgpRoute': MagicMock(), 'bgprouteadd': MagicMock()}
        self.assertIsNotNone(
            self.grpc.send_api(api='test_api', args='some-args', service='BgpRoute', library='test_yaml'))
        self.grpc.services = {'bgprouteadd': MagicMock()}
        self.assertIsNotNone(
            self.grpc.send_api(api_call='bgprouteadd(1)', args='some-args', service='BgpRoute', library='test_yaml'))

        self.assertIsNone(self.grpc.send_api())

        self.grpc.services = {'Test': MagicMock()}
        self.assertEquals(self.grpc.send_api(id='tc0', yaml_file='test_yaml'),
                          True)

        pfour.return_value = MockFileHandleFail('test')
        self.assertEquals(self.grpc.send_api(id='tc0', yaml_file='test_yaml'),
                          True)

        pone.find_file.side_effect = Exception()
        self.assertEquals(self.grpc.send_api(api_call='bgprouteadd',
                                             args='some-args',
                                             service='BgpRoute',
                                             library='test_yaml'),
                          False)
        self.assertEquals(self.grpc.send_api(id='tc0', yaml_file='test_yaml'),
                          False)

    @patch('authentication_service_pb2_grpc.LoginStub', return_value=MockAuthSerPb2())
    @patch('builtins.open', return_value=MockFileHandle('test'))
    @patch('importlib.import_module', return_value=Mockimportlib())
    @patch('builtins.eval')
    def test_grpc_send_api_errors(self, *args):
        """
        DOC
        """
        self.grpc.open()

        # service not provided for api
        self.assertEquals(self.grpc.send_api(api='test_api'), False)

        # args not provided for api
        self.assertEquals(self.grpc.send_api(api='test_api', service='test_service'), False)

        # service not provided for api_call
        self.assertEquals(self.grpc.send_api(api_call='test_api'), False)

    #@patch('builtins.encode')
    def test_get_grpc_id(self):
        """
        DOC
        """
        self.assertIsInstance(self.grpc.get_grpc_id(), bytes)

    @patch('jnpr.toby.hldcl.channels.grpcConn.Popen', side_effect=[Mypopen(
        "test/test.py\ntest/test.py\ntest/test.py\n"), Mypopen("test/test.py\n"), Mypopen("test/\n")])
    def test_get_module_name(self, Popen_patch):
        """
        DOC
        """
        mobject = MagicMock(spec=Grpc)
        mobject.grpc_lib_path = "path"
        mobject.bypass_jsd = None
        Grpc._get_module_name(mobject, service="service") # pylint: disable=protected-access


    @patch('importlib.import_module')
    def test_create_stub(self, import_module_mock):
        """
        DOC
        """
        mobject = MagicMock(spec=Grpc)
        mobject.channel = 'test'
        mobject.host = 'test'
        mobject.bypass_jsd = None
        mobject.services = {'service': 'test'}
        tmp = MagicMock()
        tmp.serviceStub.return_value = 'test'
        import_module_mock.return_value = tmp

        self.assertEquals(Grpc._create_stub(mobject, service='service'), True) # pylint: disable=protected-access
        self.assertEquals(Grpc._create_stub(mobject, service='service', service_name='test'), True) # pylint: disable=protected-access

        mobject.bypass_jsd = True
        self.assertEquals(Grpc._create_stub(mobject, service='service', service_name='test'), True) # pylint: disable=protected-access

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestGRPCModule)
    unittest.TextTestRunner(verbosity=2).run(SUITE)

