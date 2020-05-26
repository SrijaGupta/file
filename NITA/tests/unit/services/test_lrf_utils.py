#! /usr/bin/python3
"""
Description : Unit testcases for lrf_tools.py
Company : Juniper Networks
"""

import builtins
import unittest
import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.services.lrf_utils import *
from jnpr.toby.hldcl.unix.unix import UnixHost

builtins.t = MagicMock()

class UnitTest(unittest.TestCase):
    """
    Unit testcase for methods in lrf_utils.py
    """
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.shell = MagicMock()
    mocked_obj.shell.response = MagicMock()

#### UT for LRF_utils.py starts here
    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self.mocked_obj.shell = MagicMock()
        self.mocked_obj.shell.response = MagicMock()
        self.mocked_obj.shell.return_value.response.return_value = "Test LRF#"

    def test_initiate_lrf(self):
        """
        Unit testcase for initiate_lrf of lrf_utils.py
        """
#        self.assertEqual(initiate_lrf(self.mocked_obj, interface="em1",
#                                      server_ip="5.0.0.1", lrf_binary="testfile.exe",
#                                      port="5060"), True)

        self.assertEqual(initiate_lrf(self.mocked_obj, "em1",
                                      "5.0.0.1", "5060", "testfile.exe"), True)

    def test_lrf_path_profile_config(self):
        """
        Unit testcase for lrf_path_profile_config of lrf_utils.py
        """
#        self.assertEqual(lrf_path_profile_config(self.mocked_obj,
#                                                 server_ip="5.0.0.1", client_ip="5.0.0.2",
#                                                 path_protocol="udp"), True)

        self.assertEqual(lrf_path_profile_config(self.mocked_obj,
                                                 "5.0.0.1", "5.0.0.2","udp"), True)
    def test_create_control_template(self):
        """
        Unit testcase for create_control_template of lrf_utils.py
        """
        control_template_dict = {'11':'http-data', '10':'l7-data', '6':'ipflow-data'}
#        self.assertEqual(create_control_template(self.mocked_obj, control_template_dict,
#                                                 template_name="ip_flow"), True)
        self.assertEqual(create_control_template(self.mocked_obj, control_template_dict,
                                                 "ip_flow"), True)

    def test_create_data_template(self):
        """
        Unit testcase for create_data_template of lrf_utils.py
        """
        data_template_dict = {'app_name':'junos:facebook-access',
                              'host':'www.facebook.com'}
#        self.assertEqual(create_data_template(self.mocked_obj,
#                                              data_template_dict, template_name="http-data",
#                                              template_type="http-data-template"), True)

        self.assertEqual(create_data_template(self.mocked_obj, data_template_dict, "http-data",
                                              "http-data-template"), True)

    def test_delete_control_template(self):
        """
        Unit testcase for delete_control_template of lrf_utils.py
        """
#        self.assertEqual(delete_control_template(self.mocked_obj,
#                                                 template_name="ip_flow"), True)

        self.assertEqual(delete_control_template(self.mocked_obj,
                                                 "ip_flow"), True)

    def test_delete_control_subtemplate(self):
        """
        Unit testcase for control_sub_template of lrf_utils.py
        """
#        self.assertEqual(delete_control_sub_template(self.mocked_obj,
#                                                     template_name="http-data",
#                                                     template_type="http-data-template"), True)

        self.assertEqual(delete_control_sub_template(self.mocked_obj, "http-data",
                                                     "http-data-template"), True)

    def test_lrf_exec_command(self):
        """
        Unit testcase for lrf_exec_command of lrf_utils.py
        """
