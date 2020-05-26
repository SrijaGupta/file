
def bbevar_get_device():
    return bbe.get_devices(tags=['dut'])

def bbevar_get_interface():
    return bbe.get_interfaces('r0', interface='access')

def bbevar_get_vrf():
    return list(bbe.get_vrfs('r1'))

def bbevar_get_rt_handle():
    rth = bbe.get_rt_handle()
    if rth is None:
        return "RT handle not available"
    else:
        return "RT handle is there"

