"""
Author          : Gaurav Sinha
Created         : 29 August 2016.
Last Modified   : 14 August 2017.

Purpose : Uses HLT API based Spirent Traffic Verification.
          Supports multiplication factor, tolerance.
"""


import json
import re
import yaml
import copy # For Deep Copy.


class RT_PDT_Traffic_Verification_Data(object):
    # ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    """
    Data Structure for storing Router Tester values which would be reused.
    These include handles(port, device, router, streamblock), last results, etcetera.

    These could have been stored under "rt_handle" object directly but creating so many
    properties right under "rt_handle", which itself contains properties defined in Toby,
    would not be a nice way. It could possibly lead to overwriting of a property already
    present under "rt_handle" object.
    Instead, I am creating a property named "pdtobj" under "rt_handle" object and storing
    all these properties inside "pdtobj".

    To uniquely identify a streamblock, we need to use(tx port, streamblock) since in case
    of bidirectional streamblocks, handles are same.
    HLTAPI traffic_config returns:
    {'stream_id': {'port2': 'streamblock1'}} when 'bidirectional': 1 is provided to it.
    {'status': '1', 'stream_id': 'streamblock1'} when no 'bidirectional' key is provided to it.
    """

    def __init__(self, rt_handle):
        """
        Constructor to initialize class variables which would hold, among other things,
            -   the spirent config dict,
            -   emulated device and stream block handles,
            -   other needed maps.

        Args:
            rt_handle(mandatory): Toby Router Tester Handle.

        Returns:
            None
        """

        self.rt_handle = rt_handle

        self.yaml_file = "" # YAML file name.


        self.yaml_dict = {} # Dict containing the entire YAML file.

        """
        Stores Device, Router,Route, LSA, etc handles. Basically, all handles except port handles.
        """
        self.stc_handle_map = {}


        """
        Stores Params notational port name to actual port name map.
            Key = Notational Params Style name.
            Value = Actual Port name.
        For example,
            self.notational_to_actual__port_map = {
                "R0RT0_1_IF"    : "/2/5",
                "R0RT0_1_IF"    : "/2/6",
            }
        """
        self.notational_to_actual__port_map = {}


        """
        Stores port handles only.
            Key = notational TG port name.
            Value = Port handle.
        For example,
            self.stc_port_handle_map = {
                "R0RT0_1_IF"    : "port1",
                "R0RT0_1_IF"    : "port2",
            }
        """
        self.stc_port_handle_map = {}


        """
        Stored the Streamblock handle to Streamblock label mapping.
        For example,
            self.stc_sb_handle_to_label_map = {
                "streamblock18" : "BS__R0_host__to__R3_ospf_routes",
                "streamblock2"  : "BS__R2_host__to__R0_bgp_routes",
            }
        """
        self.stc_sb_handle_to_label_map = {}


        """
        Stores a list of streamblocks against each tag.
        This is done based on the tags mentioned under that streamblock in YAML file.
        """
        self.tag_to_sb_map = {}

        """
        Dict to store the multiplication factor for streamblocks.
        Sample:
            multiplication factor = {
              "port15": {
                "streamblock5": 1.0,
               },
               "port1": {
                 "streamblock8": 2.5,
               },
               "port6": {
                 "streamblock16": 5.0,
               },
            }
        """
        self._sb_multiplication_factor_map = {}


        """
        Constants.
        """
        self.TG_TRAFFIC_CONFIG__LABEL = "TG_TRAFFIC_CONFIG"
        self._do_not_rely_on_spirent_dropped_pkts = True # If this is set to "True",
        # rx.dropped_pkts count will get computed by "tx.total_pkts" - "rx.total_pkts".
        # This flag, right now, affects only the Aggregate Streamblock stats computation
        # (and not the detailed one; need to add it there too).
        self.USE_CONFIGURED_SB_TX_RATES = True # Do not fetch live tx fps rates for
        # streamblocks from Spirent. Fetching live rates takes a lot of time, especially
        # as we scale up.


        # Traffic Verification.
        self.stats_data = {}
        self.stats_tx_rate_data = {} # Stream wise.

        """
        self.stats_tx_rate_data_sb = {
            src_port_handle: {
                sb_handle : rate_value_in_fps
            },
        }

        Example,
        self.stats_tx_rate_data_sb = {
            port1: {
                streamblock8: 10000
            },
        }
        """
        self.stats_tx_rate_data_sb = {} # Streamblock wise.

        self.port_map = {}
        self.sb_map = {}
        self.sb_group_map = {}

        self.tolerance_user = {} # Stores what the user provided.
        self.tolerance = {} # Computed based on ports and stream blocks in the actual traffic stats.

        self.conv_result = {} # Stores Last Convergence(Detailed Stream block) Result.

        self.agg_traffic_stats = {} # Stores Last Aggregated Stream block stats.




def pdt_rt_initialize_yaml(rt_handle, yaml_file, sb_handle_var_dict, resource, **kwargs):
    """
    Initializes the Spirent port, device, stramblock Handles based Toby Router Tester Handle data.

    Parse Verify RT YAML file for Toby.
    Initializes global variables like those for multiplication factor.

    Args:
        rt_handle(mandatory): Toby Router Tester Handle.

        yaml_file(str, mandatory): Verify RT YAML file name.
        sb_handle_var_dict(dict, mandatory): Toby CV variable dict for getting streamblock
          handles from their correspoding CV var names.
        resource(str, mandatory): Notational RT device name as in Config YAML file. Example: "rt0".
        **kwargs:
            rt_notational_name(str, optional): YAML file notational device name for Router Tester.

    Returns:
        rt_data: PDT RT Data Object.
    """
    this_kwargs = {}
    if "rt_notational_name" in kwargs:
        this_kwargs = {
            "rt_notational_name" : kwargs["rt_notational_name"]
        }
    kwargs.pop("rt_notational_name", None)
    rt_data = pdt_rt_initialize_handles(
        rt_handle,
        **this_kwargs
    )

    yaml_file_data_as_string = kwargs.pop("yaml_file_data_as_string", "")


    pdt_rt_parse_yaml_file(
        yaml_file,
        sb_handle_var_dict,
        resource,
        yaml_file_data_as_string,
        rt_data=rt_data,
        **kwargs
    )

    return rt_data


def pdt_rt_initialize_handles(rt_handle, **kwargs):
    """
    Initializes the Spirent port, device, stramblock Handles based Toby Router Tester Handle data.

    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        **kwargs:
            rt_notational_name(str, optional): YAML file notational device name for Router Tester.

    Returns:
        rt_data: PDT RT Data Object.
    """

    rt_data = RT_PDT_Traffic_Verification_Data(rt_handle)
    t.log(level="debug", message="rt_data = ["+repr(rt_data)+"] ")

    if "rt_notational_name" in kwargs:
        rt_notational_name = kwargs["rt_notational_name"]
    else:
        rt_notational_name = "rt0"


    t.log(level="debug", message="rt_handle.port_to_handle_map = ["+json.dumps(rt_handle.port_to_handle_map, sort_keys=True, indent=4)+"] ")
    port_list = list(rt_handle.port_to_handle_map.keys())

    for port_item in port_list:
        port_handle = rt_handle.port_to_handle_map[port_item]


    for port_item in port_list:
        port_handle = rt_handle.port_to_handle_map[port_item]
        port_notational_name_list = list(
            t.t_dict['resources'][rt_notational_name]['interfaces'].keys()
        )
        for port_notational_name in port_notational_name_list:
            if t.t_dict['resources'][rt_notational_name]['interfaces'][port_notational_name]['name'] == port_item:
                port_notational_name__link = t.t_dict['resources'][rt_notational_name]['interfaces'][port_notational_name]['link']

                rt_data.stc_port_handle_map[port_notational_name__link] = port_handle
                rt_data.port_map[port_handle] = port_notational_name__link
                rt_data.notational_to_actual__port_map[port_notational_name__link] = port_item

    t.log(level="debug", message="rt_data.stc_port_handle_map = ["+json.dumps(rt_data.stc_port_handle_map, sort_keys=True, indent=4)+"] ")
    t.log(level="debug", message="rt_data.port_map = ["+json.dumps(rt_data.port_map, sort_keys=True, indent=4)+"] ")
    t.log(level="debug", message="rt_data.notational_to_actual__port_map = ["+\
        json.dumps(rt_data.notational_to_actual__port_map, sort_keys=True, indent=4)+"] ")
    return rt_data


def pdt_rt_parse_yaml_file(yaml_file, sb_handle_var_dict, resource, yaml_file_data_as_string, rt_data=None):
    """
    Parse Verify RT YAML file for Toby.
    Initializes global variables like those for multiplication factor.

    Args:
        yaml_file(str, mandatory): Verify RT YAML file name.
        sb_handle_var_dict(dict, mandatory): Toby CV variable dict for getting streamblock
          handles from their correspoding CV var names.
        resource(str, mandatory): Notational RT device name as in Config YAML file. Example: "rt0".
        rt_data(mandatory): PDT RT Data Object.

    Returns:
        None
    """

    rt_data.yaml_file = yaml_file
    rt_data.yaml_file_data_as_string = yaml_file_data_as_string

    if rt_data.yaml_file or rt_data.yaml_file_data_as_string:
        _load_yaml_file(
            rt_data=rt_data,
            yaml_file=rt_data.yaml_file,
            yaml_file_data_as_string=rt_data.yaml_file_data_as_string,
        )
    else:
        raise Exception("""No YAML file provided to parse.
        rt_data.yaml_file = ["""+repr(rt_data.yaml_file)+"""]
        rt_data.yaml_file_data_as_string = ["""+repr(rt_data.yaml_file_data_as_string)+"""]
        """)

    _populate_stc_sb_handle_to_label_map_toby(
        rt_data=rt_data,
        yaml_dict=rt_data.yaml_dict,
        sb_handle_var_dict=sb_handle_var_dict,
        resource=resource,
    )

    _populate_sb_tag_map(
        rt_data=rt_data,
    )

    _set_multiplication_factor_for_sb_handle_list_toby(
        rt_data=rt_data,
        yaml_dict=rt_data.yaml_dict,
        sb_handle_var_dict=sb_handle_var_dict,
        resource=resource,
    )

    _populate_streamblock_tolerance_hash_toby(
        rt_data=rt_data,
        yaml_dict=rt_data.yaml_dict,
        sb_handle_var_dict=sb_handle_var_dict,
        resource=resource,
    )

    return None


def _populate_stc_sb_handle_to_label_map_toby(yaml_dict, resource, sb_handle_var_dict, rt_data=None):
    """
    Populates the rt_data.stc_sb_handle_to_label_map dict for all the streamblocks in Verify RT YAML file.

    Args:
        yaml_dict(mandatory): YAML file contents as a dict.
        sb_handle_var_dict(mandatory): Toby CV variable dict for getting streamblock
          handles from their correspoding CV var names.
        resource(str, mandatory): Notational RT device name as in Config YAML file. Example: "rt0".
        rt_data(mandatory): PDT RT Data Object.

    Returns:
        None
    """
    t.log(level="debug", message=""" ======== FUNCTION [START] _populate_stc_sb_handle_to_label_map_toby ======== """)

    t.log(level="info", message="_populate_stc_sb_handle_to_label_map_toby | kwargs = ["+json.dumps(yaml_dict, sort_keys=True, indent=4)+"] ")
    t.log(level="info", message="_populate_stc_sb_handle_to_label_map_toby | kwargs = ["+json.dumps(resource, sort_keys=True, indent=4)+"] ")
    t.log(level="info", message="_populate_stc_sb_handle_to_label_map_toby | \
            kwargs = ["+json.dumps(sb_handle_var_dict, sort_keys=True, indent=4)+"] ")

    for sb_handle_var in yaml_dict["TG_TRAFFIC_CONFIG"]:
        try:
            sb_handle = sb_handle_var_dict[resource + "__" + sb_handle_var]
        except KeyError:
            raise Exception("""Streamblock Handle Variable name is not defined in RT Config file.
            Key Looked Up = ["""+repr(resource + "__" + sb_handle_var)+"""]
            sb_handle_var = ["""+repr(sb_handle_var)+"""]
            sb_handle_var_dict = ["""+repr(sb_handle_var_dict)+"""]
            """)
        rt_data.stc_sb_handle_to_label_map[sb_handle] = sb_handle_var
        if sb_handle_var not in rt_data.stc_handle_map:
            rt_data.stc_handle_map[sb_handle_var] = {}
        rt_data.stc_handle_map[sb_handle_var]["handle"] = sb_handle

    t.log(level="debug", message=""" ======== FUNCTION [END] _populate_stc_sb_handle_to_label_map_toby ======== """)
    return None


def _set_multiplication_factor_for_sb_handle_list_toby(yaml_dict, resource, sb_handle_var_dict, rt_data=None):
    """
    Sets Multiplication factor for all the streamblocks in YAML file.

    Args:
        yaml_dict(mandatory): YAML file contents as a dict.
        sb_handle_var_dict(mandatory): Toby CV variable dict for getting streamblock
          handles from their correspoding CV var names.
        resource(str, mandatory): Notational RT device name as in Config YAML file. Example: "rt0".
        rt_data(mandatory): PDT RT Data Object.

    Returns:
        None
    """
    t.log(level="debug", message=""" ======== FUNCTION [START] _set_multiplication_factor_for_sb_handle_list_toby ======== """)

    t.log(level="info", message="_set_multiplication_factor_for_sb_handle_list_toby | kwargs = ["\
        +json.dumps(yaml_dict, sort_keys=True, indent=4)+"] ")
    t.log(level="info", message="_set_multiplication_factor_for_sb_handle_list_toby | kwargs = ["+json.dumps(resource, sort_keys=True, indent=4)+"] ")
    t.log(level="info", message="_set_multiplication_factor_for_sb_handle_list_toby | kwargs = ["\
        +json.dumps(sb_handle_var_dict, sort_keys=True, indent=4)+"] ")

    for sb_handle_var in yaml_dict["TG_TRAFFIC_CONFIG"]:
        try:
            sb_handle = sb_handle_var_dict[resource + "__" + sb_handle_var]
        except KeyError:
            raise Exception("""Streamblock Handle Variable name is not defined in RT Config file.
            Key Looked Up = ["""+repr(resource + "__" + sb_handle_var)+"""]
            sb_handle_var = ["""+repr(sb_handle_var)+"""]
            sb_handle_var_dict = ["""+repr(sb_handle_var_dict)+"""]
            """)

        try:
            port_handle = yaml_dict["TG_TRAFFIC_CONFIG"][sb_handle_var]["port_handle"]
        except KeyError:
            raise Exception("""Mandatory parameter \"port_handle\" missing under streamblock stanza in Verify RT YAML file.
            sb_handle_var = ["""+repr(sb_handle_var)+"""]
            Streamblock Stanza from Verify RT YAML = ["""+repr(yaml_dict["TG_TRAFFIC_CONFIG"][sb_handle_var])+"""]
            """)

        if port_handle in rt_data.stc_port_handle_map:
            port_handle = rt_data.stc_port_handle_map[port_handle]

        try:
            multiplication_factor = yaml_dict["TG_TRAFFIC_CONFIG"][sb_handle_var]["_multiplication_factor"]
        except KeyError:
            multiplication_factor = 1.0 # default.


        # Set Multiplication Factor for this Stream Block. [START]
        _set_sb_rx_multiplication_factor(
            rt_data=rt_data,
            port_handle=port_handle,
            sb_handle=sb_handle,
            multiplication_factor=multiplication_factor,
        )
        # Set Multiplication Factor for this Stream Block. [END]

    t.log(level="debug", message=""" ======== FUNCTION [END] _set_multiplication_factor_for_sb_handle_list_toby ======== """)
    return None

def _populate_streamblock_tolerance_hash_toby(yaml_dict, resource, sb_handle_var_dict, rt_data=None):
    """
    Populates the rt_data.tolerance_user dict for all the streamblocks in YAML file.

    Args:
        yaml_dict(mandatory): YAML file contents as a dict.
        sb_handle_var_dict(mandatory): Toby CV variable dict for getting streamblock
          handles from their correspoding CV var names.
        resource(str, mandatory): Notational RT device name as in Config YAML file. Example: "rt0".
        rt_data(mandatory): PDT RT Data Object.

    Returns:
        None
    """
    t.log(level="debug", message=""" ======== FUNCTION [START] _populate_streamblock_tolerance_hash_toby ======== """)

    t.log(level="info", message="_populate_streamblock_tolerance_hash_toby | kwargs = ["+json.dumps(yaml_dict, sort_keys=True, indent=4)+"] ")
    t.log(level="info", message="_populate_streamblock_tolerance_hash_toby | kwargs = ["+json.dumps(resource, sort_keys=True, indent=4)+"] ")
    t.log(level="info", message="_populate_streamblock_tolerance_hash_toby | kwargs = ["\
        +json.dumps(sb_handle_var_dict, sort_keys=True, indent=4)+"] ")

    for sb_handle_var in yaml_dict["TG_TRAFFIC_CONFIG"]:
        try:
            sb_handle = sb_handle_var_dict[resource + "__" + sb_handle_var]
        except KeyError:
            raise Exception("""Streamblock Handle Variable name is not defined in RT Config file.
            Key Looked Up = ["""+repr(resource + "__" + sb_handle_var)+"""]
            sb_handle_var = ["""+repr(sb_handle_var)+"""]
            sb_handle_var_dict = ["""+repr(sb_handle_var_dict)+"""]
            """)

        this_streamblock_tolerance_hash = {}
        if "_tolerance" in yaml_dict["TG_TRAFFIC_CONFIG"][sb_handle_var]:
            this_streamblock_tolerance_hash = yaml_dict["TG_TRAFFIC_CONFIG"][sb_handle_var]["_tolerance"]

        if this_streamblock_tolerance_hash: # Non empty dicts evaluate to True in Python.
            for tolerance_port_label in this_streamblock_tolerance_hash:
                if tolerance_port_label not in rt_data.stc_port_handle_map:
                    raise Exception("""Did not find port handle mentioned in _tolerance.
                    tolerance_port_label = ["""+tolerance_port_label+"""]
                    rt_data.stc_port_handle_map = ["""+repr(rt_data.stc_port_handle_map)+"""]
                    """)
                tolerance_this_port_handle = rt_data.stc_port_handle_map[tolerance_port_label]
                tolerance_this_stream_id = sb_handle
                if "tx_port_sb_name" not in rt_data.tolerance_user:
                    rt_data.tolerance_user["tx_port_sb_name"] = {}
                if  tolerance_this_port_handle not in rt_data.tolerance_user["tx_port_sb_name"]:
                    rt_data.tolerance_user["tx_port_sb_name"][tolerance_this_port_handle] = {}
                if tolerance_this_stream_id not in rt_data.tolerance_user["tx_port_sb_name"][tolerance_this_port_handle]:
                    rt_data.tolerance_user["tx_port_sb_name"][tolerance_this_port_handle][tolerance_this_stream_id] = {}
                rt_data.tolerance_user["tx_port_sb_name"][tolerance_this_port_handle][tolerance_this_stream_id]\
                    = copy.deepcopy(this_streamblock_tolerance_hash[tolerance_port_label])


    t.log(level="debug", message=""" ======== FUNCTION [END] _populate_streamblock_tolerance_hash_toby ======== """)
    return None




def pdt_rt_start_traffic(rt_handle, rt_data=None, **kwargs):
    """
    Starts Router Tester traffic.

    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

    Returns:
        None
    """
    dict_to_pass = {}

    if "tag" in kwargs:
        if kwargs["tag"].strip() != "":
            if "tag_list" in kwargs:
                kwargs["tag_list"].append(kwargs["tag"])
            else:
                kwargs["tag_list"] = [kwargs["tag"]]
        kwargs.pop("tag", None)


    if ("tag_list" in kwargs) and len(kwargs["tag_list"]) == 0:
        kwargs.pop("tag_list", None)

    if ("sb_name_list" in kwargs) and len(kwargs["sb_name_list"]) == 0:
        kwargs.pop("sb_name_list", None)

    if "enable_arp" not in kwargs:
        dict_to_pass["enable_arp"] = 1
        _send_arp(
            rt_handle,
            rt_data=rt_data,
        ) # Adding this explicit sending of ARP since passing "enable_arp" to
        # "traffic_control" does not seem to send ARP. Need to raise Spirent ticket for that.
        import time
        time.sleep(10) # for debugging.

    if ("port_handle" not in kwargs) and ("port_name_list" not in kwargs) and\
        ("stream_handle" not in kwargs) and ("sb_name_list" not in kwargs) and ("tag_list" not in kwargs):
        dict_to_pass["port_handle"] = 'all'

    for key_item in dict_to_pass:
        kwargs[key_item] = dict_to_pass[key_item]

    received_data = _start_traffic(
        rt_handle,
        rt_data=rt_data,
        **kwargs
    )
    return received_data




def pdt_rt_get_stream_tx_rates(rt_handle, rt_data=None):
    """
    Collects Traffic Statistics while traffic is still running to get the stream level tx rates.

    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

    Returns:
        None
    """
    t.log(level="info", message="Call _get_stream_tx_rates(). ")
    stats_tx_rate_data = _get_stream_tx_rates(
        rt_handle,
        rt_data=rt_data,
    )

    return stats_tx_rate_data




def pdt_rt_get_streamblock_tx_rates(rt_handle, rt_data=None):
    """
    Collects Traffic Statistics while traffic is still running to get the streamblock tx rates.

    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

    Returns:
        None
    """
    stats_tx_rate_data_sb = {}
    if rt_data.USE_CONFIGURED_SB_TX_RATES is False:
        t.log(level="info", message="Call _get_sb_tx_rates(). ")
        stats_tx_rate_data_sb = _get_sb_tx_rates(
            rt_handle,
            rt_data=rt_data,
        )

    return stats_tx_rate_data_sb
    # return None




def pdt_rt_stop_traffic(rt_handle, *args, rt_data=None, **kwargs):
    """
    Stops Router Tester traffic.

    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

    Returns:
        None
    """
    t.log(level="info", message="Call _stop_traffic(). ")
    if "port_handle" not in kwargs:
        kwargs["port_handle"] = 'all'
    received_data = _stop_traffic(
        rt_handle,
        *args,
        rt_data=rt_data,
        # port_handle='all',
        **kwargs
    )
    return received_data
    # return None




def pdt_rt_verify_traffic(rt_handle, *args, rt_data=None, level="streamblock", **kwargs):
    """
    It performs two types of traffic verification: Streamblock level
      and Stream level.

    [Stream level traffic verification is Incomplete. Would be done as an enhancement.]


    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.
        level(optional): ["streamblock" |  "stream"]; Dictates granularity
          of traffic verification.

    Returns:
       (bool): Result of traffic convergence check.
    """

    if level == "stream":
        return _pdt_rt_check_traffic_stream(
            rt_handle,
            *args,
            rt_data=rt_data,
            **kwargs
        )
    elif level == "streamblock":
        return _pdt_rt_check_traffic_streamblock(
            rt_handle,
            *args,
            rt_data=rt_data,
            **kwargs
        )
    else:
        raise Exception("""Invalid value for level.
        level = ["""+repr(level)+"""]
        args = ["""+repr(args)+"""]
        kwargs = ["""+repr(kwargs)+"""]
        """)




def _pdt_rt_check_traffic_stream(rt_handle, rt_data=None, **kwargs):
    """
    [Incomplete. Would be done as an enhancement.]

    Performs Stream level traffic convergence check.

    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

    Returns:
       (bool): Result of traffic convergence check.
    """
    collected_stats = _collect_stats(
        rt_handle,
        rt_data=rt_data,
        port_handle=list(
            rt_data.stc_port_handle_map.values()
        ),
        mode="detailed_streams"
    )
    t.log(level="debug", message="Collected Traffic Stats ["+json.dumps(collected_stats, sort_keys=True, indent=4) + "] ")
    if "tolerance_label" in kwargs:
        tolerance_dict = rt_data.yaml_dict["TOLERANCE"][kwargs["tolerance_label"]]
        t.log(level="info", message="tolerance_dict = ["+json.dumps(tolerance_dict, sort_keys=True, indent=4)+"] ")

        processed_tolerance_dict = {}
        if "global" in tolerance_dict:
            processed_tolerance_dict["global"] = tolerance_dict["global"]
        if "tx_port_sb_name" in tolerance_dict:
            for sb_label_name in tolerance_dict["tx_port_sb_name"]:
                sb_handle = rt_data.stc_handle_map[sb_label_name]["handle"]
                t.log(level="info", message="sb_handle = ["+sb_handle+"] ")
                for port_name in tolerance_dict["tx_port_sb_name"][sb_label_name]:
                    port_handle = rt_data.stc_port_handle_map[port_name]
                    t.log(level="info", message="port_handle = ["+port_handle+"] ")

                    if "tx_port_sb_name" not in processed_tolerance_dict:
                        processed_tolerance_dict["tx_port_sb_name"] = {}
                    if port_handle not in processed_tolerance_dict["tx_port_sb_name"]:
                        processed_tolerance_dict["tx_port_sb_name"][port_handle] = {}
                    if sb_handle not in processed_tolerance_dict["tx_port_sb_name"][port_handle]:
                        processed_tolerance_dict["tx_port_sb_name"][port_handle][sb_handle] = {}
                    processed_tolerance_dict["tx_port_sb_name"][port_handle][sb_handle] = tolerance_dict["tx_port_sb_name"][sb_label_name][port_name]
        t.log(level="info", message="processed_tolerance_dict = ["+json.dumps(processed_tolerance_dict, sort_keys=True, indent=4)+"] ")

        return_dict = _check_conv_result(
            rt_handle,
            rt_data=rt_data,
            collect_fresh_stats=True,
            tolerance=processed_tolerance_dict,
        )
    else:
        return_dict = _check_conv_result(
            rt_handle,
            rt_data=rt_data,
            collect_fresh_stats=True,
        )
    t.log(level="info", message="return_dict from _check_conv_result = ["+json.dumps(return_dict, sort_keys=True, indent=4) + "] ")
    if "result" in return_dict:
        return return_dict["result"]
    else:
        return False




def _pdt_rt_check_traffic_streamblock(rt_handle, rt_data=None, **kwargs):
    """
    Performs Streamblock level traffic convergence check.

    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

    Returns:
       (bool): Result of traffic check.
    """
    collected_stats = _collect_stats(
        rt_handle,
        rt_data=rt_data,
        port_handle=list(
            rt_data.stc_port_handle_map.values()
        ),
        mode="streams",
    )
    t.log(level="debug", message="Collected Traffic Stats = ["+json.dumps(collected_stats, sort_keys=True, indent=4) + "] ")
    if "tolerance_label" in kwargs:
        tolerance_dict = rt_data.yaml_dict["TOLERANCE"][kwargs["tolerance_label"]]
        t.log(level="info", message="tolerance_dict = ["+json.dumps(tolerance_dict, sort_keys=True, indent=4)+"] ")

        processed_tolerance_dict = {}
        if "global" in tolerance_dict:
            processed_tolerance_dict["global"] = tolerance_dict["global"]
        if "tx_port_sb_name" in tolerance_dict:
            for sb_label_name in tolerance_dict["tx_port_sb_name"]:
                sb_handle = rt_data.stc_handle_map[sb_label_name]["handle"]
                t.log(level="info", message="sb_handle = ["+sb_handle+"] ")
                for port_name in tolerance_dict["tx_port_sb_name"][sb_label_name]:
                    port_handle = rt_data.stc_port_handle_map[port_name]
                    t.log(level="info", message="port_handle = ["+port_handle+"] ")

                    if "tx_port_sb_name" not in processed_tolerance_dict:
                        processed_tolerance_dict["tx_port_sb_name"] = {}
                    if port_handle not in processed_tolerance_dict["tx_port_sb_name"]:
                        processed_tolerance_dict["tx_port_sb_name"][port_handle] = {}
                    if sb_handle not in processed_tolerance_dict["tx_port_sb_name"][port_handle]:
                        processed_tolerance_dict["tx_port_sb_name"][port_handle][sb_handle] = {}
                    processed_tolerance_dict["tx_port_sb_name"][port_handle][sb_handle] = tolerance_dict["tx_port_sb_name"][sb_label_name][port_name]
        t.log(level="info", message="processed_tolerance_dict = ["+json.dumps(processed_tolerance_dict, sort_keys=True, indent=4)+"] ")

        return_dict = _check_agg_traffic_stats(
            rt_handle,
            rt_data=rt_data,
            collect_fresh_stats=True,
            tolerance=processed_tolerance_dict,
        )
    else:
        return_dict = _check_agg_traffic_stats(
            rt_handle,
            rt_data=rt_data,
            collect_fresh_stats=True,
        )
    t.log(level="debug", message="return_dict from _check_agg_traffic_stats = ["+json.dumps(return_dict, sort_keys=True, indent=4) + "] ")
    if "result" in return_dict:
        return return_dict["result"]
    else:
        return False




# def _load_yaml_file    [START].
def _load_yaml_file(rt_data=None, **kwargs):
    """
    Loads the YAML file containing the Spirent config and stores it as a dict.

    Args:
        rt_data(mandatory): PDT RT Data Object.
        yaml_file(str): YAML file name to parse.

    Returns:
        dict:
            result(bool): True if all worked. Otherwise, False.
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] _load_yaml_file ======== """)

    t.log(level="info", message="_load_yaml_file | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")


    return_dict = {
        "result" : True
    }

    if "yaml_file" in kwargs:
        rt_data.yaml_file = kwargs["yaml_file"]

    if "yaml_file_data_as_string" in kwargs:
        rt_data.yaml_file_data_as_string = kwargs["yaml_file_data_as_string"]

    if rt_data.yaml_file == "" and rt_data.yaml_file_data_as_string == "":
        return_dict["result"] = False
        t.log(level="debug", message=""" ======== FUNCTION [END] _load_yaml_file ======== """)
        return return_dict

    if rt_data.yaml_file_data_as_string != "":
        rt_data.yaml_dict = yaml.load(rt_data.yaml_file_data_as_string)
    else:
        with open(rt_data.yaml_file, 'r') as stream:
            try:
                rt_data.yaml_dict = yaml.load(stream.read())
            except yaml.YAMLError: # as exc:
                return_dict["result"] = False
                raise Exception("Error occurred while reading YAML file ["+rt_data.yaml_file+"]as dict. ")

    t.log(level="info", message="formatted = ["+json.dumps(rt_data.yaml_dict, sort_keys=True, indent=4) + "] ")

    t.log(level="debug", message=""" ======== FUNCTION [END] _load_yaml_file ======== """)

    return return_dict
# def _load_yaml_file    [END].




# Commeting this function since it is no longer used.
# # def _find_handle_by_label     [START].
# def _find_handle_by_label(rt_data=None, **kwargs):
#     """
#     Returns the handles returned by Spirent on execution of the "primary_label"'s command.
#
#     Raises exception if the "key_to_find" is specified but is not found
#     in "received_data" key in "rt_data.stc_handle_map[primary_label]".
#
#
#     Args:
#         Mandatory
#             rt_data(mandatory): PDT RT Data Object.
#             primary_label(str): First level key under "rt_data.stc_handle_map".
#         Optional
#             key_to_find(str): Label name to look for.
#             test_existence_only(bool): Flag to tell to only check for
#             existence of the "primary_label" and "key_to_find" in
#             "rt_data.stc_handle_map" and not return the handles.
#
#     Returns:
#         if "test_existence_only" is absent or "False" in kwargs:
#             The list / dict of handles obtained when that label's command
#             was  executed by Spirent HLT and handles were stored.
#         else:
#             True / False depending on whether "primary_label" and "key_to_find" exist in
#             "rt_data.stc_handle_map".
#     """
#
#     # t.log(level="info", message="kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")
#
#     key_to_find = "handle" # Default.
#     if "key_to_find" in kwargs:
#         key_to_find = kwargs["key_to_find"]
#
#
#     if "test_existence_only" not in kwargs:
#         kwargs["test_existence_only"] = False
#
#
#     if "primary_label" not in kwargs:
#         raise Exception("""Did not find the mandatory key 'primary_label' in kwargs.
#         kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
#         """)
#     primary_label = kwargs["primary_label"]
#
#
#     if primary_label in rt_data.stc_handle_map:
#         dict_for_lookup = rt_data.stc_handle_map[primary_label]
#     else:
#         if kwargs["test_existence_only"] is True:
#             return False
#         else:
#             raise Exception("""Did not find the mandatory key 'primary_label' in rt_data.stc_handle_map.
#             rt_data.stc_handle_map = ["""+json.dumps(rt_data.stc_handle_map, sort_keys=True, indent=4)+"""]
#             """)
#
#
#     if key_to_find == "handle":
#         return dict_for_lookup["handle"]
#     else:
#         if key_to_find in dict_for_lookup["received_data"]:
#             if kwargs["test_existence_only"] is True:
#                 return True
#             else:
#                 return dict_for_lookup["received_data"][key_to_find]
#         else:
#             if kwargs["test_existence_only"] is True:
#                 return False
#             else:
#                 raise Exception("""Did not find the mandatory key 'secondary_label' in rt_data.stc_handle_map.
#                 rt_data.stc_handle_map = ["""+json.dumps(rt_data.stc_handle_map, sort_keys=True, indent=4)+"""]
#                 """)
#     return None
# # def _find_handle_by_label     [END].




