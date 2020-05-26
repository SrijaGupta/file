
from jnpr.toby.security.ssl.ssl_operational_cli import *

from mock import patch
import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.hldcl.juniper.junos import Juniper

class Response:
    def __init__(self, value=""):
        self.resp = value

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=Juniper)
    mocked_obj.log = MagicMock()



    def test_get_ssl_proxy_status(self):
        try:
            get_ssl_proxy_status()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        response = {'ssl-status': {'ssl-status':{'ssl-status-pic':
                                              {'ssl-status-pic-info':'spu - 5 fpc[1] pic[1]'}}}}
        x = {'ssl-status-pic-info':'spu - 5 fpc[1] pic[1]'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response)

        self.assertEqual(get_ssl_proxy_status(device=self.mocked_obj), x)


    def test_get_ssl_cert_cache_stats(self):

        try:
            get_ssl_cert_cache_stats()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        try:
            get_ssl_cert_cache_stats(device=self.mocked_obj, fpc="1")
        except Exception as err:
            self.assertEqual(err.args[0], "Either both or none should be given as arguments : 'fpc' and 'pic'")

        try:
            get_ssl_cert_cache_stats(device=self.mocked_obj, lsys="LSYS1", tenant='TN1')
        except Exception as err:
            self.assertEqual(err.args[0], "Both'tenant' and 'lsys' should not be passed together")

        response = {'ssl-proxy-cert-cache-statistics':{'ssl-proxy-cert-cache-statistics':
                                                          {'ssl-proxy-cert-cache-statistics-pic':
                                                               {'ssl-proxy-cert-cache-statistics-pic-info':'spu - 5 fpc[1] pic[1]',
                                                                'ssl-proxy-cert-cache-statistics-sess-cache-hit': '2',
                                                                'ssl-proxy-cert-cache-statistics-sess-cache-miss':'1',
                                                                'ssl-proxy-cert-cache-statistics-sess-cache-full':'1'}}}}

        x = {'cert_cache_miss': 1,
             'cert_cache_hit': 2,
             'cert_cache_full': 1}

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response)
        self.assertEqual(get_ssl_cert_cache_stats(device=self.mocked_obj, lsys="LSYS1"), x)
        self.assertEqual(get_ssl_cert_cache_stats(device=self.mocked_obj, fpc="1", pic="1"), x)

        try:
            get_ssl_cert_cache_stats(device=self.mocked_obj, fpc="1", pic="2", tenant="TN1")
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Invalid FPC-PIC value, Keyword failing")



    def test_get_ssl_session_cache_stats(self):

        try:
            get_ssl_session_cache_stats()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        try:
            get_ssl_session_cache_stats(device=self.mocked_obj, fpc="1")
        except Exception as err:
            self.assertEqual(err.args[0], "Either both or none should be given as arguments : 'fpc' and 'pic'")

        try:
            get_ssl_session_cache_stats(device=self.mocked_obj, lsys="LSYS1", tenant='TN1')
        except Exception as err:
            self.assertEqual(err.args[0], "Both'tenant' and 'lsys' should not be passed together")

        response = {'ssl-proxy-sess-cache-statistics':{'ssl-proxy-sess-cache-statistics':
                                                          {'ssl-proxy-sess-cache-statistics-pic':
                                                               {'ssl-proxy-sess-cache-statistics-pic-info':'spu - 5 fpc[1] pic[1]',
                                                                'ssl-proxy-sess-cache-statistics-sess-cache-hit': '2',
                                                                'ssl-proxy-sess-cache-statistics-sess-cache-miss':'1',
                                                                'ssl-proxy-sess-cache-statistics-sess-cache-full':'1'}}}}

        x = {'session_cache_miss': 1,
             'session_cache_hit': 2,
             'session_cache_full': 1}

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response)
        self.assertEqual(get_ssl_session_cache_stats(device=self.mocked_obj, lsys="LSYS1"), x)
        self.assertEqual(get_ssl_session_cache_stats(device=self.mocked_obj, fpc="1", pic="1"), x)

        try:
            get_ssl_session_cache_stats(device=self.mocked_obj, fpc="1", pic="2", tenant="TN1")
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Invalid FPC-PIC value, Keyword failing")



    def test_get_all_ssl_cert(self):

        try:
            get_all_ssl_cert()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        try:
            get_all_ssl_cert(device=self.mocked_obj, lsys="LSYS1", tenant='TN1')
        except Exception as err:
            self.assertEqual(err.args[0], "Both'tenant' and 'lsys' should not be passed together")

        response = {'ssl-certificate':{'ssl-certificate':"a"}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response)
        self.assertEqual(get_all_ssl_cert(device=self.mocked_obj, lsys="LSYS1"), [])


        response = {'ssl-certificate':{'ssl-certificate':{'ssl-certificate-pic':{'ssl-cert-id':"a"}}
                                       }}
        self.mocked_obj.execute_as_rpc_command.return_value=response
        self.assertEqual(get_all_ssl_cert(device=self.mocked_obj, tenant="TN1"), ["a"])

        response = {
            'ssl-certificate': {'ssl-certificate': {'ssl-certificate-pic': {'ssl-cert-id': ["a", "b"]}}
                                }}
        self.mocked_obj.execute_as_rpc_command.return_value = response
        self.assertEqual(get_all_ssl_cert(device=self.mocked_obj),
                         ["a", "b"])

        response = {
            'ssl-certificate': {
                'ssl-certificate': {
                    'ssl-certificate-pic': [{'ssl-cert-id': ["a", "b"]}, {'ssl-cert-id': ["a","b"]}]}
            }}

        self.mocked_obj.execute_as_rpc_command.return_value = response
        self.assertEqual(get_all_ssl_cert(device=self.mocked_obj),
                         ["a", "b"])

        response1 = {
            'ssl-certificate': {
                'ssl-certificate': {'ssl-certificate-pic': [{'ssl-cert-id': ["a", "b"]},{'ssl-cert-id': ["b"]} ]}
                }}

        self.mocked_obj.execute_as_rpc_command.return_value = response1
        try:
            get_all_ssl_cert(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")



        response2 = {
            'ssl-certificate': {
                'ssl-certificate': {'ssl-certificate-pic': [{'ssl-cert-id': ["a", "b"]},
                                                            {'ssl-cert-id': ["a", "c"]}]}
            }}

        self.mocked_obj.execute_as_rpc_command.return_value = response2
        try:
            get_all_ssl_cert(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")



        response3 = {
            'ssl-certificate': {
                'ssl-certificate': {'ssl-certificate-pic': [{'ssl-cert-id': "a"},
                                                            {'ssl-cert-id': "b"}]}
            }}

        self.mocked_obj.execute_as_rpc_command.return_value = response3
        try:
            get_all_ssl_cert(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")



    def test_get_all_ssl_profile(self):
        try:
            get_all_ssl_profile()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            get_all_ssl_profile(device=self.mocked_obj, lsys="LSYS1", tenant='TN1')
        except Exception as err:
            self.assertEqual(err.args[0], "Both'tenant' and 'lsys' should not be passed together")

        response = {'ssl-profile-list':"A"}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response)
        self.assertEqual(get_all_ssl_profile(device=self.mocked_obj, lsys="LSYS1"), [])

        response = {'ssl-profile-list':{'ssl-profile-list-pic' : {'ssl-profile-id' : '10', 'ssl-profile-name':"p1"}}}
        self.mocked_obj.execute_as_rpc_command.return_value = response
        self.assertEqual(get_all_ssl_profile(device=self.mocked_obj, tenant="TN1"), {"p1":'10'})

        response = {'ssl-profile-list': {
            'ssl-profile-list-pic': [{'ssl-profile-id': ['10', '11'], 'ssl-profile-name': ["p1", "p2"]},
                                     {'ssl-profile-id': ['10', '11'], 'ssl-profile-name': ["p1", "p2"]}]}}
        self.mocked_obj.execute_as_rpc_command.return_value = response
        self.assertEqual(get_all_ssl_profile(device=self.mocked_obj, tenant="TN1"), {"p1": '10', "p2":'11'})

        response1 = {'ssl-profile-list': {
            'ssl-profile-list-pic': [
                {'ssl-profile-id': ['10', '11'], 'ssl-profile-name': ["p2"]},
                {'ssl-profile-id': ['10', '11'], 'ssl-profile-name': ["p1", "p2"]}]}}

        self.mocked_obj.execute_as_rpc_command.return_value = response1
        try:
            get_all_ssl_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")


        response2 = {'ssl-profile-list': {
            'ssl-profile-list-pic': [
                {'ssl-profile-id': ['10'], 'ssl-profile-name': ["p1", "p2"]},
                {'ssl-profile-id': ['10', '11'], 'ssl-profile-name': ["p1", "p2"]}]}}

        self.mocked_obj.execute_as_rpc_command.return_value = response2
        try:
            get_all_ssl_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")


        response3 = {'ssl-profile-list': {
            'ssl-profile-list-pic': [
                {'ssl-profile-id': ['10', '12'], 'ssl-profile-name': ["p1", "p2"]},
                {'ssl-profile-id': ['10', '11'], 'ssl-profile-name': ["p1", "p2"]}]}}

        self.mocked_obj.execute_as_rpc_command.return_value = response3
        try:
            get_all_ssl_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")


        response4 = {'ssl-profile-list': {
            'ssl-profile-list-pic': [
                {'ssl-profile-id': ['10', '11'], 'ssl-profile-name': ["p1", "p3"]},
                {'ssl-profile-id': ['10', '11'], 'ssl-profile-name': ["p1", "p2"]}]}}

        self.mocked_obj.execute_as_rpc_command.return_value = response4
        try:
            get_all_ssl_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")


        response5 = {'ssl-profile-list': {
            'ssl-profile-list-pic': [
                {'ssl-profile-id': '11', 'ssl-profile-name': "p2"},
                {'ssl-profile-id': '10', 'ssl-profile-name': "p2"}]}}

        self.mocked_obj.execute_as_rpc_command.return_value = response5
        try:
            get_all_ssl_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")


        response6 = {'ssl-profile-list': {
            'ssl-profile-list-pic': [
                {'ssl-profile-id': '11', 'ssl-profile-name': "p1"},
                {'ssl-profile-id': '11', 'ssl-profile-name': "p2"}]}}

        self.mocked_obj.execute_as_rpc_command.return_value = response6
        try:
            get_all_ssl_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")



    def test_get_ssl_profile(self):
        try:
            get_ssl_profile()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")


        try:
            get_ssl_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'profile' is a mandatory argument")


        try:
            get_ssl_profile(device=self.mocked_obj, profile="p1", lsys="LSYS1", tenant='TN1')
        except Exception as err:
            self.assertEqual(err.args[0], "Both'tenant' and 'lsys' should not be passed together")

        response = {'ssl-profile-detail':{'ssl-profile-detail':"a"}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response)

        try:
            get_ssl_profile(device=self.mocked_obj, profile="p1", lsys="LSYS1")
        except Exception as err:
            self.assertEqual(err.args[0], "Given Profile name is not configured on DUT")

        response = {'ssl-profile-detail': {'ssl-profile-detail': {'ssl-profile-detail-pic':
                                                                      {'ssl-profile-allow-non-ssl-session': 'true',
                                                                     'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                                                                     'ssl-profile-initiation-profile-id': '65537',
                                                                     'ssl-profile-nof-whitelist-entries': '0',
                                                                     'ssl-profile-profile': 'p1',
                                                                     'ssl-profile-root-ca': 'false',
                                                                     'ssl-profile-termination-profile-id': '65537',
                                                                     'ssl-profile-trace': 'false'
                                                                       }
                                                                 }
                                           }
                    }
        x = {'ssl-profile-allow-non-ssl-session': 'true',
                                                                     'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                                                                     'ssl-profile-initiation-profile-id': '65537',
                                                                     'ssl-profile-nof-whitelist-entries': '0',
                                                                     'ssl-profile-profile': 'p1',
                                                                     'ssl-profile-root-ca': 'false',
                                                                     'ssl-profile-termination-profile-id': '65537',
                                                                     'ssl-profile-trace': 'false'
                                                                       }

        self.mocked_obj.execute_as_rpc_command.return_value = response
        self.assertEqual(get_ssl_profile(device=self.mocked_obj, tenant="TN1", profile="p1"), x)

        responsex = {'ssl-profile-detail': {'ssl-profile-detail': {'ssl-profile-detail-pic':
                                                                      [{
                                                                          'ssl-profile-allow-non-ssl-session': 'true',
                                                                          'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                                                                          'ssl-profile-initiation-profile-id': '65537',
                                                                          'ssl-profile-nof-whitelist-entries': '0',
                                                                          'ssl-profile-profile': 'p1',
                                                                          'ssl-profile-root-ca': 'false',
                                                                          'ssl-profile-termination-profile-id': '65537',
                                                                          'ssl-profile-trace': 'false'
                                                                          },
                                                                          {
                                                                              'ssl-profile-allow-non-ssl-session': 'true',
                                                                              'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                                                                              'ssl-profile-initiation-profile-id': '65537',
                                                                              'ssl-profile-nof-whitelist-entries': '0',
                                                                              'ssl-profile-profile': 'p1',
                                                                              'ssl-profile-root-ca': 'false',
                                                                              'ssl-profile-termination-profile-id': '65537',
                                                                              'ssl-profile-trace': 'false'
                                                                          }
                                                                      ]
                                                                  }
                                           }
                    }

        self.mocked_obj.execute_as_rpc_command.return_value = responsex
        self.assertEqual(get_ssl_profile(device=self.mocked_obj, tenant="TN1", profile="p1"), x)

        response1 = {'ssl-profile-detail': {'ssl-profile-detail': {'ssl-profile-detail-pic':
            [{
                'ssl-profile-allow-non-ssl-session': 'tue',
                'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                'ssl-profile-initiation-profile-id': '65537',
                'ssl-profile-nof-whitelist-entries': '0',
                'ssl-profile-profile': 'p1',
                'ssl-profile-root-ca': 'false',
                'ssl-profile-termination-profile-id': '65537',
                'ssl-profile-trace': 'false'
            },
                {
                    'ssl-profile-allow-non-ssl-session': 'true',
                    'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                    'ssl-profile-initiation-profile-id': '65537',
                    'ssl-profile-nof-whitelist-entries': '0',
                    'ssl-profile-profile': 'p1',
                    'ssl-profile-root-ca': 'false',
                    'ssl-profile-termination-profile-id': '65537',
                    'ssl-profile-trace': 'false'
                }
            ]
        }
        }
        }

        self.mocked_obj.execute_as_rpc_command.return_value = response1
        try:
            get_ssl_profile(device=self.mocked_obj, profile="p1")
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")


        response2 = {'ssl-profile-detail': {'ssl-profile-detail': {'ssl-profile-detail-pic':
            [{
                'ssl-profile-allow-non-ssl-session': 'true',
                'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                'ssl-profile-initiation-profile-id': '6537',
                'ssl-profile-nof-whitelist-entries': '0',
                'ssl-profile-profile': 'p1',
                'ssl-profile-root-ca': 'false',
                'ssl-profile-termination-profile-id': '65537',
                'ssl-profile-trace': 'false'
            },
                {
                    'ssl-profile-allow-non-ssl-session': 'true',
                    'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                    'ssl-profile-initiation-profile-id': '65537',
                    'ssl-profile-nof-whitelist-entries': '0',
                    'ssl-profile-profile': 'p1',
                    'ssl-profile-root-ca': 'false',
                    'ssl-profile-termination-profile-id': '65537',
                    'ssl-profile-trace': 'false'
                }
            ]
        }
        }
        }

        self.mocked_obj.execute_as_rpc_command.return_value = response2
        try:
            get_ssl_profile(device=self.mocked_obj, profile="p1")
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")

        response3 = {'ssl-profile-detail': {'ssl-profile-detail': {'ssl-profile-detail-pic':
            [{
                'ssl-profile-allow-non-ssl-session': 'true',
                'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                'ssl-profile-initiation-profile-id': '65537',
                'ssl-profile-nof-whitelist-entries': '1',
                'ssl-profile-profile': 'p1',
                'ssl-profile-root-ca': 'false',
                'ssl-profile-termination-profile-id': '65537',
                'ssl-profile-trace': 'false'
            },
                {
                    'ssl-profile-allow-non-ssl-session': 'true',
                    'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                    'ssl-profile-initiation-profile-id': '65537',
                    'ssl-profile-nof-whitelist-entries': '0',
                    'ssl-profile-profile': 'p1',
                    'ssl-profile-root-ca': 'false',
                    'ssl-profile-termination-profile-id': '65537',
                    'ssl-profile-trace': 'false'
                }
            ]
        }
        }
        }

        self.mocked_obj.execute_as_rpc_command.return_value = response3
        try:
            get_ssl_profile(device=self.mocked_obj, profile="p1")
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")

        response4 = {'ssl-profile-detail': {'ssl-profile-detail': {'ssl-profile-detail-pic':
            [{
                'ssl-profile-allow-non-ssl-session': 'true',
                'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                'ssl-profile-initiation-profile-id': '65537',
                'ssl-profile-nof-whitelist-entries': '0',
                'ssl-profile-profile': 'p12',
                'ssl-profile-root-ca': 'false',
                'ssl-profile-termination-profile-id': '65537',
                'ssl-profile-trace': 'false'
            },
                {
                    'ssl-profile-allow-non-ssl-session': 'true',
                    'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                    'ssl-profile-initiation-profile-id': '65537',
                    'ssl-profile-nof-whitelist-entries': '0',
                    'ssl-profile-profile': 'p1',
                    'ssl-profile-root-ca': 'false',
                    'ssl-profile-termination-profile-id': '65537',
                    'ssl-profile-trace': 'false'
                }
            ]
        }
        }
        }

        self.mocked_obj.execute_as_rpc_command.return_value = response4
        try:
            get_ssl_profile(device=self.mocked_obj, profile="p1")
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")

        response5 = {'ssl-profile-detail': {'ssl-profile-detail': {'ssl-profile-detail-pic':
            [{
                'ssl-profile-allow-non-ssl-session': 'true',
                'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                'ssl-profile-initiation-profile-id': '65537',
                'ssl-profile-nof-whitelist-entries': '0',
                'ssl-profile-profile': 'p1',
                'ssl-profile-root-ca': 'fal2se',
                'ssl-profile-termination-profile-id': '65537',
                'ssl-profile-trace': 'false'
            },
                {
                    'ssl-profile-allow-non-ssl-session': 'true',
                    'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                    'ssl-profile-initiation-profile-id': '65537',
                    'ssl-profile-nof-whitelist-entries': '0',
                    'ssl-profile-profile': 'p1',
                    'ssl-profile-root-ca': 'false',
                    'ssl-profile-termination-profile-id': '65537',
                    'ssl-profile-trace': 'false'
                }
            ]
        }
        }
        }

        self.mocked_obj.execute_as_rpc_command.return_value = response5
        try:
            get_ssl_profile(device=self.mocked_obj, profile="p1")
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")

        response6 = {'ssl-profile-detail': {'ssl-profile-detail': {'ssl-profile-detail-pic':
            [{
                'ssl-profile-allow-non-ssl-session': 'true',
                'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                'ssl-profile-initiation-profile-id': '65537',
                'ssl-profile-nof-whitelist-entries': '0',
                'ssl-profile-profile': 'p1',
                'ssl-profile-root-ca': 'false',
                'ssl-profile-termination-profile-id': '650537',
                'ssl-profile-trace': 'false'
            },
                {
                    'ssl-profile-allow-non-ssl-session': 'true',
                    'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                    'ssl-profile-initiation-profile-id': '65537',
                    'ssl-profile-nof-whitelist-entries': '0',
                    'ssl-profile-profile': 'p1',
                    'ssl-profile-root-ca': 'false',
                    'ssl-profile-termination-profile-id': '65537',
                    'ssl-profile-trace': 'false'
                }
            ]
        }
        }
        }

        self.mocked_obj.execute_as_rpc_command.return_value = response6
        try:
            get_ssl_profile(device=self.mocked_obj, profile="p1")
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")

        response7 = {'ssl-profile-detail': {'ssl-profile-detail': {'ssl-profile-detail-pic':
            [{
                'ssl-profile-allow-non-ssl-session': 'true',
                'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                'ssl-profile-initiation-profile-id': '65537',
                'ssl-profile-nof-whitelist-entries': '0',
                'ssl-profile-profile': 'p1',
                'ssl-profile-root-ca': 'false',
                'ssl-profile-termination-profile-id': '65537',
                'ssl-profile-trace': 'fals2e'
            },
                {
                    'ssl-profile-allow-non-ssl-session': 'true',
                    'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
                    'ssl-profile-initiation-profile-id': '65537',
                    'ssl-profile-nof-whitelist-entries': '0',
                    'ssl-profile-profile': 'p1',
                    'ssl-profile-root-ca': 'false',
                    'ssl-profile-termination-profile-id': '65537',
                    'ssl-profile-trace': 'false'
                }
            ]
        }
        }
        }

        self.mocked_obj.execute_as_rpc_command.return_value = response7
        try:
            get_ssl_profile(device=self.mocked_obj, profile="p1")
        except Exception as err:
            self.assertEqual(err.args[0], "Mismatch in values across PICs")



    def test_get_ssl_initiator_counters(self):
        try:
            get_ssl_initiator_counters()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        try:
            get_ssl_initiator_counters(device=self.mocked_obj, fpc="1")
        except Exception as err:
            self.assertEqual(err.args[0], "Either both or none should be given as arguments : 'fpc' and 'pic'")

        try:
            get_ssl_initiator_counters(device=self.mocked_obj, lsys="LSYS1", tenant='TN1')
        except Exception as err:
            self.assertEqual(err.args[0], "Both'tenant' and 'lsys' should not be passed together")

        response = {'a':1}
        p = patch("jnpr.toby.security.ssl.ssl_operational_cli._get_counters", new=MagicMock(side_effect=[response, response]))
        p.start()

        self.assertEqual(get_ssl_initiator_counters(device=self.mocked_obj, lsys="LSYS1"), response)
        self.assertEqual(get_ssl_initiator_counters(device=self.mocked_obj, tenant="TN1"), response)
        p.stop()



    def test_get_ssl_terminator_counters(self):
        try:
            get_ssl_terminator_counters()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        try:
            get_ssl_terminator_counters(device=self.mocked_obj, fpc="1")
        except Exception as err:
            self.assertEqual(err.args[0], "Either both or none should be given as arguments : 'fpc' and 'pic'")

        try:
            get_ssl_terminator_counters(device=self.mocked_obj, lsys="LSYS1", tenant='TN1')
        except Exception as err:
            self.assertEqual(err.args[0], "Both'tenant' and 'lsys' should not be passed together")

        response = {'a':1}
        p = patch("jnpr.toby.security.ssl.ssl_operational_cli._get_counters", new=MagicMock(side_effect=[response, response]))        
        p.start()
        self.assertEqual(get_ssl_terminator_counters(device=self.mocked_obj, lsys="LSYS1"), response)

        self.assertEqual(get_ssl_terminator_counters(device=self.mocked_obj, tenant="TN1"), response)
        p.stop()



    def test_get_ssl_proxy_counters(self):
        try:
            get_ssl_proxy_counters()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        try:
            get_ssl_proxy_counters(device=self.mocked_obj, fpc="1")
        except Exception as err:
            self.assertEqual(err.args[0], "Either both or none should be given as arguments : 'fpc' and 'pic'")

        try:
            get_ssl_proxy_counters(device=self.mocked_obj, lsys="LSYS1", tenant='TN1')
        except Exception as err:
            self.assertEqual(err.args[0], "Both'tenant' and 'lsys' should not be passed together")

        response = {'a':1}

        p = patch("jnpr.toby.security.ssl.ssl_operational_cli._get_counters", new=MagicMock(side_effect=[response, response]))        
        p.start()
        self.assertEqual(get_ssl_proxy_counters(device=self.mocked_obj, lsys="LSYS1"), response)

        self.assertEqual(get_ssl_proxy_counters(device=self.mocked_obj, tenant="TN1"), response)
        p.stop()



    def test_get_counters(self):


        dct_to_return = {'a' : 2, 'b': 4}

        response = {'ssl-counters':{'ssl-counters':{'ssl-counters-pic':
                                                        {'ssl-counters-pic-info' : 'spu - 5 fpc[1] pic[1]',
                                                         'ssl-counters-name' : ['a', 'b'],
                                                         'ssl-counters-value' : ['2', '4']
                                                         }
                                                    }}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response)


        self.assertEqual(get_ssl_proxy_counters(device=self.mocked_obj, fpc="1", pic="1"), dct_to_return)


        try:
            get_ssl_proxy_counters(device=self.mocked_obj, fpc="1", pic="2")
        except Exception as err:
            self.assertEqual(err.args[0], "Invalid FPC-PIC value, Keyword failing")

        response = {'ssl-counters': {'ssl-counters': {'ssl-counters-pic':
                                                          [{
                                                              'ssl-counters-pic-info': 'spu - 5 fpc[1] pic[1]',
                                                              'ssl-counters-name': ['a', 'b'],
                                                              'ssl-counters-value': ['1', '3']
                                                           },
                                                            {
                                                                  'ssl-counters-pic-info': 'spu - 5 fpc[2] pic[1]',
                                                                  'ssl-counters-name': ['a', 'b'],
                                                                  'ssl-counters-value': ['1', '1']
                                                            }
                                                          ]
                                                      }}}

        self.mocked_obj.execute_as_rpc_command.return_value = response
        self.assertEqual(get_ssl_proxy_counters(device=self.mocked_obj),
                         dct_to_return)

    def test_get_ssl_session_details(self):
        try:
            get_ssl_session_details()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' and 'sessionid' are  mandatory arguments")
			
			
    def test_get_brief_term_profile(self):
        try:
            get_brief_term_profile()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        try:
            get_brief_term_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0],"'profile' is a mandatory argument")
			

    def test_get_detail_term_profile(self):
        try:
            get_detail_term_profile()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        try:
            get_detail_term_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0],"'profile' is a mandatory argument")


    def test_get_all_term_profile(self):
        try:
            get_all_term_profile()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")


    def test_get_all_init_profile(self):
        try:
            get_all_init_profile()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")


    def test_get_brief_init_profile(self):
        try:
            get_brief_init_profile()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        try:
            get_brief_init_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0],"'profile' is a mandatory argument")
			
			
    def test_get_detail_init_profile(self):
        try:
            get_detail_init_profile()
        except Exception as err:
            self.assertEqual(err.args[0],"'device' is a mandatory argument")

        try:
            get_detail_init_profile(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0],"'profile' is a mandatory argument")


if __name__ == '__main__':
    unittest.main()

