"""
Unit test cases for influxReader.py
author:
"""

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from jnpr.toby.system.jvision.influxReader import create_influxdb_handle, InfluxDB


@attr('unit')
class TestSystem(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        builtins.tv=MagicMock()

    def test_influx_handle(self):
        t_var = MagicMock()
        influxobj = create_influxdb_handle(t=t_var, dbname='_int')
        self.assertIsInstance(influxobj, InfluxDB)

if __name__ == '__main__':
    unittest.main()

