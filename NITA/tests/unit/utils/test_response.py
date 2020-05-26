import sys

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from jnpr.toby.utils.response import Response

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'


@attr('unit')
class TestResponse(unittest.TestCase):

    def test_Response_init(self):
        self.assertIsInstance(
            Response(response='response', status='status'), Response)

    def test_Response_response(self):
        sobject = MagicMock(spec=Response)
        sobject.resp = 'resp'
        sobject.stat = 'stat'
        self.assertEqual(Response.response(sobject), 'resp')

    def test_Response_status(self):
        sobject = MagicMock(spec=Response)
        sobject.resp = 'resp'
        sobject.stat = 'stat'
        self.assertEqual(Response.status(sobject), 'stat')

    def test___bool__(self):
        sobject = MagicMock(spec=Response)
        sobject.resp = 'resp'
        sobject.stat = 'stat'
        self.assertEqual(Response.__bool__(sobject), 'stat')

    def test____nonzero__(self):
        sobject = MagicMock(spec=Response)
        sobject.resp = 'resp'
        sobject.stat = 'stat'
        self.assertEqual(Response.__nonzero__(sobject), True)