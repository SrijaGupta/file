#
# TODO: This is a placeholder for UTs
#




import jxmlease
import time
import re
import json


def clean_config(device):

	'''
	Clear the DUT.

	'''

	device.config(command_list=['delete security nat',
								'delete applications'])

	device.commit(timeout=180)


def nat_application_test(device,rule_set,from_zone,to_zone,rule,src_address,app_name,app_test):

	'''
		Configures nat application with protocol in source or destination nat rule

		All arguments are string

		Arguments:

		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 app_name : application name
		 src_address : ipv6 or ipv4 address
		 app_test : application to test


	'''

	device.log(level='INFO',message='*****Test point: Config application with TCP/UDP protocol in source/destination nat rule!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='show security nat source rule ' + rule ).response()
	result = device.cli(command='show security nat source rule ' + rule, format='xml').response()
	status = jxmlease.parse(result)
	device.log(status)

	application = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['src-nat-app-entry']['src-nat-application']
	rule_name = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['rule-name']

	device.log(level='INFO',message=' Application : ' + application)
	device.log(level='INFO',message='Rule name : ' + rule_name)

	if application == 'configured' and rule_name == rule :
		device.log(level='INFO',message='*****PASS:the nat source rule name ' + rule + ' application is configured,it is right ! ******')
	else:
		device.log(level='ERROR',message='*****FAIL:the nat source rule name ' + rule + ' application is NOT configured,Please check ! ******')
		raise Exception('')

	result = device.cli(command='show security nat control-plane source rule all', format='text').response()
	
	if result.find(rule) != -1 and result.find('configured') != -1 :
		device.log(level='INFO',message='PASS:the nat control-plane source rule name $rule application is configured,it is right !')
	else :
		device.log(level='ERROR',message='FAIL:the nat control-plane source rule name $rule application is not configured,Please check !')
		raise Exception('')
	

	device.cli(command='show security nat source rule-application ' + rule ).response()
	result = device.cli(command='show security nat source rule-application ' + rule, format='xml').response()
	status = jxmlease.parse(result)
	device.log(status)

	app = status['rpc-reply']['source-nat-rule-application-information']['source-nat-rule-app-entry']['applications']['application']['application-term']['protocol']

	if app == app_test :
		device.log(level='INFO',message='*****PASS:the nat application is ' + app_test + ' ,it is right ! ******') 
	else :
		device.log(level='ERROR',message='******fAIL:the nat application is not' + app_test + ' ,Please check! ******') 
		raise Exception ('')



def delete_nat_rule(device,rule_set,from_zone,to_zone,rule,src_address,app_name,app_test):

	'''

	All arguments are string

	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 app_name : application name
		 src_address : ipv6 or ipv4 address
		 app_test : application to test
		 

	'''

	device.log(level='INFO',message='*****Test point: Delete source/destination nat rule with application configured!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	device.commit(timeout=180)

	time.sleep(5)

	device.config(command_list=['delete security nat source rule-set $rule_set rule ' + rule])
	
	result = device.commit(timeout=180).response()

	if result.count('error') == 1 :
		device.log(level='ERROR',message='****************FAIL:Delete source nat rule with application configured failed!********************')
	else :
		device.log(level='INFO',message='****************PASS:Delete source nat rule with application configured successfully!********************')


def change_application(device,rule_set,from_zone,to_zone,rule,src_address,app_name,app_test,app_test_new):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 app_name : application name
		 src_address : ipv6 or ipv4 address
		 app_test : application to test
		 

	'''

	device.log(level='INFO',message='*****Test point: Application content changes can invoke source/destination nat rule change!*****')

	nat_application_test(device,rule_set,from_zone,to_zone,rule,src_address,app_name,app_test)

	device.log(level='INFO',message='*****change the application content from ' + app_test + ' to ' + app_test_new + '   ! ******')

	device.config(command_list=["delete applications",
                     "set applications application " + app_name + " protocol " + app_test_new])
	device.commit(timeout=180)

	device.cli(command='show security nat source rule ' + rule ).response()
	result = device.cli(command='show security nat source rule ' + rule, format='xml').response()
	status = jxmlease.parse(result)
	device.log(status)

	application = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['src-nat-app-entry']['src-nat-application']
	rule_name = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['rule-name']

	device.log(level='INFO',message=' Application : ' + application)
	device.log(level='INFO',message='Rule name : ' + rule_name)

	if application == 'configured' and rule_name == rule :
		device.log(level='INFO',message='*****PASS:the nat source rule name ' + rule + ' application is configured,it is right ! ******')
	else:
		device.log(level='ERROR',message='*****FAIL:the nat source rule name ' + rule + ' application is NOT configured,Please check ! ******')
		raise Exception('')

	result = device.cli(command='show security nat control-plane source rule all', format='text').response()
	
	if result.find(rule) != -1 and result.find('configured') != -1 :
		device.log(level='INFO',message='PASS:the nat control-plane source rule name $rule application is configured,it is right !')
	else :
		device.log(level='ERROR',message='FAIL:the nat control-plane source rule name $rule application is not configured,Please check !')
		raise Exception('')
	

	device.cli(command='show security nat source rule-application ' + rule ).response()
	result = device.cli(command='show security nat source rule-application ' + rule, format='xml').response()
	status = jxmlease.parse(result)
	device.log(status)

	app = status['rpc-reply']['source-nat-rule-application-information']['source-nat-rule-app-entry']['applications']['application']['application-term']['protocol']

	if app == app_test_new :
		device.log(level='INFO',message='*****PASS:the nat application is ' + app_test + ' ,it is right ! ******') 
	else :
		device.log(level='ERROR',message='******fAIL:the nat application is not' + app_test + ' ,Please check! ******') 
		raise Exception ('')

def add_destination_port(device,rule_set,from_zone,to_zone,rule,src_address,dst_port,dst_port_low,dst_port_high):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dst_port : destination port
		 src_address : ipv6 or ipv4 address
		 dst_port_low : port_low
		 dst_port_high : port_high
		 
		 

	'''

	device.log(level='INFO',message="*****Test point: Add single & range destination-port configuration in source/destination nat rule!*****\n")

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port_low + " to " +  dst_port_high,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	result = device.commit(timeout=180).response()

	if result.count('error') == 1 :
		device.log(level='ERROR',message='Commit Failed')
		raise Exception('')
	else:
		device.log(level='INFO',message='Commit Successful')

	time.sleep(5)

	device.cli(command='show security nat source rule ' + rule ).response()
	result = device.cli(command='show security nat source rule ' + rule, format='xml').response()
	status = jxmlease.parse(result)
	device.log(status)

	dest_port_low_1 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low'][0]
	dest_port_low_2 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low'][1]
	dest_port_high_1 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high'][0]
	dest_port_high_2 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high'][1]

	if dest_port_low_1 == dst_port and dest_port_high_1 == dst_port and dest_port_low_2 == dst_port_low and dest_port_high_2 == dst_port_high :
		device.log(level='INFO',message='*****PASS:the destination-port is right! ******')
	else:
		device.log(level='ERROR',message='*****FAIL:the destination-port is not right! ******')
		raise Exception('')

def change_dest_port(device,rule_set,from_zone,to_zone,rule,src_address,dst_port,dst_port_new):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dst_port : destination port
		 src_address : ipv6 or ipv4 address
		 dst_port_low : port_low
		 dst_port_high : port_high
		 	 

	'''

	device.log(level='INFO',message="**********Test point: Change destination-port configuration in source/destination nat rule!*****\n")

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	result = device.commit(timeout=180).response()

	if result.count('error') == 1 :
		device.log(level='ERROR',message='Commit Failed')
		raise Exception('')
	else:
		device.log(level='INFO',message='Commit Successful')

	time.sleep(5)

	device.cli(command='show security nat source rule ' + rule ).response()
	result = device.cli(command='show security nat source rule ' + rule, format='xml').response()
	status = jxmlease.parse(result)
	device.log(status)

	dest_low = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low']
	dest_high = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high']

	device.log(dest_low)
	device.log(dest_high)

	if dest_low == dst_port and dest_high == dst_port :
		device.log(level='INFO',message='*****PASS:the destination-port is right! ******')
	else:
		device.log(level='ERROR',message='*****FAIL:the destination-port is not right! ******')
		raise Exception('')


	device.log(level='INFO',message='*****change the destination-port from ' + dst_port + ' to ' + dst_port_new + ' ! ******')

	device.config(command_list=["delete security nat source rule-set " + rule_set  + " rule " + rule + " match destination-port " + dst_port,
                     "set security nat source rule-set " +  rule_set + " rule " + rule + " match destination-port " + dst_port_new])
	device.commit(timeout=180)

	if result.count('error') == 1 :
		device.log(level='ERROR',message='Commit Failed')
		raise Exception('')
	else:
		device.log(level='INFO',message='Commit Successful')

	device.cli(command='show security nat source rule ' + rule ).response()
	result = device.cli(command='show security nat source rule ' + rule, format='xml').response()
	status = jxmlease.parse(result)
	device.log(status)

	dest_low = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low']
	dest_high = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high']

	if dest_low == dst_port_new and dest_high == dst_port_new :
		device.log(level='INFO',message='*****PASS:the destination-port is right! ******')
	else:
		device.log(level='ERROR',message='*****FAIL:the destination-port is not right! ******')
		raise Exception('')

def delete_nat_rule_with_port(device,rule_set,from_zone,to_zone,rule,src_address,dst_port):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dst_port : destination port
		 src_address : ipv6 or ipv4 address
		 dst_port_low : port_low
		 dst_port_high : port_high
		 		 

	'''

	device.log(level='INFO',message="*****Test point: Delete source/destination nat rule with destination-port configured!*****\n")

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	result = device.commit(timeout=180).response()

	if result.count('error') == 1 :
		device.log(level='ERROR',message='Commit Failed')
		raise Exception('')
	else:
		device.log(level='INFO',message='Commit Successful')

	time.sleep(5)

	device.config(command_list=["delete security nat source rule-set " + rule_set + " rule " + rule])
	result = device.commit(timeout=180).response()

	if result.count('error') == 1 :
		device.log(level='ERROR',message='******FAIL:Delete source nat rule with destination-port configured fail!****')
		raise Exception('')
	else:
		device.log(level='INFO',message='****************PASS:Delete source nat rule with destination-port configured successfully!********************')

def config_max_dest_port(device,rule_set,from_zone,to_zone,rule,src_address,dst_port_1,dst_port_2,dst_port_3,dst_port_4,dst_port_5,dst_port_6,dst_port_7,dst_port_8):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dst_port : destination port
		 src_address : ipv6 or ipv4 address
		 dst_port_low : port_low
		 dst_port_high : port_high
		
	'''

	device.log(level='INFO',message="*****Test point: Config 8 maximum entry number of dst-port in source/destination nat rule!*****\n")

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port_1,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port_2,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port_3,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port_4,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port_5,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port_6,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port_7,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port_8,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	result = device.commit(timeout=180).response()

	if result.count('error') == 1 :
		device.log(level='ERROR',message='Commit Failed')
		raise Exception('')
	else:
		device.log(level='INFO',message='Commit Successful')

	time.sleep(5)

	device.cli(command='show security nat source rule all').response()
	result = device.cli(command='show security nat source rule all', format='xml').response()
	status = jxmlease.parse(result)
	device.log(status)

	dest_low_1 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low'][0]
	dest_high_1 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high'][0]

	dest_low_2 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low'][1]
	dest_high_2 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high'][1]

	dest_low_3 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low'][2]
	dest_high_3= status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high'][2]

	dest_low_4 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low'][3]
	dest_high_4 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high'][3]

	dest_low_5 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low'][4]
	dest_high_5 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high'][4]

	dest_low_6 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low'][5]
	dest_high_6 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high'][5]

	dest_low_7 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low'][6]
	dest_high_7 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high'][6]

	dest_low_8 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-low'][7]
	dest_high_8 = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['destination-port-entry']['rule-destination-port-high'][7]


	if dest_low_1 == dst_port_1 and dest_high_1 == dst_port_1 and dest_low_2 == dst_port_2 and dest_high_2 == dst_port_2 and dest_low_3 == dst_port_3 and dest_high_3 == dst_port_3 and dest_low_4 == dst_port_4 and dest_high_4 == dst_port_4 and dest_low_5 == dst_port_5 and dest_high_5 == dst_port_5 and dest_low_6 == dst_port_6 and dest_high_6 == dst_port_6 and dest_low_7 == dst_port_7 and dest_high_7 == dst_port_7 and dest_low_8 == dst_port_8 and dest_high_8 == dst_port_8 :
		device.log(level='INFO',message='*****PASS:the destination-port is right! ******')
	else:
		device.log(level='ERROR',message='*****FAIL:the destination-port is not right! ******')
		raise Exception('')

def check_dest_port_low(device,rule_set,from_zone,to_zone,rule,src_address,app_test,dst_port_low,dst_port_high):

	device.log(level='INFO',message='*****Test point: Dst-port low cannot larger than high in NAT rule!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " +  rule + " match protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	device.commit(timeout=180)

	time.sleep(5)

	device.log(level='INFO',message="*****Config the dst-port with lower limit bigger than upper limit!*****")

	device.config(command_list=["set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port_low + " to " +  dst_port_high])

	try :
		device.commit(timeout=180)
	except:
		device.log(level='INFO',message='****PASS:dst-port upper limit should be bigger than lower limit!*****')
	else:
		device.log(level='ERROR',message='****FAIL:commit is successfully, it should be fail,please check!**********')
		raise Exception('')

def dest_port_with_application(device,rule_set,from_zone,to_zone,rule,src_address,app_name,app_test,dst_port):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dst_port : destination port
		 src_address : ipv6 or ipv4 address
		 dst_port_low : port_low
		 dst_port_high : port_high
		 app_name : application name
		 app_test : application to test		 

	'''

	device.log(level='INFO',message='*****Test point: Dst-port cannot be configured together with application in NAT rule!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	device.commit(timeout=180)

	time.sleep(5)

	device.log(level='INFO',message='"*****Config the dst-port together with application in NAT rule!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dst_port,
								"set applications application " + app_name + " protocol " + app_test,
                     			"set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name
								])


	try :
		device.commit(timeout=180)
	except:
		device.log(level='INFO',message='****PASS:Dst-port cannot config together with application in NAT rule!*****')
	else:
		device.log(level='ERROR',message='****FAIL:Commit is successfully, it should be fail,please check!*****')
		raise Exception('')

def src_port_with_application(device,rule_set,from_zone,to_zone,rule,src_address,app_name,app_test,src_port):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_port : source port
		 src_address : ipv6 or ipv4 address
		 app_name : application name
		 app_test :application test
		 
	'''

	device.log(level='INFO',message='*****Test point: Src-port cannot be configured together with application in NAT rule!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	device.commit(timeout=180)

	time.sleep(5)

	device.log(level='INFO',message='"*****Config the src-port together with application in NAT rule!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " rule " + rule + " match source-port " + src_port,
								"set applications application " + app_name + " protocol " + app_test,
                     			"set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name
								])


	try :
		device.commit(timeout=180)
	except:
		device.log(level='INFO',message='****PASS:src-port cannot config together with application in NAT rule!*****')
	else:
		device.log(level='ERROR',message='****FAIL:commit is successfully, it should be fail,please check!*****')
		raise Exception('')

def protocol_with_application(device,rule_set,from_zone,to_zone,rule,src_address,app_name,app_test):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 app_name : application name
		 app_test :application test
		 

	'''

	device.log(level='INFO',message='*****Test point: Protocol cannot be configured together with application in NAT rule!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	device.commit(timeout=180)

	time.sleep(5)

	device.log(level='INFO',message='*****Config the Protocol together with application in NAT rule!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " rule " + rule + " match protocol " + app_test,
								"set applications application " + app_name + " protocol " + app_test,
                     			"set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name
								])


	try :
		device.commit(timeout=180)
	except:
		device.log(level='INFO',message='****PASS:Protocol cannot config together with application in NAT rule!*****')
	else:
		device.log(level='ERROR',message='****FAIL:commit is successfully, it should be fail,please check!*****')
		raise Exception('')

def check_application(device,rule_set,from_zone,to_zone,rule,src_address,app_name,app_test):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 app_name : application name
		 app_test :application test
		 

	'''

	device.log(level='INFO',message='*****Test point: Only application with IP port and ICMP type is supported in NAT rule!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	device.commit(timeout=180)

	time.sleep(5)

	device.log(level='INFO',message='*****Config application*****')

	device.config(command_list=["set applications application " + app_name + " rpc-program-number 123",
                     			"set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name
								])

	try :
		res1 = device.commit(timeout=180).response()
	except:
		pass
	else:
		device.log(level='ERROR',message='****FAIL:commit is successfully, it should be fail,please check!*****')
		raise Exception('')

	device.config(command_list=["delete applications",
								"set applications application " + app_name + " protocol " + app_test,
                     			"set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name
								])

	try:
		res2 = device.commit(timeout=180).response()
	except:
		device.log(level='ERROR',message='****FAIL:commit is successfully, it should be fail,please check!*****')
		raise Exception('')
	else:
		device.log(level='INFO',message='****PASS:Only application with IP port and ICMP type is supported in NAT rule!*****')


def verify_nat_rule(device,rule,app_test):

	'''

	Verifies the nat rule.

	Arguments 
	
	device :DUT
	rule : rule name
	app_test : application to test

	'''

	device.cli(command='show security nat source rule ' + rule ).response()
	result = device.cli(command='show security nat source rule ' + rule, format='xml').response()
	status = jxmlease.parse(result)
	device.log(status)

	application = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['src-nat-app-entry']['src-nat-application']
	rule_name = status['rpc-reply']['source-nat-rule-detail-information']['source-nat-rule-entry']['rule-name']

	device.log(level='INFO',message=' Application : ' + application)
	device.log(level='INFO',message='Rule name : ' + rule_name)

	if application == 'configured' and rule_name == rule :
		device.log(level='INFO',message='*****PASS:the nat source rule name ' + rule + ' application is configured,it is right ! ******')
	else:
		device.log(level='ERROR',message='*****FAIL:the nat source rule name ' + rule + ' application is NOT configured,Please check ! ******')
		raise Exception('')

	result = device.cli(command='show security nat control-plane source rule all', format='text').response()
	
	if result.find(rule) != -1 and result.find('configured') != -1 :
		device.log(level='INFO',message='PASS:the nat control-plane source rule name $rule application is configured,it is right !')
	else :
		device.log(level='ERROR',message='FAIL:the nat control-plane source rule name $rule application is not configured,Please check !')
		raise Exception('')
	

	device.cli(command='show security nat source rule-application ' + rule ).response()
	result = device.cli(command='show security nat source rule-application ' + rule, format='xml').response()
	status = jxmlease.parse(result)
	device.log(status)

	app = status['rpc-reply']['source-nat-rule-application-information']['source-nat-rule-app-entry']['applications']['application']['application-term']['protocol']

	if app == app_test :
		device.log(level='INFO',message='*****PASS:the nat application is ' + app_test + ' ,it is right ! ******') 
	else :
		device.log(level='ERROR',message='******fAIL:the nat application is not' + app_test + ' ,Please check! ******') 
		raise Exception ('')


	
def configure_multi_nat_rule_with_application(device,rule_set,from_zone,to_zone,rule1,rule2,src_address_1,src_address_2,app_name_1,app_name_2,app_test_1,app_test_2,dest_port_1,dest_port_2):
	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 app_name : application name
		 app_test :application test
		 dest_port : destination port

	'''

	device.log(level='INFO',message='*****Test point: Configure multi source/destination nat rule entries with application!*****')

	device.config(command_list=["set applications application " + app_name_1 + " protocol " + app_test_1,
							"set applications application " + app_name_1 + " destination-port " + dest_port_1,
							"set applications application " + app_name_2 + " protocol " + app_test_2,
							"set applications application " + app_name_2 + " destination-port " + dest_port_2
							])

	device.commit(timeout=180)

	time.sleep(5)

	device.log(level='INFO',message='*****Configure multi source/destination nat rule entries with application!*****')


	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule "  + rule1 + " match source-address " + src_address_1,
                     "set security nat source rule-set " + rule_set + " rule " + rule1 + " then source-nat interface",
                     "set security nat source rule-set " + rule_set + " rule "  + rule2 + " match source-address " + src_address_2,
                     "set security nat source rule-set " + rule_set + " rule " + rule2 + " then source-nat interface",
                     "set security nat source rule-set " + rule_set + " rule " +  rule1 + " match application " + app_name_1,
                     "set security nat source rule-set " + rule_set + " rule " +  rule2 + " match application " + app_name_2])

	device.commit(timeout=180)

	time.sleep(5)


	verify_nat_rule(device,rule1,app_test_1)

	time.sleep(5)

	verify_nat_rule(device,rule2,app_test_2)


