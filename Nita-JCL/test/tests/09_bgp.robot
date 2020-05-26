*** Settings ***
Documentation     DC BGP Test cases

Resource	${JUNIPER_COMMON}/resource_files/device_resources.txt
Resource	${EXECDIR}/resource_files/resources.txt
Resource	${JUNIPER_COMMON}/resource_files/show_cmd_keywords.txt

Suite Setup	Run Keywords		Device Open Connection	vqfx1
...         AND				Device Open Connection	vqfx2
...         AND				Device Open Connection	vqfx3
...         AND				Device Open Connection	vqfx4
...         AND				Device Open Connection	vqfx5
...         AND				Device Open Connection	vmx1
...         AND				Device Open Connection	vmx2


Suite Teardown  Run Keywords	    Device Close Connection	vqfx1
...	        AND                 Device Close Connection	vqfx2
...	        AND                 Device Close Connection	vqfx3
...	        AND                 Device Close Connection	vqfx4
...	        AND                 Device Close Connection	vqfx5
...	        AND                 Device Close Connection	vmx1
...	        AND                 Device Close Connection	vmx2

*** Variables ***

${JUNIPER_COMMON}=	${CURDIR}/..
${output_directory}=	${CURDIR}
${path}=	${CURDIR}

*** Keywords ***

*** Test Cases ***
T9.1: BGP NEIGHBORS SPINE1
    [Documentation]	Objective: Check BGP is working on vmx1
    [Tags]	 BGP
    Check BGP Neighbors     vmx1	2

T9.2: BGP NEIGHBORS SPINE2
    [Documentation]	Objective: Check BGP is working on vmx2
    [Tags]	 BGP
    Check BGP Neighbors     vmx2	2 

T9.3: BGP NEIGHBORS SPINE1
    [Documentation]	Objective: Check BGP is working on vqfx1
    [Tags]	 BGP
    Check BGP Neighbors     vqfx1	5

T9.4: BGP NEIGHBORS SPINE2
    [Documentation]	Objective: Check BGP is working on vqfx2
    [Tags]	 BGP
    Check BGP Neighbors     vqfx2	5 

T9.5: BGP NEIGHBORS LEAF1
    [Documentation]	Objective: Check BGP is working on vqfx3
    [Tags]	 BGP
    Check BGP Neighbors     vqfx3	2

T9.6: BGP NEIGHBORS LEAF2
    [Documentation]	Objective: Check BGP is working on vqfx4
    [Tags]	 BGP
    Check BGP Neighbors     vqfx4	2

T9.7: BGP NEIGHBORS LEAF3
    [Documentation]	Objective: Check BGP is working on vqfx5
    [Tags]	 BGP
    Check BGP Neighbors     vqfx5	2
