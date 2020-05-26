import unittest
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.juniper.routing.router import *
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.utils.response import Response

builtin_string = 'builtins'

class TestJunosModule(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = self
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()

    def test_vty(self):
        handle = MagicMock(spec=Juniper)
        handle.mode = "vty"
        handle.destination = "fpc1"
        handle.channels = [] #Used when TobyException is raised
        handle.execute.return_value = 'Syntax error'
        handle.vty_timeout  = 60
        print("Testing vty API")
        result = Juniper.vty(handle,command=" " ,destination="",pattern="%")
        self.assertEqual(type(result),Response,"FAIL")
        try:
            result = Juniper.vty(handle,command=None ,destination="",pattern="%")
        except Exception as err:
            self.assertEqual(err.args[0], "None value is not allowed as 'command'")
        try:
            result = Juniper.vty(handle,command="" ,destination=None,pattern="%")
        except Exception as err:
            self.assertEqual(err.args[0], "None value can not be passed as  'destination'")
        try:
            result = Juniper.vty(handle,destination="",pattern="%")
        except Exception as err:
            self.assertEqual(err.args[0], "vty() missing 1 required positional argument: 'command'")
        try:
            result = Juniper.vty(handle,command="",pattern="%")
        except Exception as err:
            self.assertEqual(err.args[0], "vty() missing 1 required positional argument: 'destination'")
        try:
            result = Juniper.vty(handle,command="", destination="")
        except Exception as err:
            self.assertEqual(err.args[0], "Syntax Error when executing vty command")
        try:
            result = Juniper.vty(handle,command="", destination="" ,pattern=["%", "$"])
        except Exception as err:
            self.assertEqual(err.args[0], "Syntax Error when executing vty command") 

    def test_cty(self):
        handle = MagicMock(spec=Juniper)
        handle.mode = "cty"
        handle.destination = "fpc1"
        print ("Testing cty API")
        handle.channels = [] #Used when TobyException is raised
        handle.cty_timeout  = 60
        try:
            result = Juniper.cty(handle, command=None ,destination="",pattern="%")
        except Exception as err:
            self.assertEqual(err.args[0], "None value is not allowed as 'command'")
        try:
            result = Juniper.cty(handle, command="" ,destination=None,pattern="%")
        except Exception as err:
            self.assertEqual(err.args[0], "None value can not be passed as  'destination'")
        try: 
            result = Juniper.cty(handle, destination="", pattern="%")
        except Exception as err:
            self.assertEqual(err.args[0], "cty() missing 1 required positional argument: 'command'")
        try:
            result = Juniper.cty(handle, command="", pattern="%")
        except Exception as err:
            self.assertEqual(err.args[0], "cty() missing 1 required positional argument: 'destination'")
        try:
            result = Juniper.cty(handle,command="", destination="")
        except Exception as err:
            self.assertEqual(err.args[0], "Syntax Error when executing cty command")
        try:
            result = Juniper.cty(handle, command="", destination="" , pattern=["%", "$"])
        except Exception as err:
            self.assertEqual(err.args[0], "Syntax Error when executing cty command")
        try:
            result = Juniper.cty(handle, command=" ", destination=" " , pattern="%")
        except Exception as err:
            self.assertEqual(err.args[0], "Syntax Error when executing vty command")



if __name__ == '__main__':
    unittest.main()