def verify_flow_session(device,src_ip=None,dest_ip=None,nat_ip=None,src_port=None,dest_port=None,dest_nat=None):

	'''
	
	 Verifies the flow session

	 Arguments:

	 device : DUT
	 src_ip : source ip address
	 dest_ip : destination ip address
	 nat_ip : nat ip 
	 src_port : source port
	 dest_port : destination port
	 dest_nat : destination nat address 

	'''

	if device is None:
		raise Exception("'device' is mandatory parameter - device handle")
	if device is not None:
		#device.cli(command='show security flow session').response()
		result = device.cli(command='show security flow session', format='xml').response()
		status = jxmlease.parse(result)
		device.log(status)


		if int(status['rpc-reply']['flow-session-information']['displayed-session-count']) > 0 :
		
			in_srcip = status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['source-address']
			in_destip = status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['destination-address']
			in_destport = status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['destination-port']
			in_protocol = status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][0]['protocol']

			out_srcip = status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['source-address']
			out_destip = status['rpc-reply']['flow-session-information']['flow-session']['flow-information'][1]['destination-address']

			if dest_nat is not None :

				if dest_port is not None :

					if	in_destip == dest_ip and out_srcip == nat_ip and in_destport == dest_port :

						device.log (level='INFO',message="\n------The destination port is " + in_destport + " --------\n")
						device.log(level='INFO',message='The address is translated from  ' + in_destip + ' to ' + out_srcip)
						return 1

					else :

						device.log (level='INFO',message="\n------The source      address is " + in_destip + " ---------\n")
						device.log (level='INFO',message="\n------The destination address is " + out_srcip + "---------\n")
						device.log (level='INFO',message="\n------The address is no-translation ---------\n\n")
						return 0


				elif in_destip == dest_ip and out_srcip == nat_ip :

					device.log(level='INFO',message='The address is translated from  ' + in_destip + ' to ' + out_srcip)
					return 1

				else :

					device.log (level='INFO',message="\n------The source      address is " + in_destip + " ---------\n")
					device.log (level='INFO',message="\n------The destination address is " + out_srcip + "---------\n")
					device.log (level='INFO',message="\n------The address is no-translation ---------\n\n")
					return 0

			elif dest_port is not None :

				if	in_srcip == src_ip and out_destip == nat_ip and in_destport == dest_port :

					device.log (level='INFO',message="\n------The destination port is " + in_destport + " --------\n")
					device.log(level='INFO',message='The address is translated from  ' + in_srcip + ' to ' + out_destip)
					return 1

				else :

					device.log (level='INFO',message="\n------The source      address is " + in_srcip + " ---------\n")
					device.log (level='INFO',message="\n------The destination address is " + out_destip + "---------\n")
					device.log (level='INFO',message="\n------The address is no-translation ---------\n\n")
					return 0


			elif in_srcip == src_ip and out_destip == nat_ip :

				device.log(level='INFO',message='The address is translated from  ' + in_srcip + ' to ' + out_destip)
				return 1

			else :

				device.log (level='INFO',message="\n------The source      address is " + in_srcip + " ---------\n")
				device.log (level='INFO',message="\n------The destination address is " + out_destip + "---------\n")
				device.log (level='INFO',message="\n------The address is no-translation ---------\n\n")
				return 0


			device.cli(command='clear security flow session')
			time.sleep(5)


		else :
			device.log(level='INFO',message='NO session Found')
			raise Exception('')

