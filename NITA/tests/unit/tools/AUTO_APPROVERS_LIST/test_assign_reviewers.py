import unittest
from mock import patch, MagicMock
from jnpr.toby.tools.AUTO_APPROVERS_LIST import assign_reviewers
from ldap3 import Server

class Test_Assign_Reviewers(unittest.TestCase):

  
      def test_main(self):
          try:
             response= assign_reviewers.main(argv=(1,))
          except:
             pass
          try:
             server = MagicMock(spec=Server)
             with patch('ldap3.Server.net', return_value=server) as serv_patch:
                 assign_reviewers.main(argv=("assign_reviewvers",123,'some.yaml'))
          except:
             pass

         
      def test_get_jam_members(self):
          conn = MagicMock()
          conn.search = MagicMock()
          conn.response = [{'attributes':{'member':['A'],'sAMAccountName':'dummymembers'}},{}]
          result = assign_reviewers.get_jam_members('dummyalias',conn)
          self.assertEqual(result,['dummymembers'])

          conn.response = [{'attributes':{'member':[],'sAMAccountName':'dummymembers'}},{}]
          result = assign_reviewers.get_jam_members('dummyalias',conn)
          self.assertFalse(result)
          

if __name__ == '__main__':
   unittest.main()


