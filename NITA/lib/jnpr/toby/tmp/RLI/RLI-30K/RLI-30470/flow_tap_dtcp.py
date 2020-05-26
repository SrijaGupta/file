import re
import getpass
import sys
import hmac
import hashlib
import os
import time
import ipaddress
import paramiko
import socket
from ipaddress import IPv4Address, IPv4Network, IPv4Interface

sequence_number = 1


class flow_tap_dtcp():
      """
      Class for FLOWTAP DTCP Requests
      Supports ADD,DELETE & LIST Filter requests 

      """
      def dtcp_add_filter(self,**kwargs):
       
          """
          Method constructs ADD request based on user input parametrs and sends it to the DUT

          :param filter_type:
            **REQUIRED**     Should specify if the filter is [global/ccc_in/ccc_out/v4_in/v4_out/v6_in/v6_out/vrf]
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
          :param intf_vrf_multiple_flag:
            **OPTIONAL**     Indication as on whether multiple interfaces or multiple vrfs need to be send in the DTCP request. Value can be 0 ( multiple interfaces - needs to be a multiple of 8) and value can be 1 ( which means multiple vrf's)
          :param ttl:
            **OPTIONAL**     TTL of packet 
          :param router:
            **REQUIRED**     Router name to which DTCP ADD request should be sent 
          :return      :       Returns True if dtcp message returned is 1 else False

          Usage        :     dtcp_add_filter(version="0.8",ttl=255,router="esst480s",src_addr="20.20.20.1",dst_addr="30.30.30.1",src_port=1000,dst_port=2000,filter_type="ccc_in",num_filt=1,src_step=1,csource_id="ftap1",cdest1_id="cd1",protocol=17,csource_addr="208.223.208.9",cdest1_addr="212.25.99.81",cdest1_port=8001,intf="ge-1/3/5.0")

          """
        
          ip_src = 0
          ip_dst = 0
          router = kwargs['router']
          filter_type = ""
          csource_port  = 49153
          filters = int(kwargs['num_filt'])
          counter1 = int(0)
          sr = ''
          version = 0.7
          if('version' in kwargs) : version = kwargs['version']

          #If src_addr parameter is passed ipaddress module creates object from string 
          if('src_addr' in kwargs):
             if("*" in kwargs['src_addr']):
                  src_addr = "*"
             elif("/" in kwargs['src_addr']):
                  src_addr = ipaddress.ip_network(kwargs['src_addr'])
             else:
                  src_addr = ipaddress.ip_address(kwargs['src_addr'])

          #If dst_addr parameter is passed ipaddress module creates object from string   
          if('dst_addr' in kwargs):
             if("*" in kwargs['dst_addr']):
                  dst_addr = "*"
             elif("/" in kwargs['dst_addr']):
                  dst_addr = ipaddress.ip_network(kwargs['dst_addr'])
             else:
                  dst_addr = ipaddress.ip_address(kwargs['dst_addr'])

          #If filter_type parameter is ccc_in/v4_in/v6_in below tag will be added 
	  #In ADD request appending with intf parameter 
          if("in" in kwargs['filter_type']):
             filter_type = "X-JTap-Input-Interface"
          
          #If filter_type parameter is ccc_out/v4_out/v6_out below tag will be added 
          #In ADD request appending with intf parameter 
          if("out" in  kwargs['filter_type']):
             filter_type = "X-JTap-Output-Interface"

          #If filter_type parameter is vrf below tag will be added In ADD request appending with intf parameter 
          if("vrf" in kwargs['filter_type']):
             filter_type = "X-JTap-VRF-Name"

          #If Content destinations cd1 & cd2 are passed as parameters they are formated as cd1,cd2 in the request 
          if('cdest2_id' in kwargs.keys() and 'cdest1_id' in kwargs.keys()):
                 cdest_id   = "{0},{1}".format(kwargs['cdest1_id'],kwargs['cdest2_id'])
                 cdest_addr = "{0},{1}".format(kwargs['cdest1_addr'],kwargs['cdest2_addr'])
                 cdest_port = "{0},{1}".format(kwargs['cdest1_port'],kwargs['cdest2_port']) 
          elif('cdest1_id' in kwargs.keys()):
                 cdest_id   = kwargs['cdest1_id']
                 cdest_addr = kwargs['cdest1_addr']
                 cdest_port = kwargs['cdest1_port']
          elif('cdest2_id' in kwargs.keys()):
                 cdest_id   = kwargs['cdest2_id']
                 cdest_addr = kwargs['cdest2_addr']
                 cdest_port = kwargs['cdest2_port'] 

          if 'csource_port' in kwargs.keys(): csource_port = kwargs['csource_port']
        
          #Below code constructs the ADD request depending on parameters passed
          #While loop executed till ADD requests for number of filters requested is sent
          while(filters >= 1):
              sr = "ADD DTCP/"+str(version)+"\n"
              sr += "Csource-ID: "+str(kwargs['csource_id'])+"\n"
              sr += "Cdest-ID: "+str(cdest_id)+"\n"
              if("ccc" not in kwargs['filter_type'] or "neg" in kwargs['filter_type']):
                 sr += "Source-Address: "+str(src_addr)+"\n"
                 sr += "Dest-Address: "+str(dst_addr)+"\n"
                 sr += "Source-Port: "+str(kwargs['src_port'])+"\n"
                 sr += "Dest-Port: "+str(kwargs['dst_port'])+"\n"
              sr += "Protocol: "+str(kwargs['protocol'])+"\n"
              sr += "Priority: 2\n"
              sr += "X-JTap-Cdest-Dest-Address: "+str(cdest_addr)+"\n"
              sr += "X-JTap-Cdest-Dest-Port: "+str(cdest_port)+"\n"
              sr += "X-JTap-Cdest-Source-Address: "+str(kwargs['csource_addr'])+"\n"
              sr += "X-JTap-Cdest-Source-Port: "+str(csource_port)+"\n"
              if('intf' in kwargs and "none" not in kwargs['intf'] and 'intf_vrf_multiple_flag' not in kwargs): sr += filter_type+": "+str(kwargs['intf'])+"\n"
              
              #Below code constructs the input interface filter for 8 ifls's in one shot

              if('intf_vrf_multiple_flag' in kwargs and "0" in kwargs['intf_vrf_multiple_flag']): sr += filter_type+": "+str(kwargs['intf'])+"."+str(counter1)+","+str(kwargs['intf'])+"."+str(counter1+1)+","+str(kwargs['intf'])+"."+str(counter1+2)+","+str(kwargs['intf'])+"."+str(counter1+3)+","+str(kwargs['intf'])+"."+str(counter1+4)+","+str(kwargs['intf'])+"."+str(counter1+5)+","+str(kwargs['intf'])+"."+str(counter1+6)+","+str(kwargs['intf'])+"."+str(counter1+7)+"\n"

              #Below code constructs the vrf filter for 1 vrf per DTCP request
              if('intf' in kwargs and "none" not in kwargs['intf'] and "vrf" in kwargs['filter_type'] and 'intf_vrf_multiple_flag' in kwargs and "1" in kwargs['intf_vrf_multiple_flag']): sr += filter_type+": "+str(kwargs['intf'])+"_"+str(counter1+1)+"\n"


              if("v6" in kwargs['filter_type']): sr += "X-JTap-IP-Version: ipv6\n"
              if("ccc" in kwargs['filter_type'] or "neg" in kwargs['filter_type']): sr += "X-Jtap-Filter-Family: ccc\n"
              sr += "X-JTap-Cdest-TTL: "+str(kwargs['ttl'])+"\n"
              sr += "Flags: STATIC\n"
              sr += "\n"

              #Increments the src addr if increment step(src_step) paramet is passed
              if('src_step' in kwargs):
                 src_step = kwargs['src_step']
                 if('src_addr' in kwargs):
                  if("*" not in kwargs['src_addr']):
                     src_addr = src_addr+src_step

              #Increments the dst addr if increment step(dst_step) paramet is passed
              if('dst_step' in kwargs):
                 ds_step = kwargs['dst_step']
                 if('dst_addr' in kwargs):
                  if("*" not in kwargs['dst_addr']):
                      dst_addr = dst_addr+dst_step
              
              #Writes the string generated above to a file appending with process ID 
              PID = os.getpid()
              P = open('/tmp/filter_add_'+router+'_'+str(PID),'w')
              P.write(sr)
              P.close()
          
              print("{}{}{}".format("File created with filter to ADD is ",'/tmp/filter.fil_'+router+'_'+str(PID),'\n'))

              #Hands the file to flow tap method to send it to DUT after SSH Authentication 
              if (counter1 == 0 ):
          #    router = args[0]
                user = kwargs['csource_id']
                password = str(kwargs['csource_id'])+"123"
                file_name = '/tmp/filter_add_'+router+'_'+str(PID)
                seq_num = 0
                opt_seq_num = 0
                seq_num_found_int_file = 0
                sequence_number = 0
                key = 'Juniper'
                digest = ""
                dtcp_cmd = ""
                opt_seq_num = 1

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                socket1.connect((router,32001))

                trans = paramiko.Transport(socket1)
                trans.connect(username=user, password=password)

                #CREATE CHANNEL FOR DATA COMM
                ch = trans.open_session()

                #Invoke flow-tap-dtcp Subsystem
                ch.invoke_subsystem('flow-tap-dtcp')

              resp_file = self._flow_tap(router, kwargs['csource_id'], str(kwargs['csource_id'])+"123", '/tmp/filter_add_'+router+'_'+str(PID), sequence_number,ch)
              if('intf_vrf_multiple_flag' in kwargs and "0" in kwargs['intf_vrf_multiple_flag']):
                 filters = filters-8
                 counter1 = counter1+8
              else:
                 filters = filters-1
                 counter1 = counter1+1

              #Sends the response to dtcp response method to validate the reply
              (resp_hash, dtcp_ok) = self._dtcp_response(resp_file)

              #Removes the files generated during ADD request and reply
              os.remove('/tmp/filter_add_'+router+'_'+str(PID))
              os.remove(resp_file)

          ch.close()
          trans.close()
          socket1.close()

          if(int(dtcp_ok) == 1):
             return True
          else:
            return False 


      def _flow_tap(self,*args):
          """
          Method  opens a ssh connection to the DUT and sends the DTCP request returns the DTCP response which is written into a file 

          """
          router = args[0]
          user = args[1]
          password = args[2]
          file_name = args[3]
          ch = args[5]
          seq_num = 0
          opt_seq_num = 0
          seq_num_found_int_file = 0
          sequence_number = 0
          key = 'Juniper'
          digest = ""
          dtcp_cmd = ""
          opt_seq_num = 1