def nat_rule_without_port(device,h0,rule_set,rule,from_zone,to_zone,src_address,src_static_route,sendip_src,sendip_dest):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address

	'''

	split_ip = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_1 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	interface =  t['resources']['box']['interfaces']['r0h0']['pic']

	device.log(level='INFO',message='*****Test point: Stream match source nat rule without port or app!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + "  from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set routing-options static route " + src_static_route + " next-hop " + split_ip[0],
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface"])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src + ' -id ' + sendip_dest + ' -p icmp '+ split_ip_2[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=sendip_dest,nat_ip=split_ip_1[0])

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')

def nat_rule_with_dest_port(device,h0,rule_set,rule,from_zone,to_zone,src_address,src_static_route,sendip_src,sendip_dest,dest_port):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 dest_port : destination port
		 src_static_route : ip address

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface =  t['resources']['box']['interfaces']['r0h0']['pic']

	device.log(level='INFO',message='*****Test point: Stream match source nat rule without port or app!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + "  from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set routing-options static route " + src_static_route + " next-hop " + split_ip_2[0],
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface",
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dest_port])

	device.commit(timeout=180)

	time.sleep(5)


	device.cli(command='clear security flow session interface ' + interface)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_2[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src + ' -id ' + sendip_dest + ' -p tcp -td '+  dest_port + ' ' + split_ip_3[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=sendip_dest,nat_ip=split_ip_4[0],dest_port=dest_port)

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')

def persistent_nat_rule_with_dest_port(device,h0,rule_set,rule,from_zone,to_zone,src_address,src_static_route,sendip_src,sendip_dest,dest_port):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 src_static_route : ip address
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface =  t['resources']['box']['interfaces']['r0h0']['pic']

	device.log(level='INFO',message='*****Test point: Stream match source nat rule with dst-port configured with persistent-nat!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + "  from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set routing-options static route " + src_static_route + " next-hop " + split_ip_2[0],
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dest_port,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface persistent-nat permit any-remote-host",
                     "set security nat source interface port-overloading off"])

	device.commit(timeout=180)

	time.sleep(5)


	device.cli(command='clear security flow session interface ' + interface)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_2[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src + ' -id ' + sendip_dest + ' -p tcp -td '+  dest_port + ' ' + split_ip_3[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=sendip_dest,nat_ip=split_ip_4[0],dest_port=dest_port)

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')

def persistent_nat_rule_with_dest_port_addr_mapping(device,h0,rule_set,rule,from_zone,to_zone,src_address,src_static_route,sendip_src,sendip_dest,dest_port,pool_address,pool_name,pool_address_rel):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 src_static_route : ip address
		 pool_address : nat pool address
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface =  t['resources']['box']['interfaces']['r0h0']['pic']

	device.log(level='INFO',message='*****Test point: Stream match source nat rule with dst-port configured with persistent-nat address-mapping!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + "  from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set routing-options static route " + src_static_route + " next-hop " + split_ip_2[0],
                     "set security nat source pool " + pool_name + " address " + pool_address,
                     "set security nat source pool " + pool_name + " port no-translation",
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dest_port,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat pool " + pool_name,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat pool persistent-nat permit any-remote-host",
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat pool persistent-nat address-mapping",
                     "set security nat source interface port-overloading off"])

	device.commit(timeout=180)

	time.sleep(5)


	device.cli(command='clear security flow session interface ' + interface)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_2[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src + ' -id ' + sendip_dest + ' -p tcp -td '+  dest_port + ' ' + split_ip_3[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=sendip_dest,nat_ip=pool_address_rel,dest_port=dest_port)

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')

def nat_rule_with_dest_port_neg(device,h0,rule_set,rule,from_zone,to_zone,src_address,src_static_route,sendip_src,sendip_dest,dest_port,dest_port_1):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 src_static_route : ip address
		 dest_port : destination port 
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface =  t['resources']['box']['interfaces']['r0h0']['pic']

	device.log(level='INFO',message='*****Test point: Stream doesnt match source nat rule with dst-port configured!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + "  from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set routing-options static route " + src_static_route + " next-hop " + split_ip_2[0],
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface",
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dest_port])

	device.commit(timeout=180)

	time.sleep(5)


	device.cli(command='clear security flow session interface ' + interface)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_2[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src + ' -id ' + sendip_dest + ' -p tcp -td '+  dest_port_1 + ' ' + split_ip_3[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=sendip_dest,nat_ip=split_ip_4[0],dest_port=dest_port)


	if result == 1:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')
	else:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')

def nat_rule_with_app(device,h0,rule_set,from_zone,to_zone,rule,src_address,src_static_route,sendip_src,sendip_dest,app_name,app_test):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 src_static_route : ip address
		 app_name : application name
		 app_test :application test
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface =  t['resources']['box']['interfaces']['r0h0']['pic']

	device.log(level='INFO',message='*****Test point: Stream match source nat rule with app configured!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + "  from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set routing-options static route " + src_static_route + " next-hop " + split_ip_2[0],
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface",
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_2[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src + ' -id ' + sendip_dest + ' -p  ' + app_test + ' ' + split_ip_3[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=sendip_dest,nat_ip=split_ip_4[0])

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')


def persistent_nat_rule_with_app(device,h0,rule_set,from_zone,to_zone,rule,src_address,src_static_route,sendip_src,sendip_dest,app_name,app_test):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 src_static_route : ip address
		 app_name : application name
		 app_test :application test
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface =  t['resources']['box']['interfaces']['r0h0']['pic']

	device.log(level='INFO',message='*****Test point: Stream match source nat rule with app configured!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + "  from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set routing-options static route " + src_static_route + " next-hop " + split_ip_2[0],
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface",
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface persistent-nat permit any-remote-host",
                     "set security nat source interface port-overloading off"])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_2[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src + ' -id ' + sendip_dest + ' -p  ' + app_test + ' ' + split_ip_3[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=sendip_dest,nat_ip=split_ip_4[0])

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')


def persistent_nat_rule_with_addr_mapping(device,h0,rule_set,rule,from_zone,to_zone,src_address,src_static_route,sendip_src,sendip_dest,pool_address,pool_name,pool_address_rel,app_name,app_test):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 src_static_route : ip address
		 dest_port : destination port
		 app_name : application name
		 app_test :application test
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface =  t['resources']['box']['interfaces']['r0h0']['pic']

	device.log(level='INFO',message='*****Test point: Stream match source nat rule with app configured with persistent-nat address-mapping!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + "  from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set routing-options static route " + src_static_route + " next-hop " + split_ip_2[0],
                     "set security nat source pool " + pool_name + " address " + pool_address,
                     "set security nat source pool " + pool_name + " port no-translation",
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match source-address " + src_address,
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat pool " + pool_name,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat pool persistent-nat permit any-remote-host",
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat pool persistent-nat address-mapping",
                     "set security nat source interface port-overloading off"])

	device.commit(timeout=180)

	time.sleep(5)


	device.cli(command='clear security flow session interface ' + interface)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_2[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src + ' -id ' + sendip_dest + ' -p  ' + app_test + ' ' + split_ip_3[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=sendip_dest,nat_ip=pool_address_rel)

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')

def nat_rule_with_app_neg(device,h0,rule_set,from_zone,to_zone,rule,src_address,src_static_route,sendip_src,sendip_dest,app_name,app_test,app_test_new):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 src_static_route : ip address
		 dest_port : destination port
		 app_name : application name
		 app_test :application test
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface =  t['resources']['box']['interfaces']['r0h0']['pic']

	device.log(level='INFO',message='*****Test point: Stream  doesnt match source nat rule with app configured!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + "  from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set routing-options static route " + src_static_route + " next-hop " + split_ip_2[0],
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface",
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_2[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src + ' -id ' + sendip_dest + ' -p  ' + app_test_new + ' ' + split_ip_3[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=sendip_dest,nat_ip=split_ip_4[0])

	if result == 1:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')
	else:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')


def different_nat_rule_with_app(device,h0,rule_set,from_zone,to_zone,rule,src_address,src_static_route,sendip_src,sendip_dest,app_name,app_test,src_address_2,rule2,sendip_src_2):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 or ipv4 address
		 src_static_route : ip address
		 dest_port : destination port
		 app_name : application name
		 app_test :application test
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface =  t['resources']['box']['interfaces']['r0h0']['pic']

	device.log(level='INFO',message='*****Test point: Stream  doesnt match source nat rule with app configured!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + "  from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set routing-options static route " + src_static_route + " next-hop " + split_ip_2[0],
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface",
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " +  rule + " match application " + app_name,

                     "set security nat source rule-set " + rule_set + " rule " + rule2 + " match source-address " + src_address_2,
                     "set security nat source rule-set " + rule_set + " rule " + rule2 + " then source-nat interface",
                     "set security nat source rule-set " + rule_set + " rule " +  rule2 + " match application " + app_name
                     ])

	device.commit(timeout=180)


	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_2[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src + ' -id ' + sendip_dest + ' -p  ' + app_test + ' ' + split_ip_3[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=sendip_dest,nat_ip=split_ip_4[0])

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')

	device.cli(command='clear security flow session')

	time.sleep(5)


	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + sendip_src_2 + ' -id ' + sendip_dest + ' -p  ' + app_test + ' ' + split_ip_3[0])

	time.sleep(5)

	result = verify_flow_session(device,src_ip=sendip_src_2,dest_ip=sendip_dest,nat_ip=split_ip_4[0])

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')



def dest_nat_rule_without_port_or_app(device,h0,pool_name,dest_pool_addr,rule_set,rule,dest_addr,dest_static_route,sendip_dest):


	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dest_address : ipv6 or ipv4 address
		 dest_static_route : ip address
		 dest_port : destination port
		 app_name : application name
		 app_test :application test
		 

	'''

	

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface_1 =  t['resources']['box']['interfaces']['r0h0']['pic']
	interface_2 =  t['resources']['box']['interfaces']['r0h1']['pic']


	device.log(level='INFO',message='*****Test point: Stream match destination nat rule without port or app!*****')

	device.config(command_list=["set security nat destination pool " + pool_name + " address " + dest_pool_addr,
                     "set security nat destination rule-set " + rule_set + " from interface " + interface_2,
                     "set security nat destination rule-set " + rule_set + " rule " + rule + " match destination-address " + dest_addr,
                     "set security nat destination rule-set " + rule_set+ "  rule " + rule + " then destination-nat pool " + pool_name,
                     "set security nat proxy-arp interface " + interface_2 + " address " + dest_addr,
                     "set routing-options static route " + dest_static_route + "  next-hop " + split_ip_1[0]
		])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface_2)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_1[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	time.sleep(5)

	

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + split_ip_2[0] + ' -id ' + sendip_dest + ' -p  icmp ' + split_ip_4[0])

	#time.sleep(1)

	result = verify_flow_session(device,src_ip=split_ip_2[0],dest_ip=sendip_dest,nat_ip=split_ip_1[0],dest_nat=1)


	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')

	

