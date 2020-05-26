

def dhcp_ipv6_access(device=None, pool=None, prefix=None, prefix_length=None,range_name=None,address_range_low=None, address_range_high=None, maximum_lease_time=None, commit=False):


    if device is None:
      raise Exception("'device' is mandatory parameter for configuring dhcp")

    if pool is None:
      raise Exception("'pool' is mandatory parameter for configuring dhcp")
      #device.log(level="ERROR", msg="'pool' is a mandatory parameter for configuring dhcp")


    commands = []

    if prefix is not None:
      commands.append('set access address-assignment pool ' + pool + ' family inet6 prefix ' + prefix)

    if range_name is not None and prefix_length is not None:
      commands.append('set access address-assignment pool ' + pool + ' family inet6 range ' +  range_name  + ' prefix-length ' + prefix_length)

    if address_range_low is not None and range_name is not None:
      commands.append('set access address-assignment pool ' + pool + ' family inet6 range ' + range_name + ' low ' + address_range_low)

    if address_range_high is not None and range_name is not None:
      commands.append('set access address-assignment pool ' + pool + ' family inet6 range ' + range_name + ' high ' + address_range_high)

    if maximum_lease_time is not None :
      commands.append('set access address-assignment pool ' + pool + ' family inet6 dhcp-attributes maximum-lease-time ' + maximum_lease_time)

    device.config(command_list=commands)



    if commit:
      return device.commit(timeout=60)
    else:
      return True


def dhcp_ipv6_access_routing_instance(device=None, pool=None, routing_instance=None,prefix=None, prefix_length=None,range_name=None,address_range_low=None, address_range_high=None, maximum_lease_time=None, commit=False):


    if device is None:
      raise Exception("'device' is mandatory parameter for configuring dhcp")

    if pool is None:
      raise Exception("'pool' is mandatory parameter for configuring dhcp")
      #device.log(level="ERROR", msg="'pool' is a mandatory parameter for configuring dhcp")
    if routing_instance is None:
      raise Exception("'routing-instance' is mandatory parameter for configuring dhcp")



    commands = []

    if prefix is not None:
      commands.append('set routing-instance ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet6 prefix ' + prefix)

    if range_name is not None and prefix_length is not None:
      commands.append('set routing-instance ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet6 range ' +  range_name  + ' prefix-length ' + prefix_length)

    if address_range_low is not None and range_name is not None:
      commands.append('set routing-instance ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet6 range ' + range_name + ' low ' + address_range_low)

    if address_range_high is not None and range_name is not None:
      commands.append('set routing-instance ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet6 range ' + range_name + ' high ' + address_range_high)

    if maximum_lease_time is not None :
      commands.append('set routing-instance ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet6 dhcp-attributes maximum-lease-time ' + maximum_lease_time)

    device.config(command_list=commands)



    if commit:
      return device.commit(timeout=60)
    else:
      return True


def dhcp_ipv6_retransmission(device=None, interface=None, retransmission_attempt=None, retransmission_interval=None, commit=False):

    """
        :param Device device:
             **REQUIRED**  Handle of the device on which configuration has to be executed

        :param str pool:
             **REQUIRED**  address pool  . It can be either 'server/client'

        :param str traceoptions:
             **OPTIONAL**  Name of the traceoption configured.

        :param str server-identifier:
            *OPTIONAL*  DHCP server identifier advertised to clients.

        :return:
             * ``True`` when zone configuration is entered
                 :raises Exception:
                    *  When mandatory parameters are missing
                    *  Commit fails(when **commit** is True)
                    *  Device behaves in an unexpected way while in config/cli mode
                    *  Device handle goes bad(device disconnection).

    """
    if device is None:
        raise Exception("'device' is mandatory parameter for configuring dhcp")
    
    commands = []

    if interface is None:
        raise Exception("'device' is mandatory parameter for configuring dhcp")
    else:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcp-client')



    #commands = []

    if retransmission_attempt is not None:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client retransmission-attempt ' + retransmission_attempt)

    if retransmission_interval is not None:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client retransmission-interval ' + retransmission_interval)

    device.config(command_list=commands)
    
    if commit:
        return device.commit(timeout=60)
    else:
        return True



