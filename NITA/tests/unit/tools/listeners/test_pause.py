import unittest2 as unittest
from nose.plugins.attrib import attr
from mock import patch, MagicMock
from jnpr.toby.tools.listeners import pause

@attr('unit')
class TestLogger(unittest.TestCase):
    def test_pause_new(self):
        p = pause.pause()
        pause.resume_execution(1,2)
        p.check_for_pause('testcases', 'before', 'KEY1')

if __name__=='__main__':
    unittest.main()
