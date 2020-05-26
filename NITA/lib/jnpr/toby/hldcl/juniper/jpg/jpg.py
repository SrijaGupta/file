'''
    Created on Sep 26, 2016
    @author: Terralogic Team
'''
import os
import re
import traceback
import time
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.exception.toby_exception import TobyException


class Jpg(Juniper):
    '''
    Generic JPG class for Juniper Packet Generator
    '''

    def __init__(self, *args, **kwargs):
        '''
        Base class for Juniper Packet Generator Package
        :param host:
            **REQUIRED** host-name or IP address of target device
        :param os:
            *OPTIONAL* Operating System of device. Default is JUNOS
        :param user:
            *OPTIONAL* Login user name. If not provided will be derived from
            Toby framework defaults.
        :param password:
            *OPTIONAL* Login Password. If not provided will be derived from
            Toby framework defaults.
        :param model:
             *OPTIONAL* Model of device. Default is None.
        :param dual_re:
            *OPTIONAL* Connect to both the RE's. Default is False. Will return
            object which is connected to master RE.
        :param routing_engine:
            *OPTIONAL*  Connect to routing engine specified.
            Supported values are master/backup.
            Cannot be used with dual_re.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            values are telnet/ssh/netconf/console
        :param console:
            *OPTIONAL* Flag to identify console login. Default is False.
        :param port:
            *OPTIONAL* Port on device to which connection needs to made.
        :param tag:
            *OPTIONAL* Tag to uniquely idetify the device object
        :return: Device object based on os and model
        '''
        # Initalize the jpg device using the Juniper super class
        super(Jpg, self).__init__(**kwargs)

        # Initalize the log
        self.interfaces = {}
        self.inout_intf_rep_pair = []
        self.inout_intf_pair = []
        self.user_filter = []
        self.jpg_config = []
        self.term_array = []
        self.config_arr = []
        self.cmd = dict(
            set_fw_by_vlan="set firewall family" +
            " bridge filter %s term %s from learn-vlan-id %s",
            set_fw_by_vlan_prio="set firewall family bridge" +
            " filter %s term %s from learn-vlan-1p-priority %s",
            set_fw_by_accept_count="set firewall family bridge filter %s " +
            "term %s then accept count %s",
            set_fw_then_count="set firewall family bridge filter %s " +
            "term %s then count %s",
            set_fw_then_accept="set firewall family bridge filter " +
            "%s term %s then accept",
            set_fw_then_fwd="set firewall family bridge filter " +
            "%s term %s then forwarding-class %s",
            set_fw_by_source_port="set firewall family bridge " +
            "filter %s term %s from source-port %s",
            set_fw_by_dest_port="set firewall family bridge" +
            " filter %s term %s from destination-port %s",
            set_fw_from_source_ip="set firewall family bridge" +
            " filter %s term %s from ip-source-address %s",
            set_fw_from_dest_mac="set firewall family bridge" +
            " filter %s term %s from destination-mac-address %s",
            set_fw_from_source_mac="set firewall family bridge" +
            " filter %s term %s from source-mac-address %s",
            set_fw_from_dest_ip="set firewall family bridge" +
            " filter %s term %s from ip-destination-address %s",
            set_fw_from_ip__precedence="set firewall family bridge" +
            " filter %s term %s from ip-precedence %s",
            set_fw_by_eth_type="set firewall family bridge " +
            "filter %s term %s from ether-type %s",
            del_fw_tern_default="delete firewall family bridge filter %s " +
            "term default",
            show_bridge_flood="show bridge flood bridge-domain %s",
            show_chassis_fpc_pic_stt="show chassis fpc pic-status",
            show_interfaces="show interfaces %s",
            show_chassis_fpc="show chassis fpc",
            show_intf_diag_optics="show interfaces diagnostics " +
            "optics %s",
            show_forward_port_mirroring="show configuration " +
            "forwarding-options port-mirroring",
            set_chassis_fpc_instance="set chassis fpc %s " +
            "port-mirror-instance %s",
            set_mirror_rate="set forwarding-options " +
            "port-mirroring input rate %s",
            set_mirror_instance_rate="set forwarding-options " +
            "port-mirroring instance %s input rate %s",
            set_mirror_inst_output="set forwarding-options " +
            "port-mirroring instance %s family vpls output no-filter-check",
            set_mirror_instance_param="set forwarding-options " +
            "port-mirroring instance %s input-parameters-instance %s",
            set_mirror_instance_intf="set forwarding-options " +
            "port-mirroring instance %s family vpls output interface %s",
            set_class_of_service="set class-of-service forwarding-classes " +
            "class %s queue-num %s",
            set_COS_interface="set class-of-service interfaces %s " +
            "scheduler-map-chassis control-schedular",
            set_COS_scheduler="set class-of-service scheduler-maps " +
            "control-schedular forwarding-class %s scheduler control-sch",
            set_COS_priority="set class-of-service schedulers " +
            "control-sch priority strict-high",
            set_intf_filter_in="set interfaces %s unit 0 family " +
            "bridge filter input %s",
            set_interface_mtu="set interfaces %s mtu %s",
            set_interface_filter_out="set interfaces %s unit 0 family " +
            "bridge filter output %s",
            set_fw_discard="set firewall family bridge filter %s " +
            "term %s then discard",
            set_fw_port_mirror_instance="set firewall family bridge filter " +
            "%s term %s then port-mirror-instance %s",
            set_fw_ip_protocol="set firewall family bridge filter %s term " +
            "%s from ip-protocol %s",
            set_fw_icmp_type="set firewall family bridge filter %s term " +
            "%s from icmp-type %s",
            set_int_encap="set interfaces %s encapsulation ethernet-bridge",
            set_int_bridge="set interfaces %s unit 0 family bridge",
            set_domain_int="set bridge-domains %s interface %s",
            set_domain_option="set bridge-domains %s bridge-options " +
            "no-mac-learning",
            set_fw_port="set firewall family bridge filter %s term " +
            "%s from port %s",
            show_brdg_flood_brdg_domain="show bridge flood " +
            "bridge-domain %s",
            show_version="show version",
            cprod_a_show_nhdb_id="cprod -A %s -c show nhdb id %s rec",
            cprod_a_show_nhdb_id_grep="cprod -A %s -c show nhdb id %s " +
            "rec | grep %s",
            show_intf_grep_speed="show interfaces %s| grep speed",
            show_bridge_domain="show configuration bridge-domains",
            del_chas_fpc="delete chassis fpc %s",
            del_int="delete interfaces %s",
            del_fwd_inst="delete forwarding-options port-mirroring " +
            "instance %s",
            del_COS_int="delete class-of-service interfaces %s",
            del_fw_filter="delete firewall family bridge filter %s",
            del_br_domain="delete bridge-domains %s",
            sysctl_random_port="sysctl net.inet.ip.portrange.randomized",
            set_root_pwd="set system root-authentication plain-text-password",
            set_pwd="Embe1mpls",
            show_intf_terse="show interface %s terse",
            set_intf_gige_opt="set interfaces %s gigether-options loopback",
            cprod_show_nhdb="cprod -A %s -c show nhdb id %s rec",
            del_intf_gige="delete interfaces %s gigether-options loopback",
            nhchange_composite="route\.new nhchange %s composite %s %s " +
            "compose-as split-horizon",
            set_intf_disable="set interfaces %s disable",
            del_intf_disable="delete interfaces %s disable"
            )

    def configure_jpg(self):
        '''
        This funaction will do the configuration of the jpg

        DESCRIPTION:
            This function will do the following:
                - retrieve the ingress and egress interfaces
                - Reset the Jpg Configuration
                - Configure the bridge configuration
                - Configure the jpg replication
        
        ARGUMENTS:
            []
            :param:None

        ROBOT USAGE:
            configure jpg

        :returns: True if the configuration succeeds
        '''
        self.su(password=self.cmd['set_pwd'])
        self.__get_ingress_egress_interfaces()
        self.log(message="inout_intf_pair : %s" % self.inout_intf_pair,
                 level='info')
        self.log(message="inout_intf_rep_pair : %s" % self.inout_intf_rep_pair,
                 level='info')
        if len(self.inout_intf_pair) != 0 and\
                len(self.inout_intf_rep_pair) != 0:
            self.__reset_jpg_config()
            self.__configure_jpg_bridge()
            self.__configure_jpg_replication()
        os.environ['JPG'] = 'JPG'
        return True

    def __get_ingress_egress_interfaces(self):
        '''
        Get a list of all pairs of ingress and egress interface that have
        a same bridge name
        :returns: a list of ingress and egress interface pairs
            e.g ["r0-1-1|r1-1-1","r2-1-2|r3-2-3"]
        '''
        scanarr = []

        intfs = self.interfaces

        for intf in intfs.keys():

            if intf != "" and intf not in scanarr:
                flag = 0
                for key in intfs.keys():
                    if intfs[intf] and intfs[key] and\
                            intfs[intf] != intfs[key]:
                        if 'jpg-bridge-name' in intfs[intf].keys() and\
                                intfs[intf]['jpg-bridge-name'] and\
                                'jpg-bridge-name' in intfs[key].keys() and\
                                intfs[key]['jpg-bridge-name'] and\
                                'pic'in intfs[intf].keys() and\
                                intfs[intf]['pic'] and\
                                'pic' in intfs[key].keys() and\
                                intfs[key]['pic']:

                            bridge1 = intfs[intf][
                                'jpg-bridge-name'].strip().rstrip()
                            bridge2 = intfs[key][
                                'jpg-bridge-name'].strip().rstrip()

                            if bridge1 == bridge2:
                                flag = 1
                                intf_pic = intfs[intf]['pic']
                                key_pic = intfs[key]['pic']

                                if 'jpg-replication-factor' in intfs[intf].keys() and intfs[intf]['jpg-replication-factor']:

                                    reppair = intf_pic + "," + str(intfs[intf]['jpg-replication-factor']) + \
                                        "|" + key_pic + "," + ''
                                    pair = intf_pic + "|" + key_pic

                                elif 'jpg-replication-factor' in intfs[key].keys() and intfs[key]['jpg-replication-factor']:

                                    reppair = key_pic + "," + str(intfs[key]['jpg-replication-factor']) + \
                                        "|" + intf_pic + "," + ''
                                    pair = key_pic + "|" + intf_pic

                                else:
                                    err_hdl_msg = "jpg-replication-factor is a mandatory knob that" + \
                                        " should be present in the ingress interface bundle of JPG. " + \
                                        "Since jpg-replication-factor is not present. Aborted the " + \
                                        "script. Please modify .yaml file with jpg-replication-" + \
                                        "factor in ingress interface"
                                    raise TobyException(err_hdl_msg, host_obj=self)
                                scanarr.append(intf)
                                scanarr.append(key)
                                if reppair not in self.inout_intf_rep_pair:
                                    self.inout_intf_rep_pair.append(reppair)
                                if pair not in self.inout_intf_pair:
                                    self.inout_intf_pair.append(pair)
                        else:
                            msg = "Either jpg-bridge-name or pic is not present under Interfaces bundle " + \
                                  "of JPG device and hence aborting the script"
                            self.log(message=msg, level='error')
                            raise TobyException(msg, host_obj=self)

                if flag == 0:
                    msg = "BRIDGE NAME did not match for %s for bridge-name %s and hence aborting the script " + \
                        "as can't configure JPG. Please Add the same bridge name in one more interface bundle under JPG"
                    self.log(message=msg % (intf, intfs[intf]['jpg-bridge-name']), level='error')
                    raise TobyException(msg % (intf, intfs[intf]['jpg-bridge-name']), host_obj=self)
        self.log(message="Ingress_Egress_Pair = %s" % self.inout_intf_pair, level='info')
        self.log(message="Ingress_Egress_Replication_Pair = %s "
                 % self.inout_intf_rep_pair, level='info')
        return True

    def __reset_jpg_config(self):
        '''
            Reset/cleanup the old configuration on JPG device based on
            the pair of ingress and egress interfaces
            :param None:
            :returns: True
        '''
        intf_pair = self.inout_intf_pair

        delete_bd_arr = []
        cmds = []
        for intf in intf_pair:
            (ingress_intf, egress_intf) = intf.split('|')
            self.log(message="Ingress Port: %s , Egress Port: %s"
                     % (ingress_intf, egress_intf), level='info')

            fpcnum = re.match(r'.*?-(\d+)\/', ingress_intf).group(1)
            self.log(message="FPC number: %s" % fpcnum, level='info')

            in_ = ingress_intf.replace("-", "").replace("/", "_")
            out_ = egress_intf.replace("-", "").replace("/", "_")

            filter_ingress = "filter_ingress_" + in_
            filter_egress_input = "filter_egress_in_" + out_
            filter_egress_output = "filter_egress_out_" + out_

            bd_name = "bd_" + in_ + "_" + out_
            pm_name = "pm_" + in_ + "_" + out_

            self.log(message="BridgeDomain_Name:  %s, PortMirror_Name: %s"
                     % (bd_name, pm_name), level='info')
            msg = "Filter_IN = %s, Filter_OUT_EGR = %s, Filter_IN_EGR = \
            %s\n\n" % (filter_ingress, filter_egress_output,
                       filter_egress_input)
            self.log(message=msg, level='info')

            egress_with_star = re.match(r"(.*\/)\d+", egress_intf).group(1) + "*"

            self.shell(command=self.cmd['sysctl_random_port'])

            self.config(command_list=[self.cmd['set_root_pwd']], pattern='New password:')
            self.config(command_list=[self.cmd['set_pwd']], pattern='Retype new password:')
            self.config(command_list=[self.cmd['set_pwd']])

            show = self.cmd['show_bridge_domain'] + " | display set | grep interface | grep " + ingress_intf
            output = self.cli(command=show)
            result = output.response()
            for line in result.split("\n"):
                bd_arr = re.match(r"set bridge-domains (.*) interface %s(.*)"
                                  % ingress_intf, line)
                if bd_arr and bd_arr.group(1) not in delete_bd_arr:
                    delete_bd_arr.append(bd_arr.group(1))

            show = self.cmd['show_bridge_domain'] + \
                " | display set | grep interface | grep " + egress_intf
            output = self.cli(command=show)
            res = output.response()
            for line in res.split("\n"):
                bd_arr = re.match(r"set bridge-domains (.*) interface %s(.*)"
                                  % egress_intf, line)
                if bd_arr and bd_arr.group(1) not in delete_bd_arr:
                    delete_bd_arr.append(bd_arr.group(1))

            cmds = cmds + [self.cmd['del_chas_fpc'] % fpcnum,
                           self.cmd['del_int'] % ingress_intf,
                           self.cmd['del_int'] % egress_intf,
                           self.cmd['del_fwd_inst'] % pm_name,
                           self.cmd['del_COS_int'] % egress_with_star,
                           self.cmd['del_fw_filter'] % filter_ingress,
                           self.cmd['del_fw_filter'] % filter_egress_input,
                           self.cmd['del_fw_filter'] % filter_egress_output]
            cmds.append(self.cmd['del_br_domain'] % bd_name)

        show = "show bridge-domains | display set | grep bd_ |display xml"
        output = self.config(command_list=[show])
        res = output.response().split("\n")
        bd_name_list = []
        for line in res:
            check = re.match(r'<name>(.*)<\/name>', line)
            if check:
                bd_name_list.append(check.group(1))
        for bd_name_temp in bd_name_list:
            show = "show bridge-domains |display set | no-more | " +\
                "grep %s | match interface | count" % bd_name_temp
            output = self.config(command_list=[show])
            res = output.response().split("\n")
            lines1 = 0
            for line in res:
                check = re.match(r"Count: (.*) lines", line)
                if check:
                    lines1 = check.group(1)
            if int(lines1) > 2:
                self.log(
                    message="Need to delete %s as something went wrong in "
                    % bd_name_temp + "previous script", level='info')
                delete_bd_arr.append(bd_name_temp)

        # Adding code to delete bridge-domain if there is a
        # stray entry in configuration
        self.log(message="delete_bd_arr === %s" % delete_bd_arr,
                 level='info')
        for bd_name in delete_bd_arr:
            show = self.cmd['show_bridge_domain']\
                + " %s| display set | grep interface" % bd_name
            res = self.cli(command=show)
            bd_int1 = 0
            bd_int2 = 0
            bd_config = res.response().split("\n")
            if re.search("\w+", res.response()):
                for line in bd_config:
                    if not re.match(r'set.*', line):
                        bd_config.remove(line)
                bd_int1 = bd_config[0].split(" ")
                bd_int1 = bd_int1[-1].split(".")
                bd_int2 = bd_config[1].split(" ")
                bd_int2 = bd_int2[-1].split(".")
            if bd_int1 != 0:
                cmds.append("delete interfaces %s" % bd_int1[0])
            if bd_int2 != 0:
                cmds.append("delete interfaces %s" % bd_int2[0])
            cmds.append("delete bridge-domains %s" % bd_name)

        self.config(command_list=cmds)

        result = False
        try:
            result = self.commit().response()
        except Exception as err:
            self.log(message=err, level='Error')
            return result
        return True

    def __configure_jpg_bridge(self):
        '''
        Config ingress and express interface include forwarding-options
        port-mirroring, class of service,firewall family
        bridge filter policy,encapsulation and bridge-domains.
        :param: none
        :definition:
            ingress_intf: get the information of "ingress" interface.
            egress_intf: get the information of "exgress" interface.
            filter_ingress:the filter "ingress" which interface on the "in" way
            filter_egress_input: the filter "ingress' which interface on
            the "out" way
            filter_egress_output: the filter "exgress' which interface on
            the "out" way
            bd_name:bridge domain name (ex:bd_ge2/2/1_xe1/3/2)
            pm_name:port mirror name (ex:pm_ge2/2/1_xe1/3/2)
            ingress_with_unit:the ingress interface with unit like ge-2/2/2.100
            exgress_with_unit:the exgress interface with unit like ge-2/2/2.100
            egress_with_star: ex ge-2/2/2*
        :returns: True if commit already success without syntax error.
        False and put out the log if commit check got error.
        '''

        intf_pair = self.inout_intf_pair
        for intf in intf_pair:
            self.config_arr = []
            (ingress_intf, egress_intf) = intf.split('|')
            self.log(message="Ingress Port: %s , Egress Port: %s"
                     % (ingress_intf, egress_intf), level='info')

            fpcnum = re.match(r'.*?-(\d+)\/', ingress_intf).group(1)

            self.log(message="FPC number: %s" % fpcnum, level='info')

            fpcnum1 = re.match(r'.*?-(\d+)\/', egress_intf).group(1)
            self.log(message="FPC number1: %s" % fpcnum1, level='info')

            in_ = ingress_intf.replace("-", "").replace("/", "_")
            out_ = egress_intf.replace("-", "").replace("/", "_")

            filter_ingress = "filter_ingress_" + in_
            filter_egress_input = "filter_egress_in_" + out_
            filter_egress_output = "filter_egress_out_" + out_

            bd_name = "bd_" + in_ + "_" + out_
            pm_name = "pm_" + in_ + "_" + out_
            self.log(message="BridgeDomain_Name: %s , PortMirror_Name: %s"
                     % (bd_name, pm_name), level='info')

            egress_with_star = re.match(r"(.*\/)\d+",
                                        egress_intf).group(1) + "*"
            ingress_with_unit = ingress_intf + ".0"
            egress_with_unit = egress_intf + ".0"

            show = self.cli(command=self.cmd['show_forward_port_mirroring'])

            self.__config_build__(
                cmd=[self.cmd['set_chassis_fpc_instance'] % (fpcnum, 'pm1')])

            if re.search("\w+", show.response()):
                self.log(message="Port Mirror is configured will use for " +
                         "other Port Mirror instance\n", level='info')
            else:
                self.log(
                    message="No Bridge-Domain configured, hence configuring\n",
                    level='warn')
                self.__config_build__(
                    cmd=[self.cmd['set_chassis_fpc_instance'] % (fpcnum,
                                                                 'pm1'),
                         self.cmd['set_chassis_fpc_instance'] % (fpcnum1,
                                                                 'pm1'),
                         self.cmd['set_mirror_rate'] % '1',
                         self.cmd['set_mirror_instance_rate'] % ('pm1', '1'),
                         self.cmd['set_mirror_inst_output'] % 'pm1'])
            mtu = 9192
            self.__config_build__(
                cmd=[self.cmd['set_mirror_instance_param'] % (pm_name, 'pm1'),
                     self.cmd['set_mirror_instance_intf'] % (pm_name,
                                                             egress_with_unit),
                     self.cmd['set_mirror_inst_output'] % pm_name,
                     self.cmd['set_class_of_service'] % ('FC-Q0', '0'),
                     self.cmd['set_class_of_service'] % ('FC-Q1', '1'),
                     self.cmd['set_class_of_service'] % ('FC-Q3', '3'),
                     self.cmd['set_COS_interface'] % egress_with_star,
                     self.cmd['set_COS_scheduler'] % 'FC-Q3',
                     self.cmd['set_COS_priority'],
                     self.cmd['set_intf_filter_in'] % (ingress_intf,
                                                       filter_ingress),
                     self.cmd['set_interface_mtu'] % (ingress_intf, mtu),
                     self.cmd['set_interface_mtu'] % (egress_intf, mtu),
                     self.cmd['set_interface_filter_out'] % (
                         egress_intf, filter_egress_output),
                     self.cmd['set_intf_filter_in'] % (egress_intf,
                                                       filter_egress_input)])

            filter_name1 = filter_ingress
            term = "arp"
            self.__config_build__(
                cmd=[self.cmd['set_fw_by_eth_type'] % (filter_name1, term,
                                                       'arp'),
                     self.cmd['set_fw_then_count'] % (filter_name1, term,
                                                      term),
                     self.cmd['set_fw_then_fwd'] % (filter_name1, term,
                                                    'FC-Q3'),
                     self.cmd['set_fw_discard'] % (filter_name1, term),
                     self.cmd['set_fw_port_mirror_instance'] % (filter_name1,
                                                                term,
                                                                pm_name)])

            term = "ospf"
            self.__config_build__(
                cmd=[self.cmd['set_fw_ip_protocol'] % (filter_name1, term,
                                                       'ospf'),
                     self.cmd['set_fw_then_count'] % (filter_name1, term,
                                                      term),
                     self.cmd['set_fw_then_fwd'] % (filter_name1, term,
                                                    'FC-Q3'),
                     self.cmd['set_fw_discard'] % (filter_name1, term),
                     self.cmd['set_fw_port_mirror_instance'] % (filter_name1,
                                                                term,
                                                                pm_name)])

            term = "pim"
            self.__config_build__(
                cmd=[self.cmd['set_fw_ip_protocol'] % (filter_name1, term,
                                                       'pim'),
                     self.cmd['set_fw_then_count'] % (filter_name1, term,
                                                      term),
                     self.cmd['set_fw_then_fwd'] % (filter_name1, term,
                                                    'FC-Q3'),
                     self.cmd['set_fw_discard'] % (filter_name1, term),
                     self.cmd['set_fw_port_mirror_instance'] % (filter_name1,
                                                                term,
                                                                pm_name)])

            term = "bgp"
            self.__config_build__(cmd=[
                self.cmd['set_fw_port'] % (filter_name1, term, term),
                self.cmd['set_fw_then_count'] % (filter_name1, term, term),
                self.cmd['set_fw_then_fwd'] % (filter_name1, term, 'FC-Q3'),
                self.cmd['set_fw_discard'] % (filter_name1, term),
                self.cmd['set_fw_port_mirror_instance'] % (filter_name1,
                                                           term, pm_name)])

            term = "igmp"
            self.__config_build__(
                cmd=[self.cmd['set_fw_ip_protocol'] % (filter_name1, term,
                                                       'igmp'),
                     self.cmd['set_fw_then_count'] % (filter_name1, term,
                                                      term),
                     self.cmd['set_fw_then_fwd'] % (filter_name1, term,
                                                    'FC-Q3'),
                     self.cmd['set_fw_discard'] % (filter_name1, term),
                     self.cmd['set_fw_port_mirror_instance'] % (filter_name1,
                                                                term,
                                                                pm_name)])

            term = "ptp"
            self.__config_build__(
                cmd=[self.cmd['set_fw_port'] % (filter_name1, term, '319'),
                     self.cmd['set_fw_port'] % (filter_name1, term, '320'),
                     self.cmd['set_fw_then_count'] % (filter_name1, term,
                                                      term),
                     self.cmd['set_fw_then_fwd'] % (filter_name1, term,
                                                    'FC-Q3'),
                     self.cmd['set_fw_discard'] % (filter_name1, term),
                     self.cmd['set_fw_port_mirror_instance'] % (filter_name1,
                                                                term,
                                                                pm_name)])

            term = "esmc"
            self.__config_build__(
                cmd=[self.cmd['set_fw_by_eth_type'] % (filter_name1, term,
                                                       '34825'),
                     self.cmd['set_fw_then_count'] % (filter_name1, term,
                                                      term),
                     self.cmd['set_fw_then_fwd'] % (filter_name1, term,
                                                    'FC-Q3'),
                     self.cmd['set_fw_discard'] % (filter_name1, term),
                     self.cmd['set_fw_port_mirror_instance'] % (filter_name1,
                                                                term,
                                                                pm_name)])

            term = "isis"
            self.__config_build__(
                cmd=[self.cmd['set_fw_from_dest_mac'] % (filter_name1, term,
                                                         '01:80:c2:00:00:14'),
                     self.cmd['set_fw_from_dest_mac'] % (filter_name1, term,
                                                         '01:80:c2:00:00:15'),
                     self.cmd['set_fw_then_count'] % (filter_name1, term,
                                                      term),
                     self.cmd['set_fw_then_fwd'] % (filter_name1, term,
                                                    'FC-Q3'),
                     self.cmd['set_fw_discard'] % (filter_name1, term),
                     self.cmd['set_fw_port_mirror_instance'] % (filter_name1,
                                                                term,
                                                                pm_name)])

            term = "icmp"
            self.__config_build__(
                cmd=[self.cmd['set_fw_ip_protocol'] % (filter_name1, term,
                                                       'icmp'),
                     self.cmd['set_fw_icmp_type'] % (filter_name1, term,
                                                     'echo-reply'),
                     self.cmd['set_fw_icmp_type'] % (filter_name1, term,
                                                     'echo-request'),
                     self.cmd['set_fw_icmp_type'] % (filter_name1, term,
                                                     'unreachable'),
                     self.cmd['set_fw_then_count'] % (filter_name1, term,
                                                      term),
                     self.cmd['set_fw_then_fwd'] % (filter_name1, term,
                                                    'FC-Q3'),
                     self.cmd['set_fw_discard'] % (filter_name1, term),
                     self.cmd['set_fw_port_mirror_instance'] % (filter_name1,
                                                                term,
                                                                pm_name)])

            term = "default"
            self.__config_build__(
                cmd=[self.cmd['set_fw_then_fwd'] % (filter_name1, term,
                                                    'FC-Q0'),
                     self.cmd['set_fw_then_accept'] % (filter_name1, term),
                     self.cmd['set_fw_then_count'] % (filter_name1, term,
                                                      term)])

            for filter_name in filter_egress_input, filter_egress_output:
                term = "arp"
                self.__config_build__(
                    cmd=[self.cmd['set_fw_by_eth_type'] % (filter_name, term,
                                                           'arp'),
                         self.cmd['set_fw_then_count'] % (filter_name, term,
                                                          term),
                         self.cmd['set_fw_then_fwd'] % (filter_name, term,
                                                        'FC-Q3'),
                         self.cmd['set_fw_then_accept'] % (filter_name, term)])

                term = "ospf"
                self.__config_build__(
                    cmd=[self.cmd['set_fw_ip_protocol'] % (filter_name, term,
                                                           'ospf'),
                         self.cmd['set_fw_then_count'] % (filter_name, term,
                                                          term),
                         self.cmd['set_fw_then_fwd'] % (filter_name, term,
                                                        'FC-Q3'),
                         self.cmd['set_fw_then_accept'] % (filter_name, term)])

                term = "pim"
                self.__config_build__(
                    cmd=[self.cmd['set_fw_ip_protocol'] % (filter_name, term,
                                                           'pim'),
                         self.cmd['set_fw_then_count'] % (filter_name, term,
                                                          term),
                         self.cmd['set_fw_then_fwd'] % (filter_name, term,
                                                        'FC-Q3'),
                         self.cmd['set_fw_then_accept'] % (filter_name, term)])

                term = "bgp"
                self.__config_build__(
                    cmd=[self.cmd['set_fw_port'] % (filter_name, term,
                                                    'bgp'),
                         self.cmd['set_fw_then_count'] % (filter_name, term,
                                                          term),
                         self.cmd['set_fw_then_fwd'] % (filter_name, term,
                                                        'FC-Q3'),
                         self.cmd['set_fw_then_accept'] % (filter_name, term)])

                term = "igmp"

                self.__config_build__(
                    cmd=[self.cmd['set_fw_ip_protocol'] % (filter_name, term,
                                                           'igmp'),
                         self.cmd['set_fw_then_count'] % (filter_name, term,
                                                          term),
                         self.cmd['set_fw_then_fwd'] % (filter_name, term,
                                                        'FC-Q3'),
                         self.cmd['set_fw_then_accept'] % (filter_name, term)])

                term = "esmc"
                self.__config_build__(
                    cmd=[self.cmd['set_fw_by_eth_type'] % (filter_name, term,
                                                           '34825'),
                         self.cmd['set_fw_then_count'] % (filter_name, term,
                                                          term),
                         self.cmd['set_fw_then_fwd'] % (filter_name, term,
                                                        'FC-Q3'),
                         self.cmd['set_fw_then_accept'] % (filter_name, term)])

                term = "ptp"
                self.__config_build__(
                    cmd=[self.cmd['set_fw_port'] % (filter_name, term, '319'),
                         self.cmd['set_fw_port'] % (filter_name, term, '320'),
                         self.cmd['set_fw_then_count'] % (filter_name, term,
                                                          term),
                         self.cmd['set_fw_then_fwd'] % (filter_name, term,
                                                        'FC-Q3'),
                         self.cmd['set_fw_then_accept'] % (filter_name, term)])

                term = "isis"
                self.__config_build__(
                    cmd=[self.cmd['set_fw_from_dest_mac'] % (
                        filter_name, term, '01:80:c2:00:00:14'),
                         self.cmd['set_fw_from_dest_mac'] % (
                             filter_name, term, '01:80:c2:00:00:15'),
                         self.cmd['set_fw_then_count'] % (filter_name, term,
                                                          term),
                         self.cmd['set_fw_then_fwd'] % (filter_name, term,
                                                        'FC-Q3'),
                         self.cmd['set_fw_then_accept'] % (filter_name, term)])

                term = "icmp"
                self.__config_build__(
                    cmd=[self.cmd['set_fw_ip_protocol'] % (filter_name, term,
                                                           'icmp'),
                         self.cmd['set_fw_icmp_type'] % (filter_name, term,
                                                         'echo-reply'),
                         self.cmd['set_fw_icmp_type'] % (filter_name, term,
                                                         'echo-request'),
                         self.cmd['set_fw_icmp_type'] % (filter_name, term,
                                                         'unreachable'),
                         self.cmd['set_fw_icmp_type'] % (filter_name, term,
                                                         'time-exceeded'),
                         self.cmd['set_fw_then_count'] % (filter_name, term,
                                                          term),
                         self.cmd['set_fw_then_fwd'] % (filter_name, term,
                                                        'FC-Q3'),
                         self.cmd['set_fw_then_accept'] % (filter_name, term)])

                term = "default"
                self.__config_build__(
                    cmd=[self.cmd['set_fw_then_fwd'] % (filter_name, term,
                                                        'FC-Q0'),
                         self.cmd['set_fw_then_accept'] % (filter_name, term),
                         self.cmd['set_fw_then_count'] % (filter_name, term,
                                                          term)])

            self.__config_build__(
                cmd=[self.cmd['set_int_encap'] % ingress_intf,
                     self.cmd['set_int_bridge'] % ingress_intf,
                     self.cmd['set_domain_int'] % (bd_name, ingress_with_unit),
                     self.cmd['set_domain_option'] % bd_name,
                     self.cmd['set_int_encap'] % egress_intf,
                     self.cmd['set_int_bridge'] % egress_intf,
                     self.cmd['set_domain_int'] % (bd_name, egress_with_unit)])
            self.config(command_list=self.config_arr)
            # Added as part of TT-30637
            self.log(message="Proceeding for checking commit error\n",
                     level='info')

            result = False
            try:
                result = self.commit().response()
            except Exception as err:
                self.log(message=err, level='Error')
                return result
        return True

    def __configure_jpg_replication(self):
        '''
        Configure JPG replication by doing the following actions:
            - Get the fpc number, bridge-domain name from ingress interface
            - Doing interface Flap by disable and enable ingress interface to
            remove stary next-hops
            - Checking for the interfaces status, if it is down,
            configure loop-back
            - Get the nhindex for route-flood-group-name which value is
            __all_ces__ by "show bridge flood bridge-domain"
            (with parameter bridge-domain name)
            - Check the plaform of device, if it is MX80 or MX104,
            fpc number is tfeb0
            - Get response from cprod command (with parameter fpc number
            and nhindex) and get Inner Next Hop Id
            - Get response from cprod command (with parameter fpc number,
            nhindex and ingress interface) and get the ingress Next Hop Id
            - Get response from cprod command (with parameter fpc number,
            nhindex and egress interface) and get the egress Next Hop Id
            - Link Speed of Egress Port (link_speed_p2) and Ingress Port
            (link_speed_p1), set rep_factor = link_speed_p2/link_speed_p1
            - Execute the replication command (with parameter inner Next Hop Id
            and ingress Next Hop Id)from shell mode and
            delete the configured loop-back interface
        :param None
        :return
            TRUE if no error occurred
            FALSE if an error occurred
        '''


        for intf in self.inout_intf_rep_pair:
            (ingress_intf_rep, egress_intf_rep) = intf.split('|')
            (ingress_intf, ingress_rep) = ingress_intf_rep.split(',')
            # (egress_intf, egress_rep) = egress_intf_rep.split(',')
            egress_intf = egress_intf_rep.split(',')[0]

            fpcnum = "fpc" + re.match(r".*?-(\d+)/", ingress_intf).group(1)
            self.log(message="FPC number: %s" % fpcnum, level='info')

            in_ = ingress_intf.replace("-", "").replace("/", "_")

            eg_ = egress_intf.replace("-", "").replace("/", "_")

            bd_name = "bd_" + in_ + "_" + eg_

            self.log(message="Doing interface Flap to remove stary next-hops",
                     level='info')