def dhcp_ipv6_attributes_option(device=None,option=None,pool=None,ipv6_address=None,string=None,routing_instance=None,commit=False):


    if device is None:
        raise Exception("'device' is mandatory parameter for configuring dhcp")

    if pool is None:
        raise Exception("'pool' is mandatory parameter for configuring dhcp")

    commands = []

    cmd = 'set access address-assignment pool '

    if option is not None and ipv6_address is not None:
        if isinstance(option,list) and isinstance(ipv6_address,list) :
            cmd = cmd + pool + ' family inet6 dhcp-attributes option '
            option_length = len(option)
            #length = length - 1 
            for length in range (0,len(option)):
                commands.append(cmd + option[length] + ' ipv6-address ' + ipv6_address[length])


    if option is not None and string is not None:
        if isinstance(option,list) and isinstance(string,list) :
            cmd = cmd + pool + ' family inet6 dhcp-attributes option '
            option_length = len(option)
            #length = length - 1 
            for length in range (0,len(option)):
                commands.append(cmd + option[length] + ' string ' + string[length])
           


    device.config(command_list=commands)

        # Committing the config if asked by user
    if commit:
        return device.commit(timeout=60)
    else:
        return True
    


def dhcp_ipv6_attributes_option_routing_instance(device=None,option=None,pool=None,ipv6_address=None,string=None,routing_instance=None,commit=False):


    if device is None:
        raise Exception("'device' is mandatory parameter for configuring dhcp")

    if pool is None:
        raise Exception("'pool' is mandatory parameter for configuring dhcp")

    if routing_instance is None:
      raise Exception("'routing-instance' is mandatory parameter for configuring dhcp")


    commands = []

    cmd = 'set routing-instance ' + routing_instance + ' access address-assignment pool '

    if option is not None and ipv6_address is not None:
        if isinstance(option,list) and isinstance(ipv6_address,list) :
            cmd = cmd + pool + ' family inet6 dhcp-attributes option '
            option_length = len(option)
            #length = length - 1 
            for length in range (0,len(option)):
                commands.append(cmd + option[length] + ' ipv6-address ' + ipv6_address[length])


    if option is not None and string is not None:
        if isinstance(option,list) and isinstance(string,list) :
            cmd = cmd + pool + ' family inet6 dhcp-attributes option '
            option_length = len(option)
            #length = length - 1 
            for length in range (0,len(option)):
                commands.append(cmd + option[length] + ' string ' + string[length])
           


    device.config(command_list=commands)

        # Committing the config if asked by user
    if commit:
        return device.commit(timeout=60)
    else:
        return True


def dhcp_local_server_ipv6(device=None, interface=None,group=None,pool_name=None,rapid_commit=False,delegated_pool=False,commit=False):



    if device is None:
      raise Exception("'device' is mandatory parameter for configuring dhcp")

    if group is None:
        raise Exception("'group' is mandatory parameter for configuring dhcp")
        #device.log(level="ERROR", msg="'pool' is a mandatory parameter for configuring dhcp")

    commands = []


    if group is not None and pool_name is None :
      commands.append('set routing-instances ' + routing_instance + ' system services dhcp-local-server dhcpv6 group ' + group + '  overrides process-inform pool ' + pool_name)

    if group is not None and interface is None :
      commands.append('set routing-instances ' + routing_instance + ' system services dhcp-local-server dhcpv6 group ' + group + ' interface ' + interface)

    if group is not None and pool_name is not None:
      commands.append('set system services dhcp-local-server dhcpv6 group ' + group + '  overrides process-inform pool ' + pool_name)

    if group is not None and pool_name is not None and rapid_commit is True:
      commands.append('set system services dhcp-local-server dhcpv6 group ' + group + '  overrides process-inform pool rapid-commit' )

    if group is not None and pool_name is not None and delegated_pool is True:
      commands.append('set system services dhcp-local-server dhcpv6 group ' + group + '  overrides process-inform pool delegated-pool ' + pool_name )

    if group is not None and interface is not None:
      commands.append('set system services dhcp-local-server dhcpv6 group ' + group + ' interface ' + interface)



    device.config(command_list=commands)



    if commit:
        return device.commit(timeout=60)
    else:
        return True


def dhcp_local_server_ipv6_routing_instance(device=None, interface=None,group=None,pool_name=None,routing_instance=None,rapid_commit=False,delegated_pool=False,commit=False):

    if device is None:
      raise Exception("'device' is mandatory parameter for configuring dhcp")

    if group is None:
        raise Exception("'group' is mandatory parameter for configuring dhcp")
        #device.log(level="ERROR", msg="'pool' is a mandatory parameter for configuring dhcp")
    if routing_instance is None:
        raise Exception("'routing-instance' is mandatory parameter for configuring dhcp")


    commands = []


    if pool_name is not None:
      commands.append('set routing-instances ' + routing_instance + ' system services dhcp-local-server dhcpv6 group ' + group + '  overrides process-inform pool ' + pool_name)

    if interface is not None :
      commands.append('set routing-instances ' + routing_instance + ' system services dhcp-local-server dhcpv6 group ' + group + ' interface ' + interface)

    device.config(command_list=commands)



    if commit:
        return device.commit(timeout=60)
    else:
        return True



