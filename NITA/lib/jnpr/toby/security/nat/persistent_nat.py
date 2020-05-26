#
# TODO: This is a placeholder for UTs
#




import re
import time
import random
import jxmlease

def router_config(r0,sapt_pool,sat_pool,shift_pool,sa_net,phone1_ip,phone2_ip,da_net,stund_ip,stund2_ip,asterisk_ip,phone3_ip,phone4_ip):

	'''
		Configures zones,policy,application and nat source pool on the dut.

		Mandatory Arguments:

		All the arguments are STR type

			r0 : DUT  
			sapt_pool : SAPT pool address
			sat_pool  : SAT pool address
			shift_pool : shift pool address
			sa_net : address
			phone1_ip : phone1_ip address
			phone2_ip : phone2_ip address
			da_net : address
			stund_ip : destination ip
			stund2_ip : destination ip
			asterisk_ip : ip address
			phone3_ip : ip address
			phone4_ip : ip address


	'''

	phone1_ip=phone1_ip+'/32'
	phone2_ip=phone2_ip+'/32'
	phone3_ip=phone3_ip+'/32'
	phone4_ip=phone4_ip+'/32'


	stund_ip=stund_ip+'/32'
	stund2_ip=stund2_ip+'/32'

	asterisk_ip=asterisk_ip+'/32'


	r0.config(command_list=["delete security",
				"delete applications"])

	r0.commit(timeout=180)
	cmd_1="set security policies from-zone trust to-zone untrust policy";

	r0.config(command_list=["set security zones security-zone trust interfaces " +  t['resources']['box']['interfaces']['r0h0']['pic'],
	"set security zones security-zone trust host-inbound-traffic system-services all",
	"set security zones security-zone trust host-inbound-traffic protocols all",
    "set security zones security-zone untrust interfaces " + t['resources']['box']['interfaces']['r0h1']['pic'],
    "set security zones security-zone untrust host-inbound-traffic protocols all",
    "set security zones security-zone untrust host-inbound-traffic system-services all",
    "set security nat source pool src-nat-with-pat address " + sapt_pool,
    "set security nat source pool src-nat-without-pat address " + sat_pool,
    "set security nat source pool src-nat-without-pat port no-translation",
	"set security nat source pool src-nat-without-pat overflow-pool src-nat-with-pat",
    "set security nat source pool src-nat-by-shifting address " + shift_pool,
    "set security nat source pool src-nat-by-shifting host-address-base " + phone1_ip,
    "set security zones security-zone trust address-book address SA_net " + sa_net,
    "set security zones security-zone trust address-book address sa_phone1 " + phone1_ip,
    "set security zones security-zone trust address-book address sa_phone2 " + phone2_ip,
    "set security zones security-zone untrust address-book address DA_net " + da_net,
    "set security zones security-zone untrust address-book address stun_server " + stund_ip,
    "set security zones security-zone untrust address-book address stun_server_2ip " + stund2_ip,
    "set security zones security-zone untrust address-book address sip_proxy " + asterisk_ip,
    "set security zones security-zone untrust address-book address phone3 " + phone3_ip,
    "set security zones security-zone untrust address-book address phone4 " + phone4_ip,
	"set applications application my_stun protocol tcp",
    "set applications application my_stun source-port 0-65535",
    "set applications application my_stun destination-port 3479",
    "set applications application my_stun_udp protocol udp",
    "set applications application my_stun_udp source-port 0-65535",
    "set applications application my_stun_udp destination-port 3479",
    "set security flow tcp-session tcp-initial-timeout 30",
    "set security policies from-zone trust to-zone untrust policy stun_traffic match source-address sa_phone1",
"set security policies from-zone trust to-zone untrust policy stun_traffic match source-address sa_phone2",
"set security policies from-zone trust to-zone untrust policy stun_traffic match destination-address stun_server",
"set security policies from-zone trust to-zone untrust policy stun_traffic match destination-address stun_server_2ip",
"set security policies from-zone trust to-zone untrust policy stun_traffic match application junos-stun",
"set security policies from-zone trust to-zone untrust policy stun_traffic match application my_stun",
"set security policies from-zone trust to-zone untrust policy stun_traffic match application my_stun_udp",
"set security policies from-zone trust to-zone untrust policy stun_traffic then permit",
"set security policies from-zone trust to-zone untrust policy source-nat match source-address SA_net",
"set security policies from-zone trust to-zone untrust policy source-nat match destination-address DA_net",
"set security policies from-zone trust to-zone untrust policy source-nat match application junos-persistent-nat",
"set security policies from-zone trust to-zone untrust policy source-nat then permit"
                   ])


	r0.commit(timeout=180)

def config_nat(r0,phone1_ip,stund_ip,stund2_ip,da_net,pst_nat_type=None,nat_type=None,timeout=None,max_session=None):
	
	phone1_ip=phone1_ip+'/32'
	stund_ip=stund_ip+'/32'
	stund2_ip=stund2_ip+'/32'


	r0.config(command_list=["set security nat source rule-set src_nat from zone trust",
                                "set security nat source rule-set src_nat to zone untrust",
		"set security nat source rule-set src_nat rule cone_nat match source-address " + phone1_ip,
		"set security nat source rule-set src_nat rule cone_nat match destination-address " + stund_ip,
		"set security nat source rule-set src_nat rule cone_nat match destination-address " + stund2_ip,
		"set security nat source rule-set src_nat rule cone_nat match destination-address " + da_net,
		"set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-by-shifting",
"set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat permit " + pst_nat_type])


	if timeout is not None:
		r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat inactivity-timeout "+ timeout ])

	if max_session is not None:
		r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat max-session-number "+ max_session])

	if  pst_nat_type == "any-remote-host":
		r0.config(command_list=["set security policies from-zone untrust to-zone trust policy incoming match source-address DA_net",
"set security policies from-zone untrust to-zone trust policy incoming match destination-address SA_net",
"set security policies from-zone untrust to-zone trust policy incoming match application junos-persistent-nat",
"set security policies from-zone untrust to-zone trust policy incoming then permit"])

	if nat_type == "SRC_BY_SHIFTING":
		r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-by-shifting"])

	if nat_type == "SAT":
		r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-without-pat"])

	if nat_type == "SAPT":
		r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-with-pat"])


	if nat_type == "INTERFACE":
		r0.config(command_list=["delete security nat source rule-set src_nat rule cone_nat then",
"set security nat source rule-set src_nat rule cone_nat then source-nat interface persistent-nat permit "+ pst_nat_type])
		if timeout is not None:
    			r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat interface persistent-nat inactivity-timeout " + timeout])

		if max_session is not None:
    			r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat interface persistent-nat max-session-number " + max_session])
		r0.config(command_list=["set security nat source interface port-overloading off"])

	r0.commit(timeout=180)
	


def config_nat1(r0,phone1_ip,stund_ip,stund2_ip,asterisk_ip,da_net,pst_nat_type=None,nat_type=None,timeout=None,max_session=None):


	'''
	
	Configure nat rule-set on DUT

		Optional Argument :  
								pst_nat_type : nat_type
								timeout : timeout value
								max_session : Max session value

		Manadatory :

		r0 :DUT
		phone1_ip : ip address
		stund_ip :ip address
		stund2_ip :ip address
		asterisk : ip address
		da_net : ip address


	'''
	
	phone1_ip=phone1_ip+'/32'
	stund_ip=stund_ip+'/32'
	stund2_ip=stund2_ip+'/32'
	asterisk_ip=asterisk_ip+'/32'


	r0.config(command_list=["set security nat source rule-set src_nat from zone trust",
                                "set security nat source rule-set src_nat to zone untrust",
		"set security nat source rule-set src_nat rule cone_nat match source-address " + phone1_ip,
		"set security nat source rule-set src_nat rule cone_nat match destination-address " + stund_ip,
		"set security nat source rule-set src_nat rule cone_nat match destination-address " + stund2_ip,
		"set security nat source rule-set src_nat rule cone_nat match destination-address " + asterisk_ip,
		"set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat address-mapping",
		"set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-by-shifting",
"set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat permit " + pst_nat_type])


	if timeout is not None:
		r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat inactivity-timeout "+ timeout ])

	if max_session is not None:
		r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat max-session-number "+ max_session])

	if  pst_nat_type == "any-remote-host":
		r0.config(command_list=["set security policies from-zone untrust to-zone trust policy incoming match source-address DA_net",
"set security policies from-zone untrust to-zone trust policy incoming match destination-address SA_net",
"set security policies from-zone untrust to-zone trust policy incoming match application junos-persistent-nat",
"set security policies from-zone untrust to-zone trust policy incoming then permit"])

	if nat_type == "SRC_BY_SHIFTING":
		r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-by-shifting"])

	if nat_type == "SAT":
		r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-without-pat"])

	if nat_type == "SAPT":
		r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-with-pat"])


	if nat_type == "INTERFACE":
		r0.config(command_list=["delete security nat source rule-set src_nat rule cone_nat then",
"set security nat source rule-set src_nat rule cone_nat then source-nat interface persistent-nat permit "+ pst_nat_type])
		if timeout is not None:
    			r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat interface persistent-nat inactivity-timeout " + timeout])

		if max_session is not None:
    			r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat interface persistent-nat max-session-number " + max_session])
		r0.config(command_list=["set security nat source interface port-overloading off"])

	r0.commit(timeout=180)


def get_pst_nat_binding(device=None,src_ip=None,dest_ip=None,src_port=None,dest_port=None,protocol=None,i=None):

	'''

	Returns destination port and destination address from the session.

	Arguments :

		device : DUT
		src_ip : ip address
		dest_ip : ip address
		src_port : port no
		dest_port : port no
		protocol : tcp | udp


	'''


	if device is None:
		raise Exception("'device' is mandatory parameter - device handle")
	if device is not None:
		#device.cli(command='show security flow session').response()
		result = device.cli(command='show security flow session', format='xml').response()
		status = jxmlease.parse(result)
		device.log(status)

		sess = int(status['rpc-reply']['flow-session-information']['displayed-session-count']) - 1

		if int(status['rpc-reply']['flow-session-information']['displayed-session-count']) == 1:
			d_port = str((status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['destination-port']))
			d_address = status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['destination-address']
		else:
			d_port = str((status['rpc-reply']['flow-session-information']['flow-session'][sess]['flow-information'][1]['destination-port']))
			d_address = status['rpc-reply']['flow-session-information']['flow-session'][sess]['flow-information'][1]['destination-address']


		add = []
		add.append(d_address)
		add.append(d_port)

		return add
	
