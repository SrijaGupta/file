''' This module contains db_wrapper class for database operations
    such as create tables, write table '''

__author__ = ['Manasa H G', 'Murli']
__contact__ = 'manasahg@uniper.net'
__copyright__ = 'Juniper Networks Inc.'

import re
import warnings
import os
import json
import pymysql
from jnpr.toby.services import utils


class db_wrapper(object):

    ''' class for creating tables and writing data to database

    Robot Example for importing::
        Library db_wrapper.py
    '''

    def __init__(self, database_name=None, hostname=None):
        ''' constructor method to create an object of the class and initilialize its variables

        :param string database_name:
            **OPTIONAL** Name of the database. Default value is rpt_snp_services_srx_manasahg
        :param string hostname:
            **OPTIONAL** Name of the host where the database resides. Default value is 10.223.3.29
        '''

        if database_name:
            self.database_name = database_name
        else:
            self.database_name = 'rpt_snp_services_srx'

        if hostname:
            self.hostname = hostname
        else:
            self.hostname = '10.223.3.29'

        self.log = utils.log
        self.username = 'snpuser'
        self.password = 'Embe1mpls'
        self.non_regression_database_name = 'rpt_snp_services_nr'
        self.mapping_table = 'trendr_mapping'
        self.testcase_info_table = 'testcase_info'
        self.update_table = 'table_updates'
        self.update_table_dict = dict()
        self.table_name = None
        self.script_name = None
        self.write_regression = None
        self.num_script_name = None
        self.conn = None
        self.cursor = None
        self.total_tbl = None
        self.connected_database = None
        self.num_testcase_name = None
        self.router_config = ""

    def connect_to_db(self, database_name=None):
        ''' connect to database

        :param string database_name:
            **OPTIONAL** Name of the database. Default value is rpt_snp_services_srx_manasahg
        '''

        self.log("DEBUG", "Database name is {}".format(database_name))
        try:
            if not database_name:
                self.log("DEBUG", "Going to connect to {}".format(
                    self.database_name))
                self.conn = pymysql.connect(
                    host=self.hostname, user=self.username,
                    passwd=self.password, db=self.database_name)
                self.log("DEBUG",
                         "Connected to {} with object {}".format(self.database_name, self.conn))
                self.connected_database = self.database_name
            elif database_name:
                self.log("DEBUG", "Going to connect to {}".format(database_name))
                self.conn = pymysql.connect(
                    host=self.hostname, user=self.username, passwd=self.password, db=database_name)
                self.log("DEBUG", "Connected to {} with object {}".format(
                    database_name, self.conn))
                self.connected_database = database_name
            self.cursor = self.conn.cursor()
            self.cursor.connection.autocommit(True)
        except pymysql.Error as error:
            self.log("DEBUG", "Error connecting to database {}".format(error))
            raise

    def close_db(self):
        ''' close the db connection '''

        try:
            self.cursor.close()
            self.conn.close()
            self.log("DEBUG", "self.conn while closing: {}".format(self.conn))
        except pymysql.Error as error:
            self.log(
                "DEBUG", "Error closing the connection to database: {}".format(error))
            raise

    def create_table_if_not_exists(self, table_name, values):
        ''' create Table if it doesn't exist

        :param string table_name:
            **REQUIRED** Name of the table to be created.
        :param dictionary values:
            **REQUIRED** Key-Value pair consisting of name of the attribute and its datatype.
        '''

        col_list = list()
        table_details = ""
        for colname, coltype in values.items():
            table_details = table_details + colname + " " + coltype + ", "
            col_list.append(colname)

        self.log("DEBUG", "The value of col_list :{}".format(col_list))
        self.update_table_dict[table_name] = col_list
        self.log("DEBUG", "Value of self.update_table_dict: {}".format(self.update_table_dict))
        # remove last comma  and space in the string - table_details
        table_details = table_details[:-2]

        sql1 = "CREATE TABLE IF NOT EXISTS `" + \
            table_name + "` (" + table_details + ")"
        self.log("DEBUG", "{}".format(sql1))

        self.cursor._defer_warnings = True
        try:
            self.cursor.execute(sql1)
        except pymysql.Error as error:
            self.log("DEBUG", "Error creating the table: {}".format(error))
            raise
        finally:
            self.cursor._defer_warnings = False

    def __get_row_count_for_script_name(self):
        ''' count the number of entries with the given script_name '''

        sql0 = "Select count(*) from " + self.mapping_table + \
               " where sname = '" + self.script_name + "'"
        self.log("DEBUG", "{}".format(sql0))

        try:
            self.cursor.execute(sql0)
            self.num_script_name = self.cursor.fetchone()[0]
        except pymysql.Error as error:
            self.log("DEBUG",
                     "Error while counting entries for the given script_name: {}".format(error))
            raise

    def __get_tablename_from_scriptname(self):
        ''' fetch table name for the respective script name from the mapping table

        :param string table_name:
            **REQUIRED** Name of the table to be created, \
                         whose name must be registered under appropriate script_name.
        '''

        sql1 = "Select tname from " + self.mapping_table + \
               " where sname = '" + self.script_name + "'"
        self.log("DEBUG", "{}".format(sql1))
        try:
            self.cursor.execute(sql1)
            tname = self.cursor.fetchone()[0]
            self.log("DEBUG", "Value of table name is: {}".format(tname))
        except pymysql.Error as error:
            self.log(
                "DEBUG", "Error reading table_name from the table: {}".format(error))
            raise

        if not tname or tname == self.table_name:
            self.write_regression = 1
        else:
            self.write_regression = 0

    def __get_script_to_table_mapping(self):
        ''' fetch the value of the table name for a given scipt name
            and set the flag - write_regression based on which the db name is chosen.

        :param string table_name:
            **REQUIRED** Name of the table to be created, \
                         whose name must be registered under appropriate script_name.
        '''

        self.__get_row_count_for_script_name()
        self.log("DEBUG", "num_script_name: {}".format(self.num_script_name))
        if self.num_script_name == 1:
            self.__get_tablename_from_scriptname()
        else:
            self.write_regression = 0

    def create_tables(self, table_dict, script_name, test_case_name=None):
        ''' create multiple tables.

        :param dictionary table_name:
            **REQUIRED** A dictionary of name of the tables \
                         and its attribute name and datatype to be created.
        :param string script_name:
            **REQUIRED** Name of the calling script.
        :param string test_case_name:
            **OPTIONAL** Name of the test_case_name in the calling script. Default value is None.

        Usage:
            script_name = 'name_of_the_calling_script'
            test_case_name = 'name_of_the_test_case_if_exists'
            table_dict = {'table1' : {
                            'activity' : 'Varchar(20)',
                            'topology_Name' : 'Varchar(255)',
                            'feature': 'Varchar(255)',
                            'sub_feature' : 'Varchar(255)',
                            'num_streams' : 'Varchar(25)',
                            'mss_value' : 'Varchar(25)',
                            'traffic_type' : 'Varchar(10)',
                            'thput' : 'Varchar(50)'
                            },
                        'table2' : {
                            'Name' : 'Varchar(20)',
                            'Execution_time' : 'Varchar(255)'
                            }
                        }
            class_object = db_wrapper()
            class_object.create_tables(table_dict, script_name, test_case_name)
        '''

        # decide the db
        for tname in table_dict.keys():
            if re.match(r".*_sy$", tname) or re.match(r".*_scsy$", tname):
                # script_name
                self.table_name = tname
                self.script_name = script_name
                # if test_case_name is not null, append it to script_name
                if test_case_name:
                    self.script_name = self.script_name + "-" + test_case_name
                # get mapping of table_name to script_name from db
                self.__get_script_to_table_mapping()
                # connect to non_regression db, depending on the flag -
                # write_regression
                self.log("DEBUG", "write_regression value: {}".format(
                    self.write_regression))
                if not self.write_regression:
                    self.close_db()
                    self.connect_to_db(self.non_regression_database_name)
                break

        # create table in the db
        for tname, value in table_dict.items():
            # create table if it doesn't exist; turn off the warning
            self.create_table_if_not_exists(tname, value)

    def write_table(self, table_name, values, res_handles=None):
        ''' write values to the table.

        :param string table_name:
            **REQUIRED** Name of the table to which data has to be written.
        :param list values:
            **REQUIRED** A list of values that has to be inserted to the table_name.

        Usage:
            table_name = 'sample_table_name'
            values = ['AWS', 'Topology3', 'L4 Firewall', 'Basic', '1', '1380', 'tcp', '2']
            class_object = db_wrapper()
            class_object.write_table(table_name, values)
        '''

        if self.write_regression is None:
            raise Exception("To maintain the integrity of data, \
                             function create_tables should be called before executing function write_tables, \
                             even if the table already exists.")

        self.__write_to_testcase_info_db(res_handles)

        values = [str(s) for s in values]
        self.log("DEBUG", "{}".format(values))
        query_params = "',  '".join(values)
        self.log(query_params)

        # sql query to insert data to appropriate db
        sql1 = "INSERT INTO " + table_name + \
            " values  ('" + query_params + "')"
        self.log("DEBUG", "{}".format(sql1))
        try:
            self.cursor.execute(sql1)
        except pymysql.Error as error:
            self.log("DEBUG", "Error inserting into the table: {}".format(error))
            raise
        self.__update_table(table_name, values)

    def __update_table(self, table_name, values):
        '''  update table in analyser db '''

        update_table_values = dict()
        if re.match(r".*_sy$", table_name) or re.match(r".*_scsy$", table_name):
            for index in range(0, len(self.update_table_dict[table_name])):
                if self.update_table_dict[table_name][index] == 'misc':
                    self.log("DEBUG", "{}".format(json.loads(values[index])))
                    update_table_values[self.update_table_dict[table_name][index]] = {k:v for k, v in json.loads(values[index]).items()}
                else:
                    update_table_values[self.update_table_dict[table_name][index]] = values[index]

        sql1 = "INSERT INTO " + self.update_table + " values  ('" + table_name + "', '" + \
               json.dumps(update_table_values) + "')"
        self.log("DEBUG", "{}".format(sql1))
        try:
            self.cursor.execute(sql1)
        except pymysql.Error as error:
            self.log("DEBUG", "Error inserting into the update table: {}".format(error))
            raise

    def write_multiple_tables(self, table_value_dict):
        ''' write values to multiple table.
        :param dictionary table_value_dict:
            **REQUIRED** A dictinary of multiple table name \
                         and its corresponding values that have to be inserted to database.

        Usage:
            table_value_dict = {'table1':
                            ['AWS', 'Topology3', 'L4 Firewall', 'Basic', '1', '1380', 'tcp', '2'],
                            'table2':
                            ['Azure', 'Topology2', 'S-to-S', 'Basic', '1', '1380', 'tcp', '2']
                                }
            class_object = db_wrapper()
            class_object.write_multiple_tables(table_value_dict)
        '''

        if self.write_regression is None:
            raise Exception("To maintain the integrity of data, \
                             function create_tables should be called \
                             before executing function write_tables, \
                             even if the table already exists.")

        for tname, value in table_value_dict.items():

            values = [str(s) for s in value]
            query_params = "',  '".join(values)

            # sql query to insert data to appropriate db
            sql1 = "INSERT INTO " + tname + " values  ('" + query_params + "')"
            self.log("DEBUG", "{}".format(sql1))
            try:
                self.cursor.execute(sql1)
            except pymysql.Error as error:
                self.log(
                    "DEBUG", "Error inserting into the table: {}".format(error))
                raise

    def __insert_update_testcase_info(self):
        ''' inset or update data into testcase_info table '''

        script_dict = '{"Script":"' + self.script_name + '"}'
        self.log("DEBUG", "{}".format(self.script_name))
        self.log("DEBUG", "{}".format(self.table_name))
        self.log("DEBUG", "{}".format(self.num_testcase_name))
        self.log("DEBUG", "{}".format(self.router_config))
        if self.num_testcase_name == 1:
            sql1 = "update " + self.testcase_info_table + " set descr = '', long_descr = '', config = '" + \
                self.router_config + "' , topo= '', misc = '" + script_dict + \
                "', tg_conf= ''  where testcase_name = '" + self.table_name + "'"
            self.log("DEBUG", "{}".format(sql1))
        else:
            query_params = self.table_name + "', '', '', '" + \
                self.router_config + "', '', '" + str(script_dict) + "', '"
            #query_params = [ self.table_name, '', '', self.router_config, '', script_dict ]
            #query_params = "',  '".join(query_params)

            sql1 = "insert into " + self.testcase_info_table + \
                " values ('" + query_params + "')"
        self.log("DEBUG", "{}".format(sql1))

        try:
            self.cursor.execute(sql1)
        except pymysql.Error as error:
            self.log(
                "DEBUG", "Error inserting or updating data into the table: {}".format(error))
            raise

    def __get_row_count_testcase_info(self):
        ''' count the num of entries for testcase_name '''

        sql0 = "Select count(*) from " + self.testcase_info_table + \
               " where testcase_name = '" + self.table_name + "'"

        self.log("DEBUG", "{}".format(sql0))

        try:
            self.cursor.execute(sql0)
            self.num_testcase_name = self.cursor.fetchone()[0]
        except pymysql.Error as error:
            self.log("DEBUG",
                     "Error while counting entries for the given testcase_name: {}".format(error))
            raise

    def __write_to_testcase_info_db(self, res_handles=None):
        ''' write config info to testcase_info db '''

        cmd1 = 'show configuration | find apply'
        cmd2 = 'show chassis hardware'
        pattern = '######################'
        #dut_name = t.get_devices(fv-tags='dut')[0]

        if not res_handles:
            #res_handles = [t.get_handle(resource) for resource in resources]
            #dut_name = 'xyz' # dummy
            resources = t.get_junos_resources()
            for resource in resources:
                res_handle = t.get_handle(resource)
                if 'fv-tags' in t.get_t(resource) and t.get_t(resource)['fv-tags'] == 'dut':
                    header1 = pattern + "\n" + "DUT-" + resource + \
                        "-Configuration" + "\n" + pattern + "\n\n"
                    header2 = pattern + "\n" + "DUT-" + resource + \
                        "-Hardware" + "\n" + pattern + "\n\n"
                else:
                    header1 = pattern + "\n" + resource + "-Configuration" + "\n" + pattern + "\n\n"
                    header2 = pattern + "\n" + resource + "-Hardware" + "\n" + pattern + "\n\n"

                response1 = res_handle.cli(
                    command=cmd1, format='text').response()
                self.log("DEBUG", "{}".format(response1))
                response2 = res_handle.cli(
                    command=cmd2, format='text').response()
                self.router_config = self.router_config + header1 + \
                    str(response1) + header2 + str(response2)
                self.log("DEBUG", "{}".format(self.router_config))

        else:
            self.log("DEBUG", "{}".format(res_handles))
            for item in range(0, len(res_handles)):
                if item == 0:
                    header1 = pattern + "\n" + "DUT" + \
                        "-Configuration" + "\n" + pattern + "\n\n"
                    header2 = pattern + "\n" + "DUT" + \
                        "-Hardware" + "\n" + pattern + "\n\n"
                else:
                    header1 = pattern + "\n" + "R" + \
                        str(item) + "-Configuration" + "\n" + pattern + "\n\n"
                    header2 = pattern + "\n" + "R" + \
                        str(item) + "-Hardware" + "\n" + pattern + "\n\n"

                self.log("DEBUG", "{}".format(res_handles[item]))
                response1 = res_handles[item].cli(
                    command=cmd1, format='text').response()
                self.log("DEBUG", "{}".format(response1))
                response2 = res_handles[item].cli(
                    command=cmd2, format='text').response()

                self.router_config = self.router_config + header1 + \
                    str(response1) + header2 + str(response2)
                self.log("DEBUG", "{}".format(self.router_config))

        self.__get_row_count_testcase_info()
        self.__insert_update_testcase_info()