def dest_nat_rule_with_dest_port(device,h0,pool_name,dest_pool_addr,rule_set,rule,dest_addr,dest_static_route,sendip_dest,dest_port):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dest_address : ipv6 or ipv4 address
		 dest_static_route : ip address
		 dest_port : destination port
		 app_name : application name
		 app_test :application test
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface_1 =  t['resources']['box']['interfaces']['r0h0']['pic']
	interface_2 =  t['resources']['box']['interfaces']['r0h1']['pic']


	device.log(level='INFO',message='*****Test point: Stream match destination nat rule without port or app!*****')

	device.config(command_list=["set security nat destination pool " + pool_name + " address " + dest_pool_addr,
                     "set security nat destination rule-set " + rule_set + " from interface " + interface_2,
                     "set security nat destination rule-set " + rule_set + " rule " + rule + " match destination-address " + dest_addr,
                     "set security nat destination rule-set " + rule_set+ "  rule " + rule + " then destination-nat pool " + pool_name,
                     "set security nat proxy-arp interface " + interface_2 + " address " + dest_addr,
                     "set security nat destination rule-set " + rule_set + " rule " + rule + " match destination-port " + dest_port,
                     "set routing-options static route " + dest_static_route + "  next-hop " + split_ip_1[0]
		])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface_2)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_1[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	time.sleep(5)

	

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + split_ip_2[0] + ' -id ' + sendip_dest + ' -p tcp -td '+ dest_port + ' ' + split_ip_4[0])
	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + split_ip_2[0] + ' -id ' + sendip_dest + ' -p tcp -td '+ dest_port + ' ' + split_ip_4[0])
	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + split_ip_2[0] + ' -id ' + sendip_dest + ' -p tcp -td '+ dest_port + ' ' + split_ip_4[0])
	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + split_ip_2[0] + ' -id ' + sendip_dest + ' -p tcp -td '+ dest_port + ' ' + split_ip_4[0])

	#time.sleep(1)

	result = verify_flow_session(device,src_ip=split_ip_2[0],dest_ip=sendip_dest,nat_ip=split_ip_1[0],dest_nat=1,dest_port=dest_port)

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')

	

