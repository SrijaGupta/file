#!/usr/bin/python3
"""
  DESCRIPTION:  L4_session tool specific APIs on Linux to create
                sessions (TCP or UDP) and send data.
       AUTHOR:  Suchi Pallai / Ishan Arora
      COMPANY:  Juniper Networks
      VERSION:  1.0
"""


class L4_Session():
    """
    Class for L4_session tool specific APIs
    """

    def __init__(self, unix):
        """
        Base class for L4_Session Module
        :param UnixHost unix:
         **REQUIRED** Device Object
        """
        self.dh = unix
        self.sessionid = 0
        self.pktSent = 0
        
        #Copying the tools to the host as soon as we create the Object
        program_dir = "/volume/labtools/lib/Testsuites/SRX/IPS/programs/"
        self.dh.shell(command="killall l4_session")
        unix.upload(local_file=program_dir + "l4_session", remote_file="/tmp/l4_session")
        unix.upload(local_file=program_dir + "send_to_l4_session",
                         remote_file="/tmp/send_to_l4_session")
        self.dh.shell(command="chmod 755 /tmp/l4_session")
        self.dh.shell(command="chmod 755 /tmp/send_to_l4_session")



    def check_status(self, state="presence", protocol="udp", sessid=0):
        """
        Check the L4_session program status.
        Example:
            check_status()
            check_status(state="absence", protocol="tcp", sessid=1)

        :param str state:
            *OPTIONAL* Expected State of the program.
            ``Supported values``: "presence" and "absence"
            ``Default value``   : "presence"
        :param str protocol:
            *OPTIONAL* Name of protocol.
            ``Supported values``: "tcp" and "udp"
        :param int sessid:
            *OPTIONAL* Traffic ID. By default last value used to run the l4_session program will
            be taken.
        :return: Returns True if found what is expected.
        :rtype: bool
        """
        if sessid == 0:
            sessid = self.sessionid

        port = 1025 + sessid
        cmd = "netstat -ln%s | grep %d" % (protocol[0], port)
        response = self.dh.shell(command=cmd)

        if state == "presence":
            if str(port) in response.response():
                self.dh.log(level="INFO", message="L4_Session utility is running. Presence is found"
                                                  "in the output")
            else:
                self.dh.log(level="ERROR", message="L4_Session utility is not running. Presence is "
                                                   "not found in the output")
                raise Exception("L4_Session utility is not running.Presence is not found in output")
        elif state == "absence":
            if str(port) in response.response():
                self.dh.log(level="ERROR", message="L4_Session utility is running. Absence is not "
                                                   "found in the output")
                raise Exception("L4_Session utility is not running. Absence is not found in output")
            else:
                self.dh.log(level="INFO", message="L4_Session utility is running. Absence is "
                                                  "found in the output")
        else:
            raise ValueError(
                'Unsupported value for STATE. Supported values are "presence" or "absence"')
        return True


    def check_data_received(self, state="received", pktrec=0, sessid=0):
        """
        Checks the sent packets are received or not
        Example:
            check_data_received(pktrec=1)
            check_data_received(pktrec=1, state="dropped", sessid=)

        :param str state:
            *OPTIONAL* Expected State of packet received.
            ``Supported values``: "received" and "dropped"
            ``Default value``   : "received"
        :param int pktrec:
            *OPTIONAL* No of packets received by the host
        :param int sessid:
            *OPTIONAL* Traffic ID. By default last value used to run the l4_session program
            will be taken.
        :return: Returns True if found what is expected.
        :rtype: bool
        """

        if sessid == 0:
            sessid = self.sessionid

        if pktrec == 0:
            pktrec = self.pktSent

        cmd = 'grep -c \"%d : Received\" /tmp/l4_session-%d.log' % (pktrec, sessid)
        response = self.dh.shell(command=cmd)

        if state == "received":
            if "1" in response.response():
                self.dh.log(level="INFO", message="Packet Received")
            else:
                self.dh.log(level="ERROR", message="Packet not Received")
                raise Exception("Packet not Received")
        elif state == "dropped":
            if "0" in response.response():
                self.dh.log(level="INFO", message="Packet not received, Expected for drop")
            else:
                self.dh.log(level="ERROR", message="Packet received, not Expected for drop")
                raise Exception("Packet received, not Expected for drop")
        else:
            raise ValueError(
                'Unsupported values for STATE. Supported values are "received" or "dropped"')
        return True


    def start(self, mode=None, server_ip=None, server_port=0, client_ip=None, **kwargs):
        """
        To start the Server or Client for the connection using l4_session program
        Example:
            start(mode='server', server_ip="5.0.0.1", protocol="tcp", server_port=21)
            start(mode='client', server_ip="5.0.0.1", protocol="tcp", server_port=21,
                  client_ip="4.0.0.1")

        :param str mode:
            **REQUIRED** The mode in which the l4_session program is to be run. Supported values are
            client and server
        :param str server_ip:
            **REQUIRED** Server IP to listen in server mode OR Server IP to connect in Client mode.
        :param int server_port:
            **REQUIRED**  Server port to listen for connections in server mode OR Server port to
            connect on client mode
        :param str client_ip:
            *OPTIONAL*  Client IP to make the connection
        :param int client_port:
            *OPTIONAL*  Client port to make the connection. Default is 0, where random port used
            as client port
        :param str protocol:
            *OPTIONAL*  TCP or UDP connection
        :param int sessid:
            *OPTIONAL*  Session id to differentiate between multiple sessions. If not provided,
            internally calculated.
        :param path:
            *OPTIONAL* Path of the tool to run. Default path is /tmp.
        :return: Returns the session id, if session id 0 indicates failure to start
        :rtype: int
        """
        if server_ip is None or server_port == 0:
            raise ValueError("server_ip and server_port are mandatory arguments")

        path = kwargs.get('path', "tmp")
        sessid = kwargs.get('sessid', 0)
        protocol = kwargs.get('protocol', "tcp")
        client_port = kwargs.get('client_port', 0)

        if self.sessionid == 0:
            self.dh.shell(command="killall l4_session")
            self.dh.shell(command="rm -f /tmp/l4_session-" +
                          str(self.sessionid) + ".log")
        self.sessionid += 1
        if sessid == 0:
            sessid = self.sessionid

        if mode == "server":
            cmd = "/%s/l4_session -server %d -ip %s -%s -id %d" % (
                path, server_port, server_ip, protocol, sessid)
            response = self.dh.shell(command=cmd)
            if "Cannot start session" in response.response() or "Cannot bind" \
                    in response.response():
                sessid = 0
                self.dh.log(level="ERROR", message="Starting the server failed...")
                if protocol == "tcp":
                    self.dh.shell(command="netstat -lntp")
                else:
                    self.dh.shell(command="netstat -lnup")
        elif mode == "client":
            if client_ip is None:
                cmd = "/%s/l4_session -client %s %d -port %d -%s -id %d" % (
                    path, server_ip, server_port, client_port, protocol, sessid)
            else:
                cmd = "/%s/l4_session -client %s %d -ip %s -port %d -%s -id %d" % (
                    path, server_ip, server_port, client_ip, client_port, protocol, sessid)
            response = self.dh.shell(command=cmd)
            if "Cannot start session" in response.response():
                sessid = 0
                self.dh.log(level="ERROR", message="Starting the client failed...")
        else:
            raise ValueError(
                "Unsupported value for mode. Supported values are client and server")
        return sessid


    def send_data(self, data=None, sessid=0, ipv6=False, hex_format=False, **kwargs):
        """
        Used to send packet once the session is established by the start().
        Example:
            send_data(data="USER testing", sessid=1)
            send_data(data="99 18 07 09 02 00 05 00", hex_format=True, sessid=11)
            send_data(data="331 Password required for user", ipv6=True, sessid=1)

        :param str data:
            **REQUIRED** Data which has to be sent over the established session
        :param int sessid:
            *OPTIONAL*  Session id to differentiate between multiple sessions. If not provided,
            internally calculated.
        :param bool ipv6:
            *OPTIONAL* used for ipv6 based traffic.
        :param bool hex_format:
            *OPTIONAL* data in hex format
        :param str path:
            *OPTIONAL* Path of the tool to run. Default path is /tmp.
        """
        if data is None:
            raise ValueError("data is a mandatory argument")

        if sessid == 0:
            sessid = self.sessionid
        if hex_format:
            hex_format = "-h"
        else:
            hex_format = ""
        if ipv6:
            ipv6 = "-ipv6"
        else:
            ipv6 = ""

        path = kwargs.get('path', "tmp")

        if hex_format:
            cmd = "/%s/send_to_l4_session %s -id %d %s \"%s\"" % (path, ipv6, sessid, hex_format,
                                                                 data)
        else:
            cmd = "/%s/send_to_l4_session %s -id %d %s %s" % (path, ipv6, sessid, hex_format, data)
        self.dh.shell(command=cmd)
        self.pktSent += 1


    def close(self, ipv6=False, sessid=0, path="tmp"):
        """
        It'll close the sessions if any and then it'll kill the l4_session program.
        Example:
            close()
            close(sessid=1)

        :param int sessid:
            *OPTIONAL*  Session id to differentiate between multiple sessions. If not provided,
            internally calculated.
        :param str path:
            *OPTIONAL* Path of the tool to run. Default path is /tmp.
        """
        if sessid == 0:
            sessid = self.sessionid
        if ipv6:
            ipv6 = "-ipv6"
        else:
            ipv6 = ""

        if sessid:
            cmd = "/%s/send_to_l4_session %s CMD -h 00 -id %d" % (path, ipv6, sessid)
            self.dh.shell(command=cmd)
        else:
            cmd = "/%s/send_to_l4_session %s CMD -h 00 -id %d" % (path, ipv6, sessid)
            self.dh.shell(command=cmd)
            self.dh.shell(command="killall l4_session")



