"""
Unit test cases for Csflow.py
author: dzhu 
"""
#import unittest2 as unittest
import unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import builtins
from jnpr.toby.utils import Csflow

#@attr('unit')
class TestSystem(unittest.TestCase):

    def setUp(self):
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        builtins.tv=MagicMock()

    def test_sflow_init(self):
        sflow = Csflow.Csflow()
        server =  MagicMock()
        #with self.assertRaises(Exception) as context:
        #    sflow.sflow_init(device=server, log_filename='slfowlog', decoder_path='/home/regress', decoder_port=6343)
        #self.assertTrue('cannot login to server as root user' in str(context.exception))
        sflow.sflow_init(device=server, log_filename='slfowtf', decoder_path='/home/regress', decoder_port=6343)

    def test_start_sflow_decoder(self):
        sflow = Csflow.Csflow()
        server =  MagicMock()
        sflow.log_filename = 'slfowtf'
        sflow.decoder_path = '/home/regress'
        sflow.start_sflow_decoder(server_handle=server, decoder_command='sflowtool')

    def test_stop_sflow_decoder(self):
        sflow = Csflow.Csflow()
        server =  MagicMock()
        sflow.decoder_status = True
        sflow.decoder_pid = 1234
        sflow.stop_sflow_decoder(server_handle=server)


if __name__ == '__main__' :
    unittest.main()
