"""
Radius Flow Tap
"""
import re
import hmac
import hashlib
import os
import time
import ipaddress
import socket
import paramiko

SEQUENCE_NUMBER = 1

class RadiusFlowtapDtcp():
    """
      Class for FLOWTAP DTCP Requests
      Supports ADD,DELETE & LIST Filter requests

      """

    def dtcp_add_filter(self, **kwargs):
        """
        Method constructs ADD request based on user input parametrs and sends it to the DUT
        :param filter_type:
          **REQUIRED**     Should specify if the filter is [global/ccc_in/ccc_out/v4/v6]
        :param num_filt:
          *OPTIONAL*       Specify the number of Add Requests to be sent
        :param csource_id:
          **REQUIRED**     Control Source which is pre-configured/authorized by the router
        :param cdest1_id:
          **REQUIRED**     Content Destination name to which tapped packets should be sent
        :param src_port:
          *OPTIONAL*       Source Port for which traffic should be tapped.
        :param dst_port:
          *OPTIONAL*       Destination Port for which traffic shoucsource_addrld be tapped.
        :param src_addr:
          *OPTIONAL*       Source address for which traffic should be tapped.
        :param dst_addr:
          *OPTIONAL*       Destination address for which traffic should be tapped.
        :param protocol:
          *OPTIONAL*       Protocol for which traffic should be tapped.
        :param csource_addr:
          **REQUIRED**     Control source address which needs to be encapsulated for tapped packet
        :param cdest1_addr:
          **REQUIRED**     Address of Content Destination.
        :param cdest1_port:
          **REQUIRED**     Port on Content Destination to which tapped packet needs to be sent.
        :param intf:
          **OPTIONAL**     Interface name on which tap needs to be applied
        :param router:
          **REQUIRED**     Router name to which DTCP ADD request should be sent
        :return      :       Returns True if dtcp message returned is 1 else False

        """

        router = kwargs['router']
        filter_type = ""
        csource_port = 49153
        filters = int(kwargs['num_filt'])
        sr_file = ""
        version = 0.7
        if 'version' in kwargs:
            version = kwargs['version']
        # If src_addr parameter is passed ipaddress module creates object from string
        if 'src_addr' in kwargs:
            if "*" in kwargs['src_addr']:
                src_addr = "*"
            else:
                src_addr = ipaddress.ip_address(kwargs['src_addr'])

        # If dst_addr parameter is passed ipaddress module creates object from string
        if 'dst_addr' in kwargs:
            if "*" in kwargs['dst_addr']:
                dst_addr = "*"
            else:
                dst_addr = ipaddress.ip_address(kwargs['dst_addr'])

        # If filter_type parameter is ccc_in/v4_in/v6_in below tag will be added
        # In ADD request appending with intf parameter
        if "in" in kwargs['filter_type']:
            filter_type = "X-JTap-Input-Interface"

        # If filter_type parameter is ccc_out/v4_out/v6_out below tag will be added
        # In ADD request appending with intf parameter
        if "out" in kwargs['filter_type']:
            filter_type = "X-JTap-Output-Interface"

        # If filter_type parameter is vrf below tag will be added In ADD request
	# appending with intf parameter
        if "vrf" in kwargs['filter_type']:
            filter_type = "X-JTap-VRF-Name"

        # If Content destinations cd1 & cd2 are passed as parameters
	# they are formated as cd1,cd2 in the request
        if 'cdest2_id' in kwargs.keys() and 'cdest1_id' in kwargs.keys():
            cdest_id = "{0},{1}".format(kwargs['cdest1_id'], kwargs['cdest2_id'])
            cdest_addr = "{0},{1}".format(kwargs['cdest1_addr'], kwargs['cdest2_addr'])
            cdest_port = "{0},{1}".format(kwargs['cdest1_port'], kwargs['cdest2_port'])
        elif 'cdest1_id' in kwargs.keys():
            cdest_id = kwargs['cdest1_id']
            cdest_addr = kwargs['cdest1_addr']
            cdest_port = kwargs['cdest1_port']
        elif 'cdest2_id' in kwargs.keys():
            cdest_id = kwargs['cdest2_id']
            cdest_addr = kwargs['cdest2_addr']
            cdest_port = kwargs['cdest2_port']

        if 'csource_port' in kwargs.keys():
            csource_port = kwargs['csource_port']

        # Below code constructs the ADD request depending on parameters passed
        # While loop executed till ADD requests for number of filters requested is sent
        while filters >= 1:
            sr_file = "ADD DTCP/" + str(version) + "\n"
            sr_file += "Csource-ID: " + str(kwargs['csource_id']) + "\n"
            sr_file += "Cdest-ID: " + str(cdest_id) + "\n"
            if "ccc" not in kwargs['filter_type'] or "neg" in kwargs['filter_type']:
                sr_file += "Source-Address: " + str(src_addr) + "\n"
                sr_file += "Dest-Address: " + str(dst_addr) + "\n"
                sr_file += "Source-Port: " + str(kwargs['src_port']) + "\n"
                sr_file += "Dest-Port: " + str(kwargs['dst_port']) + "\n"
            sr_file += "Protocol: " + str(kwargs['protocol']) + "\n"
            sr_file += "Priority: 2\n"
            sr_file += "X-JTap-Cdest-Dest-Address: " + str(cdest_addr) + "\n"
            sr_file += "X-JTap-Cdest-Dest-Port: " + str(cdest_port) + "\n"
            sr_file += "X-JTap-Cdest-Source-Address: " + str(kwargs['csource_addr']) + "\n"
            sr_file += "X-JTap-Cdest-Source-Port: " + str(csource_port) + "\n"
            if 'intf' in kwargs:
                sr_file += filter_type + ": " + str(kwargs['intf']) + "\n"
            if "v6" in kwargs['filter_type']:
                sr_file += "X-JTap-IP-Version: ipv6\n"
            if "ccc" in kwargs['filter_type'] or "neg" in kwargs['filter_type']:
                sr_file += "X-Jtap-Filter-Family: ccc\n"
            sr_file += "X-JTap-Cdest-TTL: " + str(kwargs['ttl']) + "\n"
            sr_file += "Flags: STATIC\n"
            sr_file += "\n"

            # Increments the src addr if increment step(src_step) paramet is passed
            if 'src_step' in kwargs:
                src_step = kwargs['src_step']
                if 'src_addr' in kwargs:
                    if "*" not in kwargs['src_addr']:
                        src_addr = src_addr + src_step

            filters = filters - 1

            # Writes the string generated above to a file appending with process ID
        pid = os.getpid()
        ptr = open('/tmp/filter_add_' + router + '_' + str(pid), 'w')
        ptr.write(sr_file)
        ptr.close()

        print("{}{}{}".format("File created with filter to ADD is ",
                              '/tmp/filter.fil_' + router + '_' + str(pid), '\n'))

        # Hands the file to flow tap method to send it to DUT after SSH Authentication
        resp_file = self._flow_tap(router, kwargs['csource_id'], str(kwargs['csource_id']) + "123",
                                   '/tmp/filter_add_' + router + '_' + str(pid), SEQUENCE_NUMBER)

        # Sends the response to dtcp response method to validate the reply
        (resp_hash, dtcp_ok) = self._dtcp_response(resp_file)

        # Removes the files generated during ADD request and reply
        os.remove('/tmp/filter_add_' + router + '_' + str(pid))
        os.remove(resp_file)

        if int(dtcp_ok) == 1:
            print("True\n")
            return True
        else:
            print("False\n")
            return False

    def dtcp_add_sbr_filter(self, **kwargs):

        """
        Method constructs ADD request based on user input parametrs and sends it to the DUT

        :param filter_type:
          **REQUIRED**     Should specify if the filter is [global/ccc_in/ccc_out/v4/v6]
        :param num_filt:
          *OPTIONAL*       Specify the number of Add Requests to be sent
        :param dst_step:
          *OPTIONAL*       Specify the number of IP's to increment in source address
        :param src_step:
          *OPTIONAL*       Specify the number of IP's to increment in destination address
        :param csource_id:
          **REQUIRED**     Control Source which is pre-configured/authorized by the router
        :param cdest1_id:
          **REQUIRED**     Content Destination name to which tapped packets should be sent
        :param src_port:
          *OPTIONAL*       Source Port for which traffic should be tapped.
        :param dst_port:
          *OPTIONAL*       Destination Port for which traffic should be tapped.
        :param src_addr:
          *OPTIONAL*       Source address for which traffic should be tapped.
        :param dst_addr:
          *OPTIONAL*       Destination address for which traffic should be tapped.
        :param protocol:
          *OPTIONAL*       Protocol for which traffic should be tapped.
        :param csource_addr:
          **REQUIRED**     Control source address which needs to be encapsulated for tapped packet
        :param cdest1_addr:
          **REQUIRED**     Address of Content Destination.
        :param cdest1_port:
          **REQUIRED**     Port on Content Destination to which tapped packet needs to be sent.
        :param intf:
          **OPTIONAL**     Interface name on which tap needs to be applied
        :param ttl:
          **OPTIONAL**     TTL of packet
        :param circuit_id:
          **OPTIONAL**     Circuit Id
        :param router:
          **REQUIRED**     Router name to which DTCP ADD request should be sent
        :return      :       Returns True if dtcp message returned is 1 else False


        """
        #ip_src = 0
        #ip_dst = 0
        router = kwargs['router']
        #filter_type = ""
        #csource_port = 49153
        filters = int(kwargs['num_filt'])
        sr_file = ''
        version = 0.7
        if 'version' in kwargs:
            version = kwargs['version']


        # Below code constructs the ADD request depending on parameters passed
        # While loop executed till ADD requests for number of filters requested is sent

        ###################### SBR #########################
        if 'user_name' not in kwargs and 'circuit_id' not in kwargs:
            raise Exception("either user_name or circuit_id argument should be provided")
        while filters >= 1:
            sr_file = "ADD DTCP/" + str(version) + "\n"
            sr_file += "Csource-ID: " + str(kwargs['csource_id']) + "\n"
            sr_file += "Cdest-ID: " + str(kwargs['cdest_id']) + "\n"
            sr_file += "Priority: 2\n"
            sr_file += "X-JTap-Cdest-Dest-Address: " + str(kwargs['cdest_addr']) + "\n"
            sr_file += "X-JTap-Cdest-Dest-Port: " + str(kwargs['cdest_port']) + "\n"
            sr_file += "X-JTap-Cdest-Source-Address: " + str(kwargs['csource_addr']) + "\n"
            sr_file += "X-JTap-Cdest-Source-Port: " + str(kwargs['csource_port']) + "\n"
            if 'user_name' in kwargs:
                sr_file += "X-UserName: " + str(kwargs['user_name']) + "\n"
            sr_file += "X-Logical-System: " + str(kwargs['li']) + "\n"
            sr_file += "X-Router-Instance: " + str(kwargs['ri']) + "\n"
            sr_file += "X-MD-Intercept-Id: 41414141\n"
            sr_file += "X-JTap-Cdest-TTL: " + str(kwargs['ttl']) + "\n"
            if 'circuit_id' in kwargs:
                sr_file += "X-RM-Circuit-id: " + str(kwargs['circuit_id']) + "\n"
            sr_file += "Flags: STATIC\n"
            sr_file += "\n"
            # Increments the src addr if increment step(src_step) paramet is passed

            filters = filters - 1

            # Writes the string generated above to a file appending with process ID
        pid = os.getpid()
        ptr = open('/tmp/filter_add_' + router + '_' + str(pid), 'w')
        ptr.write(sr_file)
        ptr.close()

        print("{}{}{}".format("File created with filter to ADD is ",
                              '/tmp/filter.fil_' + router + '_' + str(pid), '\n'))

        # Hands the file to flow tap method to send it to DUT after SSH Authentication
        resp_file = self._flow_tap(router, kwargs['csource_id'], str(kwargs['csource_id']) + "123",
                                   '/tmp/filter_add_' + router + '_' + str(pid), SEQUENCE_NUMBER)

        # Sends the response to dtcp response method to validate the reply
        (resp_hash, dtcp_ok) = self._dtcp_response(resp_file)

        # Removes the files generated during ADD request and reply
        os.remove('/tmp/filter_add_' + router + '_' + str(pid))
        os.remove(resp_file)

        if int(dtcp_ok) == 1:
            print("True\n")
            return True
        else:
            print("False\n")
            return False

    def _flow_tap(self, *args):
        """
        Opens a ssh to DUT and sends the DTCP request returns the DTCP response which is filed
        """
        router = args[0]
        user = args[1]
        password = args[2]
        file_name = args[3]
        seq_num = 0
        opt_seq_num = 0
        seq_num_found_int_file = 0
        #SEQUENCE_NUMBER = 0
        key = 'Juniper'
        digest = ""
        dtcp_cmd = ""
        strline = ""
        opt_seq_num = 1

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((router, 32001))

        trans = paramiko.Transport(socket1)
        trans.connect(username=user, password=password)

        # CREATE CHANNEL FOR DATA COMM
        cha = trans.open_session()

        # Invoke flow-tap-dtcp Subsystem
        cha.invoke_subsystem('flow-tap-dtcp')

        # Below code reads the lines in file and adds sequence number and Authentication-Info
        fpr = open(file_name, "r")
        lines = fpr.readlines()
        for line in lines:
            line = line.strip()
            if line == "":
                seq_num += 1
                if opt_seq_num or not seq_num_found_int_file:
                    # Add DTCP Sequence number
                    dtcp_cmd = dtcp_cmd + "Seq: " + str(seq_num) + '\r\n'

                    # Code to caluclate hexdigest using hmac for the add request
                    key = bytes(key, 'utf-8')
                    msg = bytes(dtcp_cmd, 'utf-8')
                    digest_maker = hmac.new(key, msg, hashlib.sha1)
                    digest = digest_maker.hexdigest()
                    dtcp_cmd = dtcp_cmd + "Authentication-Info: " + digest + '\r\n\r\n'

                    print("Sending DTCP Command\n")
                    print(dtcp_cmd)
                    cha.send(dtcp_cmd)
                    time.sleep(2)
                    data = cha.recv(2048)
                    data = data.decode("utf-8")
                    print(data)
                    pid = os.getpid()
                    ptr = open('/tmp/filter_resp_' + router + '_' + str(pid), 'w')
                    ptr.write(data)
                    ptr.close()
            else:
                if line == "seq":
                    seq_num_found_int_file = 1
                    if not opt_seq_num:
                        dtcp_cmd = dtcp_cmd + strline + "\r\n"
                else:
                    dtcp_cmd = dtcp_cmd + line + '\r\n'

        cha.close()
        trans.close()
        socket1.close()

        return '/tmp/filter_resp_' + router + '_' + str(pid)

    def _dtcp_response(self, *args):
        """
        Method  returns the DTCP reply to the requested function
        """
        resp_hash = []
        pattern1 = [re.compile(p) for p in
                    [r'^[ \t]*$', 'password', '^Warning', '^SEQ', r'^TIMESTAMP:.*', '^DTCP',
                     '^AUTHENTICATION']]
        file_name = args[0]
        dtcp_ok = 0
        print("Converting the response in the response to a hash")
        time.sleep(4)
        # Below code reads the lines in response and checks for 200 OK
        fpr = open(file_name, "r")
        lines = fpr.readlines()
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            if re.match(r'DTCP/\d.\d\s(\d+)\s(.*)', line):
                mch = re.match(r'DTCP/\d.\d\s(\d+)\s(.*)', line)
                value = mch.group(1)
                resp_hash = mch.group(2)
                if int(value) is 200:
                    print("DTCP 200 OK is received as expected")
                    dtcp_ok += 1
                else:
                    print("DTCP 200 OK is not received")
                del lines[:]
            for reg in pattern1:
                if reg.match(line):
                    break
            if not re.match(r'[A-Z]', line):
                continue
            elif line == "Received disconnect":
                break

        # out = line.split()
        #  resp_hash = out[1]
        # Returns dtcp_ok = 1 if 200 OK is recived else returns 0
        # print(resp_hash, dtcp_ok)
        return (resp_hash, dtcp_ok)

    def dtcp_list_filter(self, **kwargs):
        """
        Method  sends list request to DUT

        :param csource_id:
          **REQUIRED**     Control Source which is pre-configured/authorized by the router
        :param cdest_id:
          **REQUIRED**     Content Destination name to which tapped packets should be sent
         usage         :   dtcp_list_filter(router="esst480s")
        """
        sr_file = ''
        router = kwargs['router']

        if kwargs['id'] == 'cdest':
            sr_file = "LIST DTCP/0.7\n"
            sr_file += "Csource-ID: " + str(kwargs['csource_id']) + "\n"
            sr_file += "CDest-ID: " + str(kwargs['id_val']) + "\n"
            sr_file += "Flags: " + str(kwargs['flag']) + "\n"
            sr_file += "\n"
        else:
            sr_file = "LIST DTCP/0.7\n"
            sr_file += "Csource-ID: " + str(kwargs['csource']) + "\n"
            sr_file += "Flags:  " + str(kwargs['flags']) + "\n"
            sr_file += "\n"

        # Writes the string generated above to a file appending with process ID
        pid = os.getpid()
        ptr = open('/tmp/filter_list_' + router + '_' + str(pid), 'w')
        ptr.write(sr_file)
        ptr.close()

        # Hands the file to flow tap method to send it to DUT after SSH Authentication
        resp_file = self._flow_tap(router, kwargs['csource_id'], str(kwargs['csource_id']) + "123",
                                   '/tmp/filter_list_' + router + '_' + str(pid), SEQUENCE_NUMBER)

        # Sends the response to dtcp response method to validate the reply
        (resp_hash, dtcp_ok) = self._dtcp_response(resp_file)

        # Removes the files generated during LIST equest and reply
        os.remove('/tmp/filter_list_' + router + '_' + str(pid))
        os.remove(resp_file)
        if int(dtcp_ok) == 1:
            print("True\n")
            return True
        else:
            print("False\n")
            return False

    def dtcp_delete_filter(self, **kwargs):
        """
        Method  sends delete request to DUT
        :param csource_id:
          **REQUIRED**     Control Source which is pre-configured/authorized by the router
        :param cdest1_id:
          **REQUIRED**     Content Destination name to which tapped packets should be sent
        :param Criteria-ID:
           *Optional*      Criteria ID of the request
        :Usage         :   dtcp_delete_filter(csource_id="ftap1",id="cdest",id_val="cd1")
        """

        router = kwargs['router']
        sr_file = ""

        print("Check to create and send the delete filter")
        resp_hash = 0
        dtcp_ok = 0

        if kwargs['id'] == "cdest":
            sr_file = "DELETE DTCP/0.7\n"
            sr_file += "Csource-ID: " + str(kwargs['csource_id']) + "\n"
            sr_file += "CDest-ID: " + str(kwargs['id_val']) + "\n"
            sr_file += "Flags: STATIC\n"
            sr_file += "\n"
        else:
            sr_file = "DELETE DTCP/0.7\n"
            sr_file += "Csource-ID: " + str(kwargs['csource_id']) + "\n"
            sr_file += "Criteria-ID: " + str(kwargs['id_val']) + "\n"
            sr_file += "Flags: STATIC\n"
            sr_file += "\n"

        # Writes the string generated above to a file appending with process ID
        pid = os.getpid()
        ptr = open('/tmp/filter_del_' + router + '_' + str(pid), 'w')
        ptr.write(sr_file)
        ptr.close()
        # timeout = 1500 # timeout should be configured globally

        # Hands the file to flow tap method to send it to DUT after SSH Authentication
        resp_file = self._flow_tap(router, kwargs['csource_id'], str(kwargs['csource_id']) + "123",
                                   '/tmp/filter_del_' + router + '_' + str(pid), SEQUENCE_NUMBER)

        # Sends the response to dtcp response method to validate the reply
        (resp_hash, dtcp_ok) = self._dtcp_response(resp_file)

        # Removes the files generated during DELETE request and reply
        os.remove('/tmp/filter_del_' + router + '_' + str(pid))
        os.remove(resp_file)
        if int(dtcp_ok) == 1:
            print("True\n")
            return True
        else:
            print("True\n")
            return False



