"""Module contains the utils class for services utils methods"""
# pylint: disable=undefined-variable
__author__ = ['Sumanth Inabathini']
__contact__ = 'isumanth@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import inspect
import os
import re
import numbers
import datetime

from jnpr.toby.utils import iputils

def get_regex_ip():
    """Return regular expression to match IPv4/v6 address

    Example::

      Python:
        get_regex_ip

      Robot:
        Get Regex Ip

    :return: Regular expression to match IPv4/v6 address

    :rtype: string
    """
    regex_ipv4addr = r'(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'

    # The following will match any rfc2372 valid IPv6 address
    hex4 = r'[A-Fa-f\d]{0,4}'
    regex_ipv6addr = r"(?:(?:"+hex4 + \
        r":{1,2}?){2,7}(?:"+regex_ipv4addr+r"|"+hex4+r")?)"
    regex_ipaddr = r"(?:"+regex_ipv6addr+r"|"+regex_ipv4addr+r")"

    return regex_ipaddr

def get_regex_if():
    """Return regular expression to match interface

    Example::

      Python:
        get_regex_if

      Robot:
        Get Regex If

    :return: regular expression to match interface

    :rtype: string
    """
    return r'(?:\b(?:\w+-\d+\/\d+\/|em|irb|as|ae|rlsq|rsp|fxp|gre|ipip|reth|' + \
            r'lo|vlan|psgr|pimd|pime|pip0|pp0|tap)\d*(?::\d+)?(?:\.\d+)?)'

def log(level=None, message=None, show_method=True):
    """Log messages to console/log

    :param string level:
        **OPTIONAL** Level at which message is to be logged to console/log. Default is INFO

    :param string message:
        **REQUIRED** Message to be logged to the console/log

    :param bool show_method:
        **OPTIONAL** Show caller method information in the log. Default is True

    :return: None

    :rtype: None

    Example::

        log('INFO', 'Test case has passed')
        log('ERROR', 'Verifications failed Exp.({}), Act.({})'.format(exp, act))

    """

    if level is None and message is None:
        raise Exception("Issued 'log' without arguments. t.log() Requires min 1 argument.")
    if level is not None and message is None:
        #User didn't pass level; default to INFO
        message = level
        level = 'INFO'

    stack = inspect.stack()[1]
    calling_file = os.path.basename(stack[1])
    line = stack[2]
    sub = stack[3]

    if show_method:
        message = '{}:{}:{}() {}'.format(calling_file, line, sub, message)
    #t.log(level, '{}:{}:{}() {}'.format(calling_file, line, sub, message))
    t.log(level, message)

