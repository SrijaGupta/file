import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security.applications import applications
from jnpr.toby.hldcl.juniper.security.srx import Srx


class UnitTest(unittest.TestCase):
    # Mocking the device handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_configure_single_application_0(self):
        self.assertRaises(Exception, applications.configure_single_application)
        self.assertRaises(Exception, applications.configure_single_application, device=self.mocked_obj)
        self.assertRaises(Exception, applications.configure_single_application, device=self.mocked_obj,
                          application_name='app')

    def test_configure_single_application_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(applications.configure_single_application(device=self.mocked_obj, application_name='app',
                                                                   logical_systems='l1', term=' ', alg=' ',
                                                                   destination_port=' ', icmp_code='', icmp_type=' ',
                                                                   icmp6_code=' ', icmp6_type=' ',
                                                                   inactivity_timeout=' ', protocol=' ',
                                                                   rpc_program_number=' ', source_port=' ', uuid=' ',
                                                                   commit=False), True)
        self.assertEqual(applications.configure_single_application(device=self.mocked_obj, application_name='app',
                                                                   application_protocol=' ', ether_type= ' ',
                                                                   destination_port=' ', icmp_code='', icmp_type=' ',
                                                                   icmp6_code=' ', icmp6_type=' ',
                                                                   inactivity_timeout=' ', protocol=' ',
                                                                   rpc_program_number=' ', source_port=' ', uuid=' ',
                                                                   commit=False), True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(applications.configure_single_application(device=self.mocked_obj, application_name='app',
                                                                   application_protocol=' ', ether_type=' ',
                                                                   destination_port=' ', icmp_code='', icmp_type=' ',
                                                                   icmp6_code=' ', icmp6_type=' ',
                                                                   inactivity_timeout=' ', protocol=' ',
                                                                   rpc_program_number=' ', source_port=' ', uuid=' ',
                                                                   commit=True), True)

    def test_configure_application_set_0(self):
        self.assertRaises(Exception, applications.configure_application_set)
        self.assertRaises(Exception, applications.configure_application_set,
                          device=self.mocked_obj)
        self.assertRaises(Exception, applications.configure_application_set,
                          device=self.mocked_obj, application_set_name='a1')
        self.assertRaises(Exception, applications.configure_application_set,
                          device=self.mocked_obj, application_set_name='a1', applications='qwe')
        self.assertRaises(Exception, applications.configure_application_set,
                          device=self.mocked_obj, application_set_name='a1', applications=[])

    def test_configure_application_set_1(self):
        self.mocked_obj.config = MagicMock()
        self.assertEqual(applications.configure_application_set(device=self.mocked_obj, application_set_name=' ',
                                                                applications=[' '], logical_systems=' ', commit=False),
                         True)
        self.assertEqual(applications.configure_application_set(device=self.mocked_obj, application_set_name=' ',
                                                                applications=[' ', ' '], commit=False),
                         True)
        self.mocked_obj.commit = MagicMock(return_value=True)
        self.assertEqual(applications.configure_application_set(device=self.mocked_obj, application_set_name=' ',
                                                                applications=[' ', ' '], commit=True),
                         True)


if __name__ == '__main__':
    unittest.main()
