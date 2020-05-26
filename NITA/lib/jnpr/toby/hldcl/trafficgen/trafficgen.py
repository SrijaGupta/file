"""
Library for generic Traffic Generator functionality
"""

from jnpr.toby.hldcl.host import Host

class TrafficGen(Host):
    """
    Class for TrafficGen
    """
    def __init__(self, **kwargs):
        super(TrafficGen, self).__init__(**kwargs)

def execute_tester_command(device, command, **kwargs):
    return device.invoke(command, **kwargs)

def connect_tester(device1, **kwargs):
    return device1.connect(**kwargs)

def get_port_handle(device, intf):
    return device.get_port_handle(intf=intf)

