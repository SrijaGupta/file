import unittest2 as unittest
from mock import patch, MagicMock
from jnpr.toby.hldcl.trafficgen.spirent.elevate import Elevate

class TestElevate(unittest.TestCase):
    @patch('jnpr.toby.hldcl.trafficgen.spirent.elevate.os.path.dirname')
    @patch('jnpr.toby.hldcl.trafficgen.spirent.elevate.credentials.__file__', return_value='Dummy_file')
    @patch('jnpr.toby.hldcl.trafficgen.spirent.elevate.os.path.join')
    @patch('jnpr.toby.hldcl.trafficgen.spirent.elevate.yaml.safe_load')
    @patch('jnpr.toby.hldcl.trafficgen.spirent.elevate.get_log_dir', return_value='some')
    @patch('jnpr.toby.hldcl.trafficgen.spirent.elevate.atexit.register')
    def test__init__(self, atexit_patch, get_log_patch, yaml_load, os_patch, cred_patch, dir_patch):
        yaml_load.return_value = {'elevate-lib-path':"dummy"}
        mobject = MagicMock(spec=Elevate)
        self.assertRaises(Exception, Elevate.__init__, mobject, chassis='something')
        self.assertRaises(Exception, Elevate.__init__, mobject)
        self.assertRaises(Exception, Elevate.__init__, mobject, chassis='')
        system = {'system':{'primary':{'name':'dummy','controllers':{'re0':{'osname':'junos','mgt-ip':'0.0.0.0'}},'api-path':'somepath', 'model':'mx'}}}
        self.assertRaises(Exception, Elevate.__init__, mobject, system_data=system)

    def test_add_interfaces(self):
        mobject = MagicMock(spec=Elevate)
        Elevate.add_interfaces(mobject, 'something')

    def test_add_intf_to_port_map(self):
        mobject = MagicMock(spec=Elevate)
        Elevate.add_intf_to_port_map(mobject, 'something')

if __name__ == '__main__':
    unittest.main()
