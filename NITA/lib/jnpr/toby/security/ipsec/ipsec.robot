*** Settings ***
Documentation  Resource file for IPSEC.
...            This resource file has the keywords that can be used to perform
...            Ipsec related config and verifcation


Library           jnpr/toby/security/pki/pki.py
Library           jnpr/toby/security/ipsec/ipsec.py
Library           jnpr/toby/security/ipsec/ipsecsrx.py
Library           jnpr/toby/security/interfaces/interfaces.py
Library           OperatingSystem
Resource          jnpr/toby/hldcl/device.robot

*** Keywords ***
configure nexthop
    [Documentation]   Keyword configures next-hop style ipsec config
    ...               This is a high level keyword for configuring next
    ...               hop ipsec style config. This keywords configures basic ipsec
    ...               config. To use differnt ipsec config use the low level ipsec
    ...               keywords directly listed at http://rbu.juniper.net/jdi-test-dashboard/catalogue2/toby_kw_catalogue.html
    ...
    ...               Args:
    ...               |- dh:  Device handle
    ...               |- kwargs:  Arguments as key: value pairs
    ...                  For supported key-value pairs
    ...               |- estd_tun:  establish tunnels immediately (supported values 1 or 0)
    ...                  Look at 'create ipsec object' in http://rbu.juniper.net/jdi-test-dashboard/catalogue2/toby_kw_catalogue.html
    ...               Note if ike_auth='rsa-signatures' then  local_cert=''  local_id_fqdn=''  remote_id_fqdn=''  are  mandatory
    ...               By default ike_auth='pre-shared-keys'
    ...
    ...               Example:
    ...               For Pres-hared-keys:
    ...                 ${my_dict} =  create dictionary  local_gw=${t['resources']['r0']['interfaces']['r0-r1']['uv-ip']}
    ...                                remote_gw=${t['resources']['r1']['interfaces']['r0-r1']['uv-ip']}
    ...                                svc_intf=${t['resources']['r0']['interfaces']['r0-ms0-0']['pic']}
    ...                                intf=${t['resources']['r0']['interfaces']['r0-r1']['pic']}   estd_tun=1
    ...
    ...                 configure nexthop    ${dh0}  &{my_dict}
    ...
    ...               For RSA:
    ...
    ...                ${my_dict} =  create dictionary  local_gw=${t['resources']['r0']['interfaces']['r0-r1']['uv-ip']}
    ...                              remote_gw=${t['resources']['r1']['interfaces']['r0-r1']['uv-ip']}
    ...                              svc_intf=${t['resources']['r0']['interfaces']['r0-ms0-0']['pic']}
    ...                              intf=${t['resources']['r0']['interfaces']['r0-r1']['pic']} ike_auth=rsa-signatures
    ...                              local_cert=local_cert1  local_id_fqdn=juniper.net
    ...                configure nexthop    ${dh0}  &{my_dict}

    [Arguments]   ${dh}   &{my_dict}

    log  Configuring next hop with given parmeters &{my_dict}
    ${auth_value}=  Evaluate  $mydict.get('ike_auth')

    #log  ${my_dict['estd_tun']}
    #${ipsec_obj} =  Create Ipsec Object  ${dh}  local_gw=${my_dict['local_gw']}  remote_gw=${my_dict['remote_gw']}  svc_intf=${my_dict['svc_intf']}
    ${ipsec_obj} =  Create Ipsec Object  ${dh}  &{my_dict}
    Run keyword if  '${auth_value}' == 'rsa-signatures'
    ...     configure ipsec   ${ipsec_obj}  local_cert=${my_dict['local_cert']}  local_id_fqdn=${my_dict['local_id_fqdn']}  remote_id_fqdn=${my_dict['remote_id_fqdn']}
    ...     ELSE
    ...     configure ipsec   ${ipsec_obj}

    configure ipsec vpn rule  ${ipsec_obj}
    configure service set  ${ipsec_obj}
    Configure interface    device=${dh}     interface=${my_dict['intf']}    address=${my_dict['local_gw']}    unit=0
    Commit configuration   device=${dh}

configure dep
    [Documentation]   Keyword configures DEP style ipsec config
    ...               Follow the documentaion  from  'configure nexthop'
    ...               Example:
    ...               configure dep  ${dh0}  &{my_dict}

    [Arguments]   ${dh}   &{my_dict}

    log  Configuring DEP style with given parmeters &{my_dict}
    ${auth_value}=  Evaluate  $mydict.get('ike_auth')

    ${ipsec_obj} =  Create Ipsec Object  ${dh}  &{my_dict}

    Run keyword if  '${auth_value}' == 'rsa-signatures'
    ...     configure ipsec   ${ipsec_obj}  local_cert=${my_dict['local_cert']}  local_id_fqdn=${my_dict['local_id_fqdn']}  remote_id_fqdn=${my_dict['remote_id_fqdn']}
    ...     ELSE
    ...     configure ipsec   ${ipsec_obj}
    configure access   ${ipsec_obj}
    configure service set   ${ipsec_obj}   ike_access=1   dial_options=1
    Configure interface    device=${dh}     interface=${my_dict['intf']}    address=${my_dict['local_gw']}    unit=0
    Commit configuration   device=${dh}

configure link style
    [Documentation]   Keyword configures link style ipsec config
    ...               Follow the documentaion  from  'configure nexthop'
    ...               Example:
    ...               configure link style ${dh0}  &{my_dict}

    [Arguments]   ${dh}   &{my_dict}

    log  Configuring link style with given parmeters &{my_dict}
    ${auth_value}=  Evaluate  $mydict.get('ike_auth')

    ${ipsec_obj} =  Create Ipsec Object  ${dh}  &{my_dict}
    Run keyword if  '${auth_value}' == 'rsa-signatures'
    ...     configure ipsec   ${ipsec_obj}  local_cert=${my_dict['local_cert']}  local_id_fqdn=${my_dict['local_id_fqdn']}  remote_id_fqdn=${my_dict['remote_id_fqdn']}
    ...     ELSE
    ...     configure ipsec   ${ipsec_obj}
    configure service set  ${ipsec_obj}
    configure ipsec vpn rule  ${ipsec_obj}  ipsec_ins_intf=1
    Configure interface    device=${dh}     interface=${my_dict['intf']}    address=${my_dict['local_gw']}    unit=0
    Commit configuration   device=${dh}
