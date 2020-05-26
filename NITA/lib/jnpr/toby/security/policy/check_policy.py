import re

def check_security_policy_on_device(device=None , policy_name=None, expected=None, detail=False):

    """

    This function is used for checking security policies on device 

    Examples:

    :param Device device:
        **REQUIRED** Router handle object
    :param str policy_name:
        **REQUIRED** policy name 
    :param str expected:
        **REQUIRED** expected output from policy  
    :param bool detail:
        *OPTIONAL* display policy details output. default=False  

    :return: Exception will occurred if expected value not be present
    """
        

    if device is None:
        raise Exception("'device' is mandatory parameter - device handle")


    if device is not None :
     if detail:
       result = device.cli(command="show security policies policy-name "+policy_name+" detail").response()
     if detail is False:
       result = device.cli(command="show security policies policy-name "+policy_name).response()

       match = re.search(r''+expected, result)

       if match:
            device.log(level='INFO', message='Matched: ' + expected)
       else:  
          device.log(level='ERROR', message='Not Matched: ' + expected)
          raise Exception('Value not present '+expected)
