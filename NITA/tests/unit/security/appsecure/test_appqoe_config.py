import unittest2 as unittest
from mock import MagicMock
#from jnpr.toby.hldcl.juniper.security.srx import Srx
from jnpr.toby.hldcl.device import Device
from jnpr.toby.security.appsecure.appqoe_config import *


class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=Device)
    mocked_obj.log = MagicMock()

    def test_configure_sla_rule(self):
        self.mocked_obj.config = MagicMock(return_value=True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertTrue(configure_sla_rule(device=self.mocked_obj, sla_rule="sla_rule1", metrics_profile="profile1",
                            sampling_percentage="5", sampling_period="1000",
                            sla_export_factor="10", violation_count="10",
                            packet_loss_timeout ="500", max_outstanding_probe_requests="10",
                            switch_idle_time="10", passive_probe_params='1', active_probe_params='1'))

        try:
            x = configure_sla_rule(sla_rule='sla_rule1')
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

        try:
            x = configure_sla_rule(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "SLA rule name is a mandatory argument")

        try:
            x = configure_sla_rule(device=self.mocked_obj, sla_rule="sla_rule1")
        except Exception as err:
            self.assertEqual(err.args[0], "Metrics profile is a mandatory argument")

        try:
            x = configure_sla_rule(device=self.mocked_obj, sla_rule="sla_rule1", metrics_profile="profile1")
        except Exception as err:
            self.assertEqual(err.args[0], "Active probe params is a mandatory argument")


    def test_configure_active_probe_params(self):
        self.mocked_obj.config = MagicMock(return_value=True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertTrue(configure_active_probe(device=self.mocked_obj, probe_params="probe1", data_fill="juniper",
                                 data_size="100", probe_interval="5",
                                 probe_count="10", burst_size="10",
                                 sla_export_interval="60", dscp_code_points="000110"))

        try:
            x = configure_active_probe(probe_params="probe1")
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

        try:
            x = configure_active_probe(device=self.mocked_obj, data_size="100", probe_interval="3")
        except Exception as err:
            self.assertEqual(err.args[0], "Active probe setting name is mandatory")

        try:
            x = configure_active_probe(device=self.mocked_obj, probe_params="probe1")
        except Exception as err:
            self.assertEqual(err.args[0], "Data fill is mandatory")

        try:
            x = configure_active_probe(device=self.mocked_obj, probe_params="probe1", data_fill="juniper")
        except Exception as err:
            self.assertEqual(err.args[0], "Data size is mandatory")


    def test_configure_sla_options(self):
        self.mocked_obj.config = MagicMock(return_value=True)
        self.mocked_obj.commit = MagicMock(return_value=True)

        self.assertTrue(configure_sla_options(device=self.mocked_obj, sla_options=1,
                              local_route_switch="enabled"))

        self.assertTrue(configure_sla_options(device=self.mocked_obj, sla_options=1,
                              local_route_switch="disabled"))

        try:
            x = configure_sla_options(sla_options=1)
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

        self.assertTrue(configure_sla_options(device=self.mocked_obj))

    def test_configure_metrics_profile(self):
        self.mocked_obj.config = MagicMock(return_value=True)
        self.mocked_obj.commit = MagicMock(return_value=True)

        self.assertTrue(configure_metrics_profile(device=self.mocked_obj, metrics_profile="metric1", delay_round_trip="10000",
                            jitter="1000", jitter_type="ingress-jitter/egress-jitter/two-way-jitter",
                            match="all/any", packet_loss="5"))

        self.assertTrue(configure_metrics_profile(device=self.mocked_obj, metrics_profile="metric1", mode="delete", commit=False))

        try:
            x = configure_metrics_profile(probe_params="probe1")
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

        try:
            x = configure_metrics_profile(device=self.mocked_obj, data_size="100", delay_round_trip="3")
        except Exception as err:
            self.assertEqual(err.args[0], "Metrics profile is a mandatory argument")