# Commeting this function since it is no longer used.
# # def _get_label_base_name  [START].
# def _get_label_base_name(**kwargs):
#     """
#     Extracts the label name by removing the slice notation markers.
#
#     For example,
#         This function takes input of below types :
#             label_base_name[0 : 10 : 2]
#             label_base_name[0 : 10]
#             label_base_name[2]
#             label_base_name
#         and returns "label_base_name".
#
#     Currently, only below characters are allowed for "label_base_name"
#        ([a-zA-Z_][a-zA-Z0-9_]+)
#
#
#     Args:
#         label(str): Label name to parse which are suspected of having sliced list
#             notation(square bracket, colon, digits).
#
#     Returns:
#         dict:
#             result(bool): True if all worked. Otherwise, False.
#             base_name(str): Label names after stripping sliced list notation.
#     """
#
#     # t.log(level="info", message="kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")
#
#     # Get base name of labels without the array index(slice) part.
#     return_dict = {
#         "result"        : False,
#         "base_name"     : None,
#         "index_part"    : None,
#         "start_raw"     : None,
#         "end_raw"       : None,
#         "step_raw"      : None,
#         "start"         : None,
#         "end"           : None,
#         "step"          : None,
#
#         "secondary_label"   : None,
#     }
#     # t.log(level="info", message="kwargs = ["+repr(kwargs)+"] ")
#
#
#     if "label" in kwargs:
#         # Four possibilities.
#         #    (a) Secondary label exists with indices too.
#         #         Examples:
#         #             label_base_name[_some_secondary_label_here_][0 : 10 : 2]
#         #             label_base_name[_some_secondary_label_here_][0 : 10]
#         #             label_base_name[_some_secondary_label_here_][2]
#
#         #    (b) Secondary label exists without index part.
#         #         Examples:
#         #             label_base_name[_some_secondary_label_here_]
#
#         #    (c) No secondary label exists but indices exist.
#         #         Examples:
#         #             label_base_name[0 : 10 : 2]
#         #             label_base_name[0 : 10]
#         #             label_base_name[2]
#
#         #    (d) Neither secondary label nor indices exist.
#         #         Examples:
#         #             label_base_name
#
#         m_obj__sec_label__indices =\
#             re.search(r"^([a-zA-Z_][a-zA-Z0-9_]+?)\[\s*([a-zA-Z_][a-zA-Z0-9_]+?)\s*\]\[\s*([0-9:\-\s]+?)\s*\]", kwargs["label"])
#
#         m_obj__sec_label = re.search(r"^([a-zA-Z_][a-zA-Z0-9_]+?)\[\s*([a-zA-Z_][a-zA-Z0-9_]+?)\s*\]", kwargs["label"])
#
#         m_obj__indices = re.search(r"^([a-zA-Z_][a-zA-Z0-9_]+?)\[\s*([0-9:\-\s]+?)\s*\]", kwargs["label"])
#
#         if (m_obj__sec_label__indices is None) and (m_obj__sec_label is None) and (m_obj__indices is None):
#             # Implies Possibility(d) explained above.
#             return_dict["result"] = True
#             return_dict["base_name"] = kwargs["label"]
#
#         elif (m_obj__sec_label is not None) and (m_obj__sec_label__indices is None) and (m_obj__indices is None):
#             # Implies Possibility(b) explained above.
#             return_dict["result"] = True
#             return_dict["base_name"] = m_obj__sec_label.group(1)
#             return_dict["secondary_label"] = m_obj__sec_label.group(2)
#
#         elif (m_obj__sec_label__indices is not None) or (m_obj__indices is not None):
#
#             if m_obj__sec_label__indices is not None:
#                 # Implies Possibility(a) explained above.
#                 return_dict["result"] = True
#                 return_dict["base_name"] = m_obj__sec_label__indices.group(1)
#                 return_dict["index_part"] = m_obj__sec_label__indices.group(3)
#                 return_dict["secondary_label"] = m_obj__sec_label__indices.group(2)
#
#             elif m_obj__indices is not None:
#                 # Implies Possibility(c) explained above.
#                 return_dict["result"] = True
#                 return_dict["base_name"] = m_obj__indices.group(1)
#                 return_dict["index_part"] = m_obj__indices.group(2)
#
#             else:
#                 raise Exception("""None of the above conditions for label_name matched. Invalid label name notation detected.
#                 kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
#                 """)
#
#
#             # Section common to both(a) and (c).
#             m_obj = re.search(r"^\s*([0-9\-]*)\s*:\s*([0-9\-]*)\s*:\s*([0-9\-]*)\s*$",\
#                 return_dict["index_part"])
#             # Do not replace "([0-9\-]*)" with "([0-9\-]+)". It is intentional.
#             if m_obj:
#                 return_dict["start_raw"] = m_obj.group(1)
#                 return_dict["end_raw"] = m_obj.group(2)
#                 return_dict["step_raw"] = m_obj.group(3)
#
#                 try:
#                     return_dict["start"] = int(m_obj.group(1))
#                 except ValueError:
#                     pass
#
#                 try:
#                     return_dict["end"] = int(m_obj.group(2))
#                 except ValueError:
#                     pass
#
#                 try:
#                     return_dict["step"] = int(m_obj.group(3))
#                 except ValueError:
#                     pass
#
#             else:
#                 m_obj = re.search(r"^\s*([0-9\-]*)\s*:\s*([0-9\-]*)\s*$", return_dict["index_part"])
#                 if m_obj:
#                     return_dict["start_raw"] = m_obj.group(1)
#                     return_dict["end_raw"] = m_obj.group(2)
#
#                     try:
#                         return_dict["start"] = int(m_obj.group(1))
#                     except ValueError:
#                         pass
#
#                     try:
#                         return_dict["end"] = int(m_obj.group(2))
#                     except ValueError:
#                         pass
#
#                 else:
#                     m_obj = re.search(r"^\s*([0-9\-]*)\s*$", return_dict["index_part"])
#
#                     if m_obj:
#                         return_dict["start_raw"] = m_obj.group(1)
#
#                         try:
#                             return_dict["start"] = int(m_obj.group(1))
#                         except ValueError:
#                             pass
#
#         else:
#             raise Exception("""None of the above conditions for label_name matched. Invalid label name notation detected.
#             kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
#             """)
#
#
#
#
#     # t.log(level="info", message="return_dict = ["+json.dumps(return_dict, sort_keys=True, indent=4)+"] ")
#
#     return return_dict
# # def _get_label_base_name  [END].




