import unittest2 as unittest
from mock import MagicMock
from mock import patch
import os
from jnpr.toby.utils.linux.l4_session_traffic import l4_session_traffic
from jnpr.toby.utils.linux.l4_session import L4_Session


class UnitTest(unittest.TestCase):
    l4_so = MagicMock(spec=L4_Session)
    l4_so.dh = MagicMock()
    session_args = dict(server=l4_so, client=l4_so, server_ip='10.10.10.10',
                        client_ip='10.10.10.10', protocol='tcp', server_port='80', client_port='80')
    template_file = os.path.join(os.path.dirname(__file__), 'l4_session_traffic_unit_test.yaml')

    def test_l4_session_traffic(self):
        traffic_args = dict(xyz='abc')
        self.assertEqual(
            l4_session_traffic(template_file=self.template_file, template='unittest_traffic',
                               session_args=self.session_args, traffic_args=traffic_args), True)

    def test_exception_device_knobs(self):
        self.assertRaises(Exception, l4_session_traffic, template_file=self.template_file,
                          template='unittest_device_knobs', session_args=self.session_args)

    def test_exception_action_knobs(self):
        self.assertRaises(Exception, l4_session_traffic, template_file=self.template_file,
                          template='unittest_action_knobs', session_args=self.session_args)

    def test_exception_server_fail(self):
        self.l4_so.start = MagicMock(return_value=0)
        self.assertRaises(Exception, l4_session_traffic, template_file=self.template_file,
                          template='unittest_server_fail', session_args=self.session_args)
        self.l4_so.start = MagicMock(return_value=1)

    def test_exception_client_fail(self):
        self.l4_so.start = MagicMock(return_value=0)
        self.assertRaises(Exception, l4_session_traffic, template_file=self.template_file,
                          template='unittest_client_fail', session_args=self.session_args)
        self.l4_so.start = MagicMock(return_value=1)

if __name__ == '__main__':
    unittest.main()
