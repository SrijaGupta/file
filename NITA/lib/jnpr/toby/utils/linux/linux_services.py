"""
Linux service keywords
"""
#=========================================================================
#
#         FILE:  linux_services.py
#  DESCRIPTION:  Keywords to start,stop and check status of linux service
#       AUTHOR:  mqureshi / aishan
#      COMPANY:  Juniper Networks
#      VERSION:  1.0
#=========================================================================


import time
import re


def check_linux_running_service(device=None, service=None):
    """
    To check l7 service status
    Example -
     check_linux_running_service(device=linux, service=dovecot)
    ROBOT Example-
     check linux running service  device-${linux}  service=${dovecot}

    :param str device:
         **REQUIRED** Device handle for Linux host
    :param str service:
        **REQUIRED** L7 Service name
    :return: True if service is running
    :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")
    if service is None:
        device.log(level='ERROR', message="service argument is mandatory")
        raise ValueError("service argument is mandatory")

    response = device.shell(command="service %s status" % (service))
    if 'running' in response.response():
        return True
    elif 'unrecognized service' in response.response() or 'service could not be found' in response.response():
        device.log(level='ERROR', message='%s service is not installed' % (service))
        raise Exception("Service is not installed")
    elif 'is stopped' in response.response() or 'dead' in response.response():
        device.shell(command="service %s start" % (service))
        time.sleep(5)
        response = device.shell(command="service %s status" % (service))
        if 'running' in response.response():
            return True
        else:
            device.log(level='ERROR', message=" %s service is not running" % (service))
            raise Exception("Service is not running")
    else:
        device.log(level='ERROR', message="Unable to get service status")
        raise Exception("Unable to get service status")


def stop_services(device=None, service=None, dont_check=False):
    """
    To stop the given services on a Linux PC.
    Example:
        stop_services(service=['telnet'], device=dh)
        stop_services(service=['ftp', 'httpd'], device=dh, dont_check=True)

    ROBOT Example:
        Stop Services   service=${["telnet"]}   device=${dh}
        Stop Services   service=${["ftp", "httpd"]}   device=${dh}    dont_check=${True}

    :param Device device:
        **REQUIRED** The device handle of linux PC.
    :param list service:
        **REQUIRED** List of all the services need to be stopped on the PC.
    :param bool dont_check:
        *OPTIONAL* Pass True if dont care about if it running or not, or if its a valid service name
        or not. By default, it is False
    :return: True or False
    :rtype: bool
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")
    if service is None:
        device.log(level="ERROR", message="'service' is a mandatory argument")
        raise ValueError("'service' is a mandatory argument")

    dict_service_to_daemon = {'ftp': 'vsftpd', 'http': 'httpd', 'telnet': 'xinetd',
                              'snmp': 'snmpd', 'dhcp':'dhcpd', 'rsyslog':'rsyslog'}
    common_services = dict_service_to_daemon.keys()
    length_of_list = len(service)

    #If any service name is given, changing it to daemon name
    for i in range(0, length_of_list):
        if service[i] in common_services:
            service[i] = dict_service_to_daemon[service[i]]

    if dont_check is True:
        for service_name in service:
            device.shell(command="service " + service_name + " stop")
        return True

    init_status = device.shell(command="service --status-all").response()
    fail_flag = 0

    for serv in service:
        if re.match(".*" + serv + "[^\n]+is\\s*running.*", init_status, re.DOTALL):
            status = device.shell(command="service " + serv + " stop").response()
            if re.match(".*OK.*", status, re.DOTALL):
                device.log(level="INFO", message="Service " + serv + " successfully stopped")
            elif re.match(".*Redirecting to.*", status, re.DOTALL):
                status_centos_version7 = device.shell(command="service " + serv + " status" ).response()
                if re.match(".*inactive.*", status_centos_version7, re.DOTALL):
                   device.log(level="INFO", message="Service " + serv + " successfully stopped in Centos Latest")
                else:
                   device.log(level="ERROR", message="Service " + serv + " couldn't be stopped in Centos Latest")
            else:
                fail_flag = 1
                device.log(level="ERROR", message="Service " + serv + " couldn't be stopped")
        elif re.match(".*"+serv+".*", init_status, re.DOTALL):
            device.log(level="INFO", message="Service " + serv + " already NOT running")
        else:
            device.log(level="ERROR", message="" + serv + " : Invalid Service name")
            fail_flag = 1

    if fail_flag == 1:
        return False
    return True


