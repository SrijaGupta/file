import sys
import os
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from collections import OrderedDict, Mapping
from nose.plugins.attrib import attr
import builtins

builtins.t = MagicMock()
builtins.t.log.return_value = True

from jnpr.toby.engines.config.config_utils import *
from jnpr.toby.engines.config.config_utils import _make_number_list
from jnpr.toby.engines.config.config_utils import _make_string_list
from jnpr.toby.engines.config.config_utils import _make_ip_list
from jnpr.toby.engines.config.config_utils import _make_mixed_list
from jnpr.toby.engines.config.config_utils import _make_mac_list
from jnpr.toby.engines.config.config_utils import _make_esi_list



if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'


@attr('unit')
class TestConfigUtils(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = self
        builtins.t.log = MagicMock(return_value=True)

    @patch('builtins.open')
    @patch('jnpr.toby.engines.config.config_utils.find_file', return_value='test_string')
    @patch('jnpr.toby.engines.config.config_utils.yaml.load')
    def test_read_yaml_file(self, yaml_mock, find_file_mock, open_mock):

        yaml_mock.return_value = 'test_string';
        self.assertEqual(read_yaml(file='file'), 'test_string')
        self.assertTrue(open_mock.called)

        try:
            read_yaml(None)
        except Exception as err:
            self.assertEqual(err.args[0], "mandatory arg 'file' or 'string' is missing")

    
    def test__make_number_list(self):

        self.assertEqual(list(_make_number_list(first=1,count=2,last=10,repeat=2,cycle=2)),[1, 1])
        self.assertEqual(list(_make_number_list(first=1,count=2,last=10,repeat=2,cycle=None)),[1, 1])

        try:
            list(_make_number_list(first=1,last='doomed',repeat=2,cycle=2))
        except Exception as err:
            self.assertEqual(err.args[0], 'last value "doomed" is not a number: <class \'str\'>')

        try:
            list(_make_number_list(first=5,last=3,repeat=2,cycle=2))

        except Exception as err:
            self.assertEqual(err.args[0], "in <<5..3>> last value should be larger than first" )


    def test__make_string_list(self):
        self.assertEqual(list(_make_string_list(first='66toto34',count=2,step=1,last='toto34',repeat=2,cycle=2)),['66toto34', '66toto34'])
        self.assertEqual(list(_make_string_list(first='66toto34',count=1,step=1,last='toto34',repeat=2,cycle=2)), ['66toto34'])
        self.assertEqual(list(_make_string_list(first='toto',count=1,step=2,last='toto7',repeat=2,cycle=2)), ['toto'])
        self.assertEqual(list(_make_string_list(first='toto', count=3,step=0,last='toto7',repeat=2,cycle=2)),['toto0', 'toto0', 'toto0'])
        self.assertEqual(list(_make_string_list(first='toto', count=3,step=0,last=None,repeat=2,cycle=2)),['toto0', 'toto0', 'toto0'])
        self.assertEqual(list(_make_string_list(first='toto3',count=3,step=2, last='toto7',repeat=2,cycle=2)),['toto3', 'toto3', 'toto5'])
        self.assertEqual(list(_make_string_list(count=3)), list())

        try:
            list(_make_string_list( first= "123", count=3))
        except Exception as err:
            self.assertEqual(err.args[0], "_make_string_list: cannot parse the first element:123")

        list(_make_string_list(first='link2', count=3))
        
    @patch('logging.FileHandler')
    @patch('logging.getLogger')
    @patch('jnpr.toby.hldcl.juniper.junos.Host.log')       
    def test__make_ip_list(self, patch1, patch2, patch3):

        self.assertEqual(list(_make_ip_list(first='a',count=2,last=10,repeat=2,cycle=2)),[])
        self.assertEqual(list(_make_ip_list(first='8.8.8.8/23',count=2,last=None,repeat=2,cycle=2)), ['8.8.8.8/23', '8.8.8.8/23'])
        self.assertEqual(list(_make_ip_list(first='8.8.8.8/23',count=2,last='8.8.8.10/23',repeat=2,step=2)),['8.8.8.8/23', '8.8.8.8/23'])
        self.assertEqual(list(_make_ip_list(first='2001:db9::',count=2,repeat=2,step='/126')),['2001:db9::', '2001:db9::'])
        self.assertEqual(list(_make_ip_list(first='2001:db9::',count=2,repeat=2,step='::1')),['2001:db9::', '2001:db9::'])
        self.assertEqual(list(_make_ip_list(first='2001:db9::',count=2,repeat=2)),['2001:db9::', '2001:db9::'])
        self.assertEqual(list(_make_ip_list(first='8.8.8.8/23',count=1000,last='8.8.8.11/23',repeat=2,step=2)),['8.8.8.8/23', '8.8.8.8/23', '8.8.8.10/23', '8.8.8.10/23', '8.8.8.12/23'])
        self.assertEqual(list(_make_ip_list(first='8.8.8.8/23',count=4,last='8.8.8.11/23',repeat=2,step=2, cycle=2)),['8.8.8.8/23', '8.8.8.8/23', '8.8.8.10/23', '8.8.8.10/23'])
        self.assertEqual(list(_make_ip_list(first='8.8.8.8/23',count=4,last='8.8.8.11/23',repeat=2,step=2, cycle=2)),['8.8.8.8/23', '8.8.8.8/23', '8.8.8.10/23', '8.8.8.10/23'])
        self.assertEqual(list(_make_ip_list(first='8.8.8.8/23',count=4,last='8.8.8.11/23',repeat=2,step=2, cycle=1)), ['8.8.8.8/23', '8.8.8.8/23', '8.8.8.8/23', '8.8.8.8/23'])

        try:
            self.assertEqual(list(_make_ip_list(first='8.8.8.10/23',count=2,last='8.8.8.8/23',repeat=2,step=2)),['8.8.8.8/23', '8.8.8.8/23'])
        except Exception as err:
            self.assertEqual(err.args[0], "in <<8.8.8.10..8.8.8.8>> last value should be larger than first" )

        try:
            list(_make_ip_list(first='8.8.8.8',count=2,last=10,repeat=2,step='0.1.0.0/16'))
        except ValueError as err:
            self.assertEqual(err.args[0], "'0.1.0.0/16' does not appear to be an IPv4 or IPv6 address" )

        try:
            self.assertEqual(list(_make_ip_list(first='2001:db9::',count=2,last=10,repeat=2,step='a')),['66toto34', '66toto34'])
        except ValueError as err:
            self.assertEqual(err.args[0], "invalid literal for int() with base 10: 'a'" )

    def test__make_mac_list(self):
        self.assertEqual(list(_make_mac_list(first='05:06:07:08:09:f1',count=4)),['05:06:07:08:09:f1','05:06:07:08:09:f2','05:06:07:08:09:f3','05:06:07:08:09:f4'])
        self.assertEqual(list(_make_mac_list(first='00:00:00:00:00:00',count=2,last=10,repeat=2,cycle=2)),['00:00:00:00:00:00','00:00:00:00:00:00'])
        self.assertEqual(list(_make_mac_list(first='00:00:00:00:00:00',count=6,step=5,last=10,repeat=2,cycle=2)),['00:00:00:00:00:00','00:00:00:00:00:00','00:00:00:00:00:05','00:00:00:00:00:05','00:00:00:00:00:00','00:00:00:00:00:00'])
        self.assertEqual(list(_make_mac_list(first='00:00:00:00:01:1a',count=2,last=None)), ['00:00:00:00:01:1a','00:00:00:00:01:1b'])
        self.assertEqual(list(_make_mac_list(first='05:06:07:08:09:f1',count=4,step=2)),['05:06:07:08:09:f1','05:06:07:08:09:f3','05:06:07:08:09:f5','05:06:07:08:09:f7'])
        self.assertEqual(list(_make_mac_list(first='99:11:22:3f120:4',count=2,repeat=2,step='00:00:00:00:00:02')),[])

        try:
            self.assertEqual(list(_make_mac_list(first='11:11:11:11:11:11',count=2,last='00:00:00:00:00:00',repeat=2,step=2)),['11:11:11:11:11:11','11:11:11:11:11:11'])
        except Exception as err:
            self.assertEqual(err.args[0], "in <<11:11:11:11:11:11..00:00:00:00:00:00>> last value should be larger than first" )

    def test__make_esi_list(self):
        self.assertEqual(list(_make_esi_list(first='00:ff:ab:cd:ef:00:00:00:00:01',count=4,step=100)),['00:ff:ab:cd:ef:00:00:00:00:01','00:ff:ab:cd:ef:00:00:00:00:65','00:ff:ab:cd:ef:00:00:00:00:c9','00:ff:ab:cd:ef:00:00:00:01:2d'])
        self.assertEqual(list(_make_esi_list(first='00:0f:00:00:00:00:00:00:fe:01',count=2)),['00:0f:00:00:00:00:00:00:fe:01','00:0f:00:00:00:00:00:00:fe:02'])
        self.assertEqual(list(_make_esi_list(first='00:00:00:00:00:00:12:34:56:78',count=2,repeat=2,last=None)), ['00:00:00:00:00:00:12:34:56:78','00:00:00:00:00:00:12:34:56:78'])
        self.assertEqual(list(_make_esi_list(first='00:00:00:00:00:00:12:34:56:78',count=4,repeat=2,cycle=2,last=None)), ['00:00:00:00:00:00:12:34:56:78','00:00:00:00:00:00:12:34:56:78','00:00:00:00:00:00:12:34:56:79','00:00:00:00:00:00:12:34:56:79'])
        self.assertEqual(list(_make_esi_list(first='00:00:00:00:00:00:12:34:56:78',step=5,count=6,repeat=2,cycle=2,last=None)), ['00:00:00:00:00:00:12:34:56:78','00:00:00:00:00:00:12:34:56:78','00:00:00:00:00:00:12:34:56:7d','00:00:00:00:00:00:12:34:56:7d','00:00:00:00:00:00:12:34:56:78','00:00:00:00:00:00:12:34:56:78'])
        self.assertEqual(list(_make_esi_list(first='00:ff:00:77:00:00:12:12:fe:01',count=3,cycle=2,step='00:00:00:00:00:00:00:00:01:00')), ['00:ff:00:77:00:00:12:12:fe:01','00:ff:00:77:00:00:12:12:ff:01','00:ff:00:77:00:00:12:12:fe:01'])
        self.assertEqual(list(_make_esi_list(first='00:01:02:03:04:05:06:07:08:f0',count=4,step=5)),['00:01:02:03:04:05:06:07:08:f0','00:01:02:03:04:05:06:07:08:f5','00:01:02:03:04:05:06:07:08:fa','00:01:02:03:04:05:06:07:08:ff'])

        try:
            self.assertEqual(list(_make_esi_list(first='00:01:02:03:04:05:06:f0',count=1)),['0:01:02:03:04:05:06:f0'])
        except Exception as err:
            self.assertEqual(err.args[0], "This is not an esi identifier: 00:01:02:03:04:05:06:f0") 

    def test_is_mac(self):
        
        test_result=True
        self.assertEqual(is_mac('00:00:00:00:00:00'),test_result)
        test_result=True
        self.assertEqual(is_mac('FF:FF:FF:FF:FF:EE'),test_result)
        test_result=False
        self.assertEqual(is_mac('11:22:33:44:556'),test_result)
        test_result=False
        self.assertEqual(is_mac('GG:GG:GG:GG:GG:GG'),test_result)

    def test_is_esi(self):
        
        test_result=True
        self.assertEqual(is_esi('00:ff:00:77:00:00:12:12:fe:01'),test_result)
        test_result=False
        self.assertEqual(is_esi('FF:FF:FF:FF:FF:EE'),test_result)
        test_result=False
        self.assertEqual(is_esi('00:ff:00:77:00:00:12:12:fe:01:ab'),test_result)
        test_result=False
        self.assertEqual(is_esi('FG:ff:00:77:00:00:12:12:fe:01:ab'),test_result)
        test_result=False
        self.assertEqual(is_esi('GG:GG:GG:GG:GG:GG'),test_result)

    def test_is_ip(self):
        
        test_result='IPv4Address'
        self.assertEqual(is_ip('1.1.1.1'),test_result)
        test_result='IPv4Interface'
        self.assertEqual(is_ip('1.1.1.1/24'),test_result)
        test_result=False
        self.assertEqual(is_ip('1.1.1.1/244'),test_result)
        self.assertEqual(is_ip('ff80'),test_result)
        test_result='IPv6Address'
        self.assertEqual(is_ip('ff80::'),test_result)
        test_result='IPv6Interface'
        self.assertEqual(is_ip('ff80::/0'),test_result)


    def test__make_mixed_list(self):

        self.assertEqual(_make_mixed_list(first=None, count=None, step=1, last=None, repeat=1, cycle=None),None)
        self.assertEqual(str(type(_make_mixed_list(first='(1..4,6)', count=None, step=1, last=None, repeat=1, cycle=None))),"<class 'itertools.cycle'>")
        self.assertEqual(str(type(_make_mixed_list(first='(1..4,6)', count=None, step=1, last=None, repeat=1, cycle=3))),"<class 'itertools.cycle'>")
        self.assertEqual(str(type(_make_mixed_list(first='(1..4,6)', count=None, step=1, last=None, repeat=2, cycle=3))),"<class 'itertools.chain'>")
        self.assertEqual(str(type(_make_mixed_list(first='(1..4,6)', count=4, step=1, last=None, repeat=2, cycle=3))),"<class 'itertools.islice'>")
        self.assertEqual(str(type(_make_mixed_list(first='(1..4,6)', count=4, step=1, last='5', repeat=2, cycle=3))),"<class 'itertools.islice'>")
        self.assertEqual(str(type(_make_mixed_list(first='(1..4,6)', count=None, step=1, last=7, repeat=2, cycle=3))),"<class 'itertools.takewhile'>")

    @patch("jnpr.toby.engines.config.config_utils._make_number_list",return_value = '1.1.1.1')
    @patch("jnpr.toby.engines.config.config_utils._make_ip_list",return_value = '1.1.1.1')
    @patch("jnpr.toby.engines.config.config_utils._make_mixed_list",return_value = '1.1.1.1')
    @patch("jnpr.toby.engines.config.config_utils._make_string_list",return_value = '1.1.1.1')
    def test_make_list(self, patch_make_number_list, patch_make_ip_list,patch_make_mixed_list, patch_make_string_list ):

        self.assertEqual(str(type(make_list(first='1.1.1.1', count=2, step=1))),"<class 'str'>")
        self.assertEqual(str(type(make_list(first='1', count=2, step=1))),"<class 'str'>")
        self.assertEqual(str(type(make_list(first='(a,b,c)..', count=2, step=1))),"<class 'str'>")
        self.assertEqual(str(type(make_list(first='abc', count=2, step=1))),"<class 'str'>")
        self.assertEqual(make_list(first='', count=2, step=1),None)
        self.assertEqual(make_list(first='a', count=2, step=1,string='rt'),'1.1.1.1')

    def test_str_sort_key(self ):

        return_list= ['e', 10, '']
        self.assertEqual(str_sort_key(string='e10'),return_list)
        self.assertEqual(str_sort_key(string='E10'),return_list)

    def test_nested_set(self ):

        d1 = {'k1': {'k2': 5}}
        k1= ['k1', 'k2']
        return_list1={'k1': {'k2': 6}}
        nested_set(d1,k1 , 6) 
        self.assertEqual(return_list1,d1)   

        d1 = {'k1': {'k2': 5}}
        k1 = ['k1', 'k2']
        return_list1={'k1': {'k2': [5, 6]}}
        nested_set(d1, k1, 6, append=1)
        self.assertEqual(return_list1,d1)   

        d1={'r1':'CONFIG'}
        k1 = ['timer3', 'timer5']
        return_list1= {'r1': 'CONFIG', 'timer3': {'timer5': 45}}
        nested_set (d1, k1 , 45, append=False)
        self.assertEqual(return_list1,d1)   

        d1 = {'k1': {'k2': 5}}
        k1 = ['k1', 'k2']
        v1= [7,8]
        return_list1={'k1': {'k2': [5, 7, 8]}}
        nested_set(d1, k1, v1, append=1)
        self.assertEqual(return_list1,d1)   


    def test_nested_update(self ):

        input_keys = {'CONFIG': 4, 'r1': 'TOTO'}
        input_keys3 = {'CONFIG': {'timer':7}, 'r1': 'TOTO'}
        input_keys5 = {'CONFIG': {'timer':(1,2)}, 'r1': 'TOTO'} 
        input_keys6= {'r1': [1, 2], 'CONFIG': {'timer': 7}}

        input_base1={'r1':'CONFIG'}
        input_base2={'r1':'CONFIG'}         
        input_base3={'r1':'CONFIG'}
        input_base4={'r1':'CONFIG'}
        input_base5={'r1':'CONFIG'}
        input_base6={'r1':'CONFIG'}
        input_base7=OrderedDict([('r1', ['CONFIG', 'TOTO']), ('CONFIG', (1, 2))])

        return_list1= {'CONFIG': 4, 'r1': 'CONFIG'}
        return_list2= {'CONFIG': 4, 'r1': ['CONFIG', 'TOTO']}
        return_list3=  {'CONFIG': {'timer': 7}, 'r1': ['CONFIG', 'TOTO']}
        return_list4=   {'CONFIG': {'timer': 7}, 'r1': ['CONFIG', 'TOTO']}
        return_list5=    {'CONFIG': {'timer': (1, 2)}, 'r1': ['CONFIG', 'TOTO']}
        return_list6=   {'CONFIG': {'timer': 7}, 'r1': ['CONFIG', 1, 2]}
        return_list7=   OrderedDict([('r1', ['CONFIG', 'TOTO', 1, 2]), ('CONFIG', {'timer': 7})])

        nested_update (input_base1, input_keys, append=False)
        nested_update (input_base2, input_keys, append=True)
        nested_update (input_base3, input_keys3, append=True)
        nested_update (input_base4, input_keys3, append=True)
        nested_update (input_base5, input_keys5, append=True)
        nested_update (input_base6, input_keys6, append=1)
        nested_update (input_base7, input_keys6, append=1)

        self.assertEqual(input_base1,return_list1)
        self.assertEqual(input_base2,return_list2)
        self.assertEqual(input_base3,return_list3)
        self.assertEqual(input_base4,return_list4)
        self.assertEqual(input_base5,return_list5)
        self.assertEqual(input_base6,return_list6)
        self.assertEqual(input_base7,return_list7)


    def test_expand_to_list(self ):


        input_base='<<10#{count:10, step:4, cycle:6, repeat:3},30, 40..44 >>'
        self.assertEqual(type(expand_to_list(input_base, sort=True)),list)

        input_base='<<(1,2,3)#{count:10, step:2}>>'
        self.assertEqual(type(expand_to_list(input_base, sort=False)),list)

        input_base='<<(1,2,3)#{count:10, step:2>>'
        self.assertEqual(str(type(expand_to_list(input_base, sort=False))),"<class 'NoneType'>")

        input_base22='<<(1,2,3 #{count:10, step:2>>'
        self.assertEqual(str(type(expand_to_list(input_base, sort=False))),"<class 'NoneType'>")

        input_base='<<(1,2,3 #{count:10, step:2}>>'
        self.assertEqual(expand_to_list(input_base, sort=False),None)

        input_base= '<< a, b, (x,y,z,)..#{count:3, cycle:3, step:2}>>'
        self.assertEqual(type(expand_to_list(input_base, sort=False)),list)

        input_base= 'unit <<1..10>>  vlan-id <<1..>>'
        self.assertEqual(type(expand_to_list(input_base, sort=False)),list)

        input_base= 'unit <<1..10>>  << a, b, (x,y,z,)..#{cycle:3, step:2}>>'
        self.assertEqual(type(expand_to_list(input_base, sort=False)),list)

        input_base= '<<a,b, 10#{count:3}>>'
        self.assertEqual(type(expand_to_list(input_base, sort=False)),list)

        input_base='<<(3) #{count:10}>>'
        self.assertEqual(type(expand_to_list(input_base, sort=False)),list)

        input_base='<<10..#{count:10, step:4, cycle:6, repeat:3},30, 40..44 >>'
        self.assertEqual(type(expand_to_list(input_base, sort=False)),list)

        input_base= '<<a<< 1..>>  b<<5..>>'
        with self.assertRaisesRegexp(Exception, 'iterator'):
            expand_to_list(input_base, sort=False)

        input_base= "a<<13..3>>"
        try:
            expand_to_list(input_base, sort=False)
        except Exception as err:
            self.assertEqual(type(err.args[0]), str)

if __name__ == '__main__':
    unittest.main()
