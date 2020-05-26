""" This module defines the FreeRADIUS class and class methods.
"""
####################################
# Importing Python In Built Libraries
######################################

import time
import os
import re
import tempfile
import paramiko
from pexpect import pxssh

#################
# ToBY Libraries
#################
from jnpr.toby.utils.Vars import Vars
from robot.libraries.BuiltIn import BuiltIn

class Radius:

    """Perform Configuration and Verification Function for Radius Server : Free Radius"""

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.test = 1

    @staticmethod
    def configure_certificates(tag):
        """Configure CA certificate on the radius server.

        :return:
            True if Certificate Configured Successfully on the server
            False otherwise
        """

        t.log("inside def")
        device = t.get_handle(resource=tag)
        if device is None:
            return False

        ################ Generate certificates######################

        response = device.shell(command="mkdir morecerts")
        stdout = response.response()
        t.log("Printing Command Output: ")
        t.log(stdout)

        response = device.shell(command="mkdir morecerts/private morecerts/backup")
        stdout = response.response()
        t.log("Printing Command Output: ")
        t.log(stdout)

        response = device.shell(command="openssl req -config /usr/lib/ssl/openssl.cnf -new -x509 -keyout morecerts/private/cakey.pem -out cacert.pem -days 3650")
        stdout = response.response()
        t.log("Printing Command Output: ")
        t.log(stdout)

        response = device.shell(command="openssl x509 -in cacert.pem -out cacert.crt")
        stdout = response.response()
        t.log("Printing Command Output: ")
        t.log(stdout)
        response = device.shell(command="cp cacert.pem /etc/raddb/certs/")
        stdout = response.response()
        t.log("Printing Command Output: ")
        t.log(stdout)

        response = device.shell(command="cp cacert.crt /etc/raddb/certs/")
        stdout = response.response()
        t.log("Printing Command Output: ")
        t.log(stdout)

        response = device.shell(command="cp private/cakey.pem /etc/raddb/certs/")
        stdout = response.response()
        t.log("Printing Command Output: ")
        t.log(stdout)

        response = device.shell(command="openssl dhparam-check-text -5 512 -out/etc/raddb/certs/dh")
        stdout = response.response()
        t.log("Printing Command Output: ")
        t.log(stdout)
        response = device.shell(command="openssl rand -out/etc/raddb/certs/random 100")
        stdout = response.response()
        t.log("Printing Command Output: ")
        t.log(stdout)
        return True

    @staticmethod
    def restart_radius_server(tag, stop_start_rad):
        """Start/Stop/Restart radiusd process on freeradius server

        :return: True if radiusd process start/stop/restart  on the server
            False otherwise
        """
        result = True
        device = t.get_handle(resource=tag)
        if device is None:
            return False
        response = device.shell(command="ps aux | grep radius")
        stdout = response.response()
        t.log(stdout)
        result = "False"
        radstr = 'radiusd'
        for output in stdout.splitlines():
            if radstr in output:
                t.log("2nd Output :\n")
                output_final = output
                t.log(output_final)
                output = output_final.split()
                t.log("Radius Daemon Process Name:")
                rad_daemon = 'radiusd'
                t.log(rad_daemon)
                prc_id = output[1]
                t.log("Radius Daemon Process ID:")
                t.log(prc_id)
                break
            else:
                t.log("Radiusd not running - setting Radius user to root\n")
                rad_daemon = 'root'
        if(rad_daemon == "radiusd") and (stop_start_rad == "restart"):
            cmd = "kill -9 " + prc_id
            t.log(cmd)
            response = device.shell(command=cmd)
            stdout = response.response()
            time.sleep(2)
            response = device.shell(command="radiusd")
            stdout = response.response()
            t.log("Restarting radiusd process is Success:\n")
            t.log(stdout)
            response = device.shell(command="ps aux | grep radius")
            stdout = response.response()
            t.log(stdout)
            result = "True"
            t.log("Command done, closing SSH connection")
        elif(rad_daemon == "radiusd") and (stop_start_rad == "stop"):
            cmd = "kill -9 " + prc_id
            t.log(cmd)
            response = device.shell(command=cmd)
            stdout = response.response()
            t.log("Stoping radiusd process is Success:\n")
            t.log(stdout)
            response = device.shell(command="ps aux | grep radius")
            stdout = response.response()
            t.log(stdout)
            result = "True"
            t.log("Command done, closing SSH connection")
        elif(stop_start_rad == "start") and (rad_daemon != "radiusd"):
            response = device.shell(command="radiusd")
            stdout = response.response()
            t.log("Starting radiusd process is Success:\n")
            t.log(stdout)
            response = device.shell(command="ps aux | grep radius")
            stdout = response.response()
            t.log(stdout)
            result = "True"
            t.log("Command done, closing SSH connection")
        else:
            t.log(" Radius process already UP and Running ")
            result = "True"
            t.log("Command done, closing SSH connection")
        return result

    @staticmethod
    def add_radius_server_user(hostip, username, password, user_data, filepath, usertype, dm_param, radius_logpath):
        """Add Radius Users for Authentications and generationg Coa on freeradius server

        :return:
            True if Radius user/coa addition successful on the server
            False otherwise
        """
        t.log("Inside local")
        if dm_param != "no":
            t.log(" ********************\n")
            t.log("Fetch Values User-Name, Acct-Session-Id, Called-Station-Id & Calling-Station-Id\n")
            t.log(" *********************\n")
            # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))
            # Auth
            t.log("Yet to Authenticate .. inside local")
            transport.connect(username=username, password=password)
            # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)
        # Download
            filepath1 = radius_logpath+'mschap.log'
            localpath1 = 'mschap.log'
            sftp.get(filepath1, localpath1)
            sftp.close()
            transport.close()
            if os.stat("mschap.log").st_size == 0:
                t.log("mschap.log is EMPTY")
                return False
            rad_msg_user = 'User-Name = "'
            rad_msg_acct = 'Acct-Session-Id = "'
            rad_msg_called = 'Called-Station-Id = "'
            rad_msg_calling = 'Calling-Station-Id = "'
            file = open('mschap.log', "r")
            file_port = file.readlines()
            file.close()
        # Fetching Value for User-Name
            for line in file_port:
                if rad_msg_user in line:
                    a_list = line.split(rad_msg_user)
                    break
            t.log(a_list)
            list1 = a_list[1]
            port_list = list1.split('"')
            t.log(port_list)
            dut_user = port_list[0]
            t.log("User Name: ")
            t.log(dut_user)
            rad_user_name = 'User-Name = ' + str(dut_user)
            t.log(rad_user_name)
        # Fetching Value for Acct-Session-Id
            for line in file_port:
                if rad_msg_acct in line:
                    a_list = line.split(rad_msg_acct)
                    break
            t.log(a_list)
            list1 = a_list[1]
            port_list = list1.split('"')
            t.log(port_list)
            dut_acct = port_list[0]
            t.log("Acct Session ID: ")
            t.log(dut_acct)
            rad_acct_id = 'Acct-Session-Id = ' + str(dut_acct)
            t.log(rad_acct_id)
        # Fetching Value for Called-Station-Id
            for line in file_port:
                if rad_msg_called in line:
                    a_list = line.split(rad_msg_called)
                    break
            t.log(a_list)
            list1 = a_list[1]
            port_list = list1.split('"')
            t.log(port_list)
            dut_called = port_list[0]
            t.log("Called Station ID: ")
            t.log(dut_called)
            rad_called_id = 'Called-Station-Id = ' + str(dut_called)
            t.log(rad_called_id)
        # Fetching Value for Calling-Station-Id
            for line in file_port:
                if rad_msg_calling in line:
                    a_list = line.split(rad_msg_calling)
                    break
            t.log(a_list)
            list1 = a_list[1]
            port_list = list1.split('"')
            t.log(port_list)
            dut_calling = port_list[0]
            t.log("Calling Station ID: ")
            t.log(dut_calling)
            rad_calling_id = 'Calling-Station-Id = ' + str(dut_calling)
            t.log(rad_calling_id)
            result = "False"
        if (usertype == "coa") and (dm_param == "acct"):
        # Download
            user_data_final = str(user_data) + str(rad_acct_id)
            with open('coa', "w+") as file:
                file.write(user_data_final)
                file.close()
        # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))
        # Auth
            t.log("Yet to Authenticate")
            transport.connect(username=username, password=password)
        # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)
        # Upload
            localpath = 'coa'
            sftp.put(localpath, os.path.join(filepath, localpath))
        # Close
            sftp.close()
            transport.close()
            result = "True"
        elif (usertype == "coa") and (dm_param == "calling"):
        # Download
            user_data_final = str(user_data) + str(rad_calling_id)
            with open('coa', "w+") as file:
                file.write(user_data_final)
                file.close()
        # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))
        # Auth
            t.log("Yet to Authenticate")
            transport.connect(username=username, password=password)
        # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)
        # Upload
            localpath = 'coa'
            sftp.put(localpath, os.path.join(filepath, localpath))
        # Close
            sftp.close()
            transport.close()
            result = "True"
        elif (usertype == "coa") and (dm_param == "acct_calling"):
        # Download
            user_data_final = str(user_data) + str(rad_acct_id) + '\n' + str(rad_calling_id)
            with open('coa', "w+") as file:
                file.write(user_data_final)
                file.close()
        # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))
        # Auth
            t.log("Yet to Authenticate")
            transport.connect(username=username, password=password)
        # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)
        # Upload
            localpath = 'coa'
            sftp.put(localpath, os.path.join(filepath, localpath))
        # Close
            sftp.close()
            transport.close()
            result = "True"
        elif (usertype == "user") and (dm_param == "no"):
        # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))
        # Auth
            t.log("Yet to Authenticate")
            transport.connect(username=username, password=password)
        # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)
        # Download
            localpath = 'users'
            sftp.get(filepath, localpath)
            with open('users', "a") as file:
                file.write(user_data)
                file.close()
         # Upload
            localpath = 'users'
            sftp.put(localpath, filepath)
         # Close
            sftp.close()
            transport.close()
            result = "True"
        elif (usertype == "coa") and (dm_param == "no"):
            t.log("creating coa file\n")
            with open('coa', "w+") as file:
                file.write(user_data)
                file.close()
         # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))
         # Auth
            t.log("Yet to Authenticate")
            transport.connect(username=username, password=password)
         # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)
         # Upload
            localpath = 'coa'
            sftp.put(localpath, os.path.join(filepath, localpath))
            t.log("wait for 10 minutes")
            time.sleep(10)
         # Close
            sftp.close()
            transport.close()
            result = "True"
            t.log("We have executed this Successfully\n")
            return result
        else:
            t.log("User/CoA files creation and update failed!!")
            result = "False"
        t.log("We have executed this Successfully\n")
        return result

    @staticmethod
    def remove_radius_server_user(hostip, username, password, radius_user, filepath, usertype, attribute_num):
        """Remove Radius Users for Authentications and generationg Coa on freeradius server

        :return:
            True if Radius user/coa removal successful on the server
            False otherwise
        """
        if usertype == "user":
        # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))
        # Auth
            t.log("Yet to Authenticate")
            transport.connect(username=username, password=password)
        # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)
        # Download
            localpath = 'users'
            sftp.get(filepath, localpath)
            line_num = 0
            with open('users') as file:
                for i, line in enumerate(file, 1):
                    if radius_user in line:
                        line_num = i
            file.close()
            file = open('users', "r")
            file_list = file.readlines()
            if line_num != 0:
                del file_list[line_num-1:line_num+int(attribute_num)]
            else:
                t.log("Radius User radius_user not found")
                return True

            file2 = open("users", "w")
            file2.writelines(file_list)
            file2.close()
        # Upload
            localpath = 'users'
            sftp.put(localpath, filepath)

        # Close
            sftp.close()
            transport.close()
            result = "True"

        elif usertype == "coa":
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                username = username
                password = password
                ssh.connect(hostip, username=username, password=password)
                t.log("done ssh to")
            except:
                t.log("Connection Failed")
                return False
            result = "False"
            filename = 'coa'
            filename1 = 'output'
            targetfile = os.path.join(filepath, filename)
            targetfile1 = os.path.join(filepath, filename1)
            cmd = "rm -f " + targetfile
            cmd1 = "rm -f " + targetfile1
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdin.close()
            stdin, stdout, stderr = ssh.exec_command(cmd1)
            stdin.close()
            result = True
            time.sleep(5)
            t.log(stdout)
        else:
            t.log("Deletion Failed - User/CoA files!!")
            result = "False"

        return result
 
    @staticmethod
    def remove_radius_server_client(hostip, username, password, filepath, clientip):
        """Remove Radius clients for Authentications from clients.conf from freeradius server

        :return:
            True if Radius client removal successful on the server
            False otherwise
        """ 
        # Open a transport
        host = hostip
        port = 22
        transport = paramiko.Transport((host, port))
        # Auth
        t.log("Yet to Authenticate")
        transport.connect(username=username, password=password)
        # Go!
        t.log("Yet to open SFTPClient")
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Download
        localpath = 'clients.conf' 
        tmpfile = 'clients1.conf'
        sftp.get(filepath, localpath)
        fw = open(localpath, "r")
        #fwr = tempfile.NamedTemporaryFile(delete=False)
        #t.log(fwr.name)
        fwrite = open(tmpfile, "w")
        matopen = re.compile("%s\s{" % clientip)
        matclose = re.compile("}")
        blockopen = 0
        blockclose = 0
        line_update = 0
        for f in fw.readlines():
            if re.search(matopen, f):
                t.log("line matched for open block is %s " % f)
                blockopen = 1
            elif re.search(matclose, f) and blockopen == 1:
                t.log("line matched for close block is %s " % f)
                blockopen = 0
                blockclose = 1
                line_update += 1
            elif blockopen == 0 and not blockclose: #not re.search(matclose, f): # and not blockclose:
                fwrite.write(f)
            blockclose = 0
        t.log("line update value : %s" % line_update)
        fw.close()
        fwrite.close()
        os.rename(tmpfile, localpath)
        sftp.put(localpath, filepath)
        if line_update:
            return True
        else:
            return False

    @staticmethod
    def packet_capture_radius(tag, supplicant_name, capture_action, radius_logpath):
        """Add Radius Users for Authentications and generationg Coa on freeradius server

        :return:
            True if Radius user/coa addition successful on the server
            False otherwise
        """
        result = True
        t.log("inside def")
        device = t.get_handle(resource=tag)
        if device is None:
            return False
        response = device.shell(command="ps aux | grep radius")
        stdout = response.response()
        t.log("Printing Command Output: ")
        t.log(stdout)

        result = "False"
        radstr = 'radiusd'
        for output in stdout.splitlines():
            if radstr in output:
                t.log("2nd Output :\n")
                output_final = output
                t.log(output_final)
                output = output_final.split()
                t.log("Radius Daemon Process Name:")
                rad_daemon = 'radiusd'
                t.log(rad_daemon)
                prc_id = output[1]
                t.log("Radius Daemon Process ID:")
                t.log(prc_id)
                break
            else:
                t.log("Radiusd not running - Please check manually if no errors\n")
        if (rad_daemon == "radiusd") and (capture_action == "start"):
            t.log("removing mschap.log\n")
            #response = device.shell(command="rm -rf "+radius_logpath+"mschap.log", pattern='~]# ', timeout=10)
            response = device.shell(command="rm -rf "+radius_logpath+"mschap.log")
            t.log("Setting Directory Path \n")
            # response = device.shell(command="cd "+radius_logpath, pattern='~]# ', timeout=10)
            response = device.shell(command="cd "+radius_logpath)
            t.log("Send the radmin command wait for a prompt:\n")
            response = device.shell(command="radmin", pattern='radmin> ', timeout=10)
            t.log("Clear Debug File and Condition and wait for a prompt again\n")
            response = device.shell(command="debug file", pattern='radmin> ', timeout=10)
            t.log("Set debug file and condition for user and wait for a prompt again\n")
            response = device.shell(command="debug file mschap.log", pattern='radmin> ', timeout=10)
            response = device.shell(command=""'debug condition \'(User-Name == "'+supplicant_name+'")\'\n'"", pattern='radmin> ', timeout=10)
            t.log(" Display output for show debug condition and wait for a prompt again\n")
            response = device.shell(command="show debug condition", pattern='radmin> ', timeout=10)
            t.log("Quit fro radmin prompt\n")
            #response = device.shell(command="quit", pattern='~]# ', timeout=10)
            response = device.shell(command="quit") 
            result = "True"
        elif (rad_daemon == "radiusd") and (capture_action == "stop"):
            t.log("going to radmin\n")
            response = device.shell(command="radmin", pattern='radmin> ', timeout=10)
            time.sleep(1)
            t.log("removing debug file and condition\n")
            response = device.shell(command="debug file", pattern='radmin> ', timeout=10)
            time.sleep(1)
            response = device.shell(command="debug condition", pattern='radmin> ', timeout=10)
            time.sleep(1)
            response = device.shell(command="quit")
            result = "True"
        else:
            t.log("Radius process is not running")
            result = "False"
        t.log("Command done, closing SSH connection")
        return result

    @staticmethod
    def verify_dot1x_msgs(hostip, username, password, deviceip, proto_type, tlv_list, accounting_on, radius_logpath):
        """Verify Dot1x Message for Access and Accouting on freeradius server

        :return:
            True if Access and Accounting Verification successful on the server
            False otherwise
        """
    # Open a transport
        port = 22
        transport = paramiko.Transport((hostip, port))
    # Auth
        t.log("Yet to Authenticate")
        transport.connect(username=username, password=password)
    # Go!
        t.log("Yet to open SFTPClient")
        sftp = paramiko.SFTPClient.from_transport(transport)
    # Download
        filepath = radius_logpath+'mschap.log'
        localpath = 'mschap.log'
        sftp.get(filepath, localpath)
        sftp.close()
        transport.close()
        if os.stat("mschap.log").st_size == 0:
            t.log("mschap.log is EMPTY")
            return False

        if accounting_on == "sameserver":
            rad_msg_port = "Received Access-Request packet from host "+deviceip+" port "
            file = open('mschap.log', "r")
            file_port = file.readlines()
            file.close()

            for line in file_port:
                if rad_msg_port in line:
                    a_list = line.split(rad_msg_port)
                    t.log(a_list)

                    list1 = a_list[1]
                    port_list = list1.split(",")
                    t.log(port_list)

                    dut_port = port_list[0]
                    dut_port = int(dut_port)
                    t.log("Port Number: ")
                    t.log(dut_port)
                    result = True
                    rad_msg = "Received Access-Request packet from host "+deviceip+" port "+str(dut_port)+", id="
                    t.log(rad_msg)
                    return result
                    break

        #rad_msg = "Received Access-Request packet from host "+deviceip+" port "+str(dut_port)+", id="
        #t.log(rad_msg)

            file = open('mschap.log', "r")
            file_list = file.readlines()
            file.close()
            for line in file_list:
                if rad_msg in line:
                    a_list = line.split(rad_msg)
                    t.log(a_list)
                    list1 = a_list[1]
                    id_list = list1.split(",")
                    t.log(id_list)
                    dut_id = id_list[0]
                    dut_id = int(dut_id)
                    t.log(dut_id)
                    result = True
                    return result
                    break

            rad_acctmsg = "Received Accounting-Request packet from host "+deviceip+" port "
            t.log(rad_acctmsg)
            file = open('mschap.log', "r")
            file_port = file.readlines()
            file.close()

            for line in file_port:
                if rad_msg_port in line:
                    a_list = line.split(rad_msg_port)
                    t.log(a_list)

                    list1 = a_list[1]
                    port_list = list1.split(",")
                    t.log(port_list)

                    dut_port = port_list[0]
                    dut_port = int(dut_port)
                    t.log("Port Number: ")
                    t.log(dut_port)
                    result = True
                    rad_acctmsg = "Received Accounting-Request packet from host "+deviceip+" port "+str(dut_port)+", id="
                    t.log(rad_acctmsg)
                    return result
                    break

            file = open('mschap.log', "r")
            file_list = file.readlines()
            file.close()
            for line in file_list:
                if rad_acctmsg in line:
                    a_list = line.split(rad_acctmsg)
                    t.log(a_list)
                    list1 = a_list[1]
                    id_list = list1.split(",")
                    t.log(id_list)
                    dut_id = id_list[0]
                    dut_id = int(dut_id)
                    t.log(dut_id)
                    result = True
                    return result
                    break


            str1 = rad_msg+str(dut_id)
            send_msg = "Sending Access-Challenge packet to host "+deviceip+" port "+str(dut_port)+", id="
            str2 = send_msg+str(dut_id)
            rad_acctmsg = "Received Accounting-Request packet from host "+deviceip+" port "+str(dut_port)+", id="
            str3 = rad_acctmsg+str(dut_id)
            t.log(str1)
            t.log(str2)
            t.log(str3)
            req_pkt = 0
            chl_pkt = 0
            acpt_pkt = 0
            acct_pkt = 0
            
            for i in range(0, 8):
                str1 = rad_msg+str(dut_id+i)
                str2 = send_msg+str(dut_id+i)
                str3 = rad_acctmsg+str(dut_id+i)
                for line in file_list:
                    if str1 in line:
                        t.log("Radius message is present in str1 : ")
                        req_pkt = req_pkt + 1
                    elif str2 in line:
                        t.log("Radius message is present in str2 : ")
                        chl_pkt = chl_pkt + 1
                    elif str3 in line:
                        t.log("Radius message is present in str3 : ")
                        acct_pkt = acct_pkt + 1

            str1 = rad_msg+str(dut_id+8)
            send_msg1 = "Sending Access-Accept packet to host "+deviceip+" port "+str(dut_port)+", id="
            str2 = send_msg1+str(dut_id+8)

            for line in file_list:
                if str1 in line:
                    t.log("Radius message is present in str1 : ")
                    req_pkt = req_pkt + 1
                elif str2 in line:
                    t.log("Radius message is present in str2 : ")
                    acpt_pkt = acpt_pkt + 1

            tlv_check = 0
            t.log("TLVS........")
            t.log(tlv_list)
            for line in file_list:
                for tlv in tlv_list:
                    if tlv in line:
                        tlv_check = tlv_check + 1
                        t.log(tlv)
            if proto_type == "eap-peap":
                if (req_pkt != 9)|(chl_pkt != 8)|(acpt_pkt != 1)|(acct_pkt != 1)|(tlv_check != len(tlv_list)):
                    t.log("tlv verification is not successful with EAP-PEAP Protocol")
                    result = False
                else:
                    t.log("tlv verification is successful with EAP-PEAP Protocol")
                    result = True
            elif proto_type == "pap":
                if tlv_check >= len(tlv_list):
                    t.log("tlv verification is successful with PAP Protocol")
                    result = True
                else:
                    t.log("tlv verification is not successful with PAP Protocol")
                    result = False
            else:
                t.log('Supplied Protocol Type is not supported ')
                result = False
            return result


        if accounting_on == "diffserver":
            rad_acctmsg_port = "Received Accounting-Request packet from host "+deviceip+" port "
            t.log(rad_acctmsg_port)
            file = open('mschap.log', "r")
            file_port = file.readlines()
            file.close()

            for line in file_port:
                if rad_acctmsg_port in line:
                    a_list = line.split(rad_acctmsg_port)
                    t.log(a_list)

                    list1 = a_list[1]
                    port_list = list1.split(",")
                    t.log(port_list)

                    dut_port = port_list[0]
                    dut_port = int(dut_port)
                    t.log("Port Number: ")
                    t.log(dut_port)
                    result = True
                    rad_acctmsg = "Received Accounting-Request packet from host "+deviceip+" port "+str(dut_port)+", id="
                    t.log(rad_acctmsg)
                    return result
                    break

            file = open('mschap.log', "r")
            file_list = file.readlines()
            file.close()
            for line in file_list:
                if rad_acctmsg in line:
                    a_list = line.split(rad_acctmsg)
                    t.log(a_list)
                    list1 = a_list[1]
                    id_list = list1.split(",")
                    t.log(id_list)
                    dut_id = id_list[0]
                    dut_id = int(dut_id)
                    t.log(dut_id)
                    result = True
                    return result
                    break
            rad_acctmsg = "Received Accounting-Request packet from host "+deviceip+" port "+str(dut_port)+", id="
            str3 = rad_acctmsg+str(dut_id)
            t.log(str3)
            acct_pkt = 0

            for i in range(0, 8):
                str3 = rad_acctmsg+str(dut_id+i)
                for line in file_list:
                    if str3 in line:
                        t.log("Radius message is present in str3 : ")
                        acct_pkt = acct_pkt + 1

            tlv_check = 0
            t.log("TLVS........")
            t.log(tlv_list)
            for line in file_list:
                for tlv in tlv_list:
                    if tlv in line:
                        tlv_check = tlv_check + 1
                        t.log(tlv)
            if proto_type == "eap-peap":
                if (acct_pkt != 1)|(tlv_check != len(tlv_list)):
                    t.log("tlv verification is not successful with EAP-PEAP Protocol")
                    result = False
                else:
                    t.log("tlv verification is successful with EAP-PEAP Protocol")
                    result = True
            elif proto_type == "pap":
                if tlv_check >= len(tlv_list):
                    t.log("tlv verification is successful with PAP Protocol")
                    result = True
                else:
                    t.log("tlv verification is not successful with PAP Protocol")
                    result = False
        else:
            t.log('Supplied Protocol Type is not supported ')
            result = False
        return result


    @staticmethod
    def send_coa_dm(tag, hostip, username, password, nasip, secret, radiustype, filepath, attr_list, prot, nak):
        """Generate Coa or Disconnect From  freeradius server

        :return:
            True if Radius coa/disconnect generation successful on the server
            False otherwise
        """

    ################ Generate COA ######################
        if radiustype == "coa":
            t.log("Cleanup Existing output and coa files")
            targetfilename = 'output.txt'
            targetfilename1 = 'coa'

            if os.path.exists(targetfilename) & os.path.exists(targetfilename1):
                try:
                    os.remove(targetfilename)
                    os.remove(targetfilename1)
                    t.log("Cleanup of Files are Successful\n")
                except:
                    t.log("Error: Removing Target Files")
            else:
                t.log("Sorry, I can not find file targetfilename")
                t.log("Sorry, I can not find file targetfilename1")

            if prot == "ipv4":
                t.log("inside def")
                device = t.get_handle(resource=tag)
                if device is None:
                    return False
                t.log("Changing Directory Path:\n")
                response = device.shell(command="cd " + filepath)
                t.log("Sending CoA Message for IPV4 Session:\n")
                response = device.shell(command="cat coa | radclient -x " +str(nasip)+":3799 coa " + str(secret) +" > output.txt")
                time.sleep(40)
                stdout = response.response()
                t.log("Printing Command Output: ")
                t.log(stdout)
                result = True
                time.sleep(2)
            elif prot == "ipv6":
                t.log("inside def")
                device = t.get_handle(resource=tag)
                if device is None:
                    return False
                t.log("Changing Directory Path:\n")
                response = device.shell(command="cd " + filepath)
                t.log("Sending CoA Message for IPV6 Session:\n")
                response = device.shell(command="cat coa | radclient -6 -x  ["+str(nasip)+"]:3799 coa " + str(secret) +" > output.txt")
                time.sleep(40)
                stdout = response.response()
                t.log("Printing Command Output: ")
                t.log(stdout)
                result = True
                time.sleep(2)

            # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))
            # Auth
            t.log("Yet to Authenticate")
            transport.connect(username=username, password=password)
            # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)
            # Download
            localpath = 'output.txt'
            sftp.get(os.path.join(filepath, localpath), localpath)
            # Close
            sftp.close()
            transport.close()
            result = "True"
            if nak == "yes":
                attr_check = 0
                t.log("Attributes Values........")
                t.log(attr_list)
                with open('output.txt', 'r') as fp_file:
                    for line in fp_file:
                        for attr in attr_list:
                            if attr in line:
                                attr_check = attr_check + 1
                                result = True
                if attr_check != len(attr_list):
                    t.log("CoA send is not as Expected !!")
                    result = False
                else:
                    t.log("CoA send is as Expected and Matched Successfully!!")
                    result = True
                return result
            elif nak == "no":
                attr_check = 0
                t.log("Attributes Values........")
                t.log(attr_list)
                with open('output.txt', 'r') as fp_file:
                    for line in fp_file:
                        for attr in attr_list:
                            if attr in line:
                                attr_check = attr_check + 1
                                result = True
                    #if (attr_check != 3*len(attr_list)):
                t.log("Attribute Check Value:")
                t.log(attr_check)
                t.log("Atribute List Length :")
                temp = len(attr_list)
                t.log(temp)
                if attr_check != len(attr_list):
                    t.log("CoA send is not as Expected !!")
                    result = False
                else:
                    t.log("CoA send is as Expected and Matched Successfully!!")
                    result = True
                return result
            else:
                t.log("Error sending CoA")

        ################ Generate Disconnect Message ######################
        elif radiustype == "disconnect":
            t.log("Cleanup Existing output and coa files")
            targetfilename = 'output.txt'
            targetfilename1 = 'coa'
            if os.path.exists(targetfilename) & os.path.exists(targetfilename1):
                try:
                    os.remove(targetfilename)
                    os.remove(targetfilename1)
                    t.log("Cleanup of Files are Successful\n")
                except:
                    t.log("Error: Removing Target Files")
            else:
                t.log("Sorry, I can not find file targetfilename")
            if prot == "ipv4":
                t.log("inside def")
                device = t.get_handle(resource=tag)
                if device is None:
                    return False
                t.log("Changing Directory Path:\n")
                response = device.shell(command="cd " + filepath)
                t.log("Sending Disconnect Message for IPV4 Session:\n")
                response = device.shell(command="cat coa | radclient -x " +str(nasip)+":3799 disconnect " + str(secret) +" > output.txt")
                time.sleep(40)
                stdout = response.response()
                t.log("Printing Command Output: ")
                t.log(stdout)
                result = True
                time.sleep(2)
            elif prot == "ipv6":
                t.log("inside def")
                device = t.get_handle(resource=tag)
                if device is None:
                    return False
                t.log("Changing Directory Path:\n")
                response = device.shell(command="cd " + filepath)
                t.log("Sending Disconnect Message for IPV6 Session:\n")
                response = device.shell(command="cat coa | radclient -6 -x  ["+str(nasip)+"]:3799 disconnect " + str(secret) +" > output.txt")    
                time.sleep(40)
                stdout = response.response()
                t.log("Printing Command Output: ")
                t.log(stdout)
                result = True
                time.sleep(2)

            # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))
            # Auth
            t.log("Yet to Authenticate")
            transport.connect(username=username, password=password)
            # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)
            # Download
            localpath = 'output.txt'
            sftp.get(os.path.join(filepath, localpath), localpath)
            # Close
            sftp.close()
            transport.close()
            result = "True"
            if nak == "yes":
                attr_check = 0
                t.log("Attributes Values........")
                t.log(attr_list)
                with open('output.txt', 'r') as fp_file:
                    for line in fp_file:
                        for attr in attr_list:
                            if attr in line:
                                attr_check = attr_check + 1
                                result = True
                t.log("Attribute Check Value:")
                t.log(attr_check)
                t.log("Atribute List Length :")
                temp = len(attr_list)
                t.log(temp)
                if attr_check != len(attr_list):
                    t.log("Disconnect Message send is not as Expected !!")
                    result = False
                else:
                    t.log("Disconnect Message send is as Expected and Matched Successfully!!")
                    result = True
                return result
            elif nak == "no":
                attr_check = 0
                t.log("Attributes Values........")
                t.log(attr_list)
                with open('output.txt', 'r') as fp_file:
                    for line in fp_file:
                        for attr in attr_list:
                            if attr in line:
                                attr_check = attr_check + 1
                                result = True
                t.log("Attribute Check Value:")
                t.log(attr_check)
                t.log("Atribute List Length :")
                temp = len(attr_list)
                t.log(temp)

                if attr_check != len(attr_list):
                    t.log("Disconnect Message send is not as Expected !!")
                    result = False
                else:
                    t.log("Disconnect Message send is as Expected and Matched Successfully!!")
                    result = True
                return result
            elif nak == "na":
                attr_check = 0
                t.log("Attributes Values........")
                t.log(attr_list)
                with open('output.txt', 'r') as fp_file:
                    for line in fp_file:
                        for attr in attr_list:
                            if attr in line:
                                attr_check = attr_check + 1
                                result = True
                t.log("Attribute Check Value:")
                t.log(attr_check)
                t.log("Atribute List Length :")
                temp = len(attr_list)
                t.log(temp)
                if attr_check != len(attr_list):
                    t.log("Disconnect Message send is not as Expected !!")
                    result = False
                else:
                    t.log("Disconnect Message send is as Expected and Matched Successfully!!")
                    result = True
                return result
            else:
                t.log("Error sending CoA")

    @staticmethod
    def config_eth_ipaddr(tag, ethernet, addrtype, ipaddr):
        """Configuring ethernet ipv4/ipv6 address on freeradius server

        :return:
            True if configuration of ipv4/ipv6 is successful on the server
            False otherwise
        """
        result = True
        t.log("inside def")
        device = t.get_handle(resource=tag)
        if device is None:
            return False
        if addrtype == "ipv6":
            response = device.shell(command="ifconfig " +str(ethernet)+ " | grep inet6")
            stdout = response.response()
            t.log("Printing Command Output IPv6: ")
            t.log(stdout)
            result = False
            ipv6str = 'inet6'
            for output in stdout.splitlines():
                if ipv6str in output:
                    response = device.shell(command="ifconfig " +str(ethernet)+ " down")
                    response = device.shell(command="ifconfig " +str(ethernet)+ " up")
                    response = device.shell(command="ifconfig " +str(ethernet)+ " inet6 add " +(ipaddr))
                    stdout = response.response()
                    t.log("Printing IPV6 Command Output :\n")
                    t.log(stdout)
                    result = True
                    break
                else:
                    response = device.shell(command="ifconfig " +str(ethernet)+ " inet6 add " +(ipaddr))
                    stdout = response.response()
                    t.log("Printing IPV6 Command Output :\n")
                    t.log(stdout)
                    result = True
        elif addrtype == "ipv4":
            response = device.shell(command="ifconfig " +str(ethernet)+ " | grep inet")
            stdout = response.response()
            t.log("Printing Command Output for IPv4: ")
            t.log(stdout)
            result = False
            ipv4str = 'inet addr'
            for output in stdout.splitlines():
                if ipv4str in output:
                    response = device.shell(command="ifconfig " +str(ethernet)+ " down")
                    response = device.shell(command="ifconfig " +str(ethernet)+ " up")
                    response = device.shell(command="ifconfig " +str(ethernet) +" "+(ipaddr))
                    stdout = response.response()
                    t.log("Printing IPV4 Command Output :\n")
                    t.log(stdout)
                    result = True
                    break
                else:
                    response = device.shell(command="ifconfig " +str(ethernet) +" "+(ipaddr))
                    stdout = response.response()
                    t.log("Printing IPV4 Command Output :\n")
                    t.log(stdout)
                    result = True
        else:
            t.log("Ipv4/IPv6 ethernet IP can't be configured!! Please Enter correct data")
            result = False
        return result


    @staticmethod
    def get_st_id(hostip, username, password, value, radius_logpath):
        """Getting Session ID's for Access Accounting from freeradius server

        :return:
            True if Getting Session ID's for Access Accounting successful on the server
            False otherwise
        """
        t.log(" *********************\n")
        t.log("Fetch Values User-Name, Acct-Session-Id, Called-Station-Id & Calling-Station-Id\n")
        t.log(" **********************\n")
        # Open a transport
        host = hostip
        port = 22
        transport = paramiko.Transport((host, port))
        # Auth
        t.log("Yet to Authenticate")
        transport.connect(username=username, password=password)
        # Go!
        t.log("Yet to open SFTPClient")
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Download
        filepath1 = radius_logpath+'mschap.log'
        localpath1 = 'mschap.log'
        sftp.get(filepath1, localpath1)
        sftp.close()
        transport.close()
        if os.stat("mschap.log").st_size == 0:
            t.log("mschap.log is EMPTY")
            return False
        rad_msg_called = 'Called-Station-Id = "'
        rad_msg_calling = 'Calling-Station-Id = "'
        rad_msg_acct = 'Acct-Session-Id = "'
        file = open('mschap.log', "r")
        file_port = file.readlines()
        file.close()
        # Fetching Value for Called-Station-Id
        if value == "called":
            for line in file_port:
                if rad_msg_called in line:
                    a_list = line.split(rad_msg_called)
                    t.log(a_list)
                    list1 = a_list[1]
                    port_list = list1.split('"')
                    t.log(port_list)
                    dut_called = port_list[0]
                    t.log("Called Station ID: ")
                    t.log(dut_called)
                    Vars().set_global_variable("${V2}", dut_called)
                    result = True
                    break

        # Fetching Value for Calling-Station-Id
        if value == "calling":
            for line in file_port:
                if rad_msg_calling in line:
                    a_list = line.split(rad_msg_calling)
                    t.log(a_list)
                    list1 = a_list[1]
                    port_list = list1.split('"')
                    t.log(port_list)
                    dut_calling = port_list[0]
                    t.log("Calling Station ID: ")
                    t.log(dut_calling)
                    Vars().set_global_variable("${V3}", dut_calling)
                    result = True
                    break

        # Fetching Value for Acct-Session-Id
        if value == "acct":
            for line in file_port:
                if rad_msg_acct in line:
                    a_list = line.split(rad_msg_acct)
                    t.log(a_list)
                    list1 = a_list[1]
                    port_list = list1.split('"')
                    t.log(port_list)
                    dut_acct = port_list[0]
                    t.log("Acct Session ID: ")
                    t.log(dut_acct)
                    Vars().set_global_variable("${V4}", dut_acct)
                    result = True
                    break
        return result

    @staticmethod
    def restart_services(tag, servicename):
        """Restart any service on freeradius server

        :return:
            True if restarting service successful on the server
            False otherwise
        """
        result = True
        t.log("inside def")
        device = t.get_handle(resource=tag)
        if device is None:
            return False
        response = device.shell(command="service " +str(servicename)+ " restart")
        stdout = response.response()
        t.log("Service " +str(servicename) +" Restarted Successfully")
        result = True
        return result

    @staticmethod
    def add_cp_user(hostip, username, password, user_data, filepath, filename):
        """Add captive portal Users for Authentications and generationg Coa on freeradius server

        :return:
            True if Radius user/coa addition successful on the server
            False otherwise
        """
        # Download
        with open(filename, "w+") as file:
            file.write(user_data)
            file.close()
        # Open a transport
        host = hostip
        port = 22
        transport = paramiko.Transport((host, port))
        # Auth
        t.log("Yet to Authenticate")
        transport.connect(username=username, password=password)
        # Go!
        t.log("Yet to open SFTPClient")
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Upload
        localpath = filename
        sftp.put(localpath, os.path.join(filepath, localpath))
        # Close
        sftp.close()
        transport.close()
        result = True
        if result is True:
            t.log("Captive Portal files creation update is successful\n!!")
        else:
            t.log("Captive Portal files creation and update failed!!")
            result = False
        return result


    @staticmethod
    def authentication_user(username_vm, password_vm, username, password , url , filepath, filename, vm_name):
        """ This function will verify CWA for provided client user
            The function excepts redirect url preconfigured username/password for a client
            : return True: If the client is successfully authenticated
                   False: If any exception is raised
        """
        t.log(" *********************\n")
        t.log(" ************* AUTHENTICATING ************\n")
        t.log(" *********************\n")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=vm_name, username=username_vm, password=password_vm)
            sftp=ssh.open_sftp()
            try:
                sftp.chdir(filepath)
                command='python3 '+filepath+'/'+filename+' --username '+username+' --password '+password+' --url '+url
                t.log(command)
                stdin, stdout, stderr = ssh.exec_command(command)
                cmd_out = stdout.readlines()
                for line in cmd_out:
                     t.log(line)
                     if 'False' in line:
                         return False
                return True
            except IOError:
                t.log("check the file path")
                return False

            ssh.close()
        except paramiko.SSHException:
             t.log("Connection Error ")
             return False



    @staticmethod
    def send_verify_cp(tag, hostip, username, password, clientuser, clientpasswd, complete_url, attr_value):
        """Send and Verify captive portal Users for Authentications and generationg various status on host

        :return:
            True if Send and Verify captive portal Users  successful on the server
            False otherwise
        """
        t.log("Cleanup Existing cpoutput files")
        targetfilename = "cpoutput.txt"

        if os.path.exists(targetfilename):
            try:
                os.remove(targetfilename)
                t.log("Cleanup of Files are Successful\n")
            except:
                t.log("Error: File can't be cleaned\n")
        else:
            t.log("Sorry, I can not find file targetfilename")

        if clientuser == "no":
            t.log("inside def")
            device = t.get_handle(resource=tag)
            if device is None:
                return False
            t.log("Sending Curl command for Captive Portal Session without user:\n")
            #response = device.shell(command="curl "  +str(complete_url) +" > cpoutput.txt", pattern='~]# ', timeout=10)
            response = device.shell(command="curl "  +str(complete_url) +" > cpoutput.txt")
            time.sleep(40)
            stdout = response.response()
            t.log("Printing Command Output: ")
            t.log(stdout)
            result = True
            time.sleep(2)
            # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))

            # Auth
            t.log("Yet to Authenticate")
            transport.connect(username=username, password=password)
            # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Download
            localpath = 'cpoutput.txt'
            sftp.get(localpath, localpath)

            # Close
            sftp.close()
            transport.close()
        else:
            t.log("inside def")
            device = t.get_handle(resource=tag)
            if device is None:
                return False
            t.log("Sending Curl command for Captive Portal Session without user:\n")
            #response = device.shell(command="curl --data 'username=" +str(clientuser)+"&" + "password=" +str(clientpasswd) +"' " +str(complete_url) +" > cpoutput.txt", pattern='~]# ', timeout=10)
            response = device.shell(command="curl --data 'username=" +str(clientuser)+"&" + "password=" +str(clientpasswd) +"' " +str(complete_url) +" > cpoutput.txt")
            time.sleep(40)
            stdout = response.response()
            t.log("Printing Command Output: ")
            t.log(stdout)
            result = True
            time.sleep(2)
            # Open a transport
            host = hostip
            port = 22
            transport = paramiko.Transport((host, port))

            # Auth
            t.log("Yet to Authenticate")
            transport.connect(username=username, password=password)

            # Go!
            t.log("Yet to open SFTPClient")
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Download
            localpath = 'cpoutput.txt'
            sftp.get(localpath, localpath)

            # Close
            sftp.close()
            transport.close()


        if os.stat("cpoutput.txt").st_size == 0:
            t.log("cpoutput.txt is EMPTY")
            return False

        attr_check = 0
        t.log("Attributes Values........")
        t.log(attr_value)
        with open('cpoutput.txt', 'r') as fp_file:
            for line in fp_file:
                if attr_value in line:
                    result = True
        if result == False:
            t.log("Captive Portal Match is not as Expected !!")
            result = False
        else:
            t.log("Captive Portal is as Expected and Matched Successfully!!")
            result = True
        return result
    
    @staticmethod
    def check_wpa_supplicant(tag):
        """check if any wpa_supplicant installed on freeradius server

        :return:
            True if wpa_supplicant -v command returns version installed
            False otherwise
        """
        result = True
        t.log("inside def")
        device = t.get_handle(resource=tag)
        if device is None:
            return False
        response = device.shell(command="wpa_supplicant -v")
        stdout = response.response()
        t.log("wpa_supplicant output: %s" % stdout)
        
        for i in stdout.splitlines():
            if re.search("wpa_supplicant v\d+\.\d+",i):
               result = True
               break
            else:
               result = False
        if result:
            t.log("wpa_supplicant installed ")
        else:
            t.log("wpa_supplicant not installed")
        return result  
        
        
    @staticmethod
    def accounting_keyword(filename, ip, request_type, attribute, value):
        contents = ""
        with open(filename,"r" ,encoding='utf-8',errors='ignore') as f:
             for line in f.readlines():
                 contents += line
        reg_value = re.search("(%s).*((.|\n))*(%s:\s)(.*)"%(request_type,attribute),contents)
        macvalue = re.search("Src:\s%s"%(ip),contents)
