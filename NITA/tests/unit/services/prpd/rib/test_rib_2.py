"""
rib-api-test-module
"""

import unittest
from mock import MagicMock # pylint: disable=import-error
import netaddr
import sys



class TestRib(unittest.TestCase):
    """DOC"""

    @staticmethod
    def test_execute_prpd_api():
        """Test execute prpd api"""

        grpc_lib_path = '/volume/regressions/grpc_lib/latest'
        sys.path.append(grpc_lib_path)

        from jnpr.toby.hldcl import device # pylint: disable=import-error
        from jnpr.toby.services.prpd.prpd import execute_prpd_api # pylint: disable=import-error

        dev = MagicMock()

        dev.current_node.current_controller.default_grpc_channel = 1
        dev.current_node.current_controller.channels = {'grpc':[MagicMock(), MagicMock()]}
        dev.current_node.current_controller.channels['grpc'][1].send_api.return_value = "test"


        kwargs = {'command': 'rib_route_initialize',\
                  'default_preferences0':33,\
                  'default_preferences1':100}
        value = execute_prpd_api(dev, channel_id=None, compliance=True, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Rib Init Failed"


        kwargs = {'command': 'rib_route_cleanup'}
        value = execute_prpd_api(dev, channel_id=None, compliance=True, **kwargs)



        if value == "test":
            pass
        else:
            assert False, "Rib Init Failed"


        kwargs = {'command':'rib_route_add',\
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

        value = execute_prpd_api(dev, channel_id=None, compliance=True, **kwargs)
        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {}
        dest_prefix = ['20.1.1.1']
        kwargs = {'command': 'rib_route_add', 'next_hop_interface':'ge-0/0/0.0',\
                  'dest_prefix':dest_prefix, 'table':'inet.0', 'prefix_len':32, 'next_hop':'10.1.1.2'}
        value = execute_prpd_api(dev, channel_id=None, compliance=True, **kwargs)

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

        value = execute_prpd_api(dev, channel_id=None, compliance=True, **kwargs)
        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':'rib_route_get',\
              'dest_prefix':"0.0.0.0",\
              'table':'inet.0',\
              'prefix_len':10,\
              'count':23,\
              'route_match_type':"EXACT_OR_LONGER"}


        value = execute_prpd_api(dev, channel_id=None, compliance=True, **kwargs)
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

        value = execute_prpd_api(dev, channel_id=None, compliance=True, **kwargs)
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

        execute_prpd_api(dev, channel_id=None, command="rib_route_add", compliance=True,\
                         next_hop_interface="et-0/0/1:2.0", dest_prefix=dest_prefix_1,\
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

        execute_prpd_api(dev, channel_id=None, compliance=True, **kwargs)


        kwargs1 = {'command':'rib_route_add',\
                  'dest_prefix':'8000',\
                  'table':'mpls.0',\
                  'prefix_len':52,\
                  'next_hop':'10.40.0.1',\
                  'opcode':'pop'}


        execute_prpd_api(dev, channel_id=None, compliance=True, **kwargs1)



        for i in range(0, 10):
            intv4 = int(netaddr.IPAddress("20.1.1.1"))
            intv4 = intv4 + i
            nh4 = str(netaddr.IPAddress(intv4))
            dest_prefix_1.append(nh4)
        labels = [8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008, 8009, 8010]
        kwargs = {'command':'rib_route_add',\
                  'next_hop_interface':'ge-0/0/0.0',\
                  'dest_prefix':'10.40.0.1',\
                  'table':'inet.0',\
                  'prefix_len':32,\
                  'next_hop':dest_prefix_1,\
                  'label':labels,\
                  'opcode':'push'}

        value = execute_prpd_api(dev, channel_id=None, compliance=True, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"

        kwargs = {'command': 'rib_route_add',\
                  'next_hop_interface':'et-1/0/0:0.0',\
                  'destination_prefix':["23.1.1.2", "23.1.1.3", "23.1.1.4", "23.1.1.5",],\
                  'table':'inet.0',\
                  'prefix_len':32,\
                  'next_hop':[['10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5'],
                              ['11.1.1.2', '11.1.1.3', '11.1.1.4', '11.1.1.5'],
                              ['12.1.1.2', '12.1.1.3', '12.1.1.4', '12.1.1.5'],
                              ['13.1.1.2', '13.1.1.3', '13.1.1.4', '13.1.1.5']],\
                  'preferences0':6,\
                  'preferences1':101,\
                  'colors0':30,\
                  'colors1':31,\
                  'tags0':16,\
                  'tags1':17,\
                  'no_advertise': True,\
                  'weight':[['WEIGHT_PRIMARY'],[1,2,'WEIGHT_BACKUP'],['WEIGHT_NONE']],\
                  'bandwidth': [[100,60,80,230],[10,12],[23,22,45]]
                  }


        value = execute_prpd_api(dev, channel_id=None, version=2, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"



        kwargs = {'command': 'rib_route_add',\
                  'next_hop_interface':'et-1/0/0:0.0',\
                  'destination_prefix':["23.1.1.2", "23.1.1.3", "23.1.1.4", "23.1.1.5",],\
                  'table':'inet.0',\
                  'prefix_len':32,\
                  'next_hop':[['10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5'],
                              ['11.1.1.2', '11.1.1.3', '11.1.1.4', '11.1.1.5'],
                              ['12.1.1.2', '12.1.1.3', '12.1.1.4', '12.1.1.5'],
                              ['13.1.1.2', '13.1.1.3', '13.1.1.4', '13.1.1.5']],\
                  'preferences0':6,\
                  'preferences1':101,\
                  'colors0':30,\
                  'colors1':31,\
                  'tags0':16,\
                  'tags1':17,\
                  'no_advertise': True,\
                  'weight':[['1'],[1,2,'2'],['3']],\
                  'bandwidth': [[100,60,80,230],[10,12],[23,22,45]],\
                  'ecmp':True
                  }


        value = execute_prpd_api(dev, channel_id=None, version=2, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"


        labels = [[8001, 8002, 8003], [8001, 8002, 8003], [8001, 8002, 8003]]
        opcode = ['PUSH','PUSH','PUSH']


        kwargs = {'command': 'rib_route_add',\
                  'next_hop_interface':'et-1/0/0:0.0',\
                  'destination_prefix':["23.1.1.2", "23.1.1.3", "23.1.1.4", "23.1.1.5",],\
                  'table':'inet.0',\
                  'prefix_len':32,\
                  'next_hop':[['10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5'],
                              ['11.1.1.2', '11.1.1.3', '11.1.1.4', '11.1.1.5'],
                              ['12.1.1.2', '12.1.1.3', '12.1.1.4', '12.1.1.5'],
                              ['13.1.1.2', '13.1.1.3', '13.1.1.4', '13.1.1.5']],\
                  'preferences0':6,\
                  'preferences1':101,\
                  'colors0':30,\
                  'colors1':31,\
                  'tags0':16,\
                  'tags1':17,\
                  'no_advertise': True,\
                  'label':labels,\
                  'opcode':opcode,\
                  'weight':[['4'],[1,2,4200],[700]],\
                  'stack_labels':True,\
                  'ecmp':True
                  #'bandwidth': [[100,60,80,230],[10,12],[23,22,45]]
                  }
                  
        value = execute_prpd_api(dev, channel_id=None, version=2, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"

        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"

        labels = [[8001, 8002, 8003], [8001, 8002, 8003], [8001, 8002, 8003]]
        opcode = ['PUSH','PUSH','PUSH']


        kwargs = {'command': 'rib_route_add',\
                  'next_hop_interface':'et-1/0/0:0.0',\
                  'destination_prefix':["23.1.1.2", "23.1.1.3", "23.1.1.4", "23.1.1.5",],\
                  'table':'inet.0',\
                  'prefix_len':32,\
                  'next_hop':[['10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5'],
                              ['11.1.1.2', '11.1.1.3', '11.1.1.4', '11.1.1.5'],
                              ['12.1.1.2', '12.1.1.3', '12.1.1.4', '12.1.1.5'],
                              ['13.1.1.2', '13.1.1.3', '13.1.1.4', '13.1.1.5']],\
                  'preferences0':6,\
                  'preferences1':101,\
                  'colors0':30,\
                  'colors1':31,\
                  'tags0':16,\
                  'tags1':17,\
                  'no_advertise': True,\
                  'label':labels,\
                  'opcode':opcode,\
                  'weight':[[11],[1,2,900],[10]],\
                  'stack_labels':True
                  #'bandwidth': [[100,60,80,230],[10,12],[23,22,45]]
                  }

        value = execute_prpd_api(dev, channel_id=None, version=2, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"


        labels = [8001, 8002, 8003]
        opcode = ['PUSH','PUSH','PUSH']


        kwargs = {'command': 'rib_route_add',\
                  'next_hop_interface':'et-1/0/0:0.0',\
                  'destination_prefix':["23.1.1.2", "23.1.1.3", "23.1.1.4", "23.1.1.5",],\
                  'table':'inet.0',\
                  'prefix_len':32,\
                  'next_hop':[['10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5'],
                              ['11.1.1.2', '11.1.1.3', '11.1.1.4', '11.1.1.5'],
                              ['12.1.1.2', '12.1.1.3', '12.1.1.4', '12.1.1.5'],
                              ['13.1.1.2', '13.1.1.3', '13.1.1.4', '13.1.1.5']],\
                  'preferences0':6,\
                  'preferences1':101,\
                  'colors0':30,\
                  'colors1':31,\
                  'tags0':16,\
                  'tags1':17,\
                  'no_advertise': True,\
                  'label':labels,\
                  'opcode':opcode,\
                  'weight':[['WEIGHT_PRIMARY'],[1,2,'WEIGHT_BACKUP'],['WEIGHT_NONE']]
                  #'bandwidth': [[100,60,80,230],[10,12],[23,22,45]]
                  }

        value = execute_prpd_api(dev, channel_id=None, version=2, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "Route add failed"



if __name__ == '__main__':  # pragma: no coverage
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestRib)
    #unittest.TextTestRunner(verbosity=2).run(SUITE)
    unittest.main()

