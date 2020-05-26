def dhcp_ipv4_traceoptions(device=None, file=None, level=None, flag=None, commit=False):

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

    if file is not None:
        commands.append('set system services dhcp traceoptions ' + ' file ' + file)

    if level is not None:
        commands.append('set system services dhcp traceoptions ' + ' level ' + level)

    if flag is not None:
        commands.append('set system services dhcp traceoptions ' + ' flag ' + flag)

    device.config(command_list=commands)
    
    if commit:
        return device.commit(timeout=60)
    else:
        return True

    #if file is not None:
    #    commands.append('set system services dhcp traceoptions ' + ' file ' + file)

def dhcp_ipv4_pool(device=None, pool_ip=None, address_range_low=None, address_range_high=None, maximum_lease_time=None, 
    default_lease_time=None, router=None, server_identifier=None, commit=False):

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

    if pool_ip is None:
        device.log(level="ERROR", msg="'pool_ip' is a mandatory parameter for configuring dhcp")

    commands = []

    if address_range_low is not None:
       commands.append('set system services dhcp pool ' + pool_ip + ' address-range low ' + address_range_low)

    if address_range_high is not None:
       commands.append('set system services dhcp pool ' + pool_ip + ' address-range high ' + address_range_high)

    if maximum_lease_time is not None:
       commands.append('set system services dhcp pool ' + pool_ip + ' maximum-lease-time ' + maximum_lease_time)

    if default_lease_time is not None:
       commands.append('set system services dhcp pool ' + pool_ip + ' default-lease-time ' + default_lease_time)

    if router is not None:
       commands.append('set system services dhcp pool ' + pool_ip + ' router ' + router)

    if server_identifier is not None:
       commands.append('set system services dhcp pool ' + pool_ip + ' server-identifier ' + server_identifier)


        # Committing the config if asked by user
    device.config(command_list=commands)



    if commit:
        return device.commit(timeout=60)
    else:
        return True



def dhcp_ipv4_access_routing_instance(device=None, pool=None, routing_instance=None, network=None, range_name=None, address_range_low=None, address_range_high=None, maximum_lease_time=None, server_identifier=None, domain_name=None, name_server=None, wins_server=None, router=None, boot_file=None, boot_server=None, tftp_server=None, netbios_node_type=None, option=None, integer=None, commit=False):


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

    if pool is None:
        device.log(level="ERROR", msg="'pool' is a mandatory parameter for configuring dhcp")

    if routing_instance is None:
        device.log(level="ERROR", msg="routing-instance is a mandatory parameter for configuring dhcp")


    commands = []

    
    if network is not None:
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet network ' + network)

    if address_range_low is not None :
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet range ' + range_name + ' low ' + address_range_low)

    if address_range_high is not None:
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet range ' + range_name + ' high ' + address_range_high)

    if maximum_lease_time is not None:
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes maximum-lease-time ' + str(maximum_lease_time))

    if server_identifier is not None:
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes server-identifier ' + server_identifier) 

    if domain_name is not None :
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes domain-name ' + domain_name)

    if name_server is not None:
        if isinstance(name_server, list) and len(name_server) >=  1:
            for temp in name_server:
                commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes  name-server ' + temp)
    
    

    if wins_server is not None:
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes wins-serve ' + str(wins_server))
       
    if router is not None:
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes router ' + router)


    if boot_file is not None :
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes boot-file ' + boot_file)
       
    if boot_server is not None :
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes boot-server ' + boot_server)
       
    if tftp_server is not None :
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes tftp-server ' +  tftp_server)
       
    if netbios_node_type is not None :
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes netbios-node-type ' +  netbios_node_type)

    if option is not None and  integer is not None :
       commands.append('set routing-instances ' + routing_instance + ' access address-assignment pool ' + pool + ' family inet dhcp-attributes option ' +  str(option)  + ' integer '  +  str(integer))


    device.config(command_list=commands)



    if commit:
        return device.commit(timeout=60)
    else:
        return True
    

