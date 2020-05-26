"""UT for the module jnpr.toby.hldcl.juniper.junipernode"""

import unittest2 as unittest
from mock import patch, MagicMock

from jnpr.toby.hldcl.juniper.junipernode import JuniperNode

class TestJuniperNode(unittest.TestCase):
    """UT for JuniperNode"""
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
    @patch('jnpr.toby.hldcl.juniper.junipernode.Node.__init__')
    def test_junipernode_init(self, sup_init_patch):
        """Test '__init__' method of class JuniperNode"""
        self.assertIsInstance(JuniperNode(node_data='test'), JuniperNode)
        self.assertTrue(sup_init_patch.called)

    def test_junipernode_reboot(self):
        """Test 'reboot' method of class JuniperNode"""
        jobject = MagicMock(spec=JuniperNode)
        jobject.current_controller = MagicMock()
        jobject.current_controller.reboot.return_value = "test"
        self.assertEqual(JuniperNode.reboot(jobject), "test")

        jobject._set_current_controller.return_value = True
        jobject.controllers = {'re0':MagicMock(), 're1':MagicMock()}
        jobject.controllers['re0'].reboot.return_value = True
        jobject.controllers['re1'].reboot.return_value = True
        self.assertTrue(JuniperNode.reboot(jobject, all=True))

        jobject.controllers['re1'].reboot.return_value = False
        self.assertFalse(JuniperNode.reboot(jobject, all=True))

    def test_junipernode_is_node_master(self):
        """Test 'is_node_master' method of class JuniperNode"""
        jobject = MagicMock(spec=JuniperNode)
        jobject.current_controller = MagicMock()

        jobject.current_controller.is_master.return_value = True
        self.assertTrue(JuniperNode.is_node_master(jobject))

        jobject.current_controller.is_master.return_value = False
        self.assertFalse(JuniperNode.is_node_master(jobject))

    def test_junipernode_detect_core(self):
        """Test 'detect_core' method of class JuniperNode"""
        jobject = MagicMock(spec=JuniperNode)
        jobject.controllers = {'test':MagicMock()}

        tcobject = MagicMock()
        jobject.controllers['test'].get_testcase_name.return_value = None

        jobject.controllers['test'].detect_core.return_value = 1
        self.assertEqual(JuniperNode.detect_core(jobject), 1)

        self.assertEqual(JuniperNode.detect_core(jobject, core_path="test"), 1)
        jobject.controllers['test'].detect_core.assert_called_with(core_path="test", system_name=None, re1_hostname=None, command=None)

    def test_junipernode_save_current_config(self):
        jobject = MagicMock(spec=JuniperNode)
        jobject.controllers = {'test':MagicMock()}
        jobject.controllers['test'].save_config.return_value = 1
        self.assertEqual(JuniperNode.save_current_config(jobject,file=''), True) 

    def test_junipernode_load_saved_config(self):
        jobject = MagicMock(spec=JuniperNode)
        jobject.controllers = {'test':MagicMock()}
        jobject.controllers['test'].is_master.return_value = True
        jobject.controllers['test'].load_config.return_value = 1
        self.assertEqual(JuniperNode.load_saved_config(jobject,file=''), True)
 
        jobject.controllers['test'].is_master.return_value = False
        self.assertEqual(JuniperNode.load_saved_config(jobject,file=''), True)



if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestJuniperNode)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
