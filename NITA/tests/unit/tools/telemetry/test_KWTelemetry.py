"""UT for the module jnpr.toby.tools.telemetry.KWTelemetry"""

import unittest2 as unittest
from mock import patch, MagicMock

from jnpr.toby.tools.telemetry.KWTelemetry import KWTelemetry

class TestKWTelemetry(unittest.TestCase):
    """UT for KWTelemetry"""
    @patch('jnpr.toby.tools.telemetry.KWTelemetry.socket')
    @patch('jnpr.toby.tools.telemetry.KWTelemetry.pwd')
    @patch('jnpr.toby.tools.telemetry.KWTelemetry.os')
    @patch('jnpr.toby.tools.telemetry.KWTelemetry.create_connection', return_value="test")
    def test_kwtelemetry_init(self, conn_patch, os_patch, pwd_patch, socket_patch):
        """Test '__init__' method of class KWTelemetry"""
        socket_patch.gethostname.return_value = "regress"
        pwd_patch.getpwuid.return_value = ['user']
        os_patch.getuid.return_value = "uid"
        os_patch.getpid.return_value = 100
        kobject = KWTelemetry()
        self.assertEqual(kobject.data, {})
        self.assertEqual(kobject._hostname, "regress")
        self.assertEqual(kobject._user, "user")
        self.assertEqual(kobject._pid, 100)

    @patch('jnpr.toby.tools.telemetry.KWTelemetry.create_connection', return_value=True)
    def test_kwtelemetry__post(self, ws_crete_conn):
        """Test '_post' method of class KWTelemetry"""
        kobject = MagicMock(spec=KWTelemetry)
        kobject._user = "user"
        kobject._hostname = "hostname"
        kobject._pid = 100
        data = {}
        self.assertFalse(KWTelemetry._post(kobject, data))

        kobject._ws = MagicMock()
        kobject._ws.connected = True
        kobject._ws.send.return_value = "test"
        self.assertTrue(KWTelemetry._post(kobject, data))

        kobject._ws.connected = False
        self.assertFalse(KWTelemetry._post(kobject, data))

    def test_kwtelemetry_start_suite(self):
        """Test 'start_suite' method of class KWTelemetry"""
        kobject = MagicMock(spec=KWTelemetry)

        attrs = {}
        attrs['id'] = 111
        attrs['source'] = "source"
        attrs['longname'] = "longname"
        attrs['starttime'] = "starttime"
        attrs['tests'] = ['test1', 'test2']
        attrs['totaltests'] = 1000

        data = {}
        data['id'] = 111
        data['name'] = "test"
        data['source'] = "source"
        data['longname'] = "longname"
        data['starttime'] = "starttime"
        data['tests'] = "test1;test2"
        data['totaltests'] = 1000

        kobject._post.return_value = "test"
        self.assertIsNone(KWTelemetry.start_suite(kobject, "test", attrs))
        kobject._post.assert_called_with(data)

    def test_kwtelemetry_end_suite(self):
        """Test 'end_suite' method of class KWTelemetry"""
        kobject = MagicMock(spec=KWTelemetry)

        attrs = {}
        attrs['id'] = 111
        attrs['source'] = "source"
        attrs['longname'] = "longname"
        attrs['starttime'] = "starttime"
        attrs['endtime'] = "endtime"
        attrs['elapsedtime'] = "elapsedtime"
        attrs['status'] = "PASS"
        attrs['message'] = "msg"
        attrs['statistics'] = "stats"

        data = {}
        data['id'] = 111
        data['name'] = "test"
        data['source'] = "source"
        data['longname'] = "longname"
        data['starttime'] = "starttime"
        data['endtime'] = "endtime"
        data['elapsedtime'] = "elapsedtime"
        data['status'] = "PASS"
        data['message'] = "msg"
        data['statistics'] = "stats"

        kobject._post.return_value = "test"
        self.assertIsNone(KWTelemetry.end_suite(kobject, "test", attrs))
        kobject._post.assert_called_with(data)

    def test_kwtelemetry_start_test(self):
        """Test 'start_test' method of class KWTelemetry"""
        kobject = MagicMock(spec=KWTelemetry)

        attrs = {}
        attrs['id'] = 111
        attrs['longname'] = "longname"
        attrs['starttime'] = "starttime"

        data = {}
        data['id'] = 111
        data['testName'] = "test"
        data['longname'] = "longname"
        data['starttime'] = "starttime"

        kobject._post.return_value = "test"
        self.assertIsNone(KWTelemetry.start_test(kobject, "test", attrs))
        kobject._post.assert_called_with(data)

    def test_kwtelemetry_end_test(self):
        """Test 'end_test' method of class KWTelemetry"""
        kobject = MagicMock(spec=KWTelemetry)

        attrs = {}
        attrs['id'] = 111
        attrs['longname'] = "longname"
        attrs['starttime'] = "starttime"
        attrs['endtime'] = "endtime"
        attrs['elapsedtime'] = "elapsedtime"
        attrs['status'] = "PASS"
        attrs['message'] = "msg"

        data = {}
        data['id'] = 111
        data['testName'] = "test"
        data['longname'] = "longname"
        data['starttime'] = "starttime"
        data['endtime'] = "endtime"
        data['elapsedtime'] = "elapsedtime"
        data['status'] = "PASS"
        data['message'] = "msg"

        kobject._post.return_value = "test"
        self.assertIsNone(KWTelemetry.end_test(kobject, "test", attrs))
        kobject._post.assert_called_with(data)

    def test_kwtelemetry_start_keyword(self):
        """Test 'start_keyword' method of class KWTelemetry"""
        kobject = MagicMock(spec=KWTelemetry)

        attrs = {}
        attrs['type'] = "test"
        self.assertIsNone(KWTelemetry.start_keyword(kobject, "test", attrs))

        attrs['type'] = "KEYWORD"
        attrs['libname'] = "BUILTIN"
        self.assertIsNone(KWTelemetry.start_keyword(kobject, "test", attrs))

        attrs['libname'] = "lib"
        attrs['kwname'] = "kwname"
        attrs['args'] = "args"
        attrs['starttime'] = "starttime"

        data = {}
        data['name'] = "test"
        data['type'] = "KEYWORD"
        data['libname'] = "lib"
        data['kwname'] = "kwname"
        data['args'] = "args"
        data['starttime'] = "starttime"

        self.assertIsNone(KWTelemetry.start_keyword(kobject, "test", attrs))
        kobject._post.assert_called_with(data)

    def test_kwtelemetry_end_keyword(self):
        """Test 'end_keyword' method of class KWTelemetry"""
        kobject = MagicMock(spec=KWTelemetry)

        attrs = {}
        attrs['type'] = "test"
        self.assertIsNone(KWTelemetry.end_keyword(kobject, "test", attrs))

        attrs['type'] = "KEYWORD"
        attrs['libname'] = "BUILTIN"
        self.assertIsNone(KWTelemetry.end_keyword(kobject, "test", attrs))

        attrs['libname'] = "lib"
        attrs['kwname'] = "kwname"
        attrs['args'] = "args"
        attrs['starttime'] = "starttime"
        attrs['endtime'] = "endtime"
        attrs['elapsedtime'] = "elapsedtime"
        attrs['status'] = "PASS"

        data = {}
        data['name'] = "test"
        data['type'] = "KEYWORD"
        data['libname'] = "lib"
        data['kwname'] = "kwname"
        data['args'] = "args"
        data['starttime'] = "starttime"
        data['endtime'] = "endtime"
        data['elapsedtime'] = "elapsedtime"
        data['status'] = "PASS"

        self.assertIsNone(KWTelemetry.end_keyword(kobject, "test", attrs))
        kobject._post.assert_called_with(data)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestKWTelemetry)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
