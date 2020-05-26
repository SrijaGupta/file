"""
IDP policy related Keywords
"""

import time
from jnpr.toby.security.idp.idp_commands import get_idp_policy_commit_status


def install_idp_policy(device=None, node=None, timeout=600, validate=True):
    """
    To commit and install the IDP policy.
    Example:
        install_idp_policy(device=dh, node="local", timeout=300, validate=True)

    ROBOT Example:
        Install IDP Policy   device=${dh}   node=local   timeout=${300}   validate=${True}

    :param Device device:
        **REQUIRED** Device handle of the DUT
    :param str node:
        *OPTIONAL* Node on which to perform, in case of HA
    :param int timeout:
        *OPTIONAL* Time for which it waits for the IDP policy to load before it times out.
    :param bool validate:
        *OPTIONAL* Raises Exception in case of False
    :return: Dictionary with details
    :rtype: dict
    """
    if device is None:
        raise Exception("device is mandatory argument")

    if device.is_ha is False or node is not None:
        status = _install_idp_policy(device, node, timeout, validate)
        return status
    else:
        status1 = _install_idp_policy(device, "node0", timeout, validate)
        status2 = _install_idp_policy(device, "node1", timeout, validate)
        if status1 != status2:
            device.log(level="ERROR", message="IDP Policy installation status doesn't match on "
                                              "both nodes")
            if validate is True:
                raise Exception("IDP Policy installation status doesn't match on both nodes")
        return status1


def _install_idp_policy(device, node, timeout, validate):
    """
    Internal Function which is used by install_idp_policy()

    """
    sleep_time = 0
    commit_status = {}
    while sleep_time < timeout:
        commit_status = get_idp_policy_commit_status(device=device, node=node)
        status = commit_status.get('status')
        if status == 'error':
            device.log(level="ERROR", message="IDP Policy installation is failed : %s" \
                                              % commit_status.get('message'))
            if validate is True:
                raise Exception("IDP Policy installation is failed : %s" %
                                commit_status.get('message'))
            break
        elif status == 'nochange' or status == "success":
            device.log(level="INFO", message="IDP Policy installation is successful")
            break
        else:
            device.log(level="INFO", message="(%d/%d secs) Sleeping 30 seconds..." % (sleep_time,
                                                                                      timeout))
            time.sleep(30)
            sleep_time += 30
    if not (sleep_time < timeout):
        commit_status['status'] = 'error'
        commit_status['message'] = "IDP Security policy install timed out"
        device.log(level="ERROR", message="IDP Security policy install timed out. Waited for %d "
                                          "secs" % timeout)
        if validate is True:
            raise Exception("IDP Security policy install timed out. Waited for %d secs" % timeout)
    return commit_status