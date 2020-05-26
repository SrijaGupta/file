#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Userfw SRX keywords
Author: Wentao Wu, wtwu@juniper.net
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
import re
import ipaddress


class common_srx(object):
    """
    Description: Common SRX keywords

    keywords list:
    * clear_srx_security_pki_local_certificate
    * config_srx_security_pki_local_certificate
    * config_srx_system_login
    * delete_srx_system_login
    * config_srx_system_process_multitenancy
    * delete_srx_system_process_multitenancy
    * config_srx_lsys0
    * delete_srx_lsys0
    * config_srx_interface_ip_address
    * config_srx_static_route
    * delete_srx_static_route
    * config_srx_system_security_profile
    * delete_srx_system_security_profile
    * check_srx_system_license
    * check_srx_system_process_multitenancy
    """

    def __init__(self, device=None):
        """
        device handle
        """
        self.device = device
        self.commit_timeout = 150
        self.cli_timeout = 60

    def clear_srx_security_pki_local_certificate(self, device=None, file='cert_file'):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param file:
        *OPTIONAL* file name

        """

        if device is None:
            raise Exception("device handle is None")

        prefix = 'clear security pki '

        device.cli(command=prefix + 'local-certificate certificate-id ' + file, timeout=self.cli_timeout)
        device.cli(command=prefix + 'key-pair certificate-id ' + file, timeout=self.cli_timeout)

        return True

    def config_srx_security_pki_local_certificate(self, device=None, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str file:
        *OPTIONAL* file

        :param str size:
        *OPTIONAL* size

        :param str domain:
        *OPTIONAL* domain

        :param str email:
        *OPTIONAL* email

        :param str ip:
        *OPTIONAL* ip

        :param str subject:
        *OPTIONAL* subject

        """

        file = kwargs.get("file", 'cert_file')
        size = kwargs.get("size", 1024)
        domain = kwargs.get("domain", 'juniper.net')
        email = kwargs.get("email", 'engineer@juniper.net')
        ip = kwargs.get("ip", '1.1.1.1')
        subject = kwargs.get("subject", '"CN=John Doe,OU=Sales,O=Juniper Networks,L=Sunnyvale,ST=CA,C=US"')

        if device is None:
            raise Exception("device handle is None")

        prefix = 'request security pki '

        response = device.cli(command=prefix + 'generate-key-pair certificate-id ' + file + ' size ' + str(size), timeout=self.cli_timeout).response()
        if re.search(r"Generated\s*key\s*pair\s*{}".format(file), response, re.M) is None:
            raise Exception("------generate key pair failed!------\n")

        response = device.cli(command=prefix + 'local-certificate generate-self-signed certificate-id ' + file + ' domain-name ' + domain + ' email ' + email + ' ip-address ' + ip + ' subject ' + subject, timeout=self.cli_timeout).response()
        if re.search(r'Self-signed certificate generated and loaded successfully', response, re.M) is None:
            raise Exception("------generate self signed certificate id failed!------\n")

        return True

    def config_srx_system_login(self, device=None, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str flag:
        *OPTIONAL* login flag value [class | user]

        :param str class_name:
        *OPTIONAL* class name

        :param str logical_system:
        *OPTIONAL* logical system name

        :param str permissions:
        *OPTIONAL* permissions name

        :param str user:
        *OPTIONAL* user name

        :param str full_name:
        *OPTIONAL* full name

        :param str uid:
        *OPTIONAL* uid value

        :param str password:
        *OPTIONAL* password value

        """
        flag = kwargs.get("flag")
        class_name = kwargs.get("class_name", "LDclass1")
        logical_system = kwargs.get("logical_system", "LD1")
        permissions = kwargs.get("permissions", "all")
        user = kwargs.get("user", "LD1user")
        full_name = kwargs.get("full_name", "LD1user")
        uid = kwargs.get("uid", "1000")
        password = kwargs.get("password", "Embe1mpls")

        if device is None:
            raise Exception("device handle is None")

        if int(uid) < 99 or int(uid) > 64000:
            raise Exception("------uid is unexcepted value!------\n")

        commands = []
        prefix = 'set system login '

        if flag == 'class':
            commands.append(prefix + 'class ' + class_name + ' logical-system ' + logical_system)
            commands.append(prefix + 'class ' + class_name + ' permissions ' + permissions)
        elif flag == 'user':
            commands.append(prefix + 'user ' + user + ' full-name ' + full_name)
            commands.append(prefix + 'user ' + user + ' uid ' + uid)
            commands.append(prefix + 'user ' + user + ' class ' + class_name)
            commands.append(prefix + 'user ' + user + ' authentication plain-text-password')
        else:
            commands.append(prefix + 'class ' + class_name + ' logical-system ' + logical_system)
            commands.append(prefix + 'class ' + class_name + ' permissions ' + permissions)
            commands.append(prefix + 'user ' + user + ' full-name ' + full_name)
            commands.append(prefix + 'user ' + user + ' uid ' + uid)
            commands.append(prefix + 'user ' + user + ' class ' + class_name)
            commands.append(prefix + 'user ' + user + ' authentication plain-text-password')

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)

        if flag == 'class':
            response = device.config(command_list=commands).response()
        else:
            device.config(command_list=commands, pattern='New password:')
            pwd = [password]
            response = device.config(command_list=pwd, pattern='Retype new password:').response()
            if re.search('error', response):
                raise Exception("------password doesn't satisfy specific rule!------\n")
            response = device.config(command_list=pwd).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def delete_srx_system_login(self, device=None, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str class_name:
        *OPTIONAL* class name

        :param str logical_system:
        *OPTIONAL* logical system name

        :param str permissions:
        *OPTIONAL* permissions name

        :param str user:
        *OPTIONAL* user name

        :param str full_name:
        *OPTIONAL* full name

        :param str uid:
        *OPTIONAL* uid value

        """
        class_name = kwargs.get("class_name")
        logical_system = kwargs.get("logical_system")
        permissions = kwargs.get("permissions")
        user = kwargs.get("user")
        full_name = kwargs.get("full_name")
        uid = kwargs.get("uid")

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'delete system login '

        if class_name is not None:
            if user is not None:
                commands.append(prefix + 'user ' + user + ' class ' + class_name)
            elif logical_system is not None:
                commands.append(prefix + 'class ' + class_name + ' logical-system ' + logical_system)
            elif permissions is not None:
                commands.append(prefix + 'class ' + class_name + ' permissions ' + permissions)
            else:
                commands.append(prefix + 'class ' + class_name)
        elif user is not None:
            if full_name is not None:
                commands.append(prefix + 'user ' + user + ' full-name ' + full_name)
            elif uid is not None:
                commands.append(prefix + 'user ' + user + ' uid ' + uid)
            else:
                commands.append(prefix + 'user ' + user)
        else:
            commands.append(prefix)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        response = device.config(command_list=commands).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def config_srx_system_process_multitenancy(self, device=None, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str mode:
        *OPTIONAL* mode value

        """
        mode = kwargs.get("mode", "logical-domain")

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'set system process multitenancy mode '

        commands.append(prefix + mode)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        response = device.config(command_list=commands).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def delete_srx_system_process_multitenancy(self, device=None, commit=False):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str mode:
        *OPTIONAL* mode value

        """

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'delete system process multitenancy mode '

        commands.append(prefix)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        response = device.config(command_list=commands).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def config_srx_lsys0(self, device=None, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str flag:
        *OPTIONAL* lsys0 flag value [interfaces | instances]

        :param str interfaces:
        *OPTIONAL* logical interface name

        :param str unit:
        *OPTIONAL* unit name

        :param str peer_unit:
        *OPTIONAL* peer unit name

        :param str routing_instances:
        *OPTIONAL* routing instances name

        """
        flag = kwargs.get("flag")
        interfaces = kwargs.get("interfaces", "lt-0/0/0")
        unit = kwargs.get("unit", "11")
        peer_unit = kwargs.get("peer_unit", "10")
        routing_instances = kwargs.get("routing_instances", "vr0")

        if device is None:
            raise Exception("device handle is None")

        if int(unit) == int(peer_unit):
            raise Exception("unit and peer_unit shouldn't be equal")

        commands = []
        prefix = 'set logical-systems lsys0 '

        if flag == 'interfaces':
            commands.append(prefix + 'interfaces ' + interfaces + ' unit ' + unit + ' encapsulation ethernet-vpls')
            commands.append(prefix + 'interfaces ' + interfaces + ' unit ' + unit + ' peer-unit ' + peer_unit)
        elif flag == 'instances':
            commands.append(prefix + 'routing-instances ' + routing_instances + ' instance-type vpls')
            commands.append(prefix + 'routing-instances ' + routing_instances + ' interface ' + interfaces + '.' + unit)
        else:
            commands.append(prefix + 'interfaces ' + interfaces + ' unit ' + unit + ' encapsulation ethernet-vpls')
            commands.append(prefix + 'interfaces ' + interfaces + ' unit ' + unit + ' peer-unit ' + peer_unit)
            commands.append(prefix + 'routing-instances ' + routing_instances + ' instance-type vpls')
            commands.append(prefix + 'routing-instances ' + routing_instances + ' interface ' + interfaces + '.' + unit)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        response = device.config(command_list=commands).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def delete_srx_lsys0(self, device=None, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str interfaces:
        *OPTIONAL* logical interface name

        :param str unit:
        *OPTIONAL* unit name

        :param str peer_unit:
        *OPTIONAL* peer unit name

        :param str routing_instances:
        *OPTIONAL* routing instances name

        """

        interfaces = kwargs.get("interfaces")
        unit = kwargs.get("unit")
        peer_unit = kwargs.get("peer_unit")
        routing_instances = kwargs.get("routing_instances")

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'delete logical-systems lsys0 '

        if interfaces is not None:
            if routing_instances is not None and unit is not None:
                commands.append(prefix + 'routing-instances ' + routing_instances + ' interface ' + interfaces + '.' + unit)
            elif peer_unit is not None and unit is not None:
                commands.append(prefix + 'interfaces ' + interfaces + ' unit ' + unit + ' peer-unit ' + peer_unit)
            elif unit is not None:
                commands.append(prefix + 'interfaces ' + interfaces + ' unit ' + unit)
            else:
                commands.append(prefix + 'interfaces ' + interfaces)
        elif routing_instances is not None:
            commands.append(prefix + 'routing-instances ' + routing_instances)
        else:
            commands.append(prefix)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        response = device.config(command_list=commands).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def config_srx_interface_ip_address(self, device=None, interface=None, unit=0, ip=None, mask=24, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str interface:
        *OPTIONAL* logical interface name

        :param str unit:
        *OPTIONAL* unit name

        :param str ip:
        *OPTIONAL* ip address

        :param str mask:
        *OPTIONAL* mask value

        :param str web_authentication:
        *OPTIONAL* web authentication [http | https | redirect-to-https]

        :param str inet:
        *OPTIONAL* inet value

        :param str logical_systems:
        *OPTIONAL* logical systems name

        :param str peer_unit:
        *OPTIONAL* peer unit name

        """

        web_authentication = kwargs.get("web_authentication")
        inet = kwargs.get("inet", "inet")
        logical_systems = kwargs.get("logical_systems")
        peer_unit = kwargs.get("peer_unit")

        if device is None:
            raise Exception("device handle is None")

        commands = []

        if logical_systems is not None:
            prefix = 'set logical-systems ' + logical_systems + ' interfaces ' + interface
        else:
            prefix = 'set interfaces ' + interface

        if peer_unit is not None:
            commands.append(prefix + ' unit ' + str(unit) + ' encapsulation ethernet')
            commands.append(prefix + ' unit ' + str(unit) + ' peer-unit ' + peer_unit)

            if ip is not None:
                commands.append(prefix + ' unit ' + str(unit) + ' family ' + inet + ' address ' + ip + '/' + str(mask))

        elif web_authentication is not None:
            commands.append(prefix + ' unit ' + str(unit) + ' family ' + inet + ' address ' + ip + '/' + str(mask) + ' web-authentication ' + web_authentication)
        else:
            commands.append(prefix + ' unit ' + str(unit) + ' family ' + inet + ' address ' + ip + '/' + str(mask))

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        response = device.config(command_list=commands).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def config_srx_static_route(self, device=None, subnet=None, mask=24, nexthop=None, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str subnet:
        *OPTIONAL* subnet

        :param str mask:
        *OPTIONAL* mask value

        :param str nexthop:
        *OPTIONAL* nexthop

        :param str logical_systems:
        *OPTIONAL* logical systems name

        """

        logical_systems = kwargs.get("logical_systems")

        if device is None:
            raise Exception("device handle is None")

        commands = []

        if logical_systems is not None:
            prefix = 'set logical-systems ' + logical_systems + ' routing-options '
        else:
            prefix = 'set routing-options '

        if ipaddress.ip_address(subnet).version == 4 and ipaddress.ip_address(nexthop).version == 4:
            commands.append(prefix + 'static route ' + subnet + '/' + str(mask) + ' next-hop ' + nexthop)
        elif ipaddress.ip_address(subnet).version == 6 and ipaddress.ip_address(nexthop).version == 6:
            commands.append(prefix + 'rib inet6.0 static route ' + subnet + '/' + str(mask) + ' next-hop ' + nexthop)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        response = device.config(command_list=commands).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def delete_srx_static_route(self, device=None, subnet=None, mask=24, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str subnet:
        *OPTIONAL* subnet

        :param str mask:
        *OPTIONAL* mask value

        :param str logical_systems:
        *OPTIONAL* logical systems name

        :param str flag:
        *OPTIONAL* flag    [ipv4 | ipv6]

        """

        logical_systems = kwargs.get("logical_systems")
        flag = kwargs.get("flag")

        if device is None:
            raise Exception("device handle is None")

        commands = []

        if logical_systems is not None:
            prefix = 'delete logical-systems ' + logical_systems + ' routing-options '
        else:
            prefix = 'delete routing-options '

        if subnet is not None:
            if ipaddress.ip_address(subnet).version == 4:
                commands.append(prefix + 'static route ' + subnet + '/' + str(mask))
            elif ipaddress.ip_address(subnet).version == 6:
                commands.append(prefix + 'rib inet6.0 static route ' + subnet + '/' + str(mask))
        else:
            if flag == 'ipv4':
                commands.append(prefix + 'static')
            elif flag == 'ipv6':
                commands.append(prefix + 'rib inet6.0 static')
            else:
                commands.append(prefix)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        response = device.config(command_list=commands).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def config_srx_system_security_profile(self, device=None, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str security_profile:
        *OPTIONAL* security profile

        :param str logical_systems:
        *OPTIONAL* logical systems name

        :param str logical_systems_number:
        *OPTIONAL* logical systems number

        """

        security_profile = kwargs.get("security_profile", "ld_profile")
        logical_systems = kwargs.get("logical_systems")
        logical_systems_number = kwargs.get("logical_systems_number", '1')

        authentry_maximum = kwargs.get("authentry_maximum", '100')
        authentry_reserved = kwargs.get("authentry_reserved", '50')
        policy_maximum = kwargs.get("policy_maximum", '100')
        policy_reserved = kwargs.get("policy_reserved", '50')
        scheduler_maximum = kwargs.get("scheduler_maximum", '64')
        zone_maximum = kwargs.get("zone_maximum", '100')
        zone_reserved = kwargs.get("zone_reserved", '50')
        flow_session_reserved = kwargs.get("flow_session_reserved", '50')
        flow_gate_maximum = kwargs.get("flow_gate_maximum", '2048')
        flow_gate_reserved = kwargs.get("flow_gate_reserved", '50')
        nat_source_pool_maximum = kwargs.get("nat_source_pool_maximum", '100')
        nat_source_pool_reserved = kwargs.get("nat_source_pool_reserved", '50')
        nat_destination_pool_maximum = kwargs.get("nat_destination_pool_maximum", '100')
        nat_destination_pool_reserved = kwargs.get("nat_destination_pool_reserved", '50')
        nat_destination_pool_maximum = kwargs.get("nat_destination_pool_maximum", '100')
        nat_destination_pool_reserved = kwargs.get("nat_destination_pool_reserved", '50')
        nat_pat_address_maximum = kwargs.get("nat_pat_address_maximum", '100')
        nat_pat_address_reserved = kwargs.get("nat_pat_address_reserved", '50')
        nat_nopat_address_maximum = kwargs.get("nat_nopat_address_maximum", '100')
        nat_nopat_address_reserved = kwargs.get("nat_nopat_address_reserved", '50')
        nat_source_rule_maximum = kwargs.get("nat_source_rule_maximum", '100')
        nat_source_rule_reserved = kwargs.get("nat_source_rule_reserved", '50')
        nat_destination_rule_maximum = kwargs.get("nat_destination_rule_maximum", '100')
        nat_destination_rule_reserved = kwargs.get("nat_destination_rule_reserved", '50')
        nat_static_rule_maximum = kwargs.get("nat_static_rule_maximum", '10')
        nat_rule_referenced_prefix_maximum = kwargs.get("nat_rule_referenced_prefix_maximum", '100')
        nat_rule_referenced_prefix_reserved = kwargs.get("nat_rule_referenced_prefix_reserved", '50')
        nat_rule_referenced_prefix_maximum = kwargs.get("nat_rule_referenced_prefix_maximum", '100')
        nat_cone_binding_reserved = kwargs.get("nat_cone_binding_reserved", '50')

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'set system security-profile ' + security_profile

        if logical_systems is not None:
            if int(logical_systems_number) == 1:
                commands.append(prefix + ' logical-system ' + logical_systems)
            else:
                for i in range(1, int(logical_systems_number)):
                    commands.append(prefix + ' logical-system ' + logical_systems + str(i))
        else:
            commands.append(prefix + ' auth-entry maximum ' + str(authentry_maximum))
            commands.append(prefix + ' auth-entry reserved ' + str(authentry_reserved))
            commands.append(prefix + ' policy maximum ' + str(policy_maximum))
            commands.append(prefix + ' policy reserved ' + str(policy_reserved))
            commands.append(prefix + ' scheduler maximum ' + str(scheduler_maximum))
            commands.append(prefix + ' zone maximum ' + str(zone_maximum))
            commands.append(prefix + ' zone reserved ' + str(zone_reserved))
            commands.append(prefix + ' flow-session reserved ' + str(flow_session_reserved))
            commands.append(prefix + ' flow-gate maximum ' + str(flow_gate_maximum))
            commands.append(prefix + ' flow-gate reserved ' + str(flow_gate_reserved))
            commands.append(prefix + ' nat-source-pool maximum ' + str(nat_source_pool_maximum))
            commands.append(prefix + ' nat-source-pool reserved ' + str(nat_source_pool_reserved))
            commands.append(prefix + ' nat-destination-pool maximum ' + str(nat_destination_pool_maximum))
            commands.append(prefix + ' nat-destination-pool reserved ' + str(nat_destination_pool_reserved))
            commands.append(prefix + ' nat-pat-address maximum ' + str(nat_pat_address_maximum))
            commands.append(prefix + ' nat-pat-address reserved ' + str(nat_pat_address_reserved))
            commands.append(prefix + ' nat-nopat-address maximum ' + str(nat_nopat_address_maximum))
            commands.append(prefix + ' nat-nopat-address reserved ' + str(nat_nopat_address_reserved))
            commands.append(prefix + ' nat-source-rule maximum ' + str(nat_source_rule_maximum))
            commands.append(prefix + ' nat-source-rule reserved ' + str(nat_source_rule_reserved))
            commands.append(prefix + ' nat-destination-rule maximum ' + str(nat_destination_rule_maximum))
            commands.append(prefix + ' nat-destination-rule reserved ' + str(nat_destination_rule_reserved))
            commands.append(prefix + ' nat-static-rule maximum ' + str(nat_static_rule_maximum))
            commands.append(prefix + ' nat-rule-referenced-prefix maximum ' + str(nat_rule_referenced_prefix_maximum))
            commands.append(prefix + ' nat-rule-referenced-prefix reserved ' + str(nat_rule_referenced_prefix_reserved))
            commands.append(prefix + ' nat-cone-binding maximum ' + str(nat_rule_referenced_prefix_maximum))
            commands.append(prefix + ' nat-cone-binding reserved ' + str(nat_cone_binding_reserved))

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        response = device.config(command_list=commands).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def delete_srx_system_security_profile(self, device=None, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str security_profile:
        *OPTIONAL* security profile

        :param str logical_systems:
        *OPTIONAL* logical systems name

        :param str logical_systems_number:
        *OPTIONAL* logical systems number

        """

        security_profile = kwargs.get("security_profile")
        logical_systems = kwargs.get("logical_systems")

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'delete system security-profile '

        if security_profile is not None:
            if logical_systems is not None:
                commands.append(prefix + security_profile + ' logical-system ' + logical_systems)
            else:
                commands.append(prefix + security_profile)
        else:
            commands.append(prefix)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        response = device.config(command_list=commands).response()

        if commit:
            response = device.commit(timeout=self.commit_timeout)
        return response

    def check_srx_system_license(self, device=None, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str feature_name:
        *OPTIONAL* feature name

        :param int licenses_installed:
        *OPTIONAL* input licenses installed number

        """

        feature_name = kwargs.get("feature_name")
        licenses_installed = kwargs.get("licenses_installed", 3)

        if device is None:
            raise Exception("device handle is None")

        if feature_name is None:
            raise Exception("please input the feature name of needing to be checked!")

        response = device.cli(command='show system license', timeout=self.cli_timeout).response()

        result = re.search(r"{}\s+\d+\s+(\d+)\s+\d+\s+(.*?)[\r\n]".format(feature_name), response, re.S)
        get_licenses_installed = result.group(1)
        get_expiry = result.group(2)
        device.log(level='DEBUG', message="licenses installed number is {}".format(get_licenses_installed))
        device.log(level='DEBUG', message="get expiry vaule is {}".format(get_expiry))

        if int(get_licenses_installed) < int(licenses_installed):
            raise Exception("needed licenses installed number is less than get licenses installed number, this's unexpected!")

        if 'invalid' in get_expiry:
            raise Exception("licenses doesn't work, please check it!")
        else:
            device.log(level='DEBUG', message='check licenses is successful')
            return True

    def check_srx_system_processes_multitenancy(self, device=None, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param int mode:
        *OPTIONAL* current lsys mode

        """

        mode = kwargs.get("mode", 'logical-domain')

        if device is None:
            raise Exception("device handle is None")

        response = device.cli(command='show system processes multitenancy', timeout=self.cli_timeout).response()

        result = re.search(r"mode:\s+(.*?)\s+", response, re.S)
        get_mode = result.group(1)
        device.log(level='DEBUG', message="get mode vaule is {}".format(get_mode))

        if mode == get_mode:
            return True
        device.log(level='INFO', message='need to reboot SRX')
        return False
