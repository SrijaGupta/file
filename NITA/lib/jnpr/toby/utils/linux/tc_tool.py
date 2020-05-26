"""
tc tool related keywords
ref: http://lartc.org/manpages/tc.txt
     https://wiki.linuxfoundation.org/networking/netem
"""
__author__ = ['Indrakumar M']
__contact__ = ''
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2018'

import re

def configure_qdisc_netem(device=None, **kwargs):
    """

        :param device:
            **REQUIRED** linux handle object

        :param intf:
            **REQUIRED**  ethernet interface

        :param action:
            **OPTIONAL**  action to be performed. Default:

            Supported values : add/change/delete

        :param parent_qdisc_id:
            **OPTIONAL**  parent id

        :param qdisc_kind:
            **OPTIONAL** classless qdiscs.  Default: netem

        :param netem:
            **OPTIONAL** used only if action==delete
	    Default:0  if action==delete
            Supported values 0/1

        :param delay:
            **OPTIONAL** delay to be added

            eg values:

            100ms

            100ms 10ms     (Single space between values)

            100ms 10ms 25%

        :param distribution:
            **OPTIONAL**  Delay distribution

        :param loss:
            **OPTIONAL**  Packet loss percentage

        :param duplicate:
            **OPTIONAL**  Packet duplication percentage

        :param corrupt:
            **OPTIONAL**  Packet corruption in percentage

        :param reorder:
            **OPTIONAL** Packet re-ordering

        :return:  True on success
                  Exception on Failure

        EXAMPLE::

            for adding:

            Python:
            configure_qdisc_netem(device=<linux handle>, intf='eth0', delay='100ms')

            Robot:
            configure qdisc netem device=${linux_handle}  intf=eth0  delay=100ms

            For change:

            Python:
            configure_qdisc_netem(device=<linux handle>, action='change',
            intf='eth0', delay='100ms 10ms')

            Robot:
            configure qdisc netem  device=${linux_handle}  action=change
            ...    intf=eth0  delay=100ms 10ms

    """
    if device is None:
        raise ValueError("device is mandatory argument")
    if 'intf' not  in kwargs:
        raise ValueError("intf is mandatory argument")

    intf = kwargs.get('intf')
    action = kwargs.get('action', 'add')
    qdisc_cmd = 'tc qdisc ' + action + ' dev ' + intf
    if action != 'ls':
        netem = 1
        if action == 'delete':
            netem = int(kwargs.get('netem', 0))

        if 'parent_qdisc_id' in kwargs:
            qdisc_cmd = qdisc_cmd + ' parent ' + kwargs.get('parent_qdisc_id')
        else:
            qdisc_cmd = qdisc_cmd + ' root '

        if 'handle_qdisc_id' in kwargs:
            qdisc_cmd = qdisc_cmd + ' handle ' + kwargs.get('handle_qdisc_id')

        # QDISC_KIND := { [p|b]fifo | tbf | prio | cbq | red | etc. }
        if 'qdisc_kind' in kwargs:
            qdisc_cmd = qdisc_cmd + kwargs.get('qdisc_kind')
            if 'limit' in kwargs:
                qdisc_cmd = qdisc_cmd + ' limit ' + kwargs.get('limit')

        if netem == 1:
            qdisc_cmd = qdisc_cmd + ' netem '

        if 'delay' in kwargs:
            qdisc_cmd = qdisc_cmd + ' delay ' + kwargs.get('delay')

        if 'distribution' in kwargs:
            qdisc_cmd = qdisc_cmd + ' distribution ' + kwargs.get('distribution')

        if 'loss' in kwargs:
            qdisc_cmd = qdisc_cmd + ' loss ' + kwargs.get('loss')

        if 'duplicate' in kwargs:
            qdisc_cmd = qdisc_cmd + ' duplicate ' + kwargs.get('duplicate')

        if 'corrupt' in kwargs:
            qdisc_cmd = qdisc_cmd + ' corrupt ' + kwargs.get('corrupt')

        if 'reorder' in kwargs:
            qdisc_cmd = qdisc_cmd + ' reorder ' + kwargs.get('reorder')

    device.log("Running: " + qdisc_cmd)
    print("Running " + qdisc_cmd)
    result = device.shell(command=qdisc_cmd).response()

    if re.search(r'Illegal|not complete|Try option|File exists|not permitted', result):
        device.log(level='ERROR', message=result)
        raise  Exception('Running qdisc command failed')

    return  result