#        self.assertEqual(lrf_exec_command(self.mocked_obj,
#                                          command="set lrf display time 1000"), "Test LRF#")

        self.assertEqual(lrf_exec_command(self.mocked_obj,
                                          "set lrf display time 1000"), "Test LRF#")

    def test_stop_lrf(self):
        """
        Unit testcase for stop_lrf of lrf_utils.py
        """
        self.assertEqual(stop_lrf(self.mocked_obj), True)


    def test_data_record_validation(self):
        """
        Unit testcase1 for data_record_validation of lrf_utils.py
        """
        fail_string = """Global stats
              Template Record:
                Verified 1
                Failed 2
                New                   1
                Existing              0
                Total                 1

              Cumulative Data Template Records:
                Total:  Template type:6   Validated:3
                Total:  Template type:6   Validation Failed:2
                Total:  Template type:7   Validated:3
                Total:  Template type:7   Validation Failed:0
                Total:  Template type:10   Validated:3
                Total:  Template type:10   Validation Failed:0
                Total:  Template type:11   Validated:3
                Total:  Template type:11   Validation Failed:0

              Data Record:
                Failed                0
                Total Packets         0
                Verified              3
                Total                 3
                Records/sec           0
            """
        self.assertEqual(data_record_validation(fail_string, "time"), False)

    def test_data_record_validation_1(self):
        """
        Unit testcase2 for data_record_validation of lrf_utils.py
        """
        string1 = """Field type: Uplink Octects(103), Field Length: 4
            Field type: Downlink Octects(104), Field Length: 4
            Field type: Uplink Packets(105), Field Length: 4
            Field type: Downlink Packets(106), Field Length: 4
            Field type: IP Protocol(4), Field Length: 1
            Field type: Record Reason(112), Field Length: 1
            Field type: Flow Start Milliseconds(101), Field Length: 8
            Field type: Flow End Milliseconds(102), Field Length: 8
            Field type: Application Protocol(151), Field Length: 8
            Field type: Application Name(170), Field Length: 32
            Field type: Host(157), Field Length: 64
            Field type: User Agent(152), Field Length: 32
            Field type: Content Length - Request(154), Field Length: 4
            Field type: HTTP Response Code(155), Field Length: 2
            Field type: Language(156), Field Length: 16
            Field type: Host(157), Field Length: 64
            Field type: Location(158), Field Length: 64
            Field type: HTTP Method(159), Field Length: 8
            Field type: Referer(Http)(160), Field Length: 64
            Field type: MIME Type(161), Field Length: 32
            Field type: Http URI(163), Field Length: 255
            Field type: Time to First Byte(181), Field Length: 4
            Template Length:88
            
            
            
            
            
            Field Type:Uplink Octects, Field Value:32644
            Field Type:Downlink Octects, Field Value:966584
            Field Type:Uplink Packets, Field Value:267
            Field Type:Downlink Packets, Field Value:673
            Field Type:IP Protocol, Field Value:6
            Field Type:Record Reason, Field Value:3
            Field Type:Flow Start Milliseconds, Field Value:2501582136270914652
            Field Type:Flow End Milliseconds, Field Value:2501582136270984672
            Field Type:Application Protocol, Field Value:http
            Field Type:Application Name, Field Value:junos:facebook-access
            Field Type:Host, Field Value:www.facebook.com
            Field Type:User Agent, Field Value:Mozilla/5.0 (X11; U; Linux x86_6
            Field Type:Content Length - Request, Field Value:32795
            Field Type:HTTP Response Code, Field Value:200
            Field Type:Language, Field Value:
            Field Type:Host, Field Value:www.facebook.com
            Field Type:Location, Field Value:
            Field Type:HTTP Method, Field Value:GET
            Field Type:Referer(Http), Field Value:
            Field Type:MIME Type, Field Value:text/html
            Field Type:Http URI, Field Value:/
            Field Type:Time to First Byte, Field Value:0
            
            
            
            
            
            Field Type:Uplink Octects, Field Value:104
            Field Type:Downlink Octects, Field Value:104
            Field Type:Uplink Packets, Field Value:2
            Field Type:Downlink Packets, Field Value:2
            Field Type:IP Protocol, Field Value:6
            Field Type:Record Reason, Field Value:3
            Field Type:Flow Start Milliseconds, Field Value:2501582136270984672
            Field Type:Flow End Milliseconds, Field Value:2501582136271054677
            Field Type:Application Protocol, Field Value:http
            Field Type:Application Name, Field Value:junos:facebook-access
            Field Type:Host, Field Value:www.facebook.com
            Field Type:User Agent, Field Value:Mozilla/5.0 (X11; U; Linux x86_6
            Field Type:Content Length - Request, Field Value:32795
            Field Type:HTTP Response Code, Field Value:200
            Field Type:Language, Field Value:
            Field Type:Host, Field Value:www.facebook.com
            Field Type:Location, Field Value:
            Field Type:HTTP Method, Field Value:GET
            Field Type:Referer(Http), Field Value:
            Field Type:MIME Type, Field Value:text/html
            Field Type:Http URI, Field Value:/
            Field Type:Time to First Byte, Field Value:0
            
            
            
            
            
            
            Field Type:Uplink Octects, Field Value:52
            Field Type:Downlink Octects, Field Value:80
            Field Type:Uplink Packets, Field Value:1
            Field Type:Downlink Packets, Field Value:2
            Field Type:IP Protocol, Field Value:6
            Field Type:Record Reason, Field Value:1
            Field Type:Flow Start Milliseconds, Field Value:2501582136271054677
            Field Type:Flow End Milliseconds, Field Value:2501582136271057677
            Field Type:Application Protocol, Field Value:http
            Field Type:Application Name, Field Value:junos:facebook-access
            Field Type:Host, Field Value:www.facebook.com
            Field Type:User Agent, Field Value:Mozilla/5.0 (X11; U; Linux x86_6
            Field Type:Content Length - Request, Field Value:32795
            Field Type:HTTP Response Code, Field Value:200
            Field Type:Language, Field Value:
            Field Type:Host, Field Value:www.facebook.com
            Field Type:Location, Field Value:
            Field Type:HTTP Method, Field Value:GET
            Field Type:Referer(Http), Field Value:
            Field Type:MIME Type, Field Value:text/html
            Field Type:Http URI, Field Value:/
            Field Type:Time to First Byte, Field Value:0
            
            
            Global stats
              Template Record:
                Verified              1
                Failed                0
                New                   1
                Existing              0
                Total                 1
            
              Cumulative Data Template Records:
                Total:  Template type:6   Validated:3
                Total:  Template type:6   Validation Failed:0
                Total:  Template type:7   Validated:3
                Total:  Template type:7   Validation Failed:0
                Total:  Template type:10   Validated:3
                Total:  Template type:10   Validation Failed:0
                Total:  Template type:11   Validated:3
                Total:  Template type:11   Validation Failed:0
            
              Data Record:
                Failed                0
                Total Packets         0
                Verified              3
                Total                 3
                Records/sec           0

            """
        self.assertEqual(data_record_validation(string1, "time"), True)

if __name__ == "__main__":
    unittest.main()
