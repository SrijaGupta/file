#!/homes/mohanas/toby/venv/bin/python

"""
prpd-api-test-module
"""

import unittest
from mock import MagicMock # pylint: disable=import-error
import netaddr
import sys


class TestBgp(unittest.TestCase):
    """DOC"""

    @staticmethod
    def test_execute_prpd_api():
        """Test execute prpd api"""

        grpc_lib_path = '/volume/regressions/grpc_lib/20.1'
        sys.path.append(grpc_lib_path)

        from jnpr.toby.hldcl import device # pylint: disable=import-error
        from jnpr.toby.services.prpd.prpd import execute_prpd_api # pylint: disable=import-error

        dev = MagicMock()

        dev.current_node.current_controller.default_grpc_channel = 1
        dev.current_node.current_controller.channels = {'grpc':[MagicMock(), MagicMock()]}
        dev.current_node.current_controller.channels['grpc'][1].send_api.return_value = "test"
        
        kwargs = {'command': 'bgp_init'}
        
        value = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)
#         
        if value == "test":
            pass
        else:
            assert False, "Bgp Init failed"

        dest_prefix = ['20.1.1.1']
        kwargs = {'command': 'bgp_route_add', 'dest_prefix':dest_prefix,\
                   'table':'inet.0', 'prefix_len':32, 'next_hop':'10.1.1.2',\
                   'communities':'100:1','cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10}

        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Add failed"

        
        dest_prefix = ['2001:120:1:1::1']
        kwargs = {'command': 'bgp_route_update', 'dest_prefix':dest_prefix,\
                   'table':'inet6.0', 'prefix_len':64, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10}

        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Update failed"

        dest_prefix_1 =[]
        for i in range(0, 2):
            intv4 = int(netaddr.IPAddress("20.1.1.1"))
            intv4 = intv4 + i
            nh4 = str(netaddr.IPAddress(intv4))
            dest_prefix_1.append(nh4)
        
        kwargs = {'command': 'bgp_route_modify', 'dest_prefix':dest_prefix_1,\
                   'table':'inet6.0', 'prefix_len':64, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Modify failed"

        dest_prefix = {'dest_prefix':'2001:120:1:1::1','rd_type':0,'as_number':100,'assigned_number':1}
        kwargs = {'command': 'bgp_route_update', 'dest_prefix':dest_prefix,\
                   'table':'bgp.l3vpn-inet6.0', 'prefix_len':64, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10,'api_user':'test'}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Update failed" 

        dest_prefix = {'dest_prefix':'2001:120:1:1::1','rd_type':0,'as_number':100,'assigned_number':1}
        kwargs = {'command': 'bgp_route_update', 'dest_prefix':dest_prefix,\
                   'table':'bgp.l3vpn-inet6.0', 'prefix_len':64, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Update failed" 
   
        dest_prefix = {'dest_prefix':'120.1.1.1','rd_type':1,'as_number':100,'assigned_number':1,'ipaddress':'1.1.1.1'}
        kwargs = {'command': 'bgp_route_update', 'dest_prefix':dest_prefix,\
                   'table':'bgp.l3vpn.0', 'prefix_len':92, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10,'vpn_label':16}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Update failed" 
   
        dest_prefix = {'dest_prefix':'120.1.1.1','rd_type':2,'as_number':100,'assigned_number':1,'table':'bgp.l3vpn.0'}
        
        kwargs = {'command': 'bgp_route_remove', 'dest_prefix':dest_prefix,\
                   'table':'bgp.l3vpn.0', 'prefix_len':192, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10,'vpn_label':16,'orlonger':1}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Remove failed"

        dest_prefix = {'dest_prefix':'120.1.1.1','rd_type':2,'as_number':100,'assigned_number':1,'table':'bgp.l3vpn.0'}
        
        kwargs = {'command': 'bgp_route_remove', 'dest_prefix':dest_prefix,\
                   'table':'bgp.l3vpn.0', 'prefix_len':192, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10,'vpn_label':16,'orlonger':1,'api_user':'test'}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Remove failed"
   
        dest_prefix = {'dest_prefix':'120.1.1.1','sr_color':2,'sr_distinguisher':100}
        
        route_data = {'segment_lists':[{'weight':1,\
                        'segment_entries':[{'label':100,'traffic_class':1,'bottom_of_stack':False,'ttl':1},{'label':101,'traffic_class':1,'bottom_of_stack':1,'ttl':1}]}],\
                      'sr_preference':100,'binding_sid':{'label':100,'traffic_class':1,'bottom_of_stack':1,'ttl':1}}
        kwargs = {'command': 'bgp_route_add', 'dest_prefix':dest_prefix,'routedata':route_data,\
                   'table':'bgp.inetsrte.0', 'prefix_len':192, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Update failed" 

        dest_prefix = {'dest_prefix':'2001:120:1:1::1','sr_color':2,'sr_distinguisher':100}
        
        route_data = {'segment_lists':[{'weight':1,\
                        'segment_entries':[{'label':100,'traffic_class':1,'bottom_of_stack':False,'ttl':1},{'label':101,'traffic_class':1,'bottom_of_stack':1,'ttl':1}]}],\
                      'sr_preference':100,'binding_sid':{'label':100,'traffic_class':1,'bottom_of_stack':1,'ttl':1}}
        kwargs = {'command': 'bgp_route_add', 'dest_prefix':dest_prefix,'routedata':route_data,\
                   'table':'bgp.inet6srte.0', 'prefix_len':192, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Update failed" 
       
        dest_prefix = {'dest_prefix':'2001:120:1:1::1','sr_color':2,'sr_distinguisher':100}
        
        route_data = {'segment_lists':[{'weight':1,\
                    'segment_entries':[{'label':100,'traffic_class':1,'bottom_of_stack':False,'ttl':1},{'label':101,'traffic_class':1,'bottom_of_stack':1,'ttl':1}]}],\
                      'sr_preference':100,'binding_sid':{'label':100,'traffic_class':1,'bottom_of_stack':1,'ttl':1}}
        kwargs = {'command': 'bgp_route_get', 'dest_prefix':dest_prefix,'routedata':route_data,\
                   'table':'bgp.inet6srte.0', 'prefix_len':192, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10,'orlonger':1,'active_only':True,'route_count':10,'reply_address_format':0,'reply_table_format':0,'api_user':'test'}
        
        
        value = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        
        if value == 'test':
            pass
        else:
            assert False, "Bgp Route get failed"

        dest_prefix = {'dest_prefix':'2001:120:1:1::1','sr_color':2,'sr_distinguisher':100}
        
        route_data = {'segment_lists':[{'weight':1,\
                    'segment_entries':[{'label':100,'traffic_class':1,'bottom_of_stack':False,'ttl':1},{'label':101,'traffic_class':1,'bottom_of_stack':1,'ttl':1}]}],\
                      'sr_preference':100,'binding_sid':{'label':100,'traffic_class':1,'bottom_of_stack':1,'ttl':1}}
        kwargs = {'command': 'bgp_route_get', 'dest_prefix':dest_prefix,'routedata':route_data,\
                   'table':'bgp.inet6srte.0', 'prefix_len':192, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10,'orlonger':1,'active_only':True,'route_count':10,'reply_address_format':0,'reply_table_format':0}
        
        
        value = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        if value == 'test':
            pass
        else:
            assert False, "Bgp Route get failed"    
        
        kwargs = {'command': 'bgp_monitor_register', 'route_count':10,'reply_address_format':0,'reply_table_format':0 }
        
        value = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        if value == 'test':
            pass
        else:
            assert False, "Bgp Monitor Register failed"
         
        kwargs = {'command': 'bgp_monitor_unregister'}
        
        value = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)
        
        if value == 'test':
            pass
        else:
            assert False, "Bgp Monitor Unregister failed"
  
        dest_prefix = ['2001:120:1:1::1']
        kwargs = {'command': 'bgp_route_update', 'dest_prefix':dest_prefix,\
                   'table':'inet6.0', 'prefix_len':64, 'next_hop':['10.1.1.2','10.1.1.3'],\
                   'communities':['100:1','100:2'],'cluster_id':'1.1.1.1','originator_id':'1.1.1.1',\
                   'route_preference':100,'local_preference':400,'med':100,'aspath':'100','route_type':1,\
                   'path_cookie':10,'api_user':'test'}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Update failed"
 
        dest_prefix = ['2001:120:1:1::1']
        kwargs = {'command': 'bgp_route_update','dest_prefix':dest_prefix,'api_user':'test'}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Update failed"

        dest_prefix = ['2001:120:1:1::1']
        kwargs = {'command': 'bgp_route_update','dest_prefix':dest_prefix,'table':'inet.0','api_user':'test'}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route Update failed"
        
        """Flow spec"""

        dest_prefix = {'dest_prefix':'2001:120:1:1::1','dest_len':32,'src_prefix':'2001:12:1:1::1','src_len':32,'protocols':[10,12],'ports':[12,12]}
        
        route_data = {'discard': True,'rate_limit':1000,'mark_dscp':1,'sample':True,'redirect_to_vrf':"vrf1"}
        
        kwargs = {'command': 'bgp_route_add', 'dest_prefix':dest_prefix,'routedata':route_data,\
                   'table':'inetflow.0', 'prefix_len':64, 'next_hop':['10.1.1.2','10.1.1.3']}
        
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route add failed"
  
        dest_prefix = {'dest_prefix':'120.1.1.1','dest_len':32,'src_prefix':'12.1.1.1','src_len':32,'protocols':[10,12],'ports':[12,12]}
        
        route_data = {'discard': True,'rate_limit':1000,'mark_dscp':1,'sample':True,'redirect_to_vrf':"vrf1"}
        kwargs = {'command': 'bgp_route_modify', 'dest_prefix':dest_prefix,'routedata':route_data,\
                   'table':'inetflow.0', 'prefix_len':64, 'next_hop':['10.1.1.2','10.1.1.3']}
    
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route modify failed" 
   
        dest_prefix = {'dest_prefix':'2001:120:1:1::1','dest_len':32,'src_prefix':'2001:12:1:1::1','src_len':32,'protocols':[10,12],'ports':[12,12]}
        
        route_data = {'discard': True,'rate_limit':1000,'mark_dscp':1,'sample':True,'redirect_to_vrf':"vrf1"}
        kwargs = {'command': 'bgp_route_get', 'dest_prefix':dest_prefix,'routedata':route_data,\
                   'table':'inetflow.0', 'prefix_len':64, 'next_hop':['10.1.1.2','10.1.1.3']}
    
        value = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        if value == 'test':
            pass
        else:
            assert False, "Bgp Route get failed" 

        dest_prefix = {'dest_prefix':'12.1.1.1','dest_len':32,'src_prefix':'120.1.1.1','src_len':32,'protocols':[10,12],'ports':[12,12]}
        
        route_data = {'discard': True,'rate_limit':1000,'mark_dscp':1,'sample':True,'redirect_to_vrf':"vrf1"}
        kwargs = {'command': 'bgp_route_remove', 'dest_prefix':dest_prefix,'routedata':route_data,\
                   'table':'inetflow.0', 'prefix_len':64, 'next_hop':['10.1.1.2','10.1.1.3']}
    
        valuelist = execute_prpd_api(dev, channel_id=None, **kwargs, compliance=True)

        for value in valuelist:
            if value == 'test':
                pass
            else:
                assert False, "Bgp Route remove failed"
           
if __name__ == '__main__':  # pragma: no coverage
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestBgp)
    #unittest.TextTestRunner(verbosity=2).run(SUITE)
    unittest.main()
