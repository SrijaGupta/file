import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.infra import infra_routing
from jnpr.toby.hldcl.juniper.security.srx import Srx


# To return response of shell() method

class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_routing_options_0(self):
        self.assertRaises(Exception, infra_routing.configure_routing_options)
        self.assertRaises(Exception, infra_routing.configure_routing_options, device=self.mocked_obj,
                          interface_routes_rib_group=[0], static_route=[0], import_rib=[0])

    def test_routing_options_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(infra_routing.configure_routing_options(device=self.mocked_obj,
                                                                 interface_routes_rib_group=['inet', 'if-rib1'],
                                                                 static_rib_group='if-rib1',
                                                                 static_route=['13.13.0.0/16', '5.1.1.2'],
                                                                 import_rib=['if-rib1', 'inet.0'],
                                                                 commit=False), True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(infra_routing.configure_routing_options(device=self.mocked_obj,
                                                                 interface_routes_rib_group=['inet', 'if-rib1'],
                                                                 static_rib_group='if-rib1',
                                                                 static_route=['13.13.0.0/16', '5.1.1.2'],
                                                                 import_rib=['if-rib1', 'inet.0'],
                                                                 commit=True), True)

    def test_routing_instances_0(self):
        self.assertRaises(Exception, infra_routing.configure_routing_instances)
        self.assertRaises(Exception, infra_routing.configure_routing_instances, device=self.mocked_obj)
        self.assertRaises(Exception, infra_routing.configure_routing_instances, device=self.mocked_obj,
                          routing_instance_name='green', interface_routes_rib_group=[0])

    def test_routing_instances_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(infra_routing.configure_routing_instances(device=self.mocked_obj,
                                                                   routing_instance_name='green',
                                                                   routing_options=['inet', 'if-rib1'],
                                                                   commit=False), True)
        self.assertEqual(infra_routing.configure_routing_instances(device=self.mocked_obj,
                                                                   routing_instance_name='green',
                                                                   routing_options='inet',
                                                                   commit=False), True)
        self.assertEqual(infra_routing.configure_routing_instances(device=self.mocked_obj,
                                                                   routing_instance_name='green',
                                                                   instance_type='virtual-router',
                                                                   interface='fe-0/0/2.0',
                                                                   interface_routes_rib_group=['inet', 'if-rib1'],
                                                                   commit=False), True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(infra_routing.configure_routing_instances(device=self.mocked_obj,
                                                                   routing_instance_name='green',
                                                                   instance_type='virtual-router',
                                                                   interface='fe-0/0/2.0',
                                                                   interface_routes_rib_group=['inet', 'if-rib1'],
                                                                   commit=True), True)


if __name__ == '__main__':
    unittest.main()