def cmp_dicts(exp_data, act_data, exact=False, **kwargs):
    """Compare two dictionaries

    :param dict exp_data:
        **REQUIRED** Dictionary with expected data

    :param dict act_data:
        **REQUIRED** Dictionary with actual data

    :param bool exact:
        **OPTIONAL** Check if values are exactly equal. Default is False

    :param string tol_val:
        **OPTIONAL** Tolerance value to be considered in comparing the values. Default is None

    :param string tolerance:
        **OPTIONAL** Tolerance percentage to be considered in comparing the values. Default is None

    :param string tol_perc:
        **OPTIONAL** Tolerance percentage to be considered in comparing the values. Default is None

    :param string err_lvl:
        **OPTIONAL** Error level at which the fail conditions need to be printed. Default is ERROR

    :return: True if values are as expected else False

    :rtype: bool

    Example::

      Python:
        cmp_dicts({'sess_count':10, 'sess_id': '1'}, {'sess_count':10 , 'sess_id': '1'},
                        exact=True)
      Robot:
        ${exp_val} = Create Dictionary sess_count=10  sess_id=1
        ${act_val} = Create Dictionary sess_count=10  sess_id=1
        Cmp Dicts  $exp_val  $act_val  exact=True

    """
    err_lvl = kwargs.get('err_lvl', 'ERROR')
    tolerance = kwargs.get('tol_perc', None)
    tol_val = kwargs.get('tol_val', None)
    tol_str = ''
    if tolerance is not None:
        tol_str = "[Tolerance:"+ str(tolerance) +"%]"
    if tol_val is not None:
        tol_str = "[Tolerance:"+ str(tol_val) +"%]"

    if not exp_data:
        t.log(err_lvl, "exp_data is not defined")
        raise Exception("exp_data is not defined")

    if not act_data:
        t.log(err_lvl, "act_data is not defined")
        raise Exception("act_data is not defined")


    result = True
    for key in exp_data:
        # Making sure the expected value is defined for this key
        if exp_data[key] is None:
            t.log('ERROR', 'Value for key, %s, is not defined in expected values' % (key))
            result = False
            continue

        is_min = is_max = is_neg = False

        exp_val = exp_data[key]
        if key.startswith('min__'):
            t.log('DEBUG', "Found min__ in {}, will do min checking".format(key))
            key = re.sub('^min__', '', key)
            is_min = True
        elif key.startswith('max__'):
            t.log('DEBUG', "Found max__ in {}, will do max checking".format(key))
            key = re.sub('^max__', '', key)
            is_max = True
        elif key.startswith('neg__'):
            t.log('DEBUG', "Found neg__ in {}, will do negative checking".format(key))
            key = re.sub('^neg__', '', key)
            is_neg = True

        if key not in act_data or act_data[key] is None:
            t.log('ERROR', 'Unable to find key, %s, in actual values' % (key))
            result = False
            continue

        act_val = act_data[key]

        iter_result = False

        t.log('INFO', "For {}, Actual value is {} and Expected value is {}".format(key, act_val,
                                                                                   exp_val))

        if isinstance(exp_val, numbers.Number):
            t.log('INFO', "Comparing as number for {}".format(key))
            if tolerance is not None:
                tol_val = int(exp_val * tolerance / 100)
            if is_min:
                if (tol_val is not None and act_val <= (exp_val + tol_val)) or act_val >= exp_val:
                    iter_result = True
            elif is_max:
                if (tol_val is not None and act_val >= (exp_val - tol_val)) or act_val <= exp_val:
                    iter_result = True
            elif is_neg:
                if exact:
                    if act_val != exp_val:
                        iter_result = True
                else:
                    if act_val <= exp_val:
                        iter_result = True
            elif tol_val is not None:
                t.log('INFO', "Comparing {} and {} {}".format(act_val, exp_val, tol_str))
                if act_val >= (exp_val - tol_val) and act_val <= (exp_val + tol_val):
                    iter_result = True
            else:
                if exact:
                    if act_val == exp_val:
                        iter_result = True
                else:
                    if int(act_val) >= exp_val:
                        iter_result = True
        elif iputils.is_ip(exp_val):
            t.log('INFO', "Comparing as IPs for {}".format(key))
            iter_result = iputils.cmp_ip(exp_val, act_val)
        else:
            t.log('INFO', "Comparing as strings for {}".format(key))
            if act_val == exp_val:
                iter_result = True

        if iter_result:
            t.log('INFO', 'For %s, Actual value is %s and Expected is %s' %
                  (key, act_val, exp_val))
            t.log('INFO', 'For %s, Actual value is **AS** expected' % (key))
        else:
            result = False
            t.log('ERROR', 'For %s, Actual value is %s and Expected is %s' %
                  (key, act_val, exp_val))
            t.log('ERROR', 'For %s, Actual value is **NOT** as expected' % (key))

    return result


def cmp_val(exp_val, act_val, msg='value', **kwargs):
    """Compare two values

    :param int exp_val:
        **REQUIRED** Dictionary of expected data

    :param int act_val:
        **REQUIRED** Dictionary of actual data

    :param string msg:
        **OPTIONAL** Description of the values being compared. Default is value

    :param string tol_val:
        **OPTIONAL** Tolerance value to be considered in comparing the values. Default is None

    :param string tol_perc:
        **OPTIONAL** Tolerance percentage to be considered in comparing the values. Default is None

    :param string err_lvl:
        **OPTIONAL** Error level at which the fail conditions need to be printed. Default is ERROR

    :return: True if values as expected else False

    :rtype: bool

    Example::

      Python:
        cmp_val(1000, 900, msg='Setup Rate', tol_val=100, tol_perc=1, err_lvl='ERROR')
      Robot:
        Cmp Val  1000  900 msg=Setup Rate  tol_val=100  tol_perc=1  err_lvl=ERROR)

    """
    err_lvl = kwargs.get('err_lvl', 'ERROR')
    tol_perc = kwargs.get('tol_perc', None)
    tol_val = kwargs.get('tol_val', None)
    result = None
    if not act_val:
        if exp_val:
            t.log(
                err_lvl, "When expecting {}, actual value alone cannot be zero".format(exp_val))
            result = False
        else:
            t.log('INFO', "Both the input values are zero")
            result = True
        return result

    if tol_perc:
        # Tolerance % is specified
        if ((abs(exp_val - act_val) / float(exp_val)) * 100) > tol_perc:
            t.log(err_lvl, "Actual {}({}) and expected {}({}) are **NOT** within the \
                     tolerance limit of {}%".format(msg, act_val, msg, exp_val, tol_perc))
            result = False
        else:
            t.log('INFO', "Actual {}({}) and expected {}({}) **ARE** within the tolerance limit \
             of {}%".format(msg, act_val, msg, exp_val, tol_perc))
            result = True
        return result

    if tol_val:
        # Tolerance value is specified
        if abs(exp_val - act_val) > tol_val:
            t.log(err_lvl, "Actual {}({}) and expected {}({}) are **NOT** within the tolerance \
              limit of {}".format(msg, act_val, msg, exp_val, tol_val))
            return False
        else:
            t.log('INFO', "Actual {}({}) and expected {}({}) **ARE** within the tolerance limit \
             of {}".format(msg, act_val, msg, exp_val, tol_val))
            return True

    if int(act_val) >= int(exp_val):
        t.log('INFO', "Actual {}({}) and expected {}({}) are **AS** \
          expected".format(msg, act_val, msg, exp_val))
        return True
    else:
        t.log(err_lvl, "Actual {}({}) and expected {}({}) are **NOT** as \
          expected".format(msg, act_val, msg, exp_val))
        return False


