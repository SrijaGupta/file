#!/homes/snandu/toby/venv/bin/python

"""
prpd-api-test-module
"""

import unittest
from mock import MagicMock # pylint: disable=import-error
import netaddr
import sys



class TestPrpd(unittest.TestCase):
    """DOC"""

    @staticmethod
    def test_execute_prpd_api():
        """Test execute prpd api"""

        grpc_lib_path = '/volume/regressions/grpc_lib/latest'
        sys.path.append(grpc_lib_path)

        from jnpr.toby.hldcl import device # pylint: disable=import-error
        from jnpr.toby.services.prpd.prpd import execute_prpd_api, increment_prefix # pylint: disable=import-error

        dev = MagicMock()

        dev.current_node.current_controller.default_grpc_channel = 1
        dev.current_node.current_controller.channels = {'grpc':[MagicMock(), MagicMock()]}
        dev.current_node.current_controller.channels['grpc'][1].send_api.return_value = "test"

        prefix_list =  increment_prefix("17.27.0.1/32", 5) 
        prefix_list =  increment_prefix(5555, 10) 


        kwargs = {'command': 'rib_route_add',\
                  'next_hop_interface':'et-1/0/0:0.0',\
                  'dest_prefix':["23.1.1.2", "23.1.1.3", "23.1.1.4", "23.1.1.5",],\
                  'table':'inet.0',\
                  'prefix_len':32,\
                  'next_hop':['10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5'],\
                  'preferences0':6,\
                  'preferences1':101,\
                  'colors0':30,\
                  'colors1':31,\
                  'tags0':16,\
                  'tags1':17}

        value = execute_prpd_api(dev, channel_ID=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {}
        dest_prefix = ['20.1.1.1']
        kwargs = {'command': 'rib_route_add', 'next_hop_interface':'ge-0/0/0.0',\
                  'dest_prefix':dest_prefix, 'table':'inet.0', 'prefix_len':32, 'next_hop':'10.1.1.2'}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"


        dest_prefix = ['20.1.1.1',]

        kwargs = {'command': 'rib_route_modify',\
              'next_hop_interface':'ge-0/0/0.0',\
              'dest_prefix':dest_prefix,\
              'table':'inet.0',\
              'prefix_len':32,\
              'next_hop':'10.1.1.2',\
              'label':[100, 200, 300],\
              'opcode':['PUSH', 'PUSH', 'POP'],\
              'preferences0':12,\
              'preferences1':13,\
              'colors0':14,\
              'colors1':15,\
              'tags0':16,\
              'tags1':17,\
              'bulk_count':23}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command': 'rib_route_get',\
              'dest_prefix':"0.0.0.0",\
              'table':'inet.0',\
              'prefix_len':10,\
              'count':23,\
              'route_match_type':"EXACT_OR_LONGER"}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        dest_next_hop = []
        for i in range(0, 5):
            intv4 = int(netaddr.IPAddress("15.1.1.2"))
            intv4 = intv4 + i
            nh4 = str(netaddr.IPAddress(intv4))
            dest_next_hop.append(nh4)
            dest_prefix_1 = []


        kwargs = {'command': 'rib_route_update',\
              'next_hop_interface':'ge-0/0/0.0',\
              'dest_prefix':["20.1.1.1", "20.1.1.2"],\
              'table':'inet.0',\
              'prefix_len':32,\
              'next_hop':dest_next_hop,\
              'label':[100, 200, 300],\
              'opcode':['PUSH', 'PUSH', 'POP'],\
              'preferences0':12,\
              'preferences1':13,\
              'colors0':14,\
              'colors1':15,\
              'tags0':16,\
              'tags1':17,\
              'bulk_count':23}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"

        dest_next_hop = []
        for i in range(0, 5):
            intv4 = int(netaddr.IPAddress("15.1.1.2"))
            intv4 = intv4 + i
            nh4 = str(netaddr.IPAddress(intv4))
            dest_next_hop.append(nh4)
            dest_prefix_1 = []

        for i in range(0, 25):
            intv4 = int(netaddr.IPAddress("20.1.1.1"))
            intv4 = intv4 + i
            nh4 = str(netaddr.IPAddress(intv4))
            dest_prefix_1.append(nh4)

        execute_prpd_api(dev, channel_id=None, command="rib_route_add", next_hop_interface="et-0/0/1:2.0", dest_prefix=dest_prefix_1,\
                         table="inet.0", prefix_len=32, cookie=44444444444425, next_hop=dest_next_hop, preferences0=6,\
                         preferences1=55, colors0=10, colors1=15, tags0=44, tags1=99, bulk_count=23)
        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"

        kwargs = {'command':'rib_route_add',\
                  'next_hop_interface':'ge-0/0/0.0',\
                  'dest_prefix':'10.40.0.1',\
                  'table':'inet.0',\
                  'prefix_len':32,\
                  'next_hop':'10.10.0.1',\
                  'label':8000,\
                  'opcode':'push'}

        execute_prpd_api(dev, channel_id=None, **kwargs)


        kwargs1 = {'command':'rib_route_add',\
                  'dest_prefix':'8000',\
                  'table':'mpls.0',\
                  'prefix_len':52,\
                  'next_hop':'10.40.0.1',\
                  'opcode':'pop'}


        execute_prpd_api(dev, channel_id=None, **kwargs1)



        for i in range(0, 10):
            intv4 = int(netaddr.IPAddress("20.1.1.1"))
            intv4 = intv4 + i
            nh4 = str(netaddr.IPAddress(intv4))
            dest_prefix_1.append(nh4)

        labels = [8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008, 8009, 8010]

        kwargs = {'command':'rib_route_add',\
                  #'next_hop_interface':'ge-0/0/0.0',\
                  'dest_prefix':'10.40.0.1',\
                  'table':'inet.0',\
                  'prefix_len':32,\
                  'next_hop':dest_prefix_1,\
                  'label':labels,\
                  'opcode':'push'}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"



if __name__ == '__main__':  # pragma: no coverage
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestPrpd)
    #unittest.TextTestRunner(verbosity=2).run(SUITE)
    unittest.main()
