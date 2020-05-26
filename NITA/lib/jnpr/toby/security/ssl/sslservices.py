#!/usr/bin/python3
"""
#  DESCRIPTION:  SSL Services configuration APIs
#  AUTHOR:  Thyagarajan S Pasupathy (), thyag@juniper.net
#  Note: Methods should not be used directly in robot, but from equivalent wrapper python/robot file
"""
import re
import time

class SslServices():
    """
    Class for SSL Services configuration APIs (SSL-FP, SSL-SP, SSL-Initiation and SSL-Terminate)
    Note: Methods should not be used directly in robot, but from equivalent wrapper python/robot
    file
    """

    def __init__(self, srx):
        """
        Base class for ssl services Module
        :param srx:
         **REQUIRED** Srx Object
        :type srx: Device
        """
        if srx is None:
            raise ValueError("Device handle srx is REQUIRED argument")
        else:
            self.device = srx

    def get_ssl_statistics(self, node="local", pic=None):
        """
        Keyword to fetch ssl proxy statistics
        Example :-
            get_ssl_statistics( )
            get_ssl_statistics( node="node0")
            get_ssl_statistics( pic="fpc1 pic1")

        :param str node:
            *OPTIONAL*  HA node selection
                ``Supported values``: node0 or node1
                ``Default value``   : local
        :param str pic:
            *OPTIONAL* Pass pic value to fetch details for the respective pic alone
                ``Supported values``: "fpc1 pic0", "fpc2 pic1" etc as per requirement
        :return: Returns the dict object with values of each of the counters from statistics output
        :rtype: dict
        """
        values = {'matched': 0, 'whitelisted': 0, 'whitelisted url category match': 0, \
                  'bypassed:non-ssl': 0, 'bypassed:mem overflow': \
                      0, 'created': 0, 'ignored': 0, 'active': 0, 'dropped': 0, \
                  'bypassed:low memory': 0, 'default profile hit': 0,        \
                  'session dropped no default profile': 0, \
                  'policy hit no profile configured': 0}

        cmd = "show services ssl proxy statistics"
        proxy_statistics = self.device.cli(command=cmd)
        proxy_statistics = proxy_statistics.response()
        pic_op = []
        if pic is None:
            pic_op = re.split('PIC', proxy_statistics)
        else:
            fpc_pic = re.search(r'fpc([0-9]+)\s+pic([0-9]+)', pic)
            fpc = fpc_pic.group(1)
            pic = fpc_pic.group(2)
            pic_match = re.search(
                r'PIC:.{4,5}\s+fpc\[%s\]\s+pic\[%s\]\s+-+\s+(sessions\s+'
                r'matched\s+[0-9]+\s+sessions'
                r'\s+bypassed:non-ssl\s+[0-9]+\s+sessions\s+bypassed:mem\s+overflow\s+[0-9]+\s+'
                r'sessions\s+bypassed:low\s+memory\s+[0-9]+\s+sessions\s+created\s+[0-9]+\s+'
                r'sessions\s+ignored\s+[0-9]+\s+sessions\s+active\s+[0-9]+\s+sessions\s+'
                r'dropped\s+[0-9]+\s+sessions\s+whitelisted\s+[0-9]+\s+'
                r'\s+whitelisted\s+url\s+category\s+match\s+[0-9]+\s+default\s+profile\s+hit\s+[0-9]+\s+'
                r'session\s+dropped\s+no\s+default\s+profile\s+[0-9]+\s+'
                r'policy\s+hit\s+no\s+profile\s+configured\s+[0-9]+)'  % (fpc, pic),
                str(proxy_statistics))
            pic_op.append(pic_match.group(1))

        for line in pic_op:
            for stat in ['matched', 'whitelisted', 'whitelisted url category match', \
                         'bypassed:non-ssl', 'bypassed:mem overflow', \
                         'created', 'ignored', 'active', 'dropped', 'bypassed:low memory', \
                         'default profile hit', 'session dropped no default profile', \
                         'policy hit no profile configured']:
                if stat not in ['whitelisted url category match', 'default profile hit', \
                                'session dropped no default profile', 'policy hit no profile configured']:
                    match = re.search(r'sessions\s+%s\s+([0-9]+)' % stat, str(line))
                else:
                    match = re.search(r'%s\s+([0-9]+)' % stat, str(line))
                if match is not None:
                    values[stat] = int(match.group(1)) + int(values[stat])
        """
        # will be uncommented with PR View PR 1278760 is fixed

        proxy_statistics_xml = self.device.execute_as_rpc_command(command= 'show services '
                                                                           'ssl proxy statistics', \
                                                                  node=node)
        if "output" in proxy_statistics_xml.keys():
            proxy_statistics = proxy_statistics_xml['output']
            pic_op = []
            if pic is None:
                pic_op = re.split('PIC', proxy_statistics)
            else:
                fpc_pic = re.search(r'fpc([0-9]+)\s+pic([0-9]+)', pic)
                fpc = fpc_pic.group(1)
                pic = fpc_pic.group(2)
                pic_match = re.search(
                    r'PIC:.{4,5}\s+fpc\[%s\]\s+pic\[%s\]\s+-+\s+(sessions\s+'
                    r'matched\s+[0-9]+\s+sessions'
                    r'\s+bypassed:non-ssl\s+[0-9]+\s+sessions\s+bypassed:mem\s+overflow\s+[0-9]+\s+'
                    r'sessions\s+bypassed:low\s+memory\s+[0-9]+\s+sessions\s+created\s+[0-9]+\s+'
                    r'sessions\s+ignored\s+[0-9]+\s+sessions\s+active\s+[0-9]+\s+sessions\s+'
                    r'dropped\s+[0-9]+\s+sessions\s+whitelisted\s+[0-9]+\s+'
                    r'whitelisted\s+url\s+category'
                    r'\s+match\s+[0-9]+)' % (fpc, pic), \
                    str(proxy_statistics))
                pic_op.append(pic_match.group(1))

            for line in pic_op:
                for stat in ['matched', 'whitelisted', 'whitelisted url category match', \
                             'bypassed:non-ssl', 'bypassed:mem overflow', \
                             'created', 'ignored', 'active', 'dropped', 'bypassed:low memory']:
                    if stat != "whitelisted url category match":
                        match = re.search(r'sessions\s+%s\s+([0-9]+)' % stat, str(line))
                    else:
                        match = re.search(r'%s\s+([0-9]+)' % stat, str(line))
                    if match is not None:
                        values[stat] = int(match.group(1)) + int(values[stat])
        elif "ssl-statistics" in proxy_statistics_xml.keys():
            perpic = False
            for x in proxy_statistics_xml["ssl-statistics"]["ssl-statistics"]:
                picvalue = proxy_statistics_xml["ssl-statistics"]["ssl-statistics"][
                    "ssl-statistics-pic-info"].replace("[", "").replace("]", "").strip().split()
                if pic is not None and picvalue[1] in pic and picvalue[2] in pic:
                    perpic = True
                elif pic is not None and picvalue[1] in pic and picvalue[2] in pic and \
                                perpic is True:
                    perpic = False
                    break

                if pic is None or perpic is True:
                    if 'matched' in x:
                        values['matched'] = int(proxy_statistics_xml
                                                ["ssl-statistics"]["ssl-statistics"]
                                                ["ssl-statistics-sessions-matched"]) + \
                                            int(values['matched'])
                    if 'non-ssl' in x:
                        values['bypassed:non-ssl'] = int(proxy_statistics_xml
                                                         ["ssl-statistics"]["ssl-statistics"]
                                                         ["ssl-statistics-sessions-bypassed-non-ssl"
                                                         ]) + int(values['bypassed:non-ssl'])
                    if 'overflow' in x:
                        values['bypassed:mem overflow'] = int(proxy_statistics_xml["ssl-statistics"]
                                                              ["ssl-statistics"]
                                                              ["ssl-statistics-sessions-bypassed-"
                                                               "mem-overflow"]) + int(
                            values['bypassed:mem overflow'])
                    if 'low memory' in x:
                        values['bypassed:low memory'] = int(
                            proxy_statistics_xml["ssl-statistics"]["ssl-statistics"][
                                "ssl-statistics-sessions-bypassed-low-memory"]) + int(
                            values['bypassed:low memory'])
                    if 'created' in x:
                        values['created'] = int(
                            proxy_statistics_xml["ssl-statistics"]["ssl-statistics"][
                                "ssl-statistics-sessions-created"]) + int(values['created'])
                    if 'ignored' in x:
                        values['ignored'] = int(
                            proxy_statistics_xml["ssl-statistics"]["ssl-statistics"][
                                "ssl-statistics-sessions-ignored"]) + int(values['ignored'])
                    if 'active' in x:
                        values['active'] = int(
                            proxy_statistics_xml["ssl-statistics"]["ssl-statistics"][
                                "ssl-statistics-sessions-active"]) + int(values['active'])
                    if 'dropped' in x:
                        values['dropped'] = int(
                            proxy_statistics_xml["ssl-statistics"]["ssl-statistics"][
                                "ssl-statistics-sessions-dropped"]) + int(values['dropped'])
                    if 'whitelisted' in x and 'url' not in x:
                        values['whitelisted'] = int(
                            proxy_statistics_xml["ssl-statistics"]["ssl-statistics"][
                                "ssl-statistics-sessions-whitelisted"]) + int(values['whitelisted'])
                    if 'url' in x:
                        values['whitelisted url category match'] = int(
                            proxy_statistics_xml["ssl-statistics"]["ssl-statistics"][
                                "ssl-statistics-whitelisted-url-category-match"]) + int(
                            values['whitelisted url category match'])
        """
        return values

    def clear_ssl_statistics(self, node="local"):
        """
        Keyword to clear ssl proxy statistics
        Example :-
            clear_ssl_statistics( )
            clear_ssl_statistics( node="node0")

        :param str node:
            *OPTIONAL*  HA node selection
                ``Supported values``: node0 or node1
                ``Default value``   : local
        :return: Returns "True"
        :rtype: bool
        """
        self.device.execute_as_rpc_command(command='clear services ssl proxy statistics', node=node)

        return True

    def conf_ssl_trace_options(self, **kwargs):
        """
        ssl proxy/init/terminate trace options configuration
        Example :-
            conf_ssl_trace_options( filename="ssl-userfile", maxfiles="10", size="100",
                                        worldreadable="yes",flag="cli-configuration",
                                        level="extensive", noremotetrace="yes")
            conf_ssl_trace_options( mode="delete", filename="ssl-userfile", maxfiles="10",
                                        size="100", worldreadable="yes", flag="cli-configuration",
                                         level="extensive", noremotetrace="yes")
            conf_ssl_trace_options()
            conf_ssl_trace_options( mode="delete")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str filename:
            *OPTIONAL* Name of the ssl traceoptions file to log traces
                ``Default value``   : ssl_trace
        :param int maxfiles:
            *OPTIONAL* Maximum no of trace files to be created on system
                ``Default value``   : 3
        :param int size:
            *OPTIONAL* Maximum size of the trace file
                ``Default value``   : 128000
        :param str worldreadable:
            *OPTIONAL* world-readable configuration
                ``Supported values``: true or false
        :param str flag:
            *OPTIONAL* Configure trace flag options
                ``Supported values``: all, cli-configuration, initiation, proxy,
                selected-profile or termination
        :param str level:
            *OPTIONAL* Configure trace level options
                ``Supported values``: brief, detail, extensive or verbose
                ``Default value``   : brief
        :param str noremotetrace:
            *OPTIONAL* Disable remote tracing
                ``Supported values``: yes or no
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()

        cfg_node = mode + ' services ssl traceoptions '
        cmdlist = []

        if mode == 'delete' and len(kwargs) == 1:
            cmdlist = [cfg_node]
        elif mode == 'set' and len(kwargs) == 0:
            cmdlist.append(cfg_node + 'file ssl_trace')
        else:
            worldreadable = kwargs.get('worldreadable', None)
            flag = kwargs.get('flag', None)

            if 'filename' in kwargs:
                cmdlist.append(cfg_node + 'file ' + kwargs.get('filename'))
            if  'maxfiles' in kwargs:
                cmdlist.append(cfg_node + 'file files ' + kwargs.get('maxfiles'))
            if 'size' in kwargs:
                cmdlist.append(cfg_node + 'file size ' + kwargs.get('size'))
            if 'level' in kwargs:
                cmdlist.append(cfg_node + 'level ' + kwargs.get('level'))
            if kwargs.get('worldreadable') is not None:
                if worldreadable == 'true':
                    cmdlist.append(cfg_node + 'file ' + 'world-readable')
                else:
                    cmdlist.append(cfg_node + 'file ' + 'no-world-readable')
            if kwargs.get('flag') is not None:
                cmdlist.append(cfg_node + 'flag ' + flag)
            if kwargs.get('noremotetrace') == 'yes':
                cmdlist.append(cfg_node + 'no-remote-trace')

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == 'yes' and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_cert_identifier(self, sslplugin="proxy", certidentifier=None, **kwargs):
        """
        SSL Services profile certificate identifier configuration
        Example :-
            conf_ssl_cert_identifier(
                                sslprofile="sslprofile", certidentifier="ssl-inspect-ca")
            conf_ssl_cert_identifier( mode="delete",
                                sslprofile="sslprofile", certidentifier="ssl-inspect-ca")
            conf_ssl_cert_identifier( sslprofile="sslprofile", sslplugin='proxy',
                               certidentifier="ssl-inspect-ca")
            conf_ssl_cert_identifier( sslprofile="sslinit", sslplugin='initiation',
                               certidentifier="ssl-inspect-ca")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str sslplugin:
            **REQUIRED** ssl plugin type selection
                ``Supported values``: proxy, initiation or termination
        :param str certidentifier:
            **REQUIRED** Certificate identifier a mandatory option to be passed
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        cmdlist = []
        cfg_node = ""
        if sslprofile is None or certidentifier is None or sslplugin is None:
            self.device.log(level="ERROR", message="sslprofile, sslplugin and certidentifier are \
            REQUIRED key argument")
            raise ValueError("sslprofile, sslplugin and certidentifier are REQUIRED key argument")
        if mode == "delete" and commit != "no":
            self.device.log(level="ERROR", message="when mode is delete and commit should be no,\
             as its not appropriate to commit without root/server-certifcate statement")
            raise ValueError("when mode is delete and commit should be no,\
             as its not appropriate to commit without root/server-certifcate statement")
        if sslplugin == 'proxy':
            cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile + \
                       " root-ca " + certidentifier
        elif sslplugin == 'initiation':
            cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile +\
                       " client-certificate " + certidentifier
        elif sslplugin == 'termination':
            cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile + \
                       " server-certificate " + certidentifier
        cmdlist = [cfg_node]

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == "yes" and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_crl(self, sslplugin="proxy", crlaction=None, ifnotpresent=None, **kwargs):
        """
        SSL CRL configuration
        Example :-
            conf_ssl_crl(sslprofile="sslprofile", crlaction="if-not-present",
                                ifnotpresent="allow")
            conf_ssl_crl(sslprofile="sslprofile", crlaction="disable")
            conf_ssl_crl(sslprofile="sslprofile", crlaction="ignore-hold-instruction-code")
            conf_ssl_crl(mode="delete", sslprofile="sslprofile")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslplugin:
            *OPTIONAL* ssl plugin type selection
                ``Supported values``: proxy or initiation
                ``Default value``   : proxy
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str crlaction:
            **REQUIRED** crl action configuration options
                ``Supported values``: disable, if-not-present or ignore-hold-instruction-code
        :param str ifnotpresent:
            *OPTIONAL* if "if-not-present" action is parsed with crlaction then "if-not-present"
             argument is REQUIRED
                ``Supported values``: allow or drop
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if (sslprofile is None or crlaction is None) and mode == 'set':
            self.device.log(level="ERROR", message="sslprofile and crlaction is REQUIRED key \
            argument")
            raise ValueError("sslprofile and crlaction is REQUIRED key argument")
        if crlaction == 'if-not-present' and ifnotpresent is None and mode == 'set':
            self.device.log(level="ERROR", message="ifnotpresent is REQUIRED key argument")
            raise ValueError("ifnotpresent is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument when \
            mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")

        cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile + " actions crl "
        cmdlist = []

        if mode == "set":
            if ifnotpresent is not None:
                cmdlist.append(cfg_node + crlaction + " " + ifnotpresent)
            else:
                cmdlist.append(cfg_node + crlaction)

        # delete node specific configurations
        if mode == "delete":
            cmdlist = [cfg_node]

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == "yes" and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_custom_cipher(self, ciphersuite=None, sslplugin="proxy", **kwargs):
        """
        SSL custom cipher suite configurations
        Example :-
            conf_ssl_custom_cipher(sslprofile="sslprofile", ciphersuite="rsa-with-rc4-128-md5
                                    rsa-with-rc4-128-sha rsa-with-des-cbc-sha
                                    rsa-export-with-rc4-40-md5")
            conf_ssl_custom_cipher(mode="delete", sslprofile="sslprofile",
                                    ciphersuite="rsa-with-rc4-128-md5 rsa-with-rc4-128-sha")
            conf_ssl_custom_cipher(mode="delete", sslprofile="sslprofile")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str ciphersuite:
            **REQUIRED** custom cipher suite
                ``Supported values``:rsa-with-rc4-128-md5            RSA, 128bit rc4, md5 hash
                                    rsa-with-rc4-128-sha            RSA, 128bit rc4, sha hash
                                    rsa-with-des-cbc-sha            RSA, des cbc, sha hash
                                    rsa-with-3des-ede-cbc-sha       RSA, 3des ede/cbc, sha hash
                                    rsa-with-aes-128-cbc-sha        RSA, 128 bit aes/cbc, sha hash
                                    rsa-with-aes-256-cbc-sha        RSA, 256 bit aes/cbc, sha hash
                                    rsa-export-with-rc4-40-md5      RSA-export, 40 bit rc4, md5 hash
                                    rsa-export-with-des40-cbc-sha   RSA-export, 40 bit des/cbc, sha
        :param str sslplugin:
            *OPTIONAL* ssl plugin type selection
                ``Supported values``: proxy, initiation or termination
                ``Default value``   : proxy
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if (sslprofile is None or ciphersuite is None) and mode == 'set':
            self.device.log(level="ERROR", message="sslprofile and ciphersuite is REQUIRED key \
            argument")
            raise ValueError("sslprofile and ciphersuite is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument when \
            mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")

        cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile
        cmdlist = []
        if mode == 'set' or (mode != 'set' and ciphersuite is None):
            cmdlist.append(cfg_node + " preferred-ciphers custom")

        if ciphersuite is not None:
            for line in re.split(r'\s+', str(ciphersuite.strip())):
                cmdlist.append(cfg_node + " custom-ciphers " + line)

        # delete node specific configurations
        if mode == 'delete' and ciphersuite is None:
            cmdlist.append(cfg_node + " custom-ciphers")

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == "yes" and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_preferred_cipher(self, ciphersuite=None, sslplugin="proxy", **kwargs):
        """
        SSL preferred cipher suite configurations
        Example :-
            conf_ssl_preferred_cipher(  sslprofile="sslprofile", ciphersuite="strong")
            conf_ssl_preferred_cipher( mode="delete", sslprofile="sslprofile")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str ciphersuite:
            **REQUIRED** custom cipher suite
                ``Supported values``:
                                    medium      Use ciphers with key strength of 128-bits or greater
                                    strong      Use ciphers with key strength of 168-bits or greater
                                    weak        Use ciphers with key strength of 40-bits or greater
        :param str sslplugin:
            *OPTIONAL* ssl plugin type selection
                ``Supported values``: proxy, initiation or termination
                ``Default value``   : proxy
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if (sslprofile is None or ciphersuite is None) and mode == 'set':
            self.device.log(level="ERROR", message="sslprofile and ciphersuite is REQUIRED\
             key argument")
            raise ValueError("sslprofile and ciphersuite is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument when \
            mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")

        cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile + \
                   " preferred-ciphers "
        cmdlist = []

        cmdlist.append(cfg_node + str(ciphersuite))

        # delete node specific configurations
        if mode == "delete" and ciphersuite is None:
            cmdlist = [cfg_node]

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == "yes" and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_ignore_serv_auth(self, sslplugin="proxy", **kwargs):
        """
        SSL server certificate authentification failure ignore configuration
        Example :-
            conf_ssl_ignore_serv_auth( sslprofile="sslprofile")
            conf_ssl_ignore_serv_auth( mode="delete", sslprofile="sslprofile")
            conf_ssl_ignore_serv_auth( sslprofile="sslinit", sslplugin='initiation')
            conf_ssl_ignore_serv_auth( mode="delete", sslprofile="sslinit",
            sslplugin='initiation')

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslplugin:
            *OPTIONAL* ssl plugin type selection
                ``Supported values``: proxy or initiation
                ``Default value``   : proxy
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if sslprofile is None:
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument")
            raise ValueError("sslprofile is REQUIRED key argument")

        cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile + \
                   " actions ignore-server-auth-failure"
        cmdlist = []
        cmdlist.append(cfg_node)

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == "yes" and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_cache_timeout(self, timeout=None, **kwargs):
        """
        SSL session cache timeout configuration
        Example :-
            conf_ssl_cache_timeout(  sslprofile = "sslprofile", timeout="300")
            conf_ssl_cache_timeout( mode="delete", sslprofile = "sslprofile", timeout="300")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str timeout:
            **REQUIRED** cache timeout for ssl session
                ``Supported values``: 300 to 3600 seconds
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)
        if sslprofile is None or timeout is None:
            self.device.log(level="ERROR", message="sslprofile and timeout is REQUIRED \
            key argument")
            raise ValueError("sslprofile and timeout is REQUIRED key argument")

        cfg_node = mode + " services ssl proxy global-config session-cache-timeout "
        cmdlist = []
        cmdlist.append(cfg_node + timeout)

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == "yes" and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_cert_cache_config(self, **kwargs):
        """
        SSL session cache timeout configuration
        Example :-
        conf_cert_cache_config( device=device, cmd="certificate-cache-timeout",timeout="300")
        conf_cert_cache_config(device=device, mode="delete", cmd = "certificate-cache-timeout", timeout="300")
        conf_cert_cache_config( device=device, cmd="disable-cert-cache")
        conf_cert_cache_config(device=device, mode="delete", cmd="disable-cert-cache")
        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str timeout:
            **REQUIRED** cache timeout for ssl session
                ``Supported values``: 300 to 3600 seconds
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        cmd = kwargs.get('cmd', None)
        timeout = kwargs.get('timeout', None)
        cmdlist = []

        if cmd is None:
            self.device.log(level="ERROR", message="cmd is REQUIRED \
            key argument")
            raise ValueError("cmd is REQUIRED key argument")

        if cmd == 'certificate-cache-timeout' and timeout is None and mode == 'set':
            self.device.log(level="ERROR", message="certificate-cache-timeout value is REQUIRED \
            key argument")
            raise ValueError("timeout is REQUIRED key argument")

        if cmd == 'certificate-cache-timeout' and mode == 'set':
            cfg_node = mode + " services ssl proxy global-config certificate-cache-timeout "
            cmdlist.append(cfg_node + timeout)

        if cmd == 'certificate-cache-timeout' and mode == 'delete':
            cfg_node = mode + " services ssl proxy global-config certificate-cache-timeout "
            cmdlist.append(cfg_node)

        if cmd == 'disable-cert-cache':
            cfg_node = mode + " services ssl proxy global-config disable-cert-cache "
            cmdlist.append(cfg_node)
        # Configure and commit the configuration
        print(cmdlist)
        self.device.config(command_list=cmdlist)
        if commit == "yes" and len(cmdlist) != 0:
            self.device.commit()

        return True


    def conf_ssl_trusted_ca(self, trusted_ca_list=None, sslplugin="proxy", **kwargs):
        """
        Trusted certificate configuration
        Example :-
            conf_ssl_trusted_ca(trusted_ca_list="all", sslprofile ="sslprofile")
            conf_ssl_trusted_ca(mode="delete", trusted_ca_list="all",
                                    sslprofile = "sslprofile")
            conf_ssl_trusted_ca( trusted_ca_list="all test1 test2 test3",
                                    sslprofile = "sslprofile")
            conf_ssl_trusted_ca( mode="delete", trusted_ca_list="all test1
                                    test2 test3", sslprofile = "sslprofile")
            conf_ssl_trusted_ca( mode="delete", sslprofile = "sslprofile")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str trusted_ca_list:
            **REQUIRED**  trusted CAs list
        :param str sslplugin:
            *OPTIONAL* ssl plugin type selection
                ``Supported values``: proxy or initiation
                ``Default value``   : proxy
        :param str sslprofile:
            * REQUIRED * ssl proxy profile name
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if (sslprofile is None or trusted_ca_list is None) and mode == 'set':
            self.device.log(level="ERROR", message="sslprofile and trusted_ca_list is\
             REQUIRED key argument")
            raise ValueError("sslprofile and trusted_ca_list is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument when\
             mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")
        if len(re.split(r"\s+", str(trusted_ca_list))) >= 2 and "all" in trusted_ca_list:
            self.device.log(level="ERROR", message="trusted_ca_list can't have both all and \
            specific trusted ca profile")
            raise ValueError("trusted_ca_list can't have both all and specific trusted ca profile")

        cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile + " trusted-ca "
        cmdlist = []

        if trusted_ca_list is not None:
            for line in re.split(r'\s+', str(trusted_ca_list.strip())):
                cmdlist.append(cfg_node + line)

        # delete node specific configurations
        if mode == "delete" and trusted_ca_list is None:
            cmdlist = [cfg_node]

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == 'yes' and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_flow_trace(self, sslplugin="proxy", **kwargs):
        """
        Flow trace configuration in global ssl service level
        Example :-
            conf_ssl_flow_trace( sslprofile ="sslprofile")
            conf_ssl_flow_trace( mode="delete", sslprofile ="sslprofile")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslplugin:
            *OPTIONAL* ssl plugin type selection
                ``Supported values``: proxy, initiation or termination
                ``Default value``   : proxy
        :param str sslprofile:
            * REQUIRED * ssl proxy profile name
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if sslprofile is None:
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument")
            raise ValueError("sslprofile is REQUIRED key argument")

        cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile + \
                   " enable-flow-tracing "
        cmdlist = []
        cmdlist.append(cfg_node)

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == 'yes' and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_disable_ssl_proxy_resump(self, **kwargs):
        """
        SSL session resumption configuration
        Example :-
            conf_disable_ssl_proxy_resump( sslprofile="sslprofile")
            conf_disable_ssl_proxy_resump( mode="delete", sslprofile="sslprofile")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if sslprofile is None:
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument")
            raise ValueError("sslprofile is REQUIRED key argument")

        cfg_node = mode + " services ssl proxy profile "
        cmdlist = []

        cmdlist.append(cfg_node + sslprofile + " actions disable-session-resumption")

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == 'yes' and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_proxy_renegotiation(self, renegotiation=None, **kwargs):
        """
        SSL session renegotiation configuration
        Example :-
            conf_ssl_proxy_renegotiation( sslprofile="sslprofile", renegotiation="allow-secure")
            conf_ssl_proxy_renegotiation( mode="delete", sslprofile="sslprofile",
                                            renegotiation="allow")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str renegotiation:
            **REQUIRED** renegotiation configuration options
                ``Supported values``: allow, allow-secure or drop
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if sslprofile is None or renegotiation is None:
            self.device.log(level="ERROR", message="sslprofile and renegotiation is \
            REQUIRED key argument")
            raise ValueError("sslprofile and renegotiation is REQUIRED key argument")

        cfg_node = mode + " services ssl proxy profile " + sslprofile + " actions renegotiation " \
                   + renegotiation
        cmdlist = [cfg_node]

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == 'yes' and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_proxy_logging(self, log=None, **kwargs):
        """
        SSL Proxy logging configuration
        Example: -
            conf_ssl_proxy_logging( sslprofile= "sslprofile", log="sessions-whitelisted")
            conf_ssl_proxy_logging( mode="delete", sslprofile="sslprofile", log = "all")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslprofile:
            * REQUIRED * ssl proxy profile name
        :param str log:
            * REQUIRED * log action configuration options:
                ``Supported values``: all                  Log all events
                                      errors               Log all error events
                                      info                 Log all information events
                                      sessions-allowed     Log ssl session allow events after error
                                      sessions-dropped     Log only ssl session drop events
                                      sessions-ignored     Log  session ignore events
                                      sessions-whitelisted  Log ssl session whitelist events
                                      warning              Log all warning events
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if sslprofile is None or log is None:
            self.device.log(level="ERROR", message="sslprofile and log is REQUIRED key argument")
            raise ValueError("sslprofile and log is REQUIRED key argument")

        cfg_node = mode + " services ssl proxy profile " + sslprofile + " actions log " + log
        cmdlist = []

        if mode == "set":
            cmdlist.append(cfg_node)
        elif mode == "delete":
            cmdlist.append(mode + " services ssl proxy profile " + sslprofile + " actions log ")

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == 'yes' and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_proxy_whitelist(self, whitelist=None, **kwargs):
        """
        Whitelist configuration with global address book
        Example :-
            conf_ssl_proxy_whitelist( whitelist="DNS-server DNS-server2", sslprofile="sslprofile")
            conf_ssl_proxy_whitelist( mode="delete", whitelist="DNS-server DNS-server2",
                                        sslprofile = "sslprofile")
            conf_ssl_proxy_whitelist( mode="delete", sslprofile="sslprofile")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str whitelist:
            **REQUIRED** Configure whitelist with global address book
        : param str sslprofile:
            * REQUIRED * ssl proxy profile name
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if (sslprofile is None or whitelist is None) and mode == 'set':
            self.device.log(level="ERROR", message="sslprofile and whitelist is REQUIRED key\
             argument")
            raise ValueError("sslprofile and whitelist is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument \
            when mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")

        cfg_node = mode + " services ssl proxy profile " + sslprofile + " whitelist "
        cmdlist = []

        if whitelist is not None:
            for line in re.split(r'\s+', str(whitelist.strip())):
                cmdlist.append(cfg_node + line)

        # delete complete traceoptions node if no specific configuration is available
        if mode == "delete" and whitelist is None:
            cmdlist = [cfg_node]

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == 'yes' and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_sslsp_server_cert_list(self, servercert=None, **kwargs):
        """
        SSL Server protection Server certification list configuration
        Example :-
            conf_sslsp_server_cert_list( sslprofile="sslprofile", servercert="ssl-inspect-ca")
            conf_sslsp_server_cert_list( mode="delete", sslprofile="sslprofile",
                                            servercert="ssl-inspect-ca")
            conf_sslsp_server_cert_list( mode="delete", sslprofile="sslprofile")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str servercert:
            **REQUIRED** Server certification list. Ensure no commit is passed when only one server
            cert id is deleted from profile to avoid commit check failure
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if (sslprofile is None or servercert is None) and mode == 'set':
            self.device.log(level="ERROR", message="sslprofile and servercert is REQUIRED key\
             argument")
            raise ValueError("sslprofile and servercert is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument \
            when mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")

        cfg_node = mode + " services ssl proxy profile " + sslprofile
        cmdlist = []

        if mode == "delete" and servercert is None:
            cmdlist.append(cfg_node)
        else:
            for line in re.split(r'\s+', str(servercert.strip())):
                cmdlist.append(cfg_node + " server-certificate " + line)

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == 'yes' and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_protocol_version(self, sslplugin="proxy", tls_version=None, \
                                       **kwargs):
        """
        SSL TLS version configuration
        Example :-
            conf_ssl_protocol_version( sslprofile="sslprofile", tls_version="tls11")
            conf_ssl_protocol_version( mode="delete", sslprofile="sslprofile",
                                           tls_version="tls11")
            conf_ssl_protocol_version( sslprofile="sslinit", tls_version="tls1",
                                            sslplugin='initiation')
            conf_ssl_protocol_version( mode="delete", sslprofile="sslinit",
                                           tls_version="tls1", sslplugin='initiation')
            conf_ssl_protocol_version( sslprofile="sslterm", tls_version="tls12",
                                            sslplugin='termination')
            conf_ssl_protocol_version( mode="delete", sslprofile="sslterm",
                                           tls_version="tls12", sslplugin='termination')

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslplugin:
            *OPTIONAL* ssl plugin type selection
                ``Supported values``: proxy, initiation or termination
                ``Default value``   : proxy
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str tls_version:
            **REQUIRED** TLS version for ssl profile
                ``Supported values``: all, tls11, tls12 or tls1
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if sslprofile is None or tls_version is None:
            self.device.log(level="ERROR", message="sslprofile and tls_version is \
            REQUIRED key argument")
            raise ValueError("sslprofile and tls_version is REQUIRED key argument")

        cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile + \
                   " protocol-version " + tls_version
        cmdlist = [cfg_node]

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == 'yes' and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_enable_sess_cache(self, sslplugin="initiation", **kwargs):
        """
        SSL TLS initiation and termination plugin session cache enabling configuration
        Example :-
            conf_ssl_enable_sess_cache( sslprofile="sslinit")
            conf_ssl_enable_sess_cache( mode="delete", sslprofile="sslinit")
            conf_ssl_enable_sess_cache( sslprofile="sslterm",
                                            sslplugin='termination')


        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param str sslplugin:
            **REQUIRED** ssl plugin type selection
                ``Supported values``: initiation or termination
                ``Default value``   : initiation
        :param str sslprofile:
            **REQUIRED** ssl proxy profile name
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if sslprofile is None or sslplugin is None:
            self.device.log(level="ERROR", message="sslprofile and sslplugin is \
            REQUIRED key argument")
            raise ValueError("sslprofile and sslplugin is REQUIRED key argument")

        cfg_node = mode + " services ssl " + sslplugin + " profile " + sslprofile + \
                   " enable-session-cache "
        cmdlist = [cfg_node]

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == 'yes' and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_proxy_whitelist_url(self, whitelist=None, **kwargs):
        """
        Whitelist configuration with global address book
        Example :-
            conf_ssl_proxy_whitelist_url(
                    whitelist="Enhanced_Financial_Data_and_Services", sslprofile = "sslprofile")
            conf_ssl_proxy_whitelist_url(mode="delete",
                    whitelist="Enhanced_Financial_Data_and_Services", sslprofile = "sslprofile")
            conf_ssl_proxy_whitelist_url( whitelist="Enhanced_Social_Web_Facebook",
                    sslprofile = "sslprofile")
            conf_ssl_proxy_whitelist_url(mode="delete", sslprofile = "sslprofile")

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param whitelist:
            **REQUIRED** Configure whitelist with global address book. Not mandatory when user wants
            delete complete whitelist configuration from profile
        :param sslprofile:
            * REQUIRED * ssl proxy profile name
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)

        if (sslprofile is None or whitelist is None) and mode == 'set':
            self.device.log(level="ERROR", message="sslprofile and whitelist is \
            REQUIRED key argument")
            raise ValueError("sslprofile and whitelist is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument when \
            mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")

        cfg_node = mode + " services ssl proxy profile " + sslprofile + " whitelist-url-categories "
        cmdlist = []

        if mode == "delete" and whitelist is None:
            cmdlist = [cfg_node]
        else:
            for line in re.split(r'\s+', str(whitelist.strip())):
                cmdlist.append(cfg_node + line)

        # Configure and commit the configuration
        self.device.config(command_list=cmdlist)
        if commit == "yes" and len(cmdlist) != 0:
            self.device.commit()

        return True

    def conf_ssl_proxy(self, **kwargs):
        """
        Configuring SSL proxy in either client or server protection mode
        Example :-
            conf_ssl_proxy(sslplugin='forward_proxy',
                                sslprofile='sslprofile',
                                certidentifier='ssl-inspect-ca',
                                whitelist_url="Enhanced_Financial_Data_and_Services
                                    Enhanced_Social_Web_Facebook",
                                log="all",
                                renegotiation="allow",
                                resumption="disable",
                                enable_flow_trace="true",
                                trusted_ca_list='all',
                                ignore_server_auth="true",
                                ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-sha',
                                crlaction='if-not-present',
                                ifnotpresent='allow',
                                tls_version='all'
                                )
            conf_ssl_proxy(sslprofile='sslprofile', mode='deLeTe')

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param sslprofile:
            * REQUIRED * ssl proxy profile name
        :param str certidentifier:
            **REQUIRED** Certificate identifier a mandatory option to be passed
        :param str sslplugin:
            **REQUIRED** ssl plugin type selection
                ``Supported values``: forward_proxy or reverse_proxy
        :param str whitelist_url:
            *OPTIONAL* Configure whitelist url categories
        :param str whitelist:
            *OPTIONAL* Configure whitelist with global address book. Not mandatory when user wants
            delete complete whitelist configuration from profile
        :param str log:
            *OPTIONAL* log action configuration options:
                ``Supported values``: all                  Log all events
                                      errors               Log all error events
                                      info                 Log all information events
                                      sessions-allowed     Log ssl session allow events after error
                                      sessions-dropped     Log only ssl session drop events
                                      sessions-ignored     Log  session ignore events
                                      sessions-whitelisted  Log ssl session whitelist events
                                      warning              Log all warning events
        :param str renegotiation:
            *OPTIONAL* renegotiation configuration options
                ``Supported values``: allow, allow-secure or drop
        :param str resumption:
            *OPTIONAL* disable resumption
                ``Supported values``: disable
        :param str enable_flow_trace:
            *OPTIONAL* Enable flow trace for the ssl profile
                ``Supported values``: True
        :param str trusted_ca_list:
            *OPTIONAL*  trusted CAs list
        :param str ignore_server_auth:
            *OPTIONAL* Enabling ignore server certificate authentication
                ``Supported values``: True
        :param str ciphersuite:
            *OPTIONAL* cipher suite
                ``Supported values``:
                        Values for preferred cipher suite
                                medium      Use ciphers with key strength of 128-bits or greater
                                strong      Use ciphers with key strength of 168-bits or greater
                                weak        Use ciphers with key strength of 40-bits or greater
                        Values for custom cipher suite
                                rsa-with-rc4-128-md5            RSA, 128bit rc4, md5 hash
                                rsa-with-rc4-128-sha            RSA, 128bit rc4, sha hash
                                rsa-with-des-cbc-sha            RSA, des cbc, sha hash
                                rsa-with-3des-ede-cbc-sha       RSA, 3des ede/cbc, sha hash
                                rsa-with-aes-128-cbc-sha        RSA, 128 bit aes/cbc, sha hash
                                rsa-with-aes-256-cbc-sha        RSA, 256 bit aes/cbc, sha hash
                                rsa-export-with-rc4-40-md5      RSA-export, 40 bit rc4, md5 hash
                                rsa-export-with-des40-cbc-sha   RSA-export, 40 bit des/cbc, sha
        :param str crlaction:
            *OPTIONAL* crl action configuration options
                ``Supported values``: disable, if-not-present or ignore-hold-instruction-code
        :param str ifnotpresent:
            *OPTIONAL* if "if-not-present" action is parsed with crlaction then "if-not-present"
             argument is REQUIRED
                ``Supported values``: allow or drop
        :param str tls_version:
            *OPTIONAL* TLS version for ssl profile
                ``Supported values``: all, tls11, tls12 or tls1
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)
        certidentifier = kwargs.get('certidentifier', None)

        if (sslprofile is None or kwargs.get('sslplugin') is None or certidentifier is None) and\
                        mode == 'set':
            self.device.log(level="ERROR", message="sslprofile, sslplugin and certidentifier is \
            REQUIRED key argument")
            raise ValueError("sslprofile, sslplugin and certidentifier is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument when \
            mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")

        if mode == 'set':

            if kwargs.get('sslplugin').lower() == "forward_proxy":
                self.conf_ssl_cert_identifier(mode=mode, commit='no', sslprofile=sslprofile,\
                                                sslplugin="proxy", \
                                                certidentifier=certidentifier)
            elif kwargs.get('sslplugin').lower() == "reverse_proxy":
                self.conf_sslsp_server_cert_list(mode=mode, commit='no', sslprofile=sslprofile,\
                                                   servercert=certidentifier)
            if kwargs.get('whitelist_url') is not None:
                self.conf_ssl_proxy_whitelist_url(mode=mode, commit='no', sslprofile=sslprofile,\
                                                    whitelist=kwargs.get('whitelist_url'))
            if kwargs.get('whitelist') is not None:
                self.conf_ssl_proxy_whitelist(mode=mode, commit='no', \
                                                whitelist=kwargs.get('whitelist'), \
                                                sslprofile=sslprofile)
            if kwargs.get('log') is not None:
                self.conf_ssl_proxy_logging(mode=mode, commit='no', sslprofile=sslprofile, \
                                                 log=kwargs.get('log'))
            if kwargs.get('renegotiation') is not None:
                self.conf_ssl_proxy_renegotiation(mode=mode, commit='no', sslprofile=sslprofile,\
                                                    renegotiation=kwargs.get('renegotiation'))
            if kwargs.get('resumption') == 'disable':
                self.conf_disable_ssl_proxy_resump(mode=mode, commit='no',\
                                                         sslprofile=sslprofile)
            if kwargs.get('enable_flow_trace') == 'true':
                self.conf_ssl_flow_trace(mode=mode, commit='no', sslprofile=sslprofile)
            if kwargs.get('trusted_ca_list') is not None:
                self.conf_ssl_trusted_ca(mode=mode, commit='no', sslprofile=sslprofile,\
                                              trusted_ca_list=kwargs.get('trusted_ca_list'))
            if kwargs.get('ignore_server_auth') == 'true':
                self.conf_ssl_ignore_serv_auth(mode=mode, commit='no', sslprofile=sslprofile)
            if kwargs.get('ciphersuite') is not None:
                if kwargs.get('ciphersuite').lower() == 'medium' or \
                                kwargs.get('ciphersuite').lower() == 'strong' or\
                                kwargs.get('ciphersuite').lower() == 'weak':
                    self.conf_ssl_preferred_cipher(mode=mode, commit='no', \
                                                        sslprofile=sslprofile, \
                                                        ciphersuite=kwargs.get('ciphersuite').\
                                                        lower())
                else:
                    self.conf_ssl_custom_cipher(mode=mode, commit='no', sslprofile=sslprofile,\
                                                     ciphersuite=kwargs.get('ciphersuite').lower())
            if kwargs.get('crlaction') is not None:
                if kwargs.get('crlaction') == 'if-not-present':
                    self.conf_ssl_crl(mode=mode, commit='no', sslprofile=sslprofile, \
                                           sslplugin='proxy', crlaction=kwargs.get('crlaction').\
                                           lower(), ifnotpresent=kwargs.get('ifnotpresent').lower())
                else:
                    self.conf_ssl_crl(mode=mode, commit='no', sslprofile=sslprofile,
                                           sslplugin='proxy',
                                           crlaction=kwargs.get('crlaction').lower())
            if kwargs.get('tls_version') is not None:
                self.conf_ssl_protocol_version(mode=mode, commit='no', sslprofile=sslprofile, \
                                                    tls_version=kwargs.get('tls_version').lower())
        elif mode == 'delete':
            cmdlist = []
            cfg_node = mode + " services ssl proxy profile " + sslprofile
            cmdlist = [cfg_node]
            self.device.config(command_list=cmdlist)

        # Configure and commit the configuration
        if commit == "yes":
            self.device.commit()

        return True

    def conf_ssl_initiation(self, **kwargs):
        """
        Configuring SSL proxy in either client or server protection mode
        Example :-
            conf_ssl_initiation(
                                    sslprofile='sslinit',
                                    certidentifier='ssl-inspect-ca',
                                    enable_flow_trace="TrUe",
                                    trusted_ca_list='all',
                                    ignore_server_auth="true",
                                    ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                    crlaction='if-not-present',
                                    ifnotpresent='aLLow',
                                    tls_version='all',
                                    enable_session_cache='true'
                                    )
            conf_ssl_initiation(mode='delete', sslprofile='sslinit')

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param sslprofile:
            * REQUIRED * ssl proxy profile name
        :param str certidentifier:
            **REQUIRED** Certificate identifier a mandatory option to be passed
        :param str enable_flow_trace:
            *OPTIONAL* Enable flow trace for the ssl profile
                ``Supported values``: True
        :param str trusted_ca_list:
            *OPTIONAL*  trusted CAs list
        :param str ignore_server_auth:
            *OPTIONAL* Enabling ignore server certificate authentication
                ``Supported values``: True
        :param str ciphersuite:
            *OPTIONAL* cipher suite
                ``Supported values``:
                        Values for preferred cipher suite
                                medium      Use ciphers with key strength of 128-bits or greater
                                strong      Use ciphers with key strength of 168-bits or greater
                                weak        Use ciphers with key strength of 40-bits or greater
                        Values for custom cipher suite
                                rsa-with-rc4-128-md5            RSA, 128bit rc4, md5 hash
                                rsa-with-rc4-128-sha            RSA, 128bit rc4, sha hash
                                rsa-with-des-cbc-sha            RSA, des cbc, sha hash
                                rsa-with-3des-ede-cbc-sha       RSA, 3des ede/cbc, sha hash
                                rsa-with-aes-128-cbc-sha        RSA, 128 bit aes/cbc, sha hash
                                rsa-with-aes-256-cbc-sha        RSA, 256 bit aes/cbc, sha hash
                                rsa-export-with-rc4-40-md5      RSA-export, 40 bit rc4, md5 hash
                                rsa-export-with-des40-cbc-sha   RSA-export, 40 bit des/cbc, sha
        :param str crlaction:
            *OPTIONAL* crl action configuration options
                ``Supported values``: disable, if-not-present or ignore-hold-instruction-code
        :param str ifnotpresent:
            *OPTIONAL* if "if-not-present" action is parsed with crlaction then "if-not-present"
             argument is REQUIRED
                ``Supported values``: allow or drop
        :param str tls_version:
            *OPTIONAL* TLS version for ssl profile
                ``Supported values``: all, tls11, tls12 or tls1
        :param str enable_session_cache:
            *OPTIONAL* enable session cache
                ``Supported values``: true
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)
        certidentifier = kwargs.get('certidentifier', None)

        if sslprofile is None and certidentifier is None and mode == 'set':
            self.device.log(level="ERROR", message="sslprofile and certidentifier is \
            REQUIRED key argument")
            raise ValueError("sslprofile and certidentifier is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument when \
            mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")

        if mode == 'set':

            self.conf_ssl_cert_identifier(mode=mode, commit='no', sslprofile=sslprofile,\
                                            sslplugin="initiation",\
                                            certidentifier=certidentifier)
            if kwargs.get('enable_flow_trace') == 'true':
                self.conf_ssl_flow_trace(mode=mode, commit='no', sslplugin="initiation", \
                                              sslprofile=sslprofile)
            if kwargs.get('trusted_ca_list') is not None:
                self.conf_ssl_trusted_ca(mode=mode, commit='no', sslplugin="initiation", \
                                              sslprofile=sslprofile,\
                                              trusted_ca_list=kwargs.get('trusted_ca_list'))
            if kwargs.get('ignore_server_auth') == 'true':
                self.conf_ssl_ignore_serv_auth(mode=mode, commit='no', sslplugin="initiation", \
                                                   sslprofile=sslprofile)
            if kwargs.get('ciphersuite') is not None:
                if kwargs.get('ciphersuite').lower() == 'medium' or kwargs.get(\
                        'ciphersuite').lower() == 'strong' or kwargs.get(\
                        'ciphersuite').lower() == 'weak':
                    self.conf_ssl_preferred_cipher(mode=mode, commit='no', \
                                                        sslplugin="initiation", \
                                                        sslprofile=sslprofile,\
                                                        ciphersuite=kwargs.get('ciphersuite').\
                                                        lower())
                else:
                    self.conf_ssl_custom_cipher(mode=mode, commit='no', sslplugin="initiation"\
                                                     , sslprofile=sslprofile,
                                                     ciphersuite=kwargs.get('ciphersuite').lower())
            if kwargs.get('crlaction') is not None:
                if kwargs.get('crlaction') == 'if-not-present':
                    self.conf_ssl_crl(mode=mode, commit='no', sslprofile=sslprofile,
                                           sslplugin='initiation', \
                                           crlaction=kwargs.get('crlaction').lower(),
                                           ifnotpresent=kwargs.get('ifnotpresent').lower())
                else:
                    self.conf_ssl_crl(mode=mode, commit='no', sslprofile=sslprofile,
                                           sslplugin='initiation',
                                           crlaction=kwargs.get('crlaction').lower())
            if kwargs.get('tls_version') is not None:
                self.conf_ssl_protocol_version(mode=mode, commit='no', sslprofile=sslprofile,\
                                                    sslplugin="initiation",\
                                                    tls_version=kwargs.get('tls_version').lower())
            if kwargs.get('enable_session_cache') == 'true':
                self.conf_ssl_enable_sess_cache(mode=mode, commit='no',\
                                                     sslplugin='initiation', sslprofile=sslprofile)
        elif mode == 'delete':
            cmdlist = []
            cfg_node = mode + " services ssl initiation profile " + sslprofile
            cmdlist = [cfg_node]
            self.device.config(command_list=cmdlist)

        # Configure and commit the configuration
        if commit == "yes":
            self.device.commit()

        return True

    def conf_ssl_termination(self, **kwargs):
        """
        Configuring SSL proxy in either client or server protection mode
        Example :-
            conf_ssl_termination(
                                    sslprofile='sslterm',
                                    certidentifier='ssl-inspect-ca',
                                    enable_flow_trace="TrUe",
                                    ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                    tls_version='all',
                                    enable_session_cache='true'
                                    )
            conf_ssl_termination(mode='delete', sslprofile='sslterm')

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param sslprofile:
            * REQUIRED * ssl proxy profile name
        :param str certidentifier:
            **REQUIRED** Certificate identifier a mandatory option to be passed
        :param str enable_flow_trace:
            *OPTIONAL* Enable flow trace for the ssl profile
                ``Supported values``: True
        :param str ciphersuite:
            *OPTIONAL* cipher suite
                ``Supported values``:
                        Values for preferred cipher suite
                                medium      Use ciphers with key strength of 128-bits or greater
                                strong      Use ciphers with key strength of 168-bits or greater
                                weak        Use ciphers with key strength of 40-bits or greater
                        Values for custom cipher suite
                                rsa-with-rc4-128-md5            RSA, 128bit rc4, md5 hash
                                rsa-with-rc4-128-sha            RSA, 128bit rc4, sha hash
                                rsa-with-des-cbc-sha            RSA, des cbc, sha hash
                                rsa-with-3des-ede-cbc-sha       RSA, 3des ede/cbc, sha hash
                                rsa-with-aes-128-cbc-sha        RSA, 128 bit aes/cbc, sha hash
                                rsa-with-aes-256-cbc-sha        RSA, 256 bit aes/cbc, sha hash
                                rsa-export-with-rc4-40-md5      RSA-export, 40 bit rc4, md5 hash
                                rsa-export-with-des40-cbc-sha   RSA-export, 40 bit des/cbc, sha
        :param str tls_version:
            *OPTIONAL* TLS version for ssl profile
                ``Supported values``: all, tls11, tls12 or tls1
        :param str enable_session_cache:
            *OPTIONAL* enable session cache
                ``Supported values``: true
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', None)
        certidentifier = kwargs.get('certidentifier', None)

        if sslprofile is None and certidentifier is None and mode == 'set':
            self.device.log(level="ERROR", message="sslprofile and certidentifier is \
            REQUIRED key argument")
            raise ValueError("sslprofile and certidentifier is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument when \
            mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")

        if mode == 'set':
            self.conf_ssl_cert_identifier(mode=mode, commit='no', sslprofile=sslprofile,
                                            sslplugin="initiation", \
                                            certidentifier=certidentifier)
            if kwargs.get('enable_flow_trace') == 'true':
                self.conf_ssl_flow_trace(mode=mode, commit='no', sslplugin="initiation", \
                                              sslprofile=sslprofile)
            if kwargs.get('ciphersuite') is not None:
                if kwargs.get('ciphersuite').lower() == 'medium' or kwargs.get(
                        'ciphersuite').lower() == 'strong' or kwargs.get('ciphersuite').\
                        lower() == 'weak':
                    self.conf_ssl_preferred_cipher(mode=mode, commit='no', \
                                                        sslplugin="initiation", \
                                                        sslprofile=sslprofile,\
                                                        ciphersuite=kwargs.get('ciphersuite'). \
                                                        lower())
                else:
                    self.conf_ssl_custom_cipher(mode=mode, commit='no',\
                                                     sslplugin="initiation" \
                                                     , sslprofile=sslprofile,\
                                                     ciphersuite=kwargs.get(\
                                                         'ciphersuite').lower())
            if kwargs.get('tls_version') is not None:
                self.conf_ssl_protocol_version(mode=mode, commit='no', sslprofile=sslprofile,
                                                 sslplugin="initiation",
                                                 tls_version=kwargs.get('tls_version').lower())
            if kwargs.get('enable_session_cache') == 'true':
                self.conf_ssl_enable_sess_cache(mode=mode, commit='no', \
                                                     sslplugin='initiation',\
                                                     sslprofile=sslprofile)
        elif mode == 'delete':
            cmdlist = []
            cfg_node = mode + " services ssl termination profile " + sslprofile
            cmdlist = [cfg_node]
            self.device.config(command_list=cmdlist)

        # Configure and commit the configuration
        if commit == "yes":
            self.device.commit()

        return True

    def conf_ssl_proxy_scale(self, **kwargs):
        """
        Configuring SSL proxy in either client or server protection mode
        Example :-
            conf_ssl_proxy(sslplugin='forward_proxy',
                                sslprofile='sslprofile',
                                certidentifier='ssl-inspect-ca',
                                whitelist_url="Enhanced_Financial_Data_and_Services
                                    Enhanced_Social_Web_Facebook",
                                log="all",
                                renegotiation="allow",
                                resumption="disable",
                                enable_flow_trace="true",
                                trusted_ca_list='all',
                                ignore_server_auth="true",
                                ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-sha',
                                crlaction='if-not-present',
                                ifnotpresent='allow',
                                tls_version='all',
                                count='250',
                                commitcount='50'
                                )
            conf_ssl_proxy(sslprofile='sslprofile', mode='deLeTe')

        :param str mode:
            *OPTIONAL* Device configuration mode
                ``Supported values``: set or delete
                ``Default value``   : set
        :param sslprofile:
            * REQUIRED * ssl proxy profile name
        :param str certidentifier:
            **REQUIRED** Certificate identifier a mandatory option to be passed
        :param str sslplugin:
            **REQUIRED** ssl plugin type selection
                ``Supported values``: forward_proxy or reverse_proxy
        :param str whitelist_url:
            *OPTIONAL* Configure whitelist url categories
        :param str whitelist:
            *OPTIONAL* Configure whitelist with global address book. Not mandatory when user wants
            delete complete whitelist configuration from profile
        :param str log:
            *OPTIONAL* log action configuration options:
                ``Supported values``: all                  Log all events
                                      errors               Log all error events
                                      info                 Log all information events
                                      sessions-allowed     Log ssl session allow events after error
                                      sessions-dropped     Log only ssl session drop events
                                      sessions-ignored     Log  session ignore events
                                      sessions-whitelisted  Log ssl session whitelist events
                                      warning              Log all warning events
        :param str renegotiation:
            *OPTIONAL* renegotiation configuration options
                ``Supported values``: allow, allow-secure or drop
        :param str resumption:
            *OPTIONAL* disable resumption
                ``Supported values``: disable
        :param str enable_flow_trace:
            *OPTIONAL* Enable flow trace for the ssl profile
                ``Supported values``: True
        :param str trusted_ca_list:
            *OPTIONAL*  trusted CAs list
        :param str ignore_server_auth:
            *OPTIONAL* Enabling ignore server certificate authentication
                ``Supported values``: True
        :param str ciphersuite:
            *OPTIONAL* cipher suite
                ``Supported values``:
                        Values for preferred cipher suite
                                medium      Use ciphers with key strength of 128-bits or greater
                                strong      Use ciphers with key strength of 168-bits or greater
                                weak        Use ciphers with key strength of 40-bits or greater
                        Values for custom cipher suite
                                rsa-with-rc4-128-md5            RSA, 128bit rc4, md5 hash
                                rsa-with-rc4-128-sha            RSA, 128bit rc4, sha hash
                                rsa-with-des-cbc-sha            RSA, des cbc, sha hash
                                rsa-with-3des-ede-cbc-sha       RSA, 3des ede/cbc, sha hash
                                rsa-with-aes-128-cbc-sha        RSA, 128 bit aes/cbc, sha hash
                                rsa-with-aes-256-cbc-sha        RSA, 256 bit aes/cbc, sha hash
                                rsa-export-with-rc4-40-md5      RSA-export, 40 bit rc4, md5 hash
                                rsa-export-with-des40-cbc-sha   RSA-export, 40 bit des/cbc, sha
        :param str crlaction:
            *OPTIONAL* crl action configuration options
                ``Supported values``: disable, if-not-present or ignore-hold-instruction-code
        :param str ifnotpresent:
            *OPTIONAL* if "if-not-present" action is parsed with crlaction then "if-not-present"
             argument is REQUIRED
                ``Supported values``: allow or drop
        :param str tls_version:
            *OPTIONAL* TLS version for ssl profile
                ``Supported values``: all, tls11, tls12 or tls1
        :param str commit:
            *OPTIONAL* commit configuration option
                ``Supported values``: yes or no
                ``Default value``   : yes
        :param str count:
            *OPTIONAL* no of profiles to be configured
                ``Default value``   : 100
        :param str commitcount:
            *OPTIONAL* iteration limit count to commit
                ``Default value``   : 25
        :return: Returns "True"
        :rtype: bool
        """
        mode = kwargs.get('mode', "set").lower()
        commit = kwargs.get('commit', "yes").lower()
        sslprofile = kwargs.get('sslprofile', "sslprofile")
        certidentifier = kwargs.get('certidentifier', "ssl-inspection-sp")
        count = kwargs.get('count', 100)
        commitcount = kwargs.get('commitcount', 25)

        count_checker = 0

        if (sslprofile is None or kwargs.get('sslplugin') is None or certidentifier is None) and\
                        mode == 'set':
            self.device.log(level="ERROR", message="sslprofile, sslplugin and certidentifier is \
            REQUIRED key argument")
            raise ValueError("sslprofile, sslplugin and certidentifier is REQUIRED key argument")
        if sslprofile is None and mode != 'set':
            self.device.log(level="ERROR", message="sslprofile is REQUIRED key argument when \
            mode is delete")
            raise ValueError("sslprofile is REQUIRED key argument when mode is delete")
        while count_checker < count:
            count_checker += 1
            if mode == 'set':
                self.device.cli(command="request security pki generate-key-pair certificate-id " + \
                           certidentifier + str(count_checker) + " size 1024 type rsa")
                time.sleep(2)
                self.device.cli(command='request security pki local-certificate '
                                        'generate-self-signed certificate-id ' + certidentifier + \
                                        str(count_checker) + " domain-name www.juniper" \
                                        + str(count_checker) + ".net email security-admin@juniper"\
                           + str(count_checker) + ".net subject " + "\"CN=www.juniper" + \
                           str(count_checker) + "_self.net,OU=IT,O=Juniper\"")
                time.sleep(1)

                if kwargs.get('sslplugin').lower() == "forward_proxy":
                    self.conf_ssl_cert_identifier(mode=mode, commit='no', sslprofile=sslprofile
                                                    + str(count_checker), sslplugin="proxy", \
                                                    certidentifier=certidentifier + \
                                                                   str(count_checker))
                elif kwargs.get('sslplugin').lower() == "reverse_proxy":
                    self.conf_sslsp_server_cert_list(mode=mode, commit='no',\
                                                       sslprofile=sslprofile + str(count_checker),\
                                                       servercert=certidentifier + \
                                                                  str(count_checker))
                if kwargs.get('whitelist_url') is not None:
                    self.conf_ssl_proxy_whitelist_url(mode=mode, commit='no', \
                                                        sslprofile=sslprofile + str(count_checker),\
                                                        whitelist=kwargs.get('whitelist_url'))
                if kwargs.get('whitelist') is not None:
                    self.conf_ssl_proxy_whitelist(mode=mode, commit='no', \
                                                    whitelist=kwargs.get('whitelist'), \
                                                    sslprofile=sslprofile + str(count_checker))
                if kwargs.get('log') is not None:
                    self.conf_ssl_proxy_logging(mode=mode, commit='no', sslprofile=sslprofile +\
                                                        str(count_checker), log=kwargs.get('log'))
                if kwargs.get('renegotiation') is not None:
                    self.conf_ssl_proxy_renegotiation(mode=mode, commit='no', \
                                                        sslprofile=sslprofile + str(count_checker),\
                                                        renegotiation=kwargs.get('renegotiation'))
                if kwargs.get('resumption') == 'disable':
                    self.conf_disable_ssl_proxy_resump(mode=mode, commit='no',\
                                                             sslprofile=sslprofile + \
                                                                        str(count_checker))
                if kwargs.get('enable_flow_trace') == 'true':
                    self.conf_ssl_flow_trace(mode=mode, commit='no', sslprofile=sslprofile +\
                                                                                str(count_checker))
                if kwargs.get('trusted_ca_list') is not None:
                    self.conf_ssl_trusted_ca(mode=mode, commit='no', sslprofile=sslprofile + \
                                                                            str(count_checker),\
                                                  trusted_ca_list=kwargs.get('trusted_ca_list'))
                if kwargs.get('ignore_server_auth') == 'true':
                    self.conf_ssl_ignore_serv_auth(mode=mode, commit='no',\
                                                       sslprofile=sslprofile + str(count_checker))
                if kwargs.get('ciphersuite') is not None:
                    if kwargs.get('ciphersuite').lower() == 'medium' or \
                                    kwargs.get('ciphersuite').lower() == 'strong' or\
                                    kwargs.get('ciphersuite').lower() == 'weak':
                        self.conf_ssl_preferred_cipher(mode=mode, commit='no', \
                                                         sslprofile=sslprofile + str(count_checker)\
                                                         , ciphersuite=kwargs.get('ciphersuite').\
                                                         lower())
                    else:
                        self.conf_ssl_custom_cipher(mode=mode, commit='no', \
                                                    sslprofile=sslprofile + str(count_checker),\
                                                    ciphersuite=kwargs.get('ciphersuite').lower())
                if kwargs.get('crlaction') is not None:
                    if kwargs.get('crlaction') == 'if-not-present':
                        self.conf_ssl_crl(mode=mode, commit='no', sslprofile=sslprofile + \
                                                str(count_checker), sslplugin='proxy',\
                                               crlaction=kwargs.get('crlaction').lower(),\
                                               ifnotpresent=kwargs.get('ifnotpresent').lower())
                    else:
                        self.conf_ssl_crl(mode=mode, commit='no', sslprofile=sslprofile +\
                                            str(count_checker), sslplugin='proxy',\
                                               crlaction=kwargs.get('crlaction').lower())
                if kwargs.get('tls_version') is not None:
                    self.conf_ssl_protocol_version(mode=mode, commit='no', sslprofile=sslprofile \
                                                     + str(count_checker), \
                                                     tls_version=kwargs.get('tls_version').lower())
            elif mode == 'delete':
                cmdlist = []
                cmdlist = ["run clear security pki local-certificate certificate-id " +
                           certidentifier + str(count_checker)]
                time.sleep(1)
                self.device.config(command_list=cmdlist)
                cmdlist = ["run clear security pki key-pair certificate-id " + certidentifier +
                           str(count_checker)]
                self.device.config(command_list=cmdlist)
                time.sleep(1)
                cfg_node = mode + " services ssl proxy profile " + sslprofile + str(count_checker)
                cmdlist = [cfg_node]
                self.device.config(command_list=cmdlist)

            if count_checker % commitcount == 0:
                # Configure and commit the configuration
                if commit == "yes":
                    self.device.commit()
        return True
