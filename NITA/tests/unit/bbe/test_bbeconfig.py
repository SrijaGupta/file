"""
bbeconfig.py unit test
"""

import unittest
from mock import patch, MagicMock
from jnpr.toby.init.init import init
from jnpr.toby.bbe.bbeconfig import BBEConfig
from jnpr.toby.bbe.bbevar.bbevars import BBEVars, BBEVarDevice
import builtins
from jnpr.toby.exception.toby_exception import TobyException


class TestBbeConfig(unittest.TestCase):
    """
    test bbeconfig.py
    """
    @patch('time.sleep')
    @patch('re.search')
    #@patch('jnpr.toby.engines.config.config.config.CONFIG_SET', return_value=True)
    def test_configure_tomcat(self, patch_search, patch_sleep):
        builtins.t = MagicMock(spec=init)
        builtins.t.get_handle.return_value = MagicMock()
        bbecfg = BBEConfig()
        builtins.bbe = MagicMock(spec=BBEVars)
        builtins.bbe.get_devices.return_value = []
        builtins.t.get_handle.return_value.vc = False
        builtins.t.get_resource.return_value = {'system': {'primary': {'controllers': {'re0': {}, 're1': {}}}}}
#        self.assertEqual(bbecfg.configure_tomcat(), True)
        self.assertEqual(bbecfg.configure_tomcat(), None)
        builtins.bbe.get_devices.return_value = ['r0']
        patch_search.return_value = None
        self.assertEqual(bbecfg.configure_tomcat(), True)
        patch_search.return_value = True
        builtins.t.get_handle.return_value.execute_rpc.return_value.resp.findtext.side_effect = ['IP', 'not enabled',
                                                                                                'IP']
        try:
            bbecfg.configure_tomcat('r0')
        except:
            self.assertRaises(TobyException)

        builtins.t.get_handle.return_value.execute_rpc.return_value.resp.findtext.side_effect = ['IP', 'not enabled',
                                                                                                'Enhanced-IP',
                                                                                                 'not enabled']
        try:
            bbecfg.configure_tomcat('all')
        except:
            self.assertRaises(TobyException)
        builtins.t.get_handle.return_value.execute_rpc.return_value.resp.findtext.side_effect = ['Enhanced-IP',
                                                                                                 'not enabled',
                                                                                                 'Enhanced-IP',
                                                                                                 'enable',
                                                                                                 'Enhanced-IP',
                                                                                                 'enable']

        self.assertEqual(bbecfg.configure_tomcat(), True)
        builtins.t.get_handle.return_value.execute_rpc.return_value.resp.findtext.side_effect = ['Enhanced-IP',
                                                                                                 'not enabled',
                                                                                                 'enable',
                                                                                                 'enable',
                                                                                                 'Enhanced-IP',
                                                                                                 ]
        builtins.t.get_handle.return_value.get_current_controller_name.return_value = 're1'
        try:
            status = bbecfg.configure_tomcat()
        except:
            self.assertRaises(TobyException)
        else:
            self.assertEqual(status, True)

        builtins.t.get_handle.return_value.execute_rpc.return_value.resp.findtext.side_effect = None
        builtins.t.get_handle.return_value.reboot.side_effect = Exception('boom')
        try:
            bbecfg.configure_tomcat()
        except:
            self.assertRaises(TobyException)
        builtins.t.get_handle.return_value.reboot.side_effect = None
        builtins.t.get_handle.return_value.vc = True
        builtins.t.get_handle.return_value.set_current_controller.return_value = True
        builtins.t.get_handle.return_value.current_node.role = 'member0'
        try:
            bbecfg.configure_tomcat()
        except:
            self.assertRaises(TobyException)

        builtins.t.get_handle.return_value.current_node.role = 'member1'
        builtins.t.get_handle.return_value.pyez.return_value.resp.findtext.side_effect = ['Enhanced-IP', 'not enabled',
                                                                                          'Enhanced-IP', 'enable',
                                                                                          'Enhanced-IP', 'enable']
        self.assertEqual(bbecfg.configure_tomcat(), True)
        builtins.t.get_handle.return_value.pyez.return_value.resp.findtext.side_effect = None


if __name__ == '__main__':
    unittest.main()
