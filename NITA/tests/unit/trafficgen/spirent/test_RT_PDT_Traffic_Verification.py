import os
import sys
import unittest
import datetime
import builtins
import mock
from mock import patch, MagicMock
from jnpr.toby.init.init import init
# import RT_PDT_Traffic_Verification ## Uncomment this when testing locally.
# from RT_PDT_Traffic_Verification import RT_PDT_Traffic_Verification_Data ## Uncomment this when testing locally.
from jnpr.toby.trafficgen.spirent import RT_PDT_Traffic_Verification
from jnpr.toby.trafficgen.spirent.RT_PDT_Traffic_Verification import RT_PDT_Traffic_Verification_Data

rt_handle = MagicMock()
rt = RT_PDT_Traffic_Verification_Data(rt_handle)
yaml_file_data_as_string = """
TOLERANCE:
  tolerance__ECMP_convergence: 
    global: 0.9s 


TG_TRAFFIC_CONFIG: 
  BS_Compute_Node_r4_1_to_Customer_Node_r1_1_L2_Unicast_Tagged_v6:
    port_handle : r4rt0_1
    _tag:
      - unicast
      - delete_add_vxlan_test_case 
      - disable_enable_customer_facing_ae_test_case 
      - delete_add_vlan_customer_switch_test_case 
      - deactivate_activate_pim_test_case
    _multiplication_factor: 2
"""