def check_flow_session(device=None,src_ip=None,dest_ip=None,src_port=None,dest_port=None,protocol=None):


	'''

	Returns the session id of the session

	Arguments :

		device : DUT
		src_ip : ip address
		dest_ip : ip address
		src_port : port no
		dest_port : port no
		protocol : tcp | udp


	'''
	
	if device is None:
		raise Exception("'device' is mandatory parameter - device handle")
	if device is not None:
		#device.cli(command='show security flow session').response()
		result = device.cli(command='show security flow session', format='xml').response()
		status = jxmlease.parse(result)
		device.log(status)


		if int(status['rpc-reply']['flow-session-information']['displayed-session-count']) > 0 :
		
			device.log("For inbound session")

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['direction']) != 'In':
				device.log(level='ERROR', message='Direction is not inbound')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Direction is inbound')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['source-address']) != src_ip:
				device.log(level='ERROR', message='Source address is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Source address is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['source-port']) != src_port:
				device.log(status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['source-port'])
				device.log(src_port)
				device.log(level='ERROR', message='Source port is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Source port is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['destination-address'])!= dest_ip:	
				device.log(level='ERROR', message='Dst address is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Dst address is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['destination-port']) != dest_port:
				device.log(level='ERROR', message='Dst nat port info is not correct')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Dst nat port info is correct')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['protocol']) != protocol:
				device.log(level='ERROR', message='Protocol info is not correct')
				raise Exception("value not present")

			else:
				device.log(level='INFO', message='Protocol info is correct')

			'''
			device.log("For outbound session")

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['direction'])!= 'Out':
				device.log(level='ERROR', message='Direction is not outbound')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Direction is outbound')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['source-address']) != dest_ip:
				device.log(level='ERROR', message='Source address is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Source address is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['source-port']) != dest_port:
				device.log(level='ERROR', message='Source port is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Source port is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['destination-address'])!= src_ip:
				device.log(level='ERROR', message='Dst address is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Dst address is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['destination-port']) != src_port:
				device.log(level='ERROR', message='Dst nat port info is not correct')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Dst nat port info is correct')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['protocol']) != protocol:
				device.log(level='ERROR', message='Protocol info is not correct')
				raise Exception("value not present")

			else:
				device.log(level='INFO', message='Protocol info is correct')

			'''
			return (status['rpc-reply']['flow-session-information']['flow-session']['session-identifier'])
	
		else:
			return 0
	
		
 


def sendip(h0=None,protocol=None, src_ip=None, dst_ip=None, src_port=None, dst_port=None):

	'''
	Sends UDP or TCP traffic 

	Arguments :

		device : DUT
		src_ip : ip address
		dest_ip : ip address
		src_port : port no
		dest_port : port no
		protocol : tcp | udp

	
	'''

	h0.su()

	if protocol == "udp" :
		h0.shell(command="sendip -d r28 -p ipv4 -iv 4 -is "+ src_ip +" -id " + dst_ip + " -p udp -us " + src_port+ " -ud " + dst_port + " " + dst_ip)
	else :
		h0.shell(command="sendip -d r28 -p ipv4 -iv 4 -is " + src_ip + " -id " + dst_ip+ "  -p tcp -ts " + src_port + " -td  " + dst_port + " " + dst_ip)
	
	#time.sleep(1)

def check_flow_session_result(pst_nat_type,flow1,flow2,flow3,flow4):

	'''
	
	Verifies flow session for various nat type.

	All the arguments are integers.

	'''

	result=0


	if pst_nat_type == "ANY-REMOTE-HOST":
		if flow1 != 0 and flow2 != 0 and flow3 != 0 :
			result=1
	if pst_nat_type == "TARGET-HOST":
		if flow1 != 0 and flow2 != 0 and flow3 == 0 and flow4 == 0 :
			result=1
	if pst_nat_type == "TARGET-HOST-PORT":
		if flow1 != 0 and flow2 == 0 and flow3 == 0 and flow4 == 0 :		
			result=1

	return result


def get_bind_entry(r0,internal_ip,internal_port='0'):


	'''
	Returns bind information of the session.

	Arguments:

	r0 : DUT
	internal_ip : ip address
	internal_port : port no

	'''

	#internal_port = '0'

	string1="show security nat source persistent-nat-table internal-ip "+internal_ip + " internal-port "+internal_port  
	r0.log(string1)	
	#result = r0.cli(command='show security nat source persistent-nat-table internal-ip  ' +internal_ip + ' internal-port ' +internal_port, format='xml').response()
	result = r0.cli(command=string1, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	bind_life_time = -1;
	config_time = -1;
	curr_session = -1;
	max_session = -1;
	nat_pool = -1;
	nat_rule = -1;
	pst_type = -1;

	bind_info=[]


	if status['rpc-reply']['persist-nat-table'] != "":

		if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-left-time'] is not None:
			bind_life_time=status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-left-time']
	

		if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-config-time'] is not None:
			config_time=status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-config-time']
		
		if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-current-session-num'] is not None:
			curr_session=status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-current-session-num']

		if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-max-session-num'] is not None:
			max_session=status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-max-session-num']

		if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-pool-name'] is not None:
			nat_pool=status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-pool-name']


		if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-type'] is not None:
			pst_type=status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-type']

		if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-rule-name'] is not None:
			nat_rule=status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-rule-name']


	r0.log(level='INFO', message="\n persist-nat-left-time: " + str(bind_life_time))
	r0.log(level='INFO', message="\n persist-nat-config-time: " + str(config_time))
	r0.log(level='INFO', message="\n persist-nat-current-session-num: " + str(curr_session))
	r0.log(level='INFO', message="\n persist-nat-max-session-num: " + str(max_session))
	r0.log(level='INFO', message="\n persist-nat-pool-name: " + str(nat_pool))
	r0.log(level='INFO', message="\n persist-nat-type: " + str(pst_type) )
	r0.log(level='INFO', message="\n persist-nat-rule-name: " + str(nat_rule) )


	bind_info=[bind_life_time,config_time,curr_session,max_session,nat_pool,pst_type,nat_rule]

	return bind_info

def send_traffic_and_verify(h0, r0, h1, phone1_ip, stund_ip, src_port1, stund_port, stund2_ip, asterisk_ip, protocol=None, timeout=None, max_session=None, pst_nat_type=None):

	'''
	Main sub routine which sends traffic and verifies session.

	h0 : host 1
	h1: host 2
	r0 : dut



	'''

	#phone1_ip = "10.10.10.196"
	#stund_ip =  "20.20.20.105"
	#src_port1 = "6000"
	#stund_port = "3478"
	#stund2_ip = "20.20.20.106"
	#asterisk_ip =  "20.20.20.25"

	
	if timeout is None:
		timeout=300
	if max_session is None:
		max_session=30

	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port);
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)	
	

	
	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)
	
	r0.cli(command='clear security flow session session-identifier ' + flow1)

	time.sleep(5)

	dest_port_1=str(int(address_list[1])+1)
	sendip(h1,protocol,stund_ip,address_list[0],stund_port,address_list[1]);
	flow1=check_flow_session(r0,stund_ip,address_list[0],stund_port,address_list[1],protocol)

	if flow1 != 0:
		r0.log(level='INFO', message=" Got flow1 session id: %s" %flow1 )
		r0.cli(command='clear security flow session session-identifier ' + flow1)
		time.sleep(5)
		flow1=1

	
	sendip(h1,protocol,stund_ip,address_list[0],src_port1,address_list[1]);
	flow2=check_flow_session(r0,stund_ip,address_list[0],src_port1,address_list[1],protocol)

	if flow2 != 0:
		r0.log(level='INFO', message=" Got flow2 session id: %s" %flow2 )
		r0.cli(command='clear security flow session session-identifier ' + flow2)
		time.sleep(5)
		flow2=1


	sendip(h1,protocol,stund2_ip,address_list[0],stund_port,address_list[1]);
	flow3=check_flow_session(r0,stund2_ip,address_list[0],stund_port,address_list[1],protocol)	
	
	if flow3 != 0:
		r0.log(level='INFO', message=" Got flow3 session id: %s" %flow3 )
		r0.cli(command='clear security flow session session-identifier ' + flow3)
		time.sleep(5)
		flow3=1

	sendip(h1,protocol,stund_ip,address_list[0],stund_port,dest_port_1);
	flow4=check_flow_session(r0,stund_ip,address_list[0],stund_port,dest_port_1,protocol)

	if flow4 != 0:
		r0.log(level='INFO', message=" Got flow4 session id: %s" %flow4 )
		r0.cli(command='clear security flow session session-identifier ' + flow4)
		time.sleep(5)
		flow4=1
		


	result = check_flow_session_result(pst_nat_type,flow1,flow2,flow3,flow4)

	if result == 1:
		 r0.log(level='INFO', message="Check flow session Successful")
	else:
		 r0.log(level='ERROR', message="Check flow session Failed")


	
	sendip (h0,protocol,phone1_ip,asterisk_ip,src_port1,src_port1);
	
	address_list_1=[]
	
	address_list_1=get_pst_nat_binding (r0,phone1_ip,asterisk_ip,src_port1,src_port1,protocol);

	r0.log(level='INFO', message="******First binding info: %s" %address_list)
	r0.log(level='INFO', message="******Second binding info: %s" %address_list_1)


	if address_list_1[0] != address_list[0] or address_list_1[1] != address_list[1] :
		r0.log(level='ERROR', message="Two binding info are not same")
	else:
		r0.log(level='INFO', message="Two binding info are same")

	

	r0.log(level='INFO', message=" ******Waiting for session ageout! Sleep 70 seconds.******* ")

	time.sleep(70)

	r0.cli(command="clear security nat source persistent-nat-table all")

	time.sleep(5)


	r0.log(level='INFO', message="Verify that binding entry ageout successfully.")


	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)

	if  bind_entry_info[0] != -1 :
		r0.log(level='ERROR', message=" ******bind entry still exists. *******")
	else:
		r0.log(level='INFO', message=" ******bind entry ageout successfully. *******")

	
		
	'''
	
	if r0 is not None:
		result = r0.cli(command='show security flow session', format='xml').response()
		status = jxmlease.parse(result)
		r0.log(status)


	 '''
def binding_entry_ageout1(h0, r0, h1, phone1_ip, stund_ip, src_port1, stund_port, stund2_ip, asterisk_ip, protocol=None, timeout=None, max_session=None, pst_nat_type=None):


	'''
	Verifies bind info of the session.

	'''

	
	if timeout is None:
		timeout=300
	else:
		timeout=int(timeout)
	if max_session is None:
		max_session=30
	else:
		max_session=int(max_session)


	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port);
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	policy = "stun_traffic"

	

	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)
	
	bind_entry_info=[]


	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')


	bind_life_time = bind_entry_info[0]
	config_time = int(bind_entry_info[1])
	curr_session = int(bind_entry_info[2])
	max_session_1 = int(bind_entry_info[3])
		

	if curr_session == -1 :
		r0.log(level='ERROR', message=" ****** No binding table found. ******* ")
	elif timeout == config_time and max_session == max_session_1 :
		r0.log(level='INFO',message=" ****** Config check seccussfully. *******")
	elif pst_nat_type == 'TARGET-HOST-PORT' or pst_nat_type == 'TARGET-HOST' and max_session_1 == 8:
		r0.log(level='INFO',message=" ****** Config check seccussfully. *******")
	else:
		r0.log(level='ERROR', message=" ****** Config is wrong. ******* ")


	if bind_life_time == '-' :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time == 65535 when session exists. *******")
	
		r0.cli(command='clear security flow session session-identifier ' + flow1)

	else :
		r0.log(level='ERROR', message=" ****** Persist-nat-left-time != 65535 when session exists. ******* ")


	time.sleep(5)

	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')


	if int(bind_entry_info[0]) <= config_time and int(bind_entry_info[0]) >= 0 :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time is in the value [0,"+ str(config_time)+ "] when session disappeared  *******")
	else:
		 r0.log(level='ERROR',message=" ****** Persist-nat-left-time isn't in the value [0,"+ str(config_time)+ "] when session disappeared  *******")

	
	time.sleep(2)

	bind_entry_info_1 = get_bind_entry (r0,phone1_ip,'0')

	if int(bind_entry_info[0]) > int(bind_entry_info_1[0]) :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time is decreasing. *******")
	else:
		r0.log(level='ERROR',message=" ****** Persist-nat-left-time ageout error. *******")
	
	sendip (h1,protocol,stund_ip,address_list[0],stund_port,address_list[1]);

	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')


	if bind_entry_info[0] != '-' :
		r0.log(level='ERROR',message=" ****** Persist-nat-left-time != 65535 when session exists. *******")
	else:
		r0.log(level='INFO',message=" ****** Wait " + str(config_time) +"  seconds for binding entry timeout. ******")
		time.sleep(70)
		time.sleep(config_time)

	 
	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')

	if bind_entry_info[0] != -1 :
		r0.log(level='ERROR',message="\n ******bind entry still exists. *******\n\n")
	else:
		r0.log(level='INFO', message="\n ******bind entry ageout successfully. ******* \n\n")


	sendip(h1,protocol,stund_ip,address_list[0],stund_port,address_list[1])

	flow1=check_flow_session(r0,stund_ip,address_list[0],stund_port,address_list[1],protocol)
	
	if flow1 !=0:
		r0.log(level='ERROR', message=" Reverse sessin can be installed after binding entry ageout. ")



def binding_entry_ageout(h0, r0, h1, phone1_ip, stund_ip, src_port1, stund_port, stund2_ip, asterisk_ip, protocol=None, timeout=None, max_session=None, pst_nat_type=None):


	'''
	Verifies bind info of the session.

	'''

	
	if timeout is None:
		timeout=300
	else:
		timeout=int(timeout)
	if max_session is None:
		max_session=30
	else:
		max_session=int(max_session)


	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port);
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	policy = "stun_traffic"

	

	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)
	
	bind_entry_info=[]


	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)


	bind_life_time = bind_entry_info[0]
	config_time = int(bind_entry_info[1])
	curr_session = int(bind_entry_info[2])
	max_session_1 = int(bind_entry_info[3])
		

	if curr_session == -1 :
		r0.log(level='ERROR', message=" ****** No binding table found. ******* ")
	elif timeout == config_time and max_session == max_session_1 :
		r0.log(level='INFO',message=" ****** Config check seccussfully. *******")
	elif pst_nat_type == 'TARGET-HOST-PORT' or pst_nat_type == 'TARGET-HOST' and max_session_1 == 8:
		r0.log(level='INFO',message=" ****** Config check seccussfully. *******")
	else:
		r0.log(level='ERROR', message=" ****** Config is wrong. ******* ")


	if bind_life_time == '-' :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time == 65535 when session exists. *******")
	
		r0.cli(command='clear security flow session session-identifier ' + flow1)

	else :
		r0.log(level='ERROR', message=" ****** Persist-nat-left-time != 65535 when session exists. ******* ")


	time.sleep(5)

	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)


	if int(bind_entry_info[0]) <= config_time and int(bind_entry_info[0]) >= 0 :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time is in the value [0,"+ str(config_time)+ "] when session disappeared  *******")
	else:
		 r0.log(level='ERROR',message=" ****** Persist-nat-left-time isn't in the value [0,"+ str(config_time)+ "] when session disappeared  *******")

	
	time.sleep(2)

	bind_entry_info_1 = get_bind_entry (r0,phone1_ip,src_port1)

	if int(bind_entry_info[0]) > int(bind_entry_info_1[0]) :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time is decreasing. *******")
	else:
		r0.log(level='ERROR',message=" ****** Persist-nat-left-time ageout error. *******")
	
	sendip (h1,protocol,stund_ip,address_list[0],stund_port,address_list[1]);

	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)


	if bind_entry_info[0] != '-' :
		r0.log(level='ERROR',message=" ****** Persist-nat-left-time != 65535 when session exists. *******")
	else:
		r0.log(level='INFO',message=" ****** Wait " + str(config_time) +"  seconds for binding entry timeout. ******")
		time.sleep(70)
		time.sleep(config_time)

	 
	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)

	if bind_entry_info[0] != -1 :
		r0.log(level='ERROR',message="\n ******bind entry still exists. *******\n\n")
	else:
		r0.log(level='INFO', message="\n ******bind entry ageout successfully. ******* \n\n")


	sendip(h1,protocol,stund_ip,address_list[0],stund_port,address_list[1])

	flow1=check_flow_session(r0,stund_ip,address_list[0],stund_port,address_list[1],protocol)
	
	if flow1 !=0:
		r0.log(level='ERROR', message=" Reverse sessin can be installed after binding entry ageout. ")


def check_flow_session_2(i,device=None,src_ip=None,dest_ip=None,src_port=None,dest_port=None,protocol=None):
	
	if device is None:
		raise Exception("'device' is mandatory parameter - device handle")
	if device is not None:
		#device.cli(command='show security flow session').response()
		result = device.cli(command='show security flow session', format='xml').response()
		status = jxmlease.parse(result)
		device.log(status)


		if int(status['rpc-reply']['flow-session-information']['displayed-session-count']) > 0 :
		
			device.log("For inbound session")

			if (status['rpc-reply']['flow-session-information']['flow-session'][i]['flow-information'][0]['direction']) != 'In':
				device.log(level='ERROR', message='Direction is not inbound')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Direction is inbound')

			if (status['rpc-reply']['flow-session-information']['flow-session'][i]['flow-information'][0]['source-address']) != src_ip:
				device.log(level='ERROR', message='Source address is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Source address is right')

			if (status['rpc-reply']['flow-session-information']['flow-session'][i]['flow-information'][0]['source-port']) != src_port:
				device.log(status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['source-port'])
				device.log(src_port)
				device.log(level='ERROR', message='Source port is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Source port is right')

			if (status['rpc-reply']['flow-session-information']['flow-session'][i]['flow-information'][0]['destination-address'])!= dest_ip:	
				device.log(level='ERROR', message='Dst address is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Dst address is right')

			if (status['rpc-reply']['flow-session-information']['flow-session'][i]['flow-information'][0]['destination-port']) != dest_port:
				device.log(level='ERROR', message='Dst nat port info is not correct')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Dst nat port info is correct')

			if (status['rpc-reply']['flow-session-information']['flow-session'][i]['flow-information'][0]['protocol']) != protocol:
				device.log(level='ERROR', message='Protocol info is not correct')
				raise Exception("value not present")

			else:
				device.log(level='INFO', message='Protocol info is correct')

			'''
			device.log("For outbound session")

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['direction'])!= 'Out':
				device.log(level='ERROR', message='Direction is not outbound')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Direction is outbound')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['source-address']) != dest_ip:
				device.log(level='ERROR', message='Source address is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Source address is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['source-port']) != dest_port:
				device.log(level='ERROR', message='Source port is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Source port is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['destination-address'])!= src_ip:
				device.log(level='ERROR', message='Dst address is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Dst address is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['destination-port']) != src_port:
				device.log(level='ERROR', message='Dst nat port info is not correct')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Dst nat port info is correct')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['protocol']) != protocol:
				device.log(level='ERROR', message='Protocol info is not correct')
				raise Exception("value not present")

			else:
				device.log(level='INFO', message='Protocol info is correct')

			'''
			return (status['rpc-reply']['flow-session-information']['flow-session'][i]['session-identifier'])
	
		else:
			return 0

