#!/usr/local/bin/python3
"""
HUWAWEI DSLAM CONFIG AND VERIFICATION
"""

import telnetlib
import time
import re
import logging

__author__ = ['Sudarshan B']
__contact__ = 'sudarshanb@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

# Logging
formatter = "%(asctime)s:%(levelname)s:%(message)s"  # check for more in logging module
logging.basicConfig(format=formatter, datefmt="%b-%d-%Y %H:%M:%S")
logger = logging.getLogger(__name__)


def connect_dslam_con(dslam=None, dslam_con_port=None,
                      uname='root', password='mduadmin', prompt='MA5818'):
    """
    Subroutine Connects on to console of huwaei DSLAM and returns handler once in config mode
    :Example:
    python: connect_dslam_con(dslam='cnrd-ts58',dslam_con_port='7016',
                                uname ='root',password='mduadmin',prompt='MA5818')
    robot:  connect dslam con    dslam=cnrd-ts58    dslam_con_port=7016
                                uname =root    password=mduadmin    prompt= MA5818

    :param str dslam:
        **REQUIRED** console server name of dslam. Ex. dslam='cnrd-ts58'
    :param str dslam_con_port:
        **REQUIRED** console port number. Ex. dslam_con_port='7016'
    :param str uname:
        *OPTIONAL** user name login credential Ex. uname ='root'
    :param str password:
        *OPTIONAL** user password login credential Ex. password='mduadmin'
    :param str prompt:
        *OPTIONAL** Device prompt needed Ex. prompt='MA5818'
    :return:
        Dslam console device handler once devise is in config mode
    :raises Exception: when mandatory parameter is missing
    """
    if dslam is None:
        raise Exception("'dslam' console server name and it is a mandatory parameter ")

    elif dslam_con_port is None:
        raise Exception("'dslam_con_port' console server port \
                            number and it is a mandatory parameter ")
    cli_mode_prompt = prompt + '>'
    previlaged_mode_prompt = prompt + '#'
    config_mode_prompt = prompt + '(config)#'
    connection = telnetlib.Telnet(dslam, dslam_con_port, 10)
    time.sleep(5)
    connection.write(('\n').encode())
    login_done = False
    config_mode = False
    message = connection.read_very_eager()
    print(message.decode())
    if "invalid" in message.decode():
        connection.write('\n'.encode())
        logger.info(message.decode())

    if re.search("option", message.decode()):
        connection.write(("1").encode())
        time.sleep(5)
        connection.write('\n'.encode())
        message = connection.read_very_eager()
        logger.info(message.decode())
        connection.write(("\n").encode())

    message = connection.read_until(b'>>User name:', timeout=10)
    if '>>User password:' in message.decode():
        connection.write(("\n").encode())

    if '>>User name:' in message.decode():
        connection.write((uname + "\n").encode('UTF-8'))
        logger.info(message.decode() + uname)
        message = connection.read_until(b'>>User password:', timeout=10)
        if b'>>User password:' in message:
            connection.write((password + "\n").encode())
            logger.info(message.decode() + password)
            connection.write(("\n").encode())
            message = connection.read_until(cli_mode_prompt.encode(), timeout=20)
            if re.search(cli_mode_prompt, message.decode()):
                logger.info("login successful")
                logger.info(message.decode())
                connection.write(b'\n')
                connection.write(("enable" + "\n").encode())
                time.sleep(10)
                connection.write(("\n").encode())
                message = connection.read_very_eager()
                time.sleep(10)
                if previlaged_mode_prompt in message.decode():
                    logger.info("privilaged mode logged in")
                    login_done = True
                    config_mode = False

    if cli_mode_prompt in message.decode():
        logger.info("already login successful")
        login_done = True
        connection.write('en\n'.encode())
        message = connection.read_eager()
        if previlaged_mode_prompt in message.decode():
            logger.info("privilaged user mode logged in")
            login_done = True
            config_mode = False
    if previlaged_mode_prompt in message.decode():
        logger.info("already login successful in privilaged user mode ")
        login_done = True
        config_mode = False

    if config_mode_prompt in message.decode():
        login_done = True
        config_mode = True

    if config_mode is True:
        connection.write(("quit\n").encode())
        config_mode = False

    if login_done is True and config_mode is False:
        connection.write(("display current-configuration | include 'service-port 7'\n\n").encode())
        time.sleep(10)
        message = connection.read_very_eager()
        logger.info(message.decode())
        connection.write(("config" + "\n").encode())
        time.sleep(5)
        message = connection.read_very_eager()
        logger.info(message.decode())

    if re.search("config", message.decode()):
        print("we are in config mode")
        connection.write(("idle-timeout  255\n").encode())
        return connection

