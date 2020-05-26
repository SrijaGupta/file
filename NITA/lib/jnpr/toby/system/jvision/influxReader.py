"""
 Copyright 2017, Juniper Networks.
 All rights reserved
 mhusain@juniper.net,akanadam@juniper.net
 Created on March 28, 2017.
"""
from influxdb import InfluxDBClient

class InfluxDB(object):
    """
    Database class to fetch data from Influx DB server and
    store it in internal datastructures.
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    t = None
    def __init__(self, **kwargs):
        if not kwargs.get('dbname') and kwargs.get('t'):
            raise Exception("Database and t variables are mandatory")
        t = kwargs.get('t')
        self._user = t['user_variables']['uv-db-username']
        self._password = t['user_variables']['uv-db-password']
        self._hostname = t['user_variables']['uv-db-host']
        self._port = t['user_variables']['uv-db-port']
        self.dbname = kwargs.get('dbname')
        self.client = ""

    def db_init(self):
        """
        Create influxDB client
        The InfluxDBClient object holds necessary datastructures to connect to InfluxDB.
        Requests can be made to InfluxDB directly through the client.
        """
        t.log(level='info', message='Creating/Initializing db client')
        try:
            self.client = InfluxDBClient(self._hostname, self._port, self._user, self._password,\
                          self.dbname)
        except:
            raise Exception("Client connection to database failed")
        self.client.switch_database(self.dbname)
        t.log(level='info', message='Created db successfully with dbname:' +self.dbname)

    def db_query(self, query):
        """
        Query the db with query param.
        """
        result = self.client.query(query)
        t.log('info', result)
        return result

def create_influxdb_handle(**kwargs):
    """
    Constructor for InfluxDB Class

    """
    return InfluxDB(**kwargs)

