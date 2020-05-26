"""Module contains the turbo class for Linux traffic generator methods"""
# pylint: disable=undefined-variable
__author__ = ['Sumanth Inabathini', 'Sasikumar Sekar']
__contact__ = ['isumanth@juniper.net', 'sasik@juniper.net']
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2020'

import requests

class turbo(object):
    """
    Class for generating traffic using Linux devices

    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, **kwargs):
        self.port_pair = None
        self.resource = {}
        self.client_names = []
        self.server_names = []
        self.chassis = {}
        self.chassis['client'] = {}
        self.chassis['server'] = {}

    def init(self, port_pair=None):
        """Constructor method to update the instance of ligen class."""
        if port_pair is None:
            print("port_pair is empty")
        print(port_pair)
        self.client_ports = port_pair['client_ports']
        self.server_ports = port_pair['server_ports']
        self.client_list = self.client_ports.keys()
        self.server_list = self.server_ports.keys()

        for client in self.client_list:
            res = t.get_resource(client)
            res_name = res['system']['primary']['name']
            self.client_names.append(res['system']['primary']['name'])
            self.chassis['client'][res_name] = {}
            self.chassis['client'][res_name]['port_list'] = []
            self.chassis['client'][res_name]['ip_list'] = []
            self.chassis['client'][res_name]['gw_list'] = []

            for link in self.client_ports[client]:
                self.chassis['client'][res_name]['port_list'].append(res['interfaces'][link]['pic'])
                self.chassis['client'][res_name]['ip_list'].append(res["interfaces"][link]
                                                                   ['uv-port-ipv4'])
                self.chassis['client'][res_name]['gw_list'].append(res['interfaces'][link]
                                                                   ['uv-gw-ipv4'])

        for server in self.server_list:
            res = t.get_resource(server)
            res_name = res['system']['primary']['name']
            self.server_names.append(res['system']['primary']['name'])
            self.chassis['server'][res_name] = {}
            self.chassis['server'][res_name]['port_list'] = []
            self.chassis['server'][res_name]['ip_list'] = []
            self.chassis['server'][res_name]['gw_list'] = []

            for link in self.server_ports[server]:
                self.chassis['server'][res_name]['port_list'].append(res['interfaces'][link]['pic'])
                self.chassis['server'][res_name]['ip_list'].append(res['interfaces'][link]
                                                                   ['uv-port-ipv4'])
                self.chassis['server'][res_name]['gw_list'].append(res['interfaces'][link]
                                                                   ['uv-gw-ipv4'])

        print(self.chassis)

        return True


    def configure_chassis(self):
        """
        Configure Chassis

        """
        print(self.chassis['client'])
        print(self.chassis['server'])

        for i in self.chassis['client'].keys():
            json_body = {'role': 'client', 'is_ns_enabled': 'true'}
            response = requests.get('http://'+i+'.englab.juniper.net:8181/config/chassis',
                                    json=json_body, timeout=10).json()
            #print(response['result'])
            #print(self.chassis['client'][i]['port_list'])
            #print(response['port_list'])
            if response["result"]:
                for port in self.chassis['client'][i]['port_list']:
                    if port in response['port_list']:
                        print("Json Request Passed for client " + i)
                    else:
                        print("connected port not available in port_list sent by client " + i)
            else:
                print("Json Request Failed for client " + i)

        for i in self.chassis['server'].keys():
            json_body = {'role': 'server', 'is_ns_enabled': 'true'}
            response = requests.get('http://'+i+'.englab.juniper.net:8181/config/chassis',
                                    json=json_body, timeout=10).json()
            #print(response['result'])
            #print(self.chassis['server'][i]['port_list'])
            #print(response['port_list'])
            if response["result"]:
                for port in self.chassis['server'][i]['port_list']:
                    if port in response['port_list']:
                        print("Json Request Passed for server " + i)
                    else:
                        print("connected port not available in port_list sent by server " + i)
            else:
                print("Json Request Failed for server " + i)

        return True

    def configure_networks(self):
        """
        Configure networks

        """
        for (i, j) in zip(self.chassis['client'].keys(), self.chassis['server'].keys()):
            #print(i,j)
            json_body = {"client_port_list":self.chassis['client'][i]['port_list'],
                         "client_ip_list":self.chassis['client'][i]['ip_list'],
                         "client_gw_list":self.chassis['client'][i]['gw_list'],
                         "server_port_list":self.chassis['server'][j]['port_list'],
                         "server_ip_list":self.chassis['server'][j]['ip_list'],
                         "server_gw_list":self.chassis['server'][j]['gw_list'], "num_ip":25}
            response = requests.get('http://'+i+'.englab.juniper.net:8181/config/networks/',
                                    json=json_body, timeout=10).json()
            if response["result"]:
                print("Configured networks successfully on client " + i)
            else:
                print("Configured networks failed on client " + i)
        for (i, j) in zip(self.chassis['client'].keys(), self.chassis['server'].keys()):
            json_body = {"client_port_list":self.chassis['client'][i]['port_list'],
                         "client_ip_list":self.chassis['client'][i]['ip_list'],
                         "client_gw_list":self.chassis['client'][i]['gw_list'],
                         "server_port_list":self.chassis['server'][j]['port_list'],
                         "server_ip_list":self.chassis['server'][j]['ip_list'],
                         "server_gw_list":self.chassis['server'][j]['gw_list'], "num_ip":25}
            response = requests.get('http://'+j+'.englab.juniper.net:8181/config/networks/',
                                    json=json_body, timeout=10).json()
            if response["result"]:
                print("Configured networks successfully on server " + j)
            else:
                print("Configured networks failed on server " + j)

        return True

    def configure_traffic_profiles(self, **kwargs):
        """
        Configure traffic profiles

        """

        for (i, j) in zip(self.chassis['client'].keys(), self.chassis['server'].keys()):
            #print(i,j)
            json_body = {"protocol":kwargs['protocol'], "direction":kwargs['direction'],
                         "page_size":int(kwargs['page_size']), "dst_port":int(kwargs['dst_port']),
                         "num_ports":int(kwargs['num_ports']), "num_ip":int(kwargs['num_ip']),
                         "duration":kwargs['duration'], "num_sess":int(kwargs['num_sess'])}
            print(json_body)
            response = requests.get('http://'+i+'.englab.juniper.net:8181/config/traffic/',
                                    json=json_body, timeout=10).json()
            if response["result"]:
                print("Configured traffic profile successfully on client " + i)
            else:
                print("Configured traffic profile failed on client " + i)

        for (i, j) in zip(self.chassis['server'].keys(), self.chassis['server'].keys()):
            #print(i,j)
            json_body = {"protocol":kwargs['protocol'], "direction":kwargs['direction'],
                         "page_size":int(kwargs['page_size']), "dst_port":int(kwargs['dst_port']),
                         "num_ports":int(kwargs['num_ports']), "num_ip":int(kwargs['num_ip']),
                         "duration":kwargs['duration'], "num_sess":int(kwargs['num_sess'])}
            print(json_body)
            response = requests.get('http://'+j+'.englab.juniper.net:8181/config/traffic/',
                                    json=json_body, timeout=10).json()
            if response["result"]:
                print("Configured traffic profile successfully on server " + j)
            else:
                print("Configured traffic profile failed on server " + j)

        return True

    def start_traffic(self):
        """
        Start the traffic

        """

        for (i, j) in zip(self.chassis['server'].keys(), self.chassis['server'].keys()):
            response = requests.get('http://'+j+'.englab.juniper.net:8181/traffic/start',timeout=10).json()
            print(response)
            if response["result"]:
                print("Traffic started successfully on server " + j)
            else:
                print("Traffic start failed failed on server " + j)

        for (i, j) in zip(self.chassis['client'].keys(), self.chassis['server'].keys()):
            response = requests.get('http://'+i+'.englab.juniper.net:8181/traffic/start', timeout=10).json()

            print(response)
            if response["result"]:
                print("Traffic started successfully on client " + i)
            else:
                print("Traffic start failed on client " + i)
        return True

    def stop_traffic(self):
        """
        Stop the traffic

        """
        for (i, j) in zip(self.chassis['client'].keys(), self.chassis['server'].keys()):
            response = requests.get('http://'+i+'.englab.juniper.net:8181/traffic/stop', timeout=10).json()

            print(response)
            if response["result"]:
                print("Traffic stopped successfully on client " + i)
            else:
                print("Traffic stop failed on client " + i)

        for (i, j) in zip(self.chassis['server'].keys(), self.chassis['server'].keys()):
            response = requests.get('http://'+j+'.englab.juniper.net:8181/traffic/stop', timeout=10).json()
            print(response)
            if response["result"]:
                print("Traffic stopped successfully on server " + j)
            else:
                print("Traffic stop failed failed on server " + j)
        return True

    def get_summary_stats(self):
        """
        Get the summary statistics

        """

        for i in self.chassis['client'].keys():
            response = requests.get('http://'+i+'.englab.juniper.net:8181/stats/summary', timeout=10).json()

            print(response)
            if response["result"]:
                print("Traffic stopped successfully on client " + i)
            else:
                print("Traffic stop failed on client " + i)
        return True