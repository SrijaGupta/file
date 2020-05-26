'''
    IxLoad Library is High level support for Ixload automation.
'''
from jnpr.toby.trafficgen.ixia.ixload.IxUtils import IxUtils as IxLoadUtils
IX_UTIL = IxLoadUtils()

def load_config(rt_handle, rxf_file_path, username, password, sftp_enable=0):
    '''
        load_config Call will load the saved cofiguration into Ixload.
        Args:
        Example:
        - load_config("C:/Users/Administrator/Documents/Ixia/IxLoad/Repository/waseem_testing.rxf")
        Return:
        - Success: {"status": 1}
        - Failure: {'status': 0, 'log': Exception("unable to load sample.rxf as file doesnt exist")}
    '''
    try:
        filename = rxf_file_path.split("/")[-1]
        path = 'C:\\inetpub\\ftproot'
        remote_path = "%s\\%s" % (path, filename)
        if sftp_enable:
            IX_UTIL.sftp_load_config(rt_handle.appserver, username, password, rxf_file_path, remote_path)
        else:
            IX_UTIL.ftp_load_config(rt_handle.appserver, username, password, rxf_file_path)
        rt_handle.log(level="INFO", message="Loading the configuration: %s \n" % filename)
        IX_UTIL.load_repository(rt_handle, rt_handle.session_url, remote_path)
    except Exception as err:
        return {"status": 0, "log": err}
    return {"status": 1}

def start_test(rt_handle):
    '''
        start_test Call to start the configured test.
        Args:
        Example:
        - start_test()
        Return:
        - Success: {"status": 1, "state":running}
        - Failure: {'status': 0, 'log': Exception("No ports have been assigned to \
                                                   'Traffic2@Network2'. Please assign one \
                                                    or more ports and retry")
    '''
    try:
        IX_UTIL.run_test(rt_handle, rt_handle.session_url)
        state = IX_UTIL.get_test_current_state(rt_handle, rt_handle.session_url)
        if state.lower() == "running":
            return {"status": 1, "state": state}
        else:
            return {"status": 0, "state": state}
    except Exception as err:
        return {"status": 0, "log": err}

def stop_test(rt_handle):
    '''
        stop_test Call to stop the configured test.
        Args:
        Example:
        - stop_test()
        Return:
        - Success: {"status": 1, "state":unconfigured}
        - Failure: {'status': 0, 'log': Exception("No ports have been assigned to \
                                                'Traffic2@Network2'. Please assign one \
                                                    or more ports and retry")
    '''
    try:
        IX_UTIL.stop_traffic(rt_handle, rt_handle.session_url)
        state = IX_UTIL.get_test_current_state(rt_handle, rt_handle.session_url)
        if state.lower() == "unconfigured":
            return {"status": 1}
        else:
            return {"status": 0, "state": state}
    except Exception as err:
        return {"status": 0, "log": err}

def get_stats(rt_handle, stats_to_display, polling_interval=0, duration=0):
    '''
    get stats Call to poll the selected stats.
        Args:
            stats_to_display =   {
                        #format: { stats_source : [stat name list] }
                        "HTTPClient": ["Transaction Rates"],
                        "HTTPServer": ["TCP Failures"]
                    }
        - stats_to_display - stats to pull in the above format.
        Example:
            stats_to_display =   {
                        #format: { stats_source : [stat name list] }
                        "HTTPClient": ["Transaction Rates"],
                        "HTTPServer": ["TCP Failures"]
                    }
        - get_stats(stats_to_display)
        Return:
        -Success : {"status": 1, "stats": {HTTPClient": {"Transaction Rates":30},
                                           "HTTPServer": {"TCP Failures":0} }
        -Failure : {"status": 0, "log": "HTTPClient-Transaction Rates stats are not availble}
    '''
    try:
        state = IX_UTIL.get_test_current_state(rt_handle, rt_handle.session_url)
        if state.lower() == 'running':
            stats = IX_UTIL.poll_stats(rt_handle, rt_handle.session_url, stats_to_display, polling_interval, duration)
        else:
            raise Exception("Cannot Get Stats when ActiveTest State - '%s'"%state)
    except Exception as err:
        return {"status": 0, "log": err}
    return {"status": 1, "stats": stats}

