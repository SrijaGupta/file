#!/homes/pratim/toby/venv/bin/python

"""
gribi-api-test-module
"""
import sys
import unittest
from mock import MagicMock # pylint: disable=import-error





class Testgribi(unittest.TestCase):
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

        kwargs = {'command':"gribi_add",\
                  'type_of_operation':"next_hop",\
                  'table_name':"inet6.3",\
                  'next_hop_id':10,\
                  'labels':["50010"]}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_add",\
                  'type_of_operation':"next_hop_group",\
                  'table_name':"inet6.3",\
                  'next_hop_groupid':[110],\
                  'color':111,\
                  'next_hop_id':[10],\
                  'weight':[70]}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_add",\
                  'type_of_operation':"route",\
                  'table_name':"inetcolor.0",\
                  'family':"inet",\
                  'prefix':"10.255.2.121-111<c>",\
                  'prefix_length':64,\
                  'next_hop_groupid':110}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_add",\
                  'type_of_operation':"route",\
                  'table_name':"inet6color.0",\
                  'family':"inet6",\
                  'prefix':"::ffff:10.255.2.121-112<c6>",\
                  'prefix_length':160,\
                  'next_hop_groupid':110}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_add",\
                  'type_of_operation':"route",\
                  'table_name':"mpls.0",\
                  'family':"mpls",\
                  'prefix':"1110",\
                  'prefix_length':52,\
                  'next_hop_groupid':110}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_modify",\
                  'type_of_operation':"next_hop",\
                  'next_hop_id':10,\
                  'labels':["50011", "50009", "50003"]}
        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_add",\
                  'type_of_operation':"route",\
                  'table_name':"inet.0",\
                  'family':"inet",\
                  'prefix':"111.111.111.0",\
                  'prefix_length':24,\
                  'next_hop_groupid':110}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_add",\
                  'type_of_operation':"route",\
                  'table_name':"inet6.0",\
                  'family':"inet6",\
                  'prefix':"::ffff:111.111.111.1",\
                  'prefix_length':128,\
                  'next_hop_groupid':110}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_add",\
                  'type_of_operation':"next_hop",\
                  'table_name':"inet6.3",\
                  'next_hop_id':20,\
                  'gateway_address':"2.1.1.2",\
                  'interface_name':"xe-0/0/0:2.0"}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_modify",\
                  'type_of_operation':"next_hop_group",\
                  'table_name':"inet6.3",\
                  'next_hop_groupid':[110],\
                  'color':111,\
                  'next_hop_id':[10, 20],\
                  'weight':[70, 30]}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_add",\
                  'type_of_operation':"next_hop_group",\
                  'table_name':"inet6.3",\
                  'next_hop_groupid':[210],\
                  'color':111,\
                  'next_hop_id':[10, 20],\
                  'weight':[70, 30]}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_modify",\
                  'type_of_operation':"route",\
                  'table_name':"inetcolor.0",\
                  'family':"inet",\
                  'prefix':"10.255.2.121-111<c>",\
                  'prefix_length':64,\
                  'next_hop_groupid':210}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_modify",\
                  'type_of_operation':"route",\
                  'table_name':"inet6color.0",\
                  'family':"inet6",\
                  'prefix':"::ffff:10.255.2.121-112<c6>",\
                  'prefix_length':160,\
                  'next_hop_groupid':210}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_modify",\
                  'type_of_operation':"route",\
                  'table_name':"mpls.0",\
                  'family':"mpls",\
                  'prefix':"1110",\
                  'prefix_length':52,\
                  'next_hop_groupid':210}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_modify",\
                  'type_of_operation':"route",\
                  'table_name':"inet.0",\
                  'family':"inet",\
                  'prefix':"111.111.111.0",\
                  'prefix_length':24,\
                  'next_hop_groupid':210}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_modify",\
                  'type_of_operation':"route",\
                  'table_name':"inet6.0",\
                  'family':"inet6",\
                  'prefix':"::ffff:111.111.111.1",\
                  'prefix_length':128,\
                  'next_hop_groupid':210}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_modify",\
                  'type_of_operation':"next_hop",\
                  'next_hop_id':10,\
                  'labels':["50011", "50009", "50003"]}
        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_delete",\
                  'type_of_operation':"next_hop",\
                  'table_name':"inet6.3",\
                  'next_hop_id':20,\
                  'gateway_address':"2.1.1.2",\
                  'interface_name':"xe-0/0/0:2.0"}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_delete",\
                  'type_of_operation':"next_hop_group",\
                  'table_name':"inet6.3",\
                  'next_hop_groupid':[110],\
                  'next_hop_id':[10, 20],\
                  'weight':[70, 30]}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_delete",\
                  'type_of_operation':"next_hop_group",\
                  'table_name':"inet6.3",\
                  'next_hop_groupid':[210],\
                  'color':111,\
                  'next_hop_id':[10, 20],\
                  'weight':[70, 30]}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_delete",\
                  'type_of_operation':"route",\
                  'table_name':"inetcolor.0",\
                  'family':"inet",\
                  'prefix':"10.255.2.121-111<c>",\
                  'prefix_length':64,\
                  'next_hop_groupid':210}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_delete",\
                  'type_of_operation':"route",\
                  'table_name':"inet6color.0",\
                  'family':"inet6",\
                  'prefix':"::ffff:10.255.2.121-112<c6>",\
                  'prefix_length':160,\
                  'next_hop_groupid':210}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_delete",\
                  'type_of_operation':"route",\
                  'table_name':"mpls.0",\
                  'family':"mpls",\
                  'prefix':"1110",\
                  'prefix_length':52,\
                  'next_hop_groupid':210}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_delete",\
                  'type_of_operation':"route",\
                  'table_name':"inet.0",\
                  'family':"inet",\
                  'prefix':"111.111.111.0",\
                  'prefix_length':24,\
                  'next_hop_groupid':210}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


        kwargs = {'command':"gribi_delete",\
                  'type_of_operation':"route",\
                  'table_name':"inet6.0",\
                  'family':"inet6",\
                  'prefix':"::ffff:111.111.111.1",\
                  'prefix_length':128,\
                  'next_hop_groupid':210}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)
        if value == "test":
            pass
        else:
            assert False, "Route add failed"


if __name__ == '__main__':  # pragma: no coverage
    SUITE = unittest.TestLoader().loadTestsFromTestCase(Testgribi)
    #unittest.TextTestRunner(verbosity=2).run(SUITE)
    unittest.main()
