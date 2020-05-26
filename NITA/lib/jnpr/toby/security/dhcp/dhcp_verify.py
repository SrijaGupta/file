import jxmlease


def check_dhcp_client_statistics(device=None , routing_instance=None, bootreply=False, dhcpoffer=False, dhcpack=False, dhcpnak=False, dhcpforcerenew=False, bootrequest=False, dhcpdecline=False, dhcpdiscover=False, dhcprequest=False, dhcpinform=False, dhcprelease=False, dhcprenew=False, dhcprebind=False, commit=False):
    
    if device is None :
        raise Exception("'device' is mandatory parameter - device handle")
    else:
        result = device.cli(command="show dhcp client statistics",format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

        command = []

    if bootreply:

        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][0]['message'][0]['message-count']) 
        command.append(a)
            

    if dhcpoffer:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][0]['message'][1]['message-count']) 
        command.append(a)
    if dhcpack:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][0]['message'][2]['message-count']) 
        command.append(a)

    if dhcpnak:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][0]['message'][3]['message-count']) 
        command.append(a)

    if dhcpforcerenew:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][0]['message'][4]['message-count']) 
        command.append(a)
    
    if bootrequest:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][0]['message-count']) 
        command.append(a)

    if dhcpdecline:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][1]['message-count']) 
        command.append(a)

    if dhcpdiscover:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][2]['message-count']) 
        command.append(a)

    if dhcprequest:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][3]['message-count']) 
        command.append(a)
    
    if dhcpinform:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][4]['message-count']) 
        command.append(a)

    if dhcprelease:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][5]['message-count']) 
        command.append(a)

    if dhcprenew:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][6]['message-count']) 
        command.append(a)

    if dhcprebind:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][7]['message-count']) 
        command.append(a)

    return command


def check_dhcp_client_statistics_routing_instance(device=None , routing_instance=None, bootreply=False, dhcpoffer=False, dhcpack=False, dhcpnak=False, dhcpforcerenew=False, bootrequest=False, dhcpdecline=False, dhcpdiscover=False, dhcprequest=False, dhcpinform=False, dhcprelease=False, dhcprenew=False, dhcprebind=False, commit=False):
    
    if device is None and routing_instance is None:
        raise Exception("'device' is mandatory parameter - device handle")
    else:
        result = device.cli(command="show dhcp client statistics routing-instance " + routing_instance,format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

    command = []

    if bootreply:

        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][0]['message'][0]['message-count']) 
        command.append(a)
            

    if dhcpoffer:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][0]['message'][1]['message-count']) 
        command.append(a)
    if dhcpack:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][0]['message'][2]['message-count']) 
        command.append(a)

    if dhcpnak:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][0]['message'][3]['message-count']) 
        command.append(a)

    if dhcpforcerenew:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][0]['message'][4]['message-count']) 
        command.append(a)
    
    if bootrequest:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][0]['message-count']) 
        command.append(a)

    if dhcpdecline:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][1]['message-count']) 
        command.append(a) 

    if dhcpdiscover:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][2]['message-count']) 
        command.append(a) 

    if dhcprequest:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][3]['message-count']) 
        command.append(a) 
    
    if dhcpinform:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][4]['message-count']) 
        command.append(a) 

    if dhcprelease:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][5]['message-count']) 
        command.append(a) 

    if dhcprenew:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][6]['message-count']) 
        command.append(a) 

    if dhcprebind:
        a = int(status['rpc-reply']['dhcp-client-statistics-information']['message-table'][1]['message'][7]['message-count']) 
        command.append(a) 

    return command