def configure_lfm_on_dslam(connection= None, dslam_port=None, command=None, vlan='300'):
    """Subroutine Configured requied commands on huwaei DSLAM and retuns True after execution
    :Example:
    python: Configure_lfm_on_dslam(connection=None,dslam_port=None,command=None)
    robot:  connect dslam con    dslam=cnrd-ts58
                dslam_con_port=7016    uname =root    password=mduadmin    prompt= MA5818
    :param Device connection:
        **REQUIRED** Device handler.
    :param str dslam_port:
        *optional* Port on which configs have to be executed. Ex. dslam_port='0/1/7'
    :param str command:
            **REQUIRED** Commands to be executed on DSLAM after loging in
            Following are the commands list
            enable_efm_active : Command sets oam efm ie LFM peer in active mode
            enable_efm_passive : Command sets oam efm ie LFM peer in passive mode
            disable_efm : disables LFM peer
            config_port_untag : configures supplied port in untagged mode
            config_port_tag : configures supplied dslam port in tagged mode
            invoke_loopback_forward : invokes lfm loopback forwarding mode
            invoke_loopback_drop : invokes lfm loopback in drop mode
            reset_stat : reset port statistics for clear measurement
            reset_dslam : reset dslam with vlan 1 for other tests to work gracefully
    :param str vlan:
            **OPTIONAL* only for executing config_port_untag and config_port_tag its compulsion
    :return true once completed
    """
    srv_port = dslam_port.split('/')
    if connection is None:
        raise Exception("'connection' is a device handle and it is a mandatory parameter ")
    if command is None:
        raise Exception("'command' is mandatory parameter ")
    logger.info("command is " + command)
    if command == 'enable_efm_active':
        connection.write(("efm oam " + dslam_port + " disable\n").encode())
        time.sleep(5)
        message = connection.read_very_eager()
        logger.info(message.decode())
        connection.write(("efm oam mode " + dslam_port + " active\n").encode())
        time.sleep(5)
        message = connection.read_very_eager()
        logger.info(message.decode())
        connection.write(("efm oam " + dslam_port + " enable\n").encode())
        time.sleep(5)
        message = connection.read_very_eager()
        logger.info(message.decode())
    if command == 'enable_efm_passive':
        connection.write(("efm oam " + dslam_port + " disable\n").encode())
        time.sleep(5)
        message = connection.read_very_eager()
        logger.info(message.decode())
        connection.write(("efm oam mode " + dslam_port + " passive\n").encode())
        time.sleep(5)
        message = connection.read_very_eager()
        logger.info(message.decode())
        connection.write(("efm oam " + dslam_port + " enable\n").encode())
        time.sleep(5)
        message = connection.read_very_eager()
        logger.info(message.decode())
    if command == 'disable_efm':
        connection.write(("efm oam " + dslam_port + " disable\n").encode())
        time.sleep(5)
        message = connection.read_very_eager()
        logger.info(message.decode())
    if command == 'config_port_untag':
        srv_port = dslam_port.split('/')
        connection.write(("undo service-port " + srv_port[2] + "\n").encode())
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("undo vlan " + vlan).encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("undo vlan attrib " + vlan).encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("vlan " + vlan + " smart").encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("service-port " + srv_port[2] + " vlan " + vlan + " vdsl mode ptm "
                      + dslam_port + " multi-service user-vlan untagged tag-transform add-double "
                                     "inner-vlan 1 inner-priority 0\n").encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("vlan bind service-profile " + vlan + " profile-id 6").encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
    if command == 'config_port_tag':
        connection.write(("undo service-port " + srv_port[2] + "\n").encode())
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("vlan " + vlan + " smart").encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("vlan attrib " + vlan + " q-in-q").encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("port vlan " + vlan + " 0/0 0").encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("vlan bind service-profile " + vlan + " profile-id 6").encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("service-port " + srv_port[2] + " vlan " + vlan + " vdsl mode ptm "
                          +dslam_port+" multi-service user-vlan "
                          +vlan+" tag-transform default\n").encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
    if command == 'invoke_loopback_forward':
        connection.write(("efm loopback " + dslam_port + " start recv-forward\n").encode())
        time.sleep(2)
        message = connection.read_very_eager()
        logger.info(message.decode())
        if "Are you sure  to start" in message.decode():
            time.sleep(2)
            connection.write(("yes\n").encode())
            message = connection.read_very_eager()
            logger.info(message.decode())
    if command == 'stop_loopback':
        connection.write(("efm loopback " + dslam_port + " stop").encode())
        connection.write(("\n").encode())
        connection.write(("efm loopback " + dslam_port + " stop").encode())
        connection.write(("\n").encode())
        time.sleep(2)
        message = connection.read_very_eager()
        logger.info(message.decode())
        connection.write(("\n").encode())
    if command == 'invoke_loopback_drop':
        connection.write(("efm loopback " + dslam_port + " start\n").encode())
        time.sleep(2)
        message = connection.read_very_eager()
        if "timeout" in message.decode():
            connection.write(("\n").encode())
        logger.info(message.decode())
        time.sleep(2)
        message = connection.read_very_eager()
        logger.info(message.decode())
        if "Are you sure" in message.decode():
            connection.write(("yes\n").encode())
            time.sleep(2)
            message = connection.read_very_eager()
            logger.info(message.decode())
    if command == 'reset_stat':
        serv_port = re.split('/', dslam_port)
        connection.write(("reset statistics service-port " + serv_port[2] + "\n").encode())
        message = connection.read_very_eager()
        logger.info(message.decode())
    if command == 'reset_dslam':
        srv_port = dslam_port.split('/')
        connection.write(("undo service-port " + srv_port[2] + "\n").encode())
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        connection.write(("undo vlan bind service-profile " + vlan).encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        time.sleep(2)
        connection.write((" service-port " + srv_port[2] + " vlan 1 vdsl mode ptm "
                          + dslam_port + " tag-transform default inbound traffic-table index 6 "
                                         "outbound traffic-table index 6\n").encode())
        time.sleep(10)
        message = connection.read_very_eager()
        connection.write(("\n").encode())
        logger.info(message.decode())
        time.sleep(2)
    return 1


def check_loop_back(connection=None, dslam_port=None, packet_count=None):
    """Subroutine check the traffic statistics post loopback
    :Example:
    python: check_loop_back(connection=None,dslam_port=None,packet_count=None)
    robot:  check loop back    connection=${device}    dslam_port='0/1/7'    packet_count=${10}
    :param Device connection:
        **REQUIRED** Device handler.
    :param str dslam_port:
        **REQUIRED** Port on which configs have to be executed. Ex. dslam_port='0/1/7'
    :param int packet_count:
        **REQUIRED** packets actually pushed into dslam
    :return true once completed
    """
    if connection is None:
        raise Exception("'connection' is a device handle and it is a mandatory parameter ")
    if dslam_port is None:
        raise Exception("'dslam_port' is a mandatory parameter to check statistics")
    if packet_count is None:
        raise Exception("'packet_count' is a mandatory parameter for validation")
    serv_port = dslam_port.split('/')
    connection.write(("\n").encode())
    message = connection.read_very_eager()
    logger.info(message.decode())
    time.sleep(2)
    connection.write(("display statistics service-port " + serv_port[2] + "\n").encode())
    time.sleep(2)
    message = connection.read_very_eager()
    logger.info(message.decode())
    temp = message.decode()
    count = re.split(r'\n', temp)
    pattern = re.split(r':', count[4])
    observed_uplink_packets = int(pattern[1].strip())
    logger.info(type(pattern[1]))
    logger.info(pattern)
    logger.info(pattern[1])
    logger.info(count)
    pattern2 = re.split(r':', count[7])
    observed_downstream_packets = int(pattern2[1].strip())
    expected_max = observed_downstream_packets + 5  # exception due to keepalives exchanges
    if (observed_uplink_packets >= packet_count) and (observed_uplink_packets <= expected_max):
        logger.info("packets are looped back as expected")
    else:
        raise Exception("packets are not getting looped back")
    return True