import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.security import pic
from jnpr.toby.hldcl.juniper.security.srx import Srx
from unittest.mock import MagicMock, patch, PropertyMock 

class Response:
    # To return response of shell() method
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()
    def test_get_pic_name(self):
        try:
            pic.get_pic_name()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            pic.get_pic_name(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'port' is a mandatory argument")

        string = """Flow Sessions on FPC0 PIC1: Total sessions: 0 Flow Sessions on FPC0 PIC2: Total sessions: 0 Flow Sessions on FPC0 PIC3: Total sessions: 0 Flow Sessions on FPC1 PIC0: Total sessions: 0 Flow Sessions on FPC1 PIC1: Session ID: 50000111, Policy name: 1/4, Timeout: 1800, Valid In: 4.0.0.1/34623 --> 5.0.0.1/443;tcp, Conn Tag: 0x0, If: xe-2/2/0.0, Pkts: 6, Bytes: 591, CP Session ID: 50000140 Out: 5.0.0.1/443 --> 4.0.0.1/34623;tcp, Conn Tag: 0x0, If: xe-2/2/1.0, Pkts: 4, Bytes: 1096, CP Session ID: 50000140 Total sessions: 1 Flow Sessions on FPC1 PIC2: Total sessions: 0 Flow Sessions on FPC1 PIC3: Total sessions: 0 """
        self.mocked_obj.cli().response = MagicMock(return_value=string)
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["FPC0.PIC1", "FPC1.PIC1"])
        self.mocked_obj.get_model = MagicMock(return_value="SRX5k")
        #self.assertEqual(pic.get_pic_name(device=self.mocked_obj, port='443'),["fpc0.pic1", "fpc1.pic1"])
        self.assertEqual(pic.get_pic_name(device=self.mocked_obj, port='443'), "FPC1.PIC1")

    def test_execute_pic_command(self):
        try:
            pic.execute_pic_command()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")
        try:
            pic.get_pic_name(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'port' is a mandatory argument")

        string = """['fpc0.pic1', 'fpc0.pic2', 'fpc0.pic3', 'fpc1.pic0', 'fpc1.pic1', 'fpc1.pic2', 'fpc1.pic3'] """
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=string)
        self.mocked_obj.vty = MagicMock(return_value=['fpc0.pic1'])
        self.assertTrue(pic.execute_pic_command(device=self.mocked_obj, command='plugin junos_ssl set proxy one-crypto status 1'))

    def test_get_pic_list(self):
        try:
            pic.get_pic_list()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")
            #self.assertEqual("'device' is a mandatory argument")

        pic_list = ['fpc0.pic1', 'fpc0.pic2']
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=pic_list)
        #self.mocked_obj.vty = MagicMock(return_value=['fpc0.pic1', 'fpc0.pic2'])
        self.assertEqual(pic.get_pic_list(device=self.mocked_obj),['fpc0.pic1', 'fpc0.pic2'])        