##############################################################
# Below are the keywords which can be used in ROBOT directly #
##############################################################



def create_l4_session_object(device_handle=None):
    """
    Creates a wrapper around A linux handle with L4_Session class.
    Example:
    create_l4_session_object(device_handle=dh)

    ROBOT Example:
    Create L4 Session Object   device_handle=${dh}

    :param device_handle
        **REQUIRED** The device handle of Linux PC
    :return:
    """
    return L4_Session(device_handle)


##########################################################################
# For all the successive keywords, NEED to have L4_Session object which #
#    we can get from the above  keyword "create_l4_session_object()"    #
##########################################################################


def check_l4_session_status(l4_session_object=None, *args, **kwargs):
    """
        Check the l4_session program status.
        Example:
            check_l4_session_status(l4_session_object=dh)
            check_l4_session_status(l4_session_object=dh, state="absence", protocol="tcp", sessid=1)

        ROBOT Example:
            Check L4 session status   l4_session_object=${dh}    state=absence   protocol=tcp
                                      sessid=${1}

        :param L4_Session l4_session_object:
            **REQUIRED** The device handle of Linux PC wrapped with L4_Session class
            How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create L4 session object    device_handle=${dh}        (ROBOT)
        :param str state:
            *OPTIONAL* Expected State of l4_session program.
            ``Supported values``: "presence" and "absence"
            ``Default value``   : "presence"
        :param str protocol:
            *OPTIONAL* Name of protocol.
            ``Supported values``: "udp" and "tcp"
        :param int sessid:
            *OPTIONAL* Traffic ID. By default last value used to run the l4_session program will
            be taken.
        :return: Returns True if found what is expected.
        :rtype: bool
    """
    return l4_session_object.check_status(*args, **kwargs)


