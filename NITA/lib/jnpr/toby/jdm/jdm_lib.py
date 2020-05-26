"""
Python file containing functions specific to JDM platform

Author(s):
  Sudhir Akondi (sudhira@juniper.net)
"""

from jnpr.toby.hldcl.device import execute_cli_command_on_device
import re

class jdm_lib:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def get_expected_system_inventory_nfx(self, model):
        """
        Function that returns the expected system inventory based on the NFX model.

        Python Example:
            _inventory_ = get_expected_system_inventory_nfx(model)

        Robot Example:
            ${inventory}   Get Expected System Inventory   model=nfx150

            ${model}       Get Model    device=${r0}
            ${inventory}   Get Expected System Inventory   model=${model}

        :params str model:
          **REQUIRED** Model of the NFX

        :returns:
          Dictionary of Inventory with keys as below:
             cpu,
             hyper_thread,
             cores,
             logical_cpu
        """
        try:

            model = str(model)
            _cpu_ = 0
            _ht_ = 0
            if re.match(r".*ls1.*", model):
                _cpu_ = 4
                _ht_ = 2
            elif re.match(r".*250*", model):
                _cpu_ = 6
                _ht_ = 2
            elif re.match(r".*150_c.*", model):
                _cpu_ = 4
                _ht_ = 1
            elif re.match(r".*150.*", model):
                _cpu_ = 8
                _ht_ = 1
            else:
                raise Exception("Unknown Model: %s, unable to fetch expected system inventory" % model)

            _return_dict_ = {
                "cpu" : _cpu_,
                "hyper_thread" : _ht_,
                "cores" : _cpu_,
                "logical_cpu" : _cpu_ * _ht_
            }
            return True, _return_dict_

        except Exception as _exception_:
            raise Exception("Exception found in get_expected_system_inventory: %s : %s" % (type(_exception_), _exception_))

    def fetch_cpu_usage(self, device_handle):

        """
        Function to fetch the Usage percentage of the CPU using the command show system visibility cpu from JDM

        Python Example:
            _cpu_usage_ = fetch_cpu_usage(device_handle=r0_handle)

        Robot Example:
            ${cpu_usage}  Fetch CPU Usage   device_handle=${r0_handle}

        :params str device_handle:
          **REQUIRED** Device Handle of JDM

        :return:
          Dictionary of Logical CPU as keys and percentage usage as values
        """
        try:

            _cmd_ = "show system visibility cpu"
            _output_ = execute_cli_command_on_device(device=device_handle, command=_cmd_)

            _cpu_usage_flag_ = False
            _return_dict_ = {}
            _found_ = False
            for _row_ in _output_.split("\n"):

                _match_ = re.match(r".*CPU\s+Usages.*", _row_)
                if _match_ is not None:
                    _cpu_usage_flag_ = True
                    continue

                _match_ = re.match(r".*CPU\s+Pinning.*", _row_)
                if _match_ is not None:
                    _cpu_usage_flag_ = False
                    continue

                if _cpu_usage_flag_ is True:
                    _match_ = re.match(r"(\d+)\s+(\S+)", _row_)
                    if _match_ is not None:
                        _return_dict_[int(_match_.group(1))] = float(_match_.group(2))
                        _found_ = True

            if _found_ is False:
                raise Exception("No CPU Usage Information found in output")
            else:
                return True, _return_dict_

        except Exception as _exception_:
            raise Exception("Error: %s: %s" % (type(_exception_), _exception_))

    def fetch_cpu_pinning_info(self, device_handle, vnf_name):
        """
        Function to fetch the CPU Pinning Information for VNFs hosted on the NFX

        Python Example:
            _cpu_pin_ = fetch_cpu_pinning_info(device_handle=_dh_, vnf_name='centos-1')

        Robot Example:
            ${cpu_usage}   Fetch CPU Pinning Info   device_handle=${jdm}   vnf_name=centos-1

        :params str device_handle:
          **REQUIRED** Device handle for JDM
        :params str vnf_name:
          **REQUIRED** Name of the VNF hosted on the NFX
        :returns:
          Dictionary of logical cpu as keys and physical cpus list as value
        """
        try:

            t.log("INFO", "Fetching CPU Pinning Info of VNF: %s" % vnf_name)

            _cmd_ = "show system visibility cpu"
            _output_ = execute_cli_command_on_device(device=device_handle, command=_cmd_)

            _cpu_pinning_flag_ = False
            _return_dict_ = {}
            _found_ = False
            for _row_ in _output_.split("\n"):

                _match_ = re.match(r".*CPU\s+Pinning.*", _row_)
                if _match_ is not None:
                    _cpu_pinning_flag_ = True
                    continue

                if _cpu_pinning_flag_ is True:
                    _match_ = re.match(r"(\S+)\s+(\d+)\s+(\d+).*", _row_)
                    if _match_ is not None:
                        _vnf_ = _match_.group(1)
                        _vcpu_ = _match_.group(2)
                        _cpu_ = _match_.group(3)
                        t.log("INFO", "Match: '%s', vnf: '%s', vcpu: '%s', cpu: '%s'" %(_row_, _vnf_, _vcpu_, _cpu_))
                        if _vnf_ != vnf_name:
                            t.log("INFO", " - vnf ignored")
                            continue

                        if _vcpu_ not in _return_dict_.keys():
                            _return_dict_[_vcpu_] = [str(_cpu_)]
                        else:
                            _return_dict_[_vcpu_].append(str(_cpu_))
                        _found_ = True

            if _found_ is False:
                raise Exception("No CPU Pinning Information found for VNF: %s" % vnf_name)
            else:
                return True, _return_dict_

        except Exception as _exception_:
            raise Exception("Error: %s: %s" % (type(_exception_), _exception_))

    def verify_vnf_cpu_pinning(self, device_handle, vnf_name, ref_dict):
        """
        Function to verify the CPU Pinning details of VNF as per reference dictionary

        Python Example:
            _vnf_cpu_pin_ = { 0 : 1, 1 : 2}
            _status_ = verify_vnf_cpu_pinning(device_handle=_jdm_, vnf_name='centos-1', ref_dict=_vnf_cpu_pin)

        Robot Example:
            ${vnf_cpu_pin}   Create Dictionary    0=1   1=2
            ${status}        Verify VNF CPU Pinning    device_handle=${jdm}   vnf_name=centos-1   ref_dict=${vnf_cpu_pin}

        :param str device_handle:
          **REQUIRED** Device Handle to JDM
        :param str vnf_name:
          **REQUIRED** Name of the VNF
        :param dict  ref_dict:
          **REQUIRED** Dictionary of expected cpu pinning info as below:
             logical_cpu as key, corresponding physical_cpu as value

        :returns:  True if successful comparison, else False
        """
        try:

            t.log("INFO", "Verifying CPU Pinning info for VNF: %s , Ref Dict: %s" % (vnf_name, ref_dict))

            _status_, _cpu_dict_ = self.fetch_cpu_pinning_info(device_handle, vnf_name)
            if _status_ is False:
                t.log("ERROR", "Unable to fetch CPU Pinning Information for VNF: %s" % vnf_name)
                return False

            _return_ = True
            for _vcpu_, _cpu_set_array_ in ref_dict.items():

                if _vcpu_ not in _cpu_dict_.keys():
                    t.log("ERROR", "VCPU: '%s' not found for VNF: '%s'" % (_vcpu_, vnf_name))
                    _return_ = False
                    break

                t.log("INFO", "VCPU: '%s' found for VNF: '%s'" % (_vcpu_, vnf_name))
                for _cpu_set_ in _cpu_set_array_:
                    t.log("INFO", "Expected CPU Set: '%s' for VCPU: '%s' on VNF: '%s'"  % (_cpu_set_, _vcpu_, vnf_name))
                    if str(_cpu_set_) not in _cpu_dict_[_vcpu_]:
                        t.log("ERROR", "Expected CPU Set not found for VCPU")
                        _return_ = False
                        break

                    t.log("INFO", "CPU Set: '%s' found against VCPU: '%s' for VNF: '%s'" % (_cpu_set_, _vcpu_, vnf_name))

            if _return_ is False:
                t.log("ERROR", "CPU Pinning Info for VNF: '%s' found incorrect" % vnf_name)
                return False

            return True

        except Exception as _exception_:
            raise Exception("Exception found in verify_vnf_cpu_pinning: %s : %s" % (type(_exception_), _exception_))

    def fetch_vnf_list_from_config(self, device_handle):
        """
        Python function to get a list of VNF names configured on the JDM

        Python Example:
            _vnf_list_ = fetch_vnf_list_from_config(device_handle=_jdm_)

        Robot Example:
            ${vnf_list}  Fetch VNF List From Config   device_handle=${jdm}

        :param str device_handle:
          **REQUIRED** Device Handle of JDM

        :returns:
           List containing the VNF names
        """
        try:

            _return_list_ = []
            t.log("INFO", "Fetching Configured VNF List on device: %s" % device_handle)

            _cmd_ = "show configuration | display set | match virtual-network-functions.*image"
            _output_ = execute_cli_command_on_device(device=device_handle, command=_cmd_)

            for _row_ in _output_.split("\n"):
                _match_ = re.match(r"set\s+virtual-network-functions\s+(\S+)\s+.*", _row_)
                if _match_ is not None:
                    _return_list_.append(_match_.group(1))

            return _return_list_

        except Exception as _exception_:
            t.log("ERROR", "Exception in fetch_vnf_list_from_config: %s : %s" % (type(_exception_), _exception_))
