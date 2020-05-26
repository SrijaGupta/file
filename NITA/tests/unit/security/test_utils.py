import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security import utils
from jnpr.toby.hldcl.juniper.security.srx import Srx



class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):

    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()


    def test_get_vty_counters_as_dictionary_exception(self):
        try:
            utils.get_vty_counters_as_dictionary()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")
        try:
            utils.get_vty_counters_as_dictionary(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'command' is a mandatory argument")


    def test_get_vty_counters_as_dictionary_one(self):
        dict_expected = {'counter1': 3, 'counter2': 5}
        lst = [Response("   counter1      3\n    counter2    5")]
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(utils.get_vty_counters_as_dictionary(device=self.mocked_obj,
                                                              command="show usp jsf counters junos-ssl-policy",
                                                              pic_name="fpc1.pic1"), dict_expected)

        dict_expected2 = {'null natp': 0, 'aggr receive resource open pinhole ok':0, 'Send DNS req failed':123, 'Sun RPC map lifetime (min)':480}
        lst = [Response("   null natp                               0\n    aggr receive resource open pinhole ok            :           0\nSend DNS req failed     : 123\n Sun RPC map lifetime (min):            480\n")]
        self.mocked_obj.vty.side_effect=lst
        self.assertEqual(utils.get_vty_counters_as_dictionary(device=self.mocked_obj, command="show usp jsf counters junos-ssl-policy", pic_name="fpc1.pic1"), dict_expected2)


    def test_get_vty_counters_as_dictionary_two(self):
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0.pic1", "fpc1.pic1"])
        dict_expected = {'counter1': 22, 'counter2': 30}
        lst = [Response("   counter1      10\n    counter2    15"), Response("   counter1      12\n    counter2    15")]
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(utils.get_vty_counters_as_dictionary(device=self.mocked_obj, command="show usp jsf counters junos-ssl-policy"), dict_expected)



if __name__ == '__main__':
    unittest.main()