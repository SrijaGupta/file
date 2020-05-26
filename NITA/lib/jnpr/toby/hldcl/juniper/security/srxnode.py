"""
Class for SrxNode Devices
"""
import jxmlease
from jnpr.toby.hldcl.juniper.junipernode import JuniperNode
from jnpr.toby.exception.toby_exception import TobyException
from lxml import etree
import re

class SrxNode(JuniperNode):
    """
    Class Node to create JunOS srx node objects.
    """
    def __init__(self, *args, **kwargs):
        """

        Base class for JunOS devices

        :param nodedict:
            **REQUIRED** nodedict of node
        :return: node object based os and model
        """
        super(SrxNode, self).__init__(*args, **kwargs)

    def node_name(self):
        """
        Get name of the chassis in the cluster

        :return: name of the chassis in the cluster ("node0"/"node1").
        """
        # Execute show version on the connected device
        sccs = self.current_controller.cli( command="show version", format="xml").response()
        match = re.match(r"(<rpc-reply.*>)([\s\S]*)(<cli>[\s\S]*</rpc-reply>)", sccs)
        sccs = match.group(2) # will only get the XML response of the command
        # Get RG stats
        try:
            root = etree.fromstring(sccs)
            status = jxmlease.parse_etree(root)
            host_name = self.current_controller.shell(command='hostname').response()
            node0_name = status['multi-routing-engine-results'][
                'multi-routing-engine-item'][0]['software-information']['host-name']
            node1_name = status['multi-routing-engine-results'][
                'multi-routing-engine-item'][1]['software-information']['host-name']
            if str(node0_name).lower() == str(host_name).lower():
                return "node0"
            elif str(node1_name).lower() == str(host_name).lower():
                return "node1"
        except:
            self.current_controller.log(level='ERROR', message='Chassis cluster is not enabled')
            raise TobyException("Chassis cluster is not enabled")

    def is_node_master(self):
        """
        :return: return true if the current re is master else false
        """
        return True

    def is_node_status_primary(self):
        """
        Module to check if node status is primary
        :return: return true if the current node is primary else false
        """
        sccs = self.current_controller.cli(
            command="show chassis cluster status redundancy-group 0",
            format="xml").response()
        match = re.match(r"(<rpc-reply.*>)([\s\S]*)(<cli>[\s\S]*</rpc-reply>)", sccs)
        sccs = match.group(2) # will only get the XML response of the command
        try:
            root = etree.fromstring(sccs)
            status = jxmlease.parse_etree(root)
            status = status['chassis-cluster-status']['redundancy-group']['device-stats']
        except:
            raise TobyException('Chassis cluster is not enabled')
        node = self.node_name()
        if node == 'node0' and status['redundancy-group-status'][0] == 'primary':
            return True
        elif node == 'node1' and status['redundancy-group-status'][1] == 'primary':
            return True
        return False

