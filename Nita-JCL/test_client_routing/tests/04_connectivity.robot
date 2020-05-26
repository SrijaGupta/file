*** Settings ***
Documentation     DC Connectivity Test cases

Resource	${JUNIPER_COMMON}/resource_files/connectivity_resources.txt
Resource	${JUNIPER_COMMON}/resource_files/device_resources.txt
Resource	${EXECDIR}/resource_files/resources.txt

Suite Setup	Box Open Connection	client1	client2
Suite Teardown	Box Close Connection	client1	client2

*** Variables ***

${JUNIPER_COMMON}=	${CURDIR}/..
${output_directory}=	${CURDIR}
${path}=	${CURDIR}

*** Keywords ***

*** Test Cases ***

T4.1: PING TEST client1 client2
	[Documentation]	Objective: Check client1 to client2 link
	[Tags]	CONNECTIVITY	client1	client2
	
	# on client1:
	Configure Interface on Box	client1	eth1	${client1_ip}	${client_password}
	Ping Test From Box	client1	${client1_gateway}
	Configure Route on Box	client1	${client2_subnet}	${client1_gateway}	${client_password}
	
	# on client2:
	Configure Interface on Box	client2	eth1	${client2_ip}	${client_password}
	Ping Test From Box	client2	${client2_gateway}
	Configure Route on Box	client2	${client1_subnet}	${client2_gateway}	${client_password}
	
	# on client1:
	Ping Test From Box	client1	${client2_ip}
	# on client2:
	Ping Test From Box	client2	${client1_ip}


T4.2: PING TEST client1 client3
	[Documentation]	Objective: Check client1 to client3 link
	[Tags]	CONNECTIVITY	client1	client3
	
	# on client1:
	Configure Interface on Box	client1	eth1	${client1_ip}	${client_password}
	Ping Test From Box	client1	${client1_gateway}
	Configure Route on Box	client1	${client3_subnet}	${client1_gateway}	${client_password}
	
	# on client3:
	Configure Interface on Box	client3	eth1	${client3_ip}	${client_password}
	Ping Test From Box	client3	${client3_gateway}
	Configure Route on Box	client3	${client1_subnet}	${client3_gateway}	${client_password}
	
	# on client1:
	Ping Test From Box	client1	${client3_ip}
	# on client3:
	Ping Test From Box	client3	${client1_ip}


T4.3: PING TEST client2 client3
	[Documentation]	Objective: Check client2 to client3 link
	[Tags]	CONNECTIVITY	client2	client3
	
	# on client2:
	Configure Interface on Box	client2	eth1	${client2_ip}	${client_password}
	Ping Test From Box	client2	${client2_gateway}
	Configure Route on Box	client2	${client3_subnet}	${client2_gateway}	${client_password}
	
	# on client3:
	Configure Interface on Box	client3	eth1	${client3_ip}	${client_password}
	Ping Test From Box	client3	${client3_gateway}
	Configure Route on Box	client3	${client2_subnet}	${client3_gateway}	${client_password}
	
	# on client1:
	Ping Test From Box	client2	${client3_ip}
	# on client3:
	Ping Test From Box	client3	${client2_ip}