def dest_nat_rule_with_dest_port_neg(device,h0,pool_name,dest_pool_addr,rule_set,rule,dest_addr,dest_static_route,sendip_dest,dest_port,dest_port_2):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dest_address : ipv6 or ipv4 address
		 dest_static_route : ip address
		 dest_port : destination port
		 app_name : application name
		 app_test :application test
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface_1 =  t['resources']['box']['interfaces']['r0h0']['pic']
	interface_2 =  t['resources']['box']['interfaces']['r0h1']['pic']


	device.log(level='INFO',message='*****Test point: Stream doesnt match destination nat rule with dst-port configured!*****')

	device.config(command_list=["set security nat destination pool " + pool_name + " address " + dest_pool_addr,
                     "set security nat destination rule-set " + rule_set + " from interface " + interface_2,
                     "set security nat destination rule-set " + rule_set + " rule " + rule + " match destination-address " + dest_addr,
                     "set security nat destination rule-set " + rule_set+ "  rule " + rule + " then destination-nat pool " + pool_name,
                     "set security nat proxy-arp interface " + interface_2 + " address " + dest_addr,
                     "set security nat destination rule-set " + rule_set + " rule " + rule + " match destination-port " + dest_port,
                     "set routing-options static route " + dest_static_route + "  next-hop " + split_ip_1[0]
		])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface_2)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_1[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	time.sleep(15)

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + split_ip_2[0] + ' -id ' + sendip_dest + ' -p tcp -td '+ dest_port_2 + ' ' + split_ip_4[0])

	#time.sleep(1)

	result = verify_flow_session(device,src_ip=split_ip_2[0],dest_ip=sendip_dest,nat_ip=split_ip_1[0],dest_nat=1,dest_port=dest_port)

	

	if result == 1:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')
	else:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')