def check_l4_session_packet_received(l4_session_object=None, *args, **kwargs):
    """
        Checks the sent packets are received or not
        Example:
            check_l4_session_packet_received(l4_session_object=dh, pkt_rec=1)
            check_l4_session_packet_received(l4_session_object=dh, pktrec=1, state="dropped",
                                             sessid=2 )

        ROBOT Example
            Check L4 session packet received   l4_session_object=${dh}   pktrec=${1}   state=dropped
                                               sessid=${2}

        :param L4_Session l4_session_object:
            **REQUIRED** The device handle of Linux PC wrapped with L4_Session class
            How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create L4 session object    device_handle=${dh}        (ROBOT)
        :param str state:
            *OPTIONAL* Expected State of packet received.
            ``Supported values``: "received" and "dropped"
            ``Default value``   : "received"
        :param int pktrec:
            *OPTIONAL* No of packets received by the host
        :param int sessid:
            *OPTIONAL* Traffic ID. By default last value used to run the l4_session program
            will be taken.
        :return: Returns True if found what is expected.
        :rtype: bool
    """
    return l4_session_object.check_data_received(*args, **kwargs)


def l4_session_send_data(l4_session_object=None, *args, **kwargs):
    """
        Used to send packet once the session is established by the start_pkt.
        Example:
            l4_session_send_data(l4_session_object=dh, data="USER testing", sessid=1)
            l4_session_send_data(l4_session_object=dh, data="99 18 07 09 02 00 05 00",
                                 hex_format=True, sessid=11)
            l4_session_send_data(l4_session_object=dh, data="331 Password required for user",
                                 ipv6=True, sessid=1)

        ROBOT Example:
            l4 session send data   l4_session_object=${dh}   data=${"USER testing"}   sessid=${1}

        :param L4_Session l4_session_object:
           **REQUIRED** The device handle of linux PC wrapped with L4_Session class
           How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create L4 session object    device_handle=${dh}        (ROBOT)
        :param str data:
            **REQUIRED** Data which has to be sent over the established session
        :param int sessid:
            *OPTIONAL*  Session id to differentiate between multiple sessions. If not provided,
            internally calculated.
        :param bool ipv6:
            *OPTIONAL* Used for ipv6 based traffic.
        :param bool hex_format:
            *OPTIONAL* Data in hex format
        :param str path:
            *OPTIONAL* Path of the tool to run. Default path is /tmp.
    """
    return l4_session_object.send_data(*args, **kwargs)


