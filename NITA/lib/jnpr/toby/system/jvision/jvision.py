"""
Copyright (C) 2016-2017, Juniper Networks, Inc.
All rights reserved.
Authors: akanadam, wtang, akachana
Description:
        Toby Jvision test suite
"""
# pylint: disable=locally-disabled,undefined-variable,invalid-name
import re
import os
import socket
import ipaddress
import json
import ast
from jnpr.toby.logger.logger import get_log_dir
import paramiko
from paramiko import SSHClient
from scp import SCPClient
from jnpr.toby.system.jvision.influxReader import InfluxDB
from jnpr.toby.hldcl.host import upload_file
from jnpr.toby.hldcl.device import connect_to_device
from jnpr.toby.exception.toby_exception import TobyException
#from influxReader import InfluxDB
#import builtins
#t=t
#tv=tv

class jvision(object):
    """
    Base Class for Toby Jvision
    Protocol/feature independent Design
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    def __init__(self):
        self.decoder_path = {'grpc': None, 'udp': None, 'gnmi': None}
        self.decoder_status = {'grpc':False, 'udp':False, 'gnmi':False}
        self.decoder_pid = {'grpc': None, 'udp': None, 'gnmi':None}
        self.decoder_port = {'grpc': None, 'udp': None, 'gnmi':None}
        self.decoder_type = ''
        self.json_filename = ''
        self.dut_ip_address = ''
        self.server_ip_address = ''
        self.db_obj = None
        self.db_query = ''
        self.db_params = {}
        self.db_measure = ''
        self.log_head = ''
        self.log_path = get_log_dir()
        self.db_name = self.log_head
        self.db_path = '' #self.log_path+'/'+self.db_name
        self.type = ''
        self.json_file = ''
        self.grpc_port = ''
        self.file_name_pem = ''
        self.cid = ''
        self.json_params = {}

    def jvision_init(self, **kwargs):
        """
        Initialize keyword for Jvision Server. The parameters are
        device, interface, server_ip_address, dut_ip_address
        decoder_path, decoder_port

        Usage:

        jvision init    device=<server handle>  interface=<Interface of server facing DUT>
        server_ip_address=<server ip address>   dut_ip_address=<dut ip address>
        decoder_path=<location of decoder>      decoder_port=<decoder part>    mgmt_ip=<flag for mgmt_ip>

        Example :

        jvision init    device=${h0}    interface=eth1
        server_ip_address=1.1.1.1/24   dut_ip_address=1.1.1.2/24
        decoder_path=  grpc=/opt/jvision/grpc/oc/    decoder_port=4321    mgmt_ip=False
        """
        if not kwargs.get('device') or not kwargs.get('interface') \
                or not kwargs.get('server_ip_address') or not kwargs.get('dut_ip_address'):
            t.log(level='ERROR', message='missing mandatory server '
                                         'or interface or server ip address or dut ip address')
            raise ValueError("server & dut information are mandatory arguments")
        count = 5
        server = kwargs.get('device')
        interface = kwargs.get('interface')
        if kwargs.get('mgmt_ip'):
            mgmt_ip = ast.literal_eval(kwargs.get('mgmt_ip'))
        else:
            mgmt_ip = False
        self.server_ip_address = kwargs.get('server_ip_address')
        self.dut_ip_address = kwargs.get('dut_ip_address')
        if not server.su():
            raise ValueError("cannot login to server as root user")
        if mgmt_ip == False:
            try:
                t.log(level='INFO', message='configuring IP address on interface facing DUT')
                server.shell(command="ifconfig %s 0" % interface + '\n')
                server.shell(command='ifconfig ' + interface + ' ' + self.server_ip_address + '\n')
                t.log(level='INFO', message='verify IP address configuration on interface')
                response = server.shell(command="ifconfig %s" % interface + '\n')
                server_ip = str(ipaddress.IPv4Interface(self.server_ip_address)).split("/")
                match = re.search('inet' + '.*' + server_ip[0] + '.*' + 'Mask:', response.response())
                if match:
                    t.log(level='INFO', message="Server IP address is configured successfully")
                else:
                    t.log(level='ERROR', message="Server IP address is not configured successfully")
                t.log(level='INFO', message='configuring static route to DUT')
                dut_network = str(ipaddress.IPv4Network(self.dut_ip_address, strict=False).with_netmask).split("/")
                dut_ip = str(ipaddress.IPv4Interface(self.dut_ip_address)).split("/")
                server.shell(command='route add -net ' + dut_network[0] + ' '
                             + 'netmask' + ' ' + dut_network[1] + ' ' + 'dev' + ' ' + interface + '\n')
                response = server.shell(command="netstat -nr" + '\n')
                match = re.search(dut_network[0] + '.*' + dut_network[1] + '.*', response.response())
                if match:
                    t.log(level='INFO', message="Route to DUT is configured successfully")
                else:
                    t.log(level='ERROR', message="Route to DUT is not configured successfully")
            except:
                t.log(level='ERROR', message='shell command execution failed')
                raise ValueError("cannot configure IP address and route on server")
        dut_ip = str(ipaddress.IPv4Interface(self.dut_ip_address)).split("/")
        t.log(level='INFO', message='Verify if DUT is reachable')
        response = server.shell(command=('ping ' + dut_ip[0]
                                         + ' ' + '-c' + ' ' + str(count)) + '\n')
        match = re.search(str(count) + ' ' + 'packets transmitted,' + ' ' +
                          str(count) + ' ' + 'received,' + ' ' + '0% packet loss', response.response())
        if match:
            t.log(level='INFO', message="Ping successful to DUT")
        else:
            t.log(level='ERROR', message="Ping unsuccessful to DUT")
        if not kwargs.get('decoder_path'):
            t.log(level='ERROR', message='missing mandatory params')
            raise ValueError("missing mandatory params")
        if not isinstance(kwargs.get('decoder_port'), dict) and \
                isinstance(kwargs.get('decoder_path'), dict):
            t.log(level='ERROR', message='params must be dictionary')
            raise TypeError("params must be dictionary")
        else:
            if kwargs.get('decoder_path').get('grpc'):
                self.decoder_path['grpc'] = str(kwargs.get('decoder_path')['grpc'])
                self.decoder_port['grpc'] = int(kwargs.get('decoder_port')['grpc'])
            if kwargs.get('decoder_path').get('udp'):
                self.decoder_path['udp'] = str(kwargs.get('decoder_path')['udp'])
                self.decoder_port['udp'] = int(kwargs.get('decoder_port')['udp'])
            if kwargs.get('decoder_path').get('gnmi'):
                self.decoder_path['gnmi'] = str(kwargs.get('decoder_path')['gnmi'])
                self.decoder_port['gnmi'] = int(kwargs.get('decoder_port')['gnmi'])
            if kwargs.get('decoder_path').get('gnmi-dialout'):
                self.decoder_path['gnmi-dialout'] = str(kwargs.get('decoder_path')['gnmi-dialout'])
                self.decoder_port['gnmi-dialout'] = int(kwargs.get('decoder_port')['gnmi-dialout'])
        self.jv_db_server = kwargs.get('db_server', None)

    def grpc_init(self, **kwargs):
        """
            generate key and upload it to dut

            configure grpc on device
        """

        if not kwargs.get('server_handle') or not kwargs.get('dut_handle'):
            t.log(level='ERROR', message='missing server handle or dut handle')
            raise ValueError("missing server handle or dut handles")

        dut = kwargs.get('dut_handle')
        server = kwargs.get('server_handle')

        file_name = 'privatekey'
        key_size = kwargs.get('key_size')
        port = kwargs.get('port')
        file_name_key = file_name + '.key'
        file_name_csr = file_name + '.csr'
        file_name_key_orig = file_name_key + '.orig'
        file_name_crt = file_name + '.crt'
        file_name_pem = file_name + '.pem'
        password = 'Juniper'
        dut_host_name = tv['uv-jv-dut-ip']
        common_name = dut_host_name
        self.file_name_pem = file_name_pem

        if not key_size:
            key_size = 2048

        if not port:
            port = 50051

        key_size = str(key_size)
        port = str(port)
        self.grpc_port = port
        t.log(level='INFO', message=common_name)

        try:
            dut.config(command_list=['delete security certificates local mycert', 'delete system services extension-service request-response  grpc'])
            dut.commit()

            dut.config(command_list=['set system services extension-service request-response grpc clear-text port ' + port,
                                     'set system services extension-service request-response grpc skip-authentication',
                                     'set system services extension-service notification allow-clients address 0.0.0.0/0'])
            dut.commit()
        except:
            t.log(level='ERROR', message="configure grpc failed on router")
            raise ValueError("configure grpc failed on router")

        try:
            server.su()
            server.shell(command='cd /tmp')
            server.shell(command='ls -ls')
            server.shell(command='rm -rf ' + file_name + '.*')

            server.shell(command='openssl genrsa -des3 -out ' + file_name_key + ' ' + key_size, pattern=file_name_key + ':')
            server.shell(command=password, pattern=file_name_key + ':')
            server.shell(command=password)
            server.shell(command='openssl req -new -key ' + file_name_key + ' -out ' + file_name_csr, pattern=file_name_key + ':')
            server.shell(command=password, pattern='Country Name \(2 letter code\) \[AU\]:')
            server.shell(command='', pattern='State or Province Name \(full name\) \[Some-State\]:')
            server.shell(command='', pattern='Locality Name \(eg, city\) \[\]:')
            server.shell(command='', pattern='Organization Name \(eg, company\) \[Internet Widgits Pty Ltd\]:')
            server.shell(command='', pattern='Organizational Unit Name \(eg, section\) \[\]:')
            server.shell(command='', pattern='Common Name \(e.g. server FQDN or YOUR name\) \[\]:')
            server.shell(command=common_name, pattern='Email Address \[\]:')
            server.shell(command='', pattern='A challenge password \[\]:')
            server.shell(command='', pattern='An optional company name \[\]:')
            server.shell(command='')
            server.shell(command='cp ' + file_name_key + ' ' + file_name_key_orig)
            server.shell(command='openssl rsa -in ' + file_name_key_orig + ' -out ' + file_name_key, pattern=file_name_key_orig + ':')
            server.shell(command=password)
            server.shell(command='openssl x509 -req -days 365 -in ' + file_name_csr + ' -signkey ' + file_name_key + ' -out ' + file_name_crt)
            server.shell(command='cat ' + file_name_key + ' ' + file_name_crt + '>>' + file_name_pem)
            response = server.shell(command='ls -ls')
            match = re.search(file_name_pem, response.response())
            if match:
                t.log(level='INFO', message="pem file is generated successfully")
            else:
                t.log(level='ERROR', message="pem file is not generated successfully")

        except:
            t.log(level='ERROR', message='pem file generation failed')
            raise ValueError("cannot generate pem file on server")

        try:
            server.shell(command='scp ' + file_name_pem + ' regress@' + dut_host_name + ':/tmp', pattern='Password:')
            server.shell(command='MaRtInI')

        except:
            t.log(level='ERROR', message='pem file uploaded to router unsucessfully')
            raise ValueError("pem file uploaded to router unsucessfully")

    def _trim_db_measure_param(self):
        self.db_params['db_measure'] = str(self.db_params['db_measure'])
        self.db_params['db_measure'] = re.sub(r'^"|"$', '', self.db_params['db_measure'])  # chomp trailing double quotes if any
        arr = self.db_params['db_measure'].split(',')   # split them and add double quotes for each
        self.db_params['db_measure'] = ','.join('"%s"' % x for x in arr )
        return self.db_params['db_measure']

    def _build_db_query(self):
        """
        Build Database Query with user params
        """

        base_query = "select * from " +  self._trim_db_measure_param()
        if all([self.db_params['db_where_jkey'], self.db_params['db_where_comp_id']]):
            self.db_params['db_where_key'] = self.db_params['db_where_jkey'] + " and " + \
                                             self.db_params['db_where_comp_id']
        elif self.db_params['db_where_jkey']:
            self.db_params['db_where_key'] = self.db_params['db_where_jkey']
        elif self.db_params['db_where_comp_id']:
            self.db_params['db_where_key'] = self.db_params['db_where_comp_id']
        else:
            t.log(level='info', message=base_query)
            base_query = base_query + " limit " + str(self.db_params['db_limit']) + ";"
            return base_query
        base_query = base_query + " where " + self.db_params['db_where_key'] + " limit " \
                     + str(self.db_params['db_limit']) + ";"
        t.log(level='info', message=base_query)
        t.log(level='info', message=base_query)
        return base_query

    def start_jvision_decoder(self, **kwargs):
        """
        start jvision decoder on jvision server
        :param server_handle: jvision server object
        :param decoder_type: type of the decoder(grpc/udp/gnmi)
        :param decoder_command: cmd line arg to run decoder of decoder_type

        Example
        Start Jvision decoder    server_handle=${h0}
        decoder_type=grpc    decoder_command=python oc_db.py
        """
        if not kwargs.get('server_handle'):
            t.log(level='ERROR', message='missing madatory server_tag')
        server = kwargs.get('server_handle')
        self.decoder_type = kwargs.get('decoder_type')
        self.type = kwargs.get('type')
        decoder_cmd = ''
        if self.type == 'python':
            decoder_cmd = kwargs.get('decoder_command') + " -c " + self.json_file
        elif self.type == 'go' and self.decoder_type == 'grpc':
            decoder_cmd = kwargs.get('decoder_command') + " " + self.json_file
        elif self.type == 'go' and self.decoder_type == 'gnmi':
            decoder_cmd = kwargs.get('decoder_command')+" --config "+self.json_file+" --gnmi"+" --log "+ self.log_head+".log"
        elif self.type == 'go' and self.decoder_type == 'udp':
            decoder_cmd = kwargs.get('decoder_command')+" --config "+self.json_file+" --log "+ self.log_head+".log"
        elif self.type == 'go' and self.decoder_type == 'gnmi-dialout':
            decoder_cmd = kwargs.get('decoder_command')+" --config "+self.json_file+" --gnmi-dialout"+" --log "+ self.log_head+".log"
        server.su()
        try:
            t.log(level='INFO', message='starting decoder')
            self.decoder_status[self.decoder_type] = True
            server.shell(command='cd '+ str(self.decoder_path[self.decoder_type]) + '\n')
            decoder_res = server.shell(command=decoder_cmd +
                                       ' >/dev/null 2>&1 &').response()
            decoder_res = decoder_res.split()[-1]
            self.decoder_pid[self.decoder_type] = int(decoder_res)
            t.log(level='INFO', message="decoder PID is "+ str(decoder_res))
        except TypeError:
            t.log(level='ERROR', message='shell command execution failed')
        except ValueError:
            t.log(level='ERROR', message='shell command execution failed')
        return True

    def _grpc_ssh_config(self, **kwargs):
        '''
          _grpc_ssh_config
          delete the existing grpc configurations and change them to ssh version
        '''

        if not kwargs.get('dut_handle'):
            t.log(level='ERROR', message='missing server handle or dut handle')
            raise ValueError("missing server handle or dut handle")

        if self.file_name_pem == '' or self.grpc_port == '':
            t.log(level='ERROR', message=' pem file name or grpc_port is invalid')
            raise ValueError("pem file name or grpc_port is invalid")

        dut = kwargs.get('dut_handle')
        try:
            dut.config(command_list=['delete security certificates local mycert', 'delete system services extension-service request-response  grpc'])
            dut.commit()

            dut.config(command_list=['set security certificates local mycert load-key-file /tmp/' + self.file_name_pem,
                                     'set system services extension-service request-response grpc ssl address 0.0.0.0 port ' + self.grpc_port,
                                     'set system services extension-service request-response grpc ssl local-certificate mycert',
                                     'set system services extension-service traceoptions flag all'])
            dut.commit()
        except:
            t.log(level='ERROR', message="configure grpc ssh failed on router")
            raise ValueError("configure grpc ssh failed on router")

    def query_db(self, mode="both", **kwargs):
        """
        Query the InfluxDB with db_params. The parameters are
        mode, dictionary of database params like db_measure,component_id,
        jkey,jvalue
        :param mode:determine storing the result in a var or file
        mode=both:result in var and file
        mode=file:result in file on disk
        mode=var:result is returned to store in a var
        :param db_params:dictionary of database params
        :param type raw
        :query <raw_query>
        Example:
        ${db_result}=  Query Db    mode=file    db_params=${Db_params}
        ${db_result}=  Query Db    mode=file    type=raw   query=<raw_query>
        """
        self.jv_db_init()
        if kwargs.get('type') == 'raw':
            self.db_query = kwargs.get('query', None)
            t.log('info', self.db_query)
        else:
            self.db_params['db_measure'] = kwargs.get('db_params')['db_measure']
            self.db_params['db_where_jkey'] = kwargs.get('db_params')['db_where_jkey']
            self.db_params['db_where_comp_id'] = kwargs.get('db_params')['db_where_comp_id']
            t.log('info', self.db_params['db_where_jkey'])
            t.log('info', self.db_params['db_where_comp_id'])
            self.db_params['db_limit'] = kwargs.get('db_params')['db_limit']
            self.db_query = self._build_db_query()
        jv_db_result = self.jv_db_query(self.db_query)
        jv_list_keys = jv_db_result.keys()
        t.log(level='info', message=jv_list_keys)
        jv_list = list(jv_db_result.get_points())
        jv_result = json.dumps(jv_list, indent=4)
        t.log('info', jv_result)
        self.db_path = self.log_path + "/" + self.log_head
        t.log('info', self.db_path)
        if mode in ["file", "both"]:
            with open(self.db_path, 'w+') as db_file:
                try:
                    db_file.write(jv_result)
                except TypeError:
                    t.log('error', "TypeError in the dict for json file")
                except ValueError:
                    t.log("ValueError in the dict for json file")
                except:
                    t.log("OtherError is found in the dict for json file")
                    raise ValueError("OtherError is found in the dict for json file")
            if mode == "both":
                return jv_result
        else:
            return jv_result

    def query_kpi(self, **kwargs):
        """
        Keyword for getting data for a specific KPI
        query kpi    kpi=kpi4    mode=file    db_measure=${measurement_name}
        All parameters are mandatory
        Result will be dumped in a file/variable acc to kpi parameter
        Result files are stored under ~/<LOG_DIR>/*_kpi
        """
        kpi = kwargs.get('kpi')
        self.db_measure = kwargs.get('db_measure')
        db_measure = self.db_measure
        db_measure = db_measure.replace('"', '')
        if not kpi or not db_measure:
            t.log(level='ERROR', message='kpi or db measure is missing')
        mode = kwargs.get('mode')
        self.jv_db_init()
        jv_sensor = []
        jv_list_oc_log = []
        if kpi == 'kpi1':
            t.log('executing kpi1')
            base_query = r'SELECT "in-payload-length-bytes" , "in-packets" , "run-time"  FROM "' + db_measure+'-LOG"'
            t.log(base_query)
            jv_db_result_oc_log = self.jv_db_query(base_query)
            t.log(level='info', message=jv_db_result_oc_log)
            jv_list_oc_log = list(jv_db_result_oc_log.get_points())
            t.log(jv_list_oc_log)
            for jv_key_oc_log in jv_list_oc_log:
                payload_size = float(jv_key_oc_log['in-payload-length-bytes'])/float(jv_key_oc_log['in-packets'])
                jv_sensor.append({'payload-size': payload_size})
                jv_sensor.append({'in-payload-length-bytes': jv_key_oc_log['in-payload-length-bytes']})
                jv_sensor.append({'in-packets': jv_key_oc_log['in-packets']})
            t.log(level='info', message=jv_list_oc_log)
            jv_result = json.dumps(jv_sensor, indent=4)
            t.log('info', jv_result)
        elif kpi == 'kpi4':
            t.log('executing kpi4')
            base_query = r'SELECT min(ilatency) as "min", max(ilatency) as "max", mean(ilatency) as "avg", \
                        min(ilatency) as "p-0", percentile(ilatency, 25) as "p-25", percentile(ilatency, 50) as "p-50", \
                        percentile(ilatency, 75) as "p-75", percentile(ilatency, 80) as "p-80", percentile(ilatency, 90) \
                        as "p-90", percentile(ilatency,95) as "p-95", percentile(ilatency, 100) as "p-100" FROM "' + \
                        db_measure + r'" group by sensor'
            t.log(base_query)
            jv_db_result_oc = self.jv_db_query(base_query)
            jv_list_keys = jv_db_result_oc.keys()
            t.log(level='info', message=jv_list_keys)
            jv_list_oc = list(jv_db_result_oc.get_points())
            t.log(level='info', message=jv_list_oc_log)
            for jv_elem in jv_list_oc:
                jv_elem = dict(jv_elem)
                jv_sensor.append(jv_elem)
            for i, jv_key in enumerate(jv_list_keys):
                jv_sensor[i].update({'sensor':jv_key[1]["sensor"]})
            jv_result = json.dumps(jv_sensor, indent=4)
            t.log('info', jv_result)
        self.db_path = self.log_path + "/" + self.log_head + "_" + kpi
        t.log('info', self.db_path)
        if mode in ["file", "both"]:
            with open(self.db_path, 'w')as db_file:
                try:
                    db_file.write(jv_result)
                except TypeError:
                    t.log('error', "TypeError in the dict for json file")
                except ValueError:
                    t.log("ValueError in the dict for json file")
                except:
                    t.log("OtherError is found in the dict for json file")
                    raise ValueError("OtherError is found in the dict for json file")
            db_file.close()
            if mode == "both":
                return jv_result
        else:
            return jv_result

    def stop_jvision_decoder(self, **kwargs):
        """
        stop jvision decoder on jvision server
        :param server_handle:jvision server object
        :param decoder_type:grpc/udp/gnmi

        Example:
        Stop Jvision decoder    server_handle=${h0}    decoder_type=grpc
        """
        if not kwargs.get('decoder_type') and kwargs.get('server_handle'):
            t.log(level='ERROR', message='missing mandatory params')
            raise ValueError('missing mandatory params')
        self.decoder_type = kwargs.get('decoder_type')
        server = kwargs.get('server_handle')
        if not self.decoder_status[self.decoder_type]:
            t.log(level='ERROR', message='Decoder not running')
            raise Exception("Decoder cannot be stopped if its not running")
        try:
            t.log(level='INFO', message='killing ' + self.decoder_type + ' decoder'+ "of PID as "+str(self.decoder_pid[self.decoder_type]))
            res = server.shell(command='kill ' + "-SIGTSTP " +
                               str(self.decoder_pid[self.decoder_type]) + '\n').response()
            t.log(level='INFO', message=res)
        except Exception as err:
            t.log(level='ERROR', message=err)

    def kill_jvision_decoder(self, **kwargs):
        """
        Kill jvision decoder on jvision server
        :param server_handle:jvision server object
        :param decoder_type:grpc/udp

        Example:
        Kill Jvision decoder    server_handle=${h0}    decoder_type=grpc
        """
        if not kwargs.get('decoder_type') and kwargs.get('server_handle'):
            t.log(level='ERROR', message='missing mandatory params')
            raise ValueError('missing mandatory params')
        self.decoder_type = kwargs.get('decoder_type')
        server = kwargs.get('server_handle')
        if not self.decoder_status[self.decoder_type]:
            t.log(level='ERROR', message='Decoder not running')
            raise Exception("Decoder cannot be killed if its not running")
        try:
            t.log(level='INFO', message='killing ' + self.decoder_type + ' decoder'+ "of PID as "+ str(self.decoder_pid[self.decoder_type]))
            res = server.shell(command='kill ' + "-SIGKILL " +
                               str(self.decoder_pid[self.decoder_type]) + '\n').response()
            t.log(level='INFO', message=res)
        except Exception as err:
            t.log(level='ERROR', message=err)
            #raise
        self.decoder_status[self.decoder_type] = False

    def gen_and_upload_json(self, **kwargs):
        """
        generate json file and upload to the server
        """
        self.json_params = kwargs.get('sensor_params')
        self.gnmi_params = kwargs.get('gnmi_params', None)
        self.cid = kwargs.get('cid', "cid-45")
        t.log('info', str(self.json_params))
        self.decoder_type = kwargs.get('decoder_type')
        if not self.json_params:
            t.log(level="ERROR", message="json parameters are mandatory")
            raise ValueError("json parameters are mandatory")
        db_measure = kwargs.get('db_measure')
        if self.decoder_type != "udp":
            need_eos = int(kwargs.get('eos'))
            dut_ip = self.dut_ip_address.split("/")[0]
            collector_ip = self.server_ip_address.split("/")[0]
        else:
            self.json_params["source_ips"] = kwargs.get('source_ips')
            self.json_params["detail_logging"] = kwargs.get('detail_logging')

        sensor_data = self.json_params.keys()
        jv_server = kwargs.get('jv_server', tv['h0__name'])
        if not self.jv_db_server:
            self.jv_db_server = tv['uv-db-host']
        self.log_head = t.get_session_id() + '_' +  str(os.getpid())
        session_log_head = 'session_' + self.log_head
        path_list = list(self.json_params.keys())
        t.log(path_list)
        self.db_name = self.log_head

        json_filename = kwargs.get('json_filename', None)
        if json_filename is None:
            self.json_filename = self.log_path + '/' + self.log_head + ".json"
        else:
            self.json_filename = self.log_path + '/' + json_filename
        json_filename = self.json_filename
        self.json_file = str(self.log_head + ".json")
        t.log(level='INFO', message="DB name:" + self.db_name)
        self.type = kwargs.get('type')
        decoder_path = ""
        decoder_port = self.decoder_port[self.decoder_type]
        if self.type == 'python' and self.decoder_type == 'grpc':
            decoder_path = self.decoder_path['grpc']
            jv_json = \
                {
                    "dut_list": [
                        {
                            "ip": dut_ip,
                            "port": decoder_port,
                            "session_log": session_log_head,
                            "log_head": self.log_head,
                            "oc_rpc": [
                                "subscribe"
                            ],
                            "subscribe": {
                                "path_list": [],
                                "input": {
                                    "collector_list": [
                                        {
                                            "address": collector_ip,
                                            "port": decoder_port
                                        }
                                    ]
                                },
                                "additional_config": {
                                    "limit_records": 1,
                                    "limit_time_seconds": 1,
                                    "need_eos": need_eos
                                }
                            }
                        }
                    ]
                }
            t.log(level='INFO', message="DB name:" + self.log_head)
            for key in sensor_data:
                path_dict = \
                    {
                        "path": key,
                        "filter": self.json_params[key]['filter'],
                        "sample_frequency": int(self.json_params[key]['freq']),
                        #"need_eos": int(self.json_params[key]['eos'])
                        "suppress_unchanged": "",
                        "max_silent_interval": 0
                    }
                jv_json['dut_list'][0]['subscribe']['path_list'].append(dict(path_dict))
            t.log(level='info', message=jv_json)
        elif self.type == 'go' and self.decoder_type == 'grpc':
            decoder_path = self.decoder_path['grpc']
            plist = []
            path = {}
            for i in range(len(path_list)):
                t.log(path_list[i])
                path['path'] = path_list[i]
                if self.json_params[path_list[i]].get('freq'):
                    path['freq'] = int(self.json_params[path_list[i]]['freq'])
                #path['freq'] = int(self.json_params[path_list[i]]['freq'])
                plist.append(dict(path))
            t.log(level='INFO', message=plist)
            jv_json = \
                {
                    "host": dut_ip,
                    "port": decoder_port,
                    "cid": self.cid,
                    "influx" : {
                        "server" : self.jv_db_server,
                        "port" : 8086,
                        "dbname" : self.db_name,
                        "measurement" : db_measure,
                        "user" : tv['uv-db-username'],
                        "password" : tv['uv-db-password'],
                        "recreate" : True
                    },
                    "grpc" : {
                        "ws" : 1048576
                    },
                    "paths": plist
                }
            t.log(level='info', message=jv_json)
        elif self.type == 'go' and self.decoder_type == 'udp':
            decoder_path = self.decoder_path['udp']
            udp_server_lst = []
            for i in range(len(self.json_params["udp_server"])):
                udp_serv = {}
                t.log(self.json_params["udp_server"][i])
                udp_serv['address'] = self.json_params["udp_server"][i]["address"]
                udp_serv["port"] = self.json_params["udp_server"][i]["port"]
                udp_serv['stype'] = self.json_params["udp_server"][i]["stype"]
                udp_server_lst.append(dict(udp_serv))
            t.log(level='INFO', message=udp_server_lst)
            jv_json = \
                {
                    "udp_server": udp_server_lst,
                    "source_ips": self.json_params["source_ips"],
                    "detail_logging": self.json_params["detail_logging"],
                    "influx" : {
                        "server" : self.jv_db_server,
                        "port" : 8086,
                        "dbname" : self.db_name,
                        "measurement" : db_measure,
                        "user" : tv['uv-db-username'],
                        "password" : tv['uv-db-password'],
                        "recreate" : True
                    }
                }
            t.log(level='info', message=jv_json)    
        elif self.type == 'go' and self.decoder_type == 'gnmi':
            decoder_path = self.decoder_path['gnmi']
            gnmi_dict = {}
            plist = []
            path = {}
            for i in range(len(path_list)):
                t.log(path_list[i])
                path['path'] = path_list[i]
                if self.json_params[path_list[i]].get('freq'):
                    path['freq'] = int(self.json_params[path_list[i]]['freq'])
                #path['gnmi_submode'] = int(self.json_params[path_list[i]]['gnmi_submode'])
                if self.json_params[path_list[i]].get('gnmi_submode'):
                    path['gnmi_submode'] = int(self.json_params[path_list[i]]['gnmi_submode'])
                if self.json_params[path_list[i]].get('gnmi_suppress_redundant'):
                    path['gnmi_suppress_redundant'] = int(self.json_params[path_list[i]]['gnmi_suppress_redundant'])
                if self.json_params[path_list[i]].get('gnmi_heartbeat_interval'):
                    path['gnmi_heartbeat_interval'] = int(self.json_params[path_list[i]]['gnmi_heartbeat_interval'])
                plist.append(dict(path))
            gnmi_dict = self.gnmi_params
            gnmi_dict['mode'] = int(gnmi_dict['mode'])
            gnmi_dict['encoding'] = int(gnmi_dict['encoding'])
            t.log(level='INFO', message=plist)

            jv_json = \
                {
                    "host": dut_ip,
                    "user": "regress",
                    "password": "MaRtInI",
                    "port": decoder_port,
                    "cid": self.cid,
                    "influx" : {
                        "server" : self.jv_db_server,
                        "port" : 8086,
                        "dbname" : self.db_name,
                        "measurement" : db_measure,
                        "user" : tv['uv-db-username'],
                        "password" : tv['uv-db-password'],
                        "recreate" : True
                    },
                    "gnmi" : gnmi_dict,
                    "grpc" : {
                        "ws" : 1048576
                    },
                    "paths": plist
                }
            t.log(level='info', message="gnmi_json is")
            t.log(level='info', message=jv_json)
        else:
            t.log(level='error', message='incorrect arguments')
        with open(json_filename, 'a+')as json_file:
            try:
                json.dump(jv_json, json_file)
            except TypeError:
                t.log('error', "TypeError in the dict for json file")
            except ValueError:
                t.log('error', "ValueError in the dict for json file")
            except:
                t.log('error', "OtherError is found in the dict for json file")
        json_file.close()

        # get the resource name  based on jv_server  passed  from tv dict
        # import pdb; import sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        tv_keys = list(tv.keys())
        tv_values = list(tv.values())
        try:
            if jv_server in tv_values:
                server=tv_keys[tv_values.index(jv_server)].split('__')[0]
                jv_server = t.get_handle(resource=server)
            else:
                jv_server = connect_to_device(host=jv_server)
        except Exception as exp:
            raise TobyException("Error: " + str(exp), host_obj=self)
        decoder_path = os.path.join(decoder_path, self.json_file) 
        try:
            upload_file(jv_server, local_file=json_filename, remote_file=decoder_path, user='root', password='Embe1mpls')
        except Exception as exp:
            raise TobyException('Upload failed with Error: ' + str(exp), host_obj=self)
        t.log("json file " + json_filename + " uploaded onto decoding server.")
        self.copy_to_db(self.jv_db_server)

    def copy_to_db(self, db_server):
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(db_server, username='root', password='Embe1mpls')
            with SCPClient(ssh.get_transport()) as scp:
                t.log('info', self.json_filename)
                json_path = "/opt/json/"
                try:
                    ssh.exec_command("mkdir "+ json_path)
                except:
                    t.log("ERROR", "Directory could not be created")
                #decoder_path = os.path.join(self.decoder_path['grpc'], self.json_file)
                t.log('info', json_path)
                scp.put(self.json_filename, json_path)
                t.log("json file " + self.json_filename + " uploaded onto db server.")
                scp.close()
            ssh.close()
            os.remove(self.json_filename)
        except (paramiko.BadHostKeyException, paramiko.AuthenticationException,
                paramiko.SSHException, socket.error) as err:
            t.log("ssh and scp error found: " + str(err))
        except:
            raise RuntimeError("Unknown error found")

    def get_json_filename(self):
        """
        Return filename for DB query result

        Example:
        ${json_filename} =  get json filename
        """
        return self.db_path

    def jv_db_init(self):
        """
        Create/Initialize InfluxDB object
        """
        t['user_variables']['uv-db-host'] = self.jv_db_server
        self.db_obj = InfluxDB(dbname=self.db_name, t=t)
        self.db_obj.db_init()
        t.log(level='info', message=self.db_obj)

    def jv_db_query(self, query):
        """
        Query DB with query
        :param: query: query passed from the user
        """
        return self.db_obj.db_query(query)
