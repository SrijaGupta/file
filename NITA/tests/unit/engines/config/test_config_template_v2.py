#!/usr/local/bin/python3

"""
config_template_v2.py Unit Test
"""
import builtins
import unittest2 as unittest
from mock import patch, mock_open, Mock, MagicMock, call
from jnpr.toby.engines.config.config_template_v2 import ConfigEngine as configv2

template_content = ''' 
filetype: config_template_v2

templates:
  enable_python3:
    vars:
        python2:
        stuff: TRUE
    config: |
      set
        system
          scripts        var['scripts']
            language     var['language']
              python3    var['python3']
              python2    var['python2']
          stuff          var['stuff']
            depth1        
              depth2a    var['depth2a']
              depth2b    abc
'''

class TestConfigEngine(unittest.TestCase):
    def test__init(self):
        new_cfg = configv2()
        self.assertIsInstance(new_cfg, configv2)

    @patch("builtins.open", new_callable=mock_open, read_data=template_content) 
    @patch("jnpr.toby.engines.config.config_utils.find_file")
    def test_process_template_files_and_config(self, mock_file, find_file):
        self.find_file = MagicMock()
        new_cfg = configv2()
        new_cfg.process_template_files(template_files=[mock_file])
        cfg = new_cfg.config(template='enable_python3', args={'python3':'scripts', 'scripts':'scripts', 'language':'language', 'depth2a':'depth2a'})

if __name__ == '__main__':
    unittest.main()