def check_dhcp_relay_statistics(device=None ,bootreply=False,dhcpoffer=False,dhcpack=False, dhcpnak=False, dhcpforcerenew=False, bootrequest=False, dhcpdecline=False, dhcpdiscover=False, dhcprequest=False, dhcpinform=False, dhcprelease=False, dhcprenew=False, dhcprebind=False,dhcpleaseunassigned=False, dhcpleaseactive=False,dhcpleaseunknown=False,dhcpbulkleasequery=False,dhcpleasequerydone=False,dhcpleasequery=False,commit=False):
    
    if device is None :
        raise Exception("'device' is mandatory parameter - device handle")
    else:
        result = device.cli(command="show dhcp relay statistics",format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

        command = []

    if bootrequest:

        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][0]['message'][0]['message-count']) 
        command.append(a)            

    if dhcpdecline:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][0]['message'][1]['message-count']) 
        command.append(a)

    if dhcpdiscover:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][0]['message'][2]['message-count']) 
        command.append(a)

    if dhcpinform:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][0]['message'][3]['message-count']) 
        command.append(a)

    if  dhcprelease:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][0]['message'][4]['message-count']) 
        command.append(a)
    
    if dhcprequest:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][0]['message'][5]['message-count']) 
        command.append(a)

    if dhcpleaseactive:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][0]['message'][6]['message-count']) 
        command.append(a)

    if dhcpleaseunassigned:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][0]['message'][7]['message-count']) 
        command.append(a)

    if dhcpleaseunknown:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][0]['message'][8]['message-count']) 
        command.append(a)
    
    if dhcpleasequerydone:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][0]['message'][9]['message-count']) 
        command.append(a)

    if bootreply:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][1]['message'][0]['message-count']) 
        command.append(a)

    if dhcpoffer:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][1]['message'][1]['message-count']) 
        command.append(a)

    if dhcpack:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][1]['message'][2]['message-count']) 
        command.append(a)

    if dhcpnak:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][1]['message'][3]['message-count']) 
        command.append(a)

    if dhcpforcerenew:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][1]['message'][4]['message-count']) 
        command.append(a)

    if dhcpleasequery:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][1]['message'][5]['message-count']) 
        command.append(a)

    if dhcpbulkleasequery:
        a = int(status['rpc-reply']['dhcp-relay-statistics-information']['message-table'][1]['message'][6]['message-count']) 
        command.append(a)

    return command  



def check_dhcp_server_statistics(device=None ,bootreply=False,dhcpoffer=False,dhcpack=False, dhcpnak=False, dhcpforcerenew=False, bootrequest=False, dhcpdecline=False, dhcpdiscover=False, dhcprequest=False, dhcpinform=False, dhcprelease=False, dhcprenew=False, dhcprebind=False,dhcpleaseunassigned=False, dhcpleaseactive=False,dhcpleaseunknown=False,dhcpleasequery=False,dhcpbulkleasequery=False,dhcpleasequerydone=False,commit=False):
    
    if device is None :
        raise Exception("'device' is mandatory parameter - device handle")
    else:
        result = device.cli(command="show dhcp server statistics",format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

        command = []

    if bootrequest:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][0]['message'][0]['message-count']) 
        command.append(a)

    if dhcpdecline:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][0]['message'][1]['message-count']) 
        command.append(a)

    if dhcpdiscover:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][0]['message'][2]['message-count']) 
        command.append(a)

    if dhcpinform:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][0]['message'][3]['message-count']) 
        command.append(a)
    
    if dhcprelease:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][0]['message'][4]['message-count']) 
        command.append(a)

    if dhcprequest:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][0]['message'][5]['message-count']) 
        command.append(a)

    if dhcpleasequery:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][0]['message'][6]['message-count']) 
        command.append(a)

    if dhcpbulkleasequery:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][0]['message'][7]['message-count']) 
        command.append(a)
    
    if bootreply:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][1]['message'][0]['message-count']) 
        command.append(a)

    if dhcpoffer:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][1]['message'][1]['message-count']) 
        command.append(a)

    if dhcpack:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][1]['message'][2]['message-count']) 
        command.append(a)

    if dhcpnak:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][1]['message'][3]['message-count']) 
        command.append(a)

    if dhcpforcerenew:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][1]['message'][4]['message-count']) 
        command.append(a)

    if dhcpleaseunassigned:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][1]['message'][5]['message-count']) 
        command.append(a)

    if dhcpleaseunknown:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][1]['message'][6]['message-count']) 
        command.append(a)

    if dhcpleaseactive:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][1]['message'][7]['message-count']) 
        command.append(a)

    if dhcpleasequerydone:
        a = int(status['rpc-reply']['dhcp-server-statistics-information']['message-table'][1]['message'][8]['message-count']) 
        command.append(a)

    return command  