# Commeting this function since it is no longer used.
# # def _check_if_valid_handle_markers_present    [START].
# def _check_if_valid_handle_markers_present(**kwargs):
#     """
#     Checks if the handle label adheres to the angle bracket notation.
#
#     Examples of valid angle marked names shown below.
#         "<handle_name_1>"
#         "  <handle_name_2> "
#         " <  handle_name_3 > "
#
#
#     Args:
#         suspected_handle(str): Handle name to parse which are suspected of having
#             angle bracket notation.
#
#     Returns:
#        (bool): True if all worked. Otherwise, False.
#     """
#
#     # t.log(level="info", message="kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")
#
#     if "suspected_handle" not in kwargs:
#         raise Exception("""ERROR | Expected mandatory argument 'suspected_handle' is missing.
#         kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
#         """)
#
#     suspected_handle = str(kwargs["suspected_handle"]).strip()
#
#     if suspected_handle[0] == "<" and suspected_handle[-1] == ">":
#         return True
#
#     return False
# # def _check_if_valid_handle_markers_present    [END].




# # def _extract_handle_name  [START].
# def _extract_handle_name(**kwargs):
#     """
#     Examples of valid angle marked names shown below.
#         "<handle_name_1>"
#         "  <handle_name_1> "
#         " <  handle_name_1 > "
#
#     The extracted name in all the three cases shown above should be "handle_name_1".
#
#
#     Args:
#         suspected_handle(str): Handle name to parse which are suspected of having
#             angle bracket notation.
#
#     Returns:
#        (bool): Matched handle name, if all worked. Otherwise, False.
#     """
#
#     # t.log(level="info", message="kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")
#
#     if "handle_name_with_marker" not in kwargs:
#         raise Exception("""ERROR | Expected mandatory argument 'handle_name_with_marker' is missing.
#         kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
#         """)
#
#     handle_name_with_marker = str(kwargs["handle_name_with_marker"]).strip()
#
#     m_obj = re.search(r"^\s*<\s*(.+?)\s*>\s*$", handle_name_with_marker)
#
#     if m_obj:
#         return m_obj.group(1)
#
#     return None
# # def _extract_handle_name  [END].




# Commeting this function since it is no longer used.
# # def _extract_handle_list  [START].
# def _extract_handle_list(**kwargs):
#     """
#     Handles could be of type list or str(in case of hard coded handle).
#
#     If type is list,
#         check each item in list for angle brackets("<", ">").
#         If angle brackets found,
#             add it to a list which would be returned.
#     If type is str,
#         add it to a list which would be returned.
#
#
#     Args:
#         value(str): Handle name to parse which are suspected of having angle bracket notation.
#
#     Returns:
#        (list): List of handles names after stripping angle bracket notational names.
#     """
#
#     # t.log(level="debug", message=""" ======== FUNCTION [START] _extract_handle_list ======== """)
#
#     # t.log(level="info", message="kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")
#
#
#     if "value" not in kwargs:
#         raise Exception("""ERROR | Mandatory argument 'value' not found in kwargs.
#         kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
#         """)
#
#     handle_list = []
#     if type(kwargs["value"]) is str:
#         if _check_if_valid_handle_markers_present(suspected_handle=kwargs["value"]) is True:
#             handle_list = [_extract_handle_name(
#                 handle_name_with_marker=kwargs["value"]
#             )]
#
#     elif type(kwargs["value"]) is list:
#         for i in range(len(kwargs["value"])):
#             if _check_if_valid_handle_markers_present(suspected_handle=kwargs["value"][i]) is True:
#                 handle_list.append(
#                     _extract_handle_name(
#                         handle_name_with_marker=kwargs["value"][i]
#                     )
#                 )
#
#
#     # t.log(level="debug", message=""" ======== FUNCTION [END] _extract_handle_list ======== """)
#
#     return handle_list
# # def _extract_handle_list  [START].




def _populate_sb_tag_map(rt_data=None, **kwargs):
    """
    Populates the tag map for all tags present in the streamblocks.


    Args:
        rt_data(mandatory): PDT RT Data Object.
        **kwargs:
            yaml_dict(dict, optional): Spirent config dict in which to perform the check.

    Returns:
        None
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] _populate_sb_tag_map ======== """)

    t.log(level="info", message="_populate_sb_tag_map | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")


    if "yaml_dict" in kwargs:
        rt_data.yaml_dict = kwargs["yaml_dict"]

    if not rt_data.yaml_dict:
        raise Exception("""rt_data.yaml_dict is empty.
        rt_data.yaml_dict = ["""+repr(rt_data.yaml_dict)+"""]
        kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
        """)


    yaml_section_label = rt_data.TG_TRAFFIC_CONFIG__LABEL
    if "yaml_section_label" in kwargs:
        yaml_section_label = kwargs["yaml_section_label"]


    for label_item in rt_data.yaml_dict[yaml_section_label]:

        if label_item[:4].lower() != "TMPL".lower() and label_item[:2] != "__":
            if "_tag" in rt_data.yaml_dict[yaml_section_label][label_item]:
                for tag_item in rt_data.yaml_dict[yaml_section_label][label_item]["_tag"]:
                    if tag_item not in rt_data.tag_to_sb_map:
                        rt_data.tag_to_sb_map[tag_item] = []
                    rt_data.tag_to_sb_map[tag_item].append(label_item)
                rt_data.yaml_dict[yaml_section_label][label_item].pop("_tag")

    t.log(level="debug", message="rt_data.tag_to_sb_map = ["+json.dumps(rt_data.tag_to_sb_map, sort_keys=True, indent=4) + "] ")

    t.log(level="debug", message=""" ======== FUNCTION [END] _populate_sb_tag_map ======== """)
    return None


def _get_sb_list_for_tag(rt_data=None, **kwargs):
    """
    Returns streamblock list for the given tag.


    Args:
        rt_data(mandatory): PDT RT Data Object.
        **kwargs:
            tag(str): Tag name for which a list of streamblocks are to be returned.

    Returns:
       (list): List of streamblocks marked with that tag in YAML file.
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] _get_sb_list_for_tag ======== """)

    t.log(level="info", message="_get_sb_list_for_tag | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")

    if kwargs["tag"] not in rt_data.tag_to_sb_map:
        sb_list = []
    else:
        sb_list = rt_data.tag_to_sb_map[kwargs["tag"]]

    t.log(level="debug", message="sb_list = ["+json.dumps(sb_list, sort_keys=True, indent=4) + "] ")

    t.log(level="debug", message=""" ======== FUNCTION [END] _get_sb_list_for_tag ======== """)
    return sb_list




