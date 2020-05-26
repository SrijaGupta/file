import sys

import unittest2 as unittest
from lxml import etree
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from jnpr.toby.hldcl.juniper.routing.mxvc import MxVc, re, time

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

@attr('unit')
class TestMxVc(unittest.TestCase):
    @patch('logging.FileHandler')
    def test_mxvc_init_failures(self, file_handler_mock):
        # No host provided
        self.assertRaises(Exception, MxVc)
        # host given in args and user name password not specified
        self.assertRaises(Exception, MxVc, 'device1')
        # dual_re and routing_engine set
        self.assertRaises(Exception, MxVc, host='device', dual_re=True,
                          routing_engine='master')

    @patch('time.sleep')
    @patch('re.search')
    def test_switch_re_master(self, re_patch, time_patch):
        mvc_obj = MagicMock(spec=MxVc)
        mvc_obj.dual_controller = False
        self.assertEqual(MxVc.switch_re_master(mvc_obj), True)

        mvc_obj.dual_controller = True
        mvc_obj.cli.return_value.response.return_value = True
        re_patch.return_value = False
        self.assertEqual(MxVc.switch_re_master(mvc_obj), True)

        match_obj = MagicMock()
        match_obj.group.return_value = 25
        re_patch.side_effect = [True, match_obj]
        mvc_obj.switch_re_master.return_value = True
        time_patch.return_value = True
        self.assertEqual(MxVc.switch_re_master(mvc_obj), True)


if __name__=='__main__':
    unittest.main()
