import jxmlease


def check_ha_flow(device=None, node=None, session_state=None, in_source_address=None, in_if=None, in_destination_address=None, out_source_address=None, out_if=None, out_destination_address=None, protocol=None):
    """

    This function is used for checking statistics value for Screens

    Examples:
    python - check_screen_statistics_value(device=device_handler, expected=expected_child_tag)

    :param Device device:
        **REQUIRED** Router handle object
    :param str interface:
        **REQUIRED** Interface name like ge-0/0/1
    :param str expected:
        **REQUIRED** Expected screen statistic info like "ids-statistics-icmp-fragment"

    :return: Exception will occurred if expected value not be present
    """
    if device is None:
        raise Exception("'device' is mandatory parameter - device handle")
    if node is None:
        device.log(level="ERROR", msg="'node' is mandatory parameter")
        raise Exception("'node' is mandatory parameter")

    if out_source_address is None:
        out_source_address = in_destination_address
    if out_destination_address is None:
        out_destination_address = in_source_address
    
    if node == 'node0':
        node = 'node 0'
    else:
        node = 'node 1'
    if device is not None and node is not None:
        result = device.cli(command="show security flow session " + node, format='xml').response()
        #result = result.split("\n",1)[2]
        #result = 'n'.join(result.split('n')[2:])
        device.log(result)

        status = jxmlease.parse(result)
        device.log(status)
        device.log(level='INFO', message='node name : ' + status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['re-name'])
        device.log(status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session']['session-state'])

        #count = len(status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['displayed-session-count'])
        #device.log(count)
        #for i in count:
        session_status = status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session']['session-state']
        device.log(session_status)
        if session_status == 'Active' or session_status == 'Backup':
            device.log(level='INFO', message='Session is ' + session_status + ' on ' + node)
            if in_source_address is not None:
            
                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session']['flow-information'][0]['source-address'] == in_source_address:
                    device.log(level='INFO', message='IN : source-address is matched ' + in_source_address)
                else:
                    device.log(level='ERROR', message='IN : source-address is not matched ' + in_source_address)

            if in_destination_address is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session']['flow-information'][0]['destination-address'] == in_destination_address:
                    device.log(level='INFO', message='IN : Destination-address is matched : ' + in_destination_address )
                else:
                    device.log(level='ERROR', message='IN : Destination-address is not matched : ' + in_destination_address )
            
            if protocol is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session']['flow-information'][0]['protocol'] == protocol:
                    device.log(level='INFO', message='IN : protocol is matched : ' + protocol )
                else:
                    device.log(level='ERROR', message='IN : protocol is not matched : ' + protocol )

            if out_source_address is not None:
            
                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session']['flow-information'][1]['source-address'] == out_source_address:
                    device.log(level='INFO', message='OUT : source-address is matched ' + out_source_address)
                else:
                    device.log(level='ERROR', message='OUT : source-address is not matched ' + out_source_address)

            if out_destination_address is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session']['flow-information'][1]['destination-address'] == out_destination_address:
                    device.log(level='INFO', message='OUT : Destination-address is matched : ' + out_destination_address )
                else:
                    device.log(level='ERROR', message='OUT : Destination-address is not matched : ' + out_destination_address )
            
            if protocol is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session']['flow-information'][1]['protocol'] == protocol:
                    device.log(level='INFO', message='OUT : protocol is matched : ' + protocol )
                else:
                    device.log(level='ERROR', message='OUT : protocol is not matched : ' + protocol )
        else:
            device.log(level='ERROR', message='Session is not active on ' + node)
            raise Exception("value not present")


def check_ha_dual_flow(device=None, node=None, session_state=None, in_source_address=None, in_if=None, in_destination_address=None, out_source_address=None, out_if=None, out_destination_address=None, protocol=None, in_destination_port=None, out_source_port=None):
    """

    This function is used for checking statistics value for Screens

    Examples:
    python - check_screen_statistics_value(device=device_handler, expected=expected_child_tag)

    :param Device device:
        **REQUIRED** Router handle object
    :param str interface:
        **REQUIRED** Interface name like ge-0/0/1
    :param str expected:
        **REQUIRED** Expected screen statistic info like "ids-statistics-icmp-fragment"

    :return: Exception will occurred if expected value not be present
    """
    if device is None:
        raise Exception("'device' is mandatory parameter - device handle")
    if node is None:
        device.log(level="ERROR", msg="'node' is mandatory parameter")
        raise Exception("'node' is mandatory parameter")

    if out_source_address is None:
        out_source_address = in_destination_address
    if out_destination_address is None:
        out_destination_address = in_source_address
    
    if node == 'node0':
        node = 'node 0'
    else:
        node = 'node 1'
    if device is not None and node is not None:
        result = device.cli(command="show security flow session " + node, format='xml').response()
        #result = result.split("\n",1)[2]
        #result = 'n'.join(result.split('n')[2:])
        device.log(result)

        status = jxmlease.parse(result)
        device.log(status)
        device.log(level='INFO', message='node name : ' + status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['re-name'])
        session_status = status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][0]['session-state']
        device.log("First Session state " + session_status)
        if session_status == 'Active' or session_status == 'Backup':
            if in_source_address is not None:
            
                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][0]['flow-information'][0]['source-address'] == in_source_address:
                    device.log(level='INFO', message='IN : source-address is matched ' + in_source_address)
                else:
                    device.log(level='ERROR', message='IN : source-address is not matched ' + in_source_address)

            if in_destination_address is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][0]['flow-information'][0]['destination-address'] == in_destination_address:
                    device.log(level='INFO', message='IN : Destination-address is matched : ' + in_destination_address )
                else:
                    device.log(level='ERROR', message='IN : Destination-address is not matched : ' + in_destination_address )
            
            if protocol is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][0]['flow-information'][0]['protocol'] == protocol:
                    device.log(level='INFO', message='IN : protocol is matched : ' + protocol )
                else:
                    device.log(level='ERROR', message='IN : protocol is not matched : ' + protocol )

            if out_source_address is not None:
            
                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][0]['flow-information'][1]['source-address'] == out_source_address:
                    device.log(level='INFO', message='OUT : source-address is matched ' + out_source_address)
                else:
                    device.log(level='ERROR', message='OUT : source-address is not matched ' + out_source_address)

            if out_destination_address is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][0]['flow-information'][1]['destination-address'] == out_destination_address:
                    device.log(level='INFO', message='OUT : Destination-address is matched : ' + out_destination_address )
                else:
                    device.log(level='ERROR', message='OUT : Destination-address is not matched : ' + out_destination_address )
            if  in_destination_port is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][0]['flow-information'][0]['destination-port'] == in_destination_port:
                    device.log(level='INFO', message='IN : Destination-port is matched : ' + in_destination_port )
                else:
                    device.log(level='ERROR', message='IN : Destination-port is not matched : ' + in_destination_port )
            if  out_source_port is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][0]['flow-information'][1]['source-port'] == out_source_port:
                    device.log(level='INFO', message='OUT : source-port is matched : ' + out_source_port )
                else:
                    device.log(level='ERROR', message='OUT : source-port is not matched : ' + out_source_port )

            ###################
        session_status1 = status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][1]['session-state']
        if session_status1 == 'Active' or session_status1 == 'Backup' :

            device.log("Second Session state " + session_status1)
            if in_source_address is not None:
            
                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][1]['flow-information'][0]['source-address'] == in_source_address:
                    device.log(level='INFO', message='IN : source-address is matched ' + in_source_address)
                else:
                    device.log(level='ERROR', message='IN : source-address is not matched ' + in_source_address)

            if in_destination_address is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][1]['flow-information'][0]['destination-address'] == in_destination_address:
                    device.log(level='INFO', message='IN : Destination-address is matched : ' + in_destination_address )
                else:
                    device.log(level='ERROR', message='IN : Destination-address is not matched : ' + in_destination_address )
            
            if protocol is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][1]['flow-information'][0]['protocol'] == protocol:
                    device.log(level='INFO', message='IN : protocol is matched : ' + protocol )
                else:
                    device.log(level='ERROR', message='IN : protocol is not matched : ' + protocol )

            if out_source_address is not None:
            
                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][1]['flow-information'][1]['source-address'] == out_source_address:
                    device.log(level='INFO', message='OUT : source-address is matched ' + out_source_address)
                else:
                    device.log(level='ERROR', message='OUT : source-address is not matched ' + out_source_address)

            if out_destination_address is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][1]['flow-information'][1]['destination-address'] == out_destination_address:
                    device.log(level='INFO', message='OUT : Destination-address is matched : ' + out_destination_address )
                else:
                    device.log(level='ERROR', message='OUT : Destination-address is not matched : ' + out_destination_address )
            
            if protocol is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][1]['flow-information'][1]['protocol'] == protocol:
                    device.log(level='INFO', message='OUT : protocol is matched : ' + protocol )
                else:
                    device.log(level='ERROR', message='OUT : protocol is not matched : ' + protocol )
            
            if protocol is not None:

                if status['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-session-information']['flow-session'][1]['flow-information'][1]['protocol'] == protocol:
                    device.log(level='INFO', message='OUT : protocol is matched : ' + protocol )
                else:
                    device.log(level='ERROR', message='OUT : protocol is not matched : ' + protocol )
        else:
            device.log(level='ERROR', message='Session is not active on ' + node)
            raise Exception("value not present")