# Commeting this function since it is no longer used.
# # def _process_handles  [START].
# def _process_handles(rt_data=None, **kwargs):
#     """
#     Return the list of handles referred to in the handle label names
#     in the Python slice notation.
#
#     Example of handle names passed to this function:
#         <any_text_here>
#         <any_text_here[2:10:3]>
#         <any_text_here[_any_secondary_label_here_]>
#         <any_text_here[_any_secondary_label_here_][1:10]>
#
#     Args:
#         rt_data(mandatory): PDT RT Data Object.
#         **kwargs:
#             handle_name(str): Space separated list of Spirent device / stream block handle names.
#
#     Returns:
#         dict:
#             result(bool): True if all worked. Otherwise, False.
#             handle_list(list): Handle list as a Python "list".
#     """
#
#     # t.log(level="debug", message=""" ======== FUNCTION [START] _process_handles ======== """)
#
#     t.log(level="info", message="_process_handles | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")
#
#
#     if "handle_name" not in kwargs:
#         raise Exception("""'handle_name' not passed to this function.
#         kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
#         """)
#
#     handle_name = _extract_handle_name(handle_name_with_marker=kwargs["handle_name"])
#
#
#     handle_label_item__base_name = handle_name
#
#     handle_label_item__split_name = _get_label_base_name(label=handle_name)
#     if handle_label_item__split_name["result"] is True:
#         handle_label_item__base_name = handle_label_item__split_name["base_name"]
#         handle_label_item__sec_label = handle_label_item__split_name["secondary_label"]
#
#
#         if handle_label_item__split_name["start_raw"] is not None:
#             if handle_label_item__split_name["start"] is not None:
#                 start_value = handle_label_item__split_name["start"]
#
#                 if handle_label_item__split_name["end_raw"] is not None:
#                     if handle_label_item__split_name["end"] is not None:
#                         end_value = handle_label_item__split_name["end"]
#
#                         if handle_label_item__split_name["step_raw"] is not None:
#                             if handle_label_item__split_name["step"] is not None:
#                                 step_value = handle_label_item__split_name["step"]
#
#                                 # Eg,
#                                 # x = range(100)
#                                 # a = x[2 : 20 : 6]
#                                 return_handle_list = _find_handle_by_label(
#                                     rt_data=rt_data,
#                                     primary_label=handle_label_item__base_name,
#                                     key_to_find=handle_label_item__sec_label if handle_label_item__sec_label is not None else "handle",
#                                 )[start_value : end_value : step_value]
#                             else:
#                                 # Eg,
#                                 # x = range(100)
#                                 # a = x[2 : 20 :]
#                                 return_handle_list = _find_handle_by_label(
#                                     rt_data=rt_data,
#                                     primary_label=handle_label_item__base_name,
#                                     key_to_find=handle_label_item__sec_label if handle_label_item__sec_label is not None else "handle",
#                                 )[start_value : end_value :]
#                         else:
#                             # Eg,
#                             # x = range(100)
#                             # a = x[2 : 20]
#                             return_handle_list = _find_handle_by_label(
#                                 rt_data=rt_data,
#                                 primary_label=handle_label_item__base_name,
#                                 key_to_find=handle_label_item__sec_label if handle_label_item__sec_label is not None else "handle",
#                             )[start_value : end_value]
#                     else:
#                         # Eg,
#                         # x = range(100)
#                         # a = x[2 :]
#                         return_handle_list = _find_handle_by_label(
#                             rt_data=rt_data,
#                             primary_label=handle_label_item__base_name,
#                             key_to_find=handle_label_item__sec_label if handle_label_item__sec_label is not None else "handle",
#                         )[start_value :]
#                 else:
#                     # Eg,
#                     # x = range(100)
#                     # a = x[2]
#
#                     # NOTE
#                     #   This is not a list.
#                     #   It i user's responsibility to provide a list or an individual
#                     #   item(which could be in the form of a single member list like x[2:3] .
#                     return_handle_list = _find_handle_by_label(
#                         rt_data=rt_data,
#                         primary_label=handle_label_item__base_name,
#                         key_to_find=handle_label_item__sec_label if handle_label_item__sec_label is not None else "handle",
#                     )[start_value]
#             else:
#                 # Eg,
#                 # x = range(100)
#                 # a = x[]
#                 raise Exception("""Unexpected format.
#                 handle_label_item__split_name = ["""+repr(handle_label_item__split_name)+"""]
#                 """)
#         else:
#             # No indices found in the label name.
#             # Eg,
#             # a = x
#             return_handle_list = _find_handle_by_label(
#                 rt_data=rt_data,
#                 primary_label=handle_label_item__base_name,
#                 key_to_find=handle_label_item__sec_label if handle_label_item__sec_label is not None else "handle",
#             )
#     else:
#         # Function _get_label_base_name returned error.
#         raise Exception("""Unexpected format.
#         handle_label_item__split_name = ["""+repr(handle_label_item__split_name)+"""]
#         """)
#
#
#     # t.log(level="debug", message=""" ======== FUNCTION [END] _process_handles ======== """)
#     return return_handle_list
# # def _process_handles  [END].




# def pdt_rt_get_port_rates     [START].
def pdt_rt_get_port_rates(rt_handle, *args, rt_data=None, **kwargs):
    """
    Gets TG port rates from Spirent.


    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.
        port_name_list(list): List of port names where to start traffic.
            List of port names like: ["R0RT0_1_IF", "R0RT0_4_IF"]
        sample_count(int): Specifies the number of times to sample. Average is
            calculated based on the sample values. Default = 5.

    Returns:
       (dict): Port Traffic Rate dict returned by Spirent.
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] pdt_rt_get_port_rates ======== """)

    t.log(level="debug", message="pdt_rt_get_port_rates | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"]")

    if "port_name_list" in kwargs:
        # Sometimes, in a corner case, the user might provide few port handles\
        #   and few port names(obviously with separate keys "port_name_list" and "port_handle").
        # Handle that scenario too.
        if "port_handle" not in kwargs:
            kwargs["port_handle"] = []
        for i in range(len(kwargs["port_name_list"])):
            if kwargs["port_name_list"][i] in rt_data.stc_port_handle_map:
                kwargs["port_handle"].append(rt_data.stc_port_handle_map[kwargs["port_name_list"][i]])
            else:
                raise Exception("""Port Name = ["""+kwargs["port_name_list"][i]+"""] does not have a mapped port handle.
                rt_data.stc_port_handle_map = ["""+json.dumps(rt_data.stc_port_handle_map, sort_keys=True, indent=4)+"""]
                """)
    if "port_handle" not in kwargs or len(kwargs["port_handle"]) == 0:
        kwargs["port_handle"] = list(rt_data.stc_port_handle_map.values())

    kwargs["mode"] = 'aggregate'

    kwargs["properties"] = [
        "tx.total_pkt_rate",
        "rx.total_pkt_rate",
    ]

    sample_count = kwargs.pop("sample_count", 5)


    t.log(level="debug", message="pdt_rt_get_port_rates | kwargs sent to\
        rt_handle.sth.traffic_stats = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"]")

    i = 0
    port_rate_dict = {}
    while i < sample_count:
        this__port_rate_dict = rt_handle.invoke('traffic_stats', *args, **kwargs)

        t.log(level="debug", message="this__port_rate_dict = ["+json.dumps(this__port_rate_dict, sort_keys=True, indent=4)+"]")

        if this__port_rate_dict['status'] == '1':
            t.log(level="debug", message="rt_handle.sth.traffic_stats success. ")
        else:
            raise Exception("""rt_handle.sth.traffic_stats failed.
            kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
            this__port_rate_dict = ["""+json.dumps(this__port_rate_dict, sort_keys=True, indent=4)+"""]
            """)

        for port_item in this__port_rate_dict:
            if port_item == "status":
                continue
            try:
                rx__total_pkt_rate = float(
                    this__port_rate_dict[port_item]["aggregate"]["rx"]["total_pkt_rate"]
                )
            except ValueError:
                raise Exception("""Cannot convert the rx port rate to float for port_item=["""+repr(port_item)+"""].
                this__port_rate_dict = ["""+json.dumps(this__port_rate_dict, sort_keys=True, indent=4)+"""]
                """)
            try:
                tx__total_pkt_rate = float(
                    this__port_rate_dict[port_item]["aggregate"]["tx"]["total_pkt_rate"]
                )
            except ValueError:
                raise Exception("""Cannot convert the rx port rate to float for port_item=["""+repr(port_item)+"""].
                this__port_rate_dict = ["""+json.dumps(this__port_rate_dict, sort_keys=True, indent=4)+"""]
                """)

            if port_item not in port_rate_dict:
                if port_item not in port_rate_dict:
                    port_rate_dict[port_item] = {}

                port_rate_dict[port_item]["rx_port_rate"] = 0.0
                port_rate_dict[port_item]["tx_port_rate"] = 0.0
            port_rate_dict[port_item]["rx_port_rate"] += rx__total_pkt_rate
            port_rate_dict[port_item]["tx_port_rate"] += tx__total_pkt_rate
        i = i + 1

    # Calculate and store average.
    for port_item in port_rate_dict:
        port_rate_dict[port_item]["rx_port_rate"] = port_rate_dict[port_item]["rx_port_rate"] / sample_count
        port_rate_dict[port_item]["tx_port_rate"] = port_rate_dict[port_item]["tx_port_rate"] / sample_count


    t.log(level="debug", message="formatted port_rate_dict = ["+json.dumps(port_rate_dict, sort_keys=True, indent=4) + "] ")

    t.log(level="debug", message=""" ======== FUNCTION [END] pdt_rt_get_port_rates ======== """)

    return port_rate_dict
    # def pdt_rt_get_port_rates     [END].


# def _collect_stats     [START].
def _collect_stats(rt_handle, *args, rt_data=None, **kwargs):
    """
    Collects traffic statistics from Spirent.


    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.
        mode(str): Same as "mode" argument of Spirent HLT API's "traffic_stats" function.
        properties(list): Same as "properties" argument of Spirent HLT API's "traffic_stats"
        function.

    Returns:
       (dict): Traffic statistics dict returned by Spirent.
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] _collect_stats ======== """)

    t.log(level="debug", message="_collect_stats | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"]")

    if "mode" not in kwargs:
        # Assumption : By default, we assume that user wants to perform convergence traffic check.
        # Default "mode" is 'detailed_streams'
        kwargs["mode"] = 'detailed_streams'

    if "properties" not in kwargs:

        if kwargs["mode"] in ["detailed_streams", "streams"]:
            # Supply default "properties" field list only in case of "detailed_streams" and "streams" modes.
            kwargs["properties"] = [
                # tx.
                "tx.total_pkts",
                "tx.total_pkt_rate",
                # rx.
                "rx.duplicate_pkts",
                "rx.total_pkts",
                "rx.dropped_pkts",
                "rx.total_pkt_rate",
                "rx.rx_port",

                #(30May2017) Added during debug session; suggested by Shashank/Ashwasthy(Spirent) during webex. Remove it later.
                "rx.rx_sig_count", # Not used for any computation. Helps in debugging the traffic loss.
                "rx.out_of_sequence_pkts", # Not used for any computation. Helps in debugging the traffic loss.
            ]


    # kwargs["records_per_page"] = 256 # Added on recommendation of Spirent Support for reducing result collection time.

    t.log(level="debug", message="_collect_stats | kwargs sent to rt_handle.sth.traffic_stats = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"]")

    kwargs["scale_mode"] = 1 # Got this fix via private patch from Spirent
    # HLTAPI_4.67_GA_822707 on 1st Many 2017. Without this random traffic drops were
    # seen in almost every time we checked traffic.
    rt_data.stats_data = rt_handle.invoke('traffic_stats', *args, **kwargs)

    t.log(level="debug", message="rt_data.stats_data returned by\
        rt_handle.sth.traffic_stats = ["+json.dumps(rt_data.stats_data, sort_keys=True, indent=4)+"]")

    if rt_data.stats_data['status'] == '1':
        t.log(level="debug", message="rt_handle.sth.traffic_stats success. ")
    else:
        raise Exception("""rt_handle.sth.traffic_stats failed.
        kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
        rt_data.stats_data = ["""+json.dumps(rt_data.stats_data, sort_keys=True, indent=4)+"""]
        """)


    t.log(level="debug", message="formatted rt_data.stats_data = ["+json.dumps(rt_data.stats_data, sort_keys=True, indent=4) + "] ")

    t.log(level="debug", message=""" ======== FUNCTION [END] _collect_stats ======== """)

    return rt_data.stats_data
# def _collect_stats     [END].




# def _populate_tolerance    [START].
def _populate_tolerance(rt_handle, rt_data=None, **kwargs):
    """
    Iterate across all ports and stream blocks to specify the value of tolerance
    for each(tx port, stream block) pair.


    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.
        tolerance(dict): dict containing the tolerance values for stream blocks.
        agg_sb_stats(dict): Contains the aggregated traffic stats as returned by
            the "traffic_stats" of Spirent HLT API function.

    Returns:
        Does not return anything as of now.
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] _populate_tolerance ======== """)

    t.log(level="debug", message="_populate_tolerance | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")


    rt_data.tolerance = {}

    if "tolerance" not in kwargs:
        kwargs["tolerance"] = rt_data.tolerance_user


    if "agg_sb_stats" in kwargs:
        # Handle Aggregated Stream block traffic stats.
        for port_item in kwargs["agg_sb_stats"]:

            if port_item not in rt_data.tolerance:
                rt_data.tolerance[port_item] = {}

            for sb_item in kwargs["agg_sb_stats"][port_item]:

                if sb_item not in rt_data.tolerance[port_item]:
                    rt_data.tolerance[port_item][sb_item] = {}

                is_tolerance_present = False
                if "tx_port_sb_name" not in kwargs["tolerance"]:
                    kwargs["tolerance"]["tx_port_sb_name"] = {}
                if port_item in kwargs["tolerance"]["tx_port_sb_name"]:
                    if sb_item in kwargs["tolerance"]["tx_port_sb_name"][port_item]:
                        is_tolerance_present = True

                if "global" in kwargs["tolerance"]:
                    is_tolerance_present = True

                # If specific tolerance value for this(tx port, stream block) pair is  not  provided,
                #     assign the global tolerance to this.
                if is_tolerance_present is False:
                    rt_data.tolerance[port_item][sb_item]["pkt_count"] = 0 # This should be type  int.
                    rt_data.tolerance[port_item][sb_item]["duration"] = 0.0 # This should be type  float.

                else:

                    if "global" in kwargs["tolerance"]:
                        # Store default tolerance value, if present.
                        this_tolerance_value = kwargs["tolerance"]["global"]

                    if "tx_port_sb_name" not in kwargs["tolerance"]:
                        kwargs["tolerance"]["tx_port_sb_name"] = {}
                    if port_item in kwargs["tolerance"]["tx_port_sb_name"]:
                        if sb_item in kwargs["tolerance"]["tx_port_sb_name"][port_item]:
                            # Overwrite the default tolerance value(if any).
                            this_tolerance_value = kwargs["tolerance"]["tx_port_sb_name"][port_item][sb_item]

                    # Assumption :
                    #     tx_rate is always available in fps.
                    tx_rate = 0.0
                    if rt_data.USE_CONFIGURED_SB_TX_RATES is False:
                        try:
                            tx_rate = float(rt_data.stats_tx_rate_data_sb[port_item][sb_item]["total_pkt_rate"])
                        except KeyError:
                            t.log(level="error", message="Could not find one of the path keys\
                                in rt_data.stats_tx_rate_data_sb to access total_pkt_rate. port_item = ["+port_item+"] sb_item = ["+sb_item+"]. ")
                        except ValueError:
                            t.log(level="error", message="tx_rate is zero. Exception would get thrown soon for Divide by Zero. ")
                    else:
                        # get the configured rates. [START]
                        tx_rate = float(
                            _get_configured_tx_rate_data_sb(
                                rt_handle,
                                sb_handle=sb_item,
                            )
                        )
                        # get the configured rates. [END]

                    tx_pkt_count = 0.0
                    try:
                        tx_pkt_count = float(kwargs["agg_sb_stats"][port_item][sb_item]["tx_pkt_count"])
                    except ValueError:
                        t.log(level="error", message="tx_pkt_count is zero. ")


                    m_obj = re.search(r"([0-9\.]+)\s*([%s]?)", this_tolerance_value)
                    if m_obj:
                        if m_obj.group(2):
                            if m_obj.group(2) == "%": # Tolerance is given as a percentage of tx frame count.
                                rt_data.tolerance[port_item][sb_item]["pkt_count"] = 0
                                try:
                                    rt_data.tolerance[port_item][sb_item]["pkt_count"] = int((float(m_obj.group(1)) * 0.01) * tx_pkt_count)
                                except ValueError:
                                    t.log(level="error", message="Exception occurred while calculating tolerance. Value is not a number. ")
                            elif m_obj.group(2) == "s": # Tolerance is given in seconds of absolute traffic drop.
                                rt_data.tolerance[port_item][sb_item]["pkt_count"] = 0
                                try:
                                    rt_data.tolerance[port_item][sb_item]["pkt_count"] = int(float(m_obj.group(1)) * tx_rate)
                                except ValueError:
                                    t.log(level="error", message="Exception occurred while calculating tolerance. Value is not a number. ")
                        else:
                            # Tolerance has been provided as exact packet count.
                            rt_data.tolerance[port_item][sb_item]["pkt_count"] = 0
                            try:
                                rt_data.tolerance[port_item][sb_item]["pkt_count"] = int(m_obj.group(1))
                            except ValueError:
                                t.log(level="error", message="Exception occurred while calculating tolerance. Value is not a number. ")

                        if tx_rate != 0.0:
                            rt_data.tolerance[port_item][sb_item]["duration"] = rt_data.tolerance[port_item][sb_item]["pkt_count"] / tx_rate
                        else:
                            rt_data.tolerance[port_item][sb_item]["duration"] = 0.0

                    else:
                        raise Exception("""Format issue with tolerance value. Examples of correct format : '200', '20s', '30%'
                        m_obj = """+repr(m_obj)+"""]
                        this_tolerance_value = ["""+repr(this_tolerance_value)+"""]
                        """)


    elif "conv_stream_stats" in kwargs:
        ####
        #### Everything in this "else" section needs to be changed for
        #### detailed stream(convergence) verification api.
        ####
        pass

    t.log(level="debug", message="formatted rt_data.tolerance = ["+json.dumps(rt_data.tolerance, sort_keys=True, indent=4) + "] ")
    t.log(level="debug", message=""" ======== FUNCTION [END] _populate_tolerance ======== """)
    return None
