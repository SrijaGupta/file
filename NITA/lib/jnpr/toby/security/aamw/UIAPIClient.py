#!/usr/bin/python

import hashlib

try:
    from http import HTTPStatus
except Exception:
    import http.client as HTTPStatus

import inspect
import json
import logging
import time

import requests
import urllib3

# Token is alive for 15 min
TOKEN_UPDATE_INTERVAL = 15 * 60
V1_URI_TEMPLATE = '/v1/skyatp/ui_api/%s'
V2_URI_TEMPLATE = '/v2/skyatp/ui_api/%s'

POST_TOKEN_URI = V1_URI_TEMPLATE % 'login/new_token'

SMTP_ACTION_URI = V1_URI_TEMPLATE % 'email/config/smtp'
IMAP_ACTION_URI = V1_URI_TEMPLATE % 'email/config/imap'

XLIST_URI = V1_URI_TEMPLATE % '{list_type}/{category}'

XLIST_ADD_SINGLE_URI = V1_URI_TEMPLATE % 'xlist/{list_type}/{category}'
XLIST_DEL_SINGLE_URI = V1_URI_TEMPLATE % \
                       'xlist_entry/{list_type}/{category}/{xlist_id}'

HOST_IP_URI = V1_URI_TEMPLATE % 'host/{host_ip}'

ENROLL_URL_GET_URI = V1_URI_TEMPLATE % 'devices/enroll'

INTEGRATED_FEED = V1_URI_TEMPLATE % 'integrated_feed'

VALID_LIST_TYPES = ['blacklist', 'whitelist']
VALID_SERVER_TYPES = ['hostnames', 'urls', 'ips', 'emails']

DEVICE_PROFILE = V1_URI_TEMPLATE % 'device_profile'
DEVICE_PROFILE_ID = V1_URI_TEMPLATE % 'device_profile/{profile_id}'
DEVICE_PROFILES = V1_URI_TEMPLATE % 'device_profiles'

DEVICE_TELEMETRY = V1_URI_TEMPLATE % 'devices/telemetry/{protocol}'

SYSLOG_EVENT_STATUS = V1_URI_TEMPLATE % 'global_config/syslog_event_status'

APP_TOKEN = V1_URI_TEMPLATE % 'app_token'
DELETE_APP_TOKEN = V1_URI_TEMPLATE % 'app_token/{token_id}'

DEVICE_ASSOCIATE_URI = V2_URI_TEMPLATE % 'device/{device_id}/associate_realm/'\
                                      '{sub_realm_id}'
LINKED_REALMS_URI = V2_URI_TEMPLATE % 'realm_management/linked_realms'
DEVICE_LIST_URI = V2_URI_TEMPLATE % 'devices'
DEVICE_URI = V2_URI_TEMPLATE % 'device/{device_id}'

FEED_LIST_URI = V2_URI_TEMPLATE % 'feeds'
XLIST_URI_V2 = V2_URI_TEMPLATE % '{list_type}/{category}'

FEED_ID = V2_URI_TEMPLATE % 'feeds/{feed_id}'
GET_FEEDS_DATA = V2_URI_TEMPLATE % 'feeds/{feed_id}/feed_data'
EXCLUDE_FEEDS_DATA = V2_URI_TEMPLATE % 'exclude_feed_data'
EXCLUDE_FEEDS_DATA_ID = V2_URI_TEMPLATE % 'exclude_feed_data/{data_id}'

VALID_LIST_TYPES_V2 = ['security_profiling']
VALID_FEED_TYPES_V2 = ['url', 'ip', 'userid']


