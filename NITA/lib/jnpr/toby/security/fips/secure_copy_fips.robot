***Settings***
Documentation    Keyword Used to do secure copy Fips package based on the image version
...              it takes one argument as device handle of the router 
Resource   jnpr/toby/Master.robot
Library    String

*** Variables ***

${dest_path}     /var/tmp/
${source_path}   regress@eng-shell6.juniper.net\:/volume/build/junos

*** Keywords ***

Secure Copy Fips
   [Arguments]    ${device}
   [Documentation]    Copies FIPS packages to device
   ${router_re0}=    set variable    ${device}
   Set Global Variable    ${router_re0}
   ${check}=       Execute Shell Command on Device   ${router_re0}    command=uname -a
   ${check_image}=   Get Regexp Matches   ${check}   occam
   ${string_len}=    Get Length   ${check_image}
   ${ret_image}=    set variable if   ${string_len}==0    non occam    occam 
   Run keyword if   ${string_len}==0     Begin
   [return]    ${ret_image}

Begin    	
    [Documentation]    Internal keyword. Start the transfer
    ${status}=	Execute CLI Command on Device   ${router_re0}    command=show version | match Junos:
	${status_match}=   Split String   ${status}   ${SPACE}
	${version}=  Get From List  ${status_match}  1
	Set Global Variable    ${version}
	Run keyword if  '${version[4]}'=='-'	GetProductionVersion
	Run keyword if  '${version[4]}'!='-'	GetVersion
	${list}=	Execute shell Command On Device     ${router_re0}     command=sysctl -a | egrep -i 'hw.machine_arch'
	${partial_match} =  Split String   ${list}   ${SPACE}
	${Processor_type} =  Get From List    ${partial_match}    1
	Log  "Processor_type=${Processor_type}"
	${image}=   Set Variable If   
	...	'${Processor_type}'=='i386'   fips-mode-i386-${version}-signed.tgz
	...     '${Processor_type}'=='amd64'  fips-mode-i386-${version}-signed.tgz	  
	...	'${Processor_type}'=='powerpc'  fips-mode-ppc-${version}-signed.tgz 
	...	'${Processor_type}'!='powerpc' and '${Processor_type}'!='i386' and '${Processor_type}'!='amd64'    unknown	  
	Log   "${image}"
	${result}=   Set Variable If   
	...	'${version[4]}'=='-' 	production
	...	'${version[4]}'=='X'   	service
	...	'${version[4]}'=='F' or '${version[4]}'=='R'   release
	Log   "result=${result}"
	Set Global Variable    ${result}
	Run keyword if  '${result}'=='production'	GetProductionPath
	Run keyword if  '${result}'!='production'	GetPath
	Log   "search_path=${search_path}"
	${source_path}=	  Catenate    SEPARATOR=/  ${source_path}  ${search_path}  
	${source_path}=	  Catenate    SEPARATOR=/  ${source_path}  ship
    ${source_path}=	  Catenate    SEPARATOR=/  ${source_path}  ${image}
    ${temp_image}=   set variable  cvs-update-external.log  
    Log   "source_path=${source_path}"
    Execute shell Command on Device    ${router_re0}    command=scp -o "StrictHostKeyChecking no" ${source_path} ${dest_path}  pattern=(.*)Password:(.*)
    Execute Shell Command on Device   ${router_re0}   command=MaRtInI   timeout=${300}
	Execute shell Command On Device     ${router_re0}     command=cd ${dest_path}
	Execute shell Command On Device     ${router_re0}     command=pwd
	${list_of_fips_image}=	 Execute shell Command On Device     ${router_re0}     command=ls *fips*${Processor_type}*.tgz
	${list_of_fips_image}=	 Execute shell Command On Device     ${router_re0}     command=ls ${image}

GetProductionVersion
    [Documentation]    Internal keyword. Checks the OS version
	${version} =     Should Match Regexp     ${version}  (\\d{2}.\\d-\\d+.\\d)
	${version} =     set variable     ${version[0]}
	Set Global Variable    ${version}
	Log  "version=${version}"
	${partial_prod}=   Split String   ${version}   -
	${prod_match}=  Get From List  ${partial_prod}  1
	${prod_match} =     Should Match Regexp     ${prod_match}  (\\d+.\\d) 
	Set Global Variable    ${prod_match}
	Log  "prod_match=${prod_match[0]}"
	@{root_version}=   Should Match Regexp   ${version}  (\\d{2}\.\\d)
	${partial_root_ver}=  Split String    @{root_version}  0
	Set Global Variable    ${partial_root_ver}
	${root_ver}=  Get From List  ${partial_root_ver}  0
	#${root_version}=   Should Match Regexp   ${version}  (\\d+.\\d)
	Log  "root_ver=${root_ver}"

GetVersion
    [Documentation]    Internal Keyword. Gets the version
	${version} =     Should Match Regexp     ${version}  (\\d{2}.\\d[A-Z]\\d+.\\d)
	${version} =     set variable     ${version[0]}
	Set Global Variable    ${version}
	Log  "version=${version}"
	@{root_version}=   Should Match Regexp   ${version}  (\\d{2}\.\\d)
	${partial_root_ver}=  Split String    @{root_version}  0
	Set Global Variable    ${partial_root_ver}
	${root_ver}=  Get From List  ${partial_root_ver}  0
	Set Global Variable    ${root_ver}
	Log  "root_ver=${root_ver}"

GetProductionPath
    [Documentation]    Internal Keyword. Constructs the path
    ${search_path}=   Set Variable        ${partial_root_ver[0]}/${result}/${prod_match[0]}
	Set Global Variable    ${search_path}
	Log  ${search_path}

GetPath
    [Documentation]    Internal Keyword. Sets the path
    ${search_path}=   Set Variable        ${partial_root_ver[0]}/${result}/${version}
	Set Global Variable    ${search_path}
	Log  ${search_path}