def update_data_from_output(data, output, args):
    """Update data with the values in output based on the args

    :param dict data:
        **REQUIRED** Dictionary to be updated based on the args

    :param dict output:
        **REQUIRED** Dictionary containing the data to be updated

    :param dict args:
        **OPTIONAL** Dictionary containing the keys to be updated

    :return: None

    :rtype: None

    Example::

      Python:
        get_val({}, {'pool-configured-port-range': 10} ,
            { 'pool-configured-port-range': 'configured_port_range'})
      Robot:

        ${output} = Create Dictionary pool-configured-port-range=10
        ${args} = Create Dictionary pool-configured-port-range=configured_port_range
        Get Val  ${data}  ${output}  ${args}

    """

    for key, value in args.items():
        if key in output:
            data[value] = str(output[key])


#def load_defaults_and_update_opts_from_args(kwargs, defaults=None, obj=None):
def update_opts_from_args(args, defaults=None, opts=None):
    """Load default values and update optional values from input args

    First, opts is loaded with default values, if passed and then all the optional arguments
    are loaded from args.
    opts is set to empty dictionary if not passed.

    :param dict args:
        **REQUIRED** Keyword args list

    :param dict defaults:
        **OPTIONAL** Dictionary containing the default data. Default is None

    :param dict opts:
        **OPTIONAL** Args and values are updated in the input object passed. Default is None

    :return: Dictionary updated with defaults and args

    :rtype: dict

    Example::

      Python:
        Eg 1:
        input = update_opts_from_args(args={'src_ip' : '1.1.1.1'}, defaults={'src_ip' : None})
        Here, input is updated with defaults and args

        Eg 2:
        this = {}
        this['count'] = 1
        update_opts_from_args(args={'src_ip' : '1.1.1.1'}, defaults={'src_ip' : None}, opts=this)

        In this example, this is updated with defaults and args

      Robot:

        ${args} = Create Dictionary src_ip=1.1.1.1
        ${defaults} = Create Dictionary src_ip=None
        ${opts} = Update Opts From Args  ${args}  ${defaults}  ${opts}
    """

    if opts is None:
        opts = {}

    # Set all default values
    if defaults is not None:
        for key in defaults:
            opts[key] = defaults[key]

    # Overwrite the default values if passed by user
    for key in args:
        # If default value is integer, preserve the data type
        # as all values passed from Robot will be strings
        if key in defaults and isinstance(defaults[key], int):
            opts[key] = int(args[key])
        else:
            opts[key] = args[key]

    return opts

def get_time_diff(datetime1, datetime2):
    """Return time difference in seconds between two datetimes

    :param string datetime1:
        **REQUIRED** First parameter containing datetime

    :param string datetime2:
        **OPTIONAL** Second parameter containing datetime

    :return: String containing diffrence in seconds

    :rtype: string

    Example::

      Python:
        get_time_diff('2011-10-31 04:46:04', '2011-10-31 04:48:34')

      Robot:

        Get Time Diff  2011-10-31 04:46:04  011-10-31 04:48:34
    """

    date2 = datetime.datetime.strptime(datetime2, '%Y-%m-%d %H:%M:%S')
    date1 = datetime.datetime.strptime(datetime1, '%Y-%m-%d %H:%M:%S')
    diff = date2 - date1
    return diff.total_seconds()