#          ssh = paramiko.SSHClient()
#          ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       
#          socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#          socket1.connect((router,32001))
       
#          trans = paramiko.Transport(socket1)
#          trans.connect(username=user, password=password)
       
          #CREATE CHANNEL FOR DATA COMM
#          ch = trans.open_session()
       
          #Invoke flow-tap-dtcp Subsystem
#          ch.invoke_subsystem('flow-tap-dtcp')

          #Below code reads the lines in file and adds sequence number and Authentication-Info to the request 
          f = open(file_name,"r")
          lines = f.readlines()
          for line in lines:
            line = line.strip()
            if(line == ""):
             seq_num += 1
             if((opt_seq_num) or not(seq_num_found_int_file)):

                # Add DTCP Sequence number
                dtcp_cmd = dtcp_cmd+"Seq: "+str(seq_num)+'\r\n'

                # Code to caluclate hexdigest using hmac for the add request
                key = bytes(key, 'utf-8')
                msg = bytes(dtcp_cmd, 'utf-8')
                digest_maker = hmac.new(key,msg, hashlib.sha1)
                digest = digest_maker.hexdigest()
                dtcp_cmd = dtcp_cmd+"Authentication-Info: "+digest+'\r\n\r\n'

                print("Sending DTCP Command\n")
                print(dtcp_cmd)
                ch.send(dtcp_cmd)
                time.sleep(5)
                data = ch.recv(2048)
                data = data.decode("utf-8")
                print(data)
                PID = os.getpid()
                P = open('/tmp/filter_resp_'+router+'_'+str(PID),'w')
                P.write(data)
                P.close()
            else:
              if(line == "seq"):
                eq_num_found_int_file = 1;
                if(not(opt_seq_num)):
                   dtcp_cmd =  dtcp_cmd+strline+"\r\n"
              else:
                  dtcp_cmd =  dtcp_cmd+line+'\r\n'  
        
        #  ch.close()
        #  trans.close()
        #  socket1.close()

          return('/tmp/filter_resp_'+router+'_'+str(PID))

      def _dtcp_response(self,*args):
          """
          Method  returns the DTCP reply to the requested function
          """
          resp_hash = []
          pattern1 = [re.compile(p) for p in [r'^[ \t]*$','password','^Warning','^SEQ',r'^TIMESTAMP:.*','^DTCP','^AUTHENTICATION']]
          file_name = args[0]
          dtcp_ok = 0
          print("Converting the response in the response to a hash")
          time.sleep(10)
          #Below code reads the lines in response and checks for 200 OK 
          f = open(file_name,"r")
          lines = f.readlines()
          for line in lines:
            line = line.strip()
            if(line == ''):
               continue
            if(re.match('DTCP/\d.\d\s(\d+)\s(.*)',line)):
                m = re.match('DTCP/\d.\d\s(\d+)\s(.*)',line)
                value = m.group(1)
                resp_hash =  m.group(2)
                if(int(value) is 200):
                   print("DTCP 200 OK is received as expected")
                   dtcp_ok += 1
                else:
                   print("DTCP 200 OK is not received")
                del lines[:]
            for reg in pattern1:
                if(reg.match(line)):
                   break
            if(not re.match(r'[A-Z]',line)):
               continue
            elif(line == "Received disconnect"):
                 break

          #  out = line.split()
          #  resp_hash = out[1]
          # Returns dtcp_ok = 1 if 200 OK is recived else returns 0
          #print(resp_hash, dtcp_ok)
          return (resp_hash, dtcp_ok)

      def dtcp_list_filter(self,**kwargs):
          """
          Method  sends list request to DUT

          :param csource_id:
            **REQUIRED**     Control Source which is pre-configured/authorized by the router 
          :param cdest_id:
            **REQUIRED**     Content Destination name to which tapped packets should be sent
           usage         :   dtcp_list_filter(router="esst480s",csource_id="ftap1",id="cdest",id_val="cd1",flag="Criteria")
          """
          sr = ""
          router = kwargs['router']
          
          if (kwargs['id'] == 'cdest' ):
            sr =  "LIST DTCP/0.7\n"
            sr += "Csource-ID: "+str(kwargs['csource_id'])+"\n"
            sr += "CDest-ID: "+str(kwargs['id_val'])+"\n"
            sr += "Flags: "+str(kwargs['flag'])+"\n"
            sr += "\n"
          else:
            sr = "LIST DTCP/0.7\n"
            sr += "Csource-ID: "+str(kwargs['csource'])+"\n"
            sr += "Flags:  "+str(kwargs['flags'])+"\n"
            sr += "\n"
          
          #Writes the string generated above to a file appending with process ID
          PID = os.getpid()
          P = open('/tmp/filter_list_'+router+'_'+str(PID),'w')
          P.write(sr)
          P.close()



          user = kwargs['csource_id']
          password = str(kwargs['csource_id'])+"123"
          file_name = '/tmp/filter_add_'+router+'_'+str(PID)
          seq_num = 0
          opt_seq_num = 0
          seq_num_found_int_file = 0
          sequence_number = 0
          key = 'Juniper'
          digest = ""
          dtcp_cmd = ""
          opt_seq_num = 1

          ssh = paramiko.SSHClient()
          ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

          socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          socket1.connect((router,32001))

          trans = paramiko.Transport(socket1)
          trans.connect(username=user, password=password)

          #CREATE CHANNEL FOR DATA COMM
          ch = trans.open_session()

          #Invoke flow-tap-dtcp Subsystem
          ch.invoke_subsystem('flow-tap-dtcp')


         
          #Hands the file to flow tap method to send it to DUT after SSH Authentication 
          resp_file = self._flow_tap(router, kwargs['csource_id'], str(kwargs['csource_id'])+"123", '/tmp/filter_list_'+router+'_'+str(PID), sequence_number,ch)
           
          #Sends the response to dtcp response method to validate the reply
          (resp_hash, dtcp_ok) = self._dtcp_response(resp_file)
          
          #Removes the files generated during LIST equest and reply
          os.remove('/tmp/filter_list_'+router+'_'+str(PID))
          os.remove(resp_file)
          ch.close()
          trans.close()
          socket1.close()
          if(int(dtcp_ok) == 1):
             return True
          else:
            return False   

      def dtcp_delete_filter(self,**kwargs):
          """
          Method  sends delete request to DUT
          :param csource_id:
            **REQUIRED**     Control Source which is pre-configured/authorized by the router 
          :param cdest1_id:
            **REQUIRED**     Content Destination name to which tapped packets should be sent 
          :param Criteria-ID:   
             *Optional*      Criteria ID of the request
          :Usage         :   dtcp_delete_filter(router="esst480s",csource_id="ftap1",id="cdest",id_val="cd1")
          """

          router = kwargs['router']
          sr = ""

          print("Check to create and send the delete filter");
          resp_hash = 0
          dtcp_ok   = 0

          if (kwargs['id'] == "cdest" ):
            sr  = "DELETE DTCP/0.7\n"
            sr += "Csource-ID: "+str(kwargs['csource_id'])+"\n"
            sr += "CDest-ID: "+str(kwargs['id_val'])+"\n"
            sr += "Flags: STATIC\n"
            sr += "\n"
          else:
            sr = "DELETE DTCP/0.7\n"
            sr += "Csource-ID: "+str(kwargs['csource_id'])+"\n"
            sr += "Criteria-ID: "+str(kwargs['id_val'])+"\n"
            sr += "Flags: STATIC\n"
            sr += "\n"
          
          #Writes the string generated above to a file appending with process ID 
          PID = os.getpid()
          P = open('/tmp/filter_del_'+router+'_'+str(PID),'w')
          P.write(sr)
          P.close()
          #timeout = 1500 # timeout should be configured globally


          user = kwargs['csource_id']
          password = str(kwargs['csource_id'])+"123"
          file_name = '/tmp/filter_add_'+router+'_'+str(PID)
          seq_num = 0
          opt_seq_num = 0
          seq_num_found_int_file = 0
          sequence_number = 0
          key = 'Juniper'
          digest = ""
          dtcp_cmd = ""
          opt_seq_num = 1


          ssh = paramiko.SSHClient()
          ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

          socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          socket1.connect((router,32001))

          trans = paramiko.Transport(socket1)
          trans.connect(username=user, password=password)

          #CREATE CHANNEL FOR DATA COMM
          ch = trans.open_session()

          #Invoke flow-tap-dtcp Subsystem
          ch.invoke_subsystem('flow-tap-dtcp')
         
          #Hands the file to flow tap method to send it to DUT after SSH Authentication  
          resp_file = self._flow_tap (router, kwargs['csource_id'], str(kwargs['csource_id'])+"123", '/tmp/filter_del_'+router+'_'+str(PID), sequence_number,ch)

          #Sends the response to dtcp response method to validate the reply
          (resp_hash, dtcp_ok) = self._dtcp_response(resp_file)
          
          #Removes the files generated during DELETE request and reply
          os.remove('/tmp/filter_del_'+router+'_'+str(PID))
          os.remove(resp_file)
          ch.close()
          trans.close()
          socket1.close()
          if(int(dtcp_ok) == 1):
             return True
          else:
            return False


if __name__ == "__main__":
  x = dtcp()
  x.dtcp_add_filter(version="0.8",ttl=255,router="esst480s",src_addr="20.20.20.1",dst_addr="30.30.30.1",src_port=1000,dst_port=2000,filter_type="ccc_in",num_filt=1,src_step=1,csource_id="ftap1",cdest1_id="cd1",protocol=17,csource_addr="208.223.208.9",cdest1_addr="212.25.99.81",cdest1_port=8001,intf="ge-1/3/5.0")
  x.dtcp_list_filter(router="esst480s",csource_id="ftap1",id="cdest",id_val="cd1",flag="Criteria")
  x.dtcp_delete_filter(router="esst480s",csource_id="ftap1",id="cdest",id_val="cd1")