def get_session_count(device):

	'''
	Returns total count of the session on the device.

	'''
	if device is None:
		raise Exception("'device' is mandatory parameter - device handle")
	if device is not None:	
		device.cli(command='show security flow session').response()
		result = device.cli(command='show security flow session', format='xml').response()
		status = jxmlease.parse(result)	
		device.log(status)


		return int(status['rpc-reply']['flow-session-information']['displayed-session-count']) 

def max_session_test1(h0, r0, h1, phone1_ip, phone3_ip, stund_ip, src_port1, src_port2, stund_port, stund2_ip, asterisk_ip, protocol=None, timeout=None, max_session=None, pst_nat_type=None):

	'''
	Verifies the maximum number of session that can be installed on different type of nat type.

	'''

	if timeout is None:
		timeout=300
	else:
		timeout=int(timeout)
	if max_session is None:
		max_session=30	
	else:
		max_session=int(max_session)


	if max_session >=8:
		r0.config(command_list=['set applications application max_session protocol udp',
					'set applications application max_session source-port ' + src_port1,
					'set applications application max_session destination-port 0-65535',
					'set applications application max_session inactivity-timeout 800',
					'delete security policies from-zone trust to-zone untrust policy source-nat match application junos-persistent-nat',
					'set security policies from-zone trust to-zone untrust policy source-nat match application max_session',
					'set security policies from-zone trust to-zone untrust policy source-nat match application junos-persistent-nat'
					])

		r0.commit(timeout=180)

	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port);
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

       
	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	bind_entry_info=[]


	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')


	bind_life_time = bind_entry_info[0]
	config_time = int(bind_entry_info[1])
	curr_session = int(bind_entry_info[2])
	max_session_1 = int(bind_entry_info[3])


	if curr_session == -1 :
		r0.log(level='ERROR', message=" ****** No binding table found. ******* ")
	elif timeout == config_time and max_session == max_session_1 :
		r0.log(level='INFO',message=" ****** Config check seccussfully. *******")
	elif pst_nat_type == 'TARGET-HOST-PORT' or pst_nat_type == 'TARGET-HOST' and max_session_1 == 8:
		r0.log(level='INFO',message=" ****** Config check seccussfully. *******")
	else:
		r0.log(level='ERROR', message=" ****** Config is wrong. ******* ")

	if bind_life_time == '-' :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time == 65535 when session exists. *******")

		r0.cli(command='clear security flow session session-identifier ' + flow1)

	else :
		r0.log(level='ERROR', message=" ****** Persist-nat-left-time != 65535 when session exists. ******* ")


	time.sleep(5)

	start=int(src_port2)+1
	end=int(src_port2)+int(max_session)+1

	for port in  range(start,end):
		sendip (h0,protocol,phone1_ip,stund2_ip,src_port1,str(port))

	
	sendip (h0,protocol,phone1_ip,stund_ip,src_port1,stund_port)

	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')

	curr_session = int(bind_entry_info[2])

	if curr_session < max_session :
		r0.log(level='ERROR',message=" Install " + str(max_session) +" sessions failed! ******* ")
	elif curr_session > max_session :
		r0.log(level='ERROR',message=" Curr_session > max_session, failed! *******")
	else :
		r0.log(level='INFO',message=" Curr_session = max_session.  ")


	before = get_session_count(r0)

	sendip (h0,protocol,phone1_ip,phone3_ip,src_port1,src_port2)	

	after = get_session_count(r0) 

	if(after > before):
		r0.log(level='INFO',message=" No session found")
	else :
		r0.log(level='ERROR',message=" Got flow session")

	
	r0.cli(command='clear security flow session source-prefix ' + phone1_ip)	

	time.sleep(10)

	if pst_nat_type == "TARGET-HOST-PORT" :
		time.sleep(4)
		sendip (h0,protocol,phone1_ip,phone3_ip,src_port1,src_port2)
		flow1=check_flow_session(r0,phone1_ip,phone3_ip,src_port1,src_port2,protocol)
	
		if flow1 != 0:
			r0.log(level='ERROR',message="\n Got flow1 session id: " + flow1)

	

	
	r0.log(level='INFO', message="\n Wait " + str(config_time) + " seconds for binding entry timeout. ")

	time.sleep(timeout)

	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')

	if bind_entry_info[0] != -1 :
		r0.log(level='ERROR',message="\n ******bind entry still exists. *******\n\n")
	else:
		r0.log(level='INFO', message="\n ******bind entry ageout successfully. ******* \n\n")
		




def max_session_test(h0, r0, h1, phone1_ip, phone3_ip, stund_ip, src_port1, src_port2, stund_port, stund2_ip, asterisk_ip, protocol=None, timeout=None, max_session=None, pst_nat_type=None):

	'''
	Verifies the maximum number of session that can be installed on different type of nat type.

	'''

	if timeout is None:
		timeout=300
	else:
		timeout=int(timeout)
	if max_session is None:
		max_session=30	
	else:
		max_session=int(max_session)


	if max_session >=8:
		r0.config(command_list=['set applications application max_session protocol udp',
					'set applications application max_session source-port ' + src_port1,
					'set applications application max_session destination-port 0-65535',
					'set applications application max_session inactivity-timeout 800',
					'delete security policies from-zone trust to-zone untrust policy source-nat match application junos-persistent-nat',
					'set security policies from-zone trust to-zone untrust policy source-nat match application max_session',
					'set security policies from-zone trust to-zone untrust policy source-nat match application junos-persistent-nat'
					])

		r0.commit(timeout=180)

	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port);
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

       
	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	bind_entry_info=[]


	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)


	bind_life_time = bind_entry_info[0]
	config_time = int(bind_entry_info[1])
	curr_session = int(bind_entry_info[2])
	max_session_1 = int(bind_entry_info[3])


	if curr_session == -1 :
		r0.log(level='ERROR', message=" ****** No binding table found. ******* ")
	elif timeout == config_time and max_session == max_session_1 :
		r0.log(level='INFO',message=" ****** Config check seccussfully. *******")
	elif pst_nat_type == 'TARGET-HOST-PORT' or pst_nat_type == 'TARGET-HOST' and max_session_1 == 8:
		r0.log(level='INFO',message=" ****** Config check seccussfully. *******")
	else:
		r0.log(level='ERROR', message=" ****** Config is wrong. ******* ")

	if bind_life_time == '-' :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time == 65535 when session exists. *******")

		r0.cli(command='clear security flow session session-identifier ' + flow1)

	else :
		r0.log(level='ERROR', message=" ****** Persist-nat-left-time != 65535 when session exists. ******* ")


	time.sleep(5)

	start=int(src_port2)+1
	end=int(src_port2)+int(max_session)+1

	for port in  range(start,end):
		sendip (h0,protocol,phone1_ip,stund2_ip,src_port1,str(port))

	
	sendip (h0,protocol,phone1_ip,stund_ip,src_port1,stund_port)

	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)

	curr_session = int(bind_entry_info[2])

	if curr_session < max_session :
		r0.log(level='ERROR',message=" Install " + str(max_session) +" sessions failed! ******* ")
	elif curr_session > max_session :
		r0.log(level='ERROR',message=" Curr_session > max_session, failed! *******")
	else :
		r0.log(level='INFO',message=" Curr_session = max_session.  ")


	before = get_session_count(r0)

	sendip (h0,protocol,phone1_ip,phone3_ip,src_port1,src_port2)	

	after = get_session_count(r0) 

	if(after > before):
		r0.log(level='ERROR',message=" Got flow session")
	else :
		r0.log(level='INFO',message=" No session found")

	
	r0.cli(command='clear security flow session source-prefix ' + phone1_ip)	

	time.sleep(10)

	if pst_nat_type == "TARGET-HOST-PORT" :
		time.sleep(4)
		sendip (h0,protocol,phone1_ip,phone3_ip,src_port1,src_port2)
		flow1=check_flow_session(r0,phone1_ip,phone3_ip,src_port1,src_port2,protocol)
	
		if flow1 != 0:
			r0.log(level='ERROR',message="\n Got flow1 session id: " + flow1)

	

	
	r0.log(level='INFO', message="\n Wait " + str(config_time) + " seconds for binding entry timeout. ")

	time.sleep(timeout)

	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)

	if bind_entry_info[0] != -1 :
		r0.log(level='ERROR',message="\n ******bind entry still exists. *******\n\n")
	else:
		r0.log(level='INFO', message="\n ******bind entry ageout successfully. ******* \n\n")
		



def check_nat_syslog(h0, r0, h1, phone1_ip, phone3_ip, stund_ip, src_port1, src_port2, stund_port, stund2_ip, asterisk_ip, protocol=None, timeout=None, max_session=None, pst_nat_type=None):

	'''

	Checks nat log information.

	'''

	if timeout is None:
		timeout=300
	else:
		timeout=int(timeout)
	if max_session is None:
		max_session=30
	else:
		max_session=int(max_session)


	r0.config(command_list=['set security log mode event',
				'set system syslog file nat-log-messages any any',
				'set system syslog file nat-log-messages structured-data',
				'set security policies from-zone trust to-zone untrust policy stun_traffic then log session-init'
				])


	r0.commit(timeout=180)


	r0.cli(command='clear log nat-log-messages')

	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port);
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)


	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	time.sleep(65)

	sendip (h1,protocol,stund_ip,address_list[0],stund_port,address_list[1])
	
	time.sleep(65)


	r0.cli(command='clear security nat source persistent-nat-table internal-ip ' + phone1_ip + ' internal-port ' + src_port1)


	time.sleep(4)
	time.sleep(timeout)

	resp = r0.cli(command='show log nat-log-messages', format='text').response()

	if resp.count('RT_PST_NAT_BINDING_CREATE') >= 1 :
		r0.log(level='INFO',message="\n There are " + str(resp.count('RT_PST_NAT_BINDING_CREATE')) + " matching RT_PST_NAT_BINDING_CREATE in the context.")

	else :
		r0.log(level='ERROR',message=" Can't find RT_PST_NAT_BINDING_CREATE records! ")


	if resp.count('RT_PST_NAT_BINDING_MATCH') >= 1 :
		r0.log(level='INFO',message="\n There are " + str(resp.count('RT_PST_NAT_BINDING_MATCH')) + " matching RT_PST_NAT_BINDING_CREATE in the context.")

	else :
		r0.log(level='ERROR',message=" Can't find RT_PST_NAT_BINDING_MATCH records! ")


	if resp.count('RT_PST_NAT_BINDING_DELETE') >= 1 :
		r0.log(level='INFO',message="\n There are " + str(resp.count('RT_PST_NAT_BINDING_DELETE')) + " matching RT_PST_NAT_BINDING_CREATE in the context.")

	else :
		r0.log(level='ERROR',message=" Can't find RT_PST_NAT_BINDING_DELETE records! ")


