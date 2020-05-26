#!/usr/local/sbin/python3
'''
    External listener for Keywords Telemetry
'''

import json
import socket
import os, re
import ssl
import pwd
from websocket import create_connection

ROBOT_LISTENER_API_VERSION = 2

class KWTelemetry(object):
    '''
        External listener for Keyword Telemetry. The listener implemented start_suite, start_test,
         end_suite, end_test and start/end keyword methods and are invoked by Robot when the
         event happens. The context data is posted to remote server for analytics.
         The keywords from BuiltIn library are skipped. This listener script is consumed by
         robot by passing as argument '--listener KWTelemetry.py' to robot executable.
    '''
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.data = {}
        self._rhost = "10.224.34.247"
        self._user = pwd.getpwuid(os.getuid())[0]
        self._hostname = socket.gethostname()
        self._pid = os.getpid()
        try:
            HOST_UP  = True if os.system("ping -c 1 -w 1 " + self._rhost + " &>/dev/null") is 0 else False   # if down 1sec else 200ms
            if HOST_UP:
                self._ws = create_connection("ws://10.224.34.247:8001/websocket", sslopt={"check_hostname": False, "cert_reqs": ssl.CERT_NONE})
                self._ws.settimeout(1)
        except Exception as exp:
            pass
    def _post(self, data):
        """
            posts the data to remote server.
              TODO: This method currently writing to file on local machine, this will be modified
               to post to remote server when the server end is ready in subsequent versions.

            :param d:
                **REQUIRED** The dictionary data to post to remote server

            :return:
                True in case posted successfully, False otherwise
        """
        data.update({'username': self._user, 'hostname': self._hostname, 'pid': self._pid})
        try:
            if hasattr(self, '_ws'):
                if not self._ws.connected:
                    HOST_UP  = True if os.system("ping -c 1 -w 1 " + self._rhost + " &>/dev/null") is 0 else False   # if down 1sec else 200ms
                    if HOST_UP:
                        self._ws = create_connection("ws://10.224.34.247:8001/websocket", sslopt={"check_hostname": False, "cert_reqs": ssl.CERT_NONE})
                        self._ws.settimeout(1)
                self._ws.send(json.dumps(data))
                return True
        except Exception as exp:
            return False
        return False

    def start_suite(self, name, attrs):
        """
            This listener method is called when test suite starts

            :param name:
                **REQUIRED** The shortname of test suite
            :param attrs:
                **REQUIRED** The attribute dictionary containing id, source, longname, starttime,
                  total tests.
            :return:
                None
        """
        data = {'id': attrs['id'],
                'name': name,
                'source': attrs['source'],
                'longname': attrs['longname'],
                'starttime': attrs['starttime'],
                'tests': ';'.join(attrs['tests']),
                'totaltests': attrs['totaltests']
               }
        self._post(data)

    def end_suite(self, name, attrs):
        """
            This listener method is called when test suite ends

            :param name:
                **REQUIRED** The shortname of test suite
            :param attrs:
                **REQUIRED** The attribute dictionary containing id, source, longname,
                  starttime, total tests, endtime, elapsedtime and status.
            :return:
                None
        """
        data = {'id': attrs['id'],
                'name': name,
                'source': attrs['source'],
                'longname': attrs['longname'],
                'starttime': attrs['starttime'],
                'endtime': attrs['endtime'],
                'elapsedtime': attrs['elapsedtime'],
                'status': attrs['status'],
                'message': attrs['message'],
                'statistics': attrs['statistics']
               }
        self._post(data)


    def start_test(self, name, attrs):
        """
            This listener method is called when test starts and posts the data to remote server

            :param name:
                **REQUIRED** The shortname of test suite
            :param attrs:
                **REQUIRED** The attribute dictionary containing id, longname, starttime,
            :return:
                None
        """
        data = {'id' : attrs['id'],
                'testName' : name,
                'longname': attrs['longname'],
                'starttime' : attrs['starttime']
               }
        self._post(data)

    def end_test(self, name, attrs):
        """
            This listener method is called when test ends and posts the data to server

            :param name:
                **REQUIRED** The shortname of test suite
            :param attrs:
                **REQUIRED** The attribute dictionary containing id, source, longname,
                   starttime, total tests, endtime, elapsedtime and status.
            :return:
                None
        """
        data = {'id': attrs['id'],
                'testName': name,
                'longname': attrs['longname'],
                'starttime': attrs['starttime'],
                'endtime': attrs['endtime'],
                'elapsedtime' : attrs['elapsedtime'],
                'status': attrs['status'],
                'message': attrs['message']
               }
        self._post(data)

    def start_keyword(self, name, attrs):
        """
            This listener method is called when keyword starts. BuiltIn keywords are ignored.

            :param name:
                **REQUIRED** The shortname of test suite
            :param attrs:
                **REQUIRED** The attribute dictionary containing type, skwname, libname & starttime
            :return:
                None
        """
        if re.match(r'\bkeyword\b', attrs['type'].lower()):
            if re.match(r'\bbuiltin\b', attrs['libname'].lower()):
                return

            data = {'name': name,
                    'type' : attrs['type'],
                    'kwname': attrs['kwname'],
                    'args': attrs['args'],
                    'libname': attrs['libname'],
                    'starttime': attrs['starttime']
                   }
            self._post(data)

    def end_keyword(self, name, attrs):
        """
            This listener method is called when keyword ends

            :param name:
                **REQUIRED** The shortname of test suite
            :param attrs:
                **REQUIRED** The attribute dictionary containing type, kwname, librname,
                 starttime, endtime, elapsedtime and status.
            :return:
                None
        """
        if re.match(r'\bkeyword\b', attrs['type'].lower()):
            if re.match(r'\bbuiltin\b', attrs['libname'].lower()):
                return
            data = {'name': name,
                    'type': attrs['type'],
                    'kwname': attrs['kwname'],
                    'args': attrs['args'],
                    'libname': attrs['libname'],
                    'starttime': attrs['starttime'],
                    'endtime': attrs['endtime'],
                    'elapsedtime': attrs['elapsedtime'],
                    'status': attrs['status']
                   }
            self._post(data)
    def __del__(self):
        try:
            self._ws.close()
        except Exception as exp:
            pass
 