def dhcp_relay_ipv6_routing_instance(device=None, server_group=None, server_group_ip=None, group=None, active_server_group=None, interface=None, routing_instance=None,overrides=False,commit=False):

    """
        :param Device device:
                **REQUIRED**  Handle of the device on which configuration has to be executed

        :param str pool_ip:
                **REQUIRED**  address pool  . It can be either 'server/client'



        :return:
                * ``True`` when zone configuration is entered
            :raises Exception:
                *  When mandatory parameters are missing
                *  Commit fails(when **commit** is True)
                *  Device behaves in an unexpected way while in config/cli mode
                *  Device handle goes bad(device disconnection).
    """
    if device is None:
        raise Exception("'device' is mandatory parameter for configuring dhcp")

    if routing_instance is None:
        raise Exception("'routing-instance' is mandatory parameter for configuring dhcp")


    commands = []
  
    if server_group is not None and server_group_ip is not None :
      commands.append('set routing-instances ' + routing_instance + ' forwarding-options dhcp-relay dhcpv6 server-group ' +  server_group  +  ' '  + server_group_ip)

    if group is not None and active_server_group is not None :
      commands.append('set routing-instances ' + routing_instance + ' forwarding-options dhcp-relay dhcpv6 group ' + group + ' active-server-group ' + active_server_group)

    if interface is not None :
      commands.append('set routing-instances ' + routing_instance + ' forwarding-options dhcp-relay dhcpv6 group ' + group + ' interface ' + interface)

    if overrides is not False :
      commands.append('set routing-instances ' + routing_instance + ' forwarding-options dhcp-relay dhcpv6 group ' + group + ' overrides send-release-on-delete')



    device.config(command_list=commands)

    if commit:
        return device.commit(timeout=60)
    else:
        return True


def dhcp_relay_ipv6(device=None, server_group=None, server_group_ip=None, group=None, active_server_group=None, interface=None, routing_instance=None,overrides=False,commit=False):

    """
        :param Device device:
                **REQUIRED**  Handle of the device on which configuration has to be executed

        :param str pool_ip:
                **REQUIRED**  address pool  . It can be either 'server/client'



        :return:
                * ``True`` when zone configuration is entered
            :raises Exception:
                *  When mandatory parameters are missing
                *  Commit fails(when **commit** is True)
                *  Device behaves in an unexpected way while in config/cli mode
                *  Device handle goes bad(device disconnection).
    """
    if device is None:
        raise Exception("'device' is mandatory parameter for configuring dhcp")

    commands = []


    if server_group is not None and server_group_ip is not None:
      commands.append('set forwarding-options dhcp-relay dhcpv6 server-group ' +  server_group  +  ' '  + server_group_ip)

    if group is not None and active_server_group is not None:
      commands.append('set forwarding-options dhcp-relay dhcpv6 group ' + group + ' active-server-group ' + active_server_group)

    if interface is not None and group is not None:
      commands.append('set forwarding-options dhcp-relay dhcpv6 group ' + group + ' interface ' + interface)

    if overrides is not False and group is not None:
      commands.append('set forwarding-options dhcp-relay dhcpv6 group ' + group + ' overrides send-release-on-delete')


        # Committing the config if asked by user
    device.config(command_list=commands)

    if commit:
        return device.commit(timeout=60)
    else:
        return True



def dhcp_relay_ipv6_routing_instance(device=None,server_group=None,server_group_ip=None,group=None,active_server_group=None,interface=None,routing_instance=None,overrides=False,commit=False):

    """
        :param Device device:
                **REQUIRED**  Handle of the device on which configuration has to be executed

        :param str pool_ip:
                **REQUIRED**  address pool  . It can be either 'server/client'



        :return:
                * ``True`` when zone configuration is entered
            :raises Exception:
                *  When mandatory parameters are missing
                *  Commit fails(when **commit** is True)
                *  Device behaves in an unexpected way while in config/cli mode
                *  Device handle goes bad(device disconnection).
    """
    if device is None:
        raise Exception("'device' is mandatory parameter for configuring dhcp")

    if routing_instance is None:
        raise Exception("'routing-instance' is mandatory parameter for configuring dhcp")
    
    commands = []


    if server_group is not None and server_group_ip is not None:
      commands.append('set routing-instances ' + routing_instance + ' forwarding-options dhcp-relay dhcpv6 server-group ' +  server_group  +  ' '  + server_group_ip)

    if group is not None and active_server_group is not None:
      commands.append('set routing-instances ' + routing_instance + ' forwarding-options dhcp-relay dhcpv6 group ' + group + ' active-server-group ' + active_server_group)

    if interface is not None and group is not None:
      commands.append('set routing-instances ' + routing_instance + ' forwarding-options dhcp-relay dhcpv6 group ' + group + ' interface ' + interface)

    if overrides is not False and group is not None:
      commands.append('set routing-instances ' + routing_instance + ' forwarding-options dhcp-relay dhcpv6 group ' + group + ' overrides send-release-on-delete')


        # Committing the config if asked by user
    device.config(command_list=commands)

    if commit:
        return device.commit(timeout=60)
    else:
        return True



