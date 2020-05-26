import sys

import unittest2 as unittest
from lxml import etree
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from jnpr.toby.hldcl.juniper.routing.mxvc import MxVc

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

routing_engines = etree.XML('''<multi-routing-engine-results>
        <multi-routing-engine-item><re-name>member0</re-name>
        <route-engine-information><route-engine><slot>0</slot>
        <mastership-state>master</mastership-state>
        </route-engine><route-engine><slot>1</slot>
        <mastership-state>backup</mastership-state></route-engine>
        </route-engine-information></multi-routing-engine-item>
        <multi-routing-engine-item><re-name>member1</re-name>
        <route-engine-information><route-engine><slot>0</slot>
        <mastership-state>master</mastership-state>
        </route-engine><route-engine><slot>1</slot>
        <mastership-state>backup</mastership-state></route-engine>
        </route-engine-information></multi-routing-engine-item>
        </multi-routing-engine-results>''')

@attr('unit')
class TestMxVc(unittest.TestCase):
    @patch('logging.FileHandler')
    def test_mxvc_init_failures(self, file_handler_mock):
        # No host provided
        self.assertRaises(Exception, MxVc)
        # host given in args and user name password not specified
        self.assertRaises(Exception, MxVc, 'device1')
        # dual_re and routing_engine set
        self.assertRaises(Exception, MxVc, host='device', dual_re=True,
                          routing_engine='master')

    """
    Below unit tests are not valid for new MXVC API. 
    
    @patch('jnpr.toby.hldcl.juniper.routing.mx.MxVc.open')
    @patch('logging.FileHandler')
    @patch(builtin_string + ".super")
    def test_mxvc_init(self, super_mock, popen, log_mock):
        self.assertIsInstance(MxVc('device1', os='junos', host='test',user='test', password='test123'), MxVc)
        self.ins = MxVc('device1', os='junos', host='test',user='test', password='test123')
        #result = self.ins.rpc._getattribute__(item='test',a='1',b='2')
    def test_mxvc_open(self):
        jobject = MagicMock(spec=MxVc)
        jobject._vc_info = MagicMock()
        jobject._connect = MagicMock()
        jobject._replace_object = MagicMock()
        jobject._get_shell_connection = MagicMock()
        jobject._kwargs = MagicMock()
        jobject.connected = True
        # strict is set
        MxVc.open(jobject)
        self.assertTrue(jobject.connected)
        # strict not set
        #jobject = MagicMock()
        jobject._kwargs.get = MagicMock(return_value=None)
        jobject._can_get_vc_info = MagicMock(return_value=None)
        jobject._get_master_re = MagicMock(return_value='MEMBER0-RE0')
        jobject._vc_info = MagicMock(side_effect=[None])
        jobject.MEMBER0_RE0 = MagicMock()
        jobject.MEMBER0_RE0._get_virual_chassis_info = MagicMock(return_value=None)
        jobject._get_members_info = MagicMock(return_value=None)
        self.assertRaises(AttributeError, MxVc.open, jobject)

        # strict is not set
        jobject._kwargs = {'dual_re': True, 'routing_engine': 'master'}
        jobject._get_master_member_info = MagicMock(return_value={'id': '0'})
        jobject._get_members_info = MagicMock(return_value={'member0': {'master': '0'}})
        jobject.MEMBER0_RE0 = MagicMock()
        self.assertTrue(MxVc.open(jobject))

    def test_mxvc_get_re_slot_name(self):
        jobject = MagicMock(spec=MxVc)
        xmldata = etree.XML(
            '<virtual-chassis-information><member-list><member><member-status>'
            'Prsnt</member-status><member-id>0</member-id><member-role>Backup*'
            '</member-role></member><member><member-status>Prsnt'
            '</member-status><member-id>1</member-id><member-role>Master'
            '</member-role></member></member-list>'
            '</virtual-chassis-information>')
        jobject.handle = MagicMock()
        jobject.handle.rpc.get_virtual_chassis_information = \
            MagicMock(return_value=xmldata)

        # other re info is wrong
        jobject._get_other_re_list = MagicMock(return_value=['member0-re12', 'member1-re12'])
        jobject._get_connected_member_info = MagicMock(return_value={'id': '0', 'role': 'master'})
        self.assertRaises(Exception, MxVc._get_re_slot_name, jobject)

        # connected to re0
        jobject._get_other_re_list = MagicMock(return_value=['member0-re1', 'member1-re1'])
        jobject._get_connected_member_info = MagicMock(return_value={'id': '0', 'role': 'master'})
        self.assertEqual(MxVc._get_re_slot_name(jobject), 'member0-re0')

        # connected to re1
        jobject._get_other_re_list = MagicMock(return_value=['member0-re0', 'member1-re0'])
        self.assertEqual(MxVc._get_re_slot_name(jobject), 'member0-re1')

        # other re is not operational which means other_re_list is empty
        # and all re list is empty
        jobject._get_other_re_list = MagicMock(return_value=[])
        self.assertRaises(Exception, MxVc._get_re_slot_name, jobject)

        # other re is not operational which means other_re_list is empty
        # and all re is not empty
        jobject._get_re_list = MagicMock(return_value=['member0-re0'])
        self.assertEqual(MxVc._get_re_slot_name(jobject), 'member0-re0')

    def test_mxvc_re_slot_name(self):
        jobject = MagicMock(spec=MxVc)
        jobject.re = 'member1-re12'
        self.assertEqual(MxVc.re_slot_name(jobject), 'MEMBER1-RE12')

    def test_mxvc_get_members_info(self):
        jobject = MagicMock(spec=MxVc)
        jobject.handle = MagicMock()
        jobject.handle.rpc.get_route_engine_information = \
            MagicMock(return_value=routing_engines)
        self.assertEqual(MxVc._get_members_info(jobject),
                         {'member0': {'master': '0', 'backup': '1'},
                          'member1': {'master': '0', 'backup': '1'}
                          }
        )

    @patch('jnpr.toby.hldcl.juniper.routing.mx.MxVc')
    def test_mxvc_connect_all_member_re_of_role(self, pmxvc):
        jobject = MagicMock(spec=MxVc)
        jobject._create_other_re_kwargs = MagicMock()
        jobject._kwargs = {}
        jobject.re = 'MEMBER0-RE0'
        jobject._get_members_info = MagicMock(
            return_value={'member0': {'master': '0', 'backup': '1'},
                          'member1': {'master': '0', 'backup': '1'}
                          }
        )
        self.assertTrue(MxVc._connect_all_member_re_of_role(jobject, 'master'))
        # vc_info is not None
        jobject.re = 'member0-re0'
        self.assertTrue(MxVc._connect_all_member_re_of_role(jobject, 'master', vc_info=True))

    def test_mxvc_connect_all_member_re_of_role_failures(self):
        jobject = MagicMock(spec=MxVc)
        jobject._get_members_info = MagicMock(
            return_value={'member0': {'master': '0', 'backup': '1'},
                          'member1': {'master': '0', 'backup': '1'}
                          }
        )
        self.assertFalse(
            MxVc._connect_all_member_re_of_role(jobject, 'master'))

    def test_mxvc_create_other_re_kwargs(self):
        jobject = MagicMock(spec=MxVc)
        jobject._get_connection_element = MagicMock(return_value='othername')
        kwargs = {'handle': True}
        other_re_kwargs = MxVc._create_other_re_kwargs(jobject, kwargs, 'member0-re1')
        self.assertEqual(other_re_kwargs.get('handle'), None)
        self.assertEqual(other_re_kwargs['host'], 'othername')

    def test_mxvc_get_connection_element(self):
        jobject = MagicMock(spec=MxVc)

        # jobject.host is a host name
        jobject.host = 'test'
        jobject._get_host_name = MagicMock(return_value='test1')
        self.assertEqual(MxVc._get_connection_element(jobject, 'member0-re1'),
                         'test1')
        # host names are equal
        jobject._get_host_ip = MagicMock(return_value='1.1.1.2')
        jobject._get_host_name = MagicMock(return_value='test')
        self.assertEqual(MxVc._get_connection_element(jobject, 'member0-re1'),
                         '1.1.1.2')
        #jobject.host is ip
        jobject.host = '1.1.1.1'
        jobject._get_host_ip = MagicMock(return_value='1.1.1.2')
        self.assertEqual(MxVc._get_connection_element(jobject, 'member0-re1'),
                         '1.1.1.2')

    def test_mxvc_get_virual_chassis_info(self):
        jobject = MagicMock(spec=MxVc)
        jobject.handle = MagicMock()
        jobject.handle.rpc.get_virtual_chassis_information = MagicMock(
            return_value='vc_ch_info'
        )
        self.assertEqual(MxVc._get_virual_chassis_info(jobject), 'vc_ch_info')
        jobject.handle.rpc.get_virtual_chassis_information = MagicMock(
            side_effect=Exception
        )
        self.assertEqual(MxVc._get_virual_chassis_info(jobject), None)

    def test_mxvc_get_master_member_info(self):
        jobject = MagicMock(spec=MxVc)
        xmldata = etree.XML(
            '<virtual-chassis-information><member-list><member><member-status>'
            'Prsnt</member-status><member-id>0</member-id><member-role>Backup*'
            '</member-role></member><member><member-status>Prsnt'
            '</member-status><member-id>1</member-id><member-role>Master'
            '</member-role></member></member-list>'
            '</virtual-chassis-information>')
        jobject.handle = MagicMock()
        jobject.handle.rpc.get_virtual_chassis_information = \
            MagicMock(return_value=xmldata)
        self.assertEqual(MxVc._get_master_member_info(jobject),
                         {'id': '1', 'role': 'master'})
        # No master member info could be retrieved
        xmldata = etree.XML('<rpc></rpc>')
        jobject.handle.rpc.get_virtual_chassis_information = \
            MagicMock(return_value=xmldata)
        self.assertEqual(MxVc._get_master_member_info(jobject),
                         {})

    def test_mxvc_get_connected_member_info(self):
        jobject = MagicMock(spec=MxVc)
        xmldata = etree.XML(
            '<virtual-chassis-information><member-list><member><member-status>'
            'Prsnt</member-status><member-id>0</member-id><member-role>Backup*'
            '</member-role></member><member><member-status>Prsnt'
            '</member-status><member-id>1</member-id><member-role>Master'
            '</member-role></member></member-list>'
            '</virtual-chassis-information>')
        jobject.handle = MagicMock()
        jobject.handle.rpc.get_virtual_chassis_information = \
            MagicMock(return_value=xmldata)
        self.assertEqual(MxVc._get_connected_member_info(jobject),
                         {'id': '0', 'role': 'backup'})
        # No member info could be retrieved
        xmldata = etree.XML('<rpc></rpc>')
        jobject.handle.rpc.get_virtual_chassis_information = \
            MagicMock(return_value=xmldata)
        self.assertRaises(Exception, MxVc._get_connected_member_info, jobject)

    def test_mxvc_get_other_re_list(self):
        jobject = MagicMock(spec=MxVc)
        xmldata = etree.XML('''<multi-routing-engine-results>
        <multi-routing-engine-item><re-name>member0-re1</re-name>
        <software-information><host-name>coulson1</host-name>
        <product-model>mx240</product-model>
        </software-information></multi-routing-engine-item>
        <multi-routing-engine-item><re-name>member1-re1</re-name>
        <software-information><host-name>ultron1</host-name>
        <product-model>mx240</product-model></software-information>
        </multi-routing-engine-item></multi-routing-engine-results>''')
        jobject.cli.return_value.response = MagicMock(return_value=xmldata)

        self.assertEqual(MxVc._get_other_re_list(jobject),
                         ['MEMBER0-RE1', 'MEMBER1-RE1'])

    def test_mxvc_get_re_list(self):
        jobject = MagicMock(spec=MxVc)
        xmldata = etree.XML('''<multi-routing-engine-results>
        <multi-routing-engine-item><re-name>member0-re1</re-name>
        <software-information><host-name>coulson1</host-name>
        <product-model>mx240</product-model>
        </software-information></multi-routing-engine-item>
        <multi-routing-engine-item><re-name>member1-re1</re-name>
        <software-information><host-name>ultron1</host-name>
        <product-model>mx240</product-model></software-information>
        </multi-routing-engine-item></multi-routing-engine-results>''')
        jobject.cli.return_value.response = MagicMock(return_value=xmldata)
        self.assertEqual(MxVc._get_re_list(jobject),
                         ['MEMBER0-RE1', 'MEMBER1-RE1'])

    def test_mxvc_can_get_vc_info(self):
        jobject = MagicMock(spec=MxVc)
        jobject.handle = MagicMock()
        jobject.handle.rpc.get_virtual_chassis_information = MagicMock()
        self.assertTrue(MxVc._can_get_vc_info(jobject))
        jobject.handle.rpc.get_virtual_chassis_information = MagicMock(
            side_effect=Exception
        )
        self.assertFalse(MxVc._can_get_vc_info(jobject))

    def test_mxvc_get_master_re(self):
        jobject = MagicMock(spec=MxVc)
        jobject.handle = MagicMock()
        jobject.handle.rpc.get_route_engine_information = \
            MagicMock(return_value=routing_engines)
        self.assertEqual(MxVc._get_master_re(jobject, 'member0'),
                         'member0-re0')
   """

if __name__=='__main__':
    unittest.main()
