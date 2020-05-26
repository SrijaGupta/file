import unittest2 as unittest
from mock import patch, MagicMock
from jnpr.toby.trafficgen.ixia.ixload import IxLoadHL
from jnpr.toby.trafficgen.ixia.ixload.IxUtils import IxUtils

class test_IxLoadHL(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.util = IxUtils()
    
    @classmethod
    def tearDownClass(self):
        rt_handle = MagicMock()
        rt_handle.log(level="INFO", message="tearDownClass: \n")
 
    def test_load_config(self):
        rt_handle = MagicMock()
        rt_handle.appserver = 'Appserver'
        rt_handle.log = MagicMock()
        rxf = "C:/Users/Administrator/Documents/Ixia/IxLoad/Repository/waseem_testing.rxf"
        # Exception case :
        result = IxLoadHL.load_config(rt_handle,rxf,"Dummy","Dummy")
        self.assertEqual(result['status'], 0)
        # try case :
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock(spec=IxUtils)
            result = IxLoadHL.load_config(rt_handle,rxf,"Dummy","Dummy")
            self.assertEqual(result['status'], 1)
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock(spec=IxUtils)
            result = IxLoadHL.load_config(rt_handle,rxf,"Dummy","Dummy","1")
            self.assertEqual(result['status'], 1)
            
    def test_disconnect(self):
        rt_handle = MagicMock()
        self.util.delete_session = MagicMock(return_value = '')
        connret = IxLoadHL.disconnect(rt_handle)
        self.assertEqual(connret, {'status': 1})
    
 
    def test_start_test(self):
        rt_handle = MagicMock()
        rt_handle.session_url = "dummy_url"
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock()
            Ixutil.get_test_current_state = MagicMock(side_effect = Exception("Negative case for disconnect API"))
            result = IxLoadHL.start_test(rt_handle)
            self.assertEqual(result['status'], 0)
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock(spec=IxUtils)
            Ixutil.get_test_current_state.return_value = "running"
            result = IxLoadHL.start_test(rt_handle)
            self.assertEqual(result['status'], 1)
            Ixutil.get_test_current_state.return_value = "dummy"
            result = IxLoadHL.start_test(rt_handle)
            self.assertEqual(result['status'], 0) 
    
    def test_stop_test(self):
        rt_handle = MagicMock()
        rt_handle.session_url = "dummy_url"
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock()
            Ixutil.get_test_current_state = MagicMock(side_effect = Exception("Negative case for disconnect API"))
            result = IxLoadHL.stop_test(rt_handle)
            self.assertEqual(result['status'], 0)
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock(spec=IxUtils)
            Ixutil.get_test_current_state.return_value = "unconfigured"
            result = IxLoadHL.stop_test(rt_handle)
            self.assertEqual(result['status'], 1)
            Ixutil.get_test_current_state.return_value = "dummy"
            result = IxLoadHL.stop_test(rt_handle)
            self.assertEqual(result['status'], 0)
    
    def test_get_stats(self):
        rt_handle = MagicMock()
        rt_handle.session_url = "dummy_url"
        stats_to_display =   {
                            #format: { stats_source : [stat name list] }
                            "HTTPClient": ["Transaction Rates"],
                            "HTTPServer": ["TCP Failures"]
                        }
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock()
            Ixutil.get_test_current_state = MagicMock(side_effect = Exception("Negative case for disconnect API"))
            result = IxLoadHL.get_stats(rt_handle, stats_to_display)
            self.assertEqual(result['status'], 0)
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock(spec=IxUtils)
            Ixutil.get_test_current_state.return_value = "running"
            result = IxLoadHL.get_stats(rt_handle, stats_to_display)
            self.assertEqual(result['status'], 1)
            Ixutil.get_test_current_state.return_value = "dummy"
            result = IxLoadHL.get_stats(rt_handle, stats_to_display)
            self.assertEqual(result['status'], 0)
    
    def test_add_chassis(self):
        rt_handle = MagicMock()
        rt_handle.session_url = "dummy_url"
        chassis_list = "dummy"
        portlist_per_community =    {
                                        "Traffic1@Network1" : [(1,5,1)]
                                    }
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock()
            Ixutil.clear_chassis_list = MagicMock(side_effect = Exception("Negative case for disconnect API"))
            result = IxLoadHL.add_chassis(rt_handle, chassis_list, portlist_per_community)
            self.assertEqual(result['status'], 0)
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock(spec=IxUtils)
            Ixutil.clear_chassis_list.return_value = "running"
            result = IxLoadHL.add_chassis(rt_handle, chassis_list, portlist_per_community)
            self.assertEqual(result['status'], 1)

    def test_emulation_http(self):
        rt_handle = MagicMock()
        data = MagicMock(mode = 'create')
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock(spec=IxUtils)
            Ixutil.emulation_protocol.return_value= "\dummy"
            a = {'mode':'create'}
            result = IxLoadHL.emulation_http(rt_handle=rt_handle, network_name="dummy",  **a)
            self.assertEqual(result['status'], 1)

    def test_emulation_ftp(self):
        rt_handle = MagicMock()
        data = MagicMock(mode = 'create')
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock(spec=IxUtils)
            Ixutil.emulation_protocol.return_value= "\dummy"
            a = {'mode':'create'}
            result = IxLoadHL.emulation_ftp(rt_handle=rt_handle, network_name="dummy",  **a)
            self.assertEqual(result['status'], 1)

    def test_emulation_dns(self):
        rt_handle = MagicMock()
        data = MagicMock(mode = 'create')
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock(spec=IxUtils)
            Ixutil.emulation_protocol.return_value= "\dummy"
            a = {'mode':'create'}
            result = IxLoadHL.emulation_dns(rt_handle=rt_handle, network_name="dummy",  **a)
            self.assertEqual(result['status'], 1)

    def test_network_config(self):
        rt_handle = MagicMock()
        with patch('jnpr.toby.trafficgen.ixia.ixload.IxLoadHL.IX_UTIL') as Ixutil:
            Ixutil.return_value = MagicMock(spec=IxUtils)
            Ixutil.get_args.return_value = [{'dummy':'dummy'}, {'no_of_agent':'2', 'network_name':'dummy'}]
            a = {'network_name':'dummy','eth_dummy':'dummy','ip_dummy':'dummy','mac_dummy':'dummy','vlan_dummy':'dummy', 'er_dummy':'dummy','er_mode':'create'}
            result = IxLoadHL.network_config(rt_handle=rt_handle, **a)
            self.assertEqual(result['status'], 0)
            
        
        
if __name__ == '__main__':
    unittest.main()