def l4_session_start(l4_session_object=None, *args, **kwargs):
    """
        To start the Server or Client for the connection using l4_session program
        Example:
            l4_session_start(l4_session_object=dh, mode='server', server_ip="5.0.0.1",
                             protocol="tcp", server_port=21)
            l4_session_start(l4_session_object=dh, mode='client', server_ip="5.0.0.1",
                             protocol="tcp", server_port=21, client_ip="4.0.0.1")

        ROBOT Example:
            L4 Session Start   l4_session_object=${dh}   mode=client   server_ip=5.0.0.1
                               protocol=tcp   server_port=${80}   client_ip=4.0.0.1

        :param L4_Session l4_session_object:
            **REQUIRED** The device handle of linux PC wrapped with L4_Session class
            How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create packet send object    device_handle=${dh}        (ROBOT)
        :param str mode:
            **REQUIRED** The mode the l4_session program to run.
            ``Supported values``: "server" and "client"
        :param str server_ip:
            **REQUIRED** Server IP to listen in server mode. Server IP to connect in Client mode.
        :param int server_port:
            **REQUIRED**  Server port to listen for connections in server mode. Server port to
            connect on client mode
        :param str client_ip:
            *OPTIONAL*  Client IP to make the connection
        :param int client_port:
            *OPTIONAL*  Client port to make the connection. Default is 0, where random port used
            as client port
        :param str protocol:
            *OPTIONAL*  TCP or UDP connection.
            ``Supported values``: "udp" and "tcp"
        :param int sessid:
            *OPTIONAL*  Session id to differentiate between multiple sessions. If not provided,
            internally calculated.
        :param str path:
            *OPTIONAL* Path of the tool to run. Default path is /tmp.
        :return: Returns the session id, if session id 0 indicates failure to start
        :rtype: int
    """
    return l4_session_object.start(*args, **kwargs)