# def _populate_tolerance    [END].




# def _check_agg_traffic_stats   [START].
def _check_agg_traffic_stats(rt_handle, rt_data=None, **kwargs):
    """
    Checks traffic based on stream block results.
    Tolerance, Inclusion / Exclusion of Stream blocks, Printing happens here
    in addition to collecting traffic stats from Spirent.


    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.
        tolerance(dict): dict containing the tolerance values for stream blocks.
        collect_fresh_stats(bool): Indicates whether to use the last stored
            traffic results or to fetch a fresh one.

    Returns:
       (bool): If all drops are within tolerance, it returns True; else, False.
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] _check_agg_traffic_stats ======== """)
    t.log(level="debug", message="_check_agg_traffic_stats | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")


    # Collect the Aggregate Stream block stats, if specified / needed.
    collect_fresh_stats = False
    if "collect_fresh_stats" in kwargs:
        collect_fresh_stats = kwargs["collect_fresh_stats"]

    if collect_fresh_stats is True:
        agg_sb_stats = _get_agg_traffic_stats(
            rt_handle,
            rt_data=rt_data,
        )
    else:
        agg_sb_stats = rt_data.agg_traffic_stats

    if not agg_sb_stats:
        raise Exception("""Stored agg_sb_stats is None.
        agg_sb_stats = ["""+json.dumps(agg_sb_stats, sort_keys=True, indent=4)+"""]
        """)

    # Get tolerance dict ready for use.
    if "tolerance" not in kwargs:
        _populate_tolerance(
            rt_handle,
            rt_data=rt_data,
            tolerance=rt_data.tolerance_user,
            agg_sb_stats=agg_sb_stats,
        )
    else:
        _populate_tolerance(
            rt_handle,
            rt_data=rt_data,
            tolerance=kwargs["tolerance"],
            agg_sb_stats=agg_sb_stats,
        )




    # Iterate and store "pass" / "fail" against each(tx port, stream block) pair.

    # Assumption :
    #     Port Names and Stream Block names have been resolved.
    #     Encountering handles for either of them is not expected here and would cause errors.

    #     This assumption could be ensured by calling the respective functions to populate below variables.
    #         rt_data.port_map
    #         rt_data.sb_map
    #         rt_data.sb_group_map
    #     This calling and populating is yet to be done.
    disp_msg = ""
    fail_found = False
    for port_item in agg_sb_stats:

        port_name = _get_real_port_name(
            rt_data=rt_data,
            port_handle=port_item
        )

        for sb_item in agg_sb_stats[port_item]:

            if sb_item in rt_data.stc_sb_handle_to_label_map:
                sb_name = rt_data.stc_sb_handle_to_label_map[sb_item]
            else:
                sb_name = sb_item

            if agg_sb_stats[port_item][sb_item]["pkt_drop_count"] <= rt_data.tolerance[port_item][sb_item]["pkt_count"]:
                if agg_sb_stats[port_item][sb_item]["pkt_drop_count"] >= 0:
                    this__disp_msg = """
    [PASS]    |    {port_item}    |    {sb_item}
    Total Rx Frame Count = {rx_total_pkts}
    Total Tx Frame Count = {tx_total_pkts}
    Duplicate Pkt Count = {rx_duplicate_pkts}
    Dropped Pkt Count = {pkt_drop_count}
    Drop Duration = {pkt_drop_dur_sec}s
    Multiplication Factor = {multiplication_factor}
    Tolerance = {tolerance}s
                    """.format(
                        port_item=port_name,
                        sb_item=sb_name,
                        pkt_drop_count=agg_sb_stats[port_item][sb_item]["pkt_drop_count"],
                        pkt_drop_dur_sec=agg_sb_stats[port_item][sb_item]["pkt_drop_dur_sec"],
                        rx_total_pkts=agg_sb_stats[port_item][sb_item]["rx_total_pkts"],
                        tx_total_pkts=agg_sb_stats[port_item][sb_item]["tx_total_pkts"],
                        rx_duplicate_pkts=agg_sb_stats[port_item][sb_item]["rx_duplicate_pkts"],
                        multiplication_factor=agg_sb_stats[port_item][sb_item]["multiplication_factor"],
                        tolerance=rt_data.tolerance[port_item][sb_item]["duration"],
                    )
                    disp_msg = disp_msg + this__disp_msg
                    t.log(level="debug", message=this__disp_msg)
                else: # pkt_drop_count is less than 0.
                    this__disp_msg = """
    [FAIL]    |    {port_item}    |    {sb_item}
    Total Rx Frame Count = {rx_total_pkts}
    Total Tx Frame Count = {tx_total_pkts}
    Duplicate Pkt Count = {rx_duplicate_pkts}
    Dropped Pkt Count = {pkt_drop_count}
    Drop Duration = {pkt_drop_dur_sec}s
    Multiplication Factor = {multiplication_factor}
    Tolerance = {tolerance}s
                    """.format(
                        port_item=port_name,
                        sb_item=sb_name,
                        pkt_drop_count=agg_sb_stats[port_item][sb_item]["pkt_drop_count"],
                        pkt_drop_dur_sec=agg_sb_stats[port_item][sb_item]["pkt_drop_dur_sec"],
                        rx_total_pkts=agg_sb_stats[port_item][sb_item]["rx_total_pkts"],
                        tx_total_pkts=agg_sb_stats[port_item][sb_item]["tx_total_pkts"],
                        rx_duplicate_pkts=agg_sb_stats[port_item][sb_item]["rx_duplicate_pkts"],
                        multiplication_factor=agg_sb_stats[port_item][sb_item]["multiplication_factor"],
                        tolerance=rt_data.tolerance[port_item][sb_item]["duration"],
                    )
                    disp_msg = disp_msg + this__disp_msg
                    t.log(level="debug", message=this__disp_msg)
                    fail_found = True
            else:
                this__disp_msg = """
    [FAIL]    |    {port_item}    |    {sb_item}
    Total Rx Frame Count = {rx_total_pkts}
    Total Tx Frame Count = {tx_total_pkts}
    Duplicate Pkt Count = {rx_duplicate_pkts}
    Dropped Pkt Count = {pkt_drop_count}
    Drop Duration = {pkt_drop_dur_sec}s
    Multiplication Factor = {multiplication_factor}
    Tolerance = {tolerance}s
                """.format(
                    port_item=port_name,
                    sb_item=sb_name,
                    pkt_drop_count=agg_sb_stats[port_item][sb_item]["pkt_drop_count"],
                    pkt_drop_dur_sec=agg_sb_stats[port_item][sb_item]["pkt_drop_dur_sec"],
                    rx_total_pkts=agg_sb_stats[port_item][sb_item]["rx_total_pkts"],
                    tx_total_pkts=agg_sb_stats[port_item][sb_item]["tx_total_pkts"],
                    rx_duplicate_pkts=agg_sb_stats[port_item][sb_item]["rx_duplicate_pkts"],
                    multiplication_factor=agg_sb_stats[port_item][sb_item]["multiplication_factor"],
                    tolerance=rt_data.tolerance[port_item][sb_item]["duration"],
                )
                disp_msg = disp_msg + this__disp_msg
                t.log(level="debug", message=this__disp_msg)
                fail_found = True

    return_dict = {}
    return_dict["result"] = False if fail_found is True else True
    return_dict["disp_msg"] = disp_msg
    success_or_fail = "FAIL" if fail_found is True else "PASS"
    t.log(level="info", message="""
======================================== ==  ==
        TRAFFIC RESULT\t| """ + success_or_fail + """
======================================== ==  ==
""" + disp_msg)

    t.log(level="debug", message=""" ======== FUNCTION [END] _check_agg_traffic_stats ======== """)
    return return_dict
# def _check_agg_traffic_stats   [END].




