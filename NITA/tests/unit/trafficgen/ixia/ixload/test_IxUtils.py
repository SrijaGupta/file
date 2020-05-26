import unittest2 as unittest
from mock import patch, MagicMock
from jnpr.toby.trafficgen.ixia.ixload.IxUtils import IxUtils


class test_IxUtils(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.util = IxUtils()
    
    @classmethod
    def tearDownClass(self):
        rt_handle = MagicMock()
        rt_handle.log(level="INFO", message="tearDownClass: \n")
    
    def test_strip_api_and_version_from_url(self):
        url = "/api/v0"
        connret = self.util.strip_api_and_version_from_url(url)
        self.assertEqual(connret, '')

    def test_perform_generic_operation(self):
        url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        self.util.wait_for_action_to_finish= MagicMock(return_value = "dummy")
        connret = self.util.perform_generic_operation(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
    
    def test_perform_generic_operation_negative(self):
        url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 0, text = "dummy")
        rt_handle.invoke = MagicMock(return_value = mock)
        self.util.wait_for_action_to_finish= MagicMock(return_value = "dummy")
        with self.assertRaises(Exception) as e:
            connret = self.util.perform_generic_operation(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(e.exception, Exception)

    def test_get_test_current_state(self):
        session_url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(currentState = "Unconfigured")
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.get_test_current_state(rt_handle=rt_handle, session_url=session_url)
        self.assertEqual(connret, "Unconfigured")
    def test_get_test_current_state1(self):
        session_url = "dummy"
        payload_dict = {'dummy':'dummy'}
        #ixload.get_arg =  self.util.strip_api_and_version_from_url(url)
        rt_handle = MagicMock()
        mock = MagicMock(currentState = "running")
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.get_test_current_state(rt_handle=rt_handle, session_url=session_url)
        self.assertEqual(connret, "running")

    def test_load_repository(self):
        session_url = "dummy"
        rxf_file_path = "dummy"
        url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        self.util.wait_for_action_to_finish= MagicMock(return_value = "dummy")
        connret = self.util.perform_generic_operation(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        connret = self.util.load_repository(rt_handle=rt_handle, session_url=session_url, rxf_file_path=rxf_file_path)
        self.assertIsNone(connret)

    def test_perform_generic_patch(self):
        url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.perform_generic_patch(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
    
    def test_add_chassis_list(self):
        session_url = "dummy"
        chassis_listl = ["dummy"]
        url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok =1, refresh_connection_url = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        self.util.wait_for_action_to_finish= MagicMock(return_value = "dummy")
        self.util.perform_generic_post= MagicMock(return_value = '1')
        connret = self.util.perform_generic_operation(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        connret = self.util.add_chassis_list(rt_handle=rt_handle, session_url=session_url, chassis_listl=chassis_listl)
        self.assertEqual(connret, 'dummy/ixload/chassisChain/chassisList/1/operations/refreshConnection')

    def test_assign_ports(self):
        session_url = "dummy"
        port_list_per_community = {"dummy" :["1/1/1"]}
        url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok =1, name = "dummy", refresh_connection_url = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.perform_generic_patch(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        rt_handle.invoke = MagicMock(return_value = mock)
        self.util.perform_generic_post= MagicMock(return_value = '1')
        connret = self.util.assign_ports(rt_handle=rt_handle, session_url=session_url, port_list_per_community=port_list_per_community)
        self.assertEqual(connret, [])
    
    def test_change_agent_configs(self):
        session_url = "dummy"
        port_list_per_community = {"dummy" :["1/1/1"]}
        url = "dummy"
        agent_name = "HTTP Client"
        value_dict = {'UserObjective':'SimulatedUsers'}
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok =1, name = "HTTP Client", refresh_connection_url = 1, objectID = "1", community_list={'objectID':"1"})
        rt_handle.invoke = MagicMock(return_value = mock)
        rt_handle.invoke = MagicMock(return_value = mock)
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.perform_generic_patch(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        connret = self.util.change_agent_configs(rt_handle=rt_handle, session_url=session_url, agent_name=agent_name, value_dict= value_dict)
        self.assertIsNone(connret)

    def test_change_objective(self):
        session_url = "dummy"
        port_list_per_community = {"dummy" :["1/1/1"]}
        url = "dummy"
        agent_name = "HTTP Client"
        value_dict = {'UserObjective':'SimulatedUsers'}
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok =1, name = "HTTP Client", refresh_connection_url = 1, objectID = "1")
        rt_handle.invoke = MagicMock(return_value = mock)
        rt_handle.invoke = MagicMock(return_value = mock)
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.perform_generic_patch(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        connret = self.util.change_objective(rt_handle=rt_handle, session_url=session_url, agent_name=agent_name, value_dict= value_dict)
        self.assertIsNone(connret)


    def test_save_rxf(self):
        session_url = "dummy"
        rxf_file_path = "dummy"
        url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        self.util.wait_for_action_to_finish= MagicMock(return_value = "dummy")
        connret =  self.util.perform_generic_operation(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        connret =  self.util.save_rxf(rt_handle=rt_handle, session_url=session_url, rxf_file_path=rxf_file_path)
        self.assertIsNone(connret)
    
    def test_run_test(self):
        session_url = "dummy"
        rxf_file_path = "dummy"
        url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        self.util.wait_for_action_to_finish= MagicMock(return_value = "dummy")
        connret =  self.util.perform_generic_operation(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        connret =  self.util.perform_generic_operation(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        connret =  self.util.run_test(rt_handle=rt_handle, session_url=session_url)
        self.assertIsInstance(connret, type(mock))
    
    def test_stop_traffic(self):
        session_url = "dummy"
        rxf_file_path = "dummy"
        url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        self.util.wait_for_action_to_finish= MagicMock(return_value = "dummy")
        connret =  self.util.perform_generic_operation(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        connret =  self.util.stop_traffic(rt_handle=rt_handle, session_url=session_url)
        self.assertIsInstance(connret, type(mock))

    def test_clear_chassis_list(self):
        list_url = "dummy"
        session_url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        connret =  self.util.clear_chassis_list(rt_handle=rt_handle, session_url=session_url)
        self.assertIsNone(connret)
    
    def test_perform_generic_delete(self):
        list_url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.perform_generic_delete(rt_handle=rt_handle, list_url=list_url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
    
    def test_delete_session(self):
        session_url= 'dummy'
        list_url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.perform_generic_delete(rt_handle=rt_handle, list_url=list_url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        connret = self.util.delete_session(rt_handle, session_url)
        self.assertIsNone(connret)

    def test_clear_agents_command_list(self):
        session_url= 'dummy'
        agent_name_list = 'dummy'
        list_url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        self.util.get_command_list_url_for_agent_name = MagicMock(return_value = mock)
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.perform_generic_delete(rt_handle=rt_handle, list_url=list_url, payload_dict=payload_dict)
        self.assertIsInstance(connret, type(mock))
        connret = self.util.clear_agents_command_list(rt_handle, session_url, agent_name_list)
        self.assertIsNone(connret)
    def test_get_objective_type(self):
        session_url = "simulatedUsers"
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1, activeRole = "Client")
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.get_objective_type(rt_handle, session_url)
        self.assertIsNone(connret)
        
    def test_perform_generic_delete_negative(self):
        list_url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 0, text = "dummy")
        rt_handle.invoke = MagicMock(return_value = mock)
        with self.assertRaises(Exception) as e:
            connret = self.util.perform_generic_delete(rt_handle=rt_handle, list_url=list_url, payload_dict=payload_dict)
        self.assertIsInstance(e.exception, Exception)
    
    def test_perform_generic_post(self):
        list_url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        headers = {'location':'/1'}
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.perform_generic_post(rt_handle-rt_handle, list_url=list_url, payload_dict=payload_dict)
        self.assertEqual(connret, '1')
        
    def test_perform_generic_patch_negative(self):
        url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 0)
        rt_handle.invoke = MagicMock(return_value = mock)
        with self.assertRaises(Exception) as e:
            connret = self.util.perform_generic_patch(rt_handle=rt_handle, url=url, payload_dict=payload_dict)
        self.assertIsInstance(e.exception, Exception)


    def test_wait_for_action_to_finish(self):
        reply_obj = "dummy"
        action_url = "dummy/api/v0/ixload/chassisChain/chassisList/1/operations/refreshConnection"
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        rt_handle.invoke = MagicMock(return_value = mock)
        connret = self.util.wait_for_action_to_finish(rt_handle, reply_obj, action_url)
        self.assertEqual(connret, 'dummy')
        
    @patch('ftplib.FTP')
    def test_ftp_save_config(self, patch1):
        server = "dummy"
        username = "dummy"
        password = "dummy"
        filename = "dummy"
        connret = self.util.ftp_save_config(server, username, password, filename)
        self.assertEqual(connret, 1)

    def test_ftp_save_config1(self):
        server = "dummy"
        username = "dummy"
        password = "dummy"
        filename = "dummy"
        with self.assertRaises(Exception) as e:
            connret = self.util.ftp_save_config(server, username, password, filename)
        self.assertIsInstance(e.exception, Exception)

    @patch('jnpr.toby.trafficgen.ixia.ixload.IxUtils.IxUtils.perform_generic_patch')
    def test_configure_ethernet(self, generic_patch):
        rt_handle = MagicMock()
        rt_handle.invoke = MagicMock(return_value=[{'name':'dummy','objectID':'dummy'}])
        self.util.configure_ethernet(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'medium':'some','other':'dummy'})
        rt_handle.invoke = MagicMock(return_value=[{'name':'Junk','objectID':'dummy'}])
        self.util.configure_ethernet(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'medium':'some','other':'dummy'})
        rt_handle.invoke = MagicMock(return_value=[{'name':'dummy','objectID':'dummy'}])
        self.util.configure_ethernet(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'other':'dummy'})
    
    @patch('jnpr.toby.trafficgen.ixia.ixload.IxUtils.IxUtils.perform_generic_patch')
    def test_configure_mac(self, generic_patch):
        rt_handle = MagicMock()
        rt_handle.invoke = MagicMock(return_value=[{'name':'dummy','objectID':'dummy'}])
        self.util.configure_mac(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'medium':'some','other':'dummy'})
        rt_handle.invoke = MagicMock(return_value=[{'name':'Junk','objectID':'dummy'}])
        self.util.configure_mac(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'medium':'some','other':'dummy'})
        rt_handle.invoke = MagicMock(return_value=[{'name':'dummy','objectID':'dummy'}])
        self.util.configure_mac(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'other':'dummy'})

    @patch('jnpr.toby.trafficgen.ixia.ixload.IxUtils.IxUtils.perform_generic_patch')
    def test_configure_vlan(self, generic_patch):
        rt_handle = MagicMock()
        rt_handle.invoke = MagicMock(return_value=[{'name':'dummy','objectID':'dummy'}])
        self.util.configure_vlan(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'medium':'some','other':'dummy'})
        rt_handle.invoke = MagicMock(return_value=[{'name':'Junk','objectID':'dummy'}])
        self.util.configure_vlan(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'medium':'some','other':'dummy'})
        rt_handle.invoke = MagicMock(return_value=[{'name':'dummy','objectID':'dummy'}])
        self.util.configure_vlan(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'other':'dummy'})

    @patch('jnpr.toby.trafficgen.ixia.ixload.IxUtils.IxUtils.perform_generic_patch')
    def test_configure_ip(self, generic_patch):
        rt_handle = MagicMock()
        rt_handle.invoke = MagicMock(return_value=[{'name':'dummy','objectID':'dummy', 'itemType':"EmulatedRouterPlugin"}])
        self.util.configure_ip(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'medium':'some','other':'dummy'})
        rt_handle.invoke = MagicMock(return_value=[{'name':'dummy','objectID':'dummy', 'itemType':"EmulatedRouterPlugin"}])
        self.util.configure_ip(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'medium':'some','other':'dummy'})
        rt_handle.invoke = MagicMock(return_value=[{'name':'dummy','objectID':'dummy', 'itemType':"EmulatedRouterPlugin2"}])
        self.util.configure_ip(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'other':'dummy'})
        rt_handle.invoke = MagicMock(return_value=[{'name':'dummy','objectID':'dummy','itemType':"EmulatedRouterPlugin"}])
        self.util.configure_ip(rt_handle=rt_handle, session_url='dummyUrl', network_name='dummy', kwargs={'other':'dummy'})
    
    def test_emulation_protocol(self):
        rt_handle = MagicMock()
        session_url= 'dummy'
        list_url = "dummy"
        payload_dict = {'dummy':'dummy'}
        rt_handle = MagicMock()
        mock = MagicMock(ok = 1)
        data = MagicMock(mode = 'create')
        a = {'mode':'create', 'role':'client'}
        self.util.add_communities(rt_handle=rt_handle, session_url='dummyUrl', community_option_list='dummy')
        self.util.get_mandatory_args({'mode':'create', 'role':'client'})
        self.util.add_activities_updated(rt_handle=rt_handle, session_url='dummyUrl', activity_list_per_community=a, community_list={'objectID':'dummy'})
        result = self.util.emulation_protocol(rt_handle=rt_handle, session_url='dummyUrl', protocol="FTP", network_name="dummy", method="dummy", kwargs={'mode':'create', 'no_of_agent':1, 'role':'client', 'agent_name':'httpclient', 'enableConstraint':'dummy', 'commandTimeout':0, "commandType":"{Get}", "userName":"root", "destination":"server_FTPServer1:21"})
        self.assertIsNone(result)
        result = self.util.emulation_protocol(rt_handle=rt_handle, session_url='dummyUrl', protocol="FTP", network_name="dummy", method="dummy", kwargs={'mode':'modify', 'no_of_agent':1, 'role':'client', 'agent_name':'httpclient', 'enableConstraint':'dummy', 'commandTimeout':0, "commandType":"{Get}", "userName":"root", "destination":"server_FTPServer1:21"})
        self.assertIsNone(result)
        result = self.util.emulation_protocol(rt_handle=rt_handle, session_url='dummyUrl', protocol="FTP", network_name="dummy", method="dummy", kwargs={'mode':'add_command', 'no_of_agent':1, 'role':'client', 'agent_name':'httpclient', 'enableConstraint':'dummy', 'commandTimeout':0, "commandType":"{Get}", "userName":"root", "destination":"server_FTPServer1:21"})
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