def save_config(rt_handle, rxf_file_path, username, password, sftp_enable=0):
    '''
       save_config Call will save the cofiguration in a given path.
       Args:
        -rxf_file_path : path where configuration need to saved, configuration will be saved in .rxf.
       Example:
       - rxf_file_path = "C:/Program Files (x86)/Python36-32/http.rxf"
       -save_config(rxf_file_path)
       Return:
       -Success :
    '''
    try:
        filename = rxf_file_path.split("/")[-1]
        path = 'C:\\inetpub\\ftproot'
        remote_path = "%s\\%s" % (path, filename)
        IX_UTIL.stop_traffic(rt_handle, rt_handle.session_url)
        IX_UTIL.get_test_current_state(rt_handle, rt_handle.session_url)
        IX_UTIL.save_rxf(rt_handle, rt_handle.session_url, remote_path)
        if sftp_enable:
            IX_UTIL.sftp_save_config(rt_handle.appserver, username, password, remote_path, rxf_file_path)
        else:
            IX_UTIL.ftp_save_config(rt_handle.appserver, username, password, filename)
    except Exception as err:
        return {"status": 0, "log": err}
    return {"status": 1}

def disconnect(rt_handle):
    '''
    Donnect Call to disconnect to the IxLoadLoad API server.
    Example:
    -disconnect()
    Return:
    -Success: {'status': 1}
    -Failure: {'status': 0, 'log': Exception(Failed to close to the session "sessions/2")}
    '''
    try:
        IX_UTIL.delete_session(rt_handle, rt_handle.session_url)
    except Exception as err:
        return {"status": 0, "log": err}
    return {"status": 1}

def get_test_status(rt_handle):
    '''
        get_test_status will return the current test status.
    '''
    try:
        state = IX_UTIL.get_test_current_state(rt_handle, rt_handle.session_url)
        return {"status": 1, "state": state}
    except Exception as err:
        return {"status": 0, "log": err}

def add_chassis(rt_handle, chassis_list, portlist_per_community=None):
    '''
        add_chassis Call to connect to the chassis.
        Args:
        - chassis_list - List of Chassis that are needed for the test.
        - portlist_per_community - List of Ports per Community that are needed for the test.
        Example:
        - add_chassis([10.221.113.254,10.221.113.251])
          kportlist_per_community =    {
                                    "Traffic1@Network1" : [(1,5,1)]
                                }
            #"Traffic2@Network2" : [(1,5,2)]
        - add_chassis([10.221.113.254,10.221.113.251], kportlist_per_community)

        Return:
        - Success: {'status': 1}
        - Failure: {'status': 0, 'log': Exception("Error while executing action \
                                                   'sessions/2/ixload/chassisChain/chassis_list'.Error \
                                                    Port Assignment	Error adding chassis 10.221.113.251: Invalid \
                                                     chassis name or IP provided. Please check if sspt-ixia is \
                                                    correct.",)}
    '''
    try:
        portlist_per_community = {} if portlist_per_community is None else portlist_per_community
        IX_UTIL.clear_chassis_list(rt_handle, rt_handle.session_url)
        if not isinstance(chassis_list, list):
            chassis_list = [chassis_list]
        IX_UTIL.add_chassis_list(rt_handle, rt_handle.session_url, chassis_list)
        if len(portlist_per_community) > 0:
            rt_handle.log(level="INFO", message="Assigning the ports: %s \n" % portlist_per_community)
            IX_UTIL.assign_ports(rt_handle, rt_handle.session_url, portlist_per_community)
            return {"status": 1}
    except Exception as err:
        return {"status": 0, "log": err}
    return {"status": 1}

def add_ports(rt_handle, portlist_per_community):
    '''
    add_ports Call to assign the ports to networks.
        Args:
        portlist_per_community =    {
                                    "Traffic1@Network1" : [(1,5,1)],
                                    "Traffic2@Network2" : [(1,5,2)]
                               }
        - portlist_per_community - ports per network in the above format.
        Example:
        portlist_per_community =    {
                                    "Traffic1@Network1" : [(1,5,1)],
                                    "Traffic2@Network2" : [(1,5,2)]
                               }
        - add_ports(portlist_per_community)
    '''
    try:
        IX_UTIL.assign_ports(rt_handle, rt_handle.session_url, portlist_per_community)
    except Exception as err:
        return {"status":0, "log": err}
    return {"status": 1}

def timeline_http_config(rt_handle, config_dict):
    '''
    Configure the timeline of HTTP based on objective type.
    '''
    try:
        IX_UTIL.get_objective_type(rt_handle, rt_handle.session_url)
        IX_UTIL.configure_time_line(rt_handle, rt_handle.session_url, config_dict)
    except Exception as err:
        return {"status":0, "log": err}
    return {"status": 1}

