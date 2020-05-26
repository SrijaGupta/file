*** Settings ***
Documentation
...     Resource file containing basic keywords to related to verification engine.
...
...     This resource file contains keywords to verify all the checks with given
...     input yaml file and additional features like single line feature veriifcation

Library      jnpr/toby/engines/verification/verifyEngine.py


*** Variables ***


*** Keywords ***
Initialize Verification Engine
        [Documentation]     initilize verify  yaml file and it is used by subsequent keywords
	    [Arguments]		${file}
        
        initialize verify engine    file=${file}    is_robot=True


Verify All Checks Under ${verify_file}
	    [Documentation]	   Verifying all checks under the given verify yaml file

	    verify all checks api    file=${verify_file}      is_robot=True

Verify Dictionary 
            [Documentation]        Verifying checks using dict format
	    [Arguments]		${dict_input}
		
            ${status} =  verify dict   input_dict=${dict_input}
            Should Be True      '${status}' == 'True'   

get all info
            [Documentation]        get all data under the given verify yaml file

            &{status} =  verify all checks api     type=get
            [Return]    &{status}

get info ${tmpl} using ${attsVals} On ${device}
        [Documentation]     get info  using direct robot keywords ( statement )

        &{status} =  verify specific checks api   type=get   info=${tmpl}   args=${attsVals}   devices=${device}
        [Return]    &{status}

Verify tags ${tags}
        [Documentation]    Verifying subset of checks based on given tag values 

        verify all checks api    tag=${tags}     is_robot=True


Verify All Checks On ${devices_list}
        [Documentation]    Verifying all checks under the initilize file On Subset of Devices

        verify all checks api    devices=${devices_list}   is_robot=True


verify all checks 
        [Documentation]    Verifying all checks under intilize verify yaml file  
        [Arguments]    &{kwargs}

	verify all checks api     is_robot=True     &{kwargs}


Verify checks ${testcases} On ${devices}  
	    [Documentation]	    Verifying specific checks Under Initilize verify yaml File on subset of devices
	
	    verify specific checks api		checks=${testcases}	   devices=${devices}        is_robot=True

Verify checks 
        [Documentation]         Verifying specific checks/file/Devices
        [Arguments]    &{kwargs}

	verify specific checks api       is_robot=True    &{kwargs}

Verify ${attsVals} Using ${tmpl} On ${router}
	[Documentation]	    verificaion based on direct robot keywords ( statement )

	verify statement checks   stanzas=${attsVals}	   template=${tmpl}     devices=${router}     is_robot=True

get
        [Documentation]    get info using specific args
        [Arguments]    &{kwargs}

        ${status} =     get specific data		&{kwargs}
        [Return]    ${status}

Verify
        [Documentation]         Verifying specific checks/file/Devices
        [Arguments]    &{kwargs}

        verify specific checks api    is_robot=True      &{kwargs}

get verify results
        [Documentation]    get last verify results and values
        [Arguments]    &{kwargs}

        ${result} =     get last verify result        &{kwargs}
        [Return]    ${result}

Verify in parallel
        [Documentation]   keyword to run checks in parallel
        [Arguments]    &{kwargs}

        verify specific checks in parallel    is_robot=True    &{kwargs}