def dhcp_ipv4_access(device=None, pool=None,network=None, range_name=None,address_range_low=None, address_range_high=None, maximum_lease_time=None, server_identifier=None, domain_name=None, name_server=None,wins_server=None, router=None, boot_file=None,boot_server=None,tftp_server=None,netbios_node_type=None,option=None,integer=None,commit=False):

   
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

    if pool is None:
        device.log(level="ERROR", msg="'pool' is a mandatory parameter for configuring dhcp")

    commands = []


    if network is not None:
       commands.append('set access address-assignment pool ' + pool + ' family inet network ' + network)
    

    if address_range_low is not None:
       commands.append('set access address-assignment pool ' + pool + ' family inet range ' + range_name + ' low ' + address_range_low)
    

    if address_range_high is not None:
       commands.append('set access address-assignment pool ' + pool + ' family inet range ' + range_name + ' high ' + address_range_high)
    

    if maximum_lease_time is not None:
       commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes  maximum-lease-time ' + str(maximum_lease_time))
    
    if server_identifier is not None:
       commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes  server-identifier ' + server_identifier) 
    

    if domain_name is not None:
       commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes  domain-name ' + domain_name)
       

    if name_server is not None:
        if isinstance(name_server, list) and len(name_server) >=  1:
            for temp in name_server:
                commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes  name-server ' + temp)
    
    

    if wins_server is not None :
       commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes  wins-serve ' + str(wins_server))
    
       
    if router is not None :
       commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes  router ' + router)
    


    if boot_file is not None :
       commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes boot-file ' + boot_file)
    
       
    if boot_server is not None :
       commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes boot-server ' + boot_server)
      
       
    if tftp_server is not None :
       commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes tftp-server ' +  tftp_server)
    
       
    if netbios_node_type is not None :
       commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes  netbios-node-type ' +  netbios_node_type)
     

    if option is not None and  integer is not None:
       commands.append('set access address-assignment pool ' + pool + ' family inet dhcp-attributes  option ' +  str(option)  + ' integer '  +  str(integer))
        


        # Committing the config if asked by user
    device.config(command_list=commands)



    if commit:
        return device.commit(timeout=60)
    else:
        return True


def access_group_profile(device=None, group_profile=None,primary_dns=None,secondary_dns=None,primary_wins=None,secondary_wins=None,commit=False):
    
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

    if group_profile is None:
        device.log(level="ERROR", msg="'pool_ip' is a mandatory parameter for configuring dhcp")

    commands = []

    if device is not None and group_profile is not None and primary_dns is not None:
        if isinstance(primary_dns, list):
            for temp in primary_dns:
                commands.append('set access group-profile  ' + group_profile + ' ppp primary-dns  ' + temp)
    if device is not None and group_profile is not None and secondary_dns is not None:
        if isinstance(secondary_dns, list):
            for temp in secondary_dns:
                commands.append('set access group-profile  ' + group_profile + ' ppp secondary-dns  ' + temp)
    

    device.config(command_list=commands)
    
    if commit:
        return device.commit(timeout=60)
    else:
        return True



def dhcp_ipv4_retransmission(device=None, interface=None, retransmission_attempt=None, retransmission_interval=None, commit=False):

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
        commands.append('set interfaces ' + interface + ' unit 0 family inet dhcp-client')



    #commands = []

    if retransmission_attempt is not None:
        commands.append('set interfaces ' + interface + ' unit 0 family inet dhcp-client retransmission-attempt ' + retransmission_attempt)

    if retransmission_interval is not None:
        commands.append('set interfaces ' + interface + ' unit 0 family inet dhcp-client retransmission-interval ' + retransmission_interval)

    device.config(command_list=commands)
    
    if commit:
        return device.commit(timeout=60)
    else:
        return True



def dhcp_relay(device=None, server_group=None, server_group_ip=None, group=None, active_server_group=None, interface=None, commit=False):

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
       commands.append('set forwarding-options dhcp-relay server-group ' +  server_group  +  ' '  + server_group_ip)

    if group is not None and active_server_group is not None:
       commands.append('set forwarding-options dhcp-relay group ' + group + ' active-server-group ' + active_server_group)

    if interface is not None:
       commands.append('set forwarding-options dhcp-relay group ' + group + ' interface ' + interface)


        # Committing the config if asked by user
    device.config(command_list=commands)

    if commit:
        return device.commit(timeout=60)
    else:
        return True


def dhcp_clear_binding(device=None, routing_instance=None,commit=False):

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
    else:
        device.cli(command="clear dhcp client binding all")
        device.cli(command="clear dhcp server binding all")
        device.cli(command="clear dhcp relay binding all")
        device.cli(command="clear dhcp client statistics")
        device.log('dhcp binding cleared')

    if device is not None and routing_instance is not None:

        device.cli(command="clear dhcp client binding all routing-instance " + routing_instance)
        device.cli(command="clear dhcp client statistics routing-instance " + routing_instance)


    





















