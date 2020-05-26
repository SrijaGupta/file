""" This module defines the valid8 class and class methods.
"""
from jnpr.toby.bbe.version import get_bbe_version
import http.client
from robot.api import logger

__author__ = ['Sai Nagarjun Ankala']
__contact__ = 'sankala@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'
__version__ = get_bbe_version()

class Valid8:
    """ This class will start valid8, stop valid8 and trigger ASR's from valid8.
    The constructor requires the Toby-generated device handle, the hostname of valid8
    server, username and password as its arguements.
    """
    def __init__(self, dev_handle):
        self.device_handle = dev_handle
        self.host = dev_handle.current_node.current_controller.host
        self.user = 'user'
        self.password = 'user'

    def start_valid8_server(self, server_name=None, ip_version=None,\
                            config=None, pcrf=None, nasreq=None, ocs=None):
        """ Starts valid8 server components(nasreq, ocs,pcrf) on valid8 server

        :param server_name:
            **REQUIRED** valid8 server name. Examples:- wf-valid8-01, wf-valid8, hcl-valid8
        :param ip_version:
            **REQUIRED** mentioned IP version file
        :param config:
            **REQUIRED** mentioned config file
        :param pcrf:
            **optional** mention pcrf file
        :param nasreq:
            **optional** mention nasreq file
        :param ocs:
            **optional** mention ocs file
        :return:
            True if the valid8 components have been started
            Throws error if server_name, ip_version, config are not passed as arguements
        """

        if server_name is None:
            logger.console("It needs a valid8 server name as an argument")
            t.log('ERROR', "Expecting valid8 server name but found None")
            raise Exception("Server information is not given")

        if ip_version is None:
            logger.console("It needs an ip version file as an argument")
            t.log('ERROR', "Expecting ip version file but found none")
            raise Exception("IP version file information is not given")

        if config is None:
            logger.console("It needs a config name as an argument")
            t.log('ERROR', "Expecting config file but found none")
            raise Exception("Config file information is not given")

        t.log('info', 'Starting valid8 components')

        conn = http.client.HTTPConnection(server_name)
        payload = "{\"traceFlags\":64,\"development\":true,\"environment\":\"" + ip_version + "\"}"
        #encode = base64.b64encode(self.user + ':' + self.password)
        headers = {'content-type': "application/json", 'Accept': "application/json",\
                   'Authorization': "Basic"}
        conn.request("PUT", "/api/1/application/Diameter/Load%20Tester/" + config, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

        if pcrf is None:
            payload = "{\"group\":\"pcrf\",\"programs\":[{\"name\":\"PR_pcrf_basicCall_S_V_2_0_0\",\"percent\":100}]}"
            conn.request("PUT", "/api/1/control/trafficTerminatorPcrf/programs", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
        else:
            payload = "{\"group\":\"pcrf\",\"programs\":[{\"name\":\""+ pcrf + "\",\"percent\":100}]}"
            conn.request("PUT", "/api/1/control/trafficTerminatorPcrf/programs", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))

        if ocs is None:
            payload = "{\"group\":\"ocs\",\"programs\":[{\"name\":\"PR_ocs_basicCall_S_V_1_0_0629\",\"percent\":100}]}"
            conn.request("PUT", "/api/1/control/trafficTerminatorocf/programs", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
        else:
            payload = "{\"group\":\"ocs\",\"programs\":[{\"name\":\"" + ocs + "\",\"percent\":100}]}"
            conn.request("PUT", "/api/1/control/trafficTerminatorocf/programs", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))

        if nasreq is None:
            payload = "{\"group\":\"nasreq\",\"programs\"\
			:[{\"name\":\"PR_nasreq_basicCall_S_V_0_0_0\",\"percent\":100}]}"
            conn.request("PUT", "/api/1/control/trafficTerminatorNasreq/programs", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
        else:
            payload = "{\"group\":\"nasreq\",\"programs\":[{\"name\":\"" + nasreq + "\",\"percent\":100}]}"
            conn.request("PUT", "/api/1/control/trafficTerminatorNasreq/programs", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))

        return True

    def stop_valid8_server(self, server_name=None):
        """ Unloads valid8 application software.

        :return:
            True if valid8 server unloads appliation software
            Throws error if server_name not passed as arguement
        """

        if server_name is None:
            logger.console("It needs a valid8 server name as an argument")
            t.log('ERROR', "Expecting valid8 server name but found None")
            raise Exception("Server information is not given")

        conn = http.client.HTTPConnection(server_name)
        payload = "{}"
        headers = {'content-type': "application/json"}
        conn.request("DELETE", "/api/1/application", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        return True

    def send_asr(self, server_name=None):
        """ Sends ASR from valid8 to dut to logout clients

        :return:
            True if valid8 server sends ASR's to dut
            Throws error if server_name not passed as arguement
        """

        if server_name is None:
            logger.console("It needs a valid8 server name as an argument")
            t.log('ERROR', "Expecting valid8 server name but found None")
            raise Exception("Server information is not given")

        conn = http.client.HTTPConnection(server_name)
        payload = "{\"sid\":\"all\"}"
        headers = {'content-type': "application/json"}
        conn.request("PUT", "/api/1/control/trafficTerminatorNasreq/sendASR", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        return True