def dhcp_ipv6_client(device=None, interface=None, client_type=None,client_ia_type=None,duid_type=None,commit=False):



    if device is None:
      raise Exception("'device' is mandatory parameter for configuring dhcp")

    if interface is None:
        raise Exception("'interface' is a mandatory parameter for configuring dhcp")
      
      #device.log(level="ERROR", msg="'interface' is a mandatory parameter for configuring dhcp")
  
        
    commands = []

    if interface is not None and client_type is not None:
      commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client client-type ' +  client_type)

    if interface is not None and client_ia_type is not None:
      commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client client-ia-type ' + client_ia_type)

    if interface is not None and duid_type is not None:
      commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client client-identifier duid-type ' + duid_type)



    device.config(command_list=commands)

    if commit:
      return device.commit(timeout=60)
    else:
      return True


def dhcp_ipv6_client_req_option(device=None, interface=None, req_option=False, dns_server=False, domain=False,fqdn=False,nis_domain=False,sip_server=False,sip_domain=False,time_zone=False,vendor_spec=False,commit=False):



    if device is None:
      raise Exception("'device' is mandatory parameter for configuring dhcp")

    if interface is None:
        raise Exception("'interface' is a mandatory parameter for configuring dhcp")
      
      #device.log(level="ERROR", msg="'pool' is a mandatory parameter for configuring dhcp")

    if req_option is False:
        raise Exception("'req_option' is a mandatory parameter for configuring dhcp")
      
      #device.log(level="ERROR", msg="'pool' is a mandatory parameter for configuring dhcp")  
        
    commands = []

    if interface is not None and req_option is not False:
      if dns_server:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client req-option dns-server')
      if domain:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client req-option domain')
      if fqdn:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client req-option fqdn')
      if nis_domain:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client req-option nis-domain')
      if sip_server:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client req-option sip-server')
      if sip_domain:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client req-option sip-domain')
      if time_zone:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client req-option time-zone')
      if vendor_spec:
        commands.append('set interfaces ' + interface + ' unit 0 family inet6 dhcpv6-client req-option vendor-spec') 


    device.config(command_list=commands)

    if commit:
      return device.commit(timeout=60)
    else:
      return True
 


def router_advertisement(device=None, interface=None, prefix=None,preferred_lifetime=None,valid_lifetime=None,max_advertisement_interval=None,min_advertisement_interval=None,no_managed_configuration=False,other_stateful_configuration=False,commit=False):


    if device is None:
      raise Exception("'device' is mandatory parameter for configuring dhcp")

    if interface is None:
      raise Exception("'Interface' is mandatory parameter for configuring dhcp")

    
        
    commands = []

    if interface is not None and prefix is not None and preferred_lifetime is not None:
       commands.append('set protocols router-advertisement interface ' + interface + ' prefix ' + prefix + ' preferred-lifetime ' + preferred_lifetime)

    if interface is not None and prefix is not None and valid_lifetime is not None:
       commands.append('set protocols router-advertisement interface ' + interface + ' prefix ' + prefix + ' valid-lifetime ' + valid_lifetime)

    if interface is not None and prefix is not None and max_advertisement_interval is not None:
       commands.append('set protocols router-advertisement interface ' + interface + ' max-advertisement-interval' + max_advertisement_interval)

    if interface is not None and prefix is not None and min_advertisement_interval is not None:
       commands.append('set protocols router-advertisement interface ' + interface + ' min-advertisement-interval' + min_advertisement_interval)

    if prefix is not None:
       commands.append('set protocols router-advertisement interface ' + interface + ' prefix ' + prefix)

    if interface is not None:
       commands.append('set protocols router-advertisement interface ' + interface )

    if no_managed_configuration is not False:
       commands.append('set protocols router-advertisement interface ' + interface + ' no-managed-configuration')
    
    if other_stateful_configuration is not False :
        commands.append('set protocols router-advertisement interface ' + interface + ' other-stateful-configuration')



    device.config(command_list=commands)

    if commit:
      return device.commit(timeout=60)
    else:
      return True