def check_pst_config(r0,max_session=None,timeout=None):

	'''
	Configures and verifies different nat type 

	'''

	sa_addr1 = '10.10.10.196/32'
	sa_addr2 = '10.10.10.197/32'
	sa_addr3 = '10.10.10.198/32'
	da_addr1 = '20.20.20.105/32'
	da_addr2 = '20.20.20.106/32'
	da_addr3 = '20.20.20.107/32'
	r1_time = '200'
	r1_session = '20'
	invalid = False


	if timeout is not None and max_session is not None :
		r0.log(level='INFO',message='It is invalid config test!')
		invalid = True
	else :
		r0.log(level='INFO',message='It is correct config test!')

	r0.log(level='INFO', message = 'Config persistent nat rule.' )

	r0.config(command_list=['set security nat source rule-set src_nat from zone trust',
							'set security nat source rule-set src_nat to zone untrust',
							'set security nat source rule-set src_nat rule full_cone match source-address ' + sa_addr1,
							'set security nat source rule-set src_nat rule full_cone match destination-address ' + da_addr1,
							'set security nat source rule-set src_nat rule full_cone then source-nat pool src-nat-with-pat',
							'set security nat source rule-set src_nat rule full_cone then source-nat pool persistent-nat permit any-remote-host',
							'set security nat source rule-set src_nat rule full_cone then source-nat pool persistent-nat inactivity-timeout ' + r1_time,
							'set security nat source rule-set src_nat rule full_cone then source-nat pool persistent-nat max-session-number ' + r1_session,
							'set security nat source rule-set src_nat rule restricted_cone match source-address '+ sa_addr2,
							'set security nat source rule-set src_nat rule restricted_cone match destination-address '+ da_addr2,
							'set security nat source rule-set src_nat rule restricted_cone then source-nat pool src-nat-without-pat',
							'set security nat source rule-set src_nat rule restricted_cone then source-nat pool persistent-nat permit target-host'
							])

	if timeout is not None:
		r0.config(command_list=['set security nat source rule-set src_nat rule restricted_cone then source-nat pool persistent-nat inactivity-timeout ' + timeout])
	if max_session is not None:
		r0.config(command_list=['set security nat source rule-set src_nat rule restricted_cone then source-nat pool persistent-nat max-session-number ' + max_session])

	r0.config(command_list=['set security nat source rule-set src_nat rule port_restricted_cone match source-address ' + sa_addr3,
							'set security nat source rule-set src_nat rule port_restricted_cone match destination-address ' + da_addr3,
							'set security nat source rule-set src_nat rule port_restricted_cone then source-nat interface persistent-nat permit target-host-port',
							'set security nat source interface port-overloading off'
							])
	r0.commit(timeout=180)

	time.sleep(5)
	rule_name =''
	pool_type =''
	pst_type =''
	tt_time =''
	session =''

	result = r0.cli(command='show security nat source rule full_cone', format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)


	rule_name = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['rule-name']
	pool_type = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['source-nat-rule-action']
	pst_type = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['persistent-nat-type']
	tt_time = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['persistent-nat-timeout']
	session = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['persistent-nat-max-session']


	if pool_type == 'src-nat-with-pat' and pst_type == 'any-remote-host' and tt_time == r1_time  and  session == r1_session :
		r0.log(level='INFO',message=' The config of full_cone rule is currect! ')
	else:
		r0.log(level='ERROR',message=' The config of full_cone rule is Wrong ')
		raise Exception ("Config Wrong")




	result = r0.cli(command='show security nat source rule restricted_cone', format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	rule_name = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['rule-name']
	pool_type = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['source-nat-rule-action']
	pst_type = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['persistent-nat-type']
	tt_time = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['persistent-nat-timeout']
	session = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['persistent-nat-max-session']


	if pool_type == 'src-nat-without-pat' and pst_type == 'target-host' and tt_time == '300'  and  session == '30' :
		r0.log(level='INFO',message=' The config of restricted_cone rule is currect! ')
	else:
		r0.log(level='ERROR',message=' The config of restricted_cone rule is Wrong ')
		raise Exception ("Config Wrong")

	result = r0.cli(command='show security nat source rule port_restricted_cone', format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	rule_name = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['rule-name']
	pool_type = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['source-nat-rule-action']
	pst_type = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['persistent-nat-type']
	tt_time = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['persistent-nat-timeout']
	session = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['source-nat-rule-action-entry']['persistent-nat-max-session']


	if pool_type == 'interface' and pst_type == 'target-host-port' and tt_time == '300'  and  session == '8' :
		r0.log(level='INFO',message=' The config of port_restricted_cone rule is currect! ')
	else:
		r0.log(level='ERROR',message=' The config of port_restricted_cone rule is Wrong ')
		raise Exception ("Config Wrong")



def traceoption(r0,h0,protocol,phone1_ip,phone3_ip,stund_ip,src_port1,stund_port,timeout=None,max_session=None):

	'''
	Verfies persistent nat information traces.
	
	'''

	if timeout is None:
		timeout=300
	else:
		timeout=int(timeout)
	if max_session is None:
		max_session=30
	else:
		max_session=int(max_session)



	r0.config(command_list=['set security nat traceoptions flag source-nat-pfe',
  							'set security nat traceoptions flag source-nat-re',
  							'set security nat traceoptions flag source-nat-rt',
  							'set security traceoptions file nat_trace',
  							'set security traceoptions file size 40000000',
  							'set security traceoptions flag all'
  							])

	r0.commit(timeout=180)

	r0.cli(command='clear log nat_trace')

	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port)
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	r0.cli(command='clear security flow session session-identifier ' + flow1)
	time.sleep(5)

	sendip (h0,protocol,phone1_ip,phone3_ip,src_port1,src_port1)
	flow2=check_flow_session(r0,phone1_ip,phone3_ip,src_port1,src_port1,protocol)

	if flow2 ==0 :
		r0.log(level='ERROR', message= 'No session found on DUT')
		raise Exception('No session found on DUT')

	r0.cli(command='clear security flow session session-identifier ' + flow2)
	time.sleep(6)
	time.sleep(timeout)


	r0.config(command_list=['deactivate security traceoptions'])
	r0.commit(timeout=180)

	r0.log(level='INFO',message='Verify that binding entry ageout successfully.')

	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)

	if bind_entry_info[0] != -1 :
		r0.log(level='ERROR', message=" ******bind entry still exists. *******")
		raise Exception('bind entry still exists.')
	else:
		r0.log(level='INFO', message=" ******bind entry ageout successfully. *******")


	result = r0.shell(command='tail -600 /var/log/nat_trace', format='text').response()

	r0.log(result)


	if re.search("pst nat binding found", result) :
		r0.log(level='INFO',message=' Found pst_nat info! ')
	else :
		r0.log(level='ERROR',message='Cant find pst_nat info!')
		raise Exception("Cant find pst_nat info!")


def negative_binding_ageout1(r0,h0,protocol,phone1_ip,phone3_ip,stund_ip,src_port1,stund_port,src_port3,timeout=None,max_session=None,test_type=None):

	'''
	Checks binding information for various test_type : interface, policy, zone, CL_SESS.
	
	'''

	if timeout is None:
		timeout=300
	else:
		timeout=int(timeout)
	if max_session is None:
		max_session=30
	else:
		max_session=int(max_session)	

	counter=0

	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port)
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)
	counter=counter + 1

	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	sendip(h0,protocol,phone1_ip,phone3_ip,src_port1,src_port3)
	flow2=check_flow_session_2(counter,r0,phone1_ip,phone3_ip,src_port1,src_port3,protocol)
	counter=counter + 1


	if flow2 != 0 :
		r0.log(level='INFO',message='Two sessions found on DUT!')
	else:
		r0.log(level='ERROR', message='No sessions found on DUT')
		raise Exception('')

	if test_type == 'INTERFACE' :
		r0.config(command_list=['set interface ' + t['resources']['box']['interfaces']['r0h0']['pic'] + ' disable',
								 'set interface ' + t['resources']['box']['interfaces']['r0h1']['pic'] + ' disable'])

		r0.commit(timeout=180)

		time.sleep(60)

	elif test_type == "POLICY" :
		r0.config(command_list=['set security policies from-zone trust to-zone untrust policy stun_traffic then deny',
						'set security policies from-zone trust to-zone untrust policy source-nat then deny'])

		r0.commit(timeout=180)

		time.sleep(60)

	elif test_type == "ZONE" :
		r0.config(command_list=['delete security zones security-zone untrust interfaces ' + t['resources']['box']['interfaces']['r0h1']['pic'] ])
		r0.commit(timeout=180)

	elif test_type == "CL_SESS" :
		r0.cli(command='clear security flow session session-identifier ' + flow1)
		r0.cli(command='clear security flow session session-identifier ' + flow2)

		time.sleep(2)

	time.sleep(10)

	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')


	if int(bind_entry_info[0]) <= timeout and int(bind_entry_info[0]) >= 0 :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time is in the value [0,"+ str(timeout)+ "] when session disappeared  *******")
	else:
		 r0.log(level='ERROR',message=" ****** Persist-nat-left-time isn't in the value [0,"+ str(timeout)+ "] when session disappeared  *******")

	
	time.sleep(2)

	bind_entry_info_1 = get_bind_entry (r0,phone1_ip,'0')

	if int(bind_entry_info[0]) > int(bind_entry_info_1[0]) :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time is decreasing. *******")
	else:
		r0.log(level='ERROR',message=" ****** Persist-nat-left-time ageout error. *******")


	r0.log(level='INFO', message="\n Wait " + str(timeout) + " seconds for binding entry timeout. ")

	time.sleep(timeout)

	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')

	if bind_entry_info[0] != -1 :
		r0.log(level='ERROR',message="\n ******bind entry still exists. *******\n\n")
	else:
		r0.log(level='INFO', message="\n ******bind entry ageout successfully. ******* \n\n")

 

	if test_type == 'INTERFACE' :
		r0.config(command_list=['delete interface ' + t['resources']['box']['interfaces']['r0h0']['pic'] + ' disable',
								 'delete interface ' + t['resources']['box']['interfaces']['r0h1']['pic'] + ' disable'])

		r0.commit(timeout=180)


def negative_binding_ageout(r0,h0,protocol,phone1_ip,phone3_ip,stund_ip,src_port1,stund_port,src_port3,timeout=None,max_session=None,test_type=None):

	'''
	Checks binding information for various test_type : interface, policy, zone, CL_SESS.
	
	'''

	if timeout is None:
		timeout=300
	else:
		timeout=int(timeout)
	if max_session is None:
		max_session=30
	else:
		max_session=int(max_session)	

	counter=0

	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port)
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)
	counter=counter + 1

	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	sendip(h0,protocol,phone1_ip,phone3_ip,src_port1,src_port3)
	flow2=check_flow_session_2(counter,r0,phone1_ip,phone3_ip,src_port1,src_port3,protocol)
	counter=counter + 1


	if flow2 != 0 :
		r0.log(level='INFO',message='Two sessions found on DUT!')
	else:
		r0.log(level='ERROR', message='No sessions found on DUT')
		raise Exception('')

	if test_type == 'INTERFACE' :
		r0.config(command_list=['set interface ' + t['resources']['box']['interfaces']['r0h0']['pic'] + ' disable',
								 'set interface ' + t['resources']['box']['interfaces']['r0h1']['pic'] + ' disable'])

		r0.commit(timeout=180)

		time.sleep(60)

	elif test_type == "POLICY" :
		r0.config(command_list=['set security policies from-zone trust to-zone untrust policy stun_traffic then deny',
						'set security policies from-zone trust to-zone untrust policy source-nat then deny'])

		r0.commit(timeout=180)

		time.sleep(60)

	elif test_type == "ZONE" :
		r0.config(command_list=['delete security zones security-zone untrust interfaces ' + t['resources']['box']['interfaces']['r0h1']['pic'] ])
		r0.commit(timeout=180)

	elif test_type == "CL_SESS" :
		r0.cli(command='clear security flow session session-identifier ' + flow1)
		r0.cli(command='clear security flow session session-identifier ' + flow2)

		time.sleep(2)

	time.sleep(10)

	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)


	if int(bind_entry_info[0]) <= timeout and int(bind_entry_info[0]) >= 0 :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time is in the value [0,"+ str(timeout)+ "] when session disappeared  *******")
	else:
		 r0.log(level='ERROR',message=" ****** Persist-nat-left-time isn't in the value [0,"+ str(timeout)+ "] when session disappeared  *******")

	
	time.sleep(2)

	bind_entry_info_1 = get_bind_entry (r0,phone1_ip,src_port1)

	if int(bind_entry_info[0]) > int(bind_entry_info_1[0]) :
		r0.log(level='INFO',message=" ****** Persist-nat-left-time is decreasing. *******")
	else:
		r0.log(level='ERROR',message=" ****** Persist-nat-left-time ageout error. *******")


	r0.log(level='INFO', message="\n Wait " + str(timeout) + " seconds for binding entry timeout. ")

	time.sleep(timeout)

	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)

	if bind_entry_info[0] != -1 :
		r0.log(level='ERROR',message="\n ******bind entry still exists. *******\n\n")
	else:
		r0.log(level='INFO', message="\n ******bind entry ageout successfully. ******* \n\n")

 

	if test_type == 'INTERFACE' :
		r0.config(command_list=['delete interface ' + t['resources']['box']['interfaces']['r0h0']['pic'] + ' disable',
								 'delete interface ' + t['resources']['box']['interfaces']['r0h1']['pic'] + ' disable'])

		r0.commit(timeout=180)


