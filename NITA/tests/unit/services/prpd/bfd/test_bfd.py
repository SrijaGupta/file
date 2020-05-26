#!/homes/achakra/toby/venv/bin/python

"""
bfd-api-test-module
"""

import unittest
from mock import MagicMock # pylint: disable=import-error
import netaddr
import sys


class TestBfd(unittest.TestCase):
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


        ##'BFD INIT'
        kwargs = {'command':'bfd_initialize'}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value == "test":
            pass
        else:
            assert False, "Bfd Init failed"

        ##'BFD SUBSCRIBE'
        kwargs = {'command':'bfd_notification_subscribe'}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value == "test":
            pass
        else:
            assert False, "Bfd Subscribe Request failed"

        ##'BFD Session Add4 1 RM 1 LO 1INTF'
        kwargs = {}
        remote_address = ['2.1.1.2']
        kwargs = {'command':'bfd_session_add', 'session_id':0, 'remote_address':remote_address, 'local_address':'2.1.1.1', \
                  'interface_name':'ge-0/0/0.0', 'remote_distinguisher':10, 'local_distinguisher':0, 'cookie':10, 'minimum_tx_interval':2000, \
                   'multiplier':3, 'minimum_rx_interval':2000, 'minimum_echo_tx_interval':2000, \
                   'session_type':'ECHO_LITE', 'session_mode':'SINGLE_HOP'}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"

        ##'BFD Session Add6 1 RM 1 LO 1INTF'
        remote_address = ['2000:2:1:1::2']
        kwargs = {'command':'bfd_session_add', 'session_id':0, 'remote_address':remote_address, 'local_address':'2000:2:1:1::1', \
                  'interface_name':'ge-0/0/0.0', 'remote_distinguisher':10, 'local_distinguisher':0, 'cookie':10, 'minimum_tx_interval':2000, \
                   'multiplier':3, 'minimum_rx_interval':2000, 'minimum_echo_tx_interval':2000, \
                   'session_type':'ECHO_LITE', 'session_mode':'SINGLE_HOP'}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"

        ##'BFD Session Add 1 RM'
        kwargs = {'command':'bfd_session_add', 'remote_address':'2.1.2.2', 'session_id':0, 'cookie':10, \
                  'session_type':'ECHO_LITE', 'session_mode':'SINGLE_HOP'}
        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"

        ##'BFD Session Add4 1 RM 1LC 1INTF'
        kwargs = {'command':'bfd_session_add', 'session_id':0, 'remote_address':'2.1.3.2', 'local_address':'2.1.3.1', \
                  'interface_name':'ge-0/0/0.0', 'cookie':10, 'minimum_tx_interval':2000, \
                   'multiplier':3, 'minimum_rx_interval':2000, 'minimum_echo_tx_interval':2000, 'session_type':'ECHO_LITE', \
                   'session_mode':'SINGLE_HOP'}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"

        ##'BFD Session delete'
        kwargs = {'command': 'bfd_session_delete', 'session_id':1}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session delete failed"

        ##'BFD Session delete bulk'
        session_id = [1, 2, 3, 4, 5]
        kwargs = {'command': 'bfd_session_delete', 'session_id':session_id}

        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session delete failed"


        #'BFD Session deleteall'
        kwargs = {'command':'bfd_session_delete_all'}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value == "test":
            pass
        else:
            assert False, "bfd session delete all failed"

        ##'BFD Unsubscribe'
        kwargs = {'command': 'bfd_notification_unsubscribe'}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value == "test":
            pass
        else:
            assert False, "bfd session unsubscribe failed"

        ##'BFD Session Add4 3 RM 3LC 3INTF'
        remote_address = ['2.1.1.2', '2.1.2.2', '2.1.3.2']
        local_address = ['2.1.1.1', '2.1.2.1', '2.1.3.1']
        interface_name = ['ge-0/0/0.0', 'ge-0/0/0.1', 'ge-0/0/0.2']
        kwargs = {'command': 'bfd_session_add', 'session_id':0, 'remote_address':remote_address, 'local_address':local_address, \
                  'interface_name':interface_name, 'remote_distinguisher':10, 'local_distinguisher':0, 'cookie':99999, 'minimum_tx_interval':1000, \
                   'multiplier':6, 'minimum_rx_interval':1000, 'minimum_echo_tx_interval': 1000, \
                   'session_type':'ECHO_LITE', 'session_mode':'SINGLE_HOP'}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"

        ##'BFD Session Add4 3 RM 1LC 1INTF'
        remote_address = ['2.1.1.2', '2.1.2.2', '2.1.3.2']
        kwargs = {'command': 'bfd_session_add', 'session_id':0, 'remote_address':remote_address, 'local_address':'2.1.1.1', \
                  'interface_name':'ge-0/0/0.0', 'remote_distinguisher':10, 'local_distinguisher':0, 'cookie':99, 'minimum_tx_interval':1000, \
                   'multiplier':3, 'session_type':'ECHO_LITE', 'session_mode':'SINGLE_HOP'}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"

        ##'BFD Session Add6 3 RM 3LC 3INTF'
        remote_address = ['2000:2:1:1::2', '2000:2:1:2::2', '2000:2:1:3::2']
        local_address = ['2000:2:1:1::1', '2000:2:1:2::1', '2000:2:1:3::1']
        interface_name = ['ge-0/0/0.0', 'ge-0/0/0.1', 'ge-0/0/0.2']
        kwargs = {'command': 'bfd_session_add', 'session_id':0, 'remote_address':remote_address, 'local_address':local_address, \
                  'interface_name':interface_name, 'remote_distinguisher':10, 'local_distinguisher':0, 'cookie':99999, 'minimum_tx_interval':1000, \
                  'multiplier':6, 'minimum_rx_interval':1000, 'minimum_echo_tx_interval': 1000, \
                   'session_type':'ECHO_LITE', 'session_mode':'SINGLE_HOP'}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"


        ##'BFD Session Add4 16 RM'
        remote_address = ['2.1.1.2', '2.1.2.2', '2.1.3.2', '2.1.4.2', '2.1.5.2', '2.1.6.2', '2.1.7.2', '2.1.8.2', '2.1.9.2', '2.1.10.2', '2.1.11.2', '2.1.12.2', '2.1.13.2', '2.1.14.2', '2.1.15.2', '2.1.16.2']
        kwargs = {'command': 'bfd_session_add', 'session_id':0, 'remote_address':remote_address, 'remote_distinguisher':10, 'local_distinguisher':0, 'cookie':99999, 'minimum_tx_interval':1000, \
                   'multiplier':6, 'minimum_rx_interval':1000, 'minimum_echo_tx_interval': 1000, \
                   'session_type':'ECHO_LITE', 'session_mode':'SINGLE_HOP'}
 

        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"


        remote_address = ['2.1.1.2', '2.1.2.2', '2.1.3.2', '2.1.4.2', '2.1.5.2']
        local_address = ['2.1.1.1', '2.1.2.1']
        interface_name = ['ge-0/0/0.0', 'ge-0/0/0.1']

        kwargs = {'command': 'bfd_session_add', 'session_id':0, 'remote_address':remote_address, 'remote_distinguisher':10, 'local_distinguisher':0, 'cookie':99999, 'minimum_tx_interval':1000, \
                   'multiplier':6, 'minimum_rx_interval':1000, 'minimum_echo_tx_interval': 1000, 'local_address':local_address, \
                  'interface_name':interface_name, 'session_type':'ECHO_LITE', 'session_mode':'SINGLE_HOP'}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"


        remote_address = ['2.1.1.2', '2.1.2.2', '2.1.3.2', '2.1.4.2', '2.1.5.2']
        local_address = ['2.1.1.1', '2.1.2.1', '2.1.3.1']
        interface_name = ['ge-0/0/0.0', 'ge-0/0/0.1']

        kwargs = {'command': 'bfd_session_add', 'session_id':0, 'remote_address':remote_address, 'remote_distinguisher':10, 'local_distinguisher':0, 'cookie':99999, 'minimum_tx_interval':1000, \
                   'multiplier':6, 'minimum_rx_interval':1000, 'minimum_echo_tx_interval': 1000, 'local_address':local_address, \
                  'interface_name':interface_name, 'session_type':'ECHO_LITE', 'session_mode':'SINGLE_HOP'}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"


        remote_address = ['2.1.1.2']
        local_address = ['2.1.1.1', '2.1.2.1', '2.1.3.1']
        interface_name = ['ge-0/0/0.0', 'ge-0/0/0.1']

        kwargs = {'command': 'bfd_session_add', 'session_id':0, 'remote_address':remote_address, 'remote_distinguisher':10, 'local_distinguisher':0, 'cookie':99999, 'minimum_tx_interval':1000, \
                   'multiplier':6, 'minimum_rx_interval':1000, 'minimum_echo_tx_interval': 1000, 'local_address':local_address, \
                  'interface_name':interface_name, 'session_type':'ECHO_LITE', 'session_mode':'SINGLE_HOP'}


        value = execute_prpd_api(dev, channel_id=None, **kwargs)

        if value[0] == "test":
            pass
        else:
            assert False, "bfd session add failed"

if __name__ == '__main__':  # pragma: no coverage
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestBfd)
    #unittest.TextTestRunner(verbosity=2).run(SUITE)
    unittest.main()