def start_services(device=None, service=None, restart=False, dont_check=False):
    """
    To Start/Restart the given services on a Linux PC
    Example:
        start_services(device=dh, service=["vsftpd", "telnet"], dont_check=True)
        start_services(device=dh, service=["ftp", "httpd"], restart=True)

    ROBOT Example:
        Start Services   device=${dh}   service=${["vsftpd", "telnet"]}    dont_check=${True}
        Start Services   device=${dh}   service=${["ftp", "httpd"]}   restart=${True}

    :param Device device:
        **REQUIRED** The device handle of linux PC.
    :param list service:
        **REQUIRED** List of the services needed to be started/restarted
    :param bool restart:
        *OPTIONAL* To Restart the service instead of just Start the service
    :param bool dont_check:
        *OPTIONAL* Pass True if dont care about if it running or not, or if its a valid service name
        or not. By default, it is False
    :return: True or False
    :rtype: bool
    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if service is None:
        device.log(level="ERROR", message="'service' is a mandatory argument")
        raise ValueError("'service' is a mandatory argument")

    operation = "start"
    if restart is True:
        operation = "re" + operation

    dict_service_to_daemon = {'ftp': 'vsftpd', 'http': 'httpd', 'telnet': 'xinetd',
                              'snmp': 'snmpd', 'dhcp': 'dhcpd', 'rsyslog': 'rsyslog'}
    common_services = dict_service_to_daemon.keys()
    length_of_list = len(service)

    # If any service name is given, changing it to daemon name
    for i in range(0, length_of_list):
        if service[i] in common_services:
            service[i] = dict_service_to_daemon[service[i]]

    if dont_check is True:
        for service_name in service:
            device.shell(command="service " + service_name + " " + operation)
        return True

    init_status = device.shell(command="service --status-all").response()
    fail_flag = 0

    for serv in service:
        if operation == "restart":
            status = device.shell(command="service " + serv + " " + operation).response()
            if re.match(".*OK.*", status, re.DOTALL):
                device.log(level="INFO", message="Service " + serv + " successfully restarted")
            elif re.match(".*unrecognized service.*", status, re.DOTALL):
                device.log(level="ERROR", message="" + serv + " : Invalid Service name")
                fail_flag = 1
            elif re.match(".*Redirecting to.*", status, re.DOTALL):
                status_centos_version7 = device.shell(command="service " + serv + " status" ).response()
                if re.match(".*running.*", status_centos_version7, re.DOTALL):
                   device.log(level="INFO", message="Service " + serv + " successfully restarted in Centos Latest")
                else:
                   device.log(level="ERROR", message="Service " + serv + " couldn't be restarted in Centos Latest")
            else:
                device.log(level="ERROR", message="Service " + serv + " couldn't be restarted")
                fail_flag = 1

        else:
            if re.match(".*" + serv + "[^\n]+is\\s*running.*", init_status, re.DOTALL):
                device.log(level="INFO", message=serv + " is already running")
            else:
                status = device.shell(command="service " + serv + " " + operation).response()
                if re.match(".*OK.*", status, re.DOTALL):
                    device.log(level="INFO", message="Service " + serv + " successfully started")
                elif re.match(".*Redirecting to.*", status, re.DOTALL):
                	status_centos_version7 = device.shell(command="service " + serv + " status" ).response()
                	if re.match(".*running.*", status_centos_version7, re.DOTALL):
                   		device.log(level="INFO", message="Service " + serv + " successfully started in Centos Latest")
                	else:
                   		device.log(level="ERROR", message="Service " + serv + " couldn't be started in Centos Latest")                
                elif re.match(".*unrecognized service.*", status, re.DOTALL):
                    device.log(level="ERROR", message="" + serv + " : Invalid Service name")
                    fail_flag = 1
                else:
                    device.log(level="ERROR", message="Service " + serv + " couldn't be started")
                    fail_flag = 1

    if fail_flag == 1:
        return False
    return True



def get_pid(list_of_process_name=None, device=None):
    """
    To get corresponding Process IDs of the Process names on the Linux PC
    Example:
    get_pid(list_of_process_name=["tcpdump"], device=dh)
        get_pid(list_of_process_name=["tcpdump, "ping"], device=dh)

    ROBOT Example:
        Get Pid   list_of_process_name=@{["tcpdump, "ping"]}   device=${dh}

    :param list list_of_process_name:
        **REQUIRED** List of process names to be converted whose PIDs are required
    :param Device device:
        **REQUIRED** Device handle of the Linux PC.
    :return: A list of corresponding PIDs
    :rtype: list
    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if list_of_process_name is None:
        device.log(level="ERROR", message="process_name has to be passed")
        raise ValueError("process_name has to be passed")

    status = device.shell(command="ps -aux").response()

    pid_list = []
    for process in list_of_process_name:
        found_flag = 0
        for lines in status.splitlines():
            match = re.search("[a-z]+\\s+([0-9]+)\\s+[0-9]+\\.[0-9]\\s+[0-9]+\\.[0-9]\\s+[0-9]+\\s+[0-9]+.*\\s+.*\\s+.*\\s*[0-9]+:[0-9]+\\s+.*" + process + ".*", lines, re.DOTALL)
            if match:
                found_flag = 1
                pid_list.append(match.group(1))
        if found_flag == 0:
            device.log(level="INFO", message="Process " + process + " is already not running")

    return pid_list


def kill_process(device=None, pids=None, process_names=None):
    """
    To kill processes on a Linux PC
    Example:
        kill_process(device=dh, pids=[1842, 1833])
        kill_process(device=dh, pids=1841, process_names=["tcpdump", "ping"])
        kill_process(device=dh, process_names="tcpdump")

    ROBOT Example:
        Kill Process   device=${dh}   pids=${[1842, 1833]}
        Kill Process   device=${dh}   pids=${1841}   process_names=${["tcpdump", "ping"]}
        Kill Process   device=${dh}   process_names=tcpdump

    :param Device device:
        **REQUIRED** Device handle of the Linux PC
    :param int pids:
        *OPTIONAL* Process ID which user wants to kill. Can also be passed as a List
    :param str process_names:
        *OPTIONAL* Process Name which user wants to kill. Can also be passed as a List
    :return: None
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if pids is None and process_names is None:
        device.log(level="ERROR", message="Either pids or process_names has to be passed")
        raise ValueError("Either pids or process_names has to be passed")
    list_to_kill = []

    if process_names is not None:
        if isinstance(process_names, list):
            list_to_kill = get_pid(list_of_process_name=process_names, device=device)
        else:
            list_to_kill = get_pid(list_of_process_name=[process_names], device=device)

    if pids is not None:
        if isinstance(pids, list):
            list_to_kill = list_to_kill + pids
        else:
            list_to_kill.append(pids)

    for pid_to_kill in list_to_kill:
        device.shell(command="kill -9 " + str(pid_to_kill))