# def _get_agg_traffic_stats     [START].
def _get_agg_traffic_stats(rt_handle, rt_data=None, **kwargs):
    """
    Returns traffic stats based on stream block results.


    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

    Returns:
       (dict): Dict containing the aggregate traffic statistics.
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] _get_agg_traffic_stats ======== """)
    t.log(level="debug", message="_get_agg_traffic_stats | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")


    t.log(level="debug", message="_get_agg_traffic_stats | rt_data.stats_data = ["+json.dumps(rt_data.stats_data, sort_keys=True, indent=4)+"] ")

    anomaly_map = {}

    for port_h_item in rt_data.stats_data:

        if isinstance(rt_data.stats_data[port_h_item], dict): # To skip key named "status".
            for sb_h_item in rt_data.stats_data[port_h_item]["stream"]:

                # Stream Block name and Tx Port name are used to populate the 'anomaly_map'.

                # If Stream Block name is not found in 'sb_map',
                #     we use the stream block handle in its place.

                # If Tx Port name is not found in 'port_map',
                #     we use the port handle in its place.
                sb_name = sb_h_item
                port_name = port_h_item

                if port_name not in anomaly_map:
                    anomaly_map[port_name] = {}

                if sb_name not in anomaly_map[port_name]:
                    anomaly_map[port_name][sb_name] = {}


                # If "total_pkts" != 0 for the given(tx port, stream block) pair in "rx" hierarchy,
                #         use it as the dropped packet count.
                # Else,
                #     use "total_pkts" from the "tx" hierarchy for that(tx port, stream block) pair as the dropped packet count.
                #     When no packets were received at all, Spirent might not give the "rx" hierarchy entry for that(tx port, stream block) pair.
                if "rx" in rt_data.stats_data[port_h_item]["stream"][sb_h_item] and \
                    "dropped_pkts" in rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"] and \
                        int(rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["total_pkts"]) != 0:
                    anomaly_map[port_name][sb_name]["rx_total_pkts"] = rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["total_pkts"]
                    anomaly_map[port_name][sb_name]["tx_total_pkts"] = rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]["total_pkts"]
                    # Taking care of duplicate packets.
                    try:
                        # Spirent returns rx.duplicate_pkts as:
                        # "duplicate_pkts": "10 10"
                        # Hence, adding a regex to extract the numeric value from it.
                        anomaly_map[port_name][sb_name]["rx_duplicate_pkts"] = 0
                        if re.search("[0-9]+", rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["duplicate_pkts"]) is not None:
                            rx_duplicate_pkts =\
                                re.search("[0-9]+", rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["duplicate_pkts"]).group()
                        anomaly_map[port_name][sb_name]["rx_duplicate_pkts"] = int(
                            rx_duplicate_pkts
                        )
                    except ValueError:
                        raise Exception("""Exception occurred while converting duplicate_pkts to int. Value is not a number.
                        duplicate_pkts = ["""+repr(rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["duplicate_pkts"])+"""]
                        """)

                    # Taking care of dropped packets.
                    anomaly_map[port_name][sb_name]["pkt_drop_count"] = 0
                    if rt_data._do_not_rely_on_spirent_dropped_pkts is True:
                        multiplication_factor = _get_sb_rx_multiplication_factor(
                            rt_data=rt_data,
                            port_handle=port_name,
                            sb_handle=sb_name,
                        )
                        anomaly_map[port_name][sb_name]["multiplication_factor"] = multiplication_factor
                        # anomaly_map[port_name][sb_name]["pkt_drop_count"] = \
                        #     int(
                        #         int(
                        #             rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]["total_pkts"]
                        #        ) * multiplication_factor
                        #    ) - int(
                        #         rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["total_pkts"]
                        #    ) # - anomaly_map[port_name][sb_name]["rx_duplicate_pkts"]
                        # anomaly_map[port_name][sb_name]["pkt_drop_count"] = \
                        #     int(
                        #         int(
                        #             rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]["total_pkts"]
                        #        ) * multiplication_factor
                        #    ) - int(
                        #         rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["total_pkts"]
                        #    ) - anomaly_map[port_name][sb_name]["rx_duplicate_pkts"]

                        # Rx "total_pkts" includes "rx_duplicate_pkts". Hence, commented
                        # the immediately above calculation and instead added below one.
                        anomaly_map[port_name][sb_name]["pkt_drop_count"] = \
                            int(
                                int(
                                    rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]["total_pkts"]
                                ) * multiplication_factor
                            ) -(int(
                                rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["total_pkts"]
                            ) - anomaly_map[port_name][sb_name]["rx_duplicate_pkts"])
                    else:
                        try:
                            anomaly_map[port_name][sb_name]["pkt_drop_count"] =\
                                int(rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["dropped_pkts"])
                        except ValueError:
                            raise Exception("""Exception occurred while converting dropped_pkts to int. Value is not a number.
                            dropped_pkts = ["""+repr(rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["dropped_pkts"])+"""]
                            """)
                else:
                    # Taking care of duplicate packets.
                    # If rx_total_pkts is 0, there cannot be any duplicate packets.
                    # No need to consider "duplicate_pkts" in this "else" section for computing "pkt_drop_count".
                    if "rx" in rt_data.stats_data[port_h_item]["stream"][sb_h_item] and\
                        "duplicate_pkts" in rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]:
                        try:
                            # Spirent returns rx.duplicate_pkts as:
                            # "duplicate_pkts": "10 10"
                            # Hence, adding a regex to extract the numeric value from it.
                            if re.search("[0-9]+", rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["duplicate_pkts"]) is not None:
                                rx_duplicate_pkts =\
                                    re.search("[0-9]+", rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["duplicate_pkts"]).group()
                            anomaly_map[port_name][sb_name]["rx_duplicate_pkts"] = int(
                                rx_duplicate_pkts
                            )
                        except ValueError:
                            raise Exception("""Exception occurred while converting duplicate_pkts to int. Value is not a number.
                            duplicate_pkts = ["""+repr(rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"]["duplicate_pkts"])+"""]
                            """)

                    # Taking care of dropped packets.
                    anomaly_map[port_name][sb_name]["rx_total_pkts"] = 0
                    anomaly_map[port_name][sb_name]["tx_total_pkts"] = rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]["total_pkts"]
                    anomaly_map[port_name][sb_name]["pkt_drop_count"] = 0
                    multiplication_factor = _get_sb_rx_multiplication_factor(
                        rt_data=rt_data,
                        port_handle=port_name,
                        sb_handle=sb_name,
                    )
                    anomaly_map[port_name][sb_name]["multiplication_factor"] = multiplication_factor
                    try:
                        anomaly_map[port_name][sb_name]["pkt_drop_count"] = \
                            int(
                                int(
                                    rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]["total_pkts"]
                                ) * multiplication_factor
                            )
                    except ValueError:
                        raise Exception("""Exception occurred while converting total_pkts to int. Value is not a number.
                        total_pkts = ["""+repr(rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]["total_pkts"])+"""]
                        """)





                anomaly_map[port_name][sb_name]["tx_rate"] = 0
                if rt_data.USE_CONFIGURED_SB_TX_RATES is False:
                    try:
                        anomaly_map[port_name][sb_name]["tx_rate"] = int(rt_data.stats_tx_rate_data_sb[port_h_item][sb_h_item]["total_pkt_rate"])


                    except KeyError:
                        t.log(level="info", message="Could not find one of the path keys\
                            in rt_data.stats_tx_rate_data_sb to access total_pkt_rate. port_h_item = ["+port_h_item+"] sb_h_item = ["+sb_h_item+"]. ")
                    except ValueError:
                        raise Exception("""Exception occurred while converting total_pkt_rate to int. Value is not a number.
                        total_pkt_rate = ["""+repr(rt_data.stats_tx_rate_data_sb[port_h_item][sb_h_item]["total_pkt_rate"])+"""]
                        """)
                else:
                    # get the configured rates. [START]
                    anomaly_map[port_name][sb_name]["tx_rate"] = _get_configured_tx_rate_data_sb(
                        rt_handle,
                        sb_handle=sb_name,
                    )
                    # get the configured rates. [END]

                anomaly_map[port_name][sb_name]["tx_pkt_count"] = 0
                try:
                    anomaly_map[port_name][sb_name]["tx_pkt_count"] = int(rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]["total_pkts"])
                except ValueError:
                    raise Exception("""Exception occurred while converting total_pkts to int. Value is not a number.
                    total_pkts = ["""+repr(rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]["total_pkts"])+"""]
                    """)



                # Compute the drop duration in seconds.
                # Assumption
                #     Step graph for loss.
                try:
                    anomaly_map[port_name][sb_name]["pkt_drop_dur_sec"] =\
                        (float(anomaly_map[port_name][sb_name]["pkt_drop_count"])) / int(anomaly_map[port_name][sb_name]["tx_rate"])
                except ZeroDivisionError:
                    anomaly_map[port_name][sb_name]["pkt_drop_dur_sec"] = None


    rt_data.agg_traffic_stats = anomaly_map

    t.log(level="debug", message=""" ======== FUNCTION [END] _get_agg_traffic_stats ======== """)
    return anomaly_map
# def _get_agg_traffic_stats     [END].




# pdt_rt_set_traffic_multiplication_factor [START].
def pdt_rt_set_traffic_multiplication_factor(rt_data=None, **kwargs):
    """
    Sets the multiplication factor for a given streamblock.
    If no multiplication factor is set in the YAML file, then it
    sets it to 1(default) for that streamblock.

    Multiplication factor is used to get what Rx is expected for the given Tx.

    Expected Rx = int(MF * Tx)

    where, MF = Multiplication Factor.

    Args:
        rt_data(mandatory): PDT RT Data Object.
        port_handle(str): Port Handle where stream block originates.
        sb_handle(str): Streamblock handle.
        sb_name(str): Streamblock for which to return the traffic statistics.
        port_name(str): Port name of the streamblock, for which to return the traffic statistics.
        multiplication_factor(float): Multiplication factor value for this streamblock.

    Returns:
       (dict): rt_data._sb_multiplication_factor_map
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] pdt_rt_set_traffic_multiplication_factor ======== """)

    t.log(level="debug", message="pdt_rt_set_traffic_multiplication_factor | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"]")


    if "port_name" in kwargs:
        if kwargs["port_name"] in rt_data.stc_port_handle_map:
            kwargs["port_handle"] = rt_data.stc_port_handle_map[kwargs["port_name"]]
        else:
            raise Exception("""Port Name = ["""+kwargs["port_name"]+"""] does not have a mapped port handle.
            rt_data.stc_port_handle_map = ["""+json.dumps(rt_data.stc_port_handle_map, sort_keys=True, indent=4)+"""]
            """)
    if "sb_name" in kwargs:
        if kwargs["sb_name"] in rt_data.stc_handle_map:
            kwargs["sb_handle"] = rt_data.stc_handle_map[kwargs["sb_name"]]["handle"]
        else:
            raise Exception("""Stream Block Name = ["""+kwargs["sb_name"]+"""] does not have a mapped stream block handle.
            rt_data.stc_handle_map = ["""+json.dumps(rt_data.stc_handle_map, sort_keys=True, indent=4)+"""]
            """)

    _set_sb_rx_multiplication_factor(
        rt_data=rt_data,
        port_handle=kwargs["port_handle"],
        sb_handle=kwargs["sb_handle"],
        multiplication_factor=float(kwargs["multiplication_factor"]),
    )


    t.log(level="debug", message=""" ======== FUNCTION [END] pdt_rt_set_traffic_multiplication_factor ======== """)

    return rt_data._sb_multiplication_factor_map
# pdt_rt_set_traffic_multiplication_factor [END].




def _set_sb_rx_multiplication_factor(rt_data=None, **kwargs):
    """
    Sets the multiplication factor for a given streamblock.
    If no multiplication factor is set in the YAML file, then it
    sets it to 1(default) for that streamblock.

    Multiplication factor is used to get what Rx is expected for the given Tx.

    Expected Rx = int(MF * Tx)

    where, MF = Multiplication Factor.

    Args:
        port_handle(str): Port Handle where stream block originates.
        rt_data(mandatory): PDT RT Data Object.
        sb_handle(str): Streamblock handle.
        multiplication_factor(float): Multiplication factor value for this streamblock.

    Returns:
       (none)
    """

    if "port_handle" not in kwargs:
        raise Exception("""Exception occurred in _set_sb_rx_multiplication_factor.
        Key 'port_handle' not found in call to _set_sb_rx_multiplication_factor().
        kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
        """)

    if "sb_handle" not in kwargs:
        raise Exception("""Exception occurred in _set_sb_rx_multiplication_factor.
        Key 'sb_handle' not found in call to _set_sb_rx_multiplication_factor().
        kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
        """)

    if "multiplication_factor" not in kwargs:
        raise Exception("""Exception occurred in _set_sb_rx_multiplication_factor.
        Key 'multiplication_factor' not found in call to _set_sb_rx_multiplication_factor().
        kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
        """)


    if kwargs["port_handle"] not in rt_data._sb_multiplication_factor_map:
        rt_data._sb_multiplication_factor_map[kwargs["port_handle"]] = {}

    rt_data._sb_multiplication_factor_map[kwargs["port_handle"]][kwargs["sb_handle"]] =\
        kwargs["multiplication_factor"]

    t.log(level="debug", message="rt_data._sb_multiplication_factor_map = ["\
        +json.dumps(rt_data._sb_multiplication_factor_map, sort_keys=True, indent=4)+"] ")

    return None
# def _set_sb_rx_multiplication_factor [END].




# def _get_sb_rx_multiplication_factor [START].
def _get_sb_rx_multiplication_factor(rt_data=None, **kwargs):
    """
    Returns the multiplication factor for a given streamblock.
    If no multiplication factor is set in the YAML file, then it returns 1(default).
    Multiplication factor is used to get what Rx is expected for the given Tx.

    Expected Rx = int(MF * Tx)

    where, MF = Multiplication Factor.

    Args:
        rt_data(mandatory): PDT RT Data Object.
        port_handle(str): Port handle to identify the streamblock.
        sb_handle(str): Streamblock handle.

    Returns:
       (str): Multiplication Factor for this streamblock.
    """

    if "port_handle" not in kwargs:
        raise Exception("""Exception occurred in _get_sb_rx_multiplication_factor.
        Key 'port_handle' not found in call to _get_sb_rx_multiplication_factor().
        kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
        """)
    if "sb_handle" not in kwargs:
        raise Exception("""Exception occurred in _get_sb_rx_multiplication_factor.
        Key 'sb_handle' not found in call to _get_sb_rx_multiplication_factor().
        kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
        """)

    if kwargs["port_handle"] not in rt_data._sb_multiplication_factor_map:
        raise Exception("""Exception occurred in _get_sb_rx_multiplication_factor.
        Key 'port_handle' not found in rt_data._sb_multiplication_factor_map.
        kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
        """)

    if kwargs["sb_handle"] not in rt_data._sb_multiplication_factor_map[kwargs["port_handle"]]:
        raise Exception("""Exception occurred in _get_sb_rx_multiplication_factor.
        Key 'sb_handle' not found in rt_data._sb_multiplication_factor_map.
        kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
        """)


    return rt_data._sb_multiplication_factor_map[kwargs["port_handle"]][kwargs["sb_handle"]]
# def _get_sb_rx_multiplication_factor [END].




# def _get_configured_tx_rate_data_sb   [START].
def _get_configured_tx_rate_data_sb(rt_handle, **kwargs):

    """
    Fetches(from Spirent) and Returns the given streamblock's
    configured tx fps rate.


    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        sb_handle(str): Handle of the streamblock whose tx rate
        has to be fetched and stored.

    Returns:
       (int) Streamblock configured tx fps rate.
    """

    t.log(level="debug", message="_get_configured_tx_rate_data_sb | START ")

    t.log(level="debug", message="_get_configured_tx_rate_data_sb | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")

    if "sb_handle" not in kwargs:
        raise Exception("""Mandatory argument  sb_handle  missing.
        kwargs = ["""+json.dumps(kwargs, sort_keys=True, indent=4)+"""]
        """)

    # old Way to get Load and LoadUnit.
    # configured_load = rt_handle.sth.invoke("stc::get "+kwargs["sb_handle"]+" -load")
    # configured_loadunit = rt_handle.sth.invoke("stc::get "+kwargs["sb_handle"]+" -loadunit")

    # New Way to get Load and LoadUnit.
    sb_load_profile = rt_handle.sth.invoke("stc::get "+kwargs["sb_handle"]+" -AffiliationStreamBlockLoadProfile-targets ")
    configured_load = rt_handle.sth.invoke("stc::get "+sb_load_profile+" -load")
    configured_loadunit = rt_handle.sth.invoke("stc::get "+sb_load_profile+" -loadunit")
    # sb_load_profile = rt_handle.invoke('invoke', "stc::get "+kwargs["sb_handle"]+" -AffiliationStreamBlockLoadProfile-targets ")
    # configured_load = rt_handle.invoke('invoke', "stc::get "+sb_load_profile+" -load")
    # configured_loadunit = rt_handle.invoke('invoke', "stc::get "+sb_load_profile+" -loadunit")
    # [READ IT : START]
    # Could not convert above calls from 'rt_handle.sth.invoke' to 'rt_handle.invoke'
    # as requested by jhayes. The below function needs to have '*args' in addtion to '**args'(actually, this one should be '**kwargs' by convention).
    # def invoke(self, function, from_spirent_robot=False, **args):
    # File : /usr/local/lib/python3.5/dist-packages/jnpr/toby/hldcl/trafficgen/spirent/spirent.py
    # [READ IT : END]
    #
    t.log(level="debug", message="configured_load = ["+configured_load+"] configured_loadunit = ["+configured_loadunit+"] ")

    configured_loadunit__strip = configured_loadunit.strip()

    if configured_loadunit__strip != "FRAMES_PER_SECOND":
        raise Exception("""Please configure load in your streamblock in fps.
        configured_loadunit = ["""+configured_loadunit+"""]
        """)
        # Later, add a function to convert the rate in other units like bandwidth to fps.

    configured_load__int = int(float(configured_load))
    # self.configured_tx_rate_data_sb[kwargs["sb_handle"]] = configured_load__int

    t.log(level="debug", message="_get_configured_tx_rate_data_sb | END ")
    return configured_load__int
# def _get_configured_tx_rate_data_sb   [END].




# def _get_sb_tx_rates   [START].
def _get_sb_tx_rates(rt_handle, rt_data=None, **kwargs):
    """
    Returns each streamblock's tx fps rate.


    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

    Returns:
       (dict):
            port_handle:
                sb_handle:
                    total_pkt_rate :(str)
    """

    t.log(level="debug", message="_get_sb_tx_rates | START ")

    t.log(level="info", message="_get_sb_tx_rates | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")


    # Collect live results for capturing the tx packet rates which
    # would be unavailable when we stop traffic.
    _collect_stats(
        rt_handle,
        rt_data=rt_data,
        port_handle=list(rt_data.stc_port_handle_map.values()),
        mode="streams",
    )


    for port_h_item in rt_data.stats_data:

        if isinstance(rt_data.stats_data[port_h_item], dict): # To skip key named "status".

            if port_h_item not in rt_data.stats_tx_rate_data_sb:
                rt_data.stats_tx_rate_data_sb[port_h_item] = {}

            for sb_h_item in rt_data.stats_data[port_h_item]["stream"]:

                if sb_h_item not in rt_data.stats_tx_rate_data_sb[port_h_item]:
                    rt_data.stats_tx_rate_data_sb[port_h_item][sb_h_item] = {}

                    rt_data.stats_tx_rate_data_sb[port_h_item][sb_h_item]["total_pkt_rate"] =\
                        rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]["total_pkt_rate"]

    t.log(level="debug", message="_get_sb_tx_rates | END ")
    return rt_data.stats_tx_rate_data_sb
# def _get_sb_tx_rates   [END].




# def _get_stream_tx_rates   [START].
def _get_stream_tx_rates(rt_handle, rt_data=None, **kwargs):
    """
    Returns each stream's tx fps rate.


    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

    Returns:
       (dict):
            port_handle:
                sb_handle:
                    stream_id:
                        total_pkt_rate :(str)
    """

    t.log(level="debug", message="_get_stream_tx_rates | START ")

    t.log(level="info", message="_get_stream_tx_rates | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")


    # Collect live results for capturing the tx packet rates which
    # would be unavailable when we stop traffic.
    _collect_stats(
        rt_handle,
        rt_data=rt_data,
        port_handle=list(rt_data.stc_port_handle_map.values()),
        mode="detailed_streams",
    )


    for port_h_item in rt_data.stats_data:
        t.log(level="info", message="port_h_item = ["+port_h_item+"] ")

        if isinstance(rt_data.stats_data[port_h_item], dict): # To skip key named "status".

            if port_h_item not in rt_data.stats_tx_rate_data:
                rt_data.stats_tx_rate_data[port_h_item] = {}

            for sb_h_item in rt_data.stats_data[port_h_item]["stream"]:
                t.log(level="info", message="port_h_item = ["+port_h_item+"] sb_h_item = ["+sb_h_item+"] ")

                if sb_h_item not in rt_data.stats_tx_rate_data[port_h_item]:
                    rt_data.stats_tx_rate_data[port_h_item][sb_h_item] = {}

                for stream_id in rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]:
                    t.log(level="info", message="port_h_item = ["+port_h_item+"] sb_h_item = ["+sb_h_item+"] stream_id = ["+stream_id+"] ")

                    if stream_id not in rt_data.stats_tx_rate_data[port_h_item][sb_h_item]:
                        rt_data.stats_tx_rate_data[port_h_item][sb_h_item][stream_id] = {}

                    rt_data.stats_tx_rate_data[port_h_item][sb_h_item][stream_id]["total_pkt_rate"] =\
                        rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"][stream_id]["total_pkt_rate"]

    t.log(level="debug", message="_get_stream_tx_rates | END ")
    return rt_data.stats_tx_rate_data
# def _get_stream_tx_rates   [END].




# def _check_conv_result     [START].
def _check_conv_result(rt_handle, rt_data=None, **kwargs):
    """
    [Incomplete. Would be done as an enhancement.]

    Checks traffic based on detailed stream level results.
    Tolerance, Inclusion / Exclusion of Stream blocks, Printing happens
    here in addition to collecting traffic stats from Spirent.


    Args:
        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.
        tolerance(dict): dict containing the tolerance values for stream blocks.
        collect_fresh_stats(bool): Indicates whether to use the last stored
            traffic results or to fetch a fresh one.

    Returns:
        Does not return anything as of now.
    """


    t.log(level="info", message="_check_conv_result | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")


    # Collect the Detailed Stream level stats, if specified / needed.
    collect_fresh_stats = False
    if "collect_fresh_stats" in kwargs:
        collect_fresh_stats = kwargs["collect_fresh_stats"]

    if collect_fresh_stats:
        conv_stream_stats = _get_conv_result(
            rt_data=rt_data,
        )
    else:
        conv_stream_stats = rt_data.agg_traffic_stats

    if not conv_stream_stats:
        raise Exception("""Stored conv_stream_stats is None.
        conv_stream_stats = ["""+json.dumps(conv_stream_stats, sort_keys=True, indent=4) + """]
        """)


    # Get tolerance dict ready for use.
    if "tolerance" not in kwargs:
        _populate_tolerance(
            rt_handle,
            rt_data=rt_data,
            tolerance=rt_data.tolerance_user,
            conv_stream_stats=conv_stream_stats,
        )
    else:
        _populate_tolerance(
            rt_handle,
            rt_data=rt_data,
            tolerance=kwargs["tolerance"],
            conv_stream_stats=conv_stream_stats,
        )




    # Iterate and store "pass" / "fail" against each(tx port, stream block) pair.

    # Assumption :
    #     Port Names and Stream Block names have been resolved.
    #     Encountering handles for either of them is not expected here and would cause errors.

    #     This assumption could be ensured by calling the respective functions to populate below variables.
    #         rt_data.port_map
    #         rt_data.sb_map
    #         rt_data.sb_group_map
    #     This calling and populating is yet to be done.
    disp_msg = ""
    fail_found = False
    for port_item in conv_stream_stats:

        port_name = _get_real_port_name(
            rt_data=rt_data,
            port_handle=port_item
        )

        for sb_item in conv_stream_stats[port_item]:
            if sb_item in rt_data.stc_sb_handle_to_label_map:
                sb_name = rt_data.stc_sb_handle_to_label_map[sb_item]
            else:
                sb_name = sb_item

            if conv_stream_stats[port_item][sb_item]["pkt_drop_count"] <= rt_data.tolerance[port_item][sb_item]["pkt_count"]:
                this__disp_msg = """
                [PASS]    |    {port_item}    |    {sb_item}
                """.format(
                    port_item=port_name, # port_item,
                    sb_item=sb_name, # sb_item,
                    # pkt_drop_count=conv_stream_stats[port_item][sb_item]["pkt_drop_count"],
                )
                disp_msg = disp_msg + this__disp_msg
                t.log(level="debug", message=this__disp_msg)
            else:
                this__disp_msg = """
                [FAIL]    |    {port_item}    |    {sb_item}
                Dropped Pkt Count = {pkt_drop_count}
                """.format(
                    port_item=port_name,# port_item,
                    sb_item=sb_name, # sb_item,
                    pkt_drop_count=conv_stream_stats[port_item][sb_item]["pkt_drop_count"],
                )
                disp_msg = disp_msg + this__disp_msg
                t.log(level="debug", message=this__disp_msg)
                fail_found = True

    return_dict = {}
    return_dict["result"] = False if fail_found is True else True
    return_dict["disp_msg"] = disp_msg
    success_or_fail = "FAIL" if fail_found is True else "PASS"
    t.log(level="info", message="""
