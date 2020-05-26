# coding: UTF-8
"""Functions/Keywords to Search values in an xml"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements

from jxmlease import parse
import pprint

__author__ = ['Revant Tiku']
__contact__ = 'rtiku@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def _findkeys(dictionary, key):
    if isinstance(dictionary, list):
        for i in dictionary:
            for x in _findkeys(i, key):
                yield x
    elif isinstance(dictionary, dict):
        if key in dictionary:
            yield dictionary[key]
        for j in dictionary.values():
            for x in _findkeys(j, key):
                yield x


def verify_values_in_cli_xml(device=None, cli=None, cli_xml=None, return_output=False, hierarchy=None, **kwargs):
    """
    Verifying Values in a CLI show command xml

    :Example:

    python: verify_values_in_cli_xml(device=r0, cli='show security ipsec security-association detail',
                            sa_block_state='up', sa_vpn_name='vpn1')

    robot: Verify Values In CLI_XML    device=${r0}    cli=show security ipsec security-association detail
           ...    sa_block_state=up    sa_vpn_name=vpn1

    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str cli:
        **REQUIRED**  CLI command.
    :param str cli_xml:
        **REQUIRED**  CLI output in xml format passed as a string.
    :param bool return_output:
        *OPTIONAL*  Set this option to True if you want the output of an xml tag to be returned.
    :param str hierarchy:
        **REQUIRED**  XML hierarchy tag to retun output. Parameter is not for usage.
    :param str kwargs: key=value pairs to match outputs.
        *OPTIONAL*  Ex.  sa_block_state='up' for <sa-block-state>up</sa-block-state>. Replace '-' with '_' from xml tags
                    For return_output=True, set key = ' '.
    :return:
    """
    if device is None:
        raise Exception("'device' is mandatory parameter.")
    if len(kwargs) == 0 and hierarchy is None:
        raise Exception('No values to match. Please pass key=value parameters to match. '
                        'Else use hierarchy parameter with return_value=True.')
    if cli is None and cli_xml is None:
        raise Exception("Either 'cli' or 'cli_xml' is mandatory. Use one of the two")
    if cli is not None:
        cli_xml = device.cli(command=cli, format='xml').response()
    if cli_xml[:4] == 'show':
        ind = cli_xml.index('\n')
        cli_xml = cli_xml[ind + 1:]
    dict_out = parse(cli_xml)
    return_value = {}
    if hierarchy is not None:
        key_xml = hierarchy.replace('_', '-')
        output = list(_findkeys(dict_out, key_xml))
        if len(output) == 0:
            raise Exception('Cannot find the mentioned key(s). ' + exp)
        return output
    device.log(pprint.pformat(dict_out))
    passed = '\nPassed Verifications-> \n<Tag>:<Matched Value> \n'
    failed = '\nFailed Verifications-> \n<Tag>:<Expected Value>:<Found Value> \n'
    result = False
    for key, value in kwargs.items():
        key_xml = key.replace('_', '-')
        output = list(_findkeys(dict_out, key_xml))
        if len(output) == 0:
            raise Exception('Cannot find the mentioned key(s). ' + exp)
        if return_output:
            return_value[key] = output
        else:
            return_value = True
            if len(output) > 1:
                result = False
                out_x = '-'
                for x in range(0,len(output)):
                    if output[x] == value:
                        passed += key + ':' + value + '\n'
                        result = True
                        out_x = output[x]
                        break
                    out_x = output[x]
                if not result:
                    failed += key + ':' + value + ':' + out_x + '\n'
                    result = False
                    break
            if len(output) == 1:
                if len(output[0]) > 1 and (isinstance(output[0], list)):
                    result = False
                    out_x = '-'
                    for x in range(0, len(output[0])):
                        if output[0][x] == value:
                            passed += key + ':' + value + '\n'
                            result = True
                            out_x = output[0][x]
                            break
                        out_x = output[0][x]
                    if not result:
                        failed += key + ':' + value + ':' + str(out_x) + '\n'
                        result = False
                        break
                elif output[0] == value:
                    passed += key + ':' + value + '\n'
                    result = True
                else:
                    failed += key + ':' + value + ':' + str(output[0]) + '\n'
                    result = False
                    break
    if (isinstance(return_value, dict) and len(return_value) > 0) or not return_value:
        return return_value
    device.log(passed)
    device.log(failed)
    if not result:
        device.log('\n##### Overall Result: Verification FAILED. #####')
        raise Exception('##### Overall Result: Verification FAILED. #####')
    else:
        device.log('\n##### Overall Result: All verifications PASSED. ##### ')
        return True


def verify_values_in_hierarchy_xml(device=None, cli=None, cli_xml=None, hierarchy=None, **kwargs):
    """
    Verifying Values in a CLI show command xml under a particular hierarchy

    :Example:

    python: verify_values_in_hierarchy_xml(device=r0, cli='show security ipsec security-association detail'
                        hierarchy='ipsec_security_associations', sa_direction='inbound', sa_tunnel_index='2')

    robot: Verify Values In Hierarchy XML    device=${r0}    cli=show security ipsec security-association detail
           ...    hierarchy=ipsec_security_associations    sa_direction=inbound    sa_tunnel_index=2

    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str cli:
        **REQUIRED**  CLI command.
    :param str cli_xml:
        **REQUIRED**  CLI output in xml format passed as a string.
    :param str hierarchy:
        **REQUIRED** Hierarchy leaf xml tag for which tags in kwargs has to be checked.
    :param kwargs:
        *OPTIONAL* key=value pairs. Replace '-' with '_' in xml tag names.
    :return:
    """
    if device is None:
        raise Exception("'device' is mandatory parameter.")
    if cli is None and cli_xml is None:
        raise Exception("Either 'cli' or 'cli_xml' is mandatory. Use one of the two. Use 'cli' with 'device'")
    if len(kwargs) == 0:
        raise Exception('No values to match. Please pass key=value parameters to match.')
    if hierarchy is None:
        raise Exception("'hierarchy' is a mandatory parameter.")
    output = verify_values_in_cli_xml(device=device, cli=cli, cli_xml=cli_xml, return_output=True, hierarchy=hierarchy)
    #device.log(pprint.pformat(output))
    result = False
    passed = '\nPassed Verifications-> \nNo such hierarchy found in CLI output'
    failed = '\nFailed Verifications-> \nNo such hierarchy found in CLI output'
    for y in range(0, len(output)):
        for x in range(0,len(output[y])):
            result = False
            passed = '\nPassed Verifications-> \n<XML Tag>:<Matched Value> \n'
            failed = '\nFailed Verifications-> \n<XML Tag>:<Expected Value>:<Found Value> \n'
            for key, value in kwargs.items():
                key_xml = key.replace('_', '-')
                try:
                    test = output[y][x][key_xml]
                except:
                    try:
                        test = output[y][key_xml]
                    except:
                        raise Exception('Verifying tag values not found.')
                if (len(test) > 1) and (isinstance(test, list)):
                    result = False
                    for index in range(0, len(test)):
                        if value == test[index]:
                            passed += key + ':' + value + '\n'
                            result = True
                            break
                    if not result:
                        failed += key + ':' + value + ':' + str(test) + '\n'
                        break
                elif value == test:
                    passed += key + ':' + value + '\n'
                    result = True
                else:
                    failed += key + ':' + value + ':' + test + '\n'
                    result = False
                    break
            if result:
                break
        if result:
            break
    device.log('\n Verification Hierarchy: ' + hierarchy)
    device.log(passed)
    device.log(failed)
    if not result:
        device.log('\n##### Overall Result: Verification FAILED. #####')
        raise Exception('\n##### Overall Result: Verification FAILED. #####')
    else:
        device.log('\n##### Overall Result: All verifications PASSED. ##### ')
        return True
