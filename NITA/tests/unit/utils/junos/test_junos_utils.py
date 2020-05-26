import builtins
from robot.libraries.BuiltIn import BuiltIn
from jnpr.toby.utils.junos.junos_utils import get_updated_system_dictionary
from jnpr.toby.utils.junos.junos_utils import get_xml_equivalent_of_set_commands
from jnpr.toby.utils.junos.junos_utils import get_junos_pid
from jnpr.toby.utils.junos.junos_utils import get_equivalent_rpc
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.utils.response import Response

from jnpr.toby.init.init import init

import unittest
import builtins
from mock import MagicMock
from mock import patch

class Response1:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class TestTime(unittest.TestCase):

    sample_dict = { 'controllers' :
                    { 're0' :
                      { 'user' : 'test_user',
                        'password' : 'test_password',
                        'connect_channels' : 'all'
                      },
                    }
                  }
    init = MagicMock(spec=init)
    get_lib_instance = MagicMock(spec=BuiltIn().get_library_instance, return_value=init)
    init._get_t = MagicMock()
    init._get_t.return_value = sample_dict
    def test_get_updated_system_dictionary(self):

        exp_dict = { 'controllers' :
                    { 're0' :
                      { 'user' : 'test_user',
                        'password' : 'test_password',
                        'connect_channels' : 'all'
                      },
                    }
                  }
        # TODO
        #self.assertEqual(get_updated_system_dictionary("r0"), exp_dict)
        #  above func call goes inside BuiltIn and throws exception. Needs more work to fix this.

    def test_get_xml_equivalent_of_set_commands(self):

        # make sure for a valid set commands, the expected xml contains
        # the confguration tags. Mock the xml response to make sure the current code
        # gets tested
        set_cmds = [
            "set system host-name porter-new"
        ]
        exp_xml = "<configuration><test></test></configuration>"

        mock_dev = MagicMock(spec=Juniper)
        mock_resp = MagicMock(spec=Response)
        mock_resp.response = MagicMock(return_value=exp_xml)
        mock_dev.config = MagicMock(return_value=mock_resp)

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(get_xml_equivalent_of_set_commands(mock_dev, set_cmds), exp_xml)


    def test_get_junos_pid_exception(self):
        try:
            get_junos_pid()
        except Exception as err:
            self.assertEqual(err.args[0], "device is a mandatory argument")

        mock_dev = MagicMock(spec=Juniper)

        try:
            get_junos_pid(device=mock_dev)
        except Exception as err:
            self.assertEqual(err.args[0], "Process_name is a mandatory argument")

        x = " 5691  -  S      0:00.90 /usr/sbin/sdk-vmmd -N    \
                5693  -  S      0:00.41 /usr/sbin/craftd -N    \
                5694  -  I      0:01.18 /usr/sbin/xntpd -j -N -g (ntpd)   \
                5695  -  I      0:01.88 /usr/sbin/mgd -N"

        mock_dev.cli = MagicMock(return_value=Response1(x))
        mock_dev.log = MagicMock()

        dct = {'/usr/sbin/mgd': '5691', 'abc': '0'}

        self.assertEqual(get_junos_pid(device=mock_dev, process_name=['abc', '/usr/sbin/mgd']), dct)

    def test_get_equivalent_rpc(self):

        cmd = "show version"
        exp_xml_rpc = "<get-software-information></get-software-information>"

        mock_dev = MagicMock(spec=Juniper)
        mock_dev.get_rpc_equivalent = MagicMock(return_value=exp_xml_rpc)

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(get_equivalent_rpc(device=mock_dev, command=cmd), exp_xml_rpc)

if __name__ =='__main__':
    unittest.main()