def check_dhcpv6_relay_statistics_routing_instance(device=None ,routing_instance=None,dhcpv6_decline=False,dhcpv6_solicit=False,dhcpv6_information_request=False, dhcpv6_release=False, dhcpv6_request=False, dhcpv6_confirm=False, dhcpv6_renew=False, dhcpv6_rebind=False, dhcpv6_relay_forw=False, dhcpv6_leasequery_reply=False, dhcpv6_leasequery_data=False, dhcpv6_leasequery_done=False, dhcpv6_advertise=False,dhcpv6_reply=False, dhcpv6_reconfigure=False,dhcpv6_relay_repl=False,dhcpv6_leasequery=False,commit=False):
    
    if device is None and routing_instance is None:
        raise Exception("'device' is mandatory parameter - device handle")
    else:
        result = device.cli(command="show dhcpv6 relay statistics routing-instance " + routing_instance,format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

    command = []

    if dhcpv6_decline:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][0]['dhcpv6-message-count']) 
        command.append(a)            

    if dhcpv6_solicit:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][1]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_information_request:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][2]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_release:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][3]['dhcpv6-message-count']) 
        command.append(a)

    if  dhcpv6_request:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][4]['dhcpv6-message-count']) 
        command.append(a)
    
    if dhcpv6_confirm:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][5]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_renew:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][6]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_rebind:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][7]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_relay_forw:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][8]['dhcpv6-message-count']) 
        command.append(a)
    
    if dhcpv6_leasequery_reply:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][9]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery_data:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][10]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery_done:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][11]['dhcpv6-message-count']) 
        command.append(a)


    if dhcpv6_advertise:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][0]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_reply:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][1]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_reconfigure:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][2]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_relay_repl:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][3]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][4]['dhcpv6-message-count']) 
        command.append(a)



    return command    


def check_dhcpv6_relay_statistics(device=None ,dhcpv6_decline=False,dhcpv6_solicit=False,dhcpv6_information_request=False, dhcpv6_release=False, dhcpv6_request=False, dhcpv6_confirm=False, dhcpv6_renew=False, dhcpv6_rebind=False, dhcpv6_relay_forw=False, dhcpv6_leasequery_reply=False, dhcpv6_leasequery_data=False, dhcpv6_leasequery_done=False, dhcpv6_advertise=False,dhcpv6_reply=False, dhcpv6_reconfigure=False,dhcpv6_relay_repl=False,dhcpv6_leasequery=False,commit=False):
    
    if device is None :
        raise Exception("'device' is mandatory parameter - device handle")
    else:
        result = device.cli(command="show dhcpv6 relay statistics" ,format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

    command = []

    if dhcpv6_decline:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][0]['dhcpv6-message-count']) 
        command.append(a)            

    if dhcpv6_solicit:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][1]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_information_request:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][2]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_release:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][3]['dhcpv6-message-count']) 
        command.append(a)

    if  dhcpv6_request:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][4]['dhcpv6-message-count']) 
        command.append(a)
    
    if dhcpv6_confirm:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][5]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_renew:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][6]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_rebind:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][7]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_relay_forw:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][8]['dhcpv6-message-count']) 
        command.append(a)
    
    if dhcpv6_leasequery_reply:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][9]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery_data:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][10]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery_done:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][11]['dhcpv6-message-count']) 
        command.append(a)


    if dhcpv6_advertise:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][0]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_reply:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][1]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_reconfigure:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][2]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_relay_repl:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][3]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery:
        a = int(status['rpc-reply']['dhcpv6-relay-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][4]['dhcpv6-message-count']) 
        command.append(a)



    return command  


def check_dhcpv6_server_statistics(device=None ,dhcpv6_decline=False,dhcpv6_solicit=False,dhcpv6_information_request=False, dhcpv6_release=False, dhcpv6_request=False, dhcpv6_confirm=False, dhcpv6_renew=False, dhcpv6_rebind=False, dhcpv6_relay_forw=False, dhcpv6_leasequery_reply=False, dhcpv6_leasequery_data=False, dhcpv6_leasequery_done=False, dhcpv6_advertise=False,dhcpv6_reply=False, dhcpv6_reconfigure=False,dhcpv6_relay_repl=False,dhcpv6_leasequery=False,commit=False):
    
    if device is None :
        raise Exception("'device' is mandatory parameter - device handle")
    else:
        result = device.cli(command="show dhcpv6 server statistics" ,format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

    command = []

    if dhcpv6_decline:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][0]['dhcpv6-message-count']) 
        command.append(a)            

    if dhcpv6_solicit:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][1]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_information_request:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][2]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_release:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][3]['dhcpv6-message-count']) 
        command.append(a)

    if  dhcpv6_request:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][4]['dhcpv6-message-count']) 
        command.append(a)
    
    if dhcpv6_confirm:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][5]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_renew:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][6]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_rebind:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][7]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_relay_forw:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][8]['dhcpv6-message-count']) 
        command.append(a)
    
    if dhcpv6_leasequery:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][9]['dhcpv6-message-count']) 
        command.append(a)

    

    if dhcpv6_advertise:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][0]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_reply:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][1]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_reconfigure:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][2]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_relay_repl:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][3]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery_reply:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][4]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery_data:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][5]['dhcpv6-message-count']) 
        command.append(a)
    if dhcpv6_leasequery_done:

        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][6]['dhcpv6-message-count']) 
        command.append(a)

    return command  


