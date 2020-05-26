#!/usr/local/bin/python3

import sys

import mock
from mock import patch
from mock import Mock
from mock import MagicMock
import unittest
import unittest2 as unittest
from optparse import Values

import builtins
from jnpr.toby.services.scale.db_wrapper import db_wrapper

builtins.t = MagicMock()

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

class test_db_wrapper(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        t.log = MagicMock()
        self.db_wrapper_obj = db_wrapper()
        self.db_wrapper_obj.write_regression = 0
        self.db_wrapper_obj.cursor = Values()
        self.db_wrapper_obj.cursor.fetchone = MagicMock() 
        self.db_wrapper_obj.cursor.fetchone.return_value = [1,2]
        self.db_wrapper_obj.cursor.execute = MagicMock()
        self.db_wrapper_obj.__write_to_testcase_info_db = MagicMock()
        self.db_wrapper_obj.__update_table = MagicMock()
        self.db_wrapper_obj.table_name = 'table1_sy'
        self.db_wrapper_obj.script_name = 'test_script_name'
        self.db_wrapper_obj.update_table_dict = {'table1_sy':[1,2]} 

    def test_create_tables(self):
        ''' Test create_tables '''

        
        self.db_wrapper_obj.__get_script_to_table_mapping = MagicMock()
        self.db_wrapper_obj.create_table_if_not_exists = MagicMock()
        self.db_wrapper_obj.connect_to_db = MagicMock()
        self.db_wrapper_obj.close_db = MagicMock()
        test_table_dict = { 'table1_sy': 
            {
            'date' : 'Varchar(255)', 
            'Activity' : 'Varchar(255)', 
            'thput' : 'Varchar(255)', 
            'pps' : 'Varchar(255)', 
            'mem_load' : 'Varchar(255)', 
            'cpu_load' : 'Varchar(255)'
            }
        }
        self.assertEqual(self.db_wrapper_obj.create_tables(test_table_dict, 'script_name'), None)

    def test_write_table(self):
        ''' Test write table '''

        values = ['21/12/2018', 'AWS', '1000', '100', '67', '47']
        self.assertEqual(self.db_wrapper_obj.write_table('table1_sy', values),None) 

        
if __name__ == '__main__':
    unittest.main()




