from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.security.appsecure import context_propagation
from jnpr.toby.hldcl.juniper.junos import Juniper


# To return response of vty() mehtod
class Response:

    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    # Mocking the handle and its methods
    mocked_obj = MagicMock(spec=Juniper)
    mocked_obj.log = MagicMock()
    mocked_obj.vty = MagicMock()
   
    def test_get_context_propagation_trace_exception(self):
        try:
            context_propagation.get_context_propagation_trace()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")
 
    def test_get_context_propagation_trace(self):
        lst = [Response("abcd")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.get_context_propagation_trace(
                           device=self.mocked_obj),
                           "abcd")


    def test_clear_flow_trace_exception(self):
        try:
            context_propagation.clear_flow_trace()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

    def test_clear_flow_trace(self):
        lst = [Response("abcd")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.clear_flow_trace(
                           device=self.mocked_obj),
                           True)

    def test_enable_jdpi_test_plugin_exception(self):
        try:
            context_propagation.enable_jdpi_test_plugin()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

    def test_enable_jdpi_test_plugin(self):
        lst = [Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response("")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.enable_jdpi_test_plugin(
                           device=self.mocked_obj),
                           True)

    def test_enable_jdpi_test_plugin_service(self):
        lst = [Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response("")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.enable_jdpi_test_plugin(
                           device=self.mocked_obj,
                           service_plugin= "yes"),
                           True)
 
    def test_disable_jdpi_test_plugin_exception(self):
        try:
            context_propagation.disable_jdpi_test_plugin()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

 
    def test_disable_jdpi_test_plugin(self):
        lst = [Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response(""),Response("")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.disable_jdpi_test_plugin(
                           device=self.mocked_obj),
                           True)

    def test_register_context_exception_no_device(self):
        try:
            context_propagation.register_context()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")


    def test_register_context_exception(self):
        try:
            context_propagation.register_context(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "protocol_id is mandatory argument")


    def test_register_context_success_no_context(self):
        lst = [Response("Successfully Registered")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.register_context(
                           device=self.mocked_obj,
                           protocol_id="75"),
                           True)

    def test_register_context_failure_no_context(self):
        lst = [Response("Failed")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        try:
            context_propagation.register_context(
                           device=self.mocked_obj,
                           protocol_id="75")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Contexts registration failed")

    def test_register_context_success_with_context(self):
        lst = [Response("Successfully Registered"),Response("Successfully Registered")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.register_context(
                           device=self.mocked_obj,
                           protocol_id="75",
                           contexts=["2","3"]),
                           True)

    def test_register_context_failure_with_context(self):
        lst = [Response("Successfully Registered"),Response("failed")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        try:
            context_propagation.register_context(
                           device=self.mocked_obj,
                           protocol_id="75",
                           contexts=["2","3"])
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Context 3 registration failed")
#---------------------------------------------------

    def test_deregister_context_exception_no_device(self):
        try:
            context_propagation.deregister_context()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

    def test_deregister_context_exception(self):
        try:
            context_propagation.deregister_context(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "protocol_id is mandatory argument")

    def test_deregister_context_success_no_context(self):
        lst = [Response("Successfully Deregistered")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.deregister_context(
                           device=self.mocked_obj,
                           protocol_id="75"),
                           True)

    def test_deregister_context_failure_no_context(self):
        lst = [Response("Failed")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        try:
            context_propagation.deregister_context(
                           device=self.mocked_obj,
                           protocol_id="75")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Contexts deregistration failed")

    def test_deregister_context_success_with_context(self):
        lst = [Response("Successfully Deregistered"),Response("Successfully Deregistered")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.deregister_context(
                           device=self.mocked_obj,
                           protocol_id="75",
                           contexts=["2","3"]),
                           True)

    def test_deregister_context_failure_with_context(self):
        lst = [Response("Not Deregistered"),Response("failed")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        try:
            context_propagation.deregister_context(
                           device=self.mocked_obj,
                           protocol_id="75",
                           contexts=["4"])
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Context 4 deregistration failed")
#-----------------------------------------

    def test_clear_context_hit_exception(self):
        try:
            context_propagation.clear_context_hit()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

    def test_clear_context_hit_protocol_all(self):
        lst = [Response("Cleared all the application context stats")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.clear_context_hit(
                           device=self.mocked_obj),
                           True)

    def test_clear_context_hit_protocol_all_failure(self):
        lst = [Response("Not cleared all the application context stats")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        try:
            context_propagation.clear_context_hit(
                           device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Contexts are not cleared")
#---------------------------------------------------

    def test_match_context_hit_exception_no_device(self):
        try:
            context_propagation.match_context_hit(context_name="abc")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

    def test_match_context_hit_exception(self):
        try:
            context_propagation.match_context_hit(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "context_name,context_id and hit_count are mandatory argument")


    def test_match_context_hit_success(self):
        lst = [Response("method                  (555)          5")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.match_context_hit(
                           device=self.mocked_obj,
                           context_name="method",
                           context_id="555",
                           protocol="all",
                           hit_count="5"),
                           True)

    def test_match_context_hit_failure(self):
        lst = [Response("method                  (555)          5")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        try:
            context_propagation.match_context_hit(
                           device=self.mocked_obj,
                           context_name="method",
                           context_id="555",
                           protocol="all",
                           hit_count="6")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "method context was not hit 6 times, match unsuccessfull")
#--------------------------------------------------

    def test_match_integer_context_propagation_exception(self):
        try:
            context_propagation.match_integer_context_propagation()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

    def test_match_integer_context_propagation_execption(self):
        try:
            context_propagation.match_integer_context_propagation(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "context_id and value are mandatory argument")

    def test_match_integer_context_propagation_success_with_count(self):
        lst = [Response("pctxt_id : signed 32 bit data => [872=>699]")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.match_integer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="872",
                           value="699",
                           count="1"),
                           True)

    def test_match_integer_context_propagation_success_with_trace(self):
        trace = "pctxt_id : signed 32 bit data => [872=>699]"
        self.assertEqual(
             context_propagation.match_integer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="872",
                           value="699",
                           count="1",
                           trace=trace),
                           True)

    def test_match_integer_context_propagation_success_no_count(self):
        lst = [Response("pctxt_id : signed 32 bit data => [872=>699]")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.match_integer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="872",
                           value="699"),
                           True)

    def test_match_integer_context_propagation_failure_with_count(self):
        lst = [Response("pctxt_id : signed 32 bit data => [872=>699]")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        try:
             context_propagation.match_integer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="872",
                           value="699",
                           count="2")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Context not propgated as per expectation")

    def test_match_integer_context_propagation_failure_no_count(self):
        lst = [Response("pctxt_id : signed 32 bit data => [872=>699]")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        try:
             context_propagation.match_integer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="872",
                           value="700")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "700 pattern not found in trace")
 
#---------------------------------------------------

    def test_match_string_context_propagation_exception_no_device(self):
        try:
            context_propagation.match_string_context_propagation()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

    def test_match_string_context_propagation_exception(self):
        try:
            context_propagation.match_string_context_propagation(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "context_id and value are mandatory argument")

    def test_match_string_context_propagation_success_with_count(self):
        lst = [Response("pctxt_id : string => [555=>[0818] T26 JDPI-TEST: EHLO(4)][0819]")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.match_string_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="555",
                           length="4",
                           value="ehlo",
                           count="1"),
                           True)

    def test_match_string_context_propagation_success_with_no_length(self):
        lst = [Response("pctxt_id : string => [555=>[0818] T26 JDPI-TEST: EHLO(4)][0819]")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.match_string_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="555",
                           value="ehlo",
                           count="1"),
                           True)

    def test_match_string_context_propagation_success_with_trace(self):
        trace = "pctxt_id : string => [555=>[0818] T26 JDPI-TEST: EHLO(4)][0819]"
        self.assertEqual(
             context_propagation.match_string_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="555",
                           length="4",
                           value="ehlo",
                           count="1",
                           trace=trace),
                           True)

    def test_match_string_context_propagation_success_no_count(self):
        lst = [Response("pctxt_id : string => [555=>[0818] T26 JDPI-TEST: EHLO(4)][0819]")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        self.assertEqual(
             context_propagation.match_string_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="555",
                           length="4",
                           value="ehlo"),
                           True)

    def test_match_string_context_propagation_failure_with_count(self):
        lst = [Response("pctxt_id : string => [555=>[0818] T26 JDPI-TEST: MAIL(4)][0819]")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)

        try:
            context_propagation.match_string_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="555",
                           length="4",
                           value="mail",
                           count="2")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Context not propgated as per expectation")

    def test_match_string_context_propagation_failure_no_count(self):
        lst = [Response("pctxt_id : string => [555=>[0818] T26 JDPI-TEST: MAIL(4)][0819]")]
        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)

        try:
            context_propagation.match_string_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="555",
                           length="4",
                           value="ehlo")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ehlo pattern not found in trace")