def dest_nat_rule_with_app(device,h0,pool_name,dest_pool_addr,rule_set,rule,dest_addr,dest_static_route,sendip_dest,app_test,app_name):


	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dest_address : ipv6 or ipv4 address
		 dest_static_route : ip address
		 dest_port : destination port
		 app_name : application name
		 app_test :application test
		 

	'''

	

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface_1 =  t['resources']['box']['interfaces']['r0h0']['pic']
	interface_2 =  t['resources']['box']['interfaces']['r0h1']['pic']


	device.log(level='INFO',message='*****Test point: Stream match destination nat rule with app configured!*****')

	device.config(command_list=["set security nat destination pool " + pool_name + " address " + dest_pool_addr,
                     "set security nat destination rule-set " + rule_set + " from interface " + interface_2,
                     "set security nat destination rule-set " + rule_set + " rule " + rule + " match destination-address " + dest_addr,
                     "set security nat destination rule-set " + rule_set+ "  rule " + rule + " then destination-nat pool " + pool_name,
                     "set security nat proxy-arp interface " + interface_2 + " address " + dest_addr,
                     "set routing-options static route " + dest_static_route + "  next-hop " + split_ip_1[0],
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat destination rule-set " + rule_set + " rule " + rule + " match application " + app_name
		])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface_2)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_1[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	time.sleep(5)

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + split_ip_2[0] + ' -id ' + sendip_dest + ' -p  '+ app_test + ' ' + split_ip_4[0])

	#time.sleep(1)

	result = verify_flow_session(device,src_ip=split_ip_2[0],dest_ip=sendip_dest,nat_ip=split_ip_1[0],dest_nat=1)


	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')


def dest_nat_rule_with_app_neg(device,h0,pool_name,dest_pool_addr,rule_set,rule,dest_addr,dest_static_route,sendip_dest,app_test,app_name,app_test_new):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dest_address : ipv6 or ipv4 address
		 dest_static_route : ip address
		 dest_port : destination port
		 app_name : application name
		 app_test :application test
		 

	'''

	

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface_1 =  t['resources']['box']['interfaces']['r0h0']['pic']
	interface_2 =  t['resources']['box']['interfaces']['r0h1']['pic']


	device.log(level='INFO',message='*****Test point: Stream match destination nat rule with app configured!*****')

	device.config(command_list=["set security nat destination pool " + pool_name + " address " + dest_pool_addr,
                     "set security nat destination rule-set " + rule_set + " from interface " + interface_2,
                     "set security nat destination rule-set " + rule_set + " rule " + rule + " match destination-address " + dest_addr,
                     "set security nat destination rule-set " + rule_set+ "  rule " + rule + " then destination-nat pool " + pool_name,
                     "set security nat proxy-arp interface " + interface_2 + " address " + dest_addr,
                     "set routing-options static route " + dest_static_route + "  next-hop " + split_ip_1[0],
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat destination rule-set " + rule_set + " rule " + rule + " match application " + app_name
		])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface_2)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_1[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	time.sleep(5)

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + split_ip_2[0] + ' -id ' + sendip_dest + ' -p  '+ app_test_new + ' ' + split_ip_4[0])

	#time.sleep(1)

	result = verify_flow_session(device,src_ip=split_ip_2[0],dest_ip=sendip_dest,nat_ip=split_ip_1[0],dest_nat=1)


	if result == 1:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')
	else:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')