def check_dhcpv6_server_statistics_routing_instance(device=None ,routing_instance=None,dhcpv6_decline=False,dhcpv6_solicit=False,dhcpv6_information_request=False, dhcpv6_release=False, dhcpv6_request=False, dhcpv6_confirm=False, dhcpv6_renew=False, dhcpv6_rebind=False, dhcpv6_relay_forw=False, dhcpv6_leasequery_reply=False, dhcpv6_leasequery_data=False, dhcpv6_leasequery_done=False, dhcpv6_advertise=False,dhcpv6_reply=False, dhcpv6_reconfigure=False,dhcpv6_relay_repl=False,dhcpv6_leasequery=False,commit=False):
    
    if device is None :
        raise Exception("'device' is mandatory parameter - device handle")
    else:
        result = device.cli(command="show dhcpv6 server statistics routing-instance " + routing_instance,format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

    command = []

    if dhcpv6_decline:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][0]['dhcpv6-message-count']) 
        command.append(a)            

    if dhcpv6_solicit:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][1]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_information_request:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][2]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_release:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][3]['dhcpv6-message-count']) 
        command.append(a)

    if  dhcpv6_request:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][4]['dhcpv6-message-count']) 
        command.append(a)
    
    if dhcpv6_confirm:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][5]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_renew:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][6]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_rebind:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][7]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_relay_forw:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][8]['dhcpv6-message-count']) 
        command.append(a)
    
    if dhcpv6_leasequery:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][9]['dhcpv6-message-count']) 
        command.append(a)

    

    if dhcpv6_advertise:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][0]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_reply:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][1]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_reconfigure:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][2]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_relay_repl:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][3]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery_reply:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][4]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery_data:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][5]['dhcpv6-message-count']) 
        command.append(a)
    if dhcpv6_leasequery_done:

        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][6]['dhcpv6-message-count']) 
        command.append(a)

    return command  