def l4_session_close(l4_session_object=None, *args, **kwargs):
    """
        It'll close the sessions if any and then it'll kill the l4_session program.
        Example:
            l4_session_close(l4_session_object=dh)
            l4_session_close(l4_session_object=dh, sessid=1)

        ROBOT Example:
            l4 session close   l4_session_object=${dh}   sessid=${1}

        :param L4_Session l4_session_object:
           **REQUIRED** The device handle of linux PC wrapped with L4_Session class
           How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create L4 session object    device_handle=${dh}        (ROBOT)
        :param int sessid:
            *OPTIONAL*  Session id to differentiate between multiple sessions. If not provided,
            internally calculated.
        :param str path:
            *OPTIONAL* Path of the tool to run. Default path is /tmp.
    """
    return l4_session_object.close(*args, **kwargs)


def l4_session_start_server(l4_session_object=None, *args, **kwargs):
    """
        To start the Server for the connection using l4_session program
        Example:
            l4_session_start_server(l4_session_object=dh, server_ip="5.0.0.1", protocol="tcp",
                                    server_port=21)

        ROBOT Example:
            l4 Session Start server   l4_session_object=${dh}   server_ip=5.0.0.1   protocol=tcp
                                      server_port=${80}

        :param L4_Session l4_session_object:
           **REQUIRED** The device handle of linux PC wrapped with L4_Session class
           How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create L4 session object    device_handle=${dh}        (ROBOT)
        :param str server_ip:
            **REQUIRED** Server IP to listen in server mode. Server IP to connect in Client mode.
        :param int server_port:
            **REQUIRED**  Server port to listen for connections in server mode. Server port to
            connect on client mode
        :param str protocol:
            *OPTIONAL*  TCP or UDP connection.
            ``Supported values``: "udp" and "tcp"
        :param int sessid:
            *OPTIONAL*  Session id to differentiate between multiple sessions. If not provided,
            internally calculated.
        :param str path:
            *OPTIONAL* Path of the tool to run. Default path is /tmp.
        :return: Returns the session id, if session id 0 indicates failure to start
        :rtype: int
    """
    sess_id = l4_session_start(l4_session_object=l4_session_object, mode="server", *args, **kwargs)
    if sess_id != 0:
        return sess_id

    raise Exception("Server failed to start")


def l4_session_start_client(l4_session_object=None, *args, **kwargs):
    """
        To start the Client for the connection using l4_session program
        Example:
            l4_session_start_client(l4_session_object=dh, server_ip="5.0.0.1", protocol="tcp",
                                    server_port=21, client_ip="4.0.0.1")

        ROBOT Example:
            L4 Session Start client   l4_session_object=${dh}   server_ip=5.0.0.1   protocol=tcp
                                      server_port=${21}   client_ip=4.0.0.1

        :param L4_Session l4_session_object:
           **REQUIRED** The device handle of linux PC wrapped with L4_Session class
           How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create L4 session object    device_handle=${dh}        (ROBOT)
        :param str server_ip:
            **REQUIRED** Server IP to listen in server mode. Server IP to connect in Client mode.
        :param int server_port:
            **REQUIRED**  Server port to listen for connections in server mode. Server port to
            connect on client mode
        :param str client_ip:
            *OPTIONAL*  Client IP to make the connection
        :param int client_port:
            *OPTIONAL*  Client port to make the connection. Default is 0, where random port used
            as client port
        :param str protocol:
            *OPTIONAL*  TCP or UDP connection.
            ``Supported values``: "udp" and "tcp"
        :param int sessid:
            *OPTIONAL*  Session id to differentiate between multiple sessions. If not provided,
            internally calculated.
        :param str path:
            *OPTIONAL* Path of the tool to run. Default path is /tmp.
        :return: Returns the session id, if session id 0 indicates failure to start
        :rtype: int
    """
    sess_id = l4_session_start(l4_session_object=l4_session_object, mode="client", *args, **kwargs)
    if sess_id != 0:
        return sess_id

    raise Exception("Client failed to start")



