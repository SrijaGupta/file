import unittest
from unittest.mock import Mock

from requests.sessions import Session

import jnpr.toby.security.aamw.UIAPIClient as client


class MockResponse(object):
    def __init__(self, decode_val, status_code):
        self.content = MockContent()
        self.content.decode = Mock(return_value=decode_val)
        self.status_code = status_code
        self.url = 'test_url'


class MockContent(object):
    def decode(self):
        return 'whatever'


class MockSession(object):
    def __init__(self):
        self.headers = dict()

    def request(self):
        pass


class TestUIAPIRequest(unittest.TestCase):
    def setUp(self):
        self.session_request_orig = Session.request
        self.uiapi_client_update_header_orig = client.UIAPIClient._update_header

    def tearDown(self):
        Session.request = self.session_request_orig
        client.UIAPIClient._update_header = self.uiapi_client_update_header_orig

    # Mock request
    def test_ui_api_request_success(self):
        mock_res = MockResponse('{"result": "good"}', 200)
        Session.request = Mock(return_value=mock_res)
        client.UIAPIClient._update_header = Mock()

        ui_api_client = client.UIAPIClient('a', 'b', 'c', 'd')

        self.assertEqual(ui_api_client._ui_api_request(
            'PUT', 'abc', {'header': 'y'}, {'data': 'y'}, {'params': 'y'},
            {'json': 'y'}, {'files': 'y'}), {"result": "good"})
        self.assertEqual(ui_api_client._ui_api_request(
            'PUT', 'abc', exp_resp_code={1, 200, 3}, raw=True),
            '{"result": "good"}')
        self.assertEqual(ui_api_client._ui_api_request(
            'PUT', 'abc', exp_resp_code={1, 2, 3}, verify=False, raw=True),
            '{"result": "good"}')

    def test_ui_api_request_fail(self):
        mock_res = MockResponse('something fail', 200)
        Session.request = Mock(return_value=mock_res)
        client.UIAPIClient._update_header = Mock()

        ui_api_client = client.UIAPIClient('a', 'b', 'c', 'd')
        with self.assertRaises(AssertionError):
            ui_api_client._ui_api_request(
                'PUT', 'abc', {'header': 'y'}, {'data': 'y'}, {'params': 'y'},
                {'json': 'y'}, {'files': 'y'})


class TestEmailAction(unittest.TestCase):

    def setUp(self):
        self.ui_api_request_orig = client.UIAPIClient._ui_api_request
        self.uiapi_client_update_header_orig = client.UIAPIClient._update_header
        client.UIAPIClient._update_header = Mock()

        client.UIAPIClient._ui_api_request = \
            Mock(return_value={'data': 'this is test data'})

        self.ui_api_client = client.UIAPIClient('a', 'b', 'c', 'd')

    def tearDown(self):
        client.UIAPIClient._ui_api_request = self.ui_api_request_orig
        client.UIAPIClient._update_header = self.uiapi_client_update_header_orig

    def test_set_email_action_success(self):
        action = 'permit'
        client.UIAPIClient._ui_api_request = \
            Mock(return_value={'data': {'smtp': {'action': action}}})
        self.assertEqual(self.ui_api_client.set_email_action(
            'smtp', action, something='sth'), None)

        action = 'block'
        client.UIAPIClient._ui_api_request = \
            Mock(return_value={'data': {'imap': {'action': action}}})
        self.assertEqual(self.ui_api_client.set_email_action(
            'imap', action, something='sth'), None)

    def test_set_email_action_fail(self):

        with self.assertRaises(ValueError):
            self.ui_api_client.set_email_action('something else', 'block',
                                                something='sth')
        with self.assertRaises(AssertionError):
            self.ui_api_client.set_email_action('smtp', 'bad',
                                                something='sth')
        with self.assertRaises(AssertionError):
            self.ui_api_client.set_email_action('imap', 'bad',
                                                something='sth')


class TestXlist(unittest.TestCase):

    def setUp(self):
        self.ui_api_request_orig = client.UIAPIClient._ui_api_request
        self.uiapi_client_update_header_orig = client.UIAPIClient._update_header
        client.UIAPIClient._update_header = Mock()
        client.UIAPIClient._ui_api_request = \
            Mock(return_value={'data': {'ips': [{'value':'1.1.1.1'}]}})

        self.ui_api_client = client.UIAPIClient('a', 'b', 'c', 'd')

    def tearDown(self):
        client.UIAPIClient._ui_api_request = self.ui_api_request_orig
        client.UIAPIClient._update_header = self.uiapi_client_update_header_orig

    def test_set_xlist_success(self):
        self.assertIsNone(
            self.ui_api_client.add_one_xlist('ips', 'blacklist', '1.1.1.1'))
        self.assertIsNone(
            self.ui_api_client.delete_one_xlist('ips', 'blacklist', '2.2.2.2'))
        self.assertIsNone(
            self.ui_api_client.delete_one_xlist('ips', 'blacklist', '1.1.1.1'))

    def test_set_xlist_fail(self):
        with self.assertRaises(AssertionError):
            self.ui_api_client.add_one_xlist('bad', 'blacklist', '1.1.1.1')
        with self.assertRaises(AssertionError):
            self.ui_api_client.add_one_xlist('ips', 'bad', '1.1.1.1')
        with self.assertRaises(AssertionError):
            self.ui_api_client.delete_one_xlist('bad', 'blacklist', '1.1.1.1')
        with self.assertRaises(AssertionError):
            self.ui_api_client.delete_one_xlist('ips', 'bad', '1.1.1.1')


class TestHAIPStatus(unittest.TestCase):

    def setUp(self):
        self.ui_api_request_orig = client.UIAPIClient._ui_api_request
        self.uiapi_client_update_header_orig = client.UIAPIClient._update_header
        client.UIAPIClient._update_header = Mock()

        client.UIAPIClient._ui_api_request = \
            Mock(return_value={'data': {'ips': [{'value':'1.1.1.1'}]}})

        self.ui_api_client = client.UIAPIClient('a', 'b', 'c', 'd')

    def tearDown(self):
        client.UIAPIClient._ui_api_request = self.ui_api_request_orig
        client.UIAPIClient._update_header = self.uiapi_client_update_header_orig

    def test_set_ha_ip_status(self):
        self.assertIsNone(self.ui_api_client.set_ha_ip_status('1.1.1.1'))

if __name__ == '__main__':
    unittest.main()