def check_dhcp_client_binding(device=None ,Interface=None,dhcpv6_solicit=False,dhcpv6_information_request=False, dhcpv6_release=False, dhcpv6_request=False, dhcpv6_confirm=False, dhcpv6_renew=False, dhcpv6_rebind=False, dhcpv6_relay_forw=False, dhcpv6_leasequery_reply=False, dhcpv6_leasequery_data=False, dhcpv6_leasequery_done=False, dhcpv6_advertise=False,dhcpv6_reply=False, dhcpv6_reconfigure=False,dhcpv6_relay_repl=False,dhcpv6_leasequery=False,commit=False):
    
    if device is None :
        raise Exception("'device' is mandatory parameter - device handle")
    else:
        result = device.cli(command="show dhcp client binding interface " + interface + " detail" ,format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

    command = []

    if dhcpv6_decline:
        a = int(status['rpc-reply']['dhcp-client-binding-information']['dhcpv6-message-table'][0]['dhcpv6-message'][0]['dhcpv6-message-count']) 
        command.append(a)            

    if dhcpv6_solicit:
        a = int(status['rpc-reply']['dhcp-client-binding-information']['dhcpv6-message-table'][0]['dhcpv6-message'][1]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_information_request:
        a = int(status['rpc-reply']['dhcp-client-binding-information']['dhcpv6-message-table'][0]['dhcpv6-message'][2]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_release:
        a = int(status['rpc-reply']['dhcp-client-binding-information']['dhcpv6-message-table'][0]['dhcpv6-message'][3]['dhcpv6-message-count']) 
        command.append(a)

    if  dhcpv6_request:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][4]['dhcpv6-message-count']) 
        command.append(a)
    
    if dhcpv6_confirm:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][5]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_renew:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][6]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_rebind:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][7]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_relay_forw:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][8]['dhcpv6-message-count']) 
        command.append(a)
    
    if dhcpv6_leasequery:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][0]['dhcpv6-message'][9]['dhcpv6-message-count']) 
        command.append(a)

    

    if dhcpv6_advertise:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][0]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_reply:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][1]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_reconfigure:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][2]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_relay_repl:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][3]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery_reply:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][4]['dhcpv6-message-count']) 
        command.append(a)

    if dhcpv6_leasequery_data:
        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][5]['dhcpv6-message-count']) 
        command.append(a)
    if dhcpv6_leasequery_done:

        a = int(status['rpc-reply']['dhcpv6-server-statistics-information']['dhcpv6-message-table'][1]['dhcpv6-message'][6]['dhcpv6-message-count']) 
        command.append(a)

    return command  

import jxmlease


def check_dhcp_client_binding(device=None ,interface=None,interface_name=False,mac_address=False,lease_state=False, allocated_address=False, server_ip_address=False,dhcp_lease_time=False, server_identifier=False, router=False, name_server=False, boot_file=False, boot_server=False, subnet_mask=False, domain_name=False, wins_server=False,commit=False):
    
    if device is None and interface is None:
        raise Exception("'device' is mandatory parameter - device handle")
    else:
        result = device.cli(command="show dhcp client binding interface " + interface + " detail" ,format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)

    command = []

    if interface_name:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['interface-name']
        command.append(a)            

    if mac_address:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['mac-address']
        command.append(a)

    if lease_state:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['lease-state']
        command.append(a)

    if allocated_address:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['allocated-address']
        command.append(a)

    if server_ip_address:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['server-ip-address']
        command.append(a) 

    if  dhcp_lease_time:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['dhcp-option-table']['dhcp-option'][0]['dhcp-option-value']
        command.append(a)
    
    if server_identifier:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['dhcp-option-table']['dhcp-option'][1]['dhcp-option-value'] 
        command.append(a)

    if router:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['dhcp-option-table']['dhcp-option'][2]['dhcp-option-value']
        command.append(a)

    if name_server:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['dhcp-option-table']['dhcp-option'][3]['dhcp-option-value'] 
        command.append(a)

    if boot_file:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['dhcp-option-table']['dhcp-option'][4]['dhcp-option-value']
        command.append(a)
    
    if boot_server:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['dhcp-option-table']['dhcp-option'][5]['dhcp-option-value'] 
        command.append(a)   

    if subnet_mask:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['dhcp-option-table']['dhcp-option'][6]['dhcp-option-value'] 
        command.append(a)

    if domain_name:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['dhcp-option-table']['dhcp-option'][7]['dhcp-option-value'] 
        command.append(a)

    if wins_server:
        a = status['rpc-reply']['dhcp-client-binding-information']['dhcp-binding']['dhcp-option-table']['dhcp-option'][8]['dhcp-option-value'] 
        command.append(a)



    return command  