#             self.shell(command='cli')
#             self.shell(command='configure')
#             self.shell(command=self.cmd['set_intf_disable'] % ingress_intf)
            self.config(
                command_list=[self.cmd['set_intf_disable'] % ingress_intf])
            self.commit()
#             self.shell(command=self.cmd['del_intf_disable'] % ingress_intf)
            self.config(
                command_list=[self.cmd['del_intf_disable'] % ingress_intf])
            self.commit()
            self.log(message="Interface Flap to remove stary next-hops Done",
                     level='info')

            time.sleep(10)

            for ifd_st in range(0, 10):
                rpc_str = self.get_rpc_equivalent(
                    command=self.cmd['show_intf_terse'] % ingress_intf)
                res = self.execute_rpc(command=rpc_str).response()
                intf_status_in = res.find(".//oper-status").text.strip()
                rpc_str = self.get_rpc_equivalent(
                    command=self.cmd['show_intf_terse'] % egress_intf)
                res = self.execute_rpc(command=rpc_str).response()
                intf_status_eg = res.find(".//oper-status").text.strip()
                self.log(message="intf_status_in: %s, intf_status_eg: %s"
                         % (intf_status_in, intf_status_eg), level='info')

                if intf_status_in != 'up' or intf_status_eg != 'up':
                    self.cli(command=self.cmd['show_chassis_fpc'] +
                             " |no-more")
                    self.cli(command=self.cmd['show_chassis_fpc_pic_stt'] +
                             " |no-more")
                    self.cli(command=self.cmd['show_intf_terse']
                             % ingress_intf)
                    self.cli(command=self.cmd['show_intf_terse']
                             % egress_intf)
                    self.config(command_list=[self.cmd['set_intf_gige_opt']
                                              % ingress_intf])
                    self.commit()
                    self.log(message="Interface is still down", level='info')
                    time.sleep(10)
                else:
                    self.log(message="INTERFACE IS UP HENCE PROCEEDING",
                             level='info')
                    break

                self.log(
                    message="Iteration count is : %s MAX re-try 9" % ifd_st,
                    level='info')

            if ifd_st == 9:
                if intf_status_in != 'down':
                    self.log(message="----ingress int down", level='error')
                if intf_status_eg != 'down':
                    self.log(message="----egress int down", level='error')

                self.log(message="Aborted! As interfaces aren't up",
                         level='error')
                self.__reset_jpg_config()

                raise TobyException("One or more Interfaces are down. Hence aborting the script", host_obj=self)

            ###################################################################
            # Checking for the interfaces status, if it is down
            # configure loop-back
            # This is done only on $port1 which is facing towards RT
            ###################################################################

            # Get the nhindex for route-flood-group-name
            show = self.cli(command=self.cmd['show_bridge_flood']
                            % bd_name)
            res = show.response()
            for line in res.split("\n"):
                check = re.match(r"(.*)(__all_ces__)(\s+)(\w+)(\s+)(\d+)(.*)",
                                 line)
                if check:
                    nhindex = check.group(6)
            try:
                nhindex
            except Exception:
                self.log(
                    message="Unable to get the nhindex for route-flood-group" +
                    "-name whose value is __all_ces__",
                    level='error')
                raise TobyException("Unable to get the nhindex for route-flood" +
                                    "-group-name whose value is __all_ces__", host_obj=self)

            show = self.cli(command=self.cmd['show_version'])
            res = show.response().split("\n")
            for line in res:
                check = re.match(r"Model: (.*)", line)
                if check:
                    model = check.group(1)

            if re.search(r'mx80|mx104', model.lower()):
                fpcnum = "tfeb0"

            # Prepare the cprod command
            cprod_cmd = self.cmd['cprod_show_nhdb'] % (fpcnum, nhindex)
