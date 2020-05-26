


robot_lib_ctx  = True
try:
	from robot.libraries.BuiltIn import BuiltIn
	from robot.running.context import EXECUTION_CONTEXTS
	ctx = EXECUTION_CONTEXTS.current if not False else EXECUTION_CONTEXTS.top
	if ctx is None:
               # print('Robot library exists, but not running!, can not access execution context, hence switching to non-robot mode of variables handling')
		robot_lib_ctx = False
except Exception as e:
	print('Import error for Robot builtins, switching to non-Robot mode of Variables handling!')
	robot_lib_ctx = False


class Vars(object):
    """
        Vars class is an Variables interface class for Toby framework. It uses Robot framework BuiltIn lib when used with Robot
        framework. When toby is used as Framework library, it will use Class member variables instead of Robot library.
        It provides set_global_variable() and get_global_variable() to set/get global variables across Robot testcases and test libraries.
        The below code demonstrate the usage of Vars library in robot testcases.

            *** Settings ***
            Library Vars.py

            *** Test Cases ***
            SampleTest
                    ${V1} = VARS.SET GLOBAL VARIABLE        \${V}   "Value1"
                    ${V2} = VARS.GET GLOBAL VARIABLE        \${V}
                    LOG     ${V1}
                    LOG     ${V2}
        The below code demonstrate the usage of the APIs in code
            from jnpr.toby.utils.Vars import Vars

            dict = { 'k1': 'v1', 'k2':'v2'}
            v = Vars().set_global_variable("%{TestVar}", dict)
            x = Vars().get_global_variable("%{TestVar}")

    """

    global_vars = {}

    @staticmethod
    def get_global_variable(var):
        """
            Get global variable value for a given variable

            :param var:
                *MANDATORY* mandatory name of variable
            :return:  Returns the value of global variable
        """
        if robot_lib_ctx:
            return BuiltIn().get_variable_value(var)
        else:
            if var in Vars().global_vars:
                return Vars().global_vars[var]
            else:
                return None

    @staticmethod
    def set_global_variable(var, val):
        """
            Set global variable 'var' to value 'val'

            :param var:
                *MANDATORY* mandatory name of variable
            :param val:
                *MANDATORY* mandatory value to be set for variable
            :return:  Returns None
        """
        if robot_lib_ctx:
            BuiltIn().set_global_variable(var, val)
        else:

            Vars().global_vars[var] = val
            return True