#        macvalue = re.search("Src:(.*)(\(%s)\)"%(mac_address),contents)
        if reg_value and macvalue:
            attribute_value=reg_value.group(5)
            print("DEBUG:attribute in packet capture:%s"%attribute_value)
            if attribute_value==value:
                  return True
            else:
                  print("DEBUG:attribute in packet capture:%s"%attribute_value)
                  return False      
        else:
            return False
        
    @staticmethod
    def verify_wpa_supplicant(tag, hostip, username, password, radius_user, radius_pwd, filepath_wpa, eth_interface):
        """Checking for any wpa_supplicant available on freeradius server

        :return:
            True if restarting service successful on the server
            False otherwise
        """        
        # Open a transport
        host = hostip
        port = 22
        transport = paramiko.Transport((host, port))
        result = True
        # Auth
        t.log("Yet to Authenticate")
        transport.connect(username=username, password=password)
        # Go!
        t.log("Yet to open SFTPClient")
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Download
        localpath = 'wpa_supplicant.conf' 
        filepath = '/etc/wpa_supplicant/wpa_supplicant.conf'
        fw = open(localpath, "w+")
        wpa_conf = "\
ctrl_interface=/var/run/wpa_supplicant\n\
ctrl_interface_group=wheel\n\
network={\n\
        key_mgmt=IEEE8021X\n\
        eap=TTLS MD5\n\
        identity=\"%s\"\n\
        anonymous_identity=\"%s\"\n\
        password=\"%s\"\n\
        phase1=\"auth=MD5\"\n\
        eapol_flags=0\n\
}\
" % (radius_user, radius_user, radius_pwd)
        fw.write(wpa_conf)
        fw.close()
        sftp.put(localpath, filepath)
        # wpa_supplicant run using handle
        t.log("inside def")
        device = t.get_handle(resource=tag)
        if device is None:
            return False
        delResponse = device.shell(command="rm -f wpa_supplicant.log")
        response = device.shell(command="sudo wpa_supplicant -c "+str(filepath_wpa)+ "  -D wired -i "+ str(eth_interface)+ " -B -f wpa_supplicant.log")
        stdout = response.response()
        t.log("wpa_supplicant output: %s" % stdout)
        time.sleep(20)
        response_kill = device.shell(command="pkill wpa_supplicant")
        logpath = "wpa_supplicant.log"
        loglocalpath = "wpa_supplicant.log"
        sftp.get(logpath, loglocalpath)
        flog = open(loglocalpath,'r')
        #flog_lines = flog.readlines()
        #t.log("log output:%s" % flog_lines)
        t.log("1:%s" % result)
        for i in flog.readlines():
            t.log("line in file: %s" % i)
            if re.search("Successfully initialized wpa_supplicant",i):
               result = True
               break
            else:
               result = False
        t.log("2:%s" % result)
        if result:
            t.log("Client successfully authenticated with wpa_supplicant")
        else:
            t.log("Client authentication failed")
        return result
        
    @staticmethod
    def userfilebackup_keyword(tag, hostip, username, password, filepath, option):
        """Checking for any wpa_supplicant available on freeradius server

        :return:
            True if restarting service successful on the server
            False otherwise
        """
        t.log("Entered userfilebackup")
        device = t.get_handle(resource=tag)
        if device is None:
            return False
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostip, username=username, password=password)
            sftp = ssh.open_sftp()
            src = filepath+"users"
            sftp.chdir(filepath)
            target = filepath+"users_backup"
            auth = filepath+"mods-config/files/authorize"
            if option == "backup":
                if sftp.stat(src):
                    t.log("inside backup")
                    mv_command = '\cp '+src+' '+target
                    stdin, stdout, stderr = ssh.exec_command(mv_command)
                    t.log("Backup Successful")
                    sftp.chdir(filepath)
                    t.log("Entering list dir")
                    command = 'truncate -s 0 '+ src
                    t.log("command %s" % command)
                    stdin, stdout, stderr = ssh.exec_command(command)
                    t.log("stdin - %s, stdout - %s, stderr - %s" % (stdin,stdout.readlines(),stderr.readlines()))
                else:
                    t.log("Source File %s doesn't exist" % src)
            if option == "restore":
                print("target is %s" % target)
                print("src is %s" % src)
                if sftp.stat(target):
                    cp_command = '\cp '+target+' '+src
                    stdin, stdout, stderr = ssh.exec_command(cp_command)
                    t.log("stdin - %s, stdout - %s, stderr - %s" % (stdin,stdout.readlines(),stderr.readlines()))
                    t.log("Restore Successful")
                    sftp.remove(target)
                else:
                    t.log("Backup File %s doesn't exist" % target)
            ssh.close()
            return True   
