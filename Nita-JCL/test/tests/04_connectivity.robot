*** Settings ***
Documentation     DC Connectivity Test cases

Resource	${JUNIPER_COMMON}/resource_files/connectivity_resources.txt
Resource	${JUNIPER_COMMON}/resource_files/device_resources.txt
Resource	${EXECDIR}/resource_files/resources.txt

Suite Setup     Device Open Connection	vmx1	vmx2	vqfx1	vqfx2	vqfx3	vqfx4	vqfx5
Suite Teardown	Device Close Connection	vmx1	vmx2	vqfx1	vqfx2	vqfx3	vqfx4	vqfx5

*** Variables ***

${JUNIPER_COMMON}=	${CURDIR}/..
${output_directory}=	${CURDIR}
${path}=	${CURDIR}

*** Keywords ***

*** Test Cases ***

T4.1.1: PING TEST ROUTER1 SPINE1 LINK
	[Documentation]	Objective: Check vmx1 to vqfx1 link
	[Tags]	CONNECTIVITY	vmx1	vqfx1

	Ping Test Between Devices	vmx1	vqfx1	${ci_vmx1_ge_0_0_1}	${ci_vqfx1_em3}

T4.1.1: PING TEST ROUTER1 SPINE2 LINK
	[Documentation]	Objective: Check vmx1 to vqfx2 link
	[Tags]	CONNECTIVITY	vmx1	vqfx2

	Ping Test Between Devices	vmx1	vqfx2	${ci_vmx1_ge_0_0_2}	${ci_vqfx2_em3}

T4.2.1: PING TEST ROUTER2 SPINE1 LINK
	[Documentation]	Objective: Check vmx2 to vqfx1 link
	[Tags]	CONNECTIVITY	vmx2	vqfx1

	Ping Test Between Devices	vmx2	vqfx1	${ci_vmx2_ge_0_0_1}	${ci_vqfx1_em4}

T4.2.1: PING TEST ROUTER2 SPINE2 LINK
	[Documentation]	Objective: Check vmx2 to vqfx2 link
	[Tags]	CONNECTIVITY	vmx2	vqfx2

	Ping Test Between Devices	vmx2	vqfx2	${ci_vmx2_ge_0_0_2}	${ci_vqfx2_em4}

T4.3: PING TEST SPINE1 LEAF1 LINK
	[Documentation]	Objective: Check vqfx1 to vqfx3 link
	[Tags]	CONNECTIVITY	vqfx1	vqfx3

	Ping Test Between Devices	vqfx1	vqfx3	${ci_vqfx1_em5}	${ci_vqfx3_em3}

T4.4: PING TEST SPINE1 LEAF2 LINK
	[Documentation]	Objective: Check vqfx1 to vqfx4 link
	[Tags]	CONNECTIVITY	vqfx1	vqfx4

	Ping Test Between Devices	vqfx1	vqfx4	${ci_vqfx1_em6}	${ci_vqfx4_em3}

T4.5: PING TEST SPINE1 LEAF3 LINK
	[Documentation]	Objective: Check vqfx1 to vqfx5 link
	[Tags]	CONNECTIVITY	vqfx1	vqfx5

	Ping Test Between Devices	vqfx1	vqfx5	${ci_vqfx1_em7}	${ci_vqfx5_em3}

T4.6: PING TEST SPINE2 LEAF1 LINK
	[Documentation]	Objective: Check vqfx2 to vqfx3 link
	[Tags]	CONNECTIVITY	SPINE2	LEAF1

	Ping Test Between Devices	vqfx2	vqfx3	${ci_vqfx2_em5}	${ci_vqfx3_em4}

T4.7: PING TEST SPINE2 LEAF2 LINK
	[Documentation]	Objective: Check vqfx2 to vqfx4 link
	[Tags]	CONNECTIVITY	vqfx2	vqfx4

	Ping Test Between Devices	vqfx2	vqfx4	${ci_vqfx2_em6}	${ci_vqfx4_em4}

T4.8: PING TEST SPINE2 LEAF3 LINK
	[Documentation]	Objective: Check vqfx2 to vqfx5 link
	[Tags]	CONNECTIVITY	vqfx2	vqfx5

	Ping Test Between Devices	vqfx2	vqfx5	${ci_vqfx2_em7}	${ci_vqfx5_em4}