#             self.shell(command='exit')
            self.shell(command='run start shell')
            crop = self.shell(command=cprod_cmd)
            res = crop.response()

            self.__verify_cprod_response(res)

            # Parse and get the Next-Hop Id, Inner Next Hop Id,
            # ingress nhid and egress nhid
            lines = res.split("\n")
            ids = []
            for line in lines:
                check = re.match(r"\s*(\d+)\(", line)
                if check:
                    ids.append(check.group(1))

            if len(ids) != 4:
                self.log(
                    message="Unable to get Next-Hop Id, Inner Next Hop Id, " +
                    "ingress nhid and egress nhid",
                    level='error')
                raise TobyException("Unable to get Next-Hop Id, Inner Next " +
                                    "Hop Id, ingress nhid and egress nhid", host_obj=self)

            inner_nhid = ids[1]

            ###################################################################
            # Get ingress Next-Hop ID
            ingress_nhid = self.__get_intf_nhid(fpcnum, nhindex, ingress_intf)

            # Get Egress Next-Hop ID
            egress_nhid = self.__get_intf_nhid(fpcnum, nhindex, egress_intf)

            ##################################################################
            # Deciding on the replication factor

            rep_factor = 1

            if ingress_rep.isdigit():
                rep_factor = int(ingress_rep)
            else:
                rpc_str = self.get_rpc_equivalent(
                    command=self.cmd['show_interfaces'] % egress_intf)
                res = self.execute_rpc(command=rpc_str).response()
                link_speed_p2 = res.find(".//physical-interface/speed")\
                    .text.strip()
                self.log(
                    message="Link Speed of Egress Port: %s" % link_speed_p2,
                    level='info')

                rpc_str = self.get_rpc_equivalent(
                    command=self.cmd['show_interfaces'] % ingress_intf)
                res = self.execute_rpc(command=rpc_str).response()
                link_speed_p1 = res.find(".//physical-interface/speed")\
                    .text.strip()
                self.log(
                    message="Link Speed of Ingress Port: %s" % link_speed_p1,
                    level='info')

                link_speed = {'1000mbps': 1,
                              '10Gbps': 10,
                              '40Gbps': 40,
                              '100Gbps': 100}
                link_speed_p2 = link_speed[link_speed_p2]
                link_speed_p1 = link_speed[link_speed_p1]

                rep_factor = int(link_speed_p2/link_speed_p1)

            self.log(message="Replication Factor: %s ," % rep_factor +
                     "inner_nhid: %s , " % inner_nhid +
                     "Ingress_nhid: %s , " % ingress_nhid +
                     "Egress_nhid: %s " % egress_nhid)

            # Preparing and executing the replication command
            egress_nhid = ' '+str(egress_nhid)
            tmp = int(rep_factor) * str(egress_nhid)

            rep_cmd = self.cmd['nhchange_composite'] % (inner_nhid,
                                                        ingress_nhid, tmp)
            self.shell(command='start shell')
            self.shell(command=rep_cmd)

            self.config(
                command_list=[self.cmd['del_intf_gige'] % ingress_intf])
            result = False
            try:
                result = self.commit().response()
            except Exception:
                self.log(message="Commit Failed", level="error")
                return result
        return True

    @staticmethod
    def jpg_replication(jpg_devices):
        '''
        Get all router session handles and execute jpg_replication_module

        ARGUMENTS:
            [jpg_devices]
            
            :param LIST jpg_devices
                *Required* list of jpg devices's objects

        ROBOT USAGE:
            ${jpg_devices_list} =  Create List ${junos_dev.current_node.current_controller}
            ${result} =    Configure Jpg Replication   devices=${jpg_devices_list}

        :return:
            TRUE/FALSE if no error occurred
            Exception if an error occurred
        '''
        results = []
        exception_result = False
        for jpg_device in jpg_devices:
            try:
                result = jpg_device.__jpg_replication_module()
            except Exception as err:
                exception_result = True
                result = err
            results.append(result)
        if not any(results) or exception_result:
            raise TobyException("Fail to execute JPG replication module on all devices")
        return not exception_result

    def __jpg_replication_module(self):
        '''
        Configure JPG replication module by doing the following actions:
            - Get the fpc number, bridge-domain name from ingress interface
            - Get the nhindex for route-flood-group-name which value is
            __all_ces__ by "show bridge flood bridge-domain"
            (with parameter bridge-domain name)
            - Check the plaform of device, if it is MX80 or MX104,
            fpc number is tfeb0
            - Get response from cprod command (with parameter fpc number
            and nhindex) and get Inner Next Hop Id
            - Get response from cprod command (with parameter fpc number,
            nhindex and ingress interface) and get the ingress Next Hop Id
            - Get response from cprod command (with parameter fpc number,
            nhindex and egress interface) and get the egress Next Hop Id
            - Link Speed of Egress Port (link_speed_p2) and Ingress Port
            (link_speed_p1), set rep_factor = link_speed_p2/link_speed_p1
            - Execute the replication command (with parameter inner Next Hop Id
            and ingress Next Hop Id)from shell mode
        :param None
        :return:
            TRUE if no error occurred
            FALSE if an error occurred
        '''
        if 'root' not in self.shell(command='whoami').response():
            self.su()
        self.__get_ingress_egress_interfaces()
        self.log(message="Replication_pair = %s" % self.inout_intf_rep_pair,
                 level='info')
        for intf in self.inout_intf_rep_pair:
            ingress_intf_rep, egress_intf_rep = intf.split('|')
            ingress_intf, ingress_rep = ingress_intf_rep.split(',')
            # egress_intf, egress_rep = egress_intf_rep.split(',')
            egress_intf = egress_intf_rep.split(',')[0]
            matched = re.search(r".*?-(\d+)/", ingress_intf)
            fpcnum = "fpc"
            if matched:
                fpcnum = fpcnum + matched.group(1)
            self.log(message="FPC number: %s" % fpcnum, level='info')
            _in = ingress_intf.replace("-", "").replace("/", "_")
            _eg = egress_intf.replace("-", "").replace("/", "_")
            bd_name = "bd_" + _in + "_" + _eg
            # Get the nhindex for route-flood-group-name whose value is
            # __all_ces__
            _command = self.cmd['show_brdg_flood_brdg_domain'] % bd_name
            res = self.cli(command=_command, format='text')
            out = res.response()
            matched = re.search(r"(.*)(__all_ces__)(\s+)(\w+)(\s+)(\d+)(.*)",
                                out)
            if matched:
                nhindex = matched.group(6)
            else:
                nhindex = None
            if not nhindex:
                continue
            # TT-30414
            _command = self.cmd['show_version']
            res = self.cli(command=_command, format='text')
            response = res.response()
            matched = re.search(r"Model:\s+(\w+)", response)
            if matched:
                model = matched.group(1)
            if re.search(r'mx80', model) or re.search(r'mx104', model):
                fpcnum = "tfeb0"
            cprod_cmd = self.cmd['cprod_a_show_nhdb_id'] % (fpcnum, nhindex)
            res = self.shell(command=cprod_cmd)
            out = res.response()
            self.__verify_cprod_response(out)
            # Parse and get the Next-Hop Id, Inner Next Hop Id, ingress nhid
            # and egress nhid
            lines = out.split("\n")
            ids = []
            for line in lines:
                if re.search(r"^\s*$", line):
                    continue
                matched = re.search(r"\s*(\d+)\(", line)
                if matched:
                    ids.append(matched.group(1))
            if not ids or len(ids) < 2:
                raise TobyException("Unable to get inner ids. ", host_obj=self)
            inner_nhid = ids[1]
            # Changes done to cater correct ingress and egress interfaces
            # Get ingress Next-Hop ID
            ingress_nhid = self.__get_intf_nhid(fpcnum, nhindex, ingress_intf)
            # Get Egress Next-Hop ID
            egress_nhid = self.__get_intf_nhid(fpcnum, nhindex, egress_intf)
            # Changes done to cater correct ingress and egress interfaces
            # Deciding on the replication factor
            rep_factor = 1
            if not re.search(r"\D", ingress_rep):
                rep_factor = ingress_rep
            else:
                _command = self.cmd['show_intf_grep_speed']
                res = self.cli(command=_command % egress_intf)
                response = res.response()
                if re.search(r",\s+Speed:\s+(\d+)", response):
                    link_speed_p2_re = re.search(r",\s+Speed:\s+(\w+),",
                                                 response)
                    link_speed_p2 = link_speed_p2_re.group(1).lower()
                self.log(
                    message="Link Speed of Egress Port: %s" % link_speed_p2,
                    level='info')
                res = self.cli(command=_command % ingress_intf)
                response = res.response()
                if re.search(r",\s+Speed:\s+(\d+)", response):
                    link_speed_p1_re = re.search(r",\s+Speed:\s+(\w+),",
                                                 response)
                    link_speed_p1 = link_speed_p1_re.group(1).lower()
                self.log(
                    message="Link Speed of Ingress Port: %s" % link_speed_p1,
                    level='info')
                link_speed_dict = {'1000mbps': 1,
                                   '10gbps': 10,
                                   '40gbps': 40,
                                   '100gbps': 100}
                link_speed_p2 = link_speed_dict.get(link_speed_p2)
                link_speed_p1 = link_speed_dict.get(link_speed_p1)
                rep_factor = link_speed_p2 / link_speed_p1
            self.log(message="Replication Factor: %s, " % rep_factor +
                     "inner_nhid: %s, " % inner_nhid +
                     "Ingress_nhid: %s, " % ingress_nhid +
                     "Egress_nhid: %s" % egress_nhid,
                     level='info')
            # Preparing and executing the replication command
            rep_cmd = "route\.new nhchange %s composite %s " % (inner_nhid,
                                                                ingress_nhid)
            tmp = "%s " % str(egress_nhid) * int(rep_factor)
            rep_cmd = rep_cmd + tmp
            rep_cmd = rep_cmd + 'compose-as split-horizon'
            self.log(message="rep_cmd: %s" % rep_cmd, level='debug')
            self.shell(command=rep_cmd)
        return True

    def setup_jpg_filter(self, **kwargs):
        '''
        Create a list of command for configuring JPG filter

        ARGUMENTS:
            [kwargs]
            :param STR filter:
                *REQUIRED*  filter name for command ,e.g : ctrl_input_dut_1
            :param STR term_name:
                *REQUIRED*  term name for command, e.g : ipterm
            :param STR port_name:
                *REQUIRED*  port name for command, e.g : ge-9/0/0
            :param STR ip_src:
                *OPTIONAL*  IP source for command, e.g : 1.1.1.0
            :param STR ip_dst:
                *OPTIONAL*  IP destination for command, e.g : 1.1.1.1
            :param STR prefix_list:
                *OPTIONAL*  Prefix list for command, e.g : filter
            :param INT vlan_id:
                *OPTIONAL*  Vlan ID for command, e.g : 10
            :param INT vlan_pri:
                *OPTIONAL*  Vlan priority for command, e.g : 1
            :param INT ether_type:
                *OPTIONAL*  Ethernet type for command, e.g : 1
            :param INT ip_precedence:
                *OPTIONAL*  IP precedence for command, e.g : 7
            :param INT single_term:
                *OPTIONAL*  Single term for command, e.g : 1
            :param INT vlan_id_count:
                *OPTIONAL*  Vlan ID count for command, e.g : 5
            :param INT vlan_id_step:
                *OPTIONAL*  Vlan ID step for command, e.g : 2
            :param INT source_port:
                *OPTIONAL*  Source port for command, e.g : http
            :param INT dest_port:
                *OPTIONAL*  Dest port for command, e.g : https
            :param INT src_mod:
                *OPTIONAL*  Source mode for command, e.g : 1
            :param INT src_num_addr:
                *OPTIONAL*  Source number address for command, e.g : 2
            :param INT src_mask:
                *OPTIONAL*  Source mask for command, e.g : 24
            :param INT dst_mod:
                *OPTIONAL*  Dest mode for command, e.g : 1
            :param INT dst_num_addr:
                *OPTIONAL*  Dest number address for command, e.g : 2
            :param INT dst_mask:
                *OPTIONAL*  Dest mask for command, e.g : 24
            :param INT step:
                *OPTIONAL*  Step for command, e.g : 2
            :param STR mac_src:
                *OPTIONAL*  MAC source for command, e.g : 00:00:00:11:00:11
            :param INT mac_dst:
                *OPTIONAL*  MAC destination for command, e.g : 00:00:00:11:00:12

        ROBOT USAGE:
            setup jpg filter    filter=ctrl_input_dut_1   term_name=ipterm    
                            ...     port_name=ge-9/0/0  

        :returns: append all commands to global lists "term_array"
                and "jpg_config"
        '''
        # Check parameter
        if "filter" not in kwargs.keys():
            self.log(message="filter name must be defined", level='error')
            return False
        else:
            filter_name = kwargs['filter']

        if "term_name" not in kwargs.keys():
            self.log(message="term name must be defined", level='error')
            return False
        else:
            term_name = kwargs['term_name']

        if "port_name" not in kwargs.keys():
            self.log(message="port name must be defined", level='error')
            return False
        else:
            port_name = kwargs['port_name']

        #  add New Filter Array
        self.__add_new_filter_to_array(filter=filter)

        # Get information from parameter

        ip_src = kwargs.get('ip_src', 'NOT_GIVEN')

        ip_dst = kwargs.get('ip_dst', 'NOT_GIVEN')

        # prefix_list_name = kwargs.get('prefix_list', 'NOT_GIVEN')

        vlan_id = kwargs.get('vlan_id', 'NOT_GIVEN')

        vlan_pri = kwargs.get('vlan_pri', 'NOT_GIVEN')

        ether_type = kwargs.get('ether_type', 'NOT_GIVEN')

        ip_precedence = kwargs.get('ip_precedence', 'NOT_GIVEN')

        single_term = kwargs.get('single_term', 0)

        # Remove the first - and replace all / by _ in port_name
        inout = port_name.replace(port_name[port_name.find("-")], "", 1).\
            replace("/", "_")

        filter_name = filter_name + "_" + inout

        # FILETER TO CARE VLAN-ID #
        if vlan_id != "NOT_GIVEN":
            vlan_id_count = kwargs.get('vlan_id_count', 'NOT_GIVEN')
            vlan_id_step = kwargs.get('vlan_id_step', 'NOT_GIVEN')

            self.term_array.append(self.cmd['del_fw_tern_default'] % filter)
            self.jpg_config.append(self.cmd['del_fw_tern_default'] % filter)

            if vlan_id_count != "NOT_GIVEN" and vlan_id_step != "NOT_GIVEN":
                last_vlan_id = int(
                    vlan_id) + int(vlan_id_count) * int(vlan_id_step)
                j = 1

                for i in range(int(vlan_id),
                               int(last_vlan_id) + 1,
                               int(vlan_id_step)):
                    if single_term == 0:
                        _ji = "%s%s" % (j, i)
                        term_namei = "%s%s" % (term_name, i)
                        term_namej = "%s%s" % (term_name, j)

                        self.term_array.append(self.cmd['set_fw_by_vlan']
                                               % (filter, term_name, _ji))

                        self.term_array.append(
                            self.cmd['set_fw_by_accept_count'] % (
                                filter, term_namej, term_namei))

                        self.jpg_config.append(self.cmd['set_fw_by_vlan']
                                               % (filter, term_name, _ji))

                        self.jpg_config.append(
                            self.cmd['set_fw_by_accept_count'] % (
                                filter, term_namej, term_namei))
                    else:
                        self.term_array.append(self.cmd['set_fw_by_vlan']
                                               % (filter, term_name, i))

                        self.term_array.append(
                            self.cmd['set_fw_by_accept_count'] % (
                                filter, term_name, term_name))

                        self.jpg_config.append(self.cmd['set_fw_by_vlan']
                                               % (filter, term_name, i))

                        self.jpg_config.append(
                            self.cmd['set_fw_by_accept_count'] % (
                                filter, term_name, term_name))
                    j = j + 1

            else:
                self.term_array.append(self.cmd['set_fw_by_vlan']
                                       % (filter, term_name, vlan_id))

                self.term_array.append(self.cmd['set_fw_by_accept_count']
                                       % (filter, term_name, term_name))

                self.jpg_config.append(self.cmd['set_fw_by_vlan']
                                       % (filter, term_name, vlan_id))

                self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                       % (filter, term_name, term_name))

            if "source_port" in kwargs.keys() and kwargs['source_port']:
                self.term_array.append(self.cmd['set_fw_by_source_port']
                                       % (filter, term_name,
                                          kwargs['source_port']))

                self.jpg_config.append(self.cmd['set_fw_by_source_port']
                                       % (filter, term_name,
                                          kwargs['source_port']))

            if "dest_port" in kwargs.keys() and kwargs['dest_port']:
                self.term_array.append(
                    self.cmd['set_fw_by_dest_port'] % (
                        filter, term_name, kwargs['dest_port']))

                self.jpg_config.append(self.cmd['set_fw_by_dest_port']
                                       % (filter, term_name,
                                          kwargs['dest_port']))

            # attach default term to filter
            self.__attach_default_term(filter=filter)

        # ============================================== #
        #         Adding Term for ether_type             #
        # ============================================== #
        if "source_port" in kwargs.keys() or "dest_port" in kwargs.keys():
            if "source_port" in kwargs.keys() and kwargs['source_port']:
                self.term_array.append(self.cmd['set_fw_by_source_port']
                                       % (filter, term_name,
                                          kwargs['source_port']))

                self.jpg_config.append(self.cmd['set_fw_by_source_port']
                                       % (filter, term_name,
                                          kwargs['source_port']))

            if "dest_port" in kwargs.keys() and kwargs['dest_port']:
                self.term_array.append(
                    self.cmd['set_fw_by_dest_port'] % (
                        filter, term_name, kwargs['dest_port']))

                self.jpg_config.append(self.cmd['set_fw_by_dest_port']
                                       % (filter, term_name,
                                          kwargs['dest_port']))

            # attach default term
            self.__attach_default_term(filter=filter)

        if ether_type != "NOT_GIVEN":
            self.term_array.append(self.cmd['del_fw_tern_default'] % filter)
            self.jpg_config.append(self.cmd['del_fw_tern_default'] % filter)

            self.term_array.append(self.cmd['set_fw_by_eth_type']
                                   % (filter, term_name, ether_type))
            self.term_array.append(self.cmd['set_fw_by_accept_count']
                                   % (filter, term_name, term_name))
            self.jpg_config.append(self.cmd['set_fw_by_eth_type']
                                   % (filter, term_name, ether_type))
            self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                   % (filter, term_name, term_name))

            # attach default term
            self.__attach_default_term(filter=filter)

        # ================================================ #
        #          Adding Term for ip_precedence         #
        # ================================================ #
        if ip_precedence != "NOT_GIVEN":
            self.term_array.append(self.cmd['del_fw_tern_default'] % filter)
            self.jpg_config.append(self.cmd['del_fw_tern_default'] % filter)

            self.term_array.append(self.cmd['set_fw_from_ip__precedence']
                                   % (filter, term_name, ip_precedence))
            self.term_array.append(self.cmd['set_fw_by_accept_count']
                                   % (filter, term_name, term_name))

            self.jpg_config.append(self.cmd['set_fw_from_ip__precedence']
                                   % (filter, term_name, ip_precedence))
            self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                   % (filter, term_name, term_name))

        # FILETER TO CARE VLAN-PRI #
        if vlan_pri != "NOT_GIVEN":
            self.term_array.append(self.cmd['del_fw_tern_default'] % filter)
            self.jpg_config.append(self.cmd['del_fw_tern_default'] % filter)

            self.term_array.append(self.cmd['set_fw_by_vlan_prio']
                                   % (filter, term_name, vlan_pri))
            self.term_array.append(self.cmd['set_fw_by_accept_count']
                                   % (filter, term_name, term_name))

            self.jpg_config.append(self.cmd['set_fw_by_vlan_prio']
                                   % (filter, term_name, vlan_pri))
            self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                   % (filter, term_name, term_name))

            # attach default term
            self.__attach_default_term(filter=filter)

        # FILETER TO CARE ip-src #
        if ip_src != "NOT_GIVEN":
            src_mod = kwargs.get('src_mod', 'NOT_GIVEN')
            src_num_addr = kwargs.get('src_num_addr', 'NOT_GIVEN')

            self.term_array.append(self.cmd['del_fw_tern_default'] % filter)
            self.jpg_config.append(self.cmd['del_fw_tern_default'] % filter)

            if src_num_addr != "NOT_GIVEN":
                step = kwargs.get('step', 'NOT_GIVEN')

                oct_array = ip_src.split(".")
                first_oct = oct_array[0]
                sec_oct = oct_array[1]
                third_oct = oct_array[2]
                fourth_oct = oct_array[3]

                for i in range(1, int(src_num_addr) + 1, 1):
                    new_src_ip = first_oct + "." + sec_oct + "." + \
                        third_oct + "." + fourth_oct
                    term_namei = "%s%s" % (term_name, i)
                    self.term_array.append(self.cmd['set_fw_from_source_ip']
                                           % (filter, term_namei, new_src_ip))
                    self.term_array.append(self.cmd['set_fw_by_accept_count']
                                           % (filter, term_namei, term_namei))

                    self.jpg_config.append(self.cmd['set_fw_from_source_ip']
                                           % (filter, term_namei, new_src_ip))
                    self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                           % (filter, term_namei, term_namei))

                    if src_mod == "1":
                        fourth_oct = fourth_oct + step
                    if src_mod == "2":
                        third_oct = third_oct + step
                    if src_mod == "3":
                        sec_oct = sec_oct + step
                    if src_mod == "4":
                        first_oct = first_oct + step

            else:
                src_mask = kwargs.get('src_mask', 'NOT_GIVEN')

                if src_mask == "NOT_GIVEN":
                    src_mask = 32
                ip_src_mask = "%s/%s" % (ip_src, src_mask)
                self.term_array.append(self.cmd['set_fw_from_source_ip']
                                       % (filter, term_name, ip_src_mask))
                self.term_array.append(self.cmd['set_fw_by_accept_count']
                                       % (filter, term_name, term_name))

                self.jpg_config.append(self.cmd['set_fw_from_source_ip']
                                       % (filter, term_name, ip_src_mask))
                self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                       % (filter, term_name, term_name))

            # attach default term
            self.__attach_default_term(filter=filter)

        # FILETER TO CARE ip-dst #
        if ip_dst != "NOT_GIVEN":
            dst_mod = kwargs.get('dst_mod', 'NOT_GIVEN')
            dst_num_addr = kwargs.get('dst_num_addr', 'NOT_GIVEN')

            self.term_array.append(self.cmd['del_fw_tern_default'] % filter)
            self.jpg_config.append(self.cmd['del_fw_tern_default'] % filter)

            if dst_num_addr != "NOT_GIVEN":
                step = kwargs.get('step', 'NOT_GIVEN')

                oct_array = ip_dst.split(".")
                first_oct = oct_array[0]
                sec_oct = oct_array[1]
                third_oct = oct_array[2]
                fourth_oct = oct_array[3]

                for i in range(1, int(dst_num_addr) + 1, 1):
                    new_dst_ip = first_oct + "." + sec_oct + "." + \
                        third_oct + "." + fourth_oct
                    term_namei = "%s%s" % (term_name, i)
                    self.term_array.append(self.cmd['set_fw_from_dest_ip']
                                           % (filter, term_namei, new_dst_ip))
                    self.term_array.append(self.cmd['set_fw_by_accept_count']
                                           % (filter, term_namei, term_namei))

                    self.jpg_config.append(self.cmd['set_fw_from_dest_ip']
                                           % (filter, term_namei, new_dst_ip))
                    self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                           % (filter, term_namei, term_namei))

                    if dst_mod == "1":
                        fourth_oct = fourth_oct + step
                    if dst_mod == "2":
                        third_oct = third_oct + step
                    if dst_mod == "3":
                        sec_oct = sec_oct + step
                    if dst_mod == "4":
                        first_oct = first_oct + step

            else:
                dst_mask = kwargs.get('dst_mask', 'NOT_GIVEN')

                if dst_mask == "NOT_GIVEN":
                    dst_mask = 32
                ip_dst_mask = "%s/%s" % (ip_dst, dst_mask)
                self.term_array.append(self.cmd['set_fw_from_dest_ip']
                                       % (filter, term_name, ip_dst_mask))
                self.term_array.append(self.cmd['set_fw_by_accept_count']
                                       % (filter, term_name, term_name))

                self.jpg_config.append(self.cmd['set_fw_from_dest_ip']
                                       % (filter, term_name, ip_dst_mask))
                self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                       % (filter, term_name, term_name))

            # attach default term
            self.__attach_default_term(filter=filter)

        # FILETER TO CARE mac_src address #
        mac_src = kwargs.get('mac_src', 'NOT_GIVEN')

        if mac_src != "NOT_GIVEN":
            src_mod = kwargs.get('src_mod', 'NOT_GIVEN')
            src_num_addr = kwargs.get('src_num_addr', 'NOT_GIVEN')

            self.term_array.append(self.cmd['del_fw_tern_default'] % filter)
            self.jpg_config.append(self.cmd['del_fw_tern_default'] % filter)

            if src_num_addr != "NOT_GIVEN":
                step = kwargs.get('step', 'NOT_GIVEN')

                oct_array = mac_src.split(":")
                first_oct = int(oct_array[5], 16)
                sec_oct = int(oct_array[4], 16)
                third_oct = int(oct_array[3], 16)
                fourth_oct = int(oct_array[2], 16)
                fifth_oct = int(oct_array[1], 16)
                sixth_oct = int(oct_array[0], 16)

                first_oct_hex = hex(first_oct).split('x')[1]
                sec_oct_hex = hex(sec_oct).split('x')[1]
                third_oct_hex = hex(third_oct).split('x')[1]
                fourth_oct_hex = hex(fourth_oct).split('x')[1]
                fifth_oct_hex = hex(fifth_oct).split('x')[1]
                sixth_oct_hex = hex(sixth_oct).split('x')[1]

                for i in range(1, int(src_num_addr) + 1, 1):
                    new_src_mac = sixth_oct_hex + ":" + fifth_oct_hex + ":" + \
                        fourth_oct_hex + ":" + third_oct_hex + ":" + \
                        sec_oct_hex + ":" + first_oct_hex
                    term_namei = "%s%s" % (term_name, i)
                    self.term_array.append(self.cmd['set_fw_from_source_mac']
                                           % (filter, term_namei, new_src_mac))
                    self.term_array.append(self.cmd['set_fw_by_accept_count']
                                           % (filter, term_namei, term_namei))

                    self.jpg_config.append(self.cmd['set_fw_from_source_mac']
                                           % (filter, term_namei, new_src_mac))
                    self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                           % (filter, term_namei, term_namei))
                    if src_mod == "1":
                        first_oct = first_oct + int(step)
                    if src_mod == "2":
                        sec_oct = sec_oct + int(step)
                    if src_mod == "3":
                        third_oct = third_oct + int(step)
                    if src_mod == "4":
                        fourth_oct = fourth_oct + int(step)
                    if src_mod == "5":
                        fifth_oct = fifth_oct + int(step)
                    if src_mod == "6":
                        sixth_oct = sixth_oct + int(step)

                    first_oct_hex = hex(first_oct).split('x')[1]
                    sec_oct_hex = hex(sec_oct).split('x')[1]
                    third_oct_hex = hex(third_oct).split('x')[1]
                    fourth_oct_hex = hex(fourth_oct).split('x')[1]
                    fifth_oct_hex = hex(fifth_oct).split('x')[1]
                    sixth_oct_hex = hex(sixth_oct).split('x')[1]

            else:
                self.term_array.append(self.cmd['set_fw_from_source_mac']
                                       % (filter, term_name, mac_src))
                self.term_array.append(self.cmd['set_fw_by_accept_count']
                                       % (filter, term_name, term_name))

                self.jpg_config.append(self.cmd['set_fw_from_source_mac']
                                       % (filter, term_name, mac_src))
                self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                       % (filter, term_name, term_name))

            # attach default term
            self.__attach_default_term(filter=filter)

        # FILETER TO CARE mac_dst address #
        mac_dst = kwargs.get('mac_dst', 'NOT_GIVEN')

        if mac_dst != "NOT_GIVEN":
            dst_mod = kwargs.get('dst_mod', 'NOT_GIVEN')
            dst_num_addr = kwargs.get('dst_num_addr', 'NOT_GIVEN')

            self.term_array.append(self.cmd['del_fw_tern_default'] % filter)
            self.jpg_config.append(self.cmd['del_fw_tern_default'] % filter)

            if dst_num_addr != "NOT_GIVEN":
                step = kwargs.get('step', 'NOT_GIVEN')

                oct_array = mac_dst.split(":")
                first_oct = int(oct_array[5], 16)
                sec_oct = int(oct_array[4], 16)
                third_oct = int(oct_array[3], 16)
                fourth_oct = int(oct_array[2], 16)
                fifth_oct = int(oct_array[1], 16)
                sixth_oct = int(oct_array[0], 16)

                first_oct_hex = hex(first_oct).split('x')[1]
                sec_oct_hex = hex(sec_oct).split('x')[1]
                third_oct_hex = hex(third_oct).split('x')[1]
                fourth_oct_hex = hex(fourth_oct).split('x')[1]
                fifth_oct_hex = hex(fifth_oct).split('x')[1]
                sixth_oct_hex = hex(sixth_oct).split('x')[1]

                for i in range(1, int(dst_num_addr) + 1, 1):
                    new_dst_mac = sixth_oct_hex + ":" + fifth_oct_hex + ":" + \
                        fourth_oct_hex + ":" + third_oct_hex + ":" + \
                        sec_oct_hex + ":" + first_oct_hex
                    term_namei = "%s%s" % (term_name, i)
                    self.term_array.append(self.cmd['set_fw_from_dest_mac']
                                           % (filter, term_namei, new_dst_mac))
                    self.term_array.append(self.cmd['set_fw_by_accept_count']
                                           % (filter, term_namei, term_namei))

                    self.jpg_config.append(self.cmd['set_fw_from_dest_mac']
                                           % (filter, term_namei, new_dst_mac))
                    self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                           % (filter, term_namei, term_namei))

                    if dst_mod == "1":
                        first_oct = first_oct + int(step)
                    if dst_mod == "2":
                        sec_oct = sec_oct + int(step)
                    if dst_mod == "3":
                        third_oct = third_oct + int(step)
                    if dst_mod == "4":
                        fourth_oct = fourth_oct + int(step)
                    if dst_mod == "5":
                        fifth_oct = fifth_oct + int(step)
                    if dst_mod == "6":
                        sixth_oct = sixth_oct + int(step)

                    first_oct_hex = hex(first_oct).split('x')[1]
                    sec_oct_hex = hex(sec_oct).split('x')[1]
                    third_oct_hex = hex(third_oct).split('x')[1]
                    fourth_oct_hex = hex(fourth_oct).split('x')[1]
                    fifth_oct_hex = hex(fifth_oct).split('x')[1]
                    sixth_oct_hex = hex(sixth_oct).split('x')[1]

            else:
                self.term_array.append(self.cmd['set_fw_from_dest_mac']
                                       % (filter, term_name, mac_dst))
                self.term_array.append(self.cmd['set_fw_by_accept_count']
                                       % (filter, term_name, term_name))

                self.jpg_config.append(self.cmd['set_fw_from_dest_mac']
                                       % (filter, term_name, mac_dst))
                self.jpg_config.append(self.cmd['set_fw_by_accept_count']
                                       % (filter, term_name, term_name))
            # attach Default Term
            self.__attach_default_term(filter=filter)

    def attach_jpg_filter(self):
        '''
        Configure the jpg filters to jpg devices from term_array

        ARGUMENTS:
            [self]
            :param: none

        ROBOT USAGE:
            Attach JPG Filter

        :return: TRUE/FALSE
            True if commit succeeds, else False
        '''

        self.config(command_list=self.term_array)

        result = False
        try:
            # result = self.commit().response()
            result = self.commit().status()
            self.log(message="Configuring user defined filter PASS",
                     level="info")
        except Exception as err:
            self.log(message=err, level='Error')
            self.log(message="Configuring user defined filter FAIL",
                     level="error")
            return result

        del self.term_array[:]
        del self.user_filter[:]
        return result

    def __add_new_filter_to_array(self, **args):
        '''
        Add a new filter to user_filter list, a global list defined
        in JPG Class. If the filter already exist, ignore it
        :return: None
            The list user_filter will be added by this function
        '''
        if 'filter' in args.keys():
            _filter = args['filter']
            _new_filter = True
            if _filter in self.user_filter:
                _new_filter = False
            if _new_filter:
                self.user_filter.append(_filter)

    def __attach_default_term(self, **args):
        '''
        Attach default term to jpg_config and term_array, global
        lists defined in JPG Class
        :param _filter:
            E.g. ['jpg_config_command2']
        :return: None
            The lists jpg_config and term_array will be added by this function
            E.g. ['jpg_config_command1', 'jpg_config_command2']
        '''
        if 'filter' in args.keys():
            _filter = args['filter']
            term = "default"
            self.jpg_config.append(
                self.cmd['set_fw_then_fwd'] % (_filter, term, 'FC-Q1'))
            self.jpg_config.append(
                self.cmd['set_fw_then_accept'] % (_filter, term))
            self.jpg_config.append(
                self.cmd['set_fw_then_count'] % (_filter, term, term))

    def get_jpg_stats(self):
        '''
        Get statistics of all jpg devices

        DESCRIPTION:
            This function will connect to all jpg device to get statistics

        ARGUMENTS:
            :param: None

        ROBOT USAGE:
            Get JPG Stats
                
        :return: stats
            Status of all jpg device will be added to the dictionary "stats"
        '''
        rpc_str = self.get_rpc_equivalent(command='show firewall')
        response = self.execute_rpc(command=rpc_str).response()

        stats = dict(filter=dict(),)
        for i in response.findall('.//filter-information'):
            filter_name = i.find('.//filter-name')
            filter_name = filter_name.text
            if filter_name:
                # get filter name
                filter_name_cli = filter_name.replace('\n', '')
                total_pack = 0
                total_byte = 0
                counters = i.findall('.//counter')
                stats['filter'][filter_name_cli] = {}
                for j in counters:
                    term_name_cli = j.find('counter-name').text.replace('\n',
                                                                        '')
                    pack_count_cli = int(j.find('packet-count').text)
                    byte_count_cli = int(j.find('byte-count').text)
                    total_pack += pack_count_cli
                    total_byte += byte_count_cli
                    count_dict = {}

                    count_dict = dict(agg={'-pktCount': pack_count_cli,
                                           '-byteCount': byte_count_cli})
                    stats['filter'][filter_name_cli][term_name_cli] = \
                        count_dict

                count_dict = {}
                count_dict = dict(agg={'-pktCount': total_pack,
                                       '-byteCount': total_byte})
                stats['filter'][filter_name_cli].update(count_dict)

        # port label stats
        # self.shell(command='cli')
        # resp = self.shell(
        #     command='show configuration interfaces|display xml|no-more')
        # response = etree.fromstring(resp.response()).find('.//interfaces')
        rpc_str = "<get-configuration database=\"commited\"><configuration>" +\
            "<interfaces/></configuration></get-configuration>"
        response = self.execute_rpc(command=rpc_str).response()
        for i in response.findall('.//interface'):
            filter_el = i.find('.//unit/family/bridge/filter')
            if filter_el is not None:
                total_pkt_count = 0
                total_byte_count = 0
                port_name = i.find('name').text
                stats[port_name] = {}
                # if filter type is input
                if filter_el.find('.//input') is not None:
                    filter_name_cli = filter_el.find('.//input/filter-name').\
                        text
                    if filter_name_cli:
                        pkt_count_cli = stats['filter'][filter_name_cli][
                            'agg']['-pktCount']
                        byte_count_cli = stats['filter'][filter_name_cli][
                            'agg']['-byteCount']
                        stats[port_name]['TX'] = {'agg': {
                            '-TxPktCount': pkt_count_cli,
                            '-TxByteCount': byte_count_cli}}

                # if filter type is output
                if filter_el.find('.//output') is not None:
                    filter_name_cli = filter_el.find('.//output/filter-name').\
                        text
                    if filter_name_cli:
                        pkt_count_cli = stats['filter'][filter_name_cli][
                            'agg']['-pktCount']
                        byte_count_cli = stats['filter'][filter_name_cli][
                            'agg']['-byteCount']
                        stats[port_name]['RX'] = {'agg': {
                            '-RxPktCount': pkt_count_cli,
                            '-RxByteCount': byte_count_cli}}

                # if filter type is input-list
                if filter_el.find('.//input-list') is not None:
                    for input_el in filter_el.findall('input-list'):
                        filter_name_cli = input_el.text
                        # if not stats[port_name].get('RX'):
                        #     stats[port_name]['RX'] = {}
                        # stats[port_name]['RX'].update({filter_name_cli: {}})
                        stats[port_name]['RX'] = {filter_name_cli: {}}
                        if filter_name_cli in stats['filter']:
                            pkt_count_cli = stats['filter'][filter_name_cli][
                                'agg']['-pktCount']
                            byte_count_cli = stats['filter'][filter_name_cli][
                                'agg']['-byteCount']
                            total_pkt_count += pkt_count_cli
                            total_byte_count += byte_count_cli
                            # add to start dict
                            for k in stats.get('filter').get(filter_name_cli).\
                                    keys():
                                if k != 'agg':
                                    pkt_count_cli = stats['filter'][
                                        filter_name_cli][k]['agg']['-pktCount']
                                    byte_count_cli = stats['filter'][
                                        filter_name_cli][k]['agg'][
                                            '-byteCount']
