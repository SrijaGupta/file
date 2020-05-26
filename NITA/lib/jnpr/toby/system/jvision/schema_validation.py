"""
Copyright (C) 2019-2020, Juniper Networks, Inc.
All rights reserved.
Authors: ganeshkt, tsrinivas
Description:
    This keyword library provides Keywords for gNMI schema validation
    This library uses the Google GNMI test framework from https://github.com/openconfig/gnmitest
"""
# pylint: disable=C0103, C0301, R0914, import-error, W1401

import os
import re
import jinja2
from jnpr.toby.logger.logger import get_log_dir
from jnpr.toby.hldcl.device import Device
import time
from datetime import datetime

class schema_validation(object):
    """
    Base Class for Schema_validation for gNMI
    Protocol/feature
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    def __init__(self):
        self.decoder_path = ''
        self.decoder_type = ''
        self.decoder_port = ''
        self.suite_protofile = ''
        self.junos_yang_path = None
        self.suite_file = ''
        self.suite = ''
        self.val_type = None
        self.gnmi_server = None
        self.server_ip_address = ''
        self.log_path = get_log_dir()
        self.gnmi_params = ''

    def gen_and_upload_suite_proto(self, **kwargs):
        """
        This keyword is used to generate the suite proto file which is input file to
         Gnmi test framework tool. This KW will also upload the file to server in specified path.

        :param gnmi_params  :     is a dictionary which specifies subscription details like mode,
                                  encoding,submode,frequency
        :param sensor_params:     List of sensor path details (ex: ['interfaces/interface'].
                                    no need to specify '/' at the begining of the path)
        :param gnmi_server  :     jvision server object
        :param dut_ip       :     target_device ip address
        :param dut_port     :     grpc port number (ex:50052/50051)
        :param validation_type:     type of Validation to be done.
                                   "path_validation" to create suite proto file for path_validation test
                                   "datatype_validation" to create suit proto file for value_validation test
        Example:
        ${Suite_file} =   gen and upload suite proto     gnmi_params=${gnmi_data}
            sensor_params=components/component gnmi_server=${tv['h0__name']}   dut_ip=143.2.2.2    dut_port=50052    validation_type=path_validation
        """

        json_params = kwargs.get('sensor_params')
        self.gnmi_params = kwargs.get('gnmi_params')
        self.val_type = kwargs.get('validation_type')
        self.gnmi_server = kwargs.get('gnmi_server')
        dut_ip = kwargs.get('dut_ip')
        dut_port = kwargs.get('dut_port')
        #t.log('DEBUG', str(self.json_params))
        if not json_params:
            #t.log(level="ERROR", message="json parameters are mandatory")
            raise Exception("json parameters are mandatory")
        if not dut_ip:
            #t.log(level="ERROR", message="dut_ip is mandatory")
            raise Exception("dut_ip is mandatory")
        if not dut_port:
            #t.log(level="ERROR", message="dut_port(grpc port) is mandatory")
            raise Exception("dut_port(grpc port) is mandatory")

        gnmi_dict = self.gnmi_params
        t.log(level='INFO', message=str(gnmi_dict))
        self.decoder_path = str(gnmi_dict['decoder_path'])
        decoder_path = self.decoder_path
        t.log(level='INFO', message="decoder path is :" + decoder_path)
        log_head = t.get_session_id() + '_' +  str(os.getpid())
        path_list = list(json_params.keys())
        t.log(path_list)
        z = time.localtime()
        current_time = str(z.tm_sec)
        self.suite_protofile = self.log_path + '/' + log_head + current_time + ".suiteproto"
        self.suite_file = str(log_head + current_time + ".suiteproto")
        t.log("suite file is " + self.suite_file)
        jv_json = None
        t.log("validation_type is  " + self.val_type)

        gnmi_dict = {}
        gnmi_dict = self.gnmi_params
        gnmi_dict['mode'] = int(gnmi_dict['mode'])
        gnmi_dict['encoding'] = int(gnmi_dict['encoding'])
        #t.log(level='INFO', message=plist)

        temp_json = self._get_jinja_template()  # path_validation or datatype_validation
        tmpl = jinja2.Template(temp_json)
        jv_json = tmpl.render(ip=dut_ip, port=dut_port,
                              path=path_list[0], mode=gnmi_dict['mode'], encod=gnmi_dict['encoding'],
                              sub_mode=gnmi_dict['sub_mode'], freq=gnmi_dict['freq'])
        t.log(level='info', message=jv_json)
        #dir_path = os.path.dirname(os.path.realpath(__file__))
        #t.log("directory path is "+ dir_path)
        t.log("suite proto file name is " + self.suite_protofile)
        f = open(self.suite_protofile, 'w+')
        f.write(str(jv_json))
        f.close()
        #t.log('INFO', "file closed")
        #  SCP to jv_server; use
        try:
            decoder_path = os.path.join(decoder_path, self.suite_file)
            dev_obj = Device(host=self.gnmi_server, os='unix', user='root', password='Embe1mpls')
            dev_obj.upload(local_file=self.suite_protofile, remote_file=decoder_path)
            t.log("suite proto file " + self.suite_file + " uploaded to server " + self.suite_protofile)
        except Exception as exp:
            t.log('ERROR', 'failed to upload files to jvision server: {}'.format(exp))
            return False

        return self.suite_file

    def _get_jinja_template(self):
        '''
            This method builds Jinja template based on type of validation
        '''
        tmp_json =  \
            ''' name: "Value_validation test to validate the data_type values in gNMI response"
                timeout: 20
                schema: "openconfig"
                instance_group_list: {
                    description: "instancegroup1"
                    instance: {
                        description: "instance1"
                        test: {
                            connection: {
                                target: "DUT"
                                address: "{{ip}}:{{port}}"
                                timeout: 60
                            }
                            description: "test1"
                            subscribe: {
                                request: {
                                    subscribe: {
                                        prefix: {
                                            target: "DUT",
                                            origin: "openconfig"
                                        }
                                        subscription: {
                                            path: {
                                                elem: {
                                                    name: "{{path}}"
                                                }
                                            }
                                            # submode
                                            mode: {{sub_mode}}
                                            sample_interval: {{freq}}
                                        }

                                        mode: {{mode}},
                                        encoding: {{encod}},
                                    }
                                }
                                log_responses: 1
                        '''
        val_str = ""
        if self.val_type == "path_validation":
            val_str = "        path_validation: {}"
        else:
            val_str = "        value_validation: {}"
        tmp_json = tmp_json + val_str +  \
            '''
                                    }
                                }
                            }
                        }'''
        return tmp_json

    def schema_validation(self, **kwargs):
        """
            This will invoke the schema_validation with gnmitest_cli tool on gnmi server.
            :param gnmi_server_handle:     gnmi server device handle, mandatory argument.
            :param suite_file   :     suite proto file
            :param output_file  :     report/output file
            :param decoder_path :     path where suite proto file present
            :param supress_known_errors : Boolean default value is False which is not to supress any errors ending with
                               './config/name not equal to any target nodes'
            Example:
            schema validation     gnmi_server_handle=${h0}    suite_file=intf_path.suiteproto
            output_file=intf_path.log    decoder_path=/usr/local/go/src/github.com/openconfig/gnmitest/cmd/gnmitest_cli/
        """
        self.suite = kwargs.get('suite_file')
        report = kwargs.get('output_file')
        server = kwargs.get('gnmi_server_handle')
        supress_known_errors = kwargs.get('supress_known_errors', False)

        if not self.suite:
            #t.log(level="ERROR", message="Argument suite_file is mandatory")
            raise Exception("Argument suite_file is mandatory")
        if not report:
            #t.log(level="ERROR", message="Argument output_file is mandatory")
            raise Exception("Argument output_file is mandatory")
        if not server:
            #t.log(level="ERROR", message="Argument gnmi_server_handle is mandatory")
            raise Exception("Argument gnmi_server_handle is mandatory")
        self.decoder_path = kwargs.get('decoder_path')
        res = ""
        try:
            server.shell(command='cd ' + self.decoder_path +'\n')
            server.shell(command='rm -rf ' + report +'\n')
            server.shell(command='gnmitest_cli -address localhost:11601 -suite ' + self.suite + ' -report ' + report +'\n')
            response = server.shell(command='cat ' + report + ' | grep result:' +'\n')
            res = str(response.response())
        except Exception as e:
            t.log(level='ERROR', message='Failed in execute shell command: ' + str(e))
            raise Exception(e)

        match = re.search('SUCCESS', res)
        if match:
            t.log(level='INFO', message="schema_validation completed successfully")
            t.log("for more logs check report file: " + report)
        else:
            if supress_known_errors:
                cmd = 'cat ' + report + " | grep message: | grep -v 'name not equal to any target nodes' "
                cmd_re = re.escape(cmd) + r'(\s*)?\r{1,2}?\n?'
                response = server.shell(command=cmd)
                res = str(response.response())
                res = re.sub(cmd_re, '', res)
                if res == "":
                    t.log(level="INFO", message="schema validation completed successfully (with only known_errors)")
                    return True
            else:
                response = server.shell(command='cat ' + report + ' | grep message:' +'\n')
            t.log(level="ERROR", message="schema validation errors: ")
            res = str(response.response())
            t.log(res + '\n')
            raise Exception("Schema validation failed!")
        return True

    def _get_junos_pkg(self, server, schemapath, version, pkgpath):
        path = os.path.join(schemapath, version)
        self.junos_yang_path = path
        oc_yang_pkg = os.path.basename(pkgpath) # pkg_path=/usr/local/go/src/github.com/openconfig/gnmitest/schemas/openconfig/19.4_daily/junos-openconfig-yang-19.4I-20191202.0.0031.tgz
        try:
            server.shell(command='rm -rf ' + path +'\n')
            server.shell(command='mkdir -p ' + path +'\n')
            server.shell(command='cd ' + path +'\n')
            server.shell(command='cp ' + pkgpath + '  ' + path + '\n')
            server.shell(command='tar -xvf ' + path + '/' + oc_yang_pkg + '\n')
        except Exception as e:
            t.log(level='ERROR', message='Failed in execute shell command: ' + str(e))
            raise Exception(e)

    def build_schema_modules(self, **kwargs):
        """
        This method will create update.sh and will run the same on gnmi_server.
        :param gnmi_server_handle:   Gnmi server handle
        :param gnmi_server_name:     Gnmi server Name
        :param pkg_path        :     path to junos-openconfig-yang-19.4I-20191202.0.0031.tgz file on gnmi server
        :param schema_path     :     schema path on server by default it will /usr/local/go/src/
        :param pkg_path        :     absolute path where OC_yang_package present in the server
        :param schema_path     :     path where update.sh file will be copied (incase if we cloned gnmitest suiteotherthan /usr/local/go path)

        Example:
        build schema modules      gnmi_server_handle=${h0}      gnmi_server_name=${tv['h0__name']}    version=19.4
        pkg_path=/homes/junos-openconfig-yang-19.4I-20191202.0.0031.tgz
        ...      schema_path=/usr/local/go/src/github.com/openconfig/gnmitest/schemas/openconfig
        """
        pkgpath = kwargs.get('pkg_path')
        server = kwargs.get('gnmi_server_handle')
        self.gnmi_server = kwargs.get('gnmi_server_name')
        version = kwargs.get('version')
        schemapath = kwargs.get('schema_path', '/usr/local/go/src/github.com/openconfig/gnmitest/schemas/openconfig')

        if not server:
            raise Exception("Argument gnmi_server_handle is mandatory")
        if not pkgpath:
            t.log(level="ERROR", message="junos build directory openconfig yang module package path is mandatory")
            raise Exception("junos build directory openconfig yang module package path is mandatory")
        if not version:
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d_%H:%M:%S")
            version = str(date_time)
        path = os.path.join(schemapath, version)
        self.junos_yang_path = path
        file_yang_path = os.path.join(version, 'openconfig', 'yang')
        file_aug_path = os.path.join(version, 'openconfig', 'augment')
        schema_update_file = os.path.join(schemapath, 'update.sh')
        try:
            self._get_junos_pkg(server, schemapath, version, pkgpath)
            z = time.localtime()
            current_time = str(z.tm_sec)
            server.shell(command='mv ' + schema_update_file + ' ' + schemapath + '/' + 'update.sh_' + current_time + 'bak' +'\n')
        except Exception as e:
            t.log(level='ERROR', message='Failed in execute shell command: ' + str(e))
            raise Exception(e)
        # Create Update.sh
        try:
            yang_path = os.path.join(path, 'openconfig', 'yang')
            aug_path = os.path.join(path, 'openconfig', 'augment')

            server.shell(command='cd ' + yang_path + '\n')
            #server.shell(command='pwd' + '\n')
            response = server.shell(command='ls ' + '\n')
            res = response.response()
            yang_files = res.split()
            del yang_files[0]
            types_yang_file = []
            for yang_file in yang_files:
                match = re.search('openconfig.*types.yang', yang_file)
                if match:
                    types_yang_file.append(yang_file)
            t.log(level='INFO', message="yang_file_types are : " + str(types_yang_file))
            server.shell(command='cd ' + aug_path + '\n')
            response = server.shell(command='ls ' + '\n')
            res = response.response()
            aug_files = res.split()
            del aug_files[0]
            tmp_data1 = '''runsed -i 's/This package was generated by.*/This package was generated by github.com\/openconfig\/gnmitest/g' $PACKAGE_NAME.go
gofmt -w -s $PACKAGE_NAME.go
rm -rf public deps telemetry '''
            tmp_data = '''#!/bin/bash

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Workaround to ensure that if we are running on OS X with a homebrew installed
# GNU sed then we can still run sed.
runsed() {
  if hash gsed 2>/dev/null; then
    gsed "$@"
  else
    sed "$@"
  fi
}

PACKAGE_NAME=gostructs
git clone --depth 1 https://github.com/Juniper/telemetry.git
git clone --depth 1 https://github.com/openconfig/public.git

go get -u github.com/openconfig/ygot
go get -t -d $GOPATH/src/github.com/openconfig/ygot/...

mkdir deps
cp  $GOPATH/src/github.com/openconfig/ygot/demo/getting_started/yang/{ietf,iana}* deps
go run $GOPATH/src/github.com/openconfig/ygot/generator/generator.go \\
  -path=public,deps,augment,deviation \\
  -output_file=$PACKAGE_NAME.go \\
  -package_name=$PACKAGE_NAME -compress_paths=false \\
  -generate_fakeroot -fakeroot_name=device \\
  -exclude_modules=ietf-interfaces \\
  -generate_append \\
  -generate_getters \\'''

            tmp_data = tmp_data + '\n'
            update_file = self.log_path + '/' + "update.sh"
            f = open(update_file, 'w+')
            f.write(tmp_data)
            for yang_file in types_yang_file:
                f.write('  '+ file_yang_path+ '/' + yang_file + ' ' + '\\' + '\n')
            for yang_file in yang_files:
                if re.search('ietf.*.yang', yang_file) or re.search('iana.*.yang ', yang_file) or\
                    re.search('openconfig.*types.yang', yang_file):
                    continue
                else:
                    f.write('  '+ file_yang_path+ '/' + yang_file + ' ' + '\\' + '\n')
            list_size = len(aug_files)
            for aug_file in aug_files:
                if list_size > 1:
                    f.write("  "+file_aug_path+"/"+ aug_file + ' ' + '\\' + '\n')
                else:
                    f.write("  "+file_aug_path+"/"+ aug_file + ' ' + '\n')
                list_size = list_size - 1
            f.write(tmp_data1)
            f.close()
            server.shell(command='chmod 755 ' + yang_path + '/*' + '\n')
            server.shell(command='chmod 755 ' + aug_path + '/*' + '\n')
            try:
                dev_obj = Device(host=self.gnmi_server, os='unix', user='root', password='Embe1mpls')
                dev_obj.upload(local_file=update_file, remote_file=schema_update_file)
                t.log("update.sh file" + " uploaded to server " + schema_update_file)
            except Exception as exp:
                t.log('ERROR', 'failed to upload files to jvision server: {}'.format(exp))
                return False

            server.shell(command='chmod 755 ' + schema_update_file + '\n')
            server.shell(command='cd ' + schemapath + '\n')
            server.shell(command='./update.sh' + '\n')
        except Exception as e:
            t.log(level='ERROR', message='Failed in execute shell command: ' + str(e))
            raise Exception(e)
        return True

    def compare_yang_models(self, **kwargs):
        """
        This API will compare Yang model files of Junos package and github.com/public repo.
        :param gnmi_server_handle:   Gnmi server handle
        :param pkg_path        :     Optional absolute path where OC_yang_package present on the server
        :param schema_path     :     Optional schema path on server by default it will /usr/local/go/src/
        Example:
           compare yang models      gnmi_server_handle=${h0}  pkg_path=/homes/junos-openconfig-yang/junos-18.2.tgz
        """
        server = kwargs.get('gnmi_server_handle')
        pkgpath = kwargs.get('pkg_path')
        version = kwargs.get('version')
        schemapath = kwargs.get('schema_path', '/usr/local/go/src/github.com/openconfig/gnmitest/schemas/openconfig')

        if server is None:
            t.log(level='ERROR', message='gnmi_server_handle is mandatory for compare_yang_model')
            raise Exception("gnmi_server_handle is mandatory for compare_yang_model")
        if not pkgpath:
            t.log(level="ERROR", message="junos build directory openconfig yang module package path is mandatory")
            raise Exception("junos build directory openconfig yang module package path is mandatory")
        if not version:
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d_%H:%M:%S")
            version = str(date_time)

        path = os.path.join(schemapath, version)
        self.junos_yang_path = os.path.join(path, '/openconfig/yang/openconfig*')
        oc_dir_name = os.path.join(schemapath, "github.com/")  # public will be crearted after git clone

        try:
            self._get_junos_pkg(server, schemapath, version, pkgpath)
            server.shell(command='mkdir -p ' + oc_dir_name +'\n')
            server.shell(command='cd ' + oc_dir_name +'\n')
            server.shell(command="git clone  --quiet --depth 1 https://github.com/openconfig/public.git . > /dev/null")  # a folder named public ?

            sh_file_data = '''#!/bin/bash

# This file is auto generated.

for file in '''
            sh_file_data += self.junos_yang_path+"/openconfig/yang/openconfig*"+'''
do
        #echo $file
        filename=$(basename $file)
        line="$(grep "oc-ext:openconfig-version" $file)"
        line='+\s*'$line
        line1=$(echo $line | sed 's/"/\\"/g')
        gitfile=$(find . -name $filename)
        if [ ! -z $gitfile ] ; then
        #echo $gitfile"+++++++++++++++++"
                #echo $line1
                #echo "Doing diffing for $gitfile"
                for hash in $(git log  --pretty=format:"%H" $gitfile )
                #for hash in $(git log $gitfile | grep "^commit " | sed 's/^commit //g')
                do
                        #echo "$hash"
                        git show $hash $gitfile | grep -q "$line1"
                        if [ $? -eq 0 ]; then
                                #echo "Checking out $gitfile"
                                git checkout $hash $gitfile
                                #echo "Running diff for $filename"
                                diff -uw $file $gitfile >diffs
                                if [ $? -ne 0 ]; then
                                        echo "$filename has below diff:"
                                        echo "+++++++++++++++++++++++++++++++++++++++"
                                        cat diffs
                                        echo "+++++++++++++++++++++++++++++++++++++++"
                                fi
                                break
                        fi
                done
        fi
done'''
            sh_file = os.path.join(self.log_path, "compare_yang_models.sh")
            f = open(sh_file, 'w')
            f.write(sh_file_data)
            f.close()
            
            sh_remote_file = os.path.join(oc_dir_name, "compare_yang_models.sh")
            try:
                host_name = server.current_node.current_controller.host
                dev_obj = Device(host=host_name, os='unix', user='root', password='Embe1mpls')
                dev_obj.upload(local_file=sh_file, remote_file=sh_remote_file)
                t.log(level='DEBUG', message="compare_yang_models.sh file" + " uploaded to server " + sh_remote_file)
            except Exception as exp:
                t.log('ERROR', 'failed to upload file to jvision server: {}'.format(exp))
                return False

            server.shell(command='chmod 755 ' + sh_remote_file + '\n')
            output = server.shell(command='./compare_yang_models.sh' + '\n').resp
            if output == "":
                t.log(level='ERROR', message='No output after invoking compare_yang_models.sh!')
            else:
                sh_output_file = os.path.join(self.log_path, "compare_yang_models.sh.out")
                f = open(sh_output_file, 'w')
                f.write(output)
                f.close()
                t.log(level='INFO', message="The YANG models diff file is at "+sh_output_file)
                server.shell(command='rm -rf '+oc_dir_name+'\n')
        except Exception as e:
            t.log(level='ERROR', message='Failed in execute shell command: ' + str(e))
            raise Exception(e)

        return True


    def pyang_validation(self, **kwargs):
        """
        This API will compare Yang model files of Junos package and github.com/public repo.
        :param gnmi_server_handle:   Gnmi server handle, this parameter is Mandatory
        :param pkg_path        :     Mandatory absolute path where OC_yang_package present on the server
                                       pkg_path=/usr/local/go/src/github.com/openconfig/gnmitest/schemas/openconfig/19.4_daily/junos-openconfig-yang-19.4I-20191202.0.0031.tgz
        :param schema_path     :     Optional schema path on server by default it will /usr/local/go/src/
        :param version         :     Optional parameter Version, if not given current date/time is used.
        :paramt format         :     Pyang tool output formats, jstree by default
        :param outputfile      :     output filename for Pyang tool, by default junos_oc_path_output.html

        Example:
            Pyang Validation      gnmi_server_handle=${h0}  pkg_path=/usr/local/go/src/github.com/openconfig/gnmitest/schemas/openconfig/19.4_daily/junos-openconfig-yang-19.4I-20191202.0.0031.tgz   format=jstree    outputfile=junos_oc_path_output_19.4.html
        """

        server = kwargs.get('gnmi_server_handle')
        pkgpath = kwargs.get('pkg_path')
        version = kwargs.get('version')
        schemapath = kwargs.get('schema_path', '/usr/local/go/src/github.com/openconfig/gnmitest/schemas/openconfig')
        pyang_format = kwargs.get('format', "jstree")
        outputfile = kwargs.get('outputfile', "junos_oc_path_output.html")
        self.gnmi_server = server

        if server is None:
            t.log(level='ERROR', message='gnmi_server_handle is mandatory for compare_yang_model')
            raise Exception("gnmi_server_handle is mandatory for compare_yang_model")
        if not pkgpath:
            t.log(level="ERROR", message="junos build directory openconfig yang module package path is mandatory")
            raise Exception("junos build directory openconfig yang module package path is mandatory")
        if not version:
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d_%H:%M:%S")
            version = str(date_time)

        junos_oc_path = os.path.join(schemapath, version)
        pyang_dir = os.path.join(schemapath, "pyang/")  # public will be crearted after git clone
        try:
            self._get_junos_pkg(server, schemapath, version, pkgpath)
        except Exception as e:
            t.log(level='ERROR', message='Failed in get Junos pkg; ' + str(e))
            raise Exception(e)
        output_file_path = os.path.join(self.log_path, outputfile)
        try:
            server.shell(command='rm -rf ' + pyang_dir +'\n')
            server.shell(command='mkdir -p ' + pyang_dir +'\n')
            server.shell(command='cd ' + pyang_dir +'\n')
            server.shell(command="git clone --quiet https://github.com/mbj4668/pyang.git . > /dev/null")  # a folder named public ?
            server.shell(command="pip install -q lxml")
            server.shell(command="source env.sh")
            pyang_ver = server.shell(command="source env.sh; pyang -v").resp
            t.log(level='INFO', message="Pyang version is "+pyang_ver)
            server.shell(command="source env.sh; pyang -p "+junos_oc_path+"/openconfig/  -o "+outputfile+" -f "+pyang_format+ " `find "+junos_oc_path+ " | egrep \"\.yang$\"`")
            try:
                host_name = server.current_node.current_controller.host
                dev_obj = Device(host=host_name, os='unix', user='root', password='Embe1mpls')
                remote_file = os.path.join(pyang_dir, outputfile)
                dev_obj.download(local_file=output_file_path, remote_file=remote_file)
                t.log(level='INFO', message="Pyang tool output file is at "+ output_file_path+"/"+remote_file)
            except Exception as exp:
                t.log('ERROR', 'failed to download file from jvision server: {}'.format(exp))
                return False
            server.shell(command='rm -rf ' + pyang_dir +'\n')
            server.shell(command='rm -rf ' + self.junos_yang_path + '\n')
        except Exception as e:
            t.log(level='ERROR', message='Failed in execute shell command: ' + str(e))
            raise Exception(e)

        return True