def timeline_ftp_config(rt_handle, config_dict):
    '''
     Configure the timeline of FTP based on objective type.
    '''
    try:
        IX_UTIL.configure_time_line(rt_handle, rt_handle.session_url, config_dict)
    except Exception as err:
        return {"status":0, "log": err}
    return {"status": 1}

def emulation_http(rt_handle, network_name, **kwargs):
    '''
        Create or modify the Http Protocol Emulation.
    '''
    try:
        if "mode" not in kwargs.keys():
            raise Exception('Argument mode not found, mode is a mandatory argument')
        IX_UTIL.emulation_protocol(rt_handle, rt_handle.session_url, network_name, "HTTP", "type1", kwargs)
    except Exception as err:
        return {"status":0, "log": err}
    return {"status": 1}

def network_config(rt_handle, **kwargs):
    '''
    network config will allow users to configure Netwrok configuration on IxLoad
    configuration on ethernet, mac, vlan, IP, Emulated roauter etc.
    '''
    try:
        if "network_name" not in kwargs.keys():
            raise Exception('mode is Argument network_name not found, a mandatory argument')
        network_name = kwargs['network_name']
        kwargs.pop('network_name')
        if len(kwargs) > 0:
            ethernet_args, kwargs = IX_UTIL.get_args("eth_", kwargs)
            ip_args, kwargs = IX_UTIL.get_args("ip_", kwargs)
            mac_args, kwargs = IX_UTIL.get_args("mac_", kwargs)
            vlan_args, kwargs = IX_UTIL.get_args("vlan_", kwargs)
            emulated_router_args, kwargs = IX_UTIL.get_args("er_", kwargs)
            if len(ethernet_args) > 0:
                IX_UTIL.configure_ethernet(rt_handle, rt_handle.session_url, network_name, ethernet_args)
            if len(ip_args) > 0:
                IX_UTIL.configure_ip(rt_handle, rt_handle.session_url, network_name, ip_args)
            if len(mac_args) > 0:
                IX_UTIL.configure_mac(rt_handle, rt_handle.session_url, network_name, mac_args)
            if len(vlan_args) > 0:
                IX_UTIL.configure_vlan(rt_handle, rt_handle.session_url, network_name, vlan_args)
            if len(emulated_router_args) > 0:
                if "mode" not in emulated_router_args.keys():
                    raise Exception('Argument er_mode not found, er_mode is a mandatory argument for Emulated Router config')
                IX_UTIL.configure_emulated_router(rt_handle, rt_handle.session_url, network_name, emulated_router_args)
    except Exception as err:
        return {"status":0, "log": err}
    return {"status": 1}

def delete_chassis(rt_handle, chassis_list):
    '''
    This method will delete chassis from configured test.
    '''
    try:
        IX_UTIL.remove_chassis_list(rt_handle, rt_handle.session_url, chassis_list)
    except Exception as err:
        return {"status": 0, "log": err}
    return {"status": 1}

def delete_port(rt_handle, port_list_per_community):
    '''
    This method will delete ports from configured test.
    '''
    try:
        IX_UTIL.remove_port(rt_handle, rt_handle.session_url, port_list_per_community)
    except Exception as err:
        return {"status": 0, "log": err}
    return {"status": 1}

def emulation_ftp(rt_handle, network_name, **kwargs):
    '''
        Create or modify the Ftp Protocol Emulation.
    '''
    try:
        if "mode" not in kwargs.keys():
            raise Exception('Argument mode not found, mode is a mandatory argument')
        IX_UTIL.emulation_protocol(rt_handle, rt_handle.session_url, network_name, "FTP", "type1", kwargs)
    except Exception as err:
        return {"status":0, "log": err}
    return {"status": 1}

def emulation_dns(rt_handle, network_name, **kwargs):
    '''
        Create or modify the DNS Protocol Emulation.
    '''
    try:
        if "mode" not in kwargs.keys():
            raise Exception('Argument mode not found, mode is a mandatory argument')
        IX_UTIL.emulation_protocol(rt_handle, rt_handle.session_url, network_name, "DNS", "type2", kwargs)
    except Exception as err:
        return {"status":0, "log": err}
    return {"status": 1}

def get_session(rt_handle):
    '''
        get_session will return the session id
    '''
    try:
        session_id = IX_UTIL.get_session_status(rt_handle, rt_handle.session_url)
    except Exception as err:
        return {"status":0, "log": err}
    return {"status": 1, "session":session_id}