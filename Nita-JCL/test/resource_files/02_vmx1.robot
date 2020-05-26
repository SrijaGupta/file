*** Settings ***
Documentation   Router Test cases

Resource	resources.txt
Resource	show_cmd_keywords.txt
Resource	device_resources.txt

Suite Setup 	Device Open Connection	${device}
Suite Teardown 	Device Close Connection	${device}

*** Variables ***

# Device to test
${device}=    vmx107

# Time diff against UTC
${time_diff}=	+ 0 minutes

*** Keywords ***

*** Test Cases ***

T1.1: CHECK SYSTEM SOFTWARE VERSION
	[Documentation]	Objective: Check software version
	[Tags]	 SYSTEM	SWITCH	SOFTWARE
	Check Software Version	${device}	19.2R1.2

T1.2: CHECK SYSTEM USER
	[Documentation]	Objective: Check System User Information
	[Tags]	SYSTEM USER
	Check System User Information	${device}

T1.3: CHECK CONFIGURATION
	[Documentation]	Objective: Check configuration for the device
	[Tags]	SYSTEM CONFIGURATION
	Check Configuration	${device}

T1.4: SHOW ROUTING TABLE
	[Documentation]	Objective: Check routing table
	[Tags]	SYSTEM	SWITCH
	Check Routing Table	${device}

T1.5: SHOW PFE STATISTICS LOCAL TRAFFIC
	[Documentation]	Objective: Check PFE statistics
	[Tags]	SYSTEM	SWITCH
	Check PFE Statistics Local Traffic	${device}

T1.6: CHECK SYSTEM CURRENT TIME
	[Documentation]	Objective: Check system current time
	[Setup] 	Run Keyword	${device}.Commands Executor	command=set date ntp 192.168.56.11 	format=text
	[Tags]	SYSTEM	SWITCH
	Check System Current Time	${device} 	${time_diff}

T1.7: CHECK NO CHASSIS ALARMS
	[Documentation]	Objective: Check there are no chassis alarms
	[Tags]	SYSTEM	SWITCH	ALARMS
	Check No Chassis Alarms	${device}

T1.8: CHECK NO SYSTEM ALARMS
	[Documentation]	Objective: Check there are no system alarms
	[Tags]	SYSTEM	SWITCH	ALARMS
	Check No System Alarms	${device}

T1.9: CHECK NO CORE DUMPS PRESENT
	[Documentation]	Objective: Check there are no core dumps present
	[Tags]	SYSTEM	SWITCH	ALARMS
	Check Core Dumps	${device}

T1.10: CHECK '/dev/ad0s1a' PARTITION HAVE ENOUGH FREE SPACE FOR UPGRADE
	[Documentation]	Objective: Check '/dev/ad0s1a' partition have at least 400MB for upgrade
	[Tags]	SYSTEM	SWITCH
	Check Partition	${device}

T1.11: CHECK FPC IS ONLINE
	[Documentation]	Objective: Check FPC is Online
	[Tags]	SYSTEM	SWITCH
	Check FPC Is Online	${device}