============================================
        TRAFFIC RESULT\t| """ + success_or_fail + """
============================================
""" + disp_msg)

    return return_dict
# def _check_conv_result     [END].




# def _get_conv_result   [START].
def _get_conv_result(rt_data=None, **kwargs):
    """
    [Incomplete. Would be done as an enhancement.]

    Returns each streamblock's max drop stream's drop duration in seconds.


    Args:
        rt_data(mandatory): PDT RT Data Object.

    Returns:
       (dict): Dict containing the convergence results. It has details
            about the worst performing stream across all stream blocks
            which converged last.
    """


    t.log(level="info", message="_get_conv_result | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")

    return_data = {}

    for port_h_item in rt_data.stats_data:

        return_data["sb"] = {}
        return_data["sbg"] = {}

        if isinstance(rt_data.stats_data[port_h_item], dict): # To skip key named "status".
            for sb_h_item in rt_data.stats_data[port_h_item]["stream"]:

                anomaly_map = {}
                max_drop_dur_stream_id = None
                max_drop_dur_sec = None

                for stream_id in rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"]:

                    anomaly_map[stream_id] = {}

                    # If "dropped_pkts" is found in "rx" hierarchy for the given stream id,
                    #     and
                    #     "total_pkts" != 0 for the given stream id in "rx" hierarchy,
                    #         use it as the dropped packet count.
                    # Else,
                    #     use "total_pkts" from the "tx" hierarchy for that stream id as the dropped packet count.
                    #     When no packets were received at all, Spirent might not give the "rx" hierarchy entry for that stream id.
                    if "rx" in rt_data.stats_data[port_h_item]["stream"][sb_h_item] and \
                        stream_id in rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"] and \
                        "dropped_pkts" in rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"][stream_id] and \
                        int(rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"][stream_id]["total_pkts"]) != 0:
                        anomaly_map[stream_id]["pkt_drop_count"] = 0
                        multiplication_factor = _get_sb_rx_multiplication_factor(
                            rt_data=rt_data,
                            port_handle=port_h_item, # port_name,
                            sb_handle=sb_h_item, # sb_name,
                        )
                        anomaly_map[stream_id]["multiplication_factor"] = multiplication_factor
                        if rt_data._do_not_rely_on_spirent_dropped_pkts is True:
                            anomaly_map[stream_id]["pkt_drop_count"] = \
                                int(
                                    int(
                                        rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"][stream_id]["total_pkts"]
                                    ) * multiplication_factor
                                ) - int(
                                    rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"][stream_id]["total_pkts"]
                                )
                        else:
                            anomaly_map[stream_id]["pkt_drop_count"] = \
                                int(
                                    rt_data.stats_data[port_h_item]["stream"][sb_h_item]["rx"][stream_id]["dropped_pkts"]
                                )

                    else:
                        multiplication_factor = _get_sb_rx_multiplication_factor(
                            rt_data=rt_data,
                            port_handle=port_h_item, # port_name,
                            sb_handle=sb_h_item, # sb_name,
                        )
                        anomaly_map[stream_id]["multiplication_factor"] = multiplication_factor
                        anomaly_map[stream_id]["pkt_drop_count"] = \
                            int(
                                int(
                                    rt_data.stats_data[port_h_item]["stream"][sb_h_item]["tx"][stream_id]["total_pkts"]
                                ) * multiplication_factor
                            )


                    anomaly_map[stream_id]["tx_rate_pps"] = rt_data.stats_tx_rate_data[port_h_item][sb_h_item][stream_id]["total_pkt_rate"]

                    # Compute the max drop duration in seconds.
                    # Assumption
                    #     Step graph for loss.
                    try:
                        anomaly_map[stream_id]["pkt_drop_dur_sec"] =\
                            (float(anomaly_map[stream_id]["pkt_drop_count"])) / int(anomaly_map[stream_id]["tx_rate_pps"])
                    except ZeroDivisionError:
                        anomaly_map[stream_id]["pkt_drop_dur_sec"] = None


                    # Compare and store the max drop duration for the entire Stream Block.
                    if max_drop_dur_stream_id is None:
                        if anomaly_map[stream_id]["pkt_drop_dur_sec"] > 0:
                            max_drop_dur_stream_id = stream_id
                            try:
                                max_drop_dur_sec = float(anomaly_map[stream_id]["pkt_drop_dur_sec"])
                            except ValueError:
                                max_drop_dur_sec = 0.0
                    else:
                        try:
                            this_max_drop_dur_sec = float(anomaly_map[stream_id]["pkt_drop_dur_sec"])
                        except ValueError:
                            this_max_drop_dur_sec = 0.0
                        if this_max_drop_dur_sec > max_drop_dur_sec:
                            max_drop_dur_stream_id = stream_id
                            max_drop_dur_sec = this_max_drop_dur_sec

                # Stream Block name and Tx Port name are used to populate the 'return_data'.

                # If Stream Block name is not found in 'sb_map',
                #     we use the stream block handle in its place.

                # If Tx Port name is not found in 'port_map',
                #     we use the port handle in its place.
                sb_name = rt_data.sb_map[sb_h_item]     if sb_h_item in rt_data.sb_map      else sb_h_item
                port_name = rt_data.port_map[port_h_item] if port_h_item in rt_data.port_map  else port_h_item


                # SB(Stream Block) as ToT(top of tree).

                # Store the max drop stream id and drop duration per Stream Block.
                if sb_name not in return_data["sb"]:
                    return_data["sb"][sb_name] = {}

                return_data["sb"][sb_name][port_name] = {}
                return_data["sb"][sb_name][port_name]["max_drop_dur_stream_id"] = max_drop_dur_stream_id
                return_data["sb"][sb_name][port_name]["max_drop_dur_sec"] = max_drop_dur_sec
                return_data["sb"][sb_name][port_name]["multiplication_factor"] = multiplication_factor


                # SBG(SB Group) as ToT(top of tree).
                if (sb_name in rt_data.sb_group_map) and (port_name in rt_data.sb_group_map[sb_name]):
                    # This stream block is part of a Stream Block Group.

                    sb_group = rt_data.sb_group_map[sb_name][port_name]


                    if sb_group in return_data["sbg"]:
                        # This is the first time we encountered a stream block belonging to this Stream Block Group.

                        return_data["sbg"][sb_group] = {}
                        return_data["sbg"][sb_group]["sb"] = sb_name
                        return_data["sbg"][sb_group]["tx_port"] = port_name
                        return_data["sbg"][sb_group]["max_drop_dur_stream_id"] = max_drop_dur_stream_id
                        return_data["sbg"][sb_group]["max_drop_dur_sec"] = max_drop_dur_sec

                    else:
                        if return_data["sbg"][sb_group]["max_drop_dur_sec"] < max_drop_dur_sec:
                            return_data["sbg"][sb_group]["sb"] = sb_name
                            return_data["sbg"][sb_group]["tx_port"] = port_name
                            return_data["sbg"][sb_group]["max_drop_dur_stream_id"] = max_drop_dur_stream_id
                            return_data["sbg"][sb_group]["max_drop_dur_sec"] = max_drop_dur_sec



    rt_data.conv_result = return_data
    return return_data
# def _get_conv_result   [END].




# def _start_traffic     [START].
def _start_traffic(rt_handle, rt_data=None, **kwargs):
    """
    Starts Traffic.

    Args:
        Accepts all arguments which Spirent HLT API function
          rt_handle.sth.traffic_control accepts except "action".

        Even if you specify "action", it would be overwritten with
          "action" value of "run".

        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

        port_name_list(list): List of port names where to start traffic.
            List of port names like: ["R0RT0_1_IF", "R0RT0_4_IF"]

        tag_list(list): List of streamblock tags where to start traffic.
            List of port names like: ["multicast_sb", "ospf_traffic"]

        sb_name_list(list): List of streamblock label names where to start traffic.
            List of port names like: ["BS__OSPF_Traffic", "Raw__Src_to_BGP_routes"]

    Returns:
        dict:
            Returns all arguments which Spirent HLT API function
            rt_handle.sth.traffic_control does.
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] _start_traffic ======== """)

    t.log(level="debug", message="_start_traffic | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"]")

    if "port_name_list" in kwargs:
        # Sometimes, in a corner case, the user might provide few port handles
        # and few port names(obviously with separate keys "port_name_list" and "port_handle").
        # Handle that scenario too.
        if "port_handle" not in kwargs:
            kwargs["port_handle"] = []
        for i in range(len(kwargs["port_name_list"])):
            if kwargs["port_name_list"][i] in rt_data.stc_port_handle_map:
                kwargs["port_handle"].append(rt_data.stc_port_handle_map[kwargs["port_name_list"][i]])
            else:
                raise Exception("""Port Name = ["""+kwargs["port_name_list"][i]+"""] does not have a mapped port handle.
                rt_data.stc_port_handle_map = ["""+json.dumps(rt_data.stc_port_handle_map, sort_keys=True, indent=4) + """]
                """)
        kwargs.pop("port_name_list", None)


    if "tag_list" in kwargs:
        # tags of streamblocks could be passed. These tags are defined in YAML file under streamblocks.
        sb_list = []
        for tag_item in kwargs["tag_list"]:
            sb_list.extend(
                _get_sb_list_for_tag(
                    rt_data=rt_data,
                    tag=tag_item
                )
            )
        if "sb_name_list" in kwargs:
            kwargs["sb_name_list"].extend(sb_list)
            kwargs["sb_name_list"] = list(set(kwargs["sb_name_list"]))
        else:
            kwargs["sb_name_list"] = sb_list

        kwargs.pop("tag_list", None)


    if "sb_name_list" in kwargs:
        # Sometimes, in a corner case, the user might provide few streamblock
        # handles and few stream block names(obviously with separate keys "sb_name_list" and "stream_handle").
        # Handle that scenario too.
        if "stream_handle" not in kwargs:
            kwargs["stream_handle"] = []
        for i in range(len(kwargs["sb_name_list"])):
            if kwargs["sb_name_list"][i] in rt_data.stc_handle_map:
                kwargs["stream_handle"].append(rt_data.stc_handle_map[kwargs["sb_name_list"][i]]["handle"])
            else:
                raise Exception("""Stream Block Name = ["""+kwargs["sb_name_list"][i]+"""] does not have a mapped stream block handle.
                rt_data.stc_handle_map = ["""+json.dumps(rt_data.stc_handle_map, sort_keys=True, indent=4) + """]
                """)
        kwargs.pop("sb_name_list", None)


    # Remove empty arguments passed to HLTAPI function sth.traffic_control.
    if "stream_handle" in kwargs and len(kwargs["stream_handle"]) == 0:
        kwargs.pop("stream_handle", None)
    if "port_handle" in kwargs and len(kwargs["port_handle"]) == 0:
        kwargs.pop("port_handle", None)


    kwargs["action"] = "run" # Default "action" for this function.

    t.log(level="debug", message="_start_traffic | kwargs sent to traffic_control = ["\
        +json.dumps(kwargs, sort_keys=True, indent=4)+"]")

    received_data = rt_handle.invoke("traffic_control", **kwargs)

    t.log(level="debug", message="_start_traffic | received_data returned by traffic_control = ["\
        +json.dumps(received_data, sort_keys=True, indent=4)+"]")

    if "status" not in received_data:
        raise Exception("""Key 'status' not found in the dict returned after Spirent HLT API function call.
        received_data = ["""+json.dumps(received_data, sort_keys=True, indent=4)+"""]
        """)

    if received_data["status"] == "0": # Do not replace with "if(not received_data["status"]): ".
        #   That expression does not evaluate to False since "0" is a string.
        raise Exception("""Key 'status' has value '0' in the dict returned after Spirent HLT API function call.
        received_data = ["""+json.dumps(received_data, sort_keys=True, indent=4)+"""]
        """)

    t.log(level="info", message="""
