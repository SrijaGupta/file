from mock import patch
from mock import MagicMock

import unittest2 as unittest
import unittest
import builtins

from lxml import etree

from robot.libraries.BuiltIn import BuiltIn
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.device import execute_cli_command_on_device

from jnpr.toby.init.attrib_init.attribute_init import populate_attributes, parse_device_inventory, log, print_help, read_inventory_file, config_inventory_pattern

CONFIGURATION_DICT = {
    'CHASSIS_CONFIGURATION' : {
        'pattern' : 'member.*|node.*|bsys-re.*|gnf2-re.*'
    },
    'MODULE_CONFIGURATION' : {
        'Chassis' : {
            'name' : 'Chassis',
            'pattern' : 'Chassis',
            'file' : 'chassis',
            'key' : 'chassis',
            'index' : False
        },
        'Routing Engine' : {
            'name' : 'Routing Engine',
            'pattern' : 'Routing Engine.*',
            'file' : 'routing_engine',
            'key' : 're',
            'index' : True
        },
        'Line Card' : {
            'name' : 'Line Card',
            'pattern' : 'FPC.*',
            'file' : 'fpc',
            'key' : 'fpc',
            'index' : True
        },
        'Interface Card' : {
            'name' : 'Interface Card',
            'pattern' : 'PIC.*',
            'file' : 'pic',
            'key' : 'pic',
            'index' : True
        },
        'Modular Interface Card' : {
            'name' : 'Modular Interface Card',
            'pattern' : 'MIC.*',
            'file' : 'mic',
            'key' : 'mic',
            'index' : True
        },
        'Power Supply' : {
            'name' : 'Power Supply',
            'pattern' : 'Power Supply.*|PEM.*|PDU.*|PSM.*',
            'file' : 'power',
            'key' : 'ps',
            'index' : True
        },
        'Fan Tray' : {
            'name' : 'Fan Tray',
            'pattern' : 'Fan Tray.*',
            'file' : 'fantray',
            'key' : 'ft',
            'index' : True
        },
        'Fabric' : {
            'name' : 'Fabric',
            'pattern' : 'SFB.*|SIB.*',
            'file' : 'fabric',
            'key' : 'fab',
            'index' : True
        }
    },
    'OVERRIDE_CONFIGURATION' : {
        'Chassis' : {
            'name' : 'Chassis',
            'key' : 'chassis',
            'override' : {
                'Routing Engine' : {
                    'override_pattern' : '_override_re_',
                    'name' : 'Routing Engine',
                    'key' : 're'
                },
                'Line Card' : {
                    'override_pattern' : '_override_fpc_',
                    'name' : 'Line Card',
                    'key' : 'fpc'
                },
                'Fan Tray' : {
                    'override_pattern' : '_override_ft_',
                    'name' : 'Fan Tray',
                    'key' : 'ft'
                },
                'Power Supply' : {
                    'override_pattern' : '_override_ps_',
                    'name' : 'Power Supply',
                    'key' : 'ps'
                }
            }
        },
        'Routing Engine' : {
            'name' : 'Routing Engine',
            'key' : 're',
            'override' : {
                'Chassis' : {
                    'override_pattern' : '_override_chassis_',
                    'name' : 'Chassis',
                    'key' : 'chassis'
                }
            }
        },
        'Fan Tray' : {
            'name' : 'Fan Tray',
            'key' : 'ft',
            'override' : {
                'Chassis' : {
                    'override_pattern' : '_override_chassis_',
                    'name' : 'Chassis',
                    'key' : 'chassis'
                }
            }
        },
        'Power Supply' : {
            'name' : 'Power Supply',
            'key' : 'ps',
            'override' : {
                'Chassis' : {
                    'override_pattern' : '_override_chassis_',
                    'name' : 'Chassis',
                    'key' : 'chassis'
                }
            }
        },
        'Line Card' : {
            'name' : 'Line Card',
            'key' : 'fpc',
            'override' : {
                'Interface Card' : {
                    'override_pattern' : '_override_pic_',
                    'name' : 'Interface Card',
                    'key' : 'pic'
                }
            }
        }
    }
}

DEFAULT_INVENTORY_DICT = {
    'chassis': {'default': {'chassis_key': 'chassis_value'}},
    'fabric': {'default': {'fabric_key': 'fabric_value'}},
    'fantray': {'default': {'ft_key': 'ft_value'}},
    'fpc': {'default': {'fpc_key': 'fpc_value'}},
    'mic': {'default': {'mic_key': 'mic_value'}},
    'pic': {'default': {'pic_key': 'pic_value'}},
    'power': {'default': {'ps_key': 'ps_value'}},
    'routing_engine': {'default': {'re_key': 're_value'}}
}