def change_pst_nat_rule(r0,h0,protocol,phone1_ip,phone2_ip,stund_ip,src_port1,src_port2,stund_port,stund2_ip,da_net):

	r0.config(command_list=["set security nat source rule-set src_nat from zone trust",
                                                        "set security nat source rule-set src_nat to zone untrust",
                                        "set security nat source rule-set src_nat rule cone_nat match source-address " + phone1_ip + '/28',
  "set security nat source rule-set src_nat rule cone_nat match destination-address " + stund_ip + "/32",
  "set security nat source rule-set src_nat rule cone_nat match destination-address " + stund2_ip  + "/32",
  "set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-by-shifting",
  "set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat permit any-remote-host",
  "set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat inactivity-timeout 120",
  "set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat max-session-number 20",
        "set security policies from-zone trust to-zone untrust policy stun_traffic match destination-address DA_net",

  "set security policies from-zone untrust to-zone trust policy incoming match source-address DA_net",
  "set security policies from-zone untrust to-zone trust policy incoming match destination-address SA_net",
  "set security policies from-zone untrust to-zone trust policy incoming match application junos-persistent-nat",
  "set security policies from-zone untrust to-zone trust policy incoming then permit",

  "set security nat source rule-set src_nat rule cone_nat_2 match source-address " + phone1_ip + "/32",
  "set security nat source rule-set src_nat rule cone_nat_2 match source-address " +phone2_ip + "/32",
  "set security nat source rule-set src_nat rule cone_nat_2 match destination-address " + da_net,
  "set security nat source rule-set src_nat rule cone_nat_2 then source-nat interface persistent-nat permit target-host-port",
  "set security nat source rule-set src_nat rule cone_nat_2 then source-nat interface persistent-nat inactivity-timeout 60",
  "set security nat source rule-set src_nat rule cone_nat_2 then source-nat interface persistent-nat max-session-number 8",
        "set security nat source interface port-overloading off"])


	r0.commit(timeout=180)

	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port)
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	bind_entry_info = get_bind_entry(r0,phone1_ip,src_port1)

	if bind_entry_info[0] == '-' and bind_entry_info[1] == '120' and bind_entry_info[2] == '1' and bind_entry_info[3] == '20' and bind_entry_info[4] == 'src-nat-by-shifting' and bind_entry_info[5] == 'any-remote-host' and bind_entry_info[6] == 'cone_nat' :
		r0.log(level='INFO',message='Install one sessions by cone_nat rule!')
	else :
		r0.log(level='ERROR',message='Install one sessions by cone_nat rule failed')
		raise Exception('')



	r0.config(command_list=['set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-with-pat',
                                                        'set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat permit target-host',
                                                        'set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat inactivity-timeout 60',
                                                        'set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat max-session-number 10'
                                                        ])

	r0.commit(timeout=180)

	time.sleep(12)

	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	if flow1 == 0 :
		r0.log(level='INFO',message='The session is ageout! ')
		bind_entry_info = get_bind_entry (r0, phone1_ip, src_port1)

		if bind_entry_info[0] == -1 :
			r0.log(level='INFO', message='The binding entry is ageout')
		else :
			r0.log(level='ERROR', message = 'The binding entry isnt ageout')

	else :
		r0.log(level='ERROR',message='The session isnt ageout! ')


	sendip (h0,protocol,phone1_ip,stund_ip,src_port1,stund_port);

	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	if address_list[0] == phone1_ip :
		r0.log(level='ERROR', message='Install one sessions without NAT. ')
	else :
		bind_entry_info = get_bind_entry(r0,phone1_ip,src_port1)

		if bind_entry_info[0] == '-' and bind_entry_info[1] == '60' and bind_entry_info[2] == '1' and bind_entry_info[3] == '10' and bind_entry_info[4] == 'src-nat-with-pat' and bind_entry_info[5] == 'target-host' and bind_entry_info[6] == 'cone_nat' :
			r0.log(level='INFO',message='Install one sessions by new_cone_nat rule')
		else:
			r0.log(level='ERROR', message= 'Install one sessions by new_cone_nat rule failed')
			raise Exception('')

	sendip (h0,protocol,phone1_ip,stund_ip,src_port2,stund_port)
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,stund_port,src_port2,protocol)

	if address_list[0] == phone1_ip :
		r0.log(level='ERROR', message='Install one sessions without NAT. ')

	else :

		bind_entry_info = get_bind_entry(r0,phone1_ip,src_port2)

		if bind_entry_info[0] == '-' and bind_entry_info[1] == '60' and bind_entry_info[2] == '1' and bind_entry_info[3] == '10' and bind_entry_info[4] == 'src-nat-with-pat' and bind_entry_info[5] == 'target-host' and bind_entry_info[6] == 'cone_nat' :
			r0.log(level='INFO',message='Install one sessions by new_cone_nat rule')
		else:
			r0.log(level='ERROR', message= 'Install one sessions by new_cone_nat rule failed')
			raise Exception('')


	r0.config(command_list=['delete security nat source rule-set src_nat rule cone_nat'])
	r0.commit(timeout=180)

	time.sleep(12)

	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)

	if bind_entry_info[0] == -1 :
		r0.log(level='INFO',message=' The binding entry is ageout')
	else :
		r0.log(level='ERROR', message= ' The binding entry isnt ageout')


	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port2)

	if bind_entry_info[0] == -1 :
		r0.log(level='INFO',message=' The binding entry is ageout')
	else :
		r0.log(level='ERROR', message= ' The binding entry isnt ageout')



	sendip(h0,protocol,phone2_ip,stund_ip,src_port1,stund_port)

	address_list=get_pst_nat_binding(r0,phone2_ip,stund_ip,src_port1,stund_port,protocol)

	if address_list[0] == phone2_ip :
		r0.log(level='ERROR', message='Install one sessions without NAT. ')

	else :

		bind_entry_info = get_bind_entry(r0,phone2_ip,src_port1)

		if bind_entry_info[0] == '-' and bind_entry_info[1] == '60' and bind_entry_info[2] == '1' and bind_entry_info[3] == '8' and bind_entry_info[4] == 'interface' and bind_entry_info[5] == 'target-host-port' and bind_entry_info[6] == 'cone_nat_2' :
			r0.log(level='INFO',message='Install one sessions by new_cone_nat_2 rule')
		else:
			r0.log(level='ERROR', message= 'Install one sessions by new_cone_nat_2 rule failed')
			raise Exception('')

	r0.config(command_list=['delete security nat source rule-set src_nat rule cone_nat_2'])
	r0.commit(timeout=180)


	time.sleep(12)

	bind_entry_info = get_bind_entry (r0, phone2_ip, src_port1)

	if bind_entry_info[0] == -1 :
		r0.log(level='INFO',message=' The binding entry is ageout')
	else :
 		r0.log(level='ERROR', message= ' The binding entry isnt ageout')



def change_pst_nat_rule_addr_mapping(r0,h0,protocol,phone1_ip,phone2_ip,stund_ip,src_port1,src_port2,stund_port,stund2_ip,da_net):

	'''
	Changes and verfies different persistent nat rules.

	'''


	r0.config(command_list=["set security nat source rule-set src_nat from zone trust",
  "set security nat source rule-set src_nat to zone untrust",
  "set security nat source rule-set src_nat rule cone_nat match source-address " + phone1_ip + "/28",
  "set security nat source rule-set src_nat rule cone_nat match destination-address "+ stund_ip + "/32",
  "set security nat source rule-set src_nat rule cone_nat match destination-address " + stund2_ip + "/32",
  "set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-by-shifting",
  "set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat address-mapping",
  "set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat permit any-remote-host",
  "set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat inactivity-timeout 120",
  "set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat max-session-number 20",  
  
  "set security policies from-zone trust to-zone untrust policy stun_traffic match destination-address DA_net",
  
  "set security policies from-zone untrust to-zone trust policy incoming match source-address DA_net",
  "set security policies from-zone untrust to-zone trust policy incoming match destination-address SA_net",
  "set security policies from-zone untrust to-zone trust policy incoming match application junos-persistent-nat",
  "set security policies from-zone untrust to-zone trust policy incoming then permit",
    
  "set security nat source rule-set src_nat rule cone_nat_2 match source-address " + phone1_ip + "/32",
  "set security nat source rule-set src_nat rule cone_nat_2 match source-address " + phone2_ip + "/32",
  "set security nat source rule-set src_nat rule cone_nat_2 match destination-address " + da_net,
  "set security nat source rule-set src_nat rule cone_nat_2 then source-nat pool src-nat-without-pat",
  "set security nat source rule-set src_nat rule cone_nat_2 then source-nat pool persistent-nat address-mapping",
    "set security nat source rule-set src_nat rule cone_nat_2 then source-nat pool persistent-nat permit any-remote-host",  
   "set security nat source rule-set src_nat rule cone_nat_2 then source-nat pool persistent-nat inactivity-timeout 60",
   "set security nat source rule-set src_nat rule cone_nat_2 then source-nat pool persistent-nat max-session-number 8"   ])

	
  

	r0.commit(timeout=180)

	sendip(h0,protocol,phone1_ip,stund_ip,src_port1,stund_port)
	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	bind_entry_info = get_bind_entry(r0,phone1_ip,'0')

	if bind_entry_info[0] == '-' and bind_entry_info[1] == '120' and bind_entry_info[2] == '1' and bind_entry_info[3] == '20' and bind_entry_info[4] == 'src-nat-by-shifting' and bind_entry_info[5] == 'any-remote-host' and bind_entry_info[6] == 'cone_nat' :
		r0.log(level='INFO',message='Install one sessions by cone_nat rule!')	
	else :
		r0.log(level='ERROR',message='Install one sessions by cone_nat rule failed')
		raise Exception('')



	r0.config(command_list=["set security nat source rule-set src_nat rule cone_nat then source-nat pool src-nat-without-pat",
		"set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat inactivity-timeout 60",
  	"set security nat source rule-set src_nat rule cone_nat then source-nat pool persistent-nat max-session-number 10" ])

	r0.commit(timeout=180)

	time.sleep(12)

	flow1=check_flow_session(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	if flow1 == 0 :
		r0.log(level='INFO',message='The session is ageout! ')
		bind_entry_info = get_bind_entry (r0, phone1_ip, '0')

		if bind_entry_info[0] == -1 :
			r0.log(level='INFO', message='The binding entry is ageout')
		else :
			r0.log(level='ERROR', message = 'The binding entry isnt ageout')

	else :
		r0.log(level='ERROR',message='The session isnt ageout! ')


	sendip (h0,protocol,phone1_ip,stund_ip,src_port1,stund_port);

	address_list=[]
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,src_port1,stund_port,protocol)

	if address_list[0] == phone1_ip :
		r0.log(level='ERROR', message='Install one sessions without NAT. ')
	else :
		bind_entry_info = get_bind_entry(r0,phone1_ip,'0')

		if bind_entry_info[0] == '-' and bind_entry_info[1] == '60' and bind_entry_info[2] == '1' and bind_entry_info[3] == '10' and bind_entry_info[4] == 'src-nat-without-pat' and bind_entry_info[5] == 'any-remote-host' and bind_entry_info[6] == 'cone_nat' :
			r0.log(level='INFO',message='Install one sessions by new_cone_nat rule')
		else:
			r0.log(level='ERROR', message= 'Install one sessions by new_cone_nat rule failed')
			raise Exception('')

	sendip (h0,protocol,phone1_ip,stund_ip,src_port2,stund_port)
	address_list=get_pst_nat_binding(r0,phone1_ip,stund_ip,stund_port,src_port2,protocol)

	if address_list[0] == phone1_ip :
		r0.log(level='ERROR', message='Install one sessions without NAT. ')

	else :

		bind_entry_info = get_bind_entry(r0,phone1_ip,'0')

		if bind_entry_info[0] == '-' and bind_entry_info[1] == '60' and bind_entry_info[2] == '2' and bind_entry_info[3] == '10' and bind_entry_info[4] == 'src-nat-without-pat' and bind_entry_info[5] == 'any-remote-host' and bind_entry_info[6] == 'cone_nat' :
			r0.log(level='INFO',message='Install one sessions by new_cone_nat rule')
		else:
			r0.log(level='ERROR', message= 'Install one sessions by new_cone_nat rule failed')
			raise Exception('')


	r0.config(command_list=['delete security nat source rule-set src_nat rule cone_nat'])
	r0.commit(timeout=180)

	time.sleep(12)

	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')

	if bind_entry_info[0] == -1 :
		r0.log(level='INFO',message=' The binding entry is ageout')
	else :
		r0.log(level='ERROR', message= ' The binding entry isnt ageout')

	bind_entry_info = get_bind_entry (r0,phone1_ip,'0')

	if bind_entry_info[0] == -1 :
		r0.log(level='INFO',message=' The binding entry is ageout')
	else :
		r0.log(level='ERROR', message= ' The binding entry isnt ageout')




	sendip(h0,protocol,phone2_ip,stund_ip,src_port1,stund_port)

	address_list=get_pst_nat_binding(r0,phone2_ip,stund_ip,src_port1,stund_port,protocol)

	if address_list[0] == phone2_ip :
		r0.log(level='ERROR', message='Install one sessions without NAT. ')

	else :

		bind_entry_info = get_bind_entry(r0,phone2_ip,'0')

		if bind_entry_info[0] == '-' and bind_entry_info[1] == '60' and bind_entry_info[2] == '1' and bind_entry_info[3] == '8' and bind_entry_info[4] == 'src-nat-without-pat' and bind_entry_info[5] == 'any-remote-host' and bind_entry_info[6] == 'cone_nat_2' :
			r0.log(level='INFO',message='Install one sessions by new_cone_nat_2 rule')
		else:
			r0.log(level='ERROR', message= 'Install one sessions by new_cone_nat_2 rule failed')
			raise Exception('')

	r0.config(command_list=['delete security nat source rule-set src_nat rule cone_nat_2'])
	r0.commit(timeout=180)


	time.sleep(12)

	bind_entry_info = get_bind_entry (r0, phone2_ip, '0')

	if bind_entry_info[0] == -1 :
		r0.log(level='INFO',message=' The binding entry is ageout')
	else :
		r0.log(level='ERROR', message= ' The binding entry isnt ageout')



def overflow_test(r0,h0,protocol,phone1_ip,stund_ip,src_port1,stund_port,timeout=None,max_session=None):

	'''
	
	Configures and verfies overflow pool.
	
	'''

	old_sa = phone1_ip + '/28'
	new_sa = phone1_ip + '/26'


	if timeout is None:
		timeout=300
	else:
		timeout=int(timeout)
	if max_session is None:
		max_session=30
	else:
		max_session=int(max_session)

	r0.config(command_list=['delete security nat source rule-set src_nat rule cone_nat match source-address ' + old_sa,
							'set security nat source rule-set src_nat rule cone_nat match source-address ' + new_sa, 
							'set security policies from-zone trust to-zone untrust policy stun_traffic match source-address SA_net'])

	r0.commit(timeout=180)


	if max_session > 20 :
		r0.config(command_list=['set applications application max_session protocol udp',
								'set applications application max_session source-port ' + src_port1,
								'set applications application max_session destination-port 0-65535',
								'set applications application max_session inactivity-timeout 300',
								'delete security policies from-zone trust to-zone untrust policy source-nat match application any',
								'set security policies from-zone trust to-zone untrust policy source-nat match application max_session'
								])
		r0.commit(timeout=180)

	src_ip = ''
	for ip in range(196,217):
		src_ip = '10.10.10.' + str(ip)
		sendip(h0,protocol,src_ip,stund_ip,src_port1,stund_port)

	address_list=[]
	address_list=get_pst_nat_binding(r0,'10.10.10.206',stund_ip,src_port1,stund_port,protocol,1)

	split_list=address_list[0].split(".")

	if int(split_list[0]) == 200 and int(split_list[1]) == 200 and int(split_list[2]) >= 1 and int(split_list[3]) <=10 :
		r0.log(level='INFO',message= address_list[0] + 'is in the value of 200.200.200.1 <-> 200.200.200.10!')
		
		if address_list[1] != src_port1 :
			r0.log(level='INFO' , message='Ports are not equal')
		else :
			r0.log(level='ERROR', message='Ports are equal')

	else :
		r0.log(level='ERROR', message=address_list[0] + ' is not in the value of 200.200.200.1 <-> 200.200.200.10! ')
	
	r0.cli(command='clear security flow session source-prefix 10.10.10. ' )

	time.sleep(10)

	r0.log(level='INFO', message="\n Wait " + str(timeout) + " seconds for binding entry timeout. ")

	time.sleep(timeout)

	bind_entry_info = get_bind_entry (r0,phone1_ip,src_port1)

	if bind_entry_info[0] != -1 :
		r0.log(level='ERROR',message="\n ******bind entry still exists. *******\n\n")
	else:
		r0.log(level='INFO', message="\n ******bind entry ageout successfully. ******* \n\n")


def get_flow_session_list(device):

	'''
		Returns inbound and outbound source and destination list from the session.

	'''

	if device is None:
		raise Exception("'device' is mandatory parameter - device handle")
	if device is not None:
		device.cli(command='show security flow session').response()
		result = device.cli(command='show security flow session', format='xml').response()
		status = jxmlease.parse(result)
		device.log(status)


		if int(status['rpc-reply']['flow-session-information']['displayed-session-count']) > 0 :

			in_src = (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['source-address'])
			in_dest = (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['destination-address'])	
			out_src = (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['source-address'])
			out_dest = (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['destination-address'])	

			sess_list = [in_src, in_dest, out_src, out_dest]
			return sess_list

		else:

			sess_list = [-1]
			return sess_list

