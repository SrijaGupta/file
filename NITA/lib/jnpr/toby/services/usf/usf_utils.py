"""THIS MODULE CONTAINS USF UTILS """
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.utils.junos.dut_tool import dut_tool

def ensure_usf_mode(device_handle):
    """ Enable USF mode and reboot devices in parallel. Skips rebooting if usf mode is already enabled.
        :param device_handle list device_handle:
            **MANDATORY**  pass single or list of device handles
        :return: True if enabling usf mode is successfull
        :rtype: bool

        Example::
            Python:
                ensure_usf_mode(r0) # r0 is device handle
                ensure_usf_mode([r0, r1]) # r0, r1 are device handles

            Robot:
                ${r0} =  Get Handle   resource=device0    controller=re0
                ${r1} =  Get Handle   resource=device0    controller=re1
                @{device_list} =  Create List    ${r0}   ${r1}
                Ensure Usf Mode    device_handle=${device_list}
    """
    if isinstance(device_handle, (list, tuple)):
        dev_list = device_handle
    else:
        dev_list = (device_handle, )
    xpath = 'unified-services-status-information/unified-services-status'
    reboot_list = []
    for dev in dev_list:
        output = dev.cli(command='show system unified-services status', timeout=120, format='xml').response()
        xml_handle = xml_tool()
        xml_tree = xml_handle.xml_string_to_dict(xml_str=output)
        xml_tree = xml_tree['rpc-reply']
        for path in xpath.split('/'):
            xml_tree = xml_tree[path]
        if xml_tree != 'Unified Services : Enabled':
            dev.config(command_list=['load override /var/tmp/baseline-config.conf']).status()
            dev.commit()
            dev.cli(command='request system enable unified-services', pattern='.*').response()
            dev.cli(command='yes').response()
            reboot_list.append(dev)
        else:
            print("USF Mode is Enabled Already....So Skipping .....!!")
    if reboot_list:
        reboot_router = dut_tool()
        reboot_router.reboot(device=reboot_list, wait=30, timeout=480, mode='cli', check_interval=30, on_parallel=True)
        for dev1 in dev_list:
            status = dev1.cli(command='show system unified-services status', timeout=120, format='xml').response()
            xml_new = xml_handle.xml_string_to_dict(xml_str=status)
            xml_new = xml_new['rpc-reply']
            for new_path in xpath.split('/'):
                xml_new = xml_new[new_path]
            if xml_new == 'Unified Services : Enabled':
                print("USF Mode is enabled !!")
            else:
                raise TobyException('USF is still not enabled')
    return True
