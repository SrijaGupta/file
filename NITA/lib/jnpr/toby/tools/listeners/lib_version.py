#!/usr/bin/python3
"""
   lib_version.py
      this is listener used to capture file versions for robot/yaml files. This needs to be invoked by toby cli
      The blob version will be encoded into each file using syntax "# $Id : <blob-id> $"
      This listener methods will be invoked based on event and will fetch the version info by parsing the file
      and the same is recorded in latest_toby_logs/toby_exec.yaml file
"""
# pylint: disable=W0612,W0613,anomalous-backslash-in-string,inconsistent-return-statements,locally-disabled,old-style-class,locally-disabled,invalid-name,import-error,locally-disabled

from robot.libraries.BuiltIn import BuiltIn
import os
import ruamel.yaml as yaml
import subprocess
import sys
import re
sys.stdout.flush()


class lib_version():
    """
       Lib_version Listener is being used by toby cli interface to capture the current execution
       run Library files being imported in robot files.
       It fetches the $Id : <version-num> from each file and dumps it into latest_toby_logs/toby_exec.yaml
       Please note that it ignores jnpr.toby package files, BuiltIn library and other robot libraries files
       which are listed at: https://github.com/robotframework/robotframework/tree/master/src/robot/libraries
       as the $Id:<verison> format is only applicable for robot files and yaml files.
    """
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self._ctx = None
        self._testname = None
        self._continue = False
        self._file_names = {}

    def start_suite(self, name, attrs):
        """
            start_suite api method
        """
        if not re.search('/jnpr/toby', attrs['source']):
            self._file_names[attrs['source']] = 1
        self._print_versions()

    def library_import(self, name, attrs):
        """
            library_import api method, invoked when an library import is done
        """
        if attrs['importer'] is not None and re.search('/jnpr/toby', attrs['source']) is None \
            and re.search('/robot/libraries', attrs['source']) is None:
            self._file_names[attrs['source']] = 1

    def resource_import(self, name, attrs):
        """
            resource_import api method
        """
        if attrs['importer'] is not None and re.search('/jnpr/toby', attrs['source']) is None \
            and re.search('/robot/libraries', attrs['source']) is None:
            self._file_names[attrs['source']] = 1

    def variables_import(self, name, attrs):
        """
            variable_import method, invoked when variable import is done
        """
        if attrs['importer'] is not None and re.search('/jnpr/toby', attrs['source']) is None \
            and re.search('/robot/libraries', attrs['source']) is None:
            self._file_names[attrs['source']] = 1

    @staticmethod
    def add_to_toby_exec(under_key, data_dict, add_under_key=True):
        """
        This method will update the toby_exec.yaml with the data given to it
        :param under_key: Specify the key under which the data_dict has to be appended in toby_exec.yaml
        :param data_dict: Data dictionary that will be added under specified key ( under_key)
        :param add_under_key: Add under_key to the toby_exec.yaml if add_under_key is set to True
        :return: None
        """
        try:
            built_in = BuiltIn()
            output_dir = built_in.get_variable_value('${OUTPUT DIR}')
            output_file = output_dir + "/toby_exec.yaml"
            if os.path.exists(output_file):
                loaded_yaml = yaml.YAML().load(open(output_file))
                if add_under_key:
                    if under_key not in loaded_yaml.keys():
                        loaded_yaml.update({under_key: dict()})
                loaded_yaml[under_key].update(data_dict)
                with open(output_file, 'w') as toby_exec_file:
                    yaml.YAML().dump(loaded_yaml, toby_exec_file)
            else:
                return False
        except IOError as exp:
            pass

    def _print_versions(self):
        """
            method to fetch blob version from file
            The blob version will be encoded into each file using syntax "$Id : <blob-id> $"
            following method will fetch this blob id and logs it in log file when suite execution starts
        """
        built_in = BuiltIn()
        output_dir = built_in.get_variable_value('${OUTPUT DIR}')
        output_file = output_dir + "/toby_exec.yaml"
        for file_name, _ in self._file_names.items():
            file_version = self._fetch_version(file_name) or "None"
            self.add_to_toby_exec(under_key="dependent_files", data_dict={file_name: file_version})

    @staticmethod
    def _fetch_version(file_name):
        """
        fetch_version is private metnod to fetch verion info from file
        """
        cmd = 'grep -oE "\\\$\s*Id\s*:\s*([a-f0-9A-F]+)\s*" ' + file_name + ' | cut -d " " -f2 '
        try:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, _ = proc.communicate()
            proc.wait()
            out = out.decode("utf-8")
            if out != "":
                out = out.rstrip('\n')
            return out
        except Exception as exp:
            pass

