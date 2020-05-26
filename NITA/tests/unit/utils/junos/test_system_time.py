
from mock import patch
import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.utils.junos import system_time
from jnpr.toby.hldcl.juniper.junos import Juniper
from datetime import datetime
import jxmlease




# To return response of shell() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=Juniper)
    mocked_obj.log = MagicMock()
    mocked_obj.execute = MagicMock()


    def test_get_system_time_exception(self):
        try:
            system_time.get_system_time()
        except Exception as err:
            self.assertEqual(err.args[0], "device is a mandatory argument")



    def test_get_system_time(self):
        dt = "2017-02-14 00:27:56 PST"
        diction1 = {}
        diction2 = {}
        diction3 = {}
        diction1['date-time'] = dt
        diction2['current-time'] = diction1
        diction3['system-uptime-information'] = diction2
        d = datetime(2017, 2, 14, 0, 27, 56)

        self.mocked_obj.get_rpc_equivalent = MagicMock()
        self.mocked_obj.get_model = MagicMock(return_value="MX")
        self.execute_rpc = MagicMock()
        jxmlease.parse_etree = MagicMock(return_value=diction3)
        self.assertEqual(system_time.get_system_time(device=self.mocked_obj), d)


        self.mocked_obj.get_model.return_value = "srx"
        self.mocked_obj.is_ha = MagicMock(return_value=True)
        self.mocked_obj.node_name = MagicMock(return_value="node0")

        lst = []
        diction4 = {}
        diction5 = {}

        diction3['re-name'] = "node0"
        lst.append(diction3)
        diction4['multi-routing-engine-item'] = lst
        diction5['multi-routing-engine-results'] = diction4

        jxmlease.parse_etree.return_value = diction5
        self.assertEqual(system_time.get_system_time(device=self.mocked_obj), d)


        try:
            system_time.get_system_time(device=self.mocked_obj, node="node2")
        except Exception as err:
            self.assertEqual(err.args[0], "Invalid HA Node value")



    def test_set_system_time_exception(self):
        try:
            system_time.set_system_time()
        except Exception as err:
            self.assertEqual(err.args[0], "device is a mandatory argument")

        try:
            system_time.set_system_time(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "date_time is a mandatory argument")


    def test_set_system_time(self):

        d = datetime(2017, 2, 14, 0, 27, 56)
        e = datetime(2017, 2, 14, 0, 27, 58)
        f = datetime(2017, 2, 14, 0, 28, 58)

        self.mocked_obj.cli = MagicMock(return_value=Response("abc"))
        p = patch("jnpr.toby.utils.junos.system_time.get_system_time", new=MagicMock(
            side_effect=[e]))
        p.start()
        self.assertEqual(system_time.set_system_time(device=self.mocked_obj, date_time=d), "abc")
        p.stop()

        p = patch("jnpr.toby.utils.junos.system_time.get_system_time", new=MagicMock(
            side_effect=[f]))
        p.start()
        self.assertEqual(system_time.set_system_time(device=self.mocked_obj, date_time=d, tolerance_in_seconds=50),"abc")
        p.stop()


    def test_sync_system_time_with_ntp_exception(self):
        try:
            system_time.sync_system_time_with_ntp()
        except Exception as err:
            self.assertEqual(err.args[0], "device is a mandatory argument")


    def test_sync_system_time_with_ntp(self):
        self.mocked_obj.cli = MagicMock(return_value=Response("abc"))
        self.assertEqual(system_time.sync_system_time_with_ntp(device=self.mocked_obj), "abc")


if __name__ == '__main__':
    unittest.main()