def traffic_telnet(h0, ip) :

	'''
	Starts the telnet traffic

	'''

	uname = "regress"
	upassword ="MaRtInI"

	h0.shell(command="telnet " + ip , pattern="login: ", timeout=5, timeout_ok="true")
	time.sleep(1); 
	h0.shell(command="regress", pattern="Password", timeout_ok="true")
	time.sleep(1); 
	h0.shell(command="MaRtInI", pattern="\$", timeout_ok="true") 
	time.sleep(1) 
	h0.shell(command="ls", pattern="\$", timeout_ok="true")

	return 1


def basic_test_shifting_ICMP(r0,h0,h1):

	r0.log(level='INFO',message='Configuring Widecaset and NAT shift on DUT')

	r0.config(command_list=["delete security", 
      "set security zones security-zone reth0z host-inbound-traffic system-services all",
      "set security zones security-zone reth0z host-inbound-traffic protocols all",
      "set security zones security-zone reth0z interfaces " + t['resources']['box']['interfaces']['r0h0']['pic'],
      "set security zones security-zone reth1z host-inbound-traffic system-services all",
      "set security zones security-zone reth1z host-inbound-traffic protocols all",
      "set security zones security-zone reth1z interfaces " + t['resources']['box']['interfaces']['r0h1']['pic'],

      
      "set security nat source pool src1 address 100.0.0.1/32 to 100.0.0.10/32",
      "set security nat source pool src1 host-address-base 10.10.10.2/32",
      "set security nat source rule-set r1 from zone reth0z",
      "set security nat source rule-set r1 to zone reth1z",
      "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.0/24",
      "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
      "set security nat source rule-set r1 rule rule1 then source-nat pool src1",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat permit any-remote-host",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat address-mapping",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat inactivity-timeout 400",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat max-session-number 20",
      "set security nat source rule-set r2 from zone reth0z",
      "set security nat source rule-set r2 to zone reth0z",
      "set security nat source rule-set r2 rule rule2 match source-address 10.10.10.0/24",
      "set security nat source rule-set r2 rule rule2 match destination-address 10.10.10.0/24",
      "set security nat source rule-set r2 rule rule2 then source-nat pool src1",
      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat permit any-remote-host",
      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat address-mapping",
      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat inactivity-timeout 400",
      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat max-session-number 20",
      
      "set security policies from-zone reth0z to-zone reth1z policy p1 match source-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match destination-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match application any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 then permit",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match source-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match destination-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match application any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 then permit",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match source-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match destination-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match application any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 then permit",
      "set security policies default-policy deny-all"])

	r0.commit(timeout=180)

	time.sleep(10)

	split_ip = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')

	h0.shell(command='ping ' + split_ip[0] + ' -c 1')

	cmd="show security nat source persistent-nat-table internal-ip " + split_ip_2[0] + " internal-port 0"
	result = r0.cli(command=cmd, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	
	pst_nat_ip = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']

	if pst_nat_ip == "" :
		r0.log(level='ERROR', message='Cone nat failed')
		raise Exception('')

	if pst_nat_ip is not None :
		response2= traffic_telnet(h1,pst_nat_ip)

	r0.cli(command='show security flow session destination-prefix ' + pst_nat_ip )

	if response2 == 0 :
		r0.log(level='ERROR', message='telnet should fails from $h[0] to $pst_nat_ip_1')
		raise Exception('')

	session_list = get_flow_session_list(r0)

	if session_list[0] != -1 :
		r0.log(level='INFO',message='In src ' + session_list[0])
		r0.log(level='INFO',message='In dest ' + session_list[1])
		r0.log(level='INFO',message='Out src ' + session_list[2])
		r0.log(level='INFO',message='Out dest ' + session_list[3])

	else :
		r0.log(level='ERROR',message='Cant find session')
		raise Exception('')

	h1.shell(command='exit')


	if session_list[2] != split_ip_2[0] :
		r0.log(level='ERROR',message='Full_cone_basic_shifting_ICMP Fail!!')
		raise Exception('')


	if session_list[3] != split_ip[0] :
		r0.log(level='ERROR',message='Full_cone_basic_shifting_ICMP Fail!!')
		raise Exception('')

	time.sleep(20)

	r0.cli(command='clear security nat source persistent-nat-table all')


def basic_test_withoutPAT_ICMP(r0,h0,h1):

	r0.log(level='INFO',message='Configuring Widecaset and NAT shift on DUT')

	r0.config(command_list=[ "delete security", 
      "set security zones security-zone reth0z host-inbound-traffic system-services all",
      "set security zones security-zone reth0z host-inbound-traffic protocols all",
      "set security zones security-zone reth0z interfaces " + t['resources']['box']['interfaces']['r0h0']['pic'],
      "set security zones security-zone reth1z host-inbound-traffic system-services all",
      "set security zones security-zone reth1z host-inbound-traffic protocols all",
      "set security zones security-zone reth1z interfaces " + t['resources']['box']['interfaces']['r0h1']['pic'],

      
      "set security nat source pool src1 address 100.0.0.1/32 to 100.0.0.10/32",
      "set security nat source pool src1 port no-translation",
      "set security nat source rule-set r1 from zone reth0z",
      "set security nat source rule-set r1 to zone reth1z",
      "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.0/24",
      "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
      "set security nat source rule-set r1 rule rule1 then source-nat pool src1",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat permit any-remote-host",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat address-mapping",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat inactivity-timeout 400",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat max-session-number 20",
      "set security nat source rule-set r2 from zone reth0z",
      "set security nat source rule-set r2 to zone reth0z",
      "set security nat source rule-set r2 rule rule2 match source-address 10.10.10.0/24",
      "set security nat source rule-set r2 rule rule2 match destination-address 10.10.10.0/24",
      "set security nat source rule-set r2 rule rule2 then source-nat pool src1",
      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat permit any-remote-host",
      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat address-mapping",
      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat inactivity-timeout 400",
      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat max-session-number 20",
      
      "set security policies from-zone reth0z to-zone reth1z policy p1 match source-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match destination-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match application any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 then permit",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match source-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match destination-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match application any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 then permit",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match source-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match destination-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match application any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 then permit",
      "set security policies default-policy deny-all"])

	r0.commit(timeout=180)

	time.sleep(10)

	split_ip = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')

	h0.shell(command='ping ' + split_ip[0] + ' -c 1')

	cmd="show security nat source persistent-nat-table internal-ip " + split_ip_2[0] + " internal-port 0"
	result = r0.cli(command=cmd, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	
	pst_nat_ip = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']

	if pst_nat_ip == "" :
		r0.log(level='ERROR', message='Cone nat failed')
		raise Exception('')

	if pst_nat_ip is not None :
		response2= traffic_telnet(h1,pst_nat_ip)

	r0.cli(command='show security flow session destination-prefix ' + pst_nat_ip )

	if response2 == 0 :
		r0.log(level='ERROR', message='telnet should fails from $h[0] to $pst_nat_ip_1')
		raise Exception('')

	session_list = get_flow_session_list(r0)

	if session_list[0] != -1 :
		r0.log(level='INFO',message='In src ' + session_list[0])
		r0.log(level='INFO',message='In dest ' + session_list[1])
		r0.log(level='INFO',message='Out src ' + session_list[2])
		r0.log(level='INFO',message='Out dest ' + session_list[3])

	else :
		r0.log(level='ERROR',message='Cant find session')
		raise Exception('')

	h1.shell(command='exit')


	if session_list[2] != split_ip_2[0] :
		r0.log(level='ERROR',message='Full_cone_basic_shifting_ICMP Fail!!')
		raise Exception('')


	if session_list[3] != split_ip[0] :
		r0.log(level='ERROR',message='Full_cone_basic_shifting_ICMP Fail!!')
		raise Exception('')

	time.sleep(20)

	r0.cli(command='clear security nat source persistent-nat-table all')

def check_config_widecast_PAT(r0):

	r0.log(level='INFO',message='Configuring Widecaset and PAT NAT on DUT')

	r0.config(command_list=["set security nat source pool src1 address 100.0.0.1/32 to 100.0.0.10/32",
 "set security nat source rule-set r1 from zone trust",
  "set security nat source rule-set r1 to zone untrust",
  "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.2/32",
  "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
  "set security nat source rule-set r1 rule rule1 then source-nat pool src1",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat permit any-remote-host",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat address-mapping",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat inactivity-timeout 60",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat max-session-number 20"
			])


	try:
		r0.commit(timeout=180)
	except:
		r0.log(level='INFO', message='Check Source NAT PAT and Widecast config Pass!!!')
	else :
		r0.log(level='ERROR', message='Check Source NAT PAT and Widecast config Fail!!!')
		raise Exception('')

	r0.config(command_list=['rollback'])
	r0.commit(timeout=180)

def check_config_widecast_interface_snat(r0):

	r0.log(level='INFO',message=" Configuring Widecaset and interface Source NAT on DUT.")
  
	r0.config (command_list=["set security nat source rule-set r1 from zone trust",
  "set security nat source rule-set r1 to zone untrust",
  "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.2/32",
  "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
  "set security nat source rule-set r1 rule rule1 then source-nat interface",
  "set security nat source rule-set r1 rule rule1 then source-nat interface persistent-nat permit any-remote-host",
  "set security nat source rule-set r1 rule rule1 then source-nat interface persistent-nat address-mapping",
  "set security nat source rule-set r1 rule rule1 then source-nat interface persistent-nat inactivity-timeout 60",
  "set security nat source rule-set r1 rule rule1 then source-nat interface persistent-nat max-session-number 20"
  			])


	try:
		r0.commit(timeout=180)
	except:
		r0.log(level='INFO', message='Check Interface Source NAT and Widecast config Pass!!!')
	else :
		r0.log(level='ERROR', message='Check Interface Source NAT and Widecast config Fail!!!')
		raise Exception('')

	r0.config(command_list=['rollback'])
	r0.commit(timeout=180)

def check_config_widecast_targethost(r0):

	r0.log(level='INFO',message=" Configuring Widecaset and interface Source NAT on DUT.")

	r0.config(command_list=["set security nat source pool src1 address 100.0.0.1/32 to 100.0.0.10/32",
  "set security nat source pool src1 port no-translation",
  "set security nat source rule-set r1 from zone trust",
  "set security nat source rule-set r1 to zone untrust",
  "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.2/32",
 "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
  "set security nat source rule-set r1 rule rule1 then source-nat pool src1",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat permit target-host",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat address-mapping",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat inactivity-timeout 60",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat max-session-number 20"
	])


	try:
		r0.commit(timeout=180)
	except:
		r0.log(level='INFO', message='Check Target-host and Widecast config Pass!!!')
	else :
		r0.log(level='ERROR', message='Check Target-host and Widecast config Fails!!!')
		raise Exception('')

	r0.config(command_list=['rollback'])
	r0.commit(timeout=180)

def check_config_widecast_interface_targethostport(r0):

	r0.log(level='INFO',message=" Configuring Widecaset and target-host-port on DUT.")


	r0.config(command_list=["set security nat source pool src1 address 100.0.0.1/32 to 100.0.0.10/32",
  "set security nat source pool src1 port no-translation",
  "set security nat source rule-set r1 from zone trust",
 "set security nat source rule-set r1 to zone untrust",
  "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.2/32",
  "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
  "set security nat source rule-set r1 rule rule1 then source-nat pool src1",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat permit target-host-port",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat address-mapping",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat inactivity-timeout 60",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat max-session-number 20"])


	try:
		r0.commit(timeout=180)
	except:
		r0.log(level='INFO', message='Check Target-host-port and Widecast config Pass!!!')
	else :
		r0.log(level='ERROR', message='Check Target-host-port and Widecast config Fails!!!')
		raise Exception('')

	r0.config(command_list=['rollback'])
	r0.commit(timeout=180)

def check_config_widecast_overflowpool(r0):

	r0.log(level='INFO',message=" Configuring Widecaset and NAT overflow-pool on DUT.")

	r0.config(command_list=["set security nat source pool src-nat-without-pat address 100.0.0.10/32 to 100.0.0.20/32",
  "set security nat source pool src-nat-without-pat port no-translation",
  "set security nat source pool src-nat-with-pat address 100.0.0.30/32 to 100.0.0.40/32",
 
  "set security nat source pool src-nat-without-pat overflow-pool src-nat-with-pat",
  "set security nat source rule-set r1 from zone trust",
  "set security nat source rule-set r1 to zone untrust",
  "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.2/32",
  "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
  "set security nat source rule-set r1 rule rule1 then source-nat pool src-nat-without-pat",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat permit any-remote-host",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat address-mapping",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat inactivity-timeout 60",
  "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat max-session-number 20" ])

	try:
		r0.commit(timeout=180)
	except:
		r0.log(level='INFO', message='Check Source NAT overflow-pool and Widecast config Pass!!!')
	else :
		r0.log(level='ERROR', message='Check Source NAT overflow-pool and Widecast config Fails!!!')
		raise Exception('')

	r0.config(command_list=['rollback'])
	r0.commit(timeout=180)

def full_cone_shifting_tcp(r0,h0,h1,h2):

	r0.log(level='INFO', message='Configuring Widecaset and NAT shift on DUT')

	r0.config(command_list=["delete security", 
      "set security zones security-zone reth0z host-inbound-traffic system-services all",
      "set security zones security-zone reth0z host-inbound-traffic protocols all",

      "set security zones security-zone reth0z interfaces " +  t['resources']['box']['interfaces']['r0h1']['pic'],
      "set security zones security-zone reth1z host-inbound-traffic system-services all",
      "set security zones security-zone reth1z host-inbound-traffic protocols all",
      "set security zones security-zone reth1z interfaces " +  t['resources']['box']['interfaces']['r0h0']['pic'],

      
      "set security nat source pool src1 address 100.0.0.1/32 to 100.0.0.10/32",
      "set security nat source pool src1 host-address-base 10.10.10.2/32",
      "set security nat source rule-set r1 from zone reth0z",
      "set security nat source rule-set r1 to zone reth1z",
      "set security nat source rule-set r1 to zone reth0z",

      "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.0/24",
      "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
       "set security nat source rule-set r1 rule rule1 match destination-address 10.10.10.0/24",

      "set security nat source rule-set r1 rule rule1 then source-nat pool src1",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat permit any-remote-host",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat address-mapping",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat inactivity-timeout 400",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat max-session-number 20",

      "set security policies from-zone reth0z to-zone reth1z policy p1 match source-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match destination-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match application any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 then permit",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match source-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match destination-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match application any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 then permit",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match source-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match destination-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match application any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 then permit",
      "set security policies default-policy deny-all"])

	r0.commit(timeout=180)

	time.sleep(10)

	split_ip = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['lnx3']['interfaces']['r0h2']['uv-ip']).split('/')


	response1 = traffic_telnet(h0, split_ip[0] )


	if response1 == 0 :
		r0.log(level='ERROR',message='Telnet fails')


	cmd="show security nat source persistent-nat-table internal-ip " + split_ip_2[0] 
	result = r0.cli(command=cmd, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry'] == "" :
		r0.log(level='ERROR', message='Cone nat failed')
		raise Exception('')
	else :
		pst_nat_ip_1 = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']
		r0.log(level='INFO',message='REFLEXIVE IP : ' + pst_nat_ip_1)
		
	h0.shell(command='exit')

	response1 = traffic_telnet(h2, split_ip[0] )


	if response1 == 0 :
		r0.log(level='ERROR',message='Telnet fails')


	cmd="show security nat source persistent-nat-table internal-ip " + split_ip_3[0] 
	result = r0.cli(command=cmd, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry'] == "" :
		r0.log(level='ERROR', message='Cone nat failed')
		raise Exception('')
	else :
		pst_nat_ip_2 = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']
		r0.log(level='INFO',message='REFLEXIVE IP : ' + pst_nat_ip_2)
		
	h2.shell(command='exit')

	response2= traffic_telnet(h0,pst_nat_ip_2)

	r0.cli(command='show security flow session destination-prefix ' + pst_nat_ip_2 )

	if response2 == 0 :
		r0.log(level='ERROR', message='telnet should fails from $h[0] to $pst_nat_ip_1')
		raise Exception('')

	session_list = get_flow_session_list(r0)

	if session_list[0] != -1 :
		r0.log(level='INFO',message='In src ' + session_list[0])
		r0.log(level='INFO',message='In dest ' + session_list[1])
		r0.log(level='INFO',message='Out src ' + session_list[2])
		r0.log(level='INFO',message='Out dest ' + session_list[3])

	else :
		r0.log(level='ERROR',message='Cant find session')
		raise Exception('')

	h0.shell(command='exit')

	if session_list[3] == pst_nat_ip_1 :
		r0.log(level='INFO',message='Full_cone_shifting_hairpinning_tcp pass!!')
	else:
		r0.log(level='INFO',message='Full_cone_shifting_hairpinning_tcp fails!!')
		raise Exception('')

	r0.cli(command="clear security flow session destination-prefix " + pst_nat_ip_2)
	r0.cli(command="clear security nat source persistent-nat-table all")


	
def full_cone_withoutPAT_tcp(r0,h0,h1,h2):

	r0.log(level='INFO',message='Configuring Widecaset and NAT shift on DUT.')

	r0.config(command_list=["delete security", 
      "set security zones security-zone reth0z host-inbound-traffic system-services all",
      "set security zones security-zone reth0z host-inbound-traffic protocols all",
      "set security zones security-zone reth0z interfaces " + t['resources']['box']['interfaces']['r0h0']['pic'],
      "set security zones security-zone reth1z host-inbound-traffic system-services all",
      "set security zones security-zone reth1z host-inbound-traffic protocols all",
      "set security zones security-zone reth1z interfaces " + t['resources']['box']['interfaces']['r0h1']['pic'],

      
      "set security nat source pool src1 address 100.0.0.1/32 to 100.0.0.10/32",
      "set security nat source pool src1 port no-translation",
      "set security nat source rule-set r1 from zone reth0z",
      "set security nat source rule-set r1 to zone reth1z",
      "set security nat source rule-set r1 to zone reth0z", 
      "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.0/24",
      "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
      "set security nat source rule-set r1 rule rule1 match destination-address 10.10.10.0/24",  
      "set security nat source rule-set r1 rule rule1 then source-nat pool src1",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat permit any-remote-host",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat address-mapping",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat inactivity-timeout 400",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat max-session-number 20",

      
      "set security policies from-zone reth0z to-zone reth1z policy p1 match source-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match destination-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match application any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 then permit",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match source-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match destination-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match application any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 then permit",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match source-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match destination-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match application any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 then permit",
      "set security policies default-policy deny-all"])


	r0.commit(timeout=180)

	time.sleep(10)

	split_ip = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['lnx3']['interfaces']['r0h2']['uv-ip']).split('/')


	response1 = traffic_telnet(h0, split_ip[0] )


	if response1 == 0 :
		r0.log(level='ERROR',message='Telnet fails')


	cmd="show security nat source persistent-nat-table internal-ip " + split_ip_2[0] 
	result = r0.cli(command=cmd, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry'] == "" :
		r0.log(level='ERROR', message='Cone nat failed')
		raise Exception('')
	else :
		pst_nat_ip_1 = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']
		r0.log(level='INFO',message='REFLEXIVE IP : ' + pst_nat_ip_1)
		
	h0.shell(command='exit')

	response1 = traffic_telnet(h2, split_ip[0] )


	if response1 == 0 :
		r0.log(level='ERROR',message='Telnet fails')


	cmd="show security nat source persistent-nat-table internal-ip " + split_ip_3[0] 
	result = r0.cli(command=cmd, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry'] == "" :
		r0.log(level='ERROR', message='Cone nat failed')
		raise Exception('')
	else :
		pst_nat_ip_2 = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']
		r0.log(level='INFO',message='REFLEXIVE IP : ' + pst_nat_ip_2)
		
	h2.shell(command='exit')

	response2= traffic_telnet(h0,pst_nat_ip_2)

	r0.cli(command='show security flow session destination-prefix ' + pst_nat_ip_2 )

	if response2 == 0 :
		r0.log(level='ERROR', message='telnet should fails from $h[0] to $pst_nat_ip_1')
		raise Exception('')

	session_list = get_flow_session_list(r0)

	if session_list[0] != -1 :
		r0.log(level='INFO',message='In src ' + session_list[0])
		r0.log(level='INFO',message='In dest ' + session_list[1])
		r0.log(level='INFO',message='Out src ' + session_list[2])
		r0.log(level='INFO',message='Out dest ' + session_list[3])

	else :
		r0.log(level='ERROR',message='Cant find session')
		raise Exception('')

	h0.shell(command='exit')

	if session_list[3] == pst_nat_ip_1 :
		r0.log(level='INFO',message='Full_cone_shifting_hairpinning_tcp pass!!')
	else:
		r0.log(level='INFO',message='Full_cone_shifting_hairpinning_tcp fails!!')
		raise Exception('')

	r0.cli(command="clear security flow session destination-prefix " + pst_nat_ip_2)
	r0.cli(command="clear security nat source persistent-nat-table all")





def full_cone_withoutPAT_ICMP(r0,h0,h1,h2):

	r0.log(level='INFO', message='Configuring Widecaset and NAT shift on DUT.')

	r0.config(command_list=["delete security", 
      "set security zones security-zone reth0z host-inbound-traffic system-services all",
      "set security zones security-zone reth0z host-inbound-traffic protocols all",
      "set security zones security-zone reth0z interfaces " + t['resources']['box']['interfaces']['r0h0']['pic'],
      "set security zones security-zone reth1z host-inbound-traffic system-services all",
      "set security zones security-zone reth1z host-inbound-traffic protocols all",
      "set security zones security-zone reth1z interfaces " + t['resources']['box']['interfaces']['r0h1']['pic'],

      
      "set security nat source pool src1 address 100.0.0.1/32 to 100.0.0.10/32",
      "set security nat source pool src1 port no-translation",
      "set security nat source rule-set r1 from zone reth0z",
      "set security nat source rule-set r1 to zone reth1z",
      "set security nat source rule-set r1 to zone reth0z",
      "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.0/24",
      "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
      "set security nat source rule-set r1 rule rule1 match destination-address 10.10.10.0/24",

      "set security nat source rule-set r1 rule rule1 then source-nat pool src1",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat permit any-remote-host",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat address-mapping",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat inactivity-timeout 400",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat max-session-number 20",
 #     "set security nat source rule-set r2 from zone reth0z",
 #     "set security nat source rule-set r2 to zone reth0z",
 #     "set security nat source rule-set r2 rule rule2 match source-address 10.10.10.0/24",
 #     "set security nat source rule-set r2 rule rule2 match destination-address 10.10.10.0/24",
 #     "set security nat source rule-set r2 rule rule2 then source-nat pool src1",
 #     "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat permit any-remote-host",
 #     "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat address-mapping",
 #     "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat inactivity-timeout 400",
 #     "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat max-session-number 20",
      
      "set security policies from-zone reth0z to-zone reth1z policy p1 match source-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match destination-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match application any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 then permit",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match source-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match destination-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match application any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 then permit",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match source-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match destination-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match application any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 then permit",
      "set security policies default-policy deny-all"])

	r0.commit(timeout=180)

	time.sleep(10)

	split_ip = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['lnx3']['interfaces']['r0h2']['uv-ip']).split('/')


	h0.shell(command='ping ' + split_ip[0] + ' -c 1')

	cmd="show security nat source persistent-nat-table internal-ip " + split_ip_2[0] 
	result = r0.cli(command=cmd, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	
	pst_nat_ip = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']

	if pst_nat_ip == "" :
		r0.log(level='ERROR', message='Cone nat failed')
		raise Exception('')


	h2.shell(command='ping ' + split_ip[0] + ' -c 1')

	cmd="show security nat source persistent-nat-table internal-ip " + split_ip_3[0] 
	result = r0.cli(command=cmd, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry'] == "" :
		r0.log(level='ERROR', message='Cone nat failed')
		raise Exception('')
	else :
		pst_nat_ip_2 = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']
		r0.log(level='INFO',message='REFLEXIVE IP : ' + pst_nat_ip_2)
		

	response2= traffic_telnet(h0,pst_nat_ip_2)

	r0.cli(command='show security flow session destination-prefix ' + pst_nat_ip_2 )

	if response2 == 0 :
		r0.log(level='ERROR', message='telnet should fails from $h[0] to $pst_nat_ip_1')
		raise Exception('')

	session_list = get_flow_session_list(r0)

	if session_list[0] != -1 :
		r0.log(level='INFO',message='In src ' + session_list[0])
		r0.log(level='INFO',message='In dest ' + session_list[1])
		r0.log(level='INFO',message='Out src ' + session_list[2])
		r0.log(level='INFO',message='Out dest ' + session_list[3])

	else :
		r0.log(level='ERROR',message='Cant find session')
		raise Exception('')

	h0.shell(command='exit')

	if session_list[3] == pst_nat_ip_1 :
		r0.log(level='INFO',message='Full_cone_withoutPAT_hairpinning_ICMP pass!!')
	else:
		r0.log(level='INFO',message='Full_cone_withoutPAT_hairpinning_ICMP Fails!!')
		raise Exception('')

	r0.cli(command="clear security flow session destination-prefix " + pst_nat_ip_2)
	r0.cli(command="clear security nat source persistent-nat-table all")


def full_cone_shifting_ICMP(r0,h0,h1,h2):

	r0.log(level='INFO',message=' Configuring Widecaset and NAT shift on DUT.')

	r0.config(command_list=["delete security", 
      "set security zones security-zone reth0z host-inbound-traffic system-services all",
      "set security zones security-zone reth0z host-inbound-traffic protocols all",
      "set security zones security-zone reth0z interfaces " + t['resources']['box']['interfaces']['r0h0']['pic'],
      "set security zones security-zone reth1z host-inbound-traffic system-services all",
      "set security zones security-zone reth1z host-inbound-traffic protocols all",
      "set security zones security-zone reth1z interfaces " + t['resources']['box']['interfaces']['r0h1']['pic'],

      
      "set security nat source pool src1 address 100.0.0.1/32 to 100.0.0.10/32",
      "set security nat source pool src1 host-address-base 10.10.10.2/32",
      "set security nat source rule-set r1 from zone reth0z",
      "set security nat source rule-set r1 to zone reth1z",
      "set security nat source rule-set r1 to zone reth0z", 
      "set security nat source rule-set r1 rule rule1 match source-address 10.10.10.0/24",
      "set security nat source rule-set r1 rule rule1 match destination-address 20.20.20.2/32",
      "set security nat source rule-set r1 rule rule1 match destination-address 10.10.10.0/24",
      "set security nat source rule-set r1 rule rule1 then source-nat pool src1",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat permit any-remote-host",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat address-mapping",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat inactivity-timeout 400",
      "set security nat source rule-set r1 rule rule1 then source-nat pool persistent-nat max-session-number 20",
#      "set security nat source rule-set r2 from zone reth0z",
#      "set security nat source rule-set r2 to zone reth0z",
#      "set security nat source rule-set r2 rule rule2 match source-address 10.10.10.0/24",
#      "set security nat source rule-set r2 rule rule2 match destination-address 10.10.10.0/24",
#      "set security nat source rule-set r2 rule rule2 then source-nat pool src1",
#      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat permit any-remote-host",
#      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat address-mapping",
#      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat inactivity-timeout 400",
#      "set security nat source rule-set r2 rule rule2 then source-nat pool persistent-nat max-session-number 20",
      
      "set security policies from-zone reth0z to-zone reth1z policy p1 match source-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match destination-address any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 match application any",
      "set security policies from-zone reth0z to-zone reth1z policy p1 then permit",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match source-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match destination-address any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 match application any",
      "set security policies from-zone reth1z to-zone reth0z policy p2 then permit",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match source-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match destination-address any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 match application any",
      "set security policies from-zone reth0z to-zone reth0z policy p3 then permit",
      "set security policies default-policy deny-all"])

	r0.commit(timeout=180)

	time.sleep(10)

	split_ip = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['lnx3']['interfaces']['r0h2']['uv-ip']).split('/')


	h0.shell(command='ping ' + split_ip[0] + ' -c 1')

	cmd="show security nat source persistent-nat-table internal-ip " + split_ip_2[0] 
	result = r0.cli(command=cmd, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	
	pst_nat_ip = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']

	if pst_nat_ip == "" :
		r0.log(level='ERROR', message='Cone nat failed')
		raise Exception('')


	h2.shell(command='ping ' + split_ip[0] + ' -c 1')

	cmd="show security nat source persistent-nat-table internal-ip " + split_ip_3[0] 
	result = r0.cli(command=cmd, format='xml').response()
	status = jxmlease.parse(result)
	r0.log(status)

	if status['rpc-reply']['persist-nat-table']['persist-nat-table-entry'] == "" :
		r0.log(level='ERROR', message='Cone nat failed')
		raise Exception('')
	else :
		pst_nat_ip_2 = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']
		r0.log(level='INFO',message='REFLEXIVE IP : ' + pst_nat_ip_2)
		

	response2= traffic_telnet(h0,pst_nat_ip_2)

	r0.cli(command='show security flow session destination-prefix ' + pst_nat_ip_2 )

	if response2 == 0 :
		r0.log(level='ERROR', message='telnet should fails from $h[0] to $pst_nat_ip_1')
		raise Exception('')

	session_list = get_flow_session_list(r0)

	if session_list[0] != -1 :
		r0.log(level='INFO',message='In src ' + session_list[0])
		r0.log(level='INFO',message='In dest ' + session_list[1])
		r0.log(level='INFO',message='Out src ' + session_list[2])
		r0.log(level='INFO',message='Out dest ' + session_list[3])

	else :
		r0.log(level='ERROR',message='Cant find session')
		raise Exception('')

	h0.shell(command='exit')

	if session_list[3] == pst_nat_ip_1 :
		r0.log(level='INFO',message='Full_cone_shifting_hairpinning_ICMP Pass!')
	else:
		r0.log(level='INFO',message='Full_cone_shifting_hairpinning_ICMP Fails!!')
		raise Exception('')

	r0.cli(command="clear security flow session destination-prefix " + pst_nat_ip_2)
	r0.cli(command="clear security nat source persistent-nat-table all")



def initial_config(r0=None, h0=None, h1=None, h2=None):

	'''

	Loads configutation on linux machines and interfaces on DUT

	'''
	'''Configuring on H0'''
	
	h0.su()
	h0.shell(command='/sbin/service network restart')
	h0.shell(command='/sbin/ifconfig ' + t['resources']['lnx1']['interfaces']['r0h0']['pic'] + ' down')
	h0.shell(command="/sbin/ifconfig " + t['resources']['lnx1']['interfaces']['r0h0']['pic'] + " 10.10.10.2 netmask 255.255.255.0 up")
	h0.shell(command='/sbin/route add -net 100.0.0.0/24 gw 10.10.10.254')
	h0.shell(command="/sbin/route add -net 20.20.20.0  netmask 255.255.255.0 gw 10.10.10.254")
	

	'''Configuring on H1'''

	h1.su()
	h1.shell(command='/sbin/ifconfig ' + t['resources']['lnx2']['interfaces']['r0h1']['pic'] + ' down')
	h1.shell(command="/sbin/ifconfig " + t['resources']['lnx2']['interfaces']['r0h1']['pic'] + " 20.20.20.2 netmask 255.255.255.0 up")
	h1.shell(command="/sbin/route add -net 200.200.200.0/24 gw 20.20.20.254")
	h1.shell(command='/sbin/route add -net 10.10.10.0/24 gw 20.20.20.254')
	h1.shell(command='/sbin/route add -net 100.0.0.0/24 gw 20.20.20.254')


	h2.su()
	h2.shell(command='/sbin/ifconfig ' + t['resources']['lnx3']['interfaces']['r0h2']['pic'] + ' down')
	h2.shell(command="/sbin/ifconfig " + t['resources']['lnx3']['interfaces']['r0h2']['pic'] + " 10.10.10.10 netmask 255.255.255.0 up")
	h2.shell(command="/sbin/route add -net 100.0.0.0/24 gw 10.10.10.254")
	h2.shell(command='/sbin/route add -net 20.20.20.0/24 gw 10.10.10.254')


	h0.shell(command='/sbin/ifconfig eth1 10.10.10.2 netmask 255.255.255.0 up')
	h0.shell(command='exit')
	h1.shell(command='/sbin/ifconfig eth1 20.20.20.2 netmask 255.255.255.0 up')
	h1.shell(command='exit')
	h2.shell(command='/sbin/ifconfig eth1 10.10.10.10 netmask 255.255.255.0 up')
	h2.shell(command='exit')



	



	r0.config(command_list=["set interfaces " + t['resources']['box']['interfaces']['r0h0']['pic']+ " unit 0 family inet address " + t['resources']['box']['interfaces']['r0h0']['uv-ip'],
	"set interfaces " + t['resources']['box']['interfaces']['r0h1']['pic']+ " unit 0 family inet address " + t['resources']['box']['interfaces']['r0h1']['uv-ip']
                        ])
	r0.commit(timeout=180)



def get_reflexive_ip(device,internal_ip,internal_port,protocol=None):

	if protocol is not None:
		result = device.cli(command="show security nat source persistent-nat-table internal-ip "+internal_ip + " internal-port "+internal_port + " internal-protocol " + protocol,format='xml').response()
		status = jxmlease.parse(result)
		device.log(status)
	else :
		result = device.cli(command="show security nat source persistent-nat-table internal-ip "+internal_ip + " internal-port "+internal_port,format='xml').response()
		status = jxmlease.parse(result)
		device.log(status)

	if status['rpc-reply']['persist-nat-table'] != "":

		device.log(level='INFO',message='Reflexvi ip : ' + status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip'])
		device.log(level='INFO',message='In Ip : ' + status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-port'])
		device.log(level='INFO',message='Protocol : ' + status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-proto'])
		device.log(level='INFO',message='In Ip : ' + status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-internal-ip'])


		reflexive_ip = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-ip']
		reflexive_port = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-port']
		proto = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-reflexive-proto']
		in_ip = status['rpc-reply']['persist-nat-table']['persist-nat-table-entry']['persist-nat-internal-ip']
		result = [reflexive_ip,proto,reflexive_port,in_ip]
		return result

	else :

		device.cli(command='clear security flow session')
		time.sleep(5)
		device.cli(command='clear security nat source persistent-nat-table all')

		raise Exception('No persistent-nat-table entry found')


def verify_flow_session_list(device,h0,ref_ip):

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')

	sess_list = get_flow_session_list(device)

	if sess_list[0] == -1 :
		device.log(level='INFO',message='No sessions found')
		h0.su()
		h0.shell(command='exit')
		raise Exception('')
	
	elif sess_list[0] == split_ip_2[0] and sess_list[1] == ref_ip and  sess_list[2] == split_ip_1[0] and sess_list[3] == split_ip_2[0] :
		device.log(level='INFO',message=' *************With persistent NAT with any-remote-host and address-mapping when using custom VR the return session PASS!!!*****************')
	else :
		device.log(level='ERROR',message=' *************With persistent NAT with any-remote-host and address-mapping when using custom VR the return session fails!!!*****************')
		h0.su()
		h0.shell(command='exit')
		raise Exception('')


def check_source_pool_resource(device,resp):

	status = jxmlease.parse(resp)
	device.log(status)

	if status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-port-translation'] == 'no translation' :

		try:
			var = status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['address-available']
		except KeyError:
			pass
		else:
			if int(status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['total-pool-address']) != int(status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['address-available']) :
				raise Exception('Fix port pool release IP resoure failed!!!!')

	else:
		if status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-address-range']['single-port'] != '0' and status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-address-range']['twin-port'] != '0' :
			raise Exception('PAT pool release port resoure failed!!!!')


def chk_flow_session(device=None,src_ip=None,dest_ip=None,src_port=None,dest_port=None,protocol=None,return_type='sess_id'):

	if device is None:
		raise Exception("'device' is mandatory parameter - device handle")
	if device is not None:
		device.cli(command='show security flow session').response()
		result = device.cli(command='show security flow session', format='xml').response()
		status = jxmlease.parse(result)
		device.log(status)


		if int(status['rpc-reply']['flow-session-information']['displayed-session-count']) > 0 :
		
			device.log("For inbound session")

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['direction']) != 'In':
				device.log(level='ERROR', message='Direction is not inbound')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Direction is inbound')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['source-address']) != src_ip:
				device.log(level='ERROR', message='Source address is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Source address is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['source-port']) != src_port:
				device.log(status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['source-port'])
				device.log(src_port)
				device.log(level='ERROR', message='Source port is not right')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Source port is right')

			if dest_ip is not None:
				if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['destination-address'])!= dest_ip:	
					device.log(level='ERROR', message='Dst address is not right')
					raise Exception("value not present")
				else:
					device.log(level='INFO', message='Dst address is right')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['destination-port']) != dest_port:
				device.log(level='ERROR', message='Dst nat port info is not correct')
				raise Exception("value not present")
			else:
				device.log(level='INFO', message='Dst nat port info is correct')

			if (status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['protocol']) != protocol:
				device.log(level='ERROR', message='Protocol info is not correct')
				raise Exception("value not present")

			else:
				device.log(level='INFO', message='Protocol info is correct')


			if return_type == 'sess_id' : 
				return (status['rpc-reply']['flow-session-information']['flow-session']['session-identifier'])

			if return_type == 'config_time' :
				return (status['rpc-reply']['flow-session-information']['flow-session']['configured-timeout'])
	
		else:

			raise Exception("No session found.....")




def check_persistent_nat_table(device,resp):

	status = jxmlease.parse(resp)

	if int(status['rpc-reply']['persist-nat-table']['persist-nat-table-statistic']['persist-nat-enode-in-use']) == 0 :
		device.log(level='INFO',message='All binging entries can ageout successfully!') 
	else :
		raise Exception('ome binding entries cant ageout successfully!')


def send_multiple_packets(h0,src_ip,dst_ip):

	h0.su()

	for i in range(1025,1035):
		dest_port = random.randint(1,1023)
		h0.shell(command="sendip -d r64 -p ipv4 -is " + src_ip + " -id " + dst_ip + " -p udp -us " + str(i) +  " -ud " + str(dest_port) + " " + dst_ip)
		h0.shell(command="sendip -d r64 -p ipv4 -is " + src_ip + " -id " + dst_ip + " -p udp -us " + str(i) + " -ud " + str(dest_port) + " " + dst_ip)

def send_multiple_hairpinning_packets(h0,src_ip,dst_ip,dest_port):

	h0.su()

	for i in range(1030,1041):
		h0.shell(command="sendip -d r64 -p ipv4 -is " + src_ip + " -id " + dst_ip + " -p udp -us " + str(i) + " -ud " + str(dest_port) + " " + dst_ip)
		h0.shell(command="sendip -d r64 -p ipv4 -is " + src_ip + " -id " + dst_ip + " -p udp -us " + str(i) + " -ud " + str(dest_port) + " " + dst_ip)


def parse_static_rule(resp):

	status = jxmlease.parse(resp)

	static_rule_name = status['rpc-reply']['static-nat-rule-information']['static-nat-rule-entry']['rule-name']
	static_ruleset_name = status['rpc-reply']['static-nat-rule-information']['static-nat-rule-entry']['rule-set-name']
	static_rule_from_context = status['rpc-reply']['static-nat-rule-information']['static-nat-rule-entry']['rule-from-context']
	static_rule_from_context_name = status['rpc-reply']['static-nat-rule-information']['static-nat-rule-entry']['rule-from-context-name']
	static_rule_host_addr = status['rpc-reply']['static-nat-rule-information']['static-nat-rule-entry']['rule-host-address-prefix']
	static_rule_dst_addr = status['rpc-reply']['static-nat-rule-information']['static-nat-rule-entry']['rule-destination-address-prefix']

	list1 = [static_rule_name,static_ruleset_name,static_rule_from_context,static_rule_from_context_name,static_rule_host_addr,static_rule_dst_addr]

	return list1

def parse_policy(resp):

	status = jxmlease.parse(resp)

	policy_src_zone_name = status['rpc-reply']['security-policies']['security-context']['context-information']['source-zone-name']
	policy_dst_zone_name = status['rpc-reply']['security-policies']['security-context']['context-information']['destination-zone-name']
	policy_name = status['rpc-reply']['security-policies']['security-context']['policies']['policy-information']['policy-name']
	policy_src_addr_name = status['rpc-reply']['security-policies']['security-context']['policies']['policy-information']['source-addresses']['source-address']['address-name']
	policy_dst_addr_name = status['rpc-reply']['security-policies']['security-context']['policies']['policy-information']['destination-addresses']['destination-address']['address-name']
	policy_action = status['rpc-reply']['security-policies']['security-context']['policies']['policy-information']['policy-action']['action-type']

	return [policy_src_zone_name,policy_dst_zone_name,policy_name,policy_src_addr_name,policy_dst_addr_name,policy_action]


def parse_nat_source_pool(device,res):

	status = jxmlease.parse(res)
	device.log(status)

	
	src_xlate_low =  status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-address-range']['address-range-low']
	src_xlate_high =  status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-address-range']['address-range-high']
	src_xlate_port_type = status['rpc-reply']['source-nat-pool-detail-information']['source-nat-pool-info-entry']['source-pool-port-translation']

	list1= [src_xlate_low,src_xlate_high,src_xlate_port_type]

	return list1

def check_port_equal(device,res):

	status = jxmlease.parse(res)
	device.log(status)

	if int(status['rpc-reply']['flow-session-information']['displayed-session-count']) > 1 :
		if status['rpc-reply']['flow-session-information']['flow-session'][0]['flow-information'][0]['destination-port'] == status['rpc-reply']['flow-session-information']['flow-session'][0]['flow-information'][1]['source-port'] :
			device.log(level='INFO',message='Port translation Check passed')
		else:
			raise Exception('Port translation Check Failed')
	else:
		if status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['destination-port'] == status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['source-port'] :
			device.log(level='INFO',message='Port translation Check passed')
		else:
			raise Exception('Port translation Check Failed')

def check_interface_nat_ports(device,resp):

	list1 = resp.split("\n")
	comp_val = list1[2]
	comp_val = re.sub("\s\s+" , " ", comp_val)
	comp_val = comp_val.split(" ")
	device.log(comp_val)

	if int(comp_val[3]) != 0 :
		raise Exception("Interface release port resoure failed!!!!")



def verify_check_sum(device,resp1):

	pattern= r'cksum\s0x.{4}\s\(correct\)'
	match = re.search
	(pattern,resp1)
	if match:
		device.log(" Check sum is correct after NAT-PT!")
	else:
		raise Exception(" Check sum is not correct after NAT-PT!")

def get_pid(device,text):

	str_list = text.split(' ')
	device.log(str_list[1])
	return str_list[1]
	


	

