"""
Unit test cases for Csflow.py
author: dzhu 
"""
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import builtins
from jnpr.toby.utils import Cmtp
import subprocess 

@attr('unit')
class TestSystem(unittest.TestCase):

    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        builtins.tv=MagicMock()

    def test_sflow_agent_dict_filtered_v4(self):
        output = subprocess.Popen(['cat', 'sflowtf'], stdout=subprocess.PIPE).communicate()[0]
        response = str(output, 'utf-8')
        #print(response)
        result = Cmtp.sflow_agent_dict_filtered(sfile=response, agent_id='1.1.1.1', sip_pat='51.1.1.*', dip_pat='52.1.1.*', ver='4', num=2)
        #Cmtp.rfprint(result, 1)

    def test_sflow_agent_dict_filtered_v6(self):
        output = subprocess.Popen(['cat', 'sflowtf6'], stdout=subprocess.PIPE).communicate()[0]
        response = str(output, 'utf-8')
        #print(response)
        result = Cmtp.sflow_agent_dict_filtered(sfile=response, agent_id='7.7.7.7', sip_pat='3001:*:*:*:*:*:*:*', dip_pat='3001:*:*:*:*:*:*:*', ver='6', num=2)
        Cmtp.rfprint(result, 1)

    def test_rfprint(self):
        test_obj = {"a":"1", "b":"2"}
        Cmtp.rfprint(test_obj, new_width=1)

if __name__ == '__main__' :
    unittest.main()
