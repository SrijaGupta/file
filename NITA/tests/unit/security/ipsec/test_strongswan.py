"""Unit test file for strongswan"""
import sys
import unittest2 as unittest

from unittest.mock import MagicMock, patch, PropertyMock
#from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.unix.unix import *
from jnpr.toby.utils.linux.openssl import *
from jnpr.toby.security.ipsec.strongswan import *
import os


if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

# To return response of shell() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class TestStrongswan(unittest.TestCase):
    linux_handle = MagicMock(spec=Unix)
    sobj = MagicMock(spec=Strongswan)
    sobj.linux_handle = MagicMock(spec=Unix)
    sobj.linux_handle.log = MagicMock()
    
    def test_create_strongswan_object(self):
        lst = [Response("/etc")]
        self.linux_handle.shell = MagicMock(side_effect=lst)
        self.linux_handle.log = MagicMock(return_value=True)
        self.linux_handle.su = MagicMock(return_value=True)
        # self.linux_handle.shell = MagicMock(return_value=response_object)
        x = create_strongswan_object(self.linux_handle, connection_name='net-t')
        self.assertEqual(isinstance(x, Strongswan), True)

        #negative case
        try:
            x = create_strongswan_object(self.linux_handle)
        except Exception as err:
            self.assertEqual(err.args[0], "Mandatory argument 'connection_name' missing")

    #@patch('jnpr.toby.security.ipsec.strongswan._create_dict_from_file')
    def test_create_ipsec_conf(self):
        #self.linux_handle = MagicMock(spec=Unix)
        lst = [Response("/etc/ipsec.conf"), Response(True)]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        self.sobj.linux_handle.upload = MagicMock(return_value=True)
        self.sobj.conn_name = 'net-t'
        self.sobj.conf_dir = '/etc'
        open = MagicMock(return_value=True)
        write = MagicMock(return_value=True)
        user_dict = {'leftsubnet': '10.1.0.0/16',
                     'leftcert': 'moonCert.pem',
                     'leftid': '@moon.strongswan.org',
                     'right': '%any',
                     'auto': 'add'
                     }
        self.assertTrue(Strongswan.create_ipsec_conf(self.sobj, ipsec_conf_dict=user_dict))
        #if append=1
        lst = [Response("/etc/ipsec.conf"), Response("success"), Response("success")]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        file_dict = {'conn net-net': {'rightsubnet': '80.0.0.0/16', 'leftid': '11.0.1.2', 'leftsubnet': '30.0.0.0/16', 'right': '11.0.1.1', 'rightid':      '11.0.1.1', 'left': '11.0.1.2', 'auto': 'start'}, 'config setup': {'cachecrls': 'yes', 'strictcrlpolicy': 'yes'}, 'conn mytest':                      {'leftcert': 'moonCert.pem', 'leftid': '@moon.strongswan.org', 'leftsubnet': '10.1.0.0/16', 'right': '%any', 'auto': 'add'}, 'con                      n %default': {'keyingtries': '1', 'esp': 'aes128-sha256!', 'rekeymargin': '3m', 'keyexchange': 'ikev1', 'keylife': '20m', 'authb                      y': 'secret', 'ikelifetime': '60m', 'ike': 'aes128-sha256-modp1024!'}}
        self._create_dict_from_file =  MagicMock(return_value=file_dict)
        #import pdb
        #pdb.set_trace()
        self.assertTrue(Strongswan.create_ipsec_conf(self.sobj, ipsec_conf_dict=user_dict, append=1))
        # negative case
        try:
            x =Strongswan.create_ipsec_conf(self.sobj)
        except Exception as err:
            self.assertEqual(err.args[0], "ipsec_dict is a mandatory argument")
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        self.sobj.linux_handle.upload = MagicMock(return_value=True)
        self.assertTrue(Strongswan.create_ipsec_conf(self.sobj, ipsec_conf_dict=user_dict, append=1))
        # upload error
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        self.sobj.linux_handle.upload = MagicMock(return_value=True)
        self.sobj.linux_handle.upload = MagicMock(return_value=False)
        try:
            x =Strongswan.create_ipsec_conf(self.sobj,ipsec_conf_dict=user_dict, append=1)
        except Exception as err:
            self.assertEqual(err.args[0], "Uploading ipsec.conf file failed")

    @patch('time.sleep')    
    def test_ipsec_up(self, mock_sleep):
        mock_sleep.return_value = True
        lst = [Response("success"), Response("success"), Response("connection  successfully")]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        self.assertTrue(Strongswan.ipsec_up(self.sobj)) 
        #restart=1
        lst = [Response("success"), Response("success"), Response("connection  successfully"), Response("connection  successfully")]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        self.assertTrue(Strongswan.ipsec_up(self.sobj, restart=1))
        #import pdb
        #pdb.set_trace()
        lst = [Response("No such file or directory"), Response("success"), Response("connection  successfully"), Response("connection  successfully")]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        self.assertTrue(Strongswan.ipsec_up(self.sobj))
        #import pdb
        #pdb.set_trace()
        lst = [Response("No such file or directory"), Response("unable to start"), Response("success"), Response("success")]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        try:
           Strongswan.ipsec_up(self.sobj)
        except Exception as err:
           self.assertEqual(err.args[0], "ipsec start failed: unable to start")

    def test_ipsec_down(self):
        lst = [Response("successfully")]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        self.assertTrue(Strongswan.ipsec_down(self.sobj))
        #negative case
        lst = [Response("error")]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        try:
           Strongswan.ipsec_down(self.sobj)
        except Exception as err:
           self.assertEqual(err.args[0], "ipsec stop failed: error")

    def test_ipsec_status_check(self):
        lst = [Response("INSTALLED")]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        self.assertTrue(Strongswan.ipsec_status_check(self.sobj))
        try:
           lst = [Response("not up")]
           self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
           self.assertTrue(Strongswan.ipsec_status_check(self.sobj))
        except Exception as err:
           self.assertEqual(err.args[0], "connection not up: not up")

    def test_add_ipsec_secrets(self):
        lst = [Response("/etc/ipsec.secrets"), Response(True)]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        self.sobj.linux_handle.upload = MagicMock(return_value=True)
        self.sobj.conf_dir = '/etc'
        self.assertTrue(Strongswan.add_ipsec_secrets(self.sobj, auth_type='PSK',
                        preshared_key='ike123', host_id='11.0.1.1', peer_id='11.0.1.2', xauth_user='user', xauth_pwd='password'))

        lst = [Response("/etc/ipsec.secrets"), Response(True)]
        self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
        self.assertTrue(Strongswan.add_ipsec_secrets(self.sobj, auth_type='RSA',local_cert='test'))
        try:
            x =Strongswan.add_ipsec_secrets(self.sobj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mandatory Argument 'auth_type' is missing")

        try:
            lst = [Response("/etc/ipsec.secrets"), Response(True)]
            self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
            x =Strongswan.add_ipsec_secrets(self.sobj, auth_type='PSK')
        except Exception as err:
            self.assertEqual(err.args[0], "Missing argument: For auth_type=psk, argument 'preshared_key' is mandatory")

        try:
            lst = [Response("/etc/ipsec.secrets"), Response(True)]
            self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
            x =Strongswan.add_ipsec_secrets(self.sobj, auth_type='RSA')
        except Exception as err:
            self.assertEqual(err.args[0], "'local_cert' is mandatory argument")

        try:
            lst = [Response("/etc/ipsec.secrets"), Response(True)]
            self.sobj.linux_handle.shell = MagicMock(side_effect=lst)
            self.sobj.linux_handle.upload = MagicMock(return_value=False)
            x =Strongswan.add_ipsec_secrets(self.sobj, auth_type='RSA',local_cert='test')
        except Exception as err:
            self.assertEqual(err.args[0], "Uploading ipsec.secrets file failed")

    def test_generate_ipsec_conf(self):
        self.assertTrue(generate_ipsec_conf(self.sobj))

    def test_wrapper_ipsec_up(self):
        self.assertTrue(ipsec_up(self.sobj))

    def test_wrapper_ipsec_down(self):
        self.assertTrue(ipsec_down(self.sobj))

    def test_wrapper_ipsec_status(self):
        self.assertTrue(ipsec_status(self.sobj))
