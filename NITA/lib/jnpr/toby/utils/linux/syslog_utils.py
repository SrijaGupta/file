"""
Syslog related Keywords
"""
import re


def check_syslog(device=None, pattern=None, syslog_src_ip=None, count=None, case_insensitive=False,
                 file="/var/log/messages", negate=False):
    """
    To check if the pattern exists or not in the syslog server log file.
    Example:
        check_syslog(device=dh, pattern="repeat=10", negate=True,
                        syslog_src_ip="3.0.0.1")
        check_syslog(device=dh, pattern="action=DROP", count=3, case_insensitive=True,
                        syslog_src_ip="3.0.0.1")

    ROBOT Example:
        check Syslog   device=${dh}   pattern=${"action=DROP"}   negate=${True}
                          syslog_src_ip=3.0.0.1
        Check Syslog   device=${dh}   pattern=${"repeat=10"}   count=${3}
                          case_insensitive=${True}   syslog_src_ip=3.0.0.1
    :param Device device:
        **REQUIRED** Device Handle of the DUT. Linux and Junos, both work.
    :param str pattern:
        **REQUIRED** The attack pattern which needs to be matched.
    :param str syslog_src_ip:
        *OPTIONAL* IP from where Syslog is generated.
    :param int count:
        *OPTIONAL* No. of times string has to be matched.
    :param bool case_insensitive:
        *OPTIONAL* Search the pattern with case insensitive option. Default value is False
        (case sensitive).
    :param bool negate:
        *OPTIONAL* To verify the absence of the string. By default value is False.
    :param str file:
        *OPTIONAL* To provide the complete path of the log file. By default it
        is "/var/log/messages".
    :return: Boolean (True or False)
    :rtype: bool
    """

    if device is None:
        raise ValueError("Mandatory argument: 'device' need to be passed")
    if pattern is None:
        device.log(level="ERROR", message="Mandatory argument: 'pattern' need to be passed")
        raise ValueError("Mandatory argument: 'pattern' need to be passed")

    cmd = "cat " + file
    if syslog_src_ip is not None:
        cmd = cmd + " | egrep " + syslog_src_ip

    # Printing the complete syslog output
    device.shell(command=cmd)
    device.shell(command=cmd + " > /tmp/check-syslog.txt")

    grep_command = "grep -E "
    if case_insensitive is True:
        grep_command = grep_command + "-i "

    response = device.shell(command="cat /tmp/check-syslog.txt | " + grep_command + "'" + pattern +
                            "' | wc -l").response()
    match = re.search(".*([0-9]+).*", response, re.DOTALL)
    word_count = match.group(1)

    if negate is True:
        if int(word_count) >= 1:
            device.log(level="ERROR", message="String *" + pattern + "* is found " +
                       word_count + " no of times, Expected : 0 times")
            device.shell(command="rm -rf /tmp/check-syslog.txt")
            raise Exception("String *" + pattern + "* is found " + word_count + " no of "
                            "times, Expected : 0 times")
        else:
            device.log(level="INFO", message="String *" + pattern + "* is found " +
                       word_count + " no of times, Expected : 0 times")
    else:
        if count is None:
            if int(word_count) >= 1:
                device.log(level="INFO", message="String *" + pattern + "* is found " +
                           word_count + " no of times, Expected : 1 or more  times")
            else:
                device.log(level="ERROR", message="String is found 0 times, Expected : 1 "
                           "or more times ")
                device.shell(command="rm -rf /tmp/check-syslog.txt")
                raise Exception("String is found 0 times, Expected : 1 or more times")

        else:
            if int(word_count) == count:
                device.log(level="INFO", message="String *" + pattern + "* is found " +
                           word_count + " times, Expected : " + str(count) + " times")
            else:
                device.log(level="ERROR", message="String *" + pattern + "* is found " +
                           word_count + " times, Expected:" + str(count) + " times")
                device.shell(command="rm -rf /tmp/check-syslog.txt")
                raise Exception("String *" + pattern + "* is found " + word_count + " times,"
                                " Expected : " + str(count) + " times")

    device.shell(command="rm -rf /tmp/check-syslog.txt")
    return True


def configure_syslogd(device=None):
    """
    It configures the syslog and restarts it.
    Example:
        configure_syslogd(device=dh)

    ROBOT Example:
        Configure Syslogd   device=${dh}

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :return: Boolean (True or False)
    :rtype: bool
    """
    if device is None:
        raise ValueError("Mandatory argument: 'device' need to be passed")
    service = "syslog"
    response = device.shell(command="rpm -qa | grep rsyslog")

    # configuring Syslog or rSyslog, depending on the repsonse
    if re.match(".*rsyslog.*", response.response(), re.DOTALL):
        service = "rsyslog"
        device.shell(
            command='sed -i -r -e s/SYSLOGD_OPTIONS\\=\\".*?\\"'
                    '/SYSLOGD_OPTIONS\\=\\"\\ -c\\ 5\\ \\-x\\"/ /etc/sysconfig/rsyslog')
    else:
        device.shell(
            command='sed -i -r -e s/SYSLOGD_OPTIONS\\=\\".*?\\"'
                    '/SYSLOGD_OPTIONS\\=\\"\\-m\\ 0\\ \\-r\\ \\-x\\"/ /etc/sysconfig/syslog')

    # Stops and starts the server back
    device.shell(command="service " + service + " restart")
    status = device.shell(command="service " + service + " status").response()

    if re.match(".*is\s+running.*", status, re.DOTALL):
        device.log(level="INFO", message="Syslogd is up and running")
        return True
    else:
        device.log(level="ERROR", message="Syslogd couldn't start back")
        raise Exception("Syslogd couldn't start back")


def clear_syslog(device=None, file="/var/log/messages", restart_server=True):
    """
    To clear PC syslog server. Stops the server, delete the log file and start the syslog
    server back.
    Example:
        clear_syslog(device=dh)
        clear_syslog(device=dh, file="/var/tmp/abc.txt")
        clear_syslog(device=dh, restart_server=False)

    ROBOT Example:
        Clear syslog   device=${dh}
        Clear syslog   device=${dh}   file=${"/var/tmp/abc.txt"}
        Clear syslog   device=${dh}   restart_server=${False}

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str file:
        *OPTIONAL* To provide the complete path of the log file. By default it
        is "/var/log/messages".
    :param bool restart_server:
        *OPTIONAL* Pass True if you want to restart the server also while clearing the syslog. Else,
        pass False just to clear the syslog.
    :return: Boolean (True or False)
    :rtype: bool
    """
    if device is None:
        raise ValueError("Mandatory argument: 'device' need to be passed")

    if restart_server is False:
        device.shell(command="echo > " + file)
        return True

    service = "syslog"
    response = device.shell(command="rpm -qa | grep rsyslog")

    # Finding whether 'syslog' is applicable or 'rsyslog'
    if re.match(".*rsyslog.*", response.response(), re.DOTALL):
        service = "rsyslog"

    device.shell(command="service " + service + " stop")
    device.shell(command="rm -f " + file)
    device.shell(command="service " + service + " start")

    status = device.shell(command="service " + service + " status").response()
    centos_version = device.shell(command="cat /etc/redhat-release").response()

    # pattern in case of Centos 6.5 n before
    pattern = ".*is\s+running.*"

    if "release 7.6" in centos_version:
        pattern = ".*active\s*\(running\)"

    if re.match(pattern, status, re.DOTALL):
        device.log(level="INFO", message="Syslogd is up and running")
        return True
    else:
        device.log(level="ERROR", message="Syslogd couldn't start back")
        raise Exception("Syslogd couldn't start back")
