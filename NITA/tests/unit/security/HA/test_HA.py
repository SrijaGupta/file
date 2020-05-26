#!/usr/bin/env python3
import unittest
import time
from mock import Mock, patch
from jnpr.toby.security.HA.HA import HA
from jnpr.toby.hldcl.juniper.security.srxsystem import SrxSystem
from jnpr.toby.hldcl.juniper.security.srx import Srx
from jxmlease import XMLCDATANode
from lxml import etree
#import pdb; pdb.set_trace()

class TestHA(unittest.TestCase):
    def setUp(self):
        self.device = Mock(spec=SrxSystem)
        self.device.log = Mock()
        self.ha = HA()
        self.ha2 = HA(device=self.device)

    def test_get_ha_node_name(self):
        mock_x1 = Mock(spec=XMLCDATANode)
        mock_x1.get_cdata.return_value = "primary"
        mock_x2 = Mock(spec=XMLCDATANode)
        mock_x2.get_cdata.return_value = "secondary"
        self.device.ha_status.return_value = {"node0":{"status":mock_x1},"node1":{"status":mock_x2}}
        self.assertEqual(self.ha.get_ha_node_name(device=self.device, rg="1", status="primary"), "node0")
        self.assertEqual(self.ha.get_ha_node_name(device=self.device, rg="1", status="secondary"), "node1")
        self.assertFalse(self.ha.get_ha_node_name(device=self.device, rg="1", status="secondary-hold"))
        self.assertRaises(Exception, self.ha.get_ha_node_name, rg="1", status="primary")
        self.assertEqual(self.ha2.get_ha_node_name(rg="1", status="primary"), "node0")

    def test_get_ha_node_status(self):
        mock_x1 = Mock(spec=XMLCDATANode)
        mock_x1.get_cdata.return_value = "primary"
        mock_x2 = Mock(spec=XMLCDATANode)
        mock_x2.get_cdata.return_value = "secondary"
        self.device.ha_status.return_value = {"node0":{"status":mock_x1},"node1":{"status":mock_x2}}
        self.assertEqual(self.ha.get_ha_node_status(device=self.device, rg="1", node="node0"), "primary")
        self.assertEqual(self.ha.get_ha_node_status(device=self.device, rg="1", node="node1"), "secondary")
        self.assertRaises(Exception, self.ha.get_ha_node_status, rg="1", node="node0")
        self.assertRaises(Exception, self.ha.get_ha_node_status, device=self.device, rg="1", node="0")
        self.assertEqual(self.ha2.get_ha_node_status(rg="1", node="node0"), "primary")

    def test_get_ha_status(self):
        mock_status_0 = Mock(spec=XMLCDATANode)
        mock_status_0.get_cdata.return_value = "primary"
        mock_status_1 = Mock(spec=XMLCDATANode)
        mock_status_1.get_cdata.return_value = "secondary"
        mock_priority_0 = Mock(spec=XMLCDATANode)
        mock_priority_0.get_cdata.return_value = "100"
        mock_priority_1 = Mock(spec=XMLCDATANode)
        mock_priority_1.get_cdata.return_value = "200"
        mock_preempt_0 = Mock(spec=XMLCDATANode)
        mock_preempt_0.get_cdata.return_value = "no"
        mock_preempt_1 = Mock(spec=XMLCDATANode)
        mock_preempt_1.get_cdata.return_value = "no"
        mock_name_0 = Mock(spec=XMLCDATANode)
        mock_name_0.get_cdata.return_value = "node0"
        mock_name_1 = Mock(spec=XMLCDATANode)
        mock_name_1.get_cdata.return_value = "node1"
        mock_failures_0 = Mock(spec=XMLCDATANode)
        mock_failures_0.get_cdata.return_value = "None"
        mock_failures_1 = Mock(spec=XMLCDATANode)
        mock_failures_1.get_cdata.return_value = "None"
        mock_failover_0 = Mock(spec=XMLCDATANode)
        mock_failover_0.get_cdata.return_value = "no"
        mock_failover_1 = Mock(spec=XMLCDATANode)
        mock_failover_1.get_cdata.return_value = "no"
        expect_status = {
	     'node0': {'failover-mode': 'no',
		       'monitor-failures': 'None',
		       'name': 'node0',
		       'preempt': 'no',
		       'priority': '100',
		       'status': 'primary'},
	     'node1': {'failover-mode': 'no',
		       'monitor-failures': 'None',
		       'name': 'node1',
		       'preempt': 'no',
		       'priority': '200',
		       'status': 'secondary'}}
        self.device.ha_status.return_value = {
		"node0":{"status":mock_status_0,
			"priority":mock_priority_0,
			"preempt":mock_preempt_0,
			"name":mock_name_0,
			"monitor-failures":mock_failures_0,
			"failover-mode":mock_failover_0,
			},
		"node1":{"status":mock_status_1,
			"priority":mock_priority_1,
			"preempt":mock_preempt_1,
			"name":mock_name_1,
			"monitor-failures":mock_failures_1,
			"failover-mode":mock_failover_1,
			}
		}
        self.assertEqual(self.ha.get_ha_status(device=self.device, rg="1"), expect_status)
        self.assertRaises(Exception, self.ha.get_ha_status, rg="1")
        self.assertEqual(self.ha2.get_ha_status(rg="1"), expect_status)

    @patch("time.sleep", return_value=None)
    def test_get_ha_healthy_status(self, mock_time):
        healthy_status = {
	     'node0': {'failover-mode': 'no',
		       'monitor-failures': 'None',
		       'name': 'node0',
		       'preempt': 'no',
		       'priority': '100',
		       'status': 'primary'},
	     'node1': {'failover-mode': 'no',
		       'monitor-failures': 'None',
		       'name': 'node1',
		       'preempt': 'no',
		       'priority': '200',
		       'status': 'secondary'}}
        priority_zero_status = {
	     'node0': {'failover-mode': 'no',
		       'monitor-failures': 'None',
		       'name': 'node0',
		       'preempt': 'no',
		       'priority': '0',
		       'status': 'primary'},
	     'node1': {'failover-mode': 'no',
		       'monitor-failures': 'None',
		       'name': 'node1',
		       'preempt': 'no',
		       'priority': '200',
		       'status': 'secondary'}}
        self.assertRaises(Exception, self.ha.get_ha_healthy_status, rg="0")
        self.ha.get_ha_status = Mock(return_value=healthy_status)
        self.ha2.get_ha_status = Mock(return_value=priority_zero_status)
        self.assertEqual(self.ha.get_ha_healthy_status(device=self.device, rg="0", retry=1, interval=15), healthy_status)
        self.assertFalse(self.ha2.get_ha_healthy_status(rg="0", retry=1, interval=15))
        # priority zero
        self.assertEqual(self.ha2.get_ha_healthy_status(device=self.device, rg="0", retry=1, interval=15, priority_zero=True), priority_zero_status)
        priority_zero_status['node0']['status'] = "disabled"
        self.assertFalse(self.ha2.get_ha_healthy_status(rg="0", retry=1, interval=15, priority_zero=True))
    
    def test_get_ha_rgs(self):
        self.device.get_rpc_equivalent = Mock(return_value="</>")
        rg0 = Mock(spec=etree._Element)
        rg0.text = "0"
        rg1 = Mock(spec=etree._Element)
        rg1.text = "1"
        mock_element = Mock(spec=etree._Element)
        mock_element.findall.side_effect = [[rg0, rg1],[]]
        self.device.execute_rpc().response.return_value = mock_element
        self.assertRaises(Exception, self.ha.get_ha_rgs)
        self.assertEqual(self.ha.get_ha_rgs(device=self.device), ["0","1"])
        self.assertFalse(self.ha2.get_ha_rgs())

    def test_execute_cli_on_node(self):
        self.device.node0 = Mock(spec=Srx)
        self.device.node1 = Mock(spec=Srx)
        self.device.node0.cli().response.return_value = "test_0"
        self.assertEqual(self.ha.execute_cli_on_node(device=self.device, node="node0"), "test_0")
        self.device.node1.cli().response.return_value = "test_1"
        self.assertEqual(self.ha.execute_cli_on_node(device=self.device, node="node1"), "test_1")

        self.assertRaises(Exception, self.ha.execute_cli_on_node, device=self.device, node="")
        
        self.device.node0.cli().response.return_value = False
        self.assertRaises(Exception, self.ha.execute_cli_on_node, device=self.device, node="node0")

        self.assertRaises(Exception, self.ha.execute_cli_on_node, node="")
        self.device.node0.cli().response.return_value = "test_3"
        self.assertEqual(self.ha2.execute_cli_on_node(node="node0"), "test_3")

    def test_execute_shell_on_node(self):
        self.device.node0 = Mock(spec=Srx)
        self.device.node1 = Mock(spec=Srx)
        self.device.node0.shell().response.return_value = "test_0"
        self.assertEqual(self.ha.execute_shell_on_node(device=self.device, node="node0"), "test_0")
        self.device.node1.shell().response.return_value = "test_1"
        self.assertEqual(self.ha.execute_shell_on_node(device=self.device, node="node1"), "test_1")

        self.assertRaises(Exception, self.ha.execute_shell_on_node, device=self.device, node="")
        
        self.device.node0.shell().response.return_value = False
        self.assertRaises(Exception, self.ha.execute_shell_on_node, device=self.device, node="node0")

        self.assertRaises(Exception, self.ha.execute_shell_on_node, node="")
        self.device.node0.shell().response.return_value = "test_3"
        self.assertEqual(self.ha2.execute_shell_on_node(node="node0"), "test_3")

    def test_do_manual_failover(self):
        self.device.failover.return_value = True
        self.assertTrue(self.ha.do_manual_failover(device=self.device))

        self.assertRaises(Exception, self.ha.do_manual_failover)
        self.assertTrue(self.ha2.do_manual_failover())


    def test_do_ip_monitoring_failover(self):
        status = [{"node0":{"status":"primary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"secondary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node1", "failover-mode":"no"}},
                  {"node0":{"status":"secondary", "priority":"0", "monitor-failures":"IP", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}},
                  {"node0":{"status":"secondary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}},
                ]
        self.device.config.return_value = True
        self.device.commit.return_value = True
        self.ha.get_ha_status = Mock(return_value="")
        self.ha.get_ha_healthy_status = Mock()
        self.ha2.get_ha_status = Mock(return_value="")
        self.ha2.get_ha_healthy_status = Mock()

        # round 1, failover succeed
        self.ha.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["\r", "\r", "s i et-9/0/0\r\ns i et-10/0/0\r\n"]
        self.assertTrue(self.ha.do_ip_monitoring_failover(self.device,
                            rg="1", ip_address="", secondary_ip_address="", interface="reth0"))
        # round 2, failover fail
        status[0]['node0']['status'] = "secondary"
        status[0]['node1']['status'] = "primary"
        self.ha.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["dummy\r", "dummy\r", "s i et-9/0/0\r\ns i et-10/0/0\r\n"]
        self.assertFalse(self.ha.do_ip_monitoring_failover(self.device,
                            rg="1", ip_address="", secondary_ip_address="", interface="reth0"))
        status[0]['node0']['status'] = "primary"
        status[0]['node1']['status'] = "secondary"
        # get False status after failover
        status[1] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["\r", "\r", "s i et-9/0/0\r\ns i et-10/0/0\r\n"]
        self.assertFalse(self.ha.do_ip_monitoring_failover(self.device,
                            rg="1", ip_address="", secondary_ip_address="", interface="reth0"))
        status[1] = {"node0":{"status":"secondary", "priority":"0", "monitor-failures":"IP", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}}
        # round 3, wrong reth config 
        self.ha.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["\r", "\r", "s i et-9/0/0\r\ns i et-10/0/0\r\ndummy\r\n"]
        self.assertFalse(self.ha.do_ip_monitoring_failover(self.device,
                            rg="1", ip_address="", secondary_ip_address="", interface="reth0"))
        # round 4, wrong interface format
        self.assertFalse(self.ha.do_ip_monitoring_failover(self.device,
                            rg="1", ip_address="", secondary_ip_address="", interface="reth0.0"))
        # round 5, abnormal HA status at beginning
        status[0] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha.do_ip_monitoring_failover(self.device,
                            rg="1", ip_address="", secondary_ip_address="", interface="reth0"))
        status[0] = {"node0":{"status":"primary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"secondary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}}
        # round 6, HA status not recovered after failvoer
        status[2] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["\r", "\r", "s i et-9/0/0\r\ns i et-10/0/0\r\n"]
        self.assertFalse(self.ha.do_ip_monitoring_failover(self.device,
                            rg="1", ip_address="", secondary_ip_address="", interface="reth0"))
        status[2] = {"node0":{"status":"secondary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}}
        # round 7, device handle is None
        self.assertRaises(Exception, self.ha.do_ip_monitoring_failover,
                            rg="1", ip_address="", secondary_ip_address="", interface="reth0")
        # round 8, device handle is passed from constructor 
        status[2]['node0']['status'] = "primary"
        status[2]['node1']['status'] = "secondary"
        self.ha2.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["\r", "\r", "s i et-9/0/0\r\ns i et-10/0/0\r\n"]
        self.assertFalse(self.ha2.do_ip_monitoring_failover(
                            rg="1", ip_address="", secondary_ip_address="", interface="reth0"))
        status[2]['node0']['status'] = "secondary"
        status[2]['node1']['status'] = "primary"

    def test_do_interface_monitor_failover(self):
        status = [{"node0":{"status":"primary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"secondary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node1", "failover-mode":"no"}},
                  {"node0":{"status":"secondary", "priority":"0", "monitor-failures":"IF", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}},
                  {"node0":{"status":"secondary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}},
                ]
        self.device.config.return_value = True
        self.device.commit.return_value = True
        self.ha.get_ha_status = Mock(return_value="")
        self.ha.get_ha_healthy_status = Mock()
        self.ha2.get_ha_status = Mock(return_value="")
        self.ha2.get_ha_healthy_status = Mock()

        # Exception
        self.assertRaises(Exception, self.ha.do_interface_monitor_failover, rg="0", interface="reth0")
        # wrong interface format
        self.assertFalse(self.ha.do_interface_monitor_failover(self.device, rg="1", interface="reth0.0"))
        # abnormal status before failover
        self.ha.get_ha_healthy_status.side_effect = [False]
        self.assertFalse(self.ha.do_interface_monitor_failover(self.device, rg="0", interface="reth0"))
        # failover succeed
        self.ha.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["s i et-9/0/0\r\ns i et-10/0/0\r\n", "dummy\r", "dummy\r"]
        self.assertTrue(self.ha.do_interface_monitor_failover(self.device, rg="1", interface="reth0"))
        # wrong reth config
        self.ha.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["s i et-9/0/0\r\ns i et-10/0/0\r\ndummy\r\n", "\r", "\r"]
        self.assertFalse(self.ha.do_interface_monitor_failover(self.device, rg="0", interface="reth0"))
        # failover fail, get False status after failover 
        status[0]['node0']['status'] = "secondary"
        status[1] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["s i et-9/0/0\r\ns i et-10/0/0\r\n", "dummy\r", "dummy\r"]
        self.assertFalse(self.ha.do_interface_monitor_failover(self.device, rg="0", interface="reth0"))
        status[0]['node0']['status'] = "primary"
        status[1] = {"node0":{"status":"secondary", "priority":"0", "monitor-failures":"IF", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                     "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}}
        # failover fail, status after failover is not expected
        status[1]['node0']['status'] = "primary"
        self.ha.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["s i et-9/0/0\r\ns i et-10/0/0\r\n", "dummy\r", "dummy\r"]
        self.assertFalse(self.ha.do_interface_monitor_failover(self.device, rg="0", interface="reth0"))
        status[1]['node0']['status'] = "secondary"
        # failover fail, get False status after recover
        status[2] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["s i et-9/0/0\r\ns i et-10/0/0\r\n", "dummy\r", "dummy\r"]
        self.assertFalse(self.ha.do_interface_monitor_failover(self.device, rg="0", interface="reth0"))
        status[2] = {"node0":{"status":"secondary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                     "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}}
        # failover fail, status after recover is not expected
        status[2]['node0']['status'] = "primary"
        self.ha2.get_ha_healthy_status.side_effect = status
        self.device.cli().response.side_effect = ["s i et-9/0/0\r\ns i et-10/0/0\r\n", "dummy\r", "dummy\r"]
        self.assertFalse(self.ha2.do_interface_monitor_failover(rg="0", interface="reth0"))
        status[2]['node0']['status'] = "secondary"

    @patch("time.sleep", return_value=None)
    def test_do_reboot_failover(self, mock_time):
        status = [{"node0":{"status":"primary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"secondary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}},
                  {"node0":{"status":"primary", "priority":"20", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"secondary", "priority":"10", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}},
                  {"node0":{"status":"secondary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}},
                  {"node0":{"status":"secondary", "priority":"20", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"10", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}},
                ]

        self.device.config.return_value = True
        self.device.commit.return_value = True
        self.ha.reboot_node = Mock(return_value=True)
        self.ha.check_fpc_pic = Mock(return_value=True)
        self.ha.get_ha_status = Mock(return_value="")
        self.ha.get_ha_healthy_status = Mock()
        self.ha.get_ha_rgs = Mock(return_value=["0","1"])
        self.ha2.get_ha_status = Mock(return_value="")
        self.ha2.get_ha_healthy_status = Mock()
        self.ha2.get_ha_rgs = Mock(return_value=False)

        # round 1, failover succeed
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertTrue(self.ha.do_reboot_failover(self.device, rg="0"))
        # round 2, failover fail due to specified rg
        status[2]['node0']['status'] = "primary"
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha.do_reboot_failover(self.device, rg="0"))
        status[2]['node0']['status'] = "secondary"
        # get False status after failover
        status[2] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha.do_reboot_failover(self.device, rg="0"))
        status[2] = {"node0":{"status":"secondary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                     "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}}
        # round 3, failover fail due to other rg
        status[3]['node0']['status'] = "primary"
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha.do_reboot_failover(self.device, rg="0"))
        status[3]['node0']['status'] = "secondary"
        # get False status after failover
        status[3] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha.do_reboot_failover(self.device, rg="0"))
        status[3] = {"node0":{"status":"secondary", "priority":"20", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"10", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}}
        # round 4, abnormal HA status at beginning for specified rg
        status[0] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha.do_reboot_failover(self.device, rg="0"))
        status[0] = {"node0":{"status":"primary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"secondary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node1", "failover-mode":"no"}}
        # round 5, abnormal HA status at beginning for another rg
        status[1] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha.do_reboot_failover(self.device, rg="0"))
        status[1] = {"node0":{"status":"primary", "priority":"20", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"secondary", "priority":"10", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node1", "failover-mode":"no"}}
        # round 6, failover required for another rg - 1 
        status[1]['node0']['status'] = "secondary"
        status[1]['node1']['status'] = "primary"
        self.ha.get_ha_healthy_status.side_effect = status
        self.ha.do_manual_failover = Mock(return_value=True)
        self.assertTrue(self.ha.do_reboot_failover(self.device, rg="0"))
        status[1]['node0']['status'] = "primary"
        status[1]['node1']['status'] = "secondary"
        # round 7, failover required for another rg - 2
        status[0]['node0']['status'] = "secondary"
        status[0]['node1']['status'] = "primary"
        self.ha.do_manual_failover = Mock(return_value=True)
        self.ha.get_ha_healthy_status.side_effect = status
        self.ha.check_via_xpath = Mock(side_effect=[False, True])
        self.assertFalse(self.ha.do_reboot_failover(self.device, rg="0"))
        status[0]['node0']['status'] = "primary"
        status[0]['node1']['status'] = "secondary"
        # round 8, device handle is None
        self.assertRaises(Exception, self.ha.do_reboot_failover, rg="0")
        # round 9, device handle is passed via constructor
        self.ha2.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha2.do_reboot_failover(rg="0"))
        # round 10, fpc is not online after rebooting
        self.ha.get_ha_healthy_status.side_effect = status
        self.ha.check_fpc_pic = Mock(return_value=False)
        self.assertFalse(self.ha.do_reboot_failover(self.device, rg="0"))

    def test_do_preempt_failover(self):
        status = [{"node0":{"status":"primary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"secondary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node1", "failover-mode":"no"}},
                  {"node0":{"status":"secondary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"254", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node1", "failover-mode":"no"}},
                  {"node0":{"status":"secondary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                   "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}},
                ]

        self.device.config.return_value = True
        self.device.commit.return_value = True
        self.ha.get_ha_status = Mock(return_value="")
        self.ha.get_ha_healthy_status = Mock()
        self.ha2.get_ha_status = Mock(return_value="")
        self.ha2.get_ha_healthy_status = Mock()

        # Exception
        self.assertRaises(Exception, self.ha.do_preempt_failover, rg="0")
        # abnormal status before failover
        self.ha.get_ha_healthy_status.side_effect = [False]
        self.assertFalse(self.ha.do_preempt_failover(self.device, rg="0"))
        # failover succeed
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertTrue(self.ha.do_preempt_failover(self.device, rg="0"))
        # failover fail, get False status after failover 
        status[0]['node0']['status'] = "secondary"
        status[1] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha.do_preempt_failover(self.device, rg="0"))
        status[0]['node0']['status'] = "primary"
        status[1] = {"node0":{"status":"secondary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node0", "failover-mode":"no"}, 
                     "node1":{"status":"primary", "priority":"254", "monitor-failures":"None", 
                            "preempt":"yes", "name":"node1", "failover-mode":"no"}}
        # failover fail, status after failover is not expected
        status[1]['node0']['status'] = "primary"
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha.do_preempt_failover(self.device, rg="0"))
        status[1]['node0']['status'] = "secondary"
        # failover fail, get False status after recover
        status[2] = False
        self.ha.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha.do_preempt_failover(self.device, rg="0"))
        status[2] = {"node0":{"status":"secondary", "priority":"200", "monitor-failures":"None", 
                            "preempt":"no", "name":"node0", "failover-mode":"no"}, 
                     "node1":{"status":"primary", "priority":"100", "monitor-failures":"None", 
                            "preempt":"no", "name":"node1", "failover-mode":"no"}}
        # failover fail, status after recover is not expected
        status[2]['node0']['status'] = "primary"
        self.ha2.get_ha_healthy_status.side_effect = status
        self.assertFalse(self.ha2.do_preempt_failover(rg="0"))
        status[2]['node0']['status'] = "secondary"


    def test_reboot_node(self):
        self.device.node_name.return_value = "node0"
        self.device.switch_node.return_value = True
        self.device.reboot.return_value = True

        self.assertRaises(Exception, self.ha.reboot_node, device=self.device, node="1")
        self.assertTrue(self.ha.reboot_node(device=self.device, node="node0"))
        self.assertTrue(self.ha.reboot_node(device=self.device, node="node1"))

        self.assertRaises(Exception, self.ha.reboot_node, node="1")
        self.assertTrue(self.ha2.reboot_node(node="node0"))

    def test_check_via_xpath(self):
        self.device.get_rpc_equivalent.return_value = "</>"
        mock_content = Mock(spec=etree._Element)
        mock_content_list = Mock(spec=etree._Element)
        mock_content_list.xpath.return_value = [mock_content]
        self.device.execute_rpc().response.return_value = mock_content_list
        # round 1
        mock_content.text = "Online"
        criteria_1 = [{'xpath':"", 'operator':"==",'expect':"Online"}, 
                      {'xpath':"", 'operator':"==",'expect':"Online|Offline"}]
        self.assertTrue(self.ha.check_via_xpath(device=self.device, command="", check_criteria=criteria_1))
        # round 2
        mock_content.text = "100"
        criteria_2 = [{'xpath':"", 'operator':">=",'expect':"200"}]
        criteria_3 = [{'xpath':"", 'operator':"==",'expect':"100|200"}]
        self.assertFalse(self.ha.check_via_xpath(device=self.device, command="", check_criteria=criteria_2))
        self.assertTrue(self.ha.check_via_xpath(device=self.device, command="", check_criteria=criteria_3))

        self.assertRaises(Exception, self.ha.check_via_xpath, command="", check_criteria=criteria_2)
        self.assertTrue(self.ha2.check_via_xpath(command="", check_criteria=criteria_3))
        # round 3
        mock_content_list.xpath.return_value = []
        self.assertFalse(self.ha.check_via_xpath(device=self.device, command="", check_criteria=criteria_3))

    @patch("time.sleep", return_value=None)
    def test_check_fpc_pic(self, mock_time):
        self.ha.check_via_xpath = Mock(return_value=True)
        self.ha2.check_via_xpath = Mock(return_value=False)
        self.assertRaises(Exception, self.ha.check_fpc_pic)
        self.assertTrue(self.ha.check_fpc_pic(device=self.device, retry=1, interval=15))
        self.assertFalse(self.ha2.check_fpc_pic(retry=1, interval=15))

    def test__quote(self):
        self.assertEqual(self.ha._quote('srx'), '"srx"')

    def test__space(self):
        self.assertEqual(self.ha._space('=='), ' == ')

if __name__ == "__main__":
    unittest.main()





