import jxmlease
import re


def interface_port(device=None):
       
    """
    Verification keyword for sum of available ports and twins ports in nat

    Examples:
    python - interface_port(device=None) 
                                                
    robot - Interface Port   device=${r0}    


    :param Device device:
    
    """
    if device is None:
       raise Exception("'device' is mandatory parameter - device handle")


    #XML verification for all parameters in nat interfcae port
    result = device.cli(command='show security nat interface-nat-ports', format='xml').response()
    status = jxmlease.parse(result)
    device.log(status)

 
    #For index 0
    print("For index 0")
    total_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][0]['total-ports'])
    device.log(level='INFO', message="Total ports : %s" %total_port)

    single_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][0]['single-ports-available'])
    device.log(level='INFO', message="Single port available : %s" %single_port)

    twin_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][0]['twin-ports-available'])
    device.log(level='INFO', message="Twin port avalable : %s" %twin_port)

    sum=int(single_port)+int(twin_port)
    device.log(level='INFO', message="Sum of single and twin ports : %s" %sum)

    if int(total_port) == int(sum):
       device.log(level='INFO', message='Toatl port count is equal to sum of single and twin ports')
    else:
       device.log(level='ERROR', message='Toatl port count is NOT equal to sum of single and twin ports')
       raise Exception("value not equal")

    #For index 1
    print("For index 1")
    total_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][1]['total-ports'])
    device.log(level='INFO', message="Total ports : %s" %total_port)

    single_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][1]['single-ports-available'])
    device.log(level='INFO', message="Single port available : %s" %single_port)

    twin_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][1]['twin-ports-available'])
    device.log(level='INFO', message="Twin port avalable : %s" %twin_port)

    sum=int(single_port)+int(twin_port)
    device.log(level='INFO', message="Sum of single and twin ports : %s" %sum)

    if int(total_port) == int(sum):
       device.log(level='INFO', message='Toatl port count is equal to sum of single and twin ports')
    else:
       device.log(level='ERROR', message='Toatl port count is NOT equal to sum of single and twin ports')
       raise Exception("value not equal")

    #For index 2
    print("For index 2")
    total_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][2]['total-ports'])
    device.log(level='INFO', message="Total ports : %s" %total_port)

    single_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][2]['single-ports-available'])
    device.log(level='INFO', message="Single port available : %s" %single_port)

    twin_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][2]['twin-ports-available'])
    device.log(level='INFO', message="Twin port avalable : %s" %twin_port)

    sum=int(single_port)+int(twin_port)
    device.log(level='INFO', message="Sum of single and twin ports : %s" %sum)

    if int(total_port) == int(sum):
       device.log(level='INFO', message='Toatl port count is equal to sum of single and twin ports')
    else:
       device.log(level='ERROR', message='Toatl port count is NOT equal to sum of single and twin ports')
       raise Exception("value not equal")


    #For index 3
    print("For index 3")
    total_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][3]['total-ports'])
    device.log(level='INFO', message="Total ports : %s" %total_port)

    single_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][3]['single-ports-available'])
    device.log(level='INFO', message="Single port available : %s" %single_port)

    twin_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][3]['twin-ports-available'])
    device.log(level='INFO', message="Twin port avalable : %s" %twin_port)

    sum=int(single_port)+int(twin_port)
    device.log(level='INFO', message="Sum of single and twin ports : %s" %sum)

    if int(total_port) == int(sum):
       device.log(level='INFO', message='Toatl port count is equal to sum of single and twin ports')
    else:
       device.log(level='ERROR', message='Toatl port count is NOT equal to sum of single and twin ports')
       raise Exception("value not equal")

    #For index 4
    print("For index 4")
    total_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][4]['total-ports'])
    device.log(level='INFO', message="Total ports : %s" %total_port)

    single_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][4]['single-ports-available'])
    device.log(level='INFO', message="Single port available : %s" %single_port)

    twin_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][4]['twin-ports-available'])
    device.log(level='INFO', message="Twin port avalable : %s" %twin_port)

    sum=int(single_port)+int(twin_port)
    device.log(level='INFO', message="Sum of single and twin ports : %s" %sum)

    if int(total_port) == int(sum):
       device.log(level='INFO', message='Toatl port count is equal to sum of single and twin ports')
    else:
       device.log(level='ERROR', message='Toatl port count is NOT equal to sum of single and twin ports')
       raise Exception("value not equal")

    #For index 5
    print("For index 5")
    total_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][5]['total-ports'])
    device.log(level='INFO', message="Total ports : %s" %total_port)

    single_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][5]['single-ports-available'])
    device.log(level='INFO', message="Single port available : %s" %single_port)

    twin_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][5]['twin-ports-available'])
    device.log(level='INFO', message="Twin port avalable : %s" %twin_port)

    sum=int(single_port)+int(twin_port)
    device.log(level='INFO', message="Sum of single and twin ports : %s" %sum)

    if int(total_port) == int(sum):
       device.log(level='INFO', message='Toatl port count is equal to sum of single and twin ports')
    else:
       device.log(level='ERROR', message='Toatl port count is NOT equal to sum of single and twin ports')
       raise Exception("value not equal")

    #For index 6
    print("For index 6")
    total_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][6]['total-ports'])
    device.log(level='INFO', message="Total ports : %s" %total_port)

    single_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][6]['single-ports-available'])
    device.log(level='INFO', message="Single port available : %s" %single_port)

    twin_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][6]['twin-ports-available'])
    device.log(level='INFO', message="Twin port avalable : %s" %twin_port)

    sum=int(single_port)+int(twin_port)
    device.log(level='INFO', message="Sum of single and twin ports : %s" %sum)

    if int(total_port) == int(sum):
       device.log(level='INFO', message='Toatl port count is equal to sum of single and twin ports')
    else:
       device.log(level='ERROR', message='Toatl port count is NOT equal to sum of single and twin ports')
       raise Exception("value not equal")

    #For index 7
    print("For index 7")
    total_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][7]['total-ports'])
    device.log(level='INFO', message="Total ports : %s" %total_port)

    single_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][7]['single-ports-available'])
    device.log(level='INFO', message="Single port available : %s" %single_port)

    twin_port = (status['rpc-reply']['interface-nat-ports-information']['interface-nat-ports-entry'][7]['twin-ports-available'])
    device.log(level='INFO', message="Twin port avalable : %s" %twin_port)

    sum=int(single_port)+int(twin_port)
    device.log(level='INFO', message="Sum of single and twin ports : %s" %sum)

    if int(total_port) == int(sum):
       device.log(level='INFO', message='Toatl port count is equal to sum of single and twin ports')
    else:
       device.log(level='ERROR', message='Toatl port count is NOT equal to sum of single and twin ports')
       raise Exception("value not equal")


def get_mac(device=None, interface=None):

    if device is None:
       raise Exception("'device' is mandatory parameter - device handle")
    if interface is None:
       raise Exception("'device' is mandatory parameter - device handle")

    name = 'show interface ' + interface + ' detail |match hardware'
    result = device.cli(command= name, format='xml').response()
#    result = device.cli(command='show interface ' + interface + ' detail', format='xml').response()
    status = jxmlease.parse(result)


    status = jxmlease.parse(result)
 #   device.log(status)
#    mac_address = (status['rpc-reply']['interface-information']['physical-interface']['current-physical-address'])
 #   device.log(level='INFO', message="Total ports : %s" %mac_address)