============================================
        START TRAFFIC \t| SUCCESS
============================================""")

    t.log(level="debug", message=""" ======== FUNCTION [END] _start_traffic ======== """)
    return received_data
# def _start_traffic     [END].




# def _stop_traffic  [START].
def _stop_traffic(rt_handle, rt_data=None, **kwargs):
    """
    Stops Traffic.

    Args:
        Accepts all arguments which Spirent HLT API function
          rt_handle.sth.traffic_control accepts except "action".
        Even if you specify "action", it would be overwritten with
          "action" value of "stop".

        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

        port_name_list(list): List of port names where to stop traffic.
            List of port names like: ["R0RT0_1_IF", "R0RT0_4_IF"]

        sb_name_list(list): List of streamblock label names where to stop traffic.
            List of port names like: ["BS__OSPF_Traffic", "Raw__Src_to_BGP_routes"]

    Returns:
        dict:
            Returns all arguments which Spirent HLT API function
            rt_handle.sth.traffic_control does.
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] _stop_traffic ======== """)

    t.log(level="debug", message="_stop_traffic | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")


    if "port_name_list" in kwargs:
        # Sometimes, in a corner case, the user might provide few port handles and
        # few port names(obviously with separate keys "port_name_list" and "port_handle").
        # Handle that scenario too.
        if "port_handle" not in kwargs:
            kwargs["port_handle"] = []
        for i in range(len(kwargs["port_name_list"])):
            if kwargs["port_name_list"][i] in rt_data.stc_port_handle_map:
                kwargs["port_handle"].append(rt_data.stc_port_handle_map[kwargs["port_name_list"][i]])
            else:
                raise Exception("""Port Name = ["""+kwargs["port_name_list"][i]+"""] does not have a mapped port handle.
                rt_data.stc_port_handle_map = ["""+json.dumps(rt_data.stc_port_handle_map, sort_keys=True, indent=4)+"""]
                """)


    if "sb_name_list" in kwargs:
        # Sometimes, in a corner case, the user might provide few streamblock
        # handles and few stream block names(obviously with separate keys "sb_name_list" and "stream_handle").
        # Handle that scenario too.
        if "stream_handle" not in kwargs:
            kwargs["stream_handle"] = []
        for i in range(len(kwargs["sb_name_list"])):
            if kwargs["sb_name_list"][i] in rt_data.stc_handle_map:
                kwargs["stream_handle"].append(rt_data.stc_handle_map[kwargs["sb_name_list"][i]]["handle"])
            else:
                raise Exception("""Stream Block Name = ["""+kwargs["sb_name_list"][i]+"""] does not have a mapped stream block handle.
                rt_data.stc_handle_map = ["""+json.dumps(rt_data.stc_handle_map, sort_keys=True, indent=4)+"""]
                """)

    # Remove empty arguments passed to HLTAPI function sth.traffic_control.
    if "stream_handle" in kwargs and len(kwargs["stream_handle"]) == 0:
        kwargs.pop("stream_handle", None)
    if "port_handle" in kwargs and len(kwargs["port_handle"]) == 0:
        kwargs.pop("port_handle", None)


    kwargs["action"] = "stop" # Default "action" for this function.

    received_data = rt_handle.invoke("traffic_control", **kwargs)

    t.log(level="debug", message="_stop_traffic | received_data = ["+json.dumps(received_data, sort_keys=True, indent=4)+"] ")

    if "status" not in received_data:
        raise Exception("""Key 'status' not found in the dict returned by Spirent HLTAPI function call.
        received_data = ["""+json.dumps(received_data, sort_keys=True, indent=4)+"""]
        """)

    if received_data["status"] == "0": # Do not replace with "if(not received_data["status"]): ".
        #   That expression does not evaluate to False since "0" is a string.
        raise Exception("""Key 'status' has value '0' in the dict returned after Spirent HLT API function call.
        received_data = ["""+json.dumps(received_data, sort_keys=True, indent=4)+"""]
        """)

    t.log(level="info", message="""
============================================
        STOP TRAFFIC \t| SUCCESS
============================================""")

    t.log(level="debug", message=""" ======== FUNCTION [END] _stop_traffic ======== """)
    return received_data
# def _stop_traffic  [END].




# def _send_arp  [START].
def _send_arp(rt_handle, rt_data=None, **kwargs):
    """
    Sends ARP Requests.

    Args:
        Accepts all arguments which Spirent HLT API function
          rt_handle.sth.arp_control.
        By default, "target" is "all".

        rt_handle(mandatory): Toby Router Tester Handle.
        rt_data(mandatory): PDT RT Data Object.

        port_name_list(list): List of port names where to initiate ARP.
            List of port names like: ["R0RT0_1_IF", "R0RT0_4_IF"]

        dev_sb_name_list(list): List of handles returned by Spirent on
            device/streamblock creation.

    Returns:
        dict:
            Returns all arguments which Spirent HLT API function
            rt_handle.sth.arp_control does.
    """

    t.log(level="debug", message=""" ======== FUNCTION [START] _send_arp ======== """)

    t.log(level="debug", message="_send_arp | kwargs = ["+json.dumps(kwargs, sort_keys=True, indent=4)+"] ")


    if "port_name_list" in kwargs:
        # Sometimes, in a corner case, the user might provide few port handles
        # and few port names(obviously with separate keys "port_name_list" and "port_handle").
        # Handle that scenario too.
        if "port_handle" not in kwargs:
            kwargs["port_handle"] = []
        for i in range(len(kwargs["port_name_list"])):
            if kwargs["port_name_list"][i] in rt_data.stc_port_handle_map:
                kwargs["port_handle"].append(rt_data.stc_port_handle_map[kwargs["port_name_list"][i]])
            else:
                raise Exception("""Port Name = ["""+kwargs["port_name_list"][i]+"""] does not have a mapped port handle.
                rt_data.stc_port_handle_map = ["""+json.dumps(rt_data.stc_port_handle_map, sort_keys=True, indent=4)+"""]
                """)
        kwargs.pop("port_name_list")


    if "dev_sb_name_list" in kwargs:
        # Sometimes, in a corner case, the user might provide few device / streamblock
        # handles and few device / stream block names(obviously with separate keys "dev_sb_name_list" and "handle").
        # Handle that scenario too.
        if "handle" not in kwargs:
            kwargs["handle"] = []
        for i in range(len(kwargs["dev_sb_name_list"])):
            if kwargs["dev_sb_name_list"][i] in rt_data.stc_handle_map:
                kwargs["handle"].append(rt_data.stc_handle_map[kwargs["dev_sb_name_list"][i]]["handle"])
            else:
                raise Exception("""Device / Stream Block Name = ["""+kwargs["dev_sb_name_list"][i]+"""] does not have a mapped handle.
                rt_data.stc_handle_map = ["""+json.dumps(rt_data.stc_handle_map, sort_keys=True, indent=4)+"""]
                """)
        kwargs.pop("dev_sb_name_list")


    if "arp_target" not in kwargs:
        kwargs["arp_target"] = "all" # Default "target" for this function.

    received_data = rt_handle.invoke("arp_control", **kwargs)
    t.log(level="debug", message="_send_arp | received_data = ["+json.dumps(received_data, sort_keys=True, indent=4)+"] ")

    if "status" not in received_data:
        raise Exception("""Key 'status' not found in the dict returned after Spirent HLT API function call.
        received_data = ["""+json.dumps(received_data, sort_keys=True, indent=4)+"""]
        """)

    if received_data["status"] == "0": # Do not replace with
        # "if(not received_data["status"]): ". That expression does not evaluate
        # to False since "0" is a string.
        raise Exception("""Key 'status' has value '0' in the dict returned after Spirent HLT API function call.
        received_data = ["""+json.dumps(received_data, sort_keys=True, indent=4)+"""]
        """)

    t.log(level="info", message="""
============================================
        SEND ARP \t| SUCCESS
============================================""")

    t.log(level="debug", message=""" ======== FUNCTION [END] _send_arp ======== """)
    return received_data
# def _send_arp  [END].




# Commeting this function since it is no longer used.
# def _is_it_label_name(label_text, rt_data=None):
#     """
#     Is the passed "label_text" a valid device / LSA / traffic stream block / etc label name.
#
#     Args:
#         Mandatory
#             label_text(str): Label name to look up for handles.
#             rt_data(mandatory): PDT RT Data Object.
#
#     Returns:
#        (bool): True if label exists; Otherwise False.
#     """
#
#     # t.log(level="debug", message=""" ======== FUNCTION [START] _is_it_label_name ======== """)
#
#     # t.log(level="info", message="Checking label_text = ["+str(label_text)+"] ")
#
#
#
#     handle_label_item__split_name = _get_label_base_name(label=label_text)
#     if handle_label_item__split_name["result"] is True:
#         handle_label_item__base_name = handle_label_item__split_name["base_name"]
#         handle_label_item__sec_label = handle_label_item__split_name["secondary_label"]
#         find_handle_by_label__result = _find_handle_by_label(
#             rt_data=rt_data,
#             primary_label=handle_label_item__base_name,
#             key_to_find=handle_label_item__sec_label if handle_label_item__sec_label is not None else "handle",
#             test_existence_only=True
#         )
#         if find_handle_by_label__result:
#
#             # t.log(level="debug", message=""" ======== FUNCTION [END] _is_it_label_name ======== """)
#             return True
#
#     # t.log(level="debug", message=""" ======== FUNCTION [END] _is_it_label_name ======== """)
#     return False


# Commeting this function since it is no longer used.
# def _is_it_port_label_name(label_text, rt_data=None):
#     """
#     Is the passed "label_text" a valid Spirent Port label name.
#
#     Args:
#         Mandatory
#             label_text(str): Label name to look up for handles.
#             rt_data(mandatory): PDT RT Data Object.
#
#     Returns:
#        (bool): True if label exists; Otherwise False.
#     """
#
#     # t.log(level="debug", message=""" ======== FUNCTION [START] _is_it_port_label_name ======== """)
#
#
#     # t.log(level="info", message="Checking label_text = ["+str(label_text)+"] ")
#     if label_text in rt_data.stc_port_handle_map:
#         # t.log(level="debug", message=""" ======== FUNCTION [END] _is_it_port_label_name ======== """)
#         return True
#     else:
#         # t.log(level="debug", message=""" ======== FUNCTION [END] _is_it_port_label_name ======== """)
#         return False


# Commeting this function since it is no longer used.
# def _replace_all_labels(rt_handle, data, rt_data=None):
#     """
#     Tries to traverse the entire data structure and
#     replaces any labels occurring as keys or values.
#
#     Cause for future concern.
#         I am ignoring other possible type classes
#     while checking instance type using "isinstance".
#
#     Args:
#         Mandatory
#             rt_handle: Toby Router Tester Handle.
#             rt_data(mandatory): PDT RT Data Object.
#             data(dict): dict in which to do recursive
#             lookup for finding and replacing label names.
#
#     Returns:
#        (dict): Original dict after making all substitutions
#         of the labels to corresponding handles.
#     """
#
#     # t.log(level="debug", message=""" ======== FUNCTION [START] _replace_all_labels ======== """)
#
#     # t.log(level="info", message="data = ["+json.dumps(data, sort_keys=True, indent=4)+"] ")
#
#
#     if isinstance(data, dict):
#         for key_item in data:
#             # print("key_item = [" + key_item + "] ")
#             substituted_key = _replace_all_labels(
#                 rt_handle,
#                 key_item,
#                 rt_data=rt_data,
#             )
#             data[substituted_key] = data.pop(key_item)
#             data[substituted_key] = _replace_all_labels(
#                 rt_handle,
#                 rt_data=rt_data,
#                 data=data[substituted_key]
#             )
#     elif isinstance(data, list):
#         for i in range(len(data)):
#             # print("list_item = [" + str(data[i])+ "] ")
#             data[i] = _replace_all_labels(
#                 rt_handle,
#                 rt_data=rt_data,
#                 data=data[i]
#             )
#     # elif isinstance(data, str): # Change "str" to "basestring" if we need to switch loyalty to Python 2 exclusively.
#     else:
#         # Risky to club everything in "else" here.
#         # In future, this section of code would create problems.
#         if isinstance(data, str):
#             if _is_it_label_name(data, rt_data=rt_data) is True:
#                 # data = self.stc_handle_map[data]["handle"]
#                 handle_label_item__split_name = _get_label_base_name(label=data)
#                 if handle_label_item__split_name["result"] is True:
#                     handle_label_item__base_name = handle_label_item__split_name["base_name"]
#                     handle_label_item__sec_label = handle_label_item__split_name["secondary_label"]
#                     data = _find_handle_by_label(
#                         rt_data=rt_data,
#                         primary_label=handle_label_item__base_name,
#                         key_to_find=handle_label_item__sec_label if handle_label_item__sec_label is not None else "handle",
#                     )
#                 else:
#                     raise Exception("""Could not retrieve handle list for the string label name.
#                         data = ["""+repr(data)+"""]
#                         handle_label_item__split_name = ["""+repr(handle_label_item__split_name)+"""]
#                     """)
#
#             elif _is_it_port_label_name(data, rt_data=rt_data) is True:
#                 data = rt_data.stc_port_handle_map[data]["handle"]
#
#     # t.log(level="debug", message=""" ======== FUNCTION [END] _replace_all_labels ======== """)
#     return data




# def _get_real_port_name    [START].
def _get_real_port_name(rt_data=None, **kwargs):
    """
    Returns the actual port name(like "/5/8") when
    port handle is passed(like "port1").

    Args:
        Mandatory
            rt_data(mandatory): PDT RT Data Object.
            port_handle(str): Spirent Port Handle.

    Returns:
        port_real_name(str): Real name of Spirent port whose port handle was passed.
    """
    if "port_handle" not in kwargs:
        t.log(level="error", message="Mandatory arg 'port_handle' missing in call to _get_real_port_name. ")
        return None

    for(port_name, port_handle) in rt_data.stc_port_handle_map.items():
        if port_handle == kwargs["port_handle"]:
            return rt_data.notational_to_actual__port_map[port_name]

    return kwargs["port_handle"] # Return original "port_handle" if the real port name was not found.
# def _get_real_port_name    [END].
