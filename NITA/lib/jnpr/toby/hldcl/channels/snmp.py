"""
Creating SNMP Channel
"""
from pysnmp.hlapi import (ContextData, nextCmd, getCmd, SnmpEngine, UdpTransportTarget, ObjectIdentity, \
                          ObjectType, CommunityData, UsmUserData, usmHMACSHAAuthProtocol, usm3DESEDEPrivProtocol)
import os
import time
import re
import random
from pysnmp.proto import api
from pyasn1.codec.ber import decoder
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
import threading
# from queue import *
from queue import Queue
import socket

# Global variable declaration
DEFAULT_MIBDIR = "http://mibs.snmplabs.com/asn1/@mib@"


class Snmp(object):
    """
    Class to create an object representing a SNMP channel to router.

    """
    def __init__(self, kwargs):
        snmp_channel_id = kwargs.get('channel_id', \
                                     str(os.getpid()) + \
                                     str(time.time()).split('.')[0] + \
                                     str(random.randint(0, 9)) \
                                     )
        self.snmpchannel = SnmpEngine(snmpEngineID=snmp_channel_id)
        self.timeout = kwargs.get('timeout', 60)
        self.mibs_dir = kwargs.get('MIBDIRS', DEFAULT_MIBDIR)
        self.mibs_custom_dir = kwargs.get('mibs_custom_dir', None)
        if self.mibs_custom_dir:
            t.log('mibs_custom_dir: '+self.mibs_custom_dir)
        self.community = kwargs.get('community', 'public')
        self.version = kwargs.get('version', 2)
        self.host = kwargs.get('host')
        # SNMP V3 settings
        self.group = kwargs.get('group')
        self.user = kwargs.get('user', 'test1')
        self.auth_type = kwargs.get('auth_type', 'usmHMACSHAAuthProtocol')
        self.auth_pass = kwargs.get('auth_pass', 'test1234')
        self.priv_type = kwargs.get('priv_type', 'usmAesCfb128Protocol')
        self.priv_pass = kwargs.get('priv_pass', 'test1234')
        self.context_engine = kwargs.get('context_engine', None)
        self.context_name = kwargs.get('context_name', '')

        self.port = kwargs.get('port', 161)
        self.transport = UdpTransportTarget((self.host, self.port))

        self.aindex = 1
        self.eindex = 8

        self.trap_port = kwargs.get('trap_port', self.get_free_port())
        self.trap_server_v4 = kwargs.get('trap_server_v4', 'localhost')
        self.trap_server_v6 = kwargs.get('trap_server_v6', '::1')

    def invoke(self, device_handle, command, *args, **kwargs):
        """
        Channel to invoke pysnmp commands
        :param device_handle: Device Handle
        :param command: pysnmp command to execute
        :param args: Arguments to send to pysnmp command
        :param kwargs: Keyword arguments to send to pysnmp command
        :return: Output of pysnmp command
        """
        t.log(level="DEBUG", message="Entering 'invoke'\n"+__file__)
        possibles = globals().copy()
        possibles.update(locals())
        cmd_to_run = possibles.get(command)
        device_handle.log("Running command %s" % command)
        if not cmd_to_run:
            t.log(level="DEBUG", message="Method "+command+" not implemented")
            raise NotImplementedError("Method %s not implemented" % command)
        return_value = cmd_to_run(*args, **kwargs)
        t.log(level="DEBUG", message="Exiting 'invoke' with return value/code :\n"+str(return_value))
        return return_value

    def create_object_identity(self, **kwargs):
        """
        :param
            oid: **REQUIRED** OID or MibSymbol
            value: **OPTION** value for snmp set
        :return: ObjectIdentity
        """
        t.log("DEBUG", "Entering 'create_object_identity'\n"+__file__)
        oid = kwargs.get('oid')
        value = kwargs.get('value')
        oidre = re.match(r'(.*)::(.*)\.(.*)', oid)
        mib_name = ''
        oid_name = ''
        if oidre:
            mib_name = oidre.group(1)
            oid_name = oidre.group(2)
            oid_index = oidre.group(3)
            object_identity = ObjectIdentity(
                mib_name, oid_name, oid_index).addAsn1MibSource(self.mibs_dir)
        else:
            oidre = re.match('(.*)::(.*)', oid)
            if oidre:
                mib_name = oidre.group(1)
                oid_name = oidre.group(2)
                object_identity = ObjectIdentity(mib_name, oid_name).addAsn1MibSource(self.mibs_dir)

        if re.match(r'^([0-9]*\.)*[0-9]*$', oid):
            object_identity = ObjectIdentity(oid).addAsn1MibSource(
                self.mibs_dir)
        elif re.match(r'^([a-z A-Z 0-9 \-]*\.)*[a-z A-Z 0-9 \-]*$', oid):
            from pysnmp.smi import builder, view
            mibbuilder = builder.MibBuilder()
            mibviewcontroller = view.MibViewController(mibbuilder)
            objectidentity1 = ObjectIdentity(oid)
            objectidentity1.resolveWithMib(mibviewcontroller)
            oid = '.'.join(map(str, objectidentity1.getOid().asTuple()))
            object_identity = ObjectIdentity(oid).addAsn1MibSource(
                self.mibs_dir)

        if self.mibs_custom_dir:
            t.log('DEBUG', "Created Object Identity with custom mib directory: "+self.mibs_custom_dir)
            object_identity = object_identity.addMibSource(self.mibs_custom_dir)
        if value:
            object_type = ObjectType(object_identity, value)
        else:
            object_type = ObjectType(object_identity)
        return object_type

    def get_snmp_id(self):
        """
        Method to retrieve channel ID of SNMP Object called upon
        :return: Channel ID
        """
        t.log("DEBUG", "Entering 'get_snmp_id'\n"+__file__)
        return_value = self.snmpchannel.snmpEngineID._value.decode('utf-8')
        t.log(level="DEBUG", message="Exiting 'get_snmp_id' with return value/code :\n"+str(return_value))
        return return_value

    def create_community_data(self, **kwargs):
        """
            :param version: SNMP Version. Default to 2
            :param user: UserID
            :param password: Password
            :return:
        """
        t.log("DEBUG", "Entering 'create_community_data'\n"+__file__)
        version = kwargs.get('version', self.version)
        user = kwargs.get('user', self.user)
        auth_type = kwargs.get('auth_type', self.auth_type)
        auth_pass = kwargs.get('auth_pass', self.auth_pass)
        priv_type = kwargs.get('priv_type', self.priv_type)
        priv_pass = kwargs.get('priv_pass', self.priv_pass)
        community = kwargs.get('community', self.community)

        valid_auth_type = ['usmHMACMD5AuthProtocol', 'usmHMACSHAAuthProtocol']
        valid_priv_type = ['usmDESPrivProtocol', 'usm3DESEDEPrivProtocol',
                           'usmAesCfb128Protocol', 'usmAesCfb192Protocol',
                           'usmAesCfb256Protocol']

        if version == 1:
            return_value = CommunityData(community, mpModel=0)
        elif version == 2:
            return_value = CommunityData(community)
        elif version == 3:
            if priv_type == 'usmNoPrivProtocol' and \
                    auth_pass in valid_auth_type:
                return_value = UsmUserData(user, auth_pass,\
                                   authProtocol=eval(auth_type))
            elif auth_type in valid_auth_type and priv_type in valid_priv_type:
                return_value = UsmUserData(user, auth_pass, priv_pass, \
                                   authProtocol=eval(auth_type),\
                                   privProtocol=eval(priv_type))
            else:
                return_value = UsmUserData(user)
        else:
            t.log(level="DEBUG", message="Invalid Version")
            raise Exception("Invalid Version")
        t.log(level="DEBUG", message="Exiting 'create_community_data' with return value/code :\n"+str(return_value))
        return return_value

    def start_trap(self, pattern_end_trap, time_end_trap,
                   timeout, port, queue):
        """
            :param pattern_end_trap
               **OPTION** the pattern you are looking for in the trap to
               stop trap. If not defined, trap will be stopped after
               timeout value
            :param time_end_trap
               **OPTION** the time for running trap. Default: 30
            :param timeout
               **OPTION** the timeout for snmp trap. Default: 300.
            :param port
               **OPTION** the port of snmp trap.
            :return:
        """
        t.log("DEBUG", "Entering 'start_trap'\n"+__file__)
        import warnings
        warnings.simplefilter("ignore", ResourceWarning)
        startedat = time.time()
        #global results
        global RESPONSE

        RESPONSE = ''

        def cbfun(transportdispatcher, transportdomain, transportaddress,
                  wholemsg):
            t.log("DEBUG", "Entering 'cbfun'\n"+__file__)
            #global results
            global RESPONSE
            while wholemsg:
                msgver = int(api.decodeMessageVersion(wholemsg))
                if msgver in api.protoModules:
                    pmod = api.protoModules[msgver]
                else:
                    RESPONSE += 'Unsupported SNMP version %s' % msgver
                    return
                reqmsg, wholemsg = decoder.decode(
                    wholemsg, asn1Spec=pmod.Message(),
                    )
                RESPONSE += 'Notification message from %s:%s: \n' % (
                    transportdomain, transportaddress
                    )
                reqpdu = pmod.apiMessage.getPDU(reqmsg)
                if msgver == api.protoVersion1:
                    varbinds = pmod.apiTrapPDU.getVarBindList(reqpdu)
                    RESPONSE += 'Var-binds: \n'
                    for oid, val in varbinds:
                        RESPONSE += '%s = %s \n' % (oid.prettyPrint(),
                                                    val.prettyPrint())
                        if pattern_end_trap and re.search(pattern_end_trap,
                                                          RESPONSE, re.I):
                            transportdispatcher.jobFinished(1)
                            RESPONSE += "Stopped trap \n"

                    RESPONSE += 'Enterprise: %s \n' % (
                        pmod.apiTrapPDU.getEnterprise(reqpdu).prettyPrint()
                        )

                    RESPONSE += 'Agent Address: %s \n' % (
                        pmod.apiTrapPDU.getAgentAddr(reqpdu).prettyPrint()
                        )
                    RESPONSE += 'Generic Trap: %s \n' % (
                        pmod.apiTrapPDU.getGenericTrap(
                            reqpdu).prettyPrint())

                    RESPONSE += 'Specific Trap: %s \n' % (
                        pmod.apiTrapPDU.getSpecificTrap(
                            reqpdu).prettyPrint()
                        )

                    RESPONSE += 'Uptime: %s \n' % (
                        pmod.apiTrapPDU.getTimeStamp(
                            reqpdu).prettyPrint()
                        )
                else:
                    varbinds = pmod.apiPDU.getVarBindList(reqpdu)

        def cbtimerfun(timenow):
            t.log("DEBUG", "Entering 'cbtimerfun'\n"+__file__)
            #global results
            global RESPONSE
            if time_end_trap is not None:
                if timenow - startedat >= time_end_trap:
                    transportdispatcher.jobFinished(1)
                    RESPONSE += "Stopped trap \n"

            if timenow - startedat >= timeout:
                t.log(level="DEBUG", message="Request timed out \n")
                raise Exception("Request timed out \n")

        transportdispatcher = AsynsockDispatcher()
        transportdispatcher.registerRecvCbFun(cbfun)
        transportdispatcher.registerTimerCbFun(cbtimerfun)
        # UDP/IPv4
        transportdispatcher.registerTransport(
            udp.domainName, udp.UdpSocketTransport().openServerMode(
                (self.trap_server_v4, port))
        )

        # UDP/IPv6
        transportdispatcher.registerTransport(
            udp6.domainName, udp6.Udp6SocketTransport().openServerMode(
                (self.trap_server_v6, port))
        )

        transportdispatcher.jobStarted(1)

        try:
            # Dispatcher will never finish as job#1 never reaches zero
            transportdispatcher.runDispatcher()
        except:
            transportdispatcher.closeDispatcher()

        queue.put(RESPONSE)
        t.log(level="DEBUG", message="Exiting 'start_trap' with return value/code :\n")
        return

    def get_trap_result(self, trigger, pattern_end_trap, time_end_trap,
                        timeout, port):
        t.log("DEBUG", "Entering 'get_trap_result'\n"+__file__)
        queue = Queue()
        thread1 = threading.Thread(target=self.start_trap, name="Thread1", \
                              args=[pattern_end_trap, time_end_trap, timeout, port, queue])
        thread2 = threading.Thread(target=trigger, name="Thread2")
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        return_value = queue.get()
        t.log(level="DEBUG", message="Exiting 'get_trap_result' with return value/code :\n"+str(return_value))
        return return_value

    def get_free_port(self):
        """
        Method to retrieve free port number on device
        :return: port
        """
        t.log("DEBUG", "Entering 'get_free_port'\n"+__file__)
        sock = socket.socket()
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        t.log(level="DEBUG", message="Exiting 'get_free_port' with return value/code :\n"+str(port))
        return port
