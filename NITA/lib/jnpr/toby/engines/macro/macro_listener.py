"""Listener that stops execution if a test fails."""

class macro_listener(object): # pylint: disable=invalid-name,too-few-public-methods
    '''
    Listener for Robot which allows the macro engine to launch at point of testcase failure
    '''
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        pass

    # end_test must be a method to conform to Robot listener, and all positional args must be left in
    def end_test(self, data, result): # pylint: disable=no-self-use,unused-argument
        '''
        Robot defined listener to launch at exact point that test ends
        '''
        from robot.libraries.BuiltIn import BuiltIn
        robot_variables = BuiltIn().get_variables()
        #If test failed...
        if not result.passed and '${macro_engine}' in robot_variables  and not robot_variables.get('${macro_already_run}'):
            macro = robot_variables['${macro}']
            macro_lib = robot_variables['${macro_lib}']
            message = robot_variables.get('${macro_message}', None)
            targets = robot_variables.get('${macro_targets}', 'all')
            resources = robot_variables.get('${macro_resources}', 'all')
            t.log_console("\n\nMacro engine has been initiated due to Test failure!!!!\n" + \
                          "All future keyword calls have been temporarily halted\n" + \
                          "\nNow running macro '" + macro + "' commands on the device(s) " + \
                          "at the exact time of test failure.\n")
            from jnpr.toby.engines.macro.cmd_macro import cmd_macro as CmdMacro
            cmd_obj = CmdMacro()
            cmd_obj.load_macros(macro_lib=macro_lib)
            cmd_obj.run_macros(macros=macro, targets=targets, resources=resources, message=message)
            t.log_console("Macro " + macro + " complete\nResults available at ./latest_toby_logs/macro_logs\n")