class TestRTTrafficVerification(unittest.TestCase):

    global_rt_data = None

    def setUp(self):
        builtins.t = self
        builtins.t.log = MagicMock()
        # Populating necessary data for creating rt_data
        yaml_file = ''
        sb_handle_var_dict = {'rt0__BS_Compute_Node_r4_1_to_Customer_Node_r1_1_L2_Unicast_Tagged_v6':'streamblock1'}
        resource = 'rt0'
        rt_handle.port_to_handle_map = {'2/3':'port1', '2/4':'port2'}
        builtins.t = self
        t.t_dict = {"resources": { 'rt0': {'interfaces':{'r4_1':{'name':'2/3', 'link':'r4rt0_1'}, \
                    'r2_1':{'name':'2/4', 'link':'r2rt0_1'}}}}}
        self.global_rt_data = RT_PDT_Traffic_Verification.pdt_rt_initialize_yaml(rt_handle, yaml_file, \
                                              sb_handle_var_dict, resource, yaml_file_data_as_string=yaml_file_data_as_string)

    def test_pdt_rt_initialize_yaml(self):
        rt_data = self.global_rt_data

        #asserting if the rt_data.port_handle_map is populated properly
        self.assertEqual(rt_data.stc_port_handle_map["r4rt0_1"], "port1")
        self.assertEqual(rt_data.stc_port_handle_map["r2rt0_1"], "port2") 
        #asserting if the rt_data.port_map is populated properly
        self.assertEqual(rt_data.port_map["port1"], "r4rt0_1")
        self.assertEqual(rt_data.port_map["port2"], "r2rt0_1")
        #asserting if the rt_data.notational_to_actual__port_map is populated properly
        self.assertEqual(rt_data.notational_to_actual__port_map["r2rt0_1"], "2/4")
        self.assertEqual(rt_data.notational_to_actual__port_map["r4rt0_1"], "2/3")

    def test_pdt_rt_start_traffic(self):
        rt_data = self.global_rt_data
        tag = "unicast"
        #with patch("rt_handle.invoke", return_value={"status":"1"}):
        result1 = {"status":"1"}
        result2 = {"status":"1"}
        rt_handle.invoke.side_effect = [result1,result2]

        #starting traffic without passing any additional arguments
        status = RT_PDT_Traffic_Verification.pdt_rt_start_traffic(rt_handle, rt_data)
        self.assertEqual(status["status"], "1")

        #starting traffic with the argument tag
        rt_handle.invoke.side_effect = [result1,result2]
        status = RT_PDT_Traffic_Verification.pdt_rt_start_traffic(rt_handle, rt_data, tag='unicast')
        self.assertEqual(status["status"], "1")  

        #starting traffic with the argument sb_name_list 
        rt_handle.invoke.side_effect = [result1,result2]
        status = RT_PDT_Traffic_Verification.pdt_rt_start_traffic(rt_handle, rt_data, tag_list='unicast', \
                     sb_name_list=['BS_Compute_Node_r4_1_to_Customer_Node_r1_1_L2_Unicast_Tagged_v6'])
        self.assertEqual(status["status"], "1")
        
        #starting traffic with the argument port_name_list
        rt_handle.invoke.side_effect = [result1,result2]
        status = RT_PDT_Traffic_Verification.pdt_rt_start_traffic(rt_handle, rt_data, port_name_list= ['r2rt0_1', 'r4rt0_1'])
        self.assertEqual(status["status"], "1")

    #def test_pdt_rt_send_arp(self):
    #    rt_data = self.global_rt_data
    #    tag = "unicast"
    #    #with patch("rt_handle.invoke", return_value={"status":"1"}):
    #    result1 = {"status":"1"}
    #    result2 = {"status":"1"}
    #    rt_handle.invoke.side_effect = [result1,result2]
    #    status = RT_PDT_Traffic_Verification._send_arp(rt_handle, rt_data)

    #    rt_handle.invoke.side_effect = [result1,result2]
    #    status = RT_PDT_Traffic_Verification.pdt_rt_send_arp(rt_handle, rt_data, tag='unicast')

    #    rt_handle.invoke.side_effect = [result1,result2]
    #    status = RT_PDT_Traffic_Verification.pdt_rt_send_arp(rt_handle, rt_data, tag_list='unicast', dev_sb_name_list=['BS_Compute_Node_r4_1_to_Customer_Node_r1_1_L2_Unicast_Tagged_v6'])

    #    rt_handle.invoke.side_effect = [result1,result2]
    #    status = RT_PDT_Traffic_Verification.pdt_rt_start_traffic(rt_handle, rt_data, port_name_list= ['r2rt0_1', 'r4rt0_1'])

    def test_pdt_rt_verify_traffic_with_streamblock(self):
        #implement with level stream also
        #with level as streamblock
        rt_data = self.global_rt_data
        tag = "unicast"
        result1 = {"status":"1", "port1": {
                      "stream": {
                          "streamblock1": {
                              "rx": {
                                  "dropped_pkts": "0",
                                  "duplicate_pkts": "0",
                                  "out_of_sequence_pkts": "0",
                                  "rx_port": "",
                                  "rx_sig_count": "0",
                                  "total_pkt_rate": "0",
                                  "total_pkts": "2000"
                              },
                              "tx": {
                                  "total_pkt_rate": "0",
                                  "total_pkts": "1000"
                              }
                           }
                        }
                     }
                  }
        rt_handle.invoke.side_effect = [result1]
        rt_handle.sth.invoke.side_effect = ["", "10000", "FRAMES_PER_SECOND"]
        result = RT_PDT_Traffic_Verification.pdt_rt_get_streamblock_tx_rates(rt_handle, rt_data)
        result = RT_PDT_Traffic_Verification.pdt_rt_verify_traffic(rt_handle=rt_handle, rt_data=rt_data, \
                                                          collect_fresh_stats=True)
        self.assertTrue(result, True)
        # Verifying traffic with tolerance
        tolerance_label = "tolerance__ECMP_convergence"
        rt_handle.invoke.side_effect = [result1, result1]
        rt_handle.sth.invoke.side_effect = ["", "10000", "FRAMES_PER_SECOND", "", "10000", "FRAMES_PER_SECOND"] 
        RT_PDT_Traffic_Verification.pdt_rt_verify_traffic(rt_handle=rt_handle, rt_data=rt_data, \
                                                          collect_fresh_stats=True, tolerance_label=tolerance_label)
        self.assertTrue(result, True)

        result1 = {"status":"1", "port1": {
                      "stream": {
                          "streamblock1": {
                              "rx": {
                                  "dropped_pkts": "0",
                                  "duplicate_pkts": "0",
                                  "out_of_sequence_pkts": "0",
                                  "rx_port": "",
                                  "rx_sig_count": "0",
                                  "total_pkt_rate": "0",
                                  "total_pkts": "0"
                              },
                              "tx": {
                                  "total_pkt_rate": "0",
                                  "total_pkts": "1000"
                              }
                           }
                        }
                     }
                  }
        rt_data._do_not_rely_on_spirent_dropped_pkts = False
        rt_handle.invoke.side_effect = [result1]
        rt_handle.sth.invoke.side_effect = ["", "10000", "FRAMES_PER_SECOND"]
        RT_PDT_Traffic_Verification.pdt_rt_get_streamblock_tx_rates(rt_handle, rt_data)
        RT_PDT_Traffic_Verification.pdt_rt_verify_traffic(rt_handle=rt_handle, rt_data=rt_data, \
                                                          collect_fresh_stats=True)
        self.assertTrue(result, True)

        rt_data._do_not_rely_on_spirent_dropped_pkts = True
        rt_data.USE_CONFIGURED_SB_TX_RATES = False
        rt_handle.invoke.side_effect = [result1, result1]
        rt_handle.sth.invoke.side_effect = ["", "10000", "FRAMES_PER_SECOND"]
        RT_PDT_Traffic_Verification.pdt_rt_get_streamblock_tx_rates(rt_handle, rt_data)
        RT_PDT_Traffic_Verification.pdt_rt_verify_traffic(rt_handle=rt_handle, rt_data=rt_data, \
                                                          collect_fresh_stats=True)
        self.assertTrue(result, True)

    #def test_pdt_rt_verify_traffic_with_stream(self):
    #    rt_data = self.global_rt_data
    #    tag = "unicast"
    #    result1 = {"status":"1", "port1": {
    #                  "stream": {
    #                      "streamblock1": {
    #                          "rx": {
    #                              "dropped_pkts": "0",
    #                              "duplicate_pkts": "0",
    #                              "out_of_sequence_pkts": "0",
    #                              "rx_port": "",
    #                              "rx_sig_count": "0",
    #                              "total_pkt_rate": "0",
    #                              "total_pkts": "1000"
    #                          },
    #                          "tx": {
    #                              "total_pkt_rate": "0",
    #                              "total_pkts": "1000"
    #                          }
    #                       }
    #                    }
    #                 }
    #              }
    #    result2 = {"status":"1", "port1": {
    #                  "stream": {
    #                      "streamblock1": {
    #                          "tx": { #streamid omkar what should this sensibly be?
    #                              "1": {
    #                                  "total_pkt_rate": "10000",
    #                                  "total_pkts": "1000",
    #                                  "pkt_drop_dur_sec": "1",
    #                                  "dropped_pkts": "0" 
    #                              }
    #                          }
    #                       }
    #                    }
    #                 }
    #              }
    #    rt_handle.invoke.side_effect = [result2]
    #    rt_handle.sth.invoke.side_effect = ["", "10000", "FRAMES_PER_SECOND"]
    #    RT_PDT_Traffic_Verification.pdt_rt_get_stream_tx_rates(rt_handle, rt_data)
    #    rt_handle.invoke.side_effect = [result2]
    #    print(rt_data.agg_traffic_stats)
    #    RT_PDT_Traffic_Verification.pdt_rt_verify_traffic(rt_handle=rt_handle, rt_data=rt_data, \
    #                                                      collect_fresh_stats=True, level="stream")

        #Covering tolerance
        #tolerance_label = "tolerance__ECMP_convergence"
        #rt_handle.invoke.side_effect = [result1, result1]
        #rt_handle.sth.invoke.side_effect = ["", "10000", "FRAMES_PER_SECOND", "", "10000", "FRAMES_PER_SECOND"]
        #RT_PDT_Traffic_Verification.pdt_rt_verify_traffic(rt_handle=rt_handle, rt_data=rt_data, \
        #                                                  collect_fresh_stats=True, level="stream", tolerance_label=tolerance_label)

    def test_pdt_rt_stop_traffic(self):
        rt_data = self.global_rt_data
        tag = "unicast"
        result1 = {"status":"1"}
        result2 = {"status":"1"}
        rt_handle.invoke.side_effect = [result1]

        #starting traffic without passing any additional arguments
        status = RT_PDT_Traffic_Verification.pdt_rt_stop_traffic(rt_handle=rt_handle, rt_data=rt_data)
        self.assertEqual(status["status"], "1")

        #starting traffic without passing the argument port_name_list
        rt_handle.invoke.side_effect = [result1]
        status = RT_PDT_Traffic_Verification.pdt_rt_stop_traffic(rt_handle=rt_handle, rt_data=rt_data, \
                        port_handle=[], port_name_list=['r2rt0_1', 'r4rt0_1'])
        self.assertEqual(status["status"], "1")

        #starting traffic without passing the argument sb_name_list
        rt_handle.invoke.side_effect = [result1]
        status = RT_PDT_Traffic_Verification.pdt_rt_stop_traffic(rt_handle=rt_handle, rt_data=rt_data, \
                        sb_name_list=['BS_Compute_Node_r4_1_to_Customer_Node_r1_1_L2_Unicast_Tagged_v6'])
        self.assertEqual(status["status"], "1")

    def test_pdt_rt_get_streamblock_tx_rates(self):
        result1 = {"status":"1", "port1": {
                      "stream": {
                          "streamblock1": {
                              "rx": {
                                  "dropped_pkts": "0",
                                  "duplicate_pkts": "0",
                                  "out_of_sequence_pkts": "0",
                                  "rx_port": "",
                                  "rx_sig_count": "0",
                                  "total_pkt_rate": "0",
                                  "total_pkts": "0"
                              },
                              "tx": {
                                  "total_pkt_rate": "0",
                                  "total_pkts": "1000"
                              }
                           }
                        }
                     }
                  }
        rt_handle.invoke.side_effect = [result1]
        rt_data = self.global_rt_data
        rt_data.USE_CONFIGURED_SB_TX_RATES = False
        result = RT_PDT_Traffic_Verification.pdt_rt_get_streamblock_tx_rates(rt_handle, rt_data)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result["port1"]["streamblock1"]["total_pkt_rate"], "0")

    def test_get_real_port_name(self):
        rt_data = self.global_rt_data
        port_handle = "port1"
        #asserting by passing the port handle
        status = RT_PDT_Traffic_Verification._get_real_port_name(rt_data, port_handle=port_handle)
        self.assertEqual(status, '2/3')
        #asserting without passing port handle
        status = RT_PDT_Traffic_Verification._get_real_port_name(rt_data)
        self.assertEqual(status, None)

    def test_pdt_rt_get_port_rates(self):
        rt_data = self.global_rt_data
        sample_count = 1
        port_name_list= ['r2rt0_1', 'r4rt0_1']
        result1 = {"status":"1", "port1": {
                      "aggregate": {
                              "rx": {
                                  "total_pkt_rate": "10000",
                              },
                              "tx": {
                                  "total_pkt_rate": "10000",
                              }
                        }
                     }
                  }
        rt_handle.invoke.side_effect = [result1]
        result = RT_PDT_Traffic_Verification.pdt_rt_get_port_rates(rt_handle, rt_data=rt_data, \
                        port_name_list=port_name_list, sample_count=sample_count)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result["port1"]["tx_port_rate"], 10000.0)
        self.assertEqual(result["port1"]["rx_port_rate"], 10000.0)

if __name__ == '__main__':
    unittest.main()