class TestAttribInitMain(unittest.TestCase):
    '''
    Unit test class for Attribute Initaliser
    '''

    MX80_CHASSIS_INFO_DICT = {
        'Midplane': ['MX80'],
        'PEM 0': ['AC Power Entry Module'],
        'Routing Engine': ['Routing Engine'],
        'TFEB 0': ['Forwarding Engine Processor', {
            'QXM 0': ['MPC QXM']
        }],
        'FPC 0': ['MPC BUILTIN', {
            'MIC 0': ['4x 10GE XFP', {
                'PIC 0': ['4x 10GE XFP', {
                    'Xcvr 0': ['XFP-10G-SR'],
                    'Xcvr 3': ['XFP-10G-SR']
                }]
            }]
        }],
        'FPC 1': ['MPC BUILTIN', {
            'MIC 1': ['3D 20x 1GE(LAN) SFP', {
                'PIC 2': ['10x 1GE(LAN) SFP', {
                    'Xcvr 0': ['SFP-SX'], 
                    'Xcvr 7': ['SFP-SX']}
                ], 
                'PIC 3': ['10x 1GE(LAN) SFP', {
                    'Xcvr 0': ['SFP-SX'], 
                    'Xcvr 9': ['SFP-SX']
                }]
            }]
        }], 
        'Fan Tray': ['Fan Tray'],
        'Chassis': ['MX80']
    }

    MX960_CHASSIS_INFO_DICT = {
        'Midplane': ['MX960 Backplane'],
        'FPM Board': ['Front Panel Display'],
        'PDM': ['Power Distribution Module'],
        'PEM 0': ['DC 4.1kW Power Entry Module'],
        'PEM 1': ['DC 4.1kW Power Entry Module'],
        'PEM 2': ['DC 4.1kW Power Entry Module'],
        'PEM 3': ['DC 4.1kW Power Entry Module'],
        'Routing Engine 0': ['RE-S-2X00x6'],
        'Routing Engine 1': ['RE-S-2X00x6'],
        'CB 0': ['Enhanced MX SCB 2'],
        'CB 1': ['Enhanced MX SCB 2'],
        'FPC 0': ['MPCE Type 2 3D EQ', {
            'CPU': ['MPCE PMB 2G '],
            'MIC 0': ['2xOC12/8xOC3 CC-CE', {
                'PIC 0': ['2xOC12/8xOC3 CC-CE', {
                    'Xcvr 1': ['SFP-SX']
                }]
            }],
            'MIC 1': ['MS-MIC-16G', {
                'PIC 2': ['MS-MIC-16G']
            }],
            'QXM 0': ['MPC QXM'],
            'QXM 1': ['MPC QXM']
        }],
        'FPC 1': ['MPCE Type 3 3D', {
            'CPU': ['HMPC PMB 2G '],
            'MIC 0': ['3D 20x 1GE(LAN) SFP', {
                'PIC 0': ['10x 1GE(LAN) SFP', {
                    'Xcvr 0': ['SFP-SX'],
                    'Xcvr 1': ['SFP-SX']
                }],
                'PIC 1': ['10x 1GE(LAN) SFP', {
                    'Xcvr 0': ['SFP-SX'],
                    'Xcvr 5': ['SFP-SX']
                }]
            }]
        }],
        'FPC 2': ['MPCE Type 3 3D', {
            'CPU': ['HMPC PMB 2G '],
            'MIC 0': ['1X100GE CFP', {
                'PIC 0': ['1X100GE CFP', {
                    'Xcvr 0': ['CFP-100G-LR4']
                }]
            }],
            'MIC 1': ['3D 20x 1GE(LAN) SFP', {
                'PIC 2': ['10x 1GE(LAN) SFP', {
                    'Xcvr 2': ['SFP-SX'],
                    'Xcvr 6': ['SFP-SX']
                }],
                'PIC 3': ['10x 1GE(LAN) SFP', {
                    'Xcvr 5': ['SFP-SX']
                }]
            }]
        }],
        'FPC 3': ['MPC 3D 16x 10GE', {
            'CPU': ['AMPC PMB'],
            'PIC 0': ['4x 10GE(LAN) SFP+', {
                'Xcvr 0': ['SFP+-10G-SR'],
                'Xcvr 2': ['SFP+-10G-SR']
            }],
            'PIC 1': ['4x 10GE(LAN) SFP+', {
                'Xcvr 0': ['SFP+-10G-SR'],
                'Xcvr 2': ['DUAL-SFP+-SR/SFP-SX']
            }],
            'PIC 2': ['4x 10GE(LAN) SFP+', {
                'Xcvr 1': ['SFP+-10G-SR'],
                'Xcvr 2': ['SFP+-10G-SR']
            }],
            'PIC 3': ['4x 10GE(LAN) SFP+', {
                'Xcvr 0': ['DUAL-SFP+-SR/SFP-SX'],
                'Xcvr 1': ['SFP+-10G-SR'],
                'Xcvr 2': ['SFP+-10G-SR']
            }]
        }],
        'FPC 4': ['MPC5E 3D Q 2CGE+4XGE', {
            'CPU': ['RMPC PMB'],
            'PIC 0': ['2X10GE SFPP OTN', {
                'Xcvr 0': ['SFP+-10G-SR'],
                'Xcvr 1': ['SFP+-10G-SR']
            }],
            'PIC 1': ['1X100GE CFP2 OTN'],
            'PIC 2': ['2X10GE SFPP OTN', {
                'Xcvr 0': ['SFP+-10G-SR'],
                'Xcvr 1': ['SFP+-10G-SR']
            }],
            'PIC 3': ['1X100GE CFP2 OTN']
        }],
        'FPC 5': ['MS-MPC', {
            'CPU': ['MS-MPC-PMB'],
            'PIC 0': ['MS-MPC-PIC'],
            'PIC 1': ['MS-MPC-PIC'],
            'PIC 2': ['MS-MPC-PIC'],
            'PIC 3': ['MS-MPC-PIC']
        }],
        'FPC 6': ['MPCE Type 3 3D', {
            'CPU': ['HMPC PMB 2G '],
            'MIC 0': ['MIC-3D-4OC3OC12-1OC48', {
                'PIC 0': ['MIC-3D-4OC3OC12-1OC48', {
                    'Xcvr 0': ['SFP-SX'],
                    'Xcvr 1': ['SFP-SX']
                }]
            }],
            'MIC 1': ['1X100GE CXP', {
                'PIC 2': ['1X100GE CXP', {
                    'Xcvr 0': ['CXP-100G-SR10']
                }]
            }]
        }],
        'FPC 7': ['MPC5E 3D 24XGE+6XLGE', {
            'CPU': ['RMPC PMB'],
            'PIC 0': ['12X10GE SFPP OTN', {
                'Xcvr 0': ['SFP+-10G-SR']
            }],
            'PIC 1': ['12X10GE SFPP OTN', {
                'Xcvr 0': ['SFP+-10G-SR']
            }],
            'PIC 2': ['3X40GE QSFPP'],
            'PIC 3': ['3X40GE QSFPP'],
            'WAN MEZZ': ['MPC5E 24XGE OTN Mezz']
        }], 
        'FPC 9': ['MPCE Type 2 3D', {
            'CPU': ['MPCE PMB 2G '],
            'MIC 0': ['3D 20x 1GE(LAN) SFP', {
                'PIC 0': ['10x 1GE(LAN) SFP', {
                    'Xcvr 0': ['SFP-SX'],
                    'Xcvr 1': ['SFP-T']
                }],
                'PIC 1': ['10x 1GE(LAN) SFP', {
                    'Xcvr 0': ['SFP-SX'],
                    'Xcvr 1': ['SFP-T'],
                    'Xcvr 7': ['SFP-SX']
                }]
            }],
            'MIC 1': ['3D 4x 10GE  XFP', {
                'PIC 2': ['2x 10GE  XFP', {
                    'Xcvr 0': ['XFP-10G-SR']
                }],
                'PIC 3': ['2x 10GE  XFP']
            }]
        }],
        'FPC 10': ['MPC Type 2 3D', {
            'CPU': ['MPC PMB 2G '],
            'MIC 0': ['MIC-3D-8DS3-E3', {
                'PIC 0': ['MIC-3D-8DS3-E3']
            }],
            'MIC 1': ['16x CHE1T1, RJ48', {
                'PIC 2': ['16x CHE1T1, RJ48']
            }]
        }],
        'FPC 11': ['MPC Type 2 3D EQ', {
            'CPU': ['MPC PMB 2G '],
            'MIC 0': ['MIC-3D-1OC192-XFP', {
                'PIC 0': ['MIC-3D-1OC192-XFP', {
                    'Xcvr 0': ['XFP-OC192-SR']
                }]
            }],
            'MIC 1': ['MIC-3D-8CHOC3-4CHOC12', {
                'PIC 2': ['MIC-3D-8CHOC3-4CHOC12', {
                    'Xcvr 0': ['SFP-SX']
                }]
            }],
            'QXM 0': ['MPC QXM'],
            'QXM 1': ['MPC QXM']
        }],
        'Fan Tray 0': ['Enhanced Fan Tray'],
        'Fan Tray 1': ['Enhanced Fan Tray'],
        'Chassis': ['MX960']
    }

    PTX5000_CHASSIS_INFO_DICT = {
        'Midplane': ['Midplane-8SeP'],
        'FPM': ['Front Panel Display'],
        'PDU 0': ['High Capacity DC PDU', {
            'PSM 0': ['High Capacity DC PSM'],
            'PSM 1': ['High Capacity DC PSM'],
            'PSM 2': ['High Capacity DC PSM'],
            'PSM 3': ['High Capacity DC PSM']
        }],
        'CCG 0': ['Clock Generator'],
        'CCG 1': ['Clock Generator'],
        'Routing Engine 0': ['RE-PTX-2X00x8'],
        'Routing Engine 1': ['RE-PTX-2X00x8'],
        'CB 0': ['Control Board 2'],
        'CB 1': ['Control Board 2'],
        'FPC 3': ['FPC-P2', {
            'CPU': ['SMPC PMB 16GB DRAM'],
            'PIC 0': ['15x100GE/15x40GE/60x10GE QSFP28 PIC', {
                'Xcvr 0': ['QSFP-100G-SR4-T2'],
                'Xcvr 1': ['QSFP-100GBASE-SR4'],
                'Xcvr 5': ['QSFP+-40G-SR4'],
                'Xcvr 6': ['QSFP+-4X10G-SR'],
                'Xcvr 7': ['QSFP+-40G-SR4'],
                'Xcvr 12': ['QSFP28-100G-AOC-20M']
            }],
            'PIC 1': ['48x10G/12x40G(LWO)QSFP+', {
                'Xcvr 4': ['QSFP+-40G-SR4'],
                'Xcvr 11': ['QSFP-100GBASE-SR4']
            }]
        }],
        'FPC 4': ['FPC-P2', {
            'CPU': ['SMPC PMB 16GB DRAM'],
            'PIC 1': ['None']
        }],
        'FPC 5': ['FPC', {
            'CPU': ['SNG PMB'],
            'PIC 1': ['24x 10GE(LWO) SFP+', {
                'Xcvr 1': ['SFP+-10G-SR'],
                'Xcvr 3': ['SFP+-10G-LR'],
                'Xcvr 5': ['SFP+-10G-SR'],
                'Xcvr 7': ['SFP+-10G-SR'],
                'Xcvr 10': ['SFP+-10G-SR'],
                'Xcvr 13': ['SFP+-10G-SR']
            }]
        }], 
        'SPMB 0': ['PTX5K CB PMB'],
        'SPMB 1': ['PTX5K CB PMB'],
        'SIB 0': ['SIB-I'],
        'SIB 1': ['SIB-I'],
        'SIB 2': ['SIB-I'],
        'SIB 3': ['SIB-I'],
        'SIB 4': ['SIB-I'],
        'SIB 5': ['SIB-I'],
        'SIB 6': ['SIB-I'],
        'SIB 7': ['SIB-I'],
        'SIB 8': ['SIB-I'],
        'Fan Tray 0': ['Vertical Fan Tray'],
        'Fan Tray 1': ['Horizontal Fan Tray V3'],
        'Fan Tray 2': ['Horizontal Fan Tray V3'],
        'Chassis': ['PTX5000']
    }

    PTX10016_CHASSIS_INFO_DICT = {
        'CB 0': ['Control Board'],
        'Chassis': ['JNP10016 [PTX10016]'],
        'FPC 0': ['LC1103 - 2C / 6Q / 60X', {
            'CPU': ['FPC CPU'],
            'Mezz': ['ULC-60S-6Q Mezz Board'],
            'PIC 0': ['60X10G', {
                'Xcvr 0': ['SFP+-10G-SR']
            }]
        }],
        'FPC 5': ['LC1101 - 30C / 30Q / 96X', {
            'CPU': ['FPC CPU'],
            'PIC 0': ['30x100GE/30x40GE/96x10GE', {
                'Xcvr 1': ['40GBASE eSR4']
            }]
        }],
        'FPD Board': ['Front Panel Display'],
        'FTC 0': ['Fan Controller 16'],
        'Fan Tray 0': ['Fan Tray 16'],
        'Midplane': ['Midplane 16'],
        'Power Supply 0': ['Power Supply DC'],
        'Routing Engine 0': ['RE-PTX-2X00x4'],
        'Routing Engine 1': ['RE-PTX-2X00x4'],
        'SIB 0': ['Switch Fabric 16'],
    }

    EX3400_CHASSIS_INFO_DICT = {
        'Pseudo CB 0': ['None'],
        'Routing Engine 0': ['RE-EX3400-24T'],
        'FPC 0': ['EX3400-24T', {
            'CPU': ['FPC CPU'],
            'PIC 0': ['24x10/100/1000 Base-T'],
            'PIC 1': ['2x40G QSFP'],
            'PIC 2': ['4x10G SFP/SFP+', {
                'Xcvr 3': ['SFP-T']
            }]
        }],
        'Power Supply 0': ['JPSU-150W-AC-AFO'],
        'Fan Tray 0': ['Fan Module, Airflow Out (AFO)'],
        'Fan Tray 1': ['Fan Module, Airflow Out (AFO)'],
        'Chassis': ['EX3400-24T']
    }

    QFX5210_CHASSIS_INFO_DICT = {
        'Pseudo CB 0': ['None'],
        'Routing Engine 0': ['RE-QFX5210-64C'],
        'FPC 0': ['QFX5210-64C', {
            'CPU': ['FPC CPU'],
            'PIC 0': ['64X40G/64X100G-QSFP', {
                'Xcvr 1': ['QSFP+-40G-SR4'],
                'Xcvr 2': ['QSFP-100GBASE-SR4'],
                'Xcvr 11': ['QSFP28-100G-CU3M'],
                'Xcvr 16': ['QSFP28-100G-CU5M'],
                'Xcvr 23': ['QSFP-100G-SR4-T2'],
                'Xcvr 25': ['QSFP+-40G-CU3M'],
                'Xcvr 59': ['QSFP-100G-SR4-T2'],
                'Xcvr 64': ['SFP+-10G-SR']
            }]
        }],
        'Power Supply 0': ['FPC Type 2'],
        'Power Supply 1': ['FPC Type 2'],
        'Fan Tray 0': ['QFX5210 Fan Tray 0, Front to Back Airflow - AFO'],
        'Fan Tray 1': ['QFX5210 Fan Tray 1, Front to Back Airflow - AFO'],
        'Fan Tray 2': ['QFX5210 Fan Tray 2, Front to Back Airflow - AFO'],
        'Fan Tray 3': ['QFX5210 Fan Tray 3, Front to Back Airflow - AFO'],
        'Chassis': ['QFX5210-64C']
    }

    QFX10002_CHASSIS_INFO_DICT = {
        'Pseudo CB 0': ['None'],
        'Routing Engine 0': ['RE-QFX10002-72Q'],
        'FPC 0': ['QFX10002-72Q', {
            'CPU': ['FPC CPU'],
            'PIC 0': ['72X40G', {
                'Xcvr 0': ['QSFP+-40G-SR4']
            }],
            'Mezz': ['Mezzanine Board']
        }],
        'Power Supply 0': ['DC AFO 1600W PSU'],
        'Power Supply 1': ['DC AFO 1600W PSU'],
        'Power Supply 2': ['DC AFO 1600W PSU'],
        'Power Supply 3': ['DC AFO 1600W PSU'],
        'Fan Tray 0': ['QFX10002 Fan Tray 0, Front to Back Airflow - AFO'],
        'Fan Tray 1': ['QFX10002 Fan Tray 1, Front to Back Airflow - AFO'],
        'Fan Tray 2': ['QFX10002 Fan Tray 2, Front to Back Airflow - AFO'],
        'Chassis': ['QFX10002-72Q']
    }

    VC_CHASSIS_INFO_DICT = {
        'Routing Engine 0': ['EX4300-24T'],
        'Routing Engine 1': ['EX4300-48P'],
        'FPC 0': ['EX4300-24T', {
            'CPU': ['FPC CPU'],
            'PIC 0': ['24x 10/100/1000 Base-T'],
            'PIC 1': ['4x 40GE QSFP+', {
                'Xcvr 0': ['QSFP+-40G-CU3M'],
                'Xcvr 1': ['QSFP+-40G-ACU10M']
            }],
            'PIC 2': ['4x 1G/10G SFP/SFP+', {
                'Xcvr 0': ['SFP+-10G-ACU5M'],
                'Xcvr 2': ['SFP+-10G-USR'],
                'Xcvr 3': ['SFP+-10G-SR']
            }],
            'Power Supply 0': ['JPSU-350-AC-AFO-A'],
            'Fan Tray 0': ['Fan Module, Airflow Out (AFO)'],
            'Fan Tray 1': ['Fan Module, Airflow Out (AFO)']
        }],
        'FPC 1': ['EX4300-48P', {
            'CPU': ['FPC CPU'],
            'PIC 0': ['48x 10/100/1000 Base-T'],
            'PIC 1': ['4x 40GE QSFP+', {
                'Xcvr 1': ['QSFP+-40G-CU3M']
            }],
            'PIC 2': ['4x 1G/10G SFP/SFP+', {
                'Xcvr 0': ['SFP+-10G-USR'],
                'Xcvr 1': ['SFP+-10G-ACU5M'],
                'Xcvr 3': ['SFP+-10G-SR']
            }],
            'Power Supply 0': ['JPSU-1100-AC-AFO-A'],
            'Fan Tray 0': ['Fan Module, Airflow Out (AFO)'],
            'Fan Tray 1': ['Fan Module, Airflow Out (AFO)']
        }],
        'FPC 2': ['EX4300-24P', {
            'CPU': ['FPC CPU'],
            'PIC 0': ['24x 10/100/1000 Base-T'],
            'PIC 1': ['4x 40GE QSFP+', {
                'Xcvr 0': ['QSFP+-40G-CU5M'],
                'Xcvr 1': ['QSFP+-40G-CU3M']
            }],
            'PIC 2': ['4x 1G/10G SFP/SFP+', {
                'Xcvr 0': ['SFP+-10G-SR'],
                'Xcvr 1': ['SFP+-10G-ACU5M'],
                'Xcvr 3': ['SFP+-10G-SR']
            }],
            'Power Supply 0': ['JPSU-350-AC-AFO-A'],
            'Power Supply 1': ['None'],
            'Fan Tray 0': ['Fan Module, Airflow Out (AFO)'],
            'Fan Tray 1': ['Fan Module, Airflow Out (AFO)']
        }],
        'FPC 3': ['EX4300-48T', {
            'CPU': ['FPC CPU'],
            'PIC 0': ['48x 10/100/1000 Base-T'],
            'PIC 1': ['4x 40GE QSFP+', {
                'Xcvr 0': ['QSFP+-40G-ACU10M'],
                'Xcvr 1': ['QSFP+-40G-CU5M']
            }],
            'PIC 2': ['4x 1G/10G SFP/SFP+', {
                'Xcvr 0': ['SFP+-10G-SR'],
                'Xcvr 1': ['SFP+-10G-SR']
            }],
            'Power Supply 0': ['JPSU-350-AC-AFO-A'],
            'Fan Tray 0': ['Fan Module, Airflow Out (AFO)'],
            'Fan Tray 1': ['Fan Module, Airflow Out (AFO)']
        }],
        'Chassis': ['Virtual Chassis']
    }

    GNF_CHASSIS_INFO_DICT = {
        'bsys-re0': {
            'Midplane': ['Enhanced MX480 Midplane'],
            'FPM Board': ['Front Panel Display'],
            'PEM 0': ['DC 2.4kW Power Entry Module'],
            'PEM 1': ['DC 2.4kW Power Entry Module'],
            'PEM 2': ['DC 2.4kW Power Entry Module'],
            'PEM 3': ['DC 2.4kW Power Entry Module'],
            'Routing Engine 0': ['RE-S-2X00x6'],
            'Routing Engine 1': ['RE-S-2X00x6'],
            'CB 0': ['Enhanced MX SCB 2'],
            'CB 1': ['Enhanced MX SCB 2'],
            'FPC 1': ['MPCE 3D 16x 10GE', {
                'CPU': ['AMPC PMB'],
                'PIC 0': ['4x 10GE(LAN) SFP+', {
                    'Xcvr 0': ['SFP+-10G-ER'],
                    'Xcvr 1': ['SFP+-10G-ER'],
                    'Xcvr 2': ['SFP+-10G-ER'],
                    'Xcvr 3': ['SFP+-10G-ER']
                }],
                'PIC 1': ['4x 10GE(LAN) SFP+', {
                    'Xcvr 0': ['SFP+-10G-ER'],
                    'Xcvr 1': ['SFP+-10G-ER'],
                    'Xcvr 2': ['SFP+-10G-ER'],
                    'Xcvr 3': ['SFP+-10G-ER']
                }],
                'PIC 2': ['4x 10GE(LAN) SFP+', {
                    'Xcvr 0': ['SFP+-10G-ER'],
                    'Xcvr 2': ['SFP+-10G-ER'],
                    'Xcvr 3': ['SFP+-10G-ER']
                }],
                'PIC 3': ['4x 10GE(LAN) SFP+', {
                    'Xcvr 0': ['SFP+-10G-ER'],
                    'Xcvr 1': ['SFP+-10G-ER'],
                    'Xcvr 2': ['SFP+-10G-ER'],
                    'Xcvr 3': ['SFP+-10G-ER']
                }]
            }],
            'Fan Tray': ['Enhanced Left Fan Tray'],
            'Chassis': ['MX480']
        },
        'gnf1-re0': {
            'Chassis': ['MX480-GNF'],
            'Routing Engine 0': ['RE-GNF-2000x1'],
            'Routing Engine 1': ['RE-GNF-2000x1']
        }
    }

    @patch('jnpr.toby.init.attrib_init.attribute_init.INVENTORY_INFORMATION', DEFAULT_INVENTORY_DICT)
    @patch('jnpr.toby.init.attrib_init.attribute_init.CHASSIS_CONFIGURATION', CONFIGURATION_DICT['CHASSIS_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.MODULE_CONFIGURATION', CONFIGURATION_DICT['MODULE_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.OVERRIDE_CONFIGURATION', CONFIGURATION_DICT['OVERRIDE_CONFIGURATION'])

    def test_populate_attributes_for_mx80(self):
        '''
        Unit test for method : attribute_init.populate_attributes for MX80 platform
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing with MX80 Sample Definition")

        self.assertIsInstance(populate_attributes(self.MX80_CHASSIS_INFO_DICT), dict)

    @patch('jnpr.toby.init.attrib_init.attribute_init.INVENTORY_INFORMATION', DEFAULT_INVENTORY_DICT)
    @patch('jnpr.toby.init.attrib_init.attribute_init.CHASSIS_CONFIGURATION', CONFIGURATION_DICT['CHASSIS_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.MODULE_CONFIGURATION', CONFIGURATION_DICT['MODULE_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.OVERRIDE_CONFIGURATION', CONFIGURATION_DICT['OVERRIDE_CONFIGURATION'])

    def test_populate_attributes_for_mx960(self):
        '''
        Unit test for method : attribute_init.populate_attributes for MX960 platform
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing with MX960 Sample Definition")

        self.assertIsInstance(populate_attributes(self.MX960_CHASSIS_INFO_DICT), dict)

    @patch('jnpr.toby.init.attrib_init.attribute_init.INVENTORY_INFORMATION', DEFAULT_INVENTORY_DICT)
    @patch('jnpr.toby.init.attrib_init.attribute_init.CHASSIS_CONFIGURATION', CONFIGURATION_DICT['CHASSIS_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.MODULE_CONFIGURATION', CONFIGURATION_DICT['MODULE_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.OVERRIDE_CONFIGURATION', CONFIGURATION_DICT['OVERRIDE_CONFIGURATION'])

    def test_populate_attributes_for_ptx5000(self):
        '''
        Unit test for method : attribute_init.populate_attributes for PTX5000 platform
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing with PTX5000 Sample Definition")

        self.assertIsInstance(populate_attributes(self.PTX5000_CHASSIS_INFO_DICT), dict)

    @patch('jnpr.toby.init.attrib_init.attribute_init.INVENTORY_INFORMATION', DEFAULT_INVENTORY_DICT)
    @patch('jnpr.toby.init.attrib_init.attribute_init.CHASSIS_CONFIGURATION', CONFIGURATION_DICT['CHASSIS_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.MODULE_CONFIGURATION', CONFIGURATION_DICT['MODULE_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.OVERRIDE_CONFIGURATION', CONFIGURATION_DICT['OVERRIDE_CONFIGURATION'])

    def test_populate_attributes_for_ptx10016(self):
        '''
        Unit test for method : attribute_init.populate_attributes for PTX10016 platform
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing with PTX10016 Sample Definition")

        self.assertIsInstance(populate_attributes(self.PTX10016_CHASSIS_INFO_DICT), dict)

    @patch('jnpr.toby.init.attrib_init.attribute_init.INVENTORY_INFORMATION', DEFAULT_INVENTORY_DICT)
    @patch('jnpr.toby.init.attrib_init.attribute_init.CHASSIS_CONFIGURATION', CONFIGURATION_DICT['CHASSIS_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.MODULE_CONFIGURATION', CONFIGURATION_DICT['MODULE_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.OVERRIDE_CONFIGURATION', CONFIGURATION_DICT['OVERRIDE_CONFIGURATION'])

    def test_populate_attributes_for_ex3400(self):
        '''
        Unit test for method : attribute_init.populate_attributes for EX3400 platform
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing with EX3400 Sample Definition")

        self.assertIsInstance(populate_attributes(self.EX3400_CHASSIS_INFO_DICT), dict)

    @patch('jnpr.toby.init.attrib_init.attribute_init.INVENTORY_INFORMATION', DEFAULT_INVENTORY_DICT)
    @patch('jnpr.toby.init.attrib_init.attribute_init.CHASSIS_CONFIGURATION', CONFIGURATION_DICT['CHASSIS_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.MODULE_CONFIGURATION', CONFIGURATION_DICT['MODULE_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.OVERRIDE_CONFIGURATION', CONFIGURATION_DICT['OVERRIDE_CONFIGURATION'])

    def test_populate_attributes_for_qfx5210(self):
        '''
        Unit test for method : attribute_init.populate_attributes for QFX5210 platform
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing with QFX5210 Sample Definition")

        self.assertIsInstance(populate_attributes(self.QFX5210_CHASSIS_INFO_DICT), dict)

    @patch('jnpr.toby.init.attrib_init.attribute_init.INVENTORY_INFORMATION', DEFAULT_INVENTORY_DICT)
    @patch('jnpr.toby.init.attrib_init.attribute_init.CHASSIS_CONFIGURATION', CONFIGURATION_DICT['CHASSIS_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.MODULE_CONFIGURATION', CONFIGURATION_DICT['MODULE_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.OVERRIDE_CONFIGURATION', CONFIGURATION_DICT['OVERRIDE_CONFIGURATION'])

    def test_populate_attributes_for_qfx10002(self):
        '''
        Unit test for method : attribute_init.populate_attributes for QFX10002 platform
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing with QFX10002 Sample Definition")

        self.assertIsInstance(populate_attributes(self.QFX10002_CHASSIS_INFO_DICT), dict)

    @patch('jnpr.toby.init.attrib_init.attribute_init.INVENTORY_INFORMATION', DEFAULT_INVENTORY_DICT)
    @patch('jnpr.toby.init.attrib_init.attribute_init.CHASSIS_CONFIGURATION', CONFIGURATION_DICT['CHASSIS_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.MODULE_CONFIGURATION', CONFIGURATION_DICT['MODULE_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.OVERRIDE_CONFIGURATION', CONFIGURATION_DICT['OVERRIDE_CONFIGURATION'])

    def test_populate_attributes_for_vc(self):
        '''
        Unit test for method : attribute_init.populate_attributes for Virtual Chassis platform
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing with Virtual Chassis Sample Definition")

        self.assertIsInstance(populate_attributes(self.VC_CHASSIS_INFO_DICT), dict)

    @patch('jnpr.toby.init.attrib_init.attribute_init.INVENTORY_INFORMATION', DEFAULT_INVENTORY_DICT)
    @patch('jnpr.toby.init.attrib_init.attribute_init.CHASSIS_CONFIGURATION', CONFIGURATION_DICT['CHASSIS_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.MODULE_CONFIGURATION', CONFIGURATION_DICT['MODULE_CONFIGURATION'])
    @patch('jnpr.toby.init.attrib_init.attribute_init.OVERRIDE_CONFIGURATION', CONFIGURATION_DICT['OVERRIDE_CONFIGURATION'])

    def test_populate_attributes_for_gnf(self):
        '''
        Unit test for method : attribute_init.populate_attributes for GNF platform
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing with GNF Sample Definition")

        self.assertIsInstance(populate_attributes(self.GNF_CHASSIS_INFO_DICT), dict)

class TestAttribInitMisc(unittest.TestCase):
    '''
    Unit test class for Attribute Initaliser to cover miscellaneous tests
    '''

    @patch('jnpr.toby.init.attrib_init.attribute_init.load')
    @patch('jnpr.toby.init.attrib_init.attribute_init.os')
    @patch('jnpr.toby.init.attrib_init.attribute_init.open')
    @patch('jnpr.toby.init.attrib_init.attribute_init.read_configuration_file')

    def test_config_inventory_pattern(self, config_mock, open_mock, os_mock, load_mock):
        '''
        Unit test for method : attribute_init.config_inventory_pattern
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing Inventory Pattern Configuration Module Used by Attribute Initialiser")

        load_mock.return_value = dict()
        config_mock.return_value = CONFIGURATION_DICT

        self.assertIsNone(config_inventory_pattern())

class TestAttribInitSanity(unittest.TestCase):
    '''
    Unit test class for Attribute Initaliser to cover sanity tests
    '''

    MX2010_CHASSIS_INFO_XML = '''
        <chassis-inventory>
            <chassis>
                <name>Chassis</name>
                <serial-number>JN1259A3FAFK</serial-number>
                <description>MX2010</description>
                <chassis-module>
                    <name>Midplane</name>
                    <version>REV 47</version>
                    <part-number>750-044636</part-number>
                    <serial-number>ABAD1621</serial-number>
                    <description>Lower Backplane</description>
                    <clei-code>IPMU810ARB</clei-code>
                    <model-number>CHAS-BP-MX2010-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PMP</name>
                    <version>REV 01</version>
                    <part-number>711-051406</part-number>
                    <serial-number>ACVD0488</serial-number>
                    <description>Power Midplane</description>
                    <model-number></model-number>
                </chassis-module>
                <chassis-module>
                    <name>FPM Board</name>
                    <version>REV 09</version>
                    <part-number>760-044634</part-number>
                    <serial-number>ABDG8729</serial-number>
                    <description>Front Panel Display</description>
                    <clei-code>IPMYA4EJRA</clei-code>
                    <model-number>MX2010-CRAFT-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PSM 0</name>
                    <version>REV 01</version>
                    <part-number>740-050037</part-number>
                    <serial-number>1EDB32000J3</serial-number>
                    <description>DC 52V Power Supply Module</description>
                    <clei-code>IPUPAKRKAA</clei-code>
                    <model-number>MX2000-PSM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>PDM 0</name>
                    <version>REV 03</version>
                    <part-number>740-045234</part-number>
                    <serial-number>1EFA3230533</serial-number>
                    <description>DC Power Dist Module</description>
                    <clei-code>IPUPAJSKAA</clei-code>
                    <model-number>MX2000-PDM-DC-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>Routing Engine 0</name>
                    <version>REV 12</version>
                    <part-number>750-055814</part-number>
                    <serial-number>CALL6691</serial-number>
                    <description>RE-S-2X00x8</description>
                    <model-number></model-number>
                </chassis-module>
                <chassis-module>
                    <name>CB 0</name>
                    <version>REV 17</version>
                    <part-number>750-055087</part-number>
                    <serial-number>CALP9482</serial-number>
                    <description>MX2K Enhanced SCB</description>
                    <clei-code>COUCAU8BAA</clei-code>
                    <model-number>REMX2K-X8-64G-S</model-number>
                </chassis-module>
                <chassis-module>
                    <name>SPMB 0</name>
                    <version>REV 05</version>
                    <part-number>711-041855</part-number>
                    <serial-number>CALP9352</serial-number>
                    <description>PMB Board</description>
                </chassis-module>
                <chassis-module>
                    <name>SFB 0</name>
                    <version>REV 13</version>
                    <part-number>750-069467</part-number>
                    <serial-number>CALX2849</serial-number>
                    <description>Switch Fabric Board 3</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                </chassis-module>
                <chassis-module>
                    <name>FPC 1</name>
                    <version>REV 82</version>
                    <part-number>750-044130</part-number>
                    <serial-number>ABDM9803</serial-number>
                    <description>MPC6E 3D</description>
                    <clei-code>IP9IATZDAE</clei-code>
                    <model-number>MX2K-MPC6E</model-number>
                    <chassis-sub-module>
                        <name>CPU</name>
                        <version>REV 12</version>
                        <part-number>711-045719</part-number>
                        <serial-number>ABDN4040</serial-number>
                        <description>RMPC PMB</description>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>MIC 1</name>
                        <version>REV 35</version>
                        <part-number>750-046532</part-number>
                        <serial-number>CAMC3598</serial-number>
                        <description>24X10GE SFPP</description>
                        <clei-code>IP9IATVDAA</clei-code>
                        <model-number>MIC6-10G</model-number>
                        <chassis-sub-sub-module>
                            <name>PIC 1</name>
                            <part-number>BUILTIN</part-number>
                            <serial-number>BUILTIN</serial-number>
                            <description>24X10GE SFPP</description>
                            <chassis-sub-sub-sub-module>
                                <name>Xcvr 0</name>
                                <version>REV 01</version>
                                <part-number>740-021309</part-number>
                                <serial-number>A9401FL</serial-number>
                                <description>SFP+-10G-LR</description>
                            </chassis-sub-sub-sub-module>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>XLM 0</name>
                        <version>REV 14</version>
                        <part-number>711-046638</part-number>
                        <serial-number>ABDL6698</serial-number>
                        <description>MPC6E XL</description>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>XLM 1</name>
                        <version>REV 14</version>
                        <part-number>711-046638</part-number>
                        <serial-number>ABDK6518</serial-number>
                        <description>MPC6E XL</description>
                    </chassis-sub-module>
                </chassis-module>
                <chassis-module>
                    <name>FPC 2</name>
                    <version>REV 39</version>
                    <part-number>750-063414</part-number>
                    <serial-number>CAMF5918</serial-number>
                    <description>MPC9E 3D</description>
                    <clei-code>IPUCBN5CAE</clei-code>
                    <model-number>MX2K-MPC9E</model-number>
                    <chassis-sub-module>
                        <name>CPU</name>
                        <version>REV 21</version>
                        <part-number>750-057177</part-number>
                        <serial-number>CALY2917</serial-number>
                        <description>SMPC PMB</description>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>MIC 0</name>
                        <version>REV 14</version>
                        <part-number>750-055992</part-number>
                        <serial-number>CALV1654</serial-number>
                        <description>MRATE-12xQSFPP-XGE-XLGE-CGE</description>
                        <clei-code>IPUIBY5MAA</clei-code>
                        <model-number>MIC-MRATE</model-number>
                        <chassis-sub-sub-module>
                            <name>PIC 0</name>
                            <part-number>BUILTIN</part-number>
                            <serial-number>BUILTIN</serial-number>
                            <description>MRATE-12xQSFPP-XGE-XLGE-CGE</description>
                            <chassis-sub-sub-sub-module>
                                <name>Xcvr 8</name>
                                <version>REV 01</version>
                                <part-number>740-061405</part-number>
                                <serial-number>1ECQ13110CJ</serial-number>
                                <description>QSFP-100G-SR4-T2</description>
                            </chassis-sub-sub-sub-module>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>MIC 1</name>
                        <version>REV 14</version>
                        <part-number>750-055992</part-number>
                        <serial-number>CALV1474</serial-number>
                        <description>MRATE-12xQSFPP-XGE-XLGE-CGE</description>
                        <clei-code>IPUIBY5MAA</clei-code>
                        <model-number>MIC-MRATE</model-number>
                        <chassis-sub-sub-module>
                            <name>PIC 1</name>
                            <part-number>BUILTIN</part-number>
                            <serial-number>BUILTIN</serial-number>
                            <description>MRATE-12xQSFPP-XGE-XLGE-CGE</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                </chassis-module>
                <chassis-module>
                    <name>FPC 3</name>
                    <version>REV 29</version>
                    <part-number>750-054576</part-number>
                    <serial-number>CAEL7916</serial-number>
                    <description>MPC8E 3D</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                    <chassis-sub-module>
                        <name>CPU</name>
                    </chassis-sub-module>
                </chassis-module>
                <chassis-module>
                    <name>FPC 8</name>
                    <version>REV 18</version>
                    <part-number>750-086583</part-number>
                    <serial-number>CAMA1800</serial-number>
                    <description>MPC11E 3D</description>
                    <clei-code>PROTOXCLEI</clei-code>
                    <model-number>PROTO-ASSEMBLY</model-number>
                    <chassis-sub-module>
                        <name>CPU</name>
                        <version>REV 19</version>
                        <part-number>750-072571</part-number>
                        <serial-number>CALX6740</serial-number>
                        <description>FMPC PMB</description>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>PIC 0</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>MRATE-5xQSFPP</description>
                        <chassis-sub-sub-module>
                            <name>Xcvr 0</name>
                            <version>1A</version>
                            <part-number>740-061408</part-number>
                            <serial-number>1FCQ52310FM</serial-number>
                            <description>QSFP-100G-CWDM4</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                    <chassis-sub-module>
                        <name>PIC 1</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>MRATE-5xQSFPP</description>
                        <chassis-sub-sub-module>
                            <name>Xcvr 1</name>
                            <version>01</version>
                            <part-number>740-061405</part-number>
                            <serial-number>1ECQ14010V0</serial-number>
                            <description>QSFP-100GBASE-SR4</description>
                        </chassis-sub-sub-module>
                    </chassis-sub-module>
                </chassis-module>
                <chassis-module>
                    <name>Fan Tray 0</name>
                    <version>REV 06</version>
                    <part-number>760-046960</part-number>
                    <serial-number>ACAY0827</serial-number>
                    <clei-code>IPU</clei-code>
                    <model-number>X2000-FANTRAY-S</model-number>
                </chassis-module>
            </chassis>
        </chassis-inventory>
    '''

    def test_parse_device_inventory(self):
        '''
        Unit test for method : attribute_init.parse_device_inventory
        '''

        print("Testing XML Parser Module Used by Attribute Initialiser")

        parser = etree.XMLParser(remove_blank_text=True)
        chassis_info_xml_format = etree.XML(self.MX2010_CHASSIS_INFO_XML, parser)

        self.assertIsInstance(parse_device_inventory(chassis_info_xml_format), dict)

    @patch('jnpr.toby.init.attrib_init.attribute_init.load')
    @patch('jnpr.toby.init.attrib_init.attribute_init.os')
    @patch('jnpr.toby.init.attrib_init.attribute_init.open')

    def test_read_inventory_file(self, open_mock, os_mock, load_mock):
        '''
        Unit test for method : attribute_init.read_inventory_file
        '''

        print("Testing Inventory File Read Module Used by Attribute Initialiser")

        load_mock.return_value = {'attribute-inventory-path': '/volume/regressions/toby/test-suites/MTS/attribute_vars'}
        self.assertIsInstance(read_inventory_file('fpc'), dict)

class TestAttribInitBasic(unittest.TestCase):
    '''
    Unit test class for Attribute Initialiser to cover basic tests
    '''

    def test_log(self):
        '''
        Unit test for method : attribute_init.log
        '''

        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        print("Testing Log Module Used by Attribute Initialiser")

        self.assertIsNone(log())
        self.assertIsNone(log("Log Message"))
        self.assertIsNone(log("Log Level", "Log Message"))
        self.assertIsNone(log(level='Log Level', message='Log Message'))
        self.assertIsNone(log(message='Log Message'))
        self.assertIsNone(log(level='Log Message'))

    def test_print_help(self):
        '''
        Unit test for method : attribute_init.print_help
        '''

        print("Testing Command-line Help Module Used by Attribute Initialiser")

        self.assertIsNone(print_help())

if __name__ == '__main__':
    unittest.main()