#                                     print port_name
                                    stats[port_name]['RX'][
                                        filter_name_cli][k] = dict(
                                            agg={'-RxPktCount': pkt_count_cli,
                                                 '-RxByteCount':
                                                 byte_count_cli})

                    stats[port_name]['RX']['agg'] = {
                        '-RxPktCount': total_pkt_count,
                        '-RxByteCount': total_byte_count}

                # if filter type is out-list
                if filter_el.find('.//output-list') is not None:
                    # reset the total pack count
                    total_pkt_count = 0
                    total_byte_count = 0
                    for input_el in filter_el.findall('output-list'):
                        filter_name_cli = input_el.text
                        # if not stats[port_name].get('TX'):
                        #     stats[port_name]['TX'] = {}
                        # stats[port_name]['TX'].update({filter_name_cli: {}})
                        stats[port_name]['TX'] = {filter_name_cli: {}}
                        if filter_name_cli in stats['filter']:
                            pkt_count_cli = stats['filter'][filter_name_cli][
                                'agg']['-pktCount']
                            byte_count_cli = stats['filter'][filter_name_cli][
                                'agg']['-byteCount']
                            total_pkt_count += pkt_count_cli
                            total_byte_count += byte_count_cli
                            # add to start dict
                            for k in stats.get('filter').get(filter_name_cli).\
                                    keys():
                                if k != 'agg':
                                    pkt_count_cli = stats['filter'][
                                        filter_name_cli][k]['agg']['-pktCount']
                                    byte_count_cli = stats['filter'][
                                        filter_name_cli][k]['agg'][
                                            '-byteCount']
                                    stats[port_name]['TX'][
                                        filter_name_cli][k] = dict(
                                            agg={'-RxPktCount': pkt_count_cli,
                                                 '-RxByteCount':
                                                 byte_count_cli})
                    stats[port_name]['TX']['agg'] = {
                        '-RxPktCount': total_pkt_count,
                        '-RxByteCount': total_byte_count}
        return stats

    def __get_interface_status(self, intf):
        '''
        Check the status of interfaces like Loss of signal or
        optic missing or interface not present
        Debugging method to be used during failures.
        :param interface:
            REQUIRED Interface, e.g. xe-0/0/1
        :returns: a string
            "Interface <intf> is not present. Hence exiting..."
                if interface is not found
            "Loss of signal present <intf>"
                if laser-rx-power-low-alarm status is "on"
            "Optics Missing"
                if interface exists but cannot find
                its laser-rx-power-low-alarm status
        '''
        rpc_str = self.get_rpc_equivalent(command=self.cmd['show_interfaces']
                                          % intf)
        response = self.execute_rpc(command=rpc_str).response()
        error_message = ""
        status = None
        if response.find(".//error-message") is not None:
            error_message = response.find(".//error-message").text
        if error_message:
            if re.search(r".*device %s not found.*" % intf, error_message):
                msg = "Interface %s is not present. Hence exiting..." % intf
                self.log(message=msg, level='error')
                _command = self.cmd['show_chassis_fpc']
                self.cli(command=_command, format='text')
                status = "Interface %s is not present. Hence exiting..." % intf
        else:
            rpc_str = self.get_rpc_equivalent(
                command=self.cmd['show_intf_diag_optics'] % intf)
            response = self.execute_rpc(command=rpc_str).response()
            laser_rx_pw_low_alarm_stt = ""
            if response.find(".//laser-rx-power-low-alarm") is not None:
                laser_rx_pw_low_alarm_stt = response.\
                    find(".//laser-rx-power-low-alarm").text
            if laser_rx_pw_low_alarm_stt and\
                    'on' in laser_rx_pw_low_alarm_stt.lower():
                status = "Loss of signal present %s" % intf
            else:
                status = "Optics Missing"
        return status

    def __verify_cprod_response(self, response):
        '''
        Verify the response of cprod command
        Debuging Method to be used to verify response of cprod command
        :param response:
            REQUIRED response of cprod command
            E.g. response of command in string as: "err:No route to host"
        :returns:
            Error if found "err:No route to host" in response
            True if not found
        '''

        if "err:No route to host" in response:
            self.log(message="System is in Error state. Exiting script..", level='error')
            self.cli(command=self.cmd['show_chassis_fpc_pic_stt'])
            raise TobyException("System is in Error state. Aborting script..", host_obj=self)
        return True

    def function_name(self):
        '''
        To get the function name.
        
        ARGUMENTS:
            []
            :param:None
        
        ROBOT USAGE:
            Function Name

        :returns:
            The function name
        '''
        return traceback.extract_stack(None, 2)[0][2]

    def __config_build__(self, cmd):
        '''
            Add to a list of config commands to execute later
        :param cmd list
            The command list to push to the config list
        '''
        self.config_arr.extend(cmd)

    def __get_intf_nhid(self, fpcnum, nhindex, intf):
        '''
            Get NextHop id for specify interface with cprod cmd
        :param fpcnum
            REQUIRED fpc number for interface , e.g fpcnum5
        :param nhindex
            REQUIRED Nexthop index for interface , e.g 960
        :param intf
            REQUIRED interface name , e.g xe-4/0/3
        :return
            intf_nhid Nexthop id of interface
        '''
        # Try 10 time
        i = 1
        while i < 11:
            cprod_cmd = self.cmd['cprod_show_nhdb'] % (fpcnum, nhindex) +\
                "|grep %s" % intf
            self.shell(command='start shell')
            crop = self.shell(command=cprod_cmd)
            res = crop.response()
            self.__verify_cprod_response(res)

            # Parse and get the Next-Hop Id, Inner Next Hop Id,
            # ingress nhid and egress nhid
            lines = res.split("\n")
            nh_ids = []
            for line in lines:
                check = re.match(r"\s*(\d+)\(", line)
                if check:
                    nh_ids.append(check.group(1))
            try:
                intf_nhid = nh_ids[0]
                return intf_nhid
            except IndexError:
                self.log(
                    message="Could not able to retrieve nhid for %s" % intf +
                    " Sleeping for 5s before retrying again...")
                time.sleep(5)
            i += 1

        self.log(
            message="Unable to get nhid for %s. Hence " % intf +
            "aborting the script", level='info')
        result = self.__get_interface_status(intf)
        self.log(
            message="!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" +
            "!!\n%s\n!!!!!!!!!!!!!!!!!!" % result +
            "!!!!!!!!!!!!!!!!!!!!!!!!!", level='error')
        raise TobyException("Unable to get nhid for %s. " % intf + "  Aborting the script", host_obj=self)

    def set_jpg_interfaces(self, intf):
        '''
        This function used to set jpg interfaces

        ARGUMENTS:
            :param STR intf: intf name

        ROBOT USAGE:
            set jpg interfaces    intf=ge 1/0/9

        :returns: True if set sucessfully
        '''
        self.interfaces = intf

    def reset_jpg_config(self):
        '''
        This function use to reset jpg configuration on JPG device

        ARGUMENTS:
            :param: None

        ROBOT USAGE:
            Reset jpg Config

        :returns: True if reset sucessfully
        '''
        self.__get_ingress_egress_interfaces()
        self.log(message="inout_intf_pair : %s" % self.inout_intf_pair,
                 level='info')
        result = True
        if len(self.inout_intf_pair) > 0:
            result = self.__reset_jpg_config()
        return result