def get_node_status_from_rg(device=None, rg=None, rg_status=None):

    if device is None:
        raise Exception("'device' is mandatory parameter - device handle")
    if rg is None:
        device.log(level="ERROR", message="'rg' is mandatory parameter ")
        raise Exception("'rg' is mandatory parameter ")
    if rg_status is None:
        device.log(level="ERROR", message="'rg_status' is mandatory parameter ")
        raise Exception("'rg_status' is mandatory parameter ")


    if device is not None and rg is not None:
        result = device.cli(command="show chassis cluster status redundancy-group " + rg , format='xml').response()
        status = jxmlease.parse(result)
        device.log(status)
        if status['rpc-reply']['chassis-cluster-status']['redundancy-group']['device-stats']['redundancy-group-status'][0] == rg_status:
            node = status['rpc-reply']['chassis-cluster-status']['redundancy-group']['device-stats']['device-name'][0]
            if node == 'node0':
                node = 'node 0'
            else:
                node = 'node 1'
            return node
        
        elif status['rpc-reply']['chassis-cluster-status']['redundancy-group']['device-stats']['redundancy-group-status'][1] == rg_status:
            node = status['rpc-reply']['chassis-cluster-status']['redundancy-group']['device-stats']['device-name'][1]
            if node == 'node0':
                node = 'node 0'
            else:
                node = 'node 1'
            return node        
        else:
            return False