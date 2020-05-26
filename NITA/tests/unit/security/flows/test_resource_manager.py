import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.flows import resource_manager
from jnpr.toby.hldcl.juniper.security.srx import Srx


class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_verify_resource_manager_0(self):
        self.assertRaises(Exception, resource_manager.verify_resource_manager)
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj)
        xml_output = Response("<rpc-reply><resmgr-settings><active-client-count>1</active-client-count>" \
                     "</resmgr-settings></rpc-reply>")
        self.mocked_obj.cli = MagicMock(return_value=xml_output)
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj, setting=True)

    def test_verify_resource_manager_1(self):
        # Setting if case
        xml_output = Response("<rpc-reply><resmgr-settings><resmgr-settings-timeout>1</resmgr-settings-timeout>"
                              "<resmgr-settings-count>2</resmgr-settings-count><resmgr-settings-pinhole-age>2"
                              "</resmgr-settings-pinhole-age></resmgr-settings></rpc-reply>")
        self.mocked_obj.cli = MagicMock(return_value=xml_output)
        self.assertEquals(resource_manager.verify_resource_manager(device=self.mocked_obj, setting=True,
                          setting_timeout='1', setting_count='2', setting_pinhole_age='2'), True)
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj, setting=True,
                          setting_timeout='20', setting_count='11', setting_pinhole_age='34')

        # Summary if case
        xml_output = Response("<rpc-reply><resource-manager-summary-information><active-client-count>1"
                              "</active-client-count><active-group-count>1</active-group-count><active-resource-count>1"
                              "</active-resource-count><active-session-count>1</active-session-count>"
                              "</resource-manager-summary-information></rpc-reply>")
        self.mocked_obj.cli = MagicMock(return_value=xml_output)
        self.assertEquals(resource_manager.verify_resource_manager(device=self.mocked_obj, summary=True,
                          resource_count='1', client_count='1', session_count='1', group_count='1'), True)
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj, summary=True,
                          resource_count='2', client_count='2', session_count='2', group_count='2')

        # Resource if case
        xml_output = Response("<rpc-reply><resmgr-resource-active><resmgr-resource-active-data>"
                              "<resmgr-resource-active-data-res-id>1</resmgr-resource-active-data-res-id>"
                              "<resmgr-resource-active-data-grp-id>1</resmgr-resource-active-data-grp-id>"
                              "<resmgr-resource-active-data-client>A</resmgr-resource-active-data-client>"
                              "</resmgr-resource-active-data><resmgr-resource-active-data>"
                              "<resmgr-resource-active-data-res-id>2</resmgr-resource-active-data-res-id>"
                              "<resmgr-resource-active-data-grp-id>2</resmgr-resource-active-data-grp-id>"
                              "<resmgr-resource-active-data-client>B</resmgr-resource-active-data-client>"
                              "</resmgr-resource-active-data>"
                              "<resmgr-resource-active-total>1</resmgr-resource-active-total>"
                              "<resmgr-resource-active-count>1</resmgr-resource-active-count>"
                              "</resmgr-resource-active></rpc-reply>")
        self.mocked_obj.cli = MagicMock(return_value=xml_output)
        self.assertEquals(resource_manager.verify_resource_manager(device=self.mocked_obj,
                                                                   resource='active', resource_count='1',
                                                                   resource_total='1', resource_id='1', group_id='1',
                                                                   client='A'), True)
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj, resource='active',
                          resource_count='2', resource_total='2', resource_id='9', group_id='9', client='X')
        self.assertEquals(resource_manager.verify_resource_manager(device=self.mocked_obj, resource='active',
                          resource_id='2', group_id='2', client='B'), True)
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj, resource='active',
                          resource_id='1', group_id='1', client='B')
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj, resource='active',
                          resource_id='1', group_id='2', client='A')
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj, resource='active',
                          resource_id='2', group_id='1', client='A')
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj, resource='active',
                          resource_id='3', group_id='2', client='B')
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj, resource='active',
                          resource_id='2', group_id='3', client='B')
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj, resource='active',
                          resource_id='2', group_id='2', client='A')
        xml_output = Response("<rpc-reply><resmgr-resource-active><resmgr-resource-active-data>"
                              "<resmgr-resource-active-data-res-id>1</resmgr-resource-active-data-res-id>"
                              "<resmgr-resource-active-data-grp-id>1</resmgr-resource-active-data-grp-id>"
                              "<resmgr-resource-active-data-client>A</resmgr-resource-active-data-client>"
                              "</resmgr-resource-active-data>"
                              "<resmgr-resource-active-total>1</resmgr-resource-active-total>"
                              "<resmgr-resource-active-count>1</resmgr-resource-active-count>"
                              "</resmgr-resource-active></rpc-reply>")
        self.mocked_obj.cli = MagicMock(return_value=xml_output)
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj,
                          resource='active', resource_id='2', group_id='2', client='A')

        # GROUP IF CASE
        xml_output = Response("<rpc-reply><resmgr-group-active><resmgr-group-active-data>"
                              "<resmgr-group-active-data-grp-id>1</resmgr-group-active-data-grp-id>"
                              "<resmgr-group-active-data-client>A</resmgr-group-active-data-client>"
                              "</resmgr-group-active-data><resmgr-group-active-data>"
                              "<resmgr-group-active-data-grp-id>2</resmgr-group-active-data-grp-id>"
                              "<resmgr-group-active-data-client>B</resmgr-group-active-data-client>"
                              "</resmgr-group-active-data>"
                              "<resmgr-group-active-total>1</resmgr-group-active-total>"
                              "<resmgr-group-active-count>1</resmgr-group-active-count>"
                              "</resmgr-group-active></rpc-reply>")
        self.mocked_obj.cli = MagicMock(return_value=xml_output)
        self.assertEquals(resource_manager.verify_resource_manager(device=self.mocked_obj,
                                                                   group='active', group_count='1',
                                                                   group_total='1', group_id='1',
                                                                   client='A'), True)
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj,
                          group='active',
                          group_count='2', group_total='2', group_id='9', client='X')
        self.assertEquals(resource_manager.verify_resource_manager(device=self.mocked_obj, group='active',
                                                                   group_id='2', client='B'), True)
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj,
                          group='active',
                          group_id='1', client='B')
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj,
                          group='active',
                          group_id='2', client='A')
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj,
                          group='active',
                          group_id='1', client='C')
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj,
                          group='active',
                          group_id='2', client='C')
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj,
                          group='active',
                          group_id='3', client='B')
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj,
                          group='active',
                          group_id='2', client='A')
        xml_output = Response("<rpc-reply><resmgr-group-active><resmgr-group-active-data>"
                              "<resmgr-group-active-data-res-id>1</resmgr-group-active-data-res-id>"
                              "<resmgr-group-active-data-grp-id>1</resmgr-group-active-data-grp-id>"
                              "<resmgr-group-active-data-client>A</resmgr-group-active-data-client>"
                              "</resmgr-group-active-data>"
                              "<resmgr-group-active-total>1</resmgr-group-active-total>"
                              "<resmgr-group-active-count>1</resmgr-group-active-count>"
                              "</resmgr-group-active></rpc-reply>")
        self.mocked_obj.cli = MagicMock(return_value=xml_output)
        self.assertRaises(Exception, resource_manager.verify_resource_manager, device=self.mocked_obj,
                          group='active', group_id='1', client='B')

if __name__ == '__main__':
    unittest.main()
