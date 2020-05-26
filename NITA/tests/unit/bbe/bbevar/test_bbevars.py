"""
bbevars.py unit test
"""

import unittest
from mock import patch, MagicMock
from jnpr.toby.init.init import init
from jnpr.toby.bbe.bbevar.bbevars import BBEVars, Vrf
from jnpr.toby.bbe.errors import BBEVarError, BBESubscriberError
from jnpr.toby.bbe.bbevar.interfaces import BBEVarInterface
from jnpr.toby.bbe.bbevar.devices import BBEVarDevice
from jnpr.toby.bbe.bbevar.subscribers import DHCPSubscribers, PPPoESubscribers
import builtins

builtins.t = MagicMock(spec=init)
builtins.t.log = MagicMock()

class TestBbeVars(unittest.TestCase):
    """
    test bbevars.py
    """
    def test_class_vrf(self):
        vrf = MagicMock(spec=Vrf)
        Vrf.__init__(vrf)
        self.assertEqual(vrf.cur, 0)
        return_value = Vrf.__iter__(vrf)
        self.assertEqual(return_value, vrf)
        return_log = Vrf.__repr__(vrf)
        self.assertIsInstance(return_log, str)
        try:
            Vrf.__next__(vrf)
        except:
            self.assertRaises(StopIteration)
        vrf.cur = 2
        vrf.max = 3
        Vrf.__next__(vrf)

    def test_class_bbevar(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        self.assertEqual(BBEVars.__init__(bbeclass), None)

    @patch('jnpr.toby.bbe.bbevar.bbevars.RTDHCPv6Server')
    @patch('jnpr.toby.bbe.bbevar.bbevars.RTDHCPv4Server')
    def test_initialization(self, patch_v4server, patch_v6server):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        # bbeclass._bbet = MagicMock(spec=init)
        patch_v4server.return_value = MagicMock()
        patch_v6server.return_value = MagicMock()
        bbeclass._rt_dhcps_ervers = {}
        bbeclass._init_devices = MagicMock()
        bbeclass._init_interfaces = MagicMock()
        bbeclass._init_connections = MagicMock()
        bbeclass._init_subscribers = MagicMock()
        bbeclass._generate_vrf = MagicMock()
        bbeclass.bbevar = {}
        bbevar = MagicMock()
        self.assertEqual(BBEVars.initialize(bbeclass, bbevar), None)

        try:
            self.assertEqual(BBEVars.initialize(bbeclass, bbevar), None)
        except:
            self.assertRaises(BBEVarError)
        bbevar = builtins.t
        self.assertEqual(BBEVars.initialize(bbeclass, bbevar), None)


    @patch('jnpr.toby.bbe.bbevar.bbevars.BBEVarDevice', return_value='device')
    def test_init_devices(self, patch_device):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        try:
            self.assertEqual(BBEVars._init_devices(bbeclass), None)
        except:
            self.assertRaises(BBEVarError)
        bbeclass._bbet = {'resources': {'r0': {'system': {'primary': {'controllers': {},
                                                              'mgt-ip': '10.9.1.123/21',
                                                              'name': 'test',
                                                              'osname': 'junos',
                                                              'dh': 'obj'}}}}}
        bbeclass._devices = {}
        self.assertEqual(BBEVars._init_devices(bbeclass), None)
        bbeclass._bbet = {'resources': {'r0': []}}
        self.assertEqual(BBEVars._init_devices(bbeclass), None)

    @patch('jnpr.toby.bbe.bbevar.bbevars.BBEVarInterface', return_value='interface')
    #@patch('jnpr.toby.bbe.bbevar.bbevars.BBEVarError')
    def test_init_interfaces(self, patch_interface):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        try:
            self.assertEqual(BBEVars._init_interfaces(bbeclass), None)
        except:
            self.assertRaises(BBEVarError)
        bbeclass._bbet = {'resources': []}
        try:
            self.assertEqual(BBEVars._init_interfaces(bbeclass), None)
        except:
            self.assertRaises(BBEVarError)
        bbeclass._bbet = {'resources':{'r0': {'interfaces': {'access0': {'link': 'access0'}}}}}
        bbeclass._interfaces = {}
        self.assertEqual(BBEVars._init_interfaces(bbeclass), None)
        bbeclass._bbet = {'resources': {'r0': {'interfaces': []}}}
        self.assertEqual(BBEVars._init_interfaces(bbeclass), None)


    #@patch('jnpr.toby.bbe.bbevar.bbevars.BBEVarError')
    def test_init_connections(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        try:
            self.assertEqual(BBEVars._init_connections(bbeclass), None)
        except:
            self.assertRaises(BBEVarError)
        bbeclass._bbet = {'resources': []}
        try:
            self.assertEqual(BBEVars._init_connections(bbeclass), None)
        except:
            self.assertRaises(BBEVarError)
        bbeclass._bbet = {'resources': {'r0': {'interfaces': {'access0': {'link': 'access0'},
                                                              'access1': {'link': 'access1'}}},
                                        'rt0': {'interfaces': {'access0':{'link': 'access0'}}}}}

        obj1 = MagicMock()
        obj1.interface_id = 'access0'
        bbeclass.get_interfaces.return_value = [obj1]
        bbeclass._connections = {}
        self.assertEqual(BBEVars._init_connections(bbeclass), None)
        bbeclass._bbet = {'resources': {'r0': {'interfaces': []}}}
        self.assertEqual(BBEVars._init_connections(bbeclass), None)
        
    @patch('jnpr.toby.bbe.bbevar.bbevars.FWASubscribers', return_value='fwa')
    @patch('jnpr.toby.bbe.bbevar.bbevars.PGWSubscribers', return_value='cups')
    @patch('jnpr.toby.bbe.bbevar.bbevars.CUPSSubscribers', return_value='cups')
    @patch('jnpr.toby.bbe.bbevar.bbevars.HAGSubscribers', return_value='hag')
    @patch('jnpr.toby.bbe.bbevar.bbevars.L2BSASubscribers', return_value='l2bsa')
    @patch('jnpr.toby.bbe.bbevar.bbevars.L2TPSubscribers', return_value='l2tp')
    @patch('jnpr.toby.bbe.bbevar.bbevars.PPPoESubscribers', return_value='pppoe')
    @patch('jnpr.toby.bbe.bbevar.bbevars.DHCPSubscribers', return_value='dhcp')
    #@patch('jnpr.toby.bbe.bbevar.bbevars.BBESubscriberError')
    def test_init_subscribers(self, patch_dhcp, patch_pppoe, patch_l2tp, patch_l2bsa, patch_hag,
                              patch_cups, patch_pgw, patch_fwa):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        try:
            self.assertEqual(BBEVars._init_subscribers(bbeclass), None)
        except:
            self.assertRaises(BBESubscriberError)
        bbeclass.get_devices.return_value = ['r0']
        self.assertEqual(BBEVars._init_subscribers(bbeclass), None)
        obj1 = MagicMock(spec=BBEVarDevice)
        obj1.device_os = 'junos'
        obj2 = MagicMock(spec=BBEVarDevice)
        obj2.device_os = 'cisco'
        bbeclass.get_devices.return_value = [obj1, obj2]
        try:
            self.assertEqual(BBEVars._init_subscribers(bbeclass), None)
        except:
            self.assertRaises(BBESubscriberError)
        obj3 = MagicMock(spec=BBEVarDevice)
        obj3.device_id = 'r0'
        obj4 = MagicMock(spec=BBEVarInterface)
        obj4.interface_config = {'subscribers': {'dhcp': [{'tag':'dhcp'}], 'pppoe': [{'tag':'pppoe'}],
                                                 'l2tp': [{'tag':'l2tp'}], 'l2bsa': [{'tag':'l2bsa'}],
                                                 'hag': [{'tag':'hag'}], 'pgw': [{'tag':'pgw'}],
                                                 'cups': [{'tag':'cups'}], 'fwa': [{'tag':'fwa'}]}}
        bbeclass.get_devices.side_effect = ([obj1, obj2], [obj3])
        bbeclass.get_interfaces.return_value = [obj4]
        bbeclass._subscribers = []
        self.assertEqual(BBEVars._init_subscribers(bbeclass), None)
        
        bbeclass.get_devices.side_effect = ([obj1, obj2], [])
        try:
            BBEVars._init_subscribers(bbeclass)
        except:
            self.assertRaises(BBESubscriberError)
        bbeclass.get_devices.side_effect = ([obj1, obj2], [obj3])
        obj6 = MagicMock(spec=BBEVarInterface)
        obj6.interface_config = {}
        bbeclass.get_interfaces.side_effect = ([obj4], [obj6])
        self.assertEqual(BBEVars._init_subscribers(bbeclass), None)
        bbeclass.get_devices.side_effect = None
        bbeclass.get_interfaces.side_effect = None
        obj5 = MagicMock()
        obj5.interface_config = ['test']
        bbeclass3 = MagicMock(spec=BBEVars)
        bbeclass3.log_tag = 'r0'
        bbeclass3.get_devices.return_value = [obj1, obj2]
        bbeclass3.get_interfaces.return_value = [obj5]

        bbeclass3._subscribers = []
        try:
            BBEVars._init_subscribers(bbeclass3)
        except:
            self.assertRaises(BBESubscriberError)


    def test_generate_vrf(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        self.assertEqual(BBEVars._generate_vrf(bbeclass), None)
        bbeclass2 = MagicMock(spec=BBEVars)
        bbeclass2.log_tag = 'BBEVAR'
        bbeclass2.bbevar = {'resources': {'r0': {'config': {'vrf': {}}}}}
        self.assertEqual(BBEVars._generate_vrf(bbeclass2), None)


    def test_get_connection(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        device = 'r0'
        interface = 'access0'
        bbeclass._connections = {('r0', 'access0'): 'dh'}
        self.assertIsInstance(BBEVars.get_connection(bbeclass, device, interface), object)


    def test_get_devices(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        bbeclass._devices = {'r0': 'object'}
        self.assertIsInstance(BBEVars.get_devices(bbeclass, 'r0'), list)
        self.assertIsInstance(BBEVars.get_devices(bbeclass, interfaces='access'), list)
        bbeclass._devices = {'r0': MagicMock(spec=BBEVarDevice)}
        self.assertIsInstance(BBEVars.get_devices(bbeclass, device_tags='access'), list)

    def test_get_interfaces(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        bbeclass._interfaces = {'access0':'obj1'}
        self.assertIsInstance(BBEVars.get_interfaces(bbeclass, device='r0'), list)
        bbeclass._interfaces = {'r0':{'access0': MagicMock(BBEVarInterface)}}
        self.assertIsInstance(BBEVars.get_interfaces(bbeclass, device='r0'), list)
        self.assertIsInstance(BBEVars.get_interfaces(bbeclass, device='r0', interfaces='access0'), list)
        self.assertIsInstance(BBEVars.get_interfaces(bbeclass, device='r0', id_only=True), list)


    def test_get_configured_subscriber_count(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        obj1 = MagicMock(DHCPSubscribers)
        obj1.count = 1000
        bbeclass.get_subscriber_handles.return_value = [obj1]
        self.assertIsInstance(BBEVars.get_configured_subscribers_count(bbeclass), int)

    def test_get_bbevar_by_keys(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        bbeclass.bbevar = MagicMock(init)
        self.assertIsInstance(BBEVars.get_bbevar_by_keys(bbeclass, []), object)
        self.assertEqual(BBEVars.get_bbevar_by_keys(bbeclass, 'string'), None)
        self.assertIsInstance(BBEVars.get_bbevar_by_keys(bbeclass, ['is_robot']), object)
        bbeclass.bbevar = {'t_dict': {'resources': {'r0': 'test'}}}
        self.assertIsInstance(BBEVars.get_bbevar_by_keys(bbeclass, ['t_dict', 'resources']), object)
        bbeclass.bbevar = {'t_dict': [{'resources': {'r0': 'test'}}, {'test': {}}]}
        self.assertIsInstance(BBEVars.get_bbevar_by_keys(bbeclass, ['t_dict', 'resources']), object)

    def test_get_rt_dhcp_server(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        bbeclass._rt_dhcps_ervers = {'ipv4':'server4'}
        self.assertIsInstance(BBEVars.get_rt_dhcp_server(bbeclass), object)

    def test_get_subscriber_handles(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        bbeclass._subscribers = ['a', 'b']
        self.assertIsInstance(BBEVars.get_subscriber_handles(bbeclass), list)

    def test_get_subscribers_call_rate(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        obj1 = MagicMock(DHCPSubscribers)
        obj1.clr = 100
        obj1.csr = 100
        obj1.family = 'dual'
        obj1.protocol = 'dhcp'
        obj1.outstanding = 200
        obj2 = MagicMock(PPPoESubscribers)
        obj2.clr = 100
        obj2.csr = 100
        obj2.protocol = 'pppoe'
        obj2.outstanding = 200
        bbeclass.get_subscriber_handles.return_value = [obj1]
        self.assertIsInstance(BBEVars.get_subscribers_call_rate(bbeclass, protocol='dhcp', family='ipv4'), dict)
        self.assertIsInstance(BBEVars.get_subscribers_call_rate(bbeclass, protocol='dhcp', family='ipv6'), dict)
        bbeclass.get_subscriber_handles.return_value = [obj2]
        self.assertIsInstance(BBEVars.get_subscribers_call_rate(bbeclass, protocol='pppoe'), dict)

    def test_get_vrfs(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        bbeclass.bbevar = MagicMock(spec=init)
        self.assertEqual(BBEVars.get_vrfs(bbeclass, device='r0'), None)

    def test_dict_merge(self):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        source = {'test':'1'}
        destination = {'test2':2}
        dict3 = {'test':'1', 'test2':2}
        self.assertEqual(BBEVars._dict_merge(bbeclass, source, destination), dict3)


    @patch('json.dump', return_value={})
    def test_dump(self, patch_json):
        bbeclass = MagicMock(spec=BBEVars)
        bbeclass.log_tag = 'BBEVAR'
        bbeclass._bbet = MagicMock(spec=init)
        bbeclass.bbevar = {'resource':{'test':'1'}}
        self.assertIsInstance(BBEVars.dump(bbeclass, 4), object)




if __name__ == '__main__':
    unittest.main()