def different_dest_nat_rule_with_app(device,h0,pool_name1,pool_name2,dest_pool_addr,rule_set,rule1,rule2,dest_addr1,dest_addr2,dest_static_route1,dest_static_route2,sendip_dest1,app_test,app_name1,app_name2,sendip_dest2):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 dest_address : ipv6 or ipv4 address
		 dest_static_route : ip address
		 dest_port : destination port
		 app_name : application name
		 app_test :application test
		 

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface_1 =  t['resources']['box']['interfaces']['r0h0']['pic']
	interface_2 =  t['resources']['box']['interfaces']['r0h1']['pic']

	device.log(level='INFO',message='*****Test point: Two streams match different destination nat rules with app configured!*****')

	device.config(command_list=["set security nat destination pool " + pool_name1 + " address " + dest_pool_addr,
                     "set security nat destination rule-set " + rule_set + " from interface " + interface_2,
                     "set security nat destination rule-set " + rule_set + " rule " + rule1 + " match destination-address " + dest_addr1,
                     "set security nat destination rule-set " + rule_set+ "  rule " + rule1 + " then destination-nat pool " + pool_name1,
                     "set security nat proxy-arp interface " + interface_2 + " address " + dest_addr1,
                     "set routing-options static route " + dest_static_route1 + "  next-hop " + split_ip_1[0],
                     "set applications application " + app_name1 + " protocol " + app_test,
                     "set security nat destination rule-set " + rule_set + " rule " + rule1 + " match application " + app_name1
		])

	device.commit(timeout=180)

	time.sleep(5)


	device.config(command_list=["set security nat destination pool " + pool_name2 + " address " + dest_pool_addr,
                     "set security nat destination rule-set " + rule_set + " from interface " + interface_2,
                     "set security nat destination rule-set " + rule_set + " rule " + rule2 + " match destination-address " + dest_addr2,
                     "set security nat destination rule-set " + rule_set+ "  rule " + rule2 + " then destination-nat pool " + pool_name2,
                     "set security nat proxy-arp interface " + interface_2 + " address " + dest_addr1,
                     "set routing-options static route " + dest_static_route2 + "  next-hop " + split_ip_1[0],
                     "set applications application " + app_name2 + " protocol " + app_test,
                     "set security nat destination rule-set " + rule_set + " rule " + rule2 + " match application " + app_name2
		])

	device.commit(timeout=180)

	time.sleep(5)



	device.cli(command='clear security flow session interface ' + interface_2)

	h0.su()
	result = h0.shell(command='/bin/ping ' + split_ip_1[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	time.sleep(10)

	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + split_ip_2[0] + ' -id ' + sendip_dest1 + ' -p  '+ app_test + ' ' + split_ip_4[0])

	#time.sleep(1)

	result = verify_flow_session(device,src_ip=split_ip_2[0],dest_ip=sendip_dest1,nat_ip=split_ip_1[0],dest_nat=1)

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')

	device.cli(command='clear security flow session')

	time.sleep(5)


	h0.shell(command='sendip -v -d r64 -p ipv4 -iv 4 -ih 5 -il 128 -is ' + split_ip_2[0] + ' -id ' + sendip_dest2 + ' -p  '+ app_test + ' ' + split_ip_4[0])

	##time.sleep(1)

	result = verify_flow_session(device,src_ip=split_ip_2[0],dest_ip=sendip_dest2,nat_ip=split_ip_1[0],dest_nat=1)

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')



def ipv6_source_nat_with_dest_port(device,h0,rule_set,rule,from_zone,to_zone,src_address,dest_port,sendip_src):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 address
		 dest_port : destination port
		

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface_1 =  t['resources']['box']['interfaces']['r0h0']['pic']
	interface_2 =  t['resources']['box']['interfaces']['r0h1']['pic']

	split_ip_5 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ipv6']).split('/')
	split_ip_6 = (t['resources']['box']['interfaces']['r0h1']['uv-ipv6']).split('/')


	device.log(level='INFO',message='*****Test point: IPv6 stream match source nat rule with dst-port configured!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule " + rule  +" match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface",
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match destination-port " + dest_port,
                     "commit"])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface_2)

	h0.su()
	result = h0.shell(command='/bin/ping6 ' + split_ip_5[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	time.sleep(10)

	h0.shell(command='sendip -v -d 100 -p ipv6 -6s ' + sendip_src + ' -6d ' + split_ip_5[0] + ' -p tcp -td ' + dest_port + ' ' + split_ip_5[0])

	##time.sleep(1)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=split_ip_5[0],nat_ip=split_ip_6[0],dest_port=dest_port)

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')


def ipv6_source_nat_with_app(device,h0,rule_set,rule,from_zone,to_zone,src_address,sendip_src,dest_port,app_name,app_test):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 address
		 dest_port : destination port
		

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface_1 =  t['resources']['box']['interfaces']['r0h0']['pic']
	interface_2 =  t['resources']['box']['interfaces']['r0h1']['pic']

	split_ip_5 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ipv6']).split('/')
	split_ip_6 = (t['resources']['box']['interfaces']['r0h1']['uv-ipv6']).split('/')


	device.log(level='INFO',message='*****Test point: IPv6 stream match source/destination nat rule with app configured!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule " + rule  +" match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface",
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match application " + app_name,
                     "commit"])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface_2)

	h0.su()
	result = h0.shell(command='/bin/ping6 ' + split_ip_5[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	time.sleep(10)

	h0.shell(command='sendip -v -d 100 -p ipv6 -6s ' + sendip_src + ' -6d ' + split_ip_5[0] + ' -p ' + app_test + ' -td ' + dest_port + ' ' + split_ip_5[0])

	#time.sleep(1)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=split_ip_5[0],nat_ip=split_ip_6[0],dest_port=dest_port)

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')


def ipv6_source_nat_with_app_neg(device,h0,rule_set,rule,from_zone,to_zone,src_address,sendip_src,dest_port,app_name,app_test,app_test_new):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 address
		 dest_port : destination port
		

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface_1 =  t['resources']['box']['interfaces']['r0h0']['pic']
	interface_2 =  t['resources']['box']['interfaces']['r0h1']['pic']

	split_ip_5 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ipv6']).split('/')
	split_ip_6 = (t['resources']['box']['interfaces']['r0h1']['uv-ipv6']).split('/')


	device.log(level='INFO',message='*****Test point: IPv6 stream doesnt match source/destination nat rule with app configured!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule " + rule  +" match source-address " + src_address,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " then source-nat interface",
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " + rule + " match application " + app_name,
                     "commit"])

	device.commit(timeout=180)

	time.sleep(5)

	device.cli(command='clear security flow session interface ' + interface_2)

	h0.su()
	result = h0.shell(command='/bin/ping6 ' + split_ip_5[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	time.sleep(10)

	h0.shell(command='sendip -v -d 100 -p ipv6 -6s ' + sendip_src + ' -6d ' + split_ip_5[0] + ' -p ' + app_test_new +  ' ' + split_ip_5[0])

	#time.sleep(1)

	result = verify_flow_session(device,src_ip=sendip_src,dest_ip=split_ip_5[0],nat_ip=split_ip_6[0])

	if result == 1:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')
	else:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')


def ipv6_diff_source_nat_with_app(device,h0,rule_set,rule1,rule2,from_zone,to_zone,src_address1,src_address2,sendip_src1,sendip_src2,app_name,app_test):

	'''

	All arguments are string
	
	Arguments:



		 device : DUT 
		 rule_set : rule_set name   
		 from_zone : from_zone name  
		 to_zone : to_zone name  
		 rule : rule name
		 src_address : ipv6 address
		 dest_port : destination port
		

	'''

	split_ip_1 = (t['resources']['lnx1']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_2 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ip']).split('/')
	split_ip_3 = (t['resources']['box']['interfaces']['r0h0']['uv-ip']).split('/')
	split_ip_4 = (t['resources']['box']['interfaces']['r0h1']['uv-ip']).split('/')
	interface_1 =  t['resources']['box']['interfaces']['r0h0']['pic']
	interface_2 =  t['resources']['box']['interfaces']['r0h1']['pic']

	split_ip_5 = (t['resources']['lnx2']['interfaces']['r0h1']['uv-ipv6']).split('/')
	split_ip_6 = (t['resources']['box']['interfaces']['r0h1']['uv-ipv6']).split('/')


	device.log(level='INFO',message='*****Test point: Two streams match different source nat rules with app configured!*****')

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule " + rule1  +" match source-address " + src_address1,
                     "set security nat source rule-set " + rule_set + " rule " + rule1 + " then source-nat interface",
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " + rule1 + " match application " + app_name,
                     "commit"])

	device.commit(timeout=180)

	time.sleep(5)

	device.config(command_list=["set security nat source rule-set " + rule_set + " from zone " + from_zone,
                     "set security nat source rule-set " + rule_set + " to zone " + to_zone,
                     "set security nat source rule-set " + rule_set + " rule " + rule2  +" match source-address " + src_address2,
                     "set security nat source rule-set " + rule_set + " rule " + rule2 + " then source-nat interface",
                     "set applications application " + app_name + " protocol " + app_test,
                     "set security nat source rule-set " + rule_set + " rule " + rule2 + " match application " + app_name,
                     "commit"])

	device.commit(timeout=180)

	time.sleep(5)


	device.cli(command='clear security flow session interface ' + interface_2)

	h0.su()
	result = h0.shell(command='/bin/ping6 ' + split_ip_5[0] + ' -c 10').response()

	match = re.search(".* 100% packet loss", result)

	if match :
		device.log(level='ERROR',message="The link between client and server is failed.")
		raise Exception('')
	else:
		device.log(level='INFO',message="The link between client and server is fine.")

	time.sleep(10)

	h0.shell(command='sendip -v -d 100 -p ipv6 -6s ' + sendip_src1 + ' -6d ' + split_ip_5[0] + ' -p ' + app_test +  ' ' + split_ip_5[0])

	#time.sleep(1)

	result = verify_flow_session(device,src_ip=sendip_src1,dest_ip=split_ip_5[0],nat_ip=split_ip_6[0])

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')

	device.cli(command='clear security flow session')

	time.sleep(5)


	h0.shell(command='sendip -v -d 100 -p ipv6 -6s ' + sendip_src2 + ' -6d ' + split_ip_5[0] + ' -p ' + app_test +  ' ' + split_ip_5[0])

	#time.sleep(1)

	result = verify_flow_session(device,src_ip=sendip_src2,dest_ip=split_ip_5[0],nat_ip=split_ip_6[0])

	if result == 1:
		device.log(level='INFO',message='------PASS: Find the expected session in the session list ! ------')
	else:
		device.log(level='ERROR',message='------FAIL: Not find the expected session in the session list !  ------')
		raise Exception('')








	











