#!/usr/local/bin/python3
# coding=utf-8
"""
    Copyright (C) 2003-2015, Juniper Networks, Inc.
    All rights reserved.
    Author:
        jpzhao
        ajaykv
    Description:
        Offline config engine tool.
    Usage:
        checkconfig.py -t toby.params.yaml -c config.yaml
        checkconfig.py -t toby.params.yaml -c config.yaml -v
        checkconfig.py -t toby.params.yaml -c config.yaml -d r0
        checkconfig.py -t toby.params.yaml -c config.yaml -d r0,r1
        checkconfig.py -t toby.params.yaml -c config.yaml -d r0,r1 -l True
        checkconfig.py -t toby.params.yaml -c config.yaml -d r0,r1 -l 1 
 """

import sys
import getopt
import builtins
import pprint
import re
from jnpr.toby.init.init import init
from jnpr.toby.utils.Vars import Vars
from jnpr.toby.hldcl.device import Device
from jnpr.toby.engines.config.config import config
import jnpr.toby.engines.config.config_utils as config_utils


builtins.t = init_obj = init()

def usage():
    '''
    print out usage information
    '''
    help_msg = '''
    checkconfig.py is an offline config engine tool. it allows you to
    build up your configuration using the config engine without connecting
    to the devices. This saves time and resource while you are experimenting and
    building up your configurations.

    This tool will do all of these offline:
        - check the config file syntax in yaml format,
        - findout if tvars is available in params
        - check if the scaling syntax, tagging is written correctly
        - convert to list of set cmds
        - print out the final result of your config, ready for loading to routers
        - print out complete t_vars avaiable to use in config engine.

    Usage:
       checkconfig.py -t topy.params.yaml -c config.yaml [-v|tvars] [-d|device_list] [-l|load]

    '''
    print(help_msg)
    
        
def main():
    '''
    check config yaml file offline
    '''
    try:
        opts = getopt.getopt(sys.argv[1:], 'hvd:t:c:l:', ['config=', 'device_list=', 'help', 'tvars','load='])[0]
        if not opts:
            print("*** missing arguments ***")
            usage()
            sys.exit()
    except getopt.GetoptError:
        print("*** wrong syntax ***")
        usage()
        sys.exit(2)

    device_list = print_tvars = tdata = load = None
    for opt, arg in opts:
        if opt == '-t':
            t_file = arg
            tdata = config_utils.read_yaml(file=t_file, ordered=False)
            t.t_dict = tdata['t']
            t.resources = tdata['t']['resources']
            t._create_global_tv_dictionary()
            builtins.tv = t.tv_dict
        elif opt in ('--config', '-c'):
            config_file = arg
        elif opt in ('--tvars', '-v'):
            print_tvars = arg
        elif opt in ('--device_list', '-d'):
            device_list = arg
        elif opt in ('--load', '-l'):
            load = arg
        elif opt in ('-h', '--help'):
            usage()
            sys.exit()

    if device_list is not None:
        device_list = device_list.split(',')

    cfg = config()
    if tdata is not None:
        cfg._config__make_c_dict()
    else:
        raise Exception('missing toby yaml file option "-t"')

    if load is not None and re.match(r'true|1', load, re.IGNORECASE):
        print("++++ Config Engine : Loading on devices")
        for device in device_list:
            dh = t._connect_device(resource=device)
            dh = t.get_handle(resource=device)
            cfg = config()
            cfg.device_handle_map[device]=dh
            cfg_set = cfg.config_engine(device_list=device,config_file=config_file)
    else:
        cfg_set = cfg.config_engine(config_file=config_file, offline='True')
        cfg_set = cfg.cfg
        print("++++ Config Engine results:")
        if not device_list:
            device_list = cfg.device_list
        for dev in device_list:
            if dev not in cfg_set:
                continue
            print("\n** "+ dev + ":")
            for line in cfg_set[dev]:
                if isinstance(line, str):
                    print(line)
                else:
                    pprint.pprint(line)

        if print_tvars is not None:
            print('\n\n=== Print  cv  dictionary (on top of t_dict) :\n')
            pprint.pprint(cfg.c_dict)
            print('\n\n==role tags: ')
            pprint.pprint(cfg.roles)

            print('\n*** Available global tv ***\n')
            pprint.pprint(tv)

            print('\n*** Available shared cv ***\n')
            try:
               pprint.pprint(cfg.get_cv())
            except:
               print('no cv available')

if __name__ == '__main__':
    main()
    sys.exit()