#-----------------------------

    def test_match_buffer_context_propagation_exception_no_device(self):
        try:
            context_propagation.match_buffer_context_propagation()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")


    def test_match_buffer_context_propagation_exception(self):
        try:
            context_propagation.match_buffer_context_propagation(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "context_id,initial_bytes and last_bytes are mandatory argument")

    def test_match_buffer_context_propagation_exception_final_trace_not_found(self):
        lst = [Response("pctxt_id : smtp byte_array total len to print => [514=>49] \r pctxt_id : smtp byte_array partial info => [514=>0x74 0x65 0x73 0x74 0x20 0x6d 0x61 0x69 0x6c 0x20 0x62 (125))] \r pctxt_id : smtp byte_array partial info => [514=>0x6c 0x64 0x20 0x61 0x6c 0x73 0x65 0x65 0x20 0x61 0x74 0x74 0x61 0x63 0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]")]

        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        first_byte = "74 65 73 74 20 6d 61 69"
        last_byte = "68 6d 65 6e 74 0d 0a"
        try:
            context_propagation.match_buffer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="514",
                           initial_bytes=first_byte,
                           last_bytes=last_byte)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Final/Last trace of content not found,match cannot take place")

# pctxt_id : smtp byte_array partial info =&gt; [514=&gt;0x74 0x65 0x73 0x74 0x20 0x6d 0x61 0x69 0x6c 0x20 0x62 0x6f 0x64 0x79 0x0d 
#pctxt_id : smtp byte_array final info =&gt; [514=&gt;0x6c 0x64 0x20 0x61 0x6c 0x73 0x65 0x65 0x20 0x61 0x74 0x74 0x61 0x63 0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]

    def test_match_buffer_context_propagation_success(self):
        lst = [Response("pctxt_id : smtp byte_array total len to print => [514=>49] \r pctxt_id : smtp byte_array partial info => [514=>0x74 0x65 0x73 0x74 0x20 0x6d 0x61 0x69 0x6c 0x20 0x62 (125))] \r pctxt_id : smtp byte_array final info => [514=>0x6c 0x64 0x20 0x61 0x6c 0x73 0x65 0x65 0x20 0x61 0x74 0x74 0x61 0x63 0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]")]

        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        first_byte = "74 65 73 74 20 6d 61 69"
        last_byte = "68 6d 65 6e 74 0d 0a"
        self.assertEqual(
             context_propagation.match_buffer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="514",
                           initial_bytes=first_byte,
                           last_bytes=last_byte,
                           length="49"),
                           True)

    def test_match_buffer_context_propagation_success_with_trace(self):
        trace = "pctxt_id : smtp byte_array total len to print => [514=>49] \r pctxt_id : smtp byte_array partial info => [514=>0x74 0x65 0x73 0x74 0x20 0x6d 0x61 0x69 0x6c 0x20 0x62 (125))] \r pctxt_id : smtp byte_array final info => [514=>0x6c 0x64 0x20 0x61 0x6c 0x73 0x65 0x65 0x20 0x61 0x74 0x74 0x61 0x63 0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]"

        first_byte = "74 65 73 74 20 6d 61 69"
        last_byte = "68 6d 65 6e 74 0d 0a"
        self.assertEqual(
             context_propagation.match_buffer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="514",
                           initial_bytes=first_byte,
                           last_bytes=last_byte,
                           trace=trace,
                           length="49"),
                           True)

    def test_match_buffer_context_propagation_success_last_bytes_less_in_trace(self):
        lst = [Response("pctxt_id : smtp byte_array total len to print => [514=>49] \r pctxt_id : smtp byte_array partial info => [514=>0x74 0x65 0x73 0x74 0x20 0x6d 0x61 0x69 0x6c 0x20 0x62 (125))] \r pctxt_id : smtp byte_array final info => [514=>0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]")]

        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        first_byte = "74 65 73 74 20 6d 61 69"
        last_byte = "74 61 63 68 6d 65 6e 74 0d 0a"
        self.assertEqual(
             context_propagation.match_buffer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="514",
                           initial_bytes=first_byte,
                           last_bytes=last_byte,
                           length="49"),
                           True)

    def test_match_buffer_context_propagation_failure_init_cont_not_match(self):
        lst = [Response("pctxt_id : smtp byte_array total len to print => [514=>49] \r pctxt_id : smtp byte_array partial info => [514=>0x74 0x65 0x73 0x74 0x20 0x6d 0x61 0x69 0x6c 0x20 0x62 (125))] \r pctxt_id : smtp byte_array final info => [514=>0x6c 0x64 0x20 0x61 0x6c 0x73 0x65 0x65 0x20 0x61 0x74 0x74 0x61 0x63 0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]")]

        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        first_byte = "ISMAIL"
        last_byte = "68 6d 65 6e 74 0d 0a"
        try:
            context_propagation.match_buffer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="514",
                           initial_bytes=first_byte,
                           last_bytes=last_byte)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Starting contents not matched")


    def test_match_buffer_context_propagation_failure_last_cont_not_match(self):
        lst = [Response("pctxt_id : smtp byte_array total len to print => [514=>49] \r pctxt_id : smtp byte_array partial info => [514=>0x74 0x65 0x73 0x74 0x20 0x6d 0x61 0x69 0x6c 0x20 0x62 (125))] \r pctxt_id : smtp byte_array final info => [514=>0x6c 0x64 0x20 0x61 0x6c 0x73 0x65 0x65 0x20 0x61 0x74 0x74 0x61 0x63 0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]")]

        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        first_byte = "74 65 73 74 20 6d 61 69"
        last_byte = "68 6d 65 6e aa bb 74 0d 0a"
        try:
            context_propagation.match_buffer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="514",
                           initial_bytes=first_byte,
                           last_bytes=last_byte,
                           length="49")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Contents not matched fully")
    

    def test_match_buffer_context_propagation_failure_length_not_match(self):
        lst = [Response("pctxt_id : smtp byte_array total len to print => [514=>49] \r pctxt_id : smtp byte_array partial info => [514=>0x74 0x65 0x73 0x74 0x20 0x6d 0x61 0x69 0x6c 0x20 0x62 (125))] \r pctxt_id : smtp byte_array final info => [514=>0x6c 0x64 0x20 0x61 0x6c 0x73 0x65 0x65 0x20 0x61 0x74 0x74 0x61 0x63 0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]")]

        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        first_byte = "74 65 73 74 20 6d 61 69"
        last_byte = "68 6d 65 6e 74 0d 0a"
        try:
            context_propagation.match_buffer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="514",
                           initial_bytes=first_byte,
                           last_bytes=last_byte,
                           length="50")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Length of content is not matched,will not match content")

    def test_match_buffer_context_propagation_success_only_final_info(self):
        lst = [Response("pctxt_id : smtp byte_array total len to print => [514=>49] \r pctxt_id : smtp byte_array final info => [514=>0x6c 0x64 0x20 0x61 0x6c 0x73 0x65 0x65 0x20 0x61 0x74 0x74 0x61 0x63 0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]")]

        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        first_byte = "6c 64 20 61 6c 73 65 65 20 61"
        last_byte = "68 6d 65 6e 74 0d 0a"
        self.assertEqual(
             context_propagation.match_buffer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="514",
                           initial_bytes=first_byte,
                           last_bytes=last_byte,
                           length="49"),
                           True)

    def test_match_buffer_context_propagation_failure_only_final_info_init_cont_not_matched(self):
        lst = [Response("pctxt_id : smtp byte_array total len to print => [514=>49] \r pctxt_id : smtp byte_array final info => [514=>0x6c 0x64 0x20 0x61 0x6c 0x73 0x65 0x65 0x20 0x61 0x74 0x74 0x61 0x63 0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]")]

        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        first_byte = "6c 64 20 61 65 20 61"
        last_byte = "68 6d 65 6e 74 0d 0a"
        try:
            context_propagation.match_buffer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="514",
                           initial_bytes=first_byte,
                           last_bytes=last_byte,
                           length="49")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Initial contents not matched")

    def test_match_buffer_context_propagation_failure_only_final_info_last_cont_not_matched(self):
        lst = [Response("pctxt_id : smtp byte_array total len to print => [514=>49] \r pctxt_id : smtp byte_array final info => [514=>0x6c 0x64 0x20 0x61 0x6c 0x73 0x65 0x65 0x20 0x61 0x74 0x74 0x61 0x63 0x68 0x6d 0x65 0x6e 0x74 0x0d 0x0a (120/49/49))]")]

        self.mocked_obj.get_srx_pfe_names = MagicMock(return_value=["fpc0"])
        self.mocked_obj.vty = MagicMock(side_effect=lst)
        first_byte = "6c 64 20 61 6c 73 65 65 20 61"
        last_byte = "68 6d 65 6e 74 0d 0a 23 45 66"
        try:
            context_propagation.match_buffer_context_propagation(
                           device=self.mocked_obj,
                           cntx_id="514",
                           initial_bytes=first_byte,
                           last_bytes=last_byte,
                           length="49")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Contents not matched fully")

if __name__ == '__main__':
    unittest.main()