def l4_session_start_connection(l4_session_object_server=None, l4_session_object_client=None,
                                *args, **kwargs):
    """
        To start the Server or Client for the connection using l4_session program
        Example:
            l4_session_start_connection(l4_session_object_server=dh1, l4_session_object_client=dh2,
                        server_ip="5.0.0.1", protocol="tcp", server_port=21, client_ip="4.0.0.1")

        ROBOT Example:
            L4 Session Start connection   l4_session_object_server=${dh1}   server_ip=5.0.0.1
                                          l4_session_object_client=${dh2}   protocol=tcp
                                          server_port=${21}   client_ip=4.0.0.1

        :param L4_Session l4_session_object_server:
            **REQUIRED** The device handle of linux PC wrapped with L4_Session class on which the
            server would run.
            How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create L4 session object    device_handle=${dh}        (ROBOT)
        :param L4_Session l4_session_object_client:
            **REQUIRED** The device handle of linux PC wrapped with L4_Session class on which the
            client would run.
            How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create L4 session object    device_handle=${dh}        (ROBOT)
        :param str server_ip:
            **REQUIRED** Server IP to listen in server mode. Server IP to connect in Client mode.
        :param int server_port:
            **REQUIRED**  Server port to listen for connections in server mode. Server port to
            connect on client mode
        :param str client_ip:
            *OPTIONAL*  Client IP to make the connection
        :param int client_port:
            *OPTIONAL*  Client port to make the connection. Default is 0, where random port used
            as client port
        :param str protocol:
            *OPTIONAL*  TCP or UDP connection.
            ``Supported values``: "udp" and "tcp"
        :param int sessid:
            *OPTIONAL*  Session id to differentiate between multiple sessions. If not provided,
            internally calculated.
        :param str path:
            *OPTIONAL* Path of the tool to run. Default path is /tmp.
        :return: Dictionary with server and client Session IDs
        :rtype: dict
    """
    dict_sessid = {}
    dict_sessid['server'] = l4_session_start_server(l4_session_object=l4_session_object_server,
                                                    *args, **kwargs)
    dict_sessid['client'] = l4_session_start_client(l4_session_object=l4_session_object_client,
                                                    *args, **kwargs)

    return dict_sessid


def l4_session_close_connection(l4_session_object_server=None, l4_session_object_client=None,
                                sessid1=0, sessid2=0, *args, **kwargs):
    """
        It'll close both server and client sessions
        Example:
        l4_session_close_connection(l4_session_object_server=dh1, l4_session_object_client=dh2)
        l4_session_close_connection(l4_session_object_server=dh1, l4_session_object_client=dh2,
                         sessid1=100, sessid2=200)

        ROBOT Example:
        L4 Session Close connection   packet send object server=${dh1}   sessid1=${100}
                                      packet send object client=${dh2}   sessid2=${200}

        :param L4_Session l4_session_object_server:
           **REQUIRED** The device handle of linux PC wrapped with L4_Session class on which the
            server is running
            How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create L4 session object    device_handle=${dh}        (ROBOT)
        :param L4_Session l4_session_object_client:
            **REQUIRED** The device handle of linux PC wrapped with L4_Session class on which the
            client is running
            How to get this object :
            create_l4_session_object(device_handle=dh)             (PYTHON)
            create L4 session object    device_handle=${dh}        (ROBOT)
        :param int sessid1:
            *OPTIONAL*  Session id for PC1 (on which server is running) to differentiate between
            multiple sessions. If not provided, internally calculated.
        :param int sessid2:
            *OPTIONAL*  Session id for PC2 (on which client is running) to differentiate between
            multiple sessions. If not provided, internally calculated.
        :param str path:
            *OPTIONAL* Path of the tool to run. Default path is /tmp.
    """

    l4_session_close(l4_session_object=l4_session_object_client, sessid=sessid2, *args, **kwargs)
    l4_session_close(l4_session_object=l4_session_object_server, sessid=sessid1, *args, **kwargs)