def connect_to_jpg_device(*args, **kwargs):
    '''
    connect jpg to the device

    ARGUMENTS:
        :param STR host:
            *OPTIONAL* Host name.
        :param STR os:
            *OPTIONAL* os name of the device.
        :param STR model:
            *OPTIONAL* model name of the deivce.

    ROBOT USAGE:
        ${device_handle} = Connect To Jpg Device    host='10.207.148.72'    os='JUNOS'    model='Jpg'

    :return : return the jpg device object
    '''
    return Jpg(*args, **kwargs)


def set_jpg_interfaces(dev, interfaces):
    '''
    Set interafaces of the JPG

    ARGUMENTS:
        [dev, interfaces]
        :param OBJECT dev:
            *REQUIRED* Device handle 
        :param STR interfaces:
            *REQUIRED* interface name

    ROBOT USAGE:
        ${junos_dev} =    Get Handle   resource=device0
        Set Jpg Interfaces     dev=${junos_dev.current_node.current_controller}    interfaces=${t['resources']['device0']['interfaces']}

    :return:None
    '''
    dev.current_node.current_controller.set_jpg_interfaces(interfaces)


def configure_jpg(dev):
    '''
    configure the JPG 

    ARGUMENTS:
        [dev]
        :param OBJECT dev:
            *REQUIRED* Device handle 

    ROBOT USAGE:
        ${junos_dev} =    Get Handle   resource=device0
        ${junos_dev.current_node.current_controller.interfaces} =    Set To Dictionary   
                    ............        ${t['resources']['device0']['interfaces']}
        ${result} =    Configure Jpg    dev=${junos_dev.current_node.current_controller}

    :return:None

    '''
    result = dev.configure_jpg()
    if not result:
        raise TobyException('Cannot configure Jpg')
    return result


