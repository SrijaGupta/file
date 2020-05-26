import unittest2 as unittest
from mock import MagicMock, patch
from jnpr.toby.hldcl.device import Device
from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.appsecure.appqoe_syslog_verify import *


class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=Device)
    mocked_obj.log = MagicMock()
    mocked_shell_obj = MagicMock(spec=UnixHost)

    def setUp(self):
        """setup before all case"""
        #self.log = message(name="SYSLOG")
        #self.tool = flow_common_tool()
        #self.xml = xml_tool()
        #self.ins = security_logging()

    @patch('jnpr.toby.utils.linux.syslog_utils.check_syslog')
    def test_validate_appqoe_metric_syslog(self, chk_syslog):

        chk_syslog.return_value=True
        sys_message = '<14>1 2018-03-29T21:49:28.166+05:30 srxdpi-skpai-spoke RT_FLOW - APPQOE_ACTIVE_SLA_METRIC_REPORT ' +\
        '[junos@2636.1.1.1.2.129 source-address="40.1.1.2" source-port="36051" destination-address="40.1.1.1" ' +\
        'destination-port="36050" application="UDP" protocol-id="17" destination-zone-name="untrust" ' +\
        'routing-instance="appqoe-vrf" destination-interface-name="gr-0/0/0.0" ip-dscp="0" ingress-jitter="118" '+\
        'egress-jitter="108" rtt-jitter="183" rtt="1851" pkt-loss="0" bytes-from-client="25284" bytes-from-server="9504" ' +\
        'packets-from-client="129" packets-from-server="99" monitoring-time="30" active-probe-params="probe1" destination-group-name="site1"]'

        lst = [Response(True), Response(True), Response(sys_message), Response(True)]
        self.mocked_obj.shell = MagicMock(return_value=Response(sys_message))
        #self.mocked_obj.shell.response = MagicMock(return_value=sys_message)
        self.assertTrue(validate_appqoe_metric_syslog(self.mocked_obj, message='ACTIVE', syslog_mode="structured",
                                      file="/var/tmp/syslog_test.txt", source_address="40.1.1.2", source_port="36051",
                                      destination_address="40.1.1.1", destination_port="36050",
                                      destination_interface="gr-0/0/0.0"))
        self.assertTrue(validate_appqoe_metric_syslog(self.mocked_obj, message='PASSIVE', syslog_mode="structured",
                                                     file="/var/tmp/syslog_test.txt", source_address="40.1.1.2",
                                                     source_port="36051",
                                                     destination_address="40.1.1.1", destination_port="36050",
                                                     destination_interface="gr-0/0/0.0"))

        #get=1
        chk_syslog.return_value = True
        get_sys_message = '<14>1 2018-03-29T21:49:28.166+05:30 srxdpi-skpai-spoke RT_FLOW - APPQOE_ACTIVE_SLA_METRIC_REPORT ' + \
                      '[junos@2636.1.1.1.2.129 source-address="40.1.1.2" source-port="36051" destination-address="40.1.1.1" ' + \
                      'destination-port="36050" application="UDP" protocol-id="17" destination-zone-name="untrust" ' + \
                      'routing-instance="appqoe-vrf" destination-interface-name="gr-0/0/0.0" ip-dscp="0" ingress-jitter="118" ' + \
                      'egress-jitter="108" rtt-jitter="183" rtt="1851" pkt-loss="0" bytes-from-client="25284" bytes-from-server="9504" ' + \
                      'packets-from-client="129" packets-from-server="99" monitoring-time="30" active-probe-params="probe1" ' +  \
                      'destination-group-name="site1"]\n' + \
                      '<14>1 2018-03-29T21:49:28.166+05:30 srxdpi-skpai-spoke RT_FLOW - APPQOE_ACTIVE_SLA_METRIC_REPORT ' + \
                      '[junos@2636.1.1.1.2.129 source-address="40.1.1.2" source-port="36051" destination-address="40.1.1.1" ' + \
                      'destination-port="36050" application="UDP" protocol-id="17" destination-zone-name="untrust" ' + \
                      'routing-instance="appqoe-vrf" destination-interface-name="gr-0/0/0.0" ip-dscp="0" ingress-jitter="118" ' + \
                      'egress-jitter="108" rtt-jitter="183" rtt="1851" pkt-loss="0" bytes-from-client="25284" bytes-from-server="9504" ' + \
                      'packets-from-client="129" packets-from-server="99" monitoring-time="30" active-probe-params="probe1" '+\
                      'destination-group-name="site1"]'
        self.mocked_obj.shell = MagicMock(return_value=Response(get_sys_message))
        self.assertEqual(validate_appqoe_metric_syslog(self.mocked_obj, message='PASSIVE', syslog_mode="structured",
                                                      file="/var/tmp/syslog_test.txt", source_address="40.1.1.2",
                                                      source_port="36051",
                                                      destination_address="40.1.1.1", destination_port="36050",
                                                      destination_interface="gr-0/0/0.0", get=1), sys_message)

        try:
            x = validate_appqoe_metric_syslog()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            x = validate_appqoe_metric_syslog(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'message' is a mandatory argument")

        try:
            x = validate_appqoe_metric_syslog(device=self.mocked_obj,message='SOME', syslog_mode="structured",
                                                      file="/var/tmp/syslog_test.txt", source_address="40.1.1.2",
                                                      source_port="36051",
                                                      destination_address="40.1.1.1", destination_port="36050",
                                                      destination_interface="gr-0/0/0.0", get=1)
        except Exception as err:
            self.assertEqual(err.args[0], "'message' can have 'PASSIVE' or 'ACTIVE' as their value")
        try:
            x = validate_appqoe_metric_syslog(device=self.mocked_obj,message='SOME', syslog_mode="diff_mode",
                                                      file="/var/tmp/syslog_test.txt", source_address="40.1.1.2",
                                                      source_port="36051",
                                                      destination_address="40.1.1.1", destination_port="36050",
                                                      destination_interface="gr-0/0/0.0", get=1)
        except Exception as err:
            self.assertEqual(err.args[0], "INVALID syslog mode")

    @patch('jnpr.toby.utils.linux.syslog_utils.check_syslog')
    def test_validate_appqoe_path_violation_syslog(self, chk_syslog):
        chk_syslog.return_value = True
        sys_message = '<14>1 2018-03-29T21:58:46.934+05:30 srxdpi-skpai-spoke RT_FLOW - APPQOE_ACTIVE_SLA_METRIC_REPORT '+\
                      '[junos@2636.1.1.1.2.129 source-address="41.1.1.2" source-port="36051" destination-address="41.1.1.1" '+\
                      'destination-port="36050" application="UDP" protocol-id="17" destination-zone-name="untrust" ' +\
                      'routing-instance="appqoe-vrf" destination-interface-name="gr-0/0/0.1" ip-dscp="6" ingress-jitter="110" '+\
                      'egress-jitter="77" rtt-jitter="151" rtt="1850" pkt-loss="0" bytes-from-client="82320" bytes-from-server="35904" '+\
                      'packets-from-client="420" packets-from-server="374" monitoring-time="30" active-probe-params="probe1" destination-group-name="site1"]'
        self.mocked_obj.shell = MagicMock(return_value=Response(sys_message))
        self.assertTrue(validate_appqoe_path_violation_syslog(self.mocked_obj, message="APPQOE_SLA_METRIC_VIOLATION", syslog_mode="structured",
                                              file="/var/tmp/syslog_test.txt", source_address="41.1.1.2",
                                              source_port="36051",
                                              destination_address="41.1.1.1", destination_port="36050",
                                              destination_interface="gr-0/0/0.0"))

        best_path_message = '<14>1 2018-03-29T21:58:44.681+05:30 srxdpi-skpai-spoke RT_FLOW - APPQOE_BEST_PATH_SELECTED '+\
                            '[junos@2636.1.1.1.2.129 source-address="19.0.0.2" source-port="51223" destination-address="9.0.0.2" '+\
                            'destination-port="250" apbr-profile="apbr1" apbr-rule="rule1" application="HTTP" nested-application="YAHOO" '+\
                            'group-name="N/A" service-name="None" protocol-id="6" source-zone-name="trust" destination-zone-name="untrust" '+\
                            'session-id-32="377" username="N/A" roles="N/A" routing-instance="appqoe-vrf" destination-interface-name="gr-0/0/0.1" '+\
                            'ip-dscp="0" sla-rule="sla1" elapsed-time="152" bytes-from-client="1824" bytes-from-server="778" packets-from-client="12" '+\
                            'packets-from-server="13" previous-interface="gr-0/0/0.0" active-probe-params="probe1" destination-group-name="site1" reason="path switch"]'
        self.mocked_obj.shell = MagicMock(return_value=Response(best_path_message))
        self.assertTrue(validate_appqoe_path_violation_syslog(self.mocked_obj, message="APPQOE_BEST_PATH_SELECTED", syslog_mode="structured",
                                              file="/var/tmp/syslog_test.txt", source_address="19.0.0.2",
                                              source_port="51223",
                                              destination_address="9.0.0.2", destination_port="250",
                                              previous_interface="gr-0/0/0.0"))

        chk_syslog.return_value = True
        get_sys_message = '<14>1 2018-03-29T21:58:46.934+05:30 srxdpi-skpai-spoke RT_FLOW - APPQOE_ACTIVE_SLA_METRIC_REPORT '+\
                      '[junos@2636.1.1.1.2.129 source-address="41.1.1.2" source-port="36051" destination-address="41.1.1.1" '+\
                      'destination-port="36050" application="UDP" protocol-id="17" destination-zone-name="untrust" ' +\
                      'routing-instance="appqoe-vrf" destination-interface-name="gr-0/0/0.1" ip-dscp="6" ingress-jitter="110" '+\
                      'egress-jitter="77" rtt-jitter="151" rtt="1850" pkt-loss="0" bytes-from-client="82320" bytes-from-server="35904" '+\
                      'packets-from-client="420" packets-from-server="374" monitoring-time="30" active-probe-params="probe1" destination-group-name="site1"]'+\
                      ' \n' + '<14>1 2018-03-29T21:58:46.934+05:30 srxdpi-skpai-spoke RT_FLOW - APPQOE_ACTIVE_SLA_METRIC_REPORT '+\
                      '[junos@2636.1.1.1.2.129 source-address="41.1.1.2" source-port="36051" destination-address="41.1.1.1" '+\
                      'destination-port="36050" application="UDP" protocol-id="17" destination-zone-name="untrust" ' +\
                      'routing-instance="appqoe-vrf" destination-interface-name="gr-0/0/0.1" ip-dscp="6" ingress-jitter="110" '+\
                      'egress-jitter="77" rtt-jitter="151" rtt="1850" pkt-loss="0" bytes-from-client="82320" bytes-from-server="35904" '+\
                      'packets-from-client="420" packets-from-server="374" monitoring-time="30" active-probe-params="probe1" destination-group-name="site1"]'

        self.mocked_obj.shell = MagicMock(return_value=Response(get_sys_message))
        self.assertEqual(validate_appqoe_path_violation_syslog(self.mocked_obj, message="APPQOE_SLA_METRIC_VIOLATION", syslog_mode="structured",
                                              file="/var/tmp/syslog_test.txt", source_address="41.1.1.2",
                                              source_port="36051",
                                              destination_address="41.1.1.1", destination_port="36050",
                                              destination_interface="gr-0/0/0.0", get=1), sys_message)

        try:
            x = validate_appqoe_path_violation_syslog()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            x = validate_appqoe_path_violation_syslog(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'message' is a mandatory argument")

        try:
            x = validate_appqoe_path_violation_syslog(device=self.mocked_obj, message='SOME', syslog_mode="structured",
                                              file="/var/tmp/syslog_test.txt", source_address="40.1.1.2",
                                              source_port="36051",
                                              destination_address="40.1.1.1", destination_port="36050",
                                              destination_interface="gr-0/0/0.0")
        except Exception as err:
            self.assertEqual(err.args[0], "INVALID message value")
        try:
            x = validate_appqoe_path_violation_syslog(device=self.mocked_obj, message='APPQOE_SLA_METRIC_VIOLATION', syslog_mode="diff_mode",
                                              file="/var/tmp/syslog_test.txt", source_address="40.1.1.2",
                                              source_port="36051",
                                              destination_address="40.1.1.1", destination_port="36050",
                                              destination_interface="gr-0/0/0.0", get=1)
        except Exception as err:
            self.assertEqual(err.args[0], "INVALID syslog mode")

    @patch('jnpr.toby.utils.linux.syslog_utils.check_syslog')
    def test_validate_appqoe_apptrack_syslog(self, chk_syslog):
        chk_syslog.return_value = True
        close_message = '<14>1 2018-03-29T22:08:12.707+05:30 srxdpi-skpai-spoke RT_FLOW - APPTRACK_SESSION_CLOSE [junos@2636.1.1.1.2.129 '+\
                        'source-address="42.1.1.2" source-port="36051" destination-address="42.1.1.1" destination-port="36050" application="UDP" '+\
                        'protocol-id="17" destination-zone-name="untrust" routing-instance="appqoe-vrf" destination-interface-name="gr-0/0/0.2" '+\
                        'ip-dscp="6" ingress-jitter="86" egress-jitter="194" rtt-jitter="232" rtt="182113" pkt-loss="16" bytes-from-client="124608" '+\
                        'bytes-from-server="26208" packets-from-client="354" packets-from-server="273" monitoring-time="30" active-probe-params="probe1" '+\
                        'destination-group-name="site1"]'
        self.mocked_obj.shell = MagicMock(return_value=Response(close_message))
        #import pdb
        #pdb.set_trace()
        self.assertTrue(validate_appqoe_apptrack_syslog(device=self.mocked_obj, message="CLOSE", file="/tmp/abc.txt",
                                        source_address="19.0.0.2",
                                        destination_address="9.0.0.2",
                                        syslog_mode="structured",
                                        application="HTTP"))

        #get=1
        get_close_message = '<14>1 2018-03-29T22:08:12.707+05:30 srxdpi-skpai-spoke RT_FLOW - APPTRACK_SESSION_CLOSE [junos@2636.1.1.1.2.129 '+\
                        'source-address="42.1.1.2" source-port="36051" destination-address="42.1.1.1" destination-port="36050" application="UDP" '+\
                        'protocol-id="17" destination-zone-name="untrust" routing-instance="appqoe-vrf" destination-interface-name="gr-0/0/0.2" '+\
                        'ip-dscp="6" ingress-jitter="86" egress-jitter="194" rtt-jitter="232" rtt="182113" pkt-loss="16" bytes-from-client="124608" '+\
                        'bytes-from-server="26208" packets-from-client="354" packets-from-server="273" monitoring-time="30" active-probe-params="probe1" '+\
                        'destination-group-name="site1"]\n' + \
                         '<14>1 2018-03-29T22:08:12.707+05:30 srxdpi-skpai-spoke RT_FLOW - APPTRACK_SESSION_CLOSE [junos@2636.1.1.1.2.129 '+\
                        'source-address="42.1.1.2" source-port="36051" destination-address="42.1.1.1" destination-port="36050" application="UDP" '+\
                        'protocol-id="17" destination-zone-name="untrust" routing-instance="appqoe-vrf" destination-interface-name="gr-0/0/0.2" '+\
                        'ip-dscp="6" ingress-jitter="86" egress-jitter="194" rtt-jitter="232" rtt="182113" pkt-loss="16" bytes-from-client="124608" '+\
                        'bytes-from-server="26208" packets-from-client="354" packets-from-server="273" monitoring-time="30" active-probe-params="probe1" '+\
                        'destination-group-name="site1"]'
        self.mocked_obj.shell = MagicMock(return_value=Response(get_close_message))
        self.assertEqual(validate_appqoe_apptrack_syslog(device=self.mocked_obj, message="CLOSE", file="/tmp/abc.txt",
                                                        source_address="19.0.0.2",
                                                        destination_address="9.0.0.2",
                                                        syslog_mode="structured",
                                                        application="HTTP", get=1), close_message)

        try:
            x = validate_appqoe_apptrack_syslog()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            x = validate_appqoe_apptrack_syslog(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'message' is a mandatory argument")
