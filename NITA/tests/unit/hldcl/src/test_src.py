import sys
import unittest2 as unittest
from mock import patch, MagicMock
from jnpr.toby.hldcl.src.src import Src
from jnpr.toby.hldcl.host import Host
from jnpr.toby.hldcl.juniper.junos import Response

class Testsrc(unittest.TestCase):

    @patch('jnpr.toby.hldcl.juniper.junos.Response')
    def test_execute(self, response_patch):
        srcobj = MagicMock(spec=Src)
        srcobj.prompt = "$"
        srcobj.handle = MagicMock()
        srcobj.channels ={}
        srcobj.channels['text'] = MagicMock()
        response_patch.return_value =  'execute output'
        srcobj.response = response_patch.return_value
        self.assertEqual(Src.execute(srcobj,pattern="$",command="show version"), 'execute output')

        srcobj.mode = 'cli'
        srcobj.config_mode = 'config'
        self.assertEqual(Src._switch_mode(srcobj), True)
        self.assertEqual(Src._switch_mode(srcobj, mode='shell'), True)
        self.assertEqual(Src._switch_mode(srcobj, mode='config'), True)

if __name__ == '__main__' :
    unittest.main()