def configure_jpg_replication(devices):
    '''
    Configure the JPG replications

    ARGUMENTS:
        [devices]
        :param LIST devices:
            *REQUIRED* devices name

    ROBOT USAGE:
        ${junos_dev} =    Get Handle   resource=device0
        ${junos_dev.current_node.current_controller.interfaces} =    Set To Dictionary    
                    ...                 ${t['resources']['device0']['interfaces']}
        ${jpg_devices_list} =    Create List     ${junos_dev.current_node.current_controller}
        ${result} =    Configure Jpg Replication    devices=${jpg_devices_list}

    return: returns the configure replication devices else
        raise an exception 
    '''
    try:
        result = Jpg.jpg_replication(devices)
    except Exception:
        raise TobyException('Cannot configure Jpg replication on devices')
    return result


def setup_jpg_filter(dev, **kwargs):
    '''
    Create a list of command for configuring JPG filter

    ARGUMENTS:
        [kwargs]
        :param STR filter:
            *REQUIRED*  filter name for command ,e.g : ctrl_input_dut_1
        :param STR term_name:
            *REQUIRED*  term name for command, e.g : ipterm
        :param STR port_name:
            *REQUIRED*  port name for command, e.g : ge-9/0/0
        :param STR ip_src:
            *OPTIONAL*  IP source for command, e.g : 1.1.1.0
        :param STR ip_dst:
            *OPTIONAL*  IP destination for command, e.g : 1.1.1.1
        :param STR prefix_list:
            *OPTIONAL*  Prefix list for command, e.g : filter
        :param INT vlan_id:
            *OPTIONAL*  Vlan ID for command, e.g : 10
        :param INT vlan_pri:
            *OPTIONAL*  Vlan priority for command, e.g : 1
        :param INT ether_type:
            *OPTIONAL*  Ethernet type for command, e.g : 1
        :param INT ip_precedence:
            *OPTIONAL*  IP precedence for command, e.g : 7
        :param INT single_term:
            *OPTIONAL*  Single term for command, e.g : 1
        :param INT vlan_id_count:
            *OPTIONAL*  Vlan ID count for command, e.g : 5
        :param INT vlan_id_step:
            *OPTIONAL*  Vlan ID step for command, e.g : 2
        :param INT source_port:
            *OPTIONAL*  Source port for command, e.g : http
        :param INT dest_port:
            *OPTIONAL*  Dest port for command, e.g : https
        :param INT src_mod:
            *OPTIONAL*  Source mode for command, e.g : 1
        :param INT src_num_addr:
            *OPTIONAL*  Source number address for command, e.g : 2
        :param INT src_mask:
            *OPTIONAL*  Source mask for command, e.g : 24
        :param INT dst_mod:
            *OPTIONAL*  Dest mode for command, e.g : 1
        :param INT dst_num_addr:
            *OPTIONAL*  Dest number address for command, e.g : 2
        :param INT dst_mask:
            *OPTIONAL*  Dest mask for command, e.g : 24
        :param INT step:
            *OPTIONAL*  Step for command, e.g : 2
        :param STR mac_src:
            *OPTIONAL*  MAC source for command, e.g : 00:00:00:11:00:11
        :param INT mac_dst:
            *OPTIONAL*  MAC destination for command, e.g : 00:00:00:11:00:12
        
 


    ROBOT USAGE:
        EX 1: ${junos_dev} =    Get Handle   resource=device0
            ${kwargs} =    Evaluate    {'filter': 'ctrl_input_dut_1', 'term_name': 'ipterm',
            ... 'port_name': 'ge-9/0/0', 'ip_src': '1.1.1.0', 'ip_dst': '1.1.1.1',
            ... 'prefix_list': '', 'vlan_id': '10', 'vlan_pri': '1', 'ether_type': '1',
            ... 'ip_precedence': '7', 'single_term': '1', 'vlan_id_count': '5', 'vlan_id_step': '2',
            ... 'source_port': '80', 'dest_port': '90', 'src_mod': '1', 'src_num_addr': '2',
            ... 'src_mask': '24', 'dst_mod': '1', 'dst_num_addr': '2', 'dst_mask': '24', 'step': '2',
            ... 'mac_src': '00:00:00:11:00:11', 'mac_dst': '00:00:00:11:00:12'}
            ${result} =    Setup Jpg Filter    ${junos_dev.current_node.current_controller}    &{kwargs}

        Ex 2:setup jpg filter    filter=ctrl_input_dut_1   term_name=ipterm    
                        ...     port_name=ge-9/0/0 

    :returns: append all commands to global lists "term_array"
                and "jpg_config"                         

    '''
    result = dev.setup_jpg_filter(**kwargs)
    if not result:
        raise TobyException('Cannot setup Jpg filter')
    return result


def attach_jpg_filter(dev):
    '''
    attach the jpg filter on device

    ARGUMENTS:
        [dev]
        :param Object dev:
            *REQUIRED* device handle

    ROBOT USAGE:
        ${junos_dev} =    Get Handle   resource=device0
        ${result} =    Attach Jpg Filter    dev=${junos_dev.current_node.current_controller}

    :return:Trur else raise an exception
    '''
    result = dev.attach_jpg_filter()
    if not result:
        raise TobyException('Cannot attach Jpg filter')
    return result


def get_jpg_stats(dev):
    '''
    Gives the current state of the JPG

    ARGUMENTS:
        [dev]
        :param Object dev:
            *REQUIRED* device handle

    ROBOT USAGE:
        ${junos_dev} =    Get Handle   resource=device0
        ${stat} =    Get Jpg Stats    ${junos_dev.current_node.current_controller}

    :return: retuen TRUE or False else raise an excption
    '''
    result = dev.get_jpg_stats()
    if not result:
        raise TobyException('Cannot get Jpg statistics')
    return result

