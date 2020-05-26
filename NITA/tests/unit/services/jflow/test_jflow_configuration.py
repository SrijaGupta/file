from jnpr.toby.services.jflow.jflow_configuration import jflow_configuration
from jnpr.toby.hldcl.unix.unix import UnixHost
from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from optparse import Values

import builtins
builtins.t = MagicMock()

class Test_jflow_configuration(unittest.TestCase):

    def setUp(self):
        device = MagicMock()
        self.jc = jflow_configuration()
        self.jc.dh = device
        self.jc.config = MagicMock()
        self.jc.commit = MagicMock()
        self.jc.config.return_value = True
        self.jc.commit.return_value = True
        builtins.t = MagicMock()

    def test_configure_inline_jflow(self):
        flow_collector_ips = ["20.50.1.2", "30.50.1.2"]
        flow_collector_src = "20.50.1.1"
        sampling_intf = "ge-1/1/1.0";
        self.assertEqual(self.jc.configure_inline_jflow(name="template_ipv4_1", template_type="ipv4",\
                template_version="10", flow_collector_ips=flow_collector_ips,\
                flow_collector_src=flow_collector_src, family="inet",\
                sampling_intf=sampling_intf), True)

    def test_configure_inline_jflow_configured_ids(self):
        flow_collector_ips = ["20.50.1.2", "30.50.1.2"]
        flow_collector_src = "20.50.1.1"
        sampling_intf = "ge-1/1/1.0";
        self.assertEqual(self.jc.configure_inline_jflow(name="template_ipv4_1", template_type="ipv4",\
                template_version="10", flow_collector_ips=flow_collector_ips,\
                flow_collector_src=flow_collector_src, family="inet",\
                sampling_intf=sampling_intf, option_refresh_packets='1',\
                option_refresh_seconds='60', template_refresh_seconds='60',\
                template_refresh_packets='1', vlan_flow_key='1',\
                oif_flow_key='1', direction_flow_key='1', configured_domain_id='10',\
                configured_template_id='1030', configured_option_template_id='1040', \
                enable_tunnel_observation='1', family_sampling_rate='1', \
                export_rate='100'), True)

if __name__ == '__main__':
    unittest.main()