class UIAPIClient(object):
    """
    Sky ATP UI API Client
    """

    def __init__(self, url, email_addr, realm, pwd):
        # Suppress warning
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.base_url = url
        self.email_addr = email_addr
        self.realm = realm
        self.pwd = pwd

        self.header = dict()
        self._last_token_update_ts = 0
        self._update_header(force=True)

    def _ui_api_request(self, method, uri, headers=None, data=None, 
                        params=None, json_content=None, files=None,
                        raw=False, verify=True, exp_resp_code=None):
        """
        Send https request:
        :param method: get, post, patch, del
        :param uri: URI path, e.g. "/v1/skyatp/lookup/hash"
        :param headers: token is expected in headers
        :param data: request body
        :param files: files to upload
        :param json_content: json to added in request
        :return: response content, and response status code
        """
        url = self.base_url + uri
        s = requests.Session()
        if headers is not None:
            s.headers.update(headers)
        else:
            s.headers.update(self.header)

        logging.info('-------------- Send request start --------------')
        logging.info("Send request for API: %s", inspect.stack()[1][3])
        logging.info("Request method: %s", method.upper())
        logging.info('Send request via link: %s', url)

        if headers:
            logging.info('Send request headers: %s', headers)
        if data:
            logging.info('Send request data: %s', data)
        if params:
            logging.info('Send request params: %s', params)
        if json_content:
            logging.info('Send request json: %s', json_content)

        r = s.request(method, url, files=files, data=data, params=params,
                      json=json_content, verify=False)
        resp, resp_code = r.content.decode('utf-8'), r.status_code

        logging.info('Request sent with url: %s', r.url)
        logging.info('-------------- Send request complete --------------')

        logging.info('-------------- Process response start --------------')
        logging.info('Expect response code: %s', exp_resp_code)
        logging.info("Actual response code: %s", resp_code)
        logging.info("Response message: %s", resp)
        if verify:
            if exp_resp_code is None:
                exp_resp_code = HTTPStatus.OK
            if type(exp_resp_code) in (set, list, tuple, dict):
                err_msg = 'Actual response code: %s, expect: %s' % \
                          (int(resp_code),
                           str([int(x) for x in exp_resp_code]))
                assert resp_code in exp_resp_code, err_msg
            else:
                err_msg = 'Actual response code: %s, expect: %s' % \
                          (int(resp_code), int(exp_resp_code))
                assert resp_code == exp_resp_code, err_msg
            logging.info('Response code verified')
        else:
            logging.info('Not verifying response code')

        if raw:
            logging.info('Returning raw message')
        else:
            try:
                resp = json.loads(resp)
            except Exception as err:
                logging.info('Exception when decoding http resp: %s', err)
                assert False, 'Response content is not in Json format'
            else:
                logging.info('Response message loaded as json')

        logging.info('-------------- Process response complete --------------')
        return resp

    def _get_pwd_hash(self):
        """
        Calculate password hash with realm name, email address and password
        :return: password hash
        """
        data_to_hash = (self.realm + self.email_addr + self.pwd).encode()
        data_hash = hashlib.sha256(data_to_hash)
        for _ in range(4096):
            data_hash = hashlib.sha256(data_hash.digest())
        return data_hash.hexdigest()

    def _update_header(self, retry=3, force=False):
        """
        Update auth header
        :param retry: max retry
        :param force: True for force update
        """
        if not force and int(time.time()) - self._last_token_update_ts <= \
                TOKEN_UPDATE_INTERVAL:
            logging.info('No need to update token: UI API token still '
                         'unexpired.')
            return

        logging.info('Start retrieving UI API token...')
        index = 0
        payload = {
            'email': self.email_addr,
            'realm': self.realm,
            'passwd_hash': self._get_pwd_hash()
        }
        headers = {'content-type': 'application/json'}
        while index < retry:
            index += 1
            logging.info('Try retrieving UI API token #%s', index)
            try:
                token = self._ui_api_request(
                    'POST', POST_TOKEN_URI, headers=headers,
                    data=json.dumps(payload))['data']
            except Exception:
                logging.warning('Fail to retrieve UI API token')
                time.sleep(5)
            else:
                logging.info('Retrieve UI API token successfully')
                self.header = {
                    'Authorization': 'Bearer %s' % token
                }
                self._last_token_update_ts = int(time.time())
                break
        else:
            err_msg = 'Fail to retrieve UI API token after %s retry' % retry
            logging.error(err_msg)
            self.header = dict()
            raise ValueError(err_msg)

    def set_email_action(self, protocol, action, **kwargs):
        """
        Set email action
        :param protocol: Protocol, can be "smtp" or "imap"
        :param action: Action
        :param kwargs: Other params
        """
        self._update_header()
        if protocol.lower() == 'smtp':
            self._set_smtp_config(action, **kwargs)
        elif protocol.lower() == 'imap':
            self._set_imap_config(action, **kwargs)
        else:
            err_msg = 'Unexpected email protocol name: %s' % protocol
            logging.error(err_msg)
            raise ValueError(err_msg)

    def _get_xlist(self, category, list_type):
        """
        Get blacklist/whitelist
        :param category: list category
        :param list_type: list type
        """
        category, list_type = self._validate_server_list_type(
            category, list_type)
        logging.info('Getting %s %s', category, list_type,)

        uri = XLIST_URI.format(category=category, list_type=list_type)
        res = self._ui_api_request('GET', uri)['data'][category]
        return [x['value'] for x in res]

    def _update_xlist(self, category, list_type, server_list):
        """
        Update xlist
        :param category: Server category
        :param list_type: List type
        :param server_list: Server list
        """
        category, list_type = self._validate_server_list_type(
            category, list_type)

        logging.info('Updating %s %s with: %s', category, list_type,
                     str(server_list))
        uri = XLIST_URI.format(category=category, list_type=list_type)
        json_dict = {
            'id': category,
            category: [{'value': server} for server in server_list]
        }
        self._ui_api_request('PUT', uri, json_content=json_dict)

    def add_one_xlist(self, category, list_type, server):
        """
        Add one xlist
        :param category: Server category
        :param list_type: List type
        :param server: Server
        """
        self._update_header()
        category, list_type = self._validate_server_list_type(
            category, list_type)

        logging.info('Adding %s %s with: %s', category, list_type, server)

        server_list = self._get_xlist(category, list_type)
        server_list.append(server)
        self._update_xlist(category, list_type, server_list)

        logging.info('Server %s added to %s %s', server, category, list_type)

    def delete_one_xlist(self, category, list_type, server):
        """
        Delete one xlist
        :param category: Server category
        :param list_type: List type
        :param server: Server
        """
        self._update_header()
        category, list_type = self._validate_server_list_type(
            category, list_type)

        logging.info('Deleting from %s %s: %s', category, list_type, server)

        server_set = set(self._get_xlist(category, list_type))
        if server not in server_set:
            logging.warning('Server %s not found in existing server list: %s',
                            server, list(server_set))
        else:
            server_set.remove(server)
            self._update_xlist(category, list_type, list(server_set))
            logging.info('Server %s deleted from %s %s', server, category,
                         list_type)

    def _set_smtp_config(self, action, **kwargs):
        """
        Set smtp configuration
        :param action: smtp action
        """
        assert action and action.lower() in ['permit', 'quarantine',
                                             'tag-and-deliver'],\
            "Unexpected action for smtp: %s" % action
        json_dict = {'action': action}
        if kwargs:
            json_dict.update(kwargs)
        json_dict = {'smtp': json_dict}
        logging.info('Setting SMTP config to %s', json_dict)
        self._ui_api_request('PUT', SMTP_ACTION_URI, json_content=json_dict)
        server_act = self._ui_api_request('GET', SMTP_ACTION_URI)['data'][
            'smtp']['action'].lower()
        assert action.lower() == server_act, \
            'Unexpected action: %s, expecting %s' % (server_act, action)

    def _set_imap_config(self, action, **kwargs):
        """
        Set imap configuration
        :param action: imap action
        """
        assert action and action.lower() in ['block', 'permit'], \
            "Unexpected action for imap: %s" % action
        json_dict = {'action': action}

        if kwargs:
            json_dict.update(kwargs)
        json_dict = {'imap': json_dict}
        logging.info('Setting IMAP config to %s', json_dict)
        self._ui_api_request('PUT', IMAP_ACTION_URI, json_content=json_dict)
        server_act = self._ui_api_request('GET', IMAP_ACTION_URI)['data'][
            'imap']['action'].lower()
        assert action.lower() == server_act, \
            'Unexpected action: %s, expecting %s' % (server_act, action)

    @staticmethod
    def _validate_server_list_type(server_type, list_type):
        """
        Validate server
        :param server_type: server type
        :param list_type: list type
        """
        assert server_type and server_type.lower() in VALID_SERVER_TYPES, \
            'Unexpected category: %s' % server_type
        assert list_type and list_type.lower() in VALID_LIST_TYPES, \
            'Unexpected list type: %s' % list_type

        return server_type.lower(), list_type.lower()

    def _validate_feed_list_type_v2(feed_type, list_type):
        """
        Validate feed list
        :param feed_type: feed type
        :param list_type: list type
        """
        assert feed_type and feed_type.lower() in VALID_FEED_TYPES_V2, \
            'Unexpected category: %s' % feed_type
        assert list_type and list_type.lower() in VALID_LIST_TYPES_V2, \
            'Unexpected list type: %s' % list_type

        return feed_type.lower(), list_type.lower()

    def set_ha_ip_status(self, ip, status=3, policy=0):
        """
        Set infected host status
        :param ip: IP server
        :param status: Host status, default to be resolved_fixed
            HOST_STATUS_NOT_STARTED = 0
            HOST_STATUS_IN_PROGRESS = 1
            HOST_STATUS_RESOLVED_FP = 2
            HOST_STATUS_RESOLVED_FIXED = 3
            HOST_STATUS_RESOLVED_IGNORE = 4
        :param policy: default is Use configured policy
            0: Use configured policy
            1: Always include host in infected hosts feed
            2: Never include host in infected hosts feed
        """
        json_dict = {'investigation_state': status, 'policy': policy}
        logging.info('Setting host %s status to %s', ip, status)
        self._ui_api_request('PATCH', HOST_IP_URI.format(host_ip=ip),
                             json_content=json_dict,
                             exp_resp_code=[HTTPStatus.OK,
                                            HTTPStatus.NOT_FOUND])

    def device_profile_post(self, profile_name, category_thresholds,
                            disabled_categories):
        """
        Create device profile
        :param profile_name: Profile name
        :param category_thresholds: Category thresholds
        :param disabled_categories: Disabled categories
        """
        self._update_header()
        data = {'category_thresholds': category_thresholds,
                'profile_name': profile_name,
                'disabled_categories': disabled_categories}
        data = json.dumps(data)
        self._ui_api_request('POST', DEVICE_PROFILE, data=data,
                             exp_resp_code=HTTPStatus.OK)

    def device_profile_delete(self, profile_id):
        """
        Delete device profile
        """
        self._update_header()
        self._ui_api_request('DELETE',
                             DEVICE_PROFILE_ID.format(profile_id=profile_id),
                             exp_resp_code=HTTPStatus.OK)

    def device_profiles_get(self):
        """
        Get device profiles
        """
        self._update_header()
        return self._ui_api_request('GET', DEVICE_PROFILES,
                                    exp_resp_code=HTTPStatus.OK)

    def clear_device_profile(self, profile_name):
        """
        Get device profile
        :param profile_name: Profile name
        """
        # get profile id
        profile_id = None
        profiles = self.device_profiles_get().get('data', {}).get(
            'profiles', [])
        for profile in profiles:
            if profile['profile_name'] == profile_name:
                profile_id = profile['profile_id']
                break

        if not profile_id:
            logging.debug("Unable to get profile id for %s", profile_name)
        else:
            self.device_profile_delete(profile_id)

    def host_get(self, host_ip):
        """
        Get host information
        :param host_ip: host ip address
        """
        self._update_header()
        return self._ui_api_request('GET', HOST_IP_URI.format(host_ip=host_ip),
                                    exp_resp_code=HTTPStatus.OK)

    def verify_recent_host_event(self, host_ip, event_type):
        """
        :param host_ip: host IP
        :param event_type:
            1: Malware hit
            2: CC hit
            3: Investigation status changed
            4: IP Change Event
            5: IP Change Event
        """
        events = self.host_get(host_ip).get('data', {}).get('events', [])
        if not events:
            return False

        if events[0].get('event_type', 0) == event_type:
            return True

        return False

    def get_telemetry(self, protocol):
        """
        Get telemetry data
        :param protocol: protocal info
        """
        self._update_header()
        return self._ui_api_request(
            'GET', DEVICE_TELEMETRY.format(protocol=protocol),
            exp_resp_code=HTTPStatus.OK)

    def get_device_telemetry_data(self, serial, protocol, action):
        """
        Get device telemetry data
        :param serial: Serial number
        :param protocol: Protocol of the counter
        :param action: Action of counter
        :return: Counter
        """
        data = self.get_telemetry(protocol)
        for device in data.get("data", []):
            if device.get("device_sn", "") == serial:
                if action == 'permit':
                    return device.get("permitted", -1)
        return -1

    def get_enroll_url(self):
        """Get enrollment url"""
        logging.info('Getting enrollment url')
        op_cmd = self._ui_api_request('POST',
                                      ENROLL_URL_GET_URI)['data']['command']
        return op_cmd[7:]

    def integrated_feed_put(self, feeds=None):
        """
        Update integrated feeds config
        :param feeds: Integrated feeds
        """
        self._update_header()

        data = {"feeds": []}
        if feeds:
            for feed in feeds:
                data["feeds"].append(
                    {'feed_name': feed, 'feed_in_ha': False})
        data = json.dumps(data)

        self._ui_api_request('PUT', INTEGRATED_FEED, data=data,
                             exp_resp_code=HTTPStatus.OK)

    def syslog_event_status_put(self):
        """
        Update syslog event status
        """
        self._update_header()

        data = {"event_log_status": {"host_status_changed_event": True,
            "malware_event": True}}
        data = json.dumps(data)

        self._ui_api_request('PUT', SYSLOG_EVENT_STATUS, data=data,
                             exp_resp_code=HTTPStatus.OK)

    def create_app_token(self, token_name):
        """
        Create an app token
        :param token_name: Token name
        :return: App token
        """
        self._update_header()

        data = {
            'access_groups': ["Open API"],
            'token_name': token_name,
            'token_desc': "test purpose"
        }

        response = self._ui_api_request(
            'POST', APP_TOKEN, data=json.dumps(data),
            exp_resp_code=HTTPStatus.OK)

        return response['data']

    def get_app_token_id(self, token_name):
        """
        Get app token id
        :param token_name: Token name
        :return: Token ID
        """
        self._update_header()

        response = self._ui_api_request(
            'GET', APP_TOKEN, exp_resp_code=HTTPStatus.OK)

        for token in response['data']['tokens']:
            if token['token_name'] == token_name:
                token_id = token['token_id']
                return token_id

        return None

    def delete_app_token(self, token_name):
        """
        Delete app token
        :param token_name: Token name
        """
        self._update_header()

        token_id = self.get_app_token_id(token_name)
        if not token_id:
            return None

        return self._ui_api_request(
            'DELETE', DELETE_APP_TOKEN.format(token_id=token_id),
            exp_resp_code=HTTPStatus.OK)

    def assign_device_to_sub_realm(self, device_host, ld_tenant_id,
                                   device_ld_name=""):
        """
        Assign a device to a logical domain
        :param device_host: Device hostname
        :param ld_tenant_id: Sub-realm tenant ID
        :param device_ld_name: Device logical domain name
        :return: Response status
        """
        self._update_header()
        device_ld_id = self._get_ldom_device_id(device_host, device_ld_name)
        ldom_sub_realm_id = self._get_ldom_sub_realm_id(ld_tenant_id)

        return self._ui_api_request(
            'POST', DEVICE_ASSOCIATE_URI.format(
                device_id=device_ld_id, sub_realm_id=ldom_sub_realm_id),
            exp_resp_code=HTTPStatus.OK)

    def remove_device_from_sub_realm(self, device_host, ld_tenant_id,
                                     device_ld_name=""):
        """
        Remove a device from a logical domain
        :param device_host: Device hostname
        :param ld_tenant_id: Sub-realm tenant ID
        :param device_ld_name: Device logical domain name
        :return: Response status
        """
        self._update_header()
        device_ld_id = self._get_ldom_device_id(device_host, device_ld_name)
        ldom_sub_realm_id = self._get_ldom_sub_realm_id(ld_tenant_id)

        return self._ui_api_request(
            'DELETE', DEVICE_ASSOCIATE_URI.format(
                device_id=device_ld_id, sub_realm_id=ldom_sub_realm_id),
            exp_resp_code=HTTPStatus.OK)

    def _get_ldom_device_id(self, device_host, device_ld_name):
        """
        Get ID for LDOM device ID
        :param device_host: Device hostname
        :param device_ld_name: Device Ldom name
        :return: Device Ldom ID
        """
        device_list = self.get_device_list(include_ldoms=True)
        for device in device_list:
            if device['logical_domain'] == device_ld_name and \
                    device['host'] == device_host:
                return device['device_id']
        raise KeyError('LDOM device not found')

    def _get_ldom_sub_realm_id(self, ld_tenant_id):
        """
        Get sub-realm ID for a LDOM
        :param ld_tenant_id: LDOM realm id
        :return: Logical domain tenant ID
        """
        sub_realm_list = self.get_sub_realms()
        for sub_realm in sub_realm_list:
            if sub_realm['sub_tenant_id'] == ld_tenant_id:
                return sub_realm['sub_realm_id']
        raise KeyError('Sub-realm not found')

    def get_device_list(self, include_ldoms=True):
        """
        Get device list
        :param include_ldoms: True for including device LDOMs
        :return: Device list
        """
        self._update_header()
        return self._ui_api_request(
            'GET', DEVICE_LIST_URI, params={'include_ldoms': include_ldoms},
            exp_resp_code=HTTPStatus.OK)['data']['devices']

    def get_sub_realms(self):
        """
        Get sub-realms
        :return: List of sub-realms
        """
        self._update_header()
        return self._ui_api_request(
            'GET', LINKED_REALMS_URI,
            exp_resp_code=HTTPStatus.OK)['data']['sub_realms']

    def device_feeds_get(self):
        """
        Get device profiles
        """
        self._update_header()
        return self._ui_api_request('GET', FEED_LIST_URI,
                                    exp_resp_code=HTTPStatus.OK)

    def check_feed_in_cloud(self, feed_name):
        """
        Check Feed In Cloud
        :param feed_name: Feed name
        :return: Ture or False
        """
        self._update_header()

        response = self._ui_api_request(
            'GET', FEED_LIST_URI, exp_resp_code=HTTPStatus.OK)
        for feed in response['data']['feeds']:
            if feed['feed_name'] == feed_name:
                return True
        return False

    def get_feed_id(self, feed_name):
        """
        Get feed id
        :param feed_name: feed name
        :return: feed ID
        """
        self._update_header()
        response = self._ui_api_request('GET', FEED_LIST_URI, 
                                        exp_resp_code=HTTPStatus.OK)
        feed_id = None
        for feed in response['data']['feeds']:
            if feed['feed_name'] == feed_name:
                feed_id = feed['feed_id']
                return feed_id
        return None

    def create_new_feed(self, feed_name):
        """
        Create a feed
        :param feed_name: Feed name
        :return: Feed
        """
        self._update_header()

        data = {
            'feed_type': "ip",
            'feed_category': "SecProfiling",
            'feed_ttl': 365,
            'feed_name': feed_name
        }

        response = self._ui_api_request(
            'POST', FEED_LIST_URI, data=json.dumps(data),
            exp_resp_code=HTTPStatus.OK)

        return response['data']

    def delete_one_feed(self, feed_name):
        """
        Delete a feed
        :param feed_name: Feed name
        :return: null
        """
        self._update_header()

        feed_id = self.get_feed_id(feed_name)
        if not feed_id:
            return None

        response = self._ui_api_request(
            'DELETE', FEED_ID.format(feed_id=feed_id),
            exp_resp_code=HTTPStatus.OK)

        return response['data']

    def get_feed_content(self, feed_name):
        """
        Get all feed entries
        :param feed_name: Feed name
        :return: feeds
        """
        self._update_header()

        feed_id = self.get_feed_id(feed_name)
        if not feed_id:
            return None

        return self._ui_api_request('GET',
                                    GET_FEEDS_DATA.format(feed_id=feed_id),
                                    exp_resp_code=HTTPStatus.OK)

    def get_data_id(self, feed_name, data_name):
        """
        Get feed entry id
        :param feed_name: feed name
        :patsm date_name: entry name
        :return: data id
        """
        self._update_header()

        feed_id = self.get_feed_id(feed_name)
        if not feed_id:
            return None

        response = self._ui_api_request(
            'GET', GET_FEEDS_DATA.format(feed_id=feed_id),
            exp_resp_code=HTTPStatus.OK)
        data_id = None
        for data in response['data']['feed_data']:
            if data['source'] == data_name:
                data_id = data['data_id']
                return data_id

        return None
        
    def delete_device(self, device_host):
        """
        Delete devices from Devices list in realm
        :return: Response Status
        """
        self._update_header()
        device_ld_id = self._get_ldom_device_id(device_host, "")

        return self._ui_api_request(
            'DELETE', DEVICE_URI.format(
                device_id=device_ld_id, exp_resp_code=HTTPStatus.OK))
