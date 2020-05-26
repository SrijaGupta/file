"""
prpd-interface-api-test-module
"""

import unittest
from mock import MagicMock # pylint: disable=import-error
import sys


class TestInterface(unittest.TestCase):
    """DOC"""

    @staticmethod
    def test_execute_prpd_api():
        """Test execute prpd api"""

        grpc_lib_path = '/volume/regressions/grpc_lib/latest'
        sys.path.append(grpc_lib_path)

        from jnpr.toby.services.prpd.prpd import execute_prpd_api # pylint: disable=import-error

        dev = MagicMock()

        dev.current_node.current_controller.default_grpc_channel = 1
        dev.current_node.current_controller.channels = {'grpc':[MagicMock(), MagicMock()]}
        dev.current_node.current_controller.channels['grpc'][1].send_api.return_value = "test"

        value = execute_prpd_api(dev, channel_id=None, command="interface_get", interface='ge-0/0/0.0', compliance=True)
        if value == "test":
            pass
        else:
            assert False, "interface_get failed"



        value = execute_prpd_api(dev, channel_id=None, command="interface_get", index=333, compliance=True)
        if value == "test":
            pass
        else:
            assert False, "interface_get failed"


        value = execute_prpd_api(dev, channel_id=None, command="interface_notification_register", compliance=True)
        if value == "test":
            pass
        else:
            assert False, "interface_notification_register failed"


        value = execute_prpd_api(dev, channel_id=None, command="interface_notification_unregister", compliance=True)
        if value == "test":
            pass
        else:
            assert False, "interface_notification_unregister failed"


        value = execute_prpd_api(dev, channel_id=None, command="interface_notification_refresh", compliance=True)
        if value == "test":
            pass
        else:
            assert False, "interface_notification_refresh failed"


if __name__ == '__main__':  # pragma: no coverage
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestInterface)
    unittest.main() #unittest.TextTestRunner(verbosity=2).run(SUITE)

