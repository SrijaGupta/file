import codecs
from io import StringIO, IOBase
import time
import unittest
from unittest.mock import Mock, patch

from jnpr.toby.hldcl.unix.unix import UnixHost
import jnpr.toby.security.aamw.verify as verify
import jnpr.toby.security.aamw.util.helper_util as helper

ARGON_TELEMETRY_STR = 'Dec  9 08:44:45 !!!!DEBUG!!!!aamwd_json_utils.c: ' \
                      'http vlue in building telemetry string: aamw.http' \
                      '.objs_blocked: 0, aamw.http.objs_permitted: 0\nDec' \
                      '  9 08:44:45 !!!!DEBUG!!!!aamwd_json_utils.c: http' \
                      's vlue in building telemetry string: aamw.https.obj' \
                      's_blocked: 0, aamw.https.objs_permitted: 0\nDec  9 ' \
                      '08:44:45 telemetry_string: \n\nDec  9 08:44:45 {"' \
                      'aamw":{"global_config_version":1512377229,"fast_che' \
                      'ck_data\nDec  9 08:44:45 _version":1512273977,"prof' \
                      'ile_config_version":1492713795,"gl\nDec  9 08:44:45 o' \
                      'bal_whitelist_version":1502233772,"global_blacklist_v' \
                      'ersion\nDec  9 08:44:45 ":1502233837,"customer_whitel' \
                      'ist_version":1512726864,"custom\nDec  9 08:44:45 er_b' \
                      'lacklist_version":1512726865,"wl-hits":0,"bl-hits":0,' \
                      '"ob\nDec  9 08:44:45 js_scored":0,"objs_ns":0,"objs_f' \
                      'ailed":0,"smtp-wl-hits":0,"s\nDec  9 08:44:45 mtp-bl-' \
                      'hits":0,"imap-wl-hits":0,"imap-bl-hits":0,"smtp_objs_' \
                      '\nDec  9 08:44:45 scored":0,"smtp_objs_ns":0,"smtp_o' \
                      'bjs_failed":0,"imap_objs_s\nDec  9 08:44:45 cored":0' \
                      ',"imap_objs_ns":0,"imap_objs_failed":0,"quarantine_o' \
                      '\nDec  9 08:44:45 bjs_processed":0,"quarantine_objs_n' \
                      's":0,"quarantine_objs_fai\nDec  9 08:44:45 led":0,"su' \
                      'bm_conn_failed":0,"cc_conn_failed":0,"control_conn\nD' \
                      'ec  9 08:44:45 _failed":0,"control_conn_active":1,"su' \
                      'bm_conn_active":0,"cc_\nDec  9 08:44:45 conn_active":' \
                      '0,"fast_check_verdicts":0,"magic_check_verdicts\nDec ' \
                      ' 9 08:44:45 ":0,"category_data":[{"name":"executable"' \
                      ',"objs_scanned":0,"\nDec  9 08:44:45 objs_blocked":0,' \
                      '"objs_skipped":0,"objs_ignored":0},{"name":"\nDec  9 ' \
                      '08:44:45 pdf","objs_scanned":0,"objs_blocked":0,"objs' \
                      '_skipped":0,"obj\nDec  9 08:44:45 s_ignored":0},{"nam' \
                      'e":"document","objs_scanned":0,"objs_bloc\nDec  9 08:' \
                      '44:45 ked":0,"objs_skipped":0,"objs_ignored":0},{"nam' \
                      'e":"archive",\nDec  9 08:44:45 "objs_scanned":0,"objs' \
                      '_blocked":0,"objs_skipped":0,"objs_ign\nDec  9 08:44:' \
                      '45 ored":0},{"name":"script","objs_scanned":0,"objs_b' \
                      'locked":0,\nDec  9 08:44:45 "objs_skipped":0,"objs_ig' \
                      'nored":0},{"name":"rich_app","objs_\nDec  9 08:44:45 ' \
                      'scanned":0,"objs_blocked":0,"objs_skipped":0,"objs_ig' \
                      'nored":\nDec  9 08:44:45 0},{"name":"library","objs_s' \
                      'canned":0,"objs_blocked":0,"objs\nDec  9 08:44:45 _s' \
                      'kipped":0,"objs_ignored":0},{"name":"java","objs_sca' \
                      'nned":\nDec  9 08:44:45 0,"objs_blocked":0,"objs_ski' \
                      'pped":0,"objs_ignored":0},{"name\nDec  9 08:44:45 ":' \
                      '"os_package","objs_scanned":0,"objs_blocked":0,"objs' \
                      '_skipp\nDec  9 08:44:45 ed":0,"objs_ignored":0},{"na' \
                      'me":"code","objs_scanned":0,"obj\nDec  9 08:44:45 s_' \
                      'blocked":0,"objs_skipped":0,"objs_ignored":0},{"name' \
                      '":"med\nDec  9 08:44:45 ia","objs_scanned":0,"objs_' \
                      'blocked":0,"objs_skipped":0,"objs\nDec  9 08:44:45 ' \
                      '_ignored":0},{"name":"config","objs_scanned":0,"obj' \
                      's_blocked\nDec  9 08:44:45 ":0,"objs_skipped":0,"obj' \
                      's_ignored":0},{"name":"mobile","obj\nDec  9 08:44:45 ' \
                      's_scanned":0,"objs_blocked":0,"objs_skipped":0,"objs_' \
                      'ignored\nDec  9 08:44:45 ":0},{"name":"emerging_threa' \
                      't","objs_scanned":0,"objs_blocke\nDec  9 08:44:45 d":' \
                      '0,"objs_skipped":0,"objs_ignored":0},{"name":"other",' \
                      '"obj\nDec  9 08:44:45 s_scanned":0,"objs_blocked":0,"' \
                      'objs_skipped":0,"objs_ignored\nDec  9 08:44:45 ":0}],' \
                      '"http":{"objs_scanned":0,"objs_blocked":0,"objs_permi' \
                      't\nDec  9 08:44:45 ted":0,"objs_ignored":0,"blacklist' \
                      '_hits":0,"whitelist_hits":\nDec  9 08:44:45 0},"https' \
                      '":{"objs_scanned":0,"objs_blocked":0,"objs_permitte\n' \
                      'Dec  9 08:44:45 d":0,"objs_ignored":0,"blacklist_hits' \
                      '":0,"whitelist_hits":0}\nDec  9 08:44:45 ,"smtp":{"ob' \
                      'js_scanned":0,"objs_quarantined":0,"objs_tagged"\nDec' \
                      '  9 08:44:45 :0,"objs_permitted":0,"blacklist_hits":' \
                      '0,"whitelist_hits":0}\nDec  9 08:44:45 ,"smtps":{"ob' \
                      'js_scanned":0,"objs_quarantined":0,"objs_tagged\nDe' \
                      'c  9 08:44:45 ":0,"objs_permitted":0,"blacklist_hit' \
                      's":0,"whitelist_hits":0\nDec  9 08:44:45 },"imap":{' \
                      '"objs_scanned":0,"objs_blocked":0,"objs_permitted"' \
                      '\nDec  9 08:44:45 :0,"blacklist_hits":0,"whitelist_h' \
                      'its":0},"imaps":{"objs_sca\nDec  9 08:44:45 nned":0,' \
                      '"objs_blocked":0,"objs_permitted":0,"blacklist_hits' \
                      '"\nDec  9 08:44:45 :0,"whitelist_hits":0},"fallback' \
                      '_reasons":{"verdict_timeout"\nDec  9 08:44:45 :0,"' \
                      'submission_timeout":0,"rate_limit":0}},"system":{"' \
                      'os":"J\nDec  9 08:44:45 NPR-11.0-20171101.093825_f' \
                      'bsd-","hw":"srx1500","sn":"P1C_000\nDec  9 08:44:4' \
                      '5 00065","ha":"no","hn":"argon-forge-08"},"telemet' \
                      'ry_schema_ve\nDec  9 08:44:45 rsion":2}\n'
INCOMPLETE_ARGON_TELEMETRY_STR = 'Dec  9 08:44:45 !!!!DEBUG!!!!aamwd_json_utils.c: ' \
                      'http vlue in building telemetry string: aamw.http' \
                      '.objs_blocked: 0, aamw.http.objs_permitted: 0\nDec' \
                      '  9 08:44:45 !!!!DEBUG!!!!aamwd_json_utils.c: http' \
                      's vlue in building telemetry string: aamw.https.obj' \
                      's_blocked: 0, aamw.https.objs_permitted: 0\nDec  9 ' \
                      '08:44:45 telemetry_string: \n\nDec  9 08:44:45 {"' \
                      'aamw":{"global_config_version":1512377229,"fast_che' \
                      'ck_data\nDec  9 08:44:45 _version":1512273977,"prof' \
                      'ile_config_version":1492713795,"gl\nDec  9 08:44:45 o' \
                      'bal_whitelist_version":1502233772,"global_blacklist_v' \
                      'ersion\nDec  9 08:44:45 ":1502233837,"customer_whitel' \
                      'ist_version":1512726864,"custom\nDec  9 08:44:45 er_b' \
                      'lacklist_version":1512726865,"wl-hits":0,"bl-hits":0,' \
                      '"ob\nDec  9 08:44:45 js_scored":0,"objs_ns":0,"objs_f' \
                      'ailed":0,"smtp-wl-hits":0,"s\nDec  9 08:44:45 mtp-bl-' \
                      'hits":0,"imap-wl-hits":0,"imap-bl-hits":0,"smtp_objs_' \
                      '\nDec  9 08:44:45 scored":0,"smtp_objs_ns":0,"smtp_o' \
                      'bjs_failed":0,"imap_objs_s\nDec  9 08:44:45 cored":0' \
                      ',"imap_objs_ns":0,"imap_objs_failed":0,"quarantine_o' \
                      '\nDec  9 08:44:45 bjs_processed":0,"quarantine_objs_n' \
                      's":0,"quarantine_objs_fai\nDec  9 08:44:45 led":0,"su' \
                      'bm_conn_failed":0,"cc_conn_failed":0,"control_conn\nD' \
                      'ec  9 08:44:45 _failed":0,"control_conn_active":1,"su' \
                      'bm_conn_active":0,"cc_\nDec  9 08:44:45 conn_active":' \
                      '0,"fast_check_verdicts":0,"magic_check_verdicts\nDec ' \
                      ' 9 08:44:45 ":0,"category_data":[{"name":"executable"' \
                      ',"objs_scanned":0,"\nDec  9 08:44:45 objs_blocked":0,' \
                      '"objs_skipped":0,"objs_ignored":0},{"name":"\nDec  9 ' \
                      '08:44:45 pdf","objs_scanned":0,"objs_blocked":0,"objs' \
                      '_skipped":0,"obj\nDec  9 08:44:45 s_ignored":0},{"nam' \
                      'e":"document","objs_scanned":0,"objs_bloc\nDec  9 08:' \
                      '44:45 ked":0,"objs_skipped":0,"objs_ignored":0},{"nam' \
                      'e":"archive",\nDec  9 08:44:45 "objs_scanned":0,"objs' \
                      '_blocked":0,"objs_skipped":0,"objs_ign\nDec  9 08:44:' \
                      '45 ored":0},{"name":"script","objs_scanned":0,"objs_b' \
                      'locked":0,\nDec  9 08:44:45 "objs_skipped":0,"objs_ig' \
                      'nored":0},{"name":"rich_app","objs_\nDec  9 08:44:45 ' \
                      'scanned":0,"objs_blocked":0,"objs_skipped":0,"objs_ig' \
                      'nored":\nDec  9 08:44:45 0},{"name":"library","objs_s' \
                      'canned":0,"objs_blocked":0,"objs\nDec  9 08:44:45 _s' \
                      'kipped":0,"objs_ignored":0},{"name":"java","objs_sca' \
                      'nned":\nDec  9 08:44:45 0,"objs_blocked":0,"objs_ski' \
                      'pped":0,"objs_ignored":0},{"name\nDec  9 08:44:45 ":' \
                      '"os_package","objs_scanned":0,"objs_blocked":0,"objs' \
                      '_skipp\nDec  9 08:44:45 ed":0,"objs_ignored":0},{"na' \
                      'me":"code","objs_scanned":0,"obj\nDec  9 08:44:45 s_' \
                      'blocked":0,"objs_skipped":0,"objs_ignored":0},{"name' \
                      '":"med\nDec  9 08:44:45 ia","objs_scanned":0,"objs_' \
                      'blocked":0,"objs_skipped":0,"objs\nDec  9 08:44:45 ' \
                      '_ignored":0},{"name":"config","objs_scanned":0,"obj' \
                      's_blocked\nDec  9 08:44:45 ":0,"objs_skipped":0,"obj' \
                      's_ignored":0},{"name":"mobile","obj\nDec  9 08:44:45 ' \
                      's_scanned":0,"objs_blocked":0,"objs_skipped":0,"objs_' \
                      'ignored\nDec  9 08:44:45 ":0},{"name":"emerging_threa' \
                      't","objs_scanned":0,"objs_blocke\nDec  9 08:44:45 d":' \
                      '0,"objs_skipped":0,"objs_ignored":0},{"name":"other",' \
                      '"obj\nDec  9 08:44:45 s_scanned":0,"objs_blocked":0,"' \
                      'objs_skipped":0,"objs_ignored\nDec  9 08:44:45 ":0}],' \
                      '"http":{"objs_scanned":0,"objs_blocked":0,"objs_permi' \
                      't\nDec  9 08:44:45 ted":0,"objs_ignored":0,"blacklist' \
                      '_hits":0,"whitelist_hits":\nDec  9 08:44:45 0},"https' \
                      '":{"objs_scanned":0,"objs_blocked":0,"objs_permitte\n' \
                      'Dec  9 08:44:45 d":0,"objs_ignored":0,"blacklist_hits' \
                      '":0,"whitelist_hits":0}\nDec  9 08:44:45 ,"smtp":{"ob' \
                      'js_scanned":0,"objs_quarantined":0,"objs_tagged"\nDec' \
                      '  9 08:44:45 :0,"objs_permitted":0,"blacklist_hits":' \
                      '0,"whitelist_hits":0}\nDec  9 08:44:45 ,"smtps":{"ob'

SECINTEL_FEED_DL_STATUS = "Category name   :CC\nFeed name     :cc_ip_data\n \
                          Version       :20200427.14\n \
                          Objects number:47411\n \
                          Create time   :2020-04-29 13:09:26 PDT\n \
                          Update time   :2020-04-29 13:35:32 PDT\n \
                          Update status :Store succeeded\n \
                          Expired       :No\n \
                          Options       :N/A"

SECINTEL_FEED_DL_STATUS_FAIL = "Category name   :CC\nFeed name     :cc_ip_data\n \
                               Version       :20200427.14\n \
                               Objects number:47411\n \
                               Create time   :2020-04-29 13:09:26 PDT\n \
                               Update time   :2020-04-29 13:35:32 PDT\n \
                               Update status :Storing\n \
                               Expired       :No\n \
                               ptions       :N/A"

SECINTEL_STATS = "Logical system: root-logical-system\n \
                 Category CC:\n \
                   Profile cc_profile:\n \
                    Total processed sessions: 243560\n \
                    Permit sessions:          2\n \
                    Block drop sessions:      0\n \
                    Block close sessions:     0\n \
                    Close redirect sessions:  0"

SECINTEL_DA = "show security dynamic-address category-name Whitelist\n \
              No.     IP-start             IP-end               Feed             Address\n \
              1       2.0.0.243            2.0.0.243            Whitelist/2      ID-80004020\n \
              \n \
              Instance default Total number of matching entries: 1"

SECINTEL_DA_NONE = "show security dynamic-address category-name CC\n \
                   \n \
                   Instance default Total number of matching entries: 0"

class MockResponse(object):
    def __init__(self, response):
        self.s = response

    def response(self):
        return self.s


def mock_io(s):
    def mock_io_func(*args, **kwargs):
        return StringIO(s)
    return mock_io_func


class TestVerify(unittest.TestCase):

    def setUp(self):
        self.handle = Mock(spec=UnixHost)
        self.handle.log = Mock()
        self.handle.download = Mock()
        self.handle.su = Mock()

        self.codecs_open_orig = codecs.open
        self.time_time_orig = time.time
        self.sleep_orig = helper.sleep
        self.get_vty_cmd_prefix_orig = helper.get_vty_cmd_prefix

        helper.get_vty_cmd_prefix = Mock(return_value='abc')
        helper.sleep = Mock()

    def tearDown(self):
        codecs.open = self.codecs_open_orig
        time.time = self.time_time_orig
        helper.sleep = self.sleep_orig
        helper.get_vty_cmd_prefix = self.get_vty_cmd_prefix_orig

    def test_get_vty_web_xlist_cnt(self):
        self.handle.shell = Mock(return_value=MockResponse(
            'HTTP:\n1\n2\n3\n5\n6\n7\n8\n9'))
        self.assertIsNotNone(verify.get_vty_web_xlist_cnt(self.handle))

        self.handle.shell = Mock(return_value=MockResponse(
            'n1\n2\n3\n5\n6\n7\n8\n9'))
        with self.assertRaises(ValueError):
            self.assertIsNotNone(verify.get_vty_web_xlist_cnt(self.handle))

    def test_get_vty_category_cnt(self):
        self.handle.shell = Mock(return_value=MockResponse(
            '----\nFile category counters\nFile Hash counters\nCategory  abc\n'
            'xyz: 123\ndef 3'))
        self.assertIsNotNone(verify.get_vty_category_cnt(self.handle))

    def test_get_vty_application_cnt(self):
        self.handle.shell = Mock(return_value=MockResponse(
            '----\nApplication AAA\nAAA AAA: 123'))
        self.assertIsNotNone(verify.get_vty_application_cnt(self.handle))

    def test_get_trace_telemetry_json(self):

        codecs.open = mock_io(ARGON_TELEMETRY_STR)
        self.assertIsNotNone(verify.get_trace_telemetry_json(self.handle,
                                                             "", 3))
        codecs.open = mock_io(INCOMPLETE_ARGON_TELEMETRY_STR)
        with self.assertRaises(TimeoutError):
            verify.get_trace_telemetry_json(self.handle, "", 0.01)

    def test_verify_telemetry_item(self):
        self.handle.cli = Mock()
        codecs.open = mock_io(ARGON_TELEMETRY_STR)

        self.assertIs(verify.verify_telemetry_item(
            self.handle, '', ['aamw', 'smtps', 'objs_scanned'], 0,
            timeout=0.01), True)

        codecs.open = mock_io(INCOMPLETE_ARGON_TELEMETRY_STR)

        with self.assertRaises(TimeoutError):
            verify.verify_telemetry_item(
                self.handle, '', ['aamw', 'smtps', 'objs_scanned'], 0,
                timeout=0.01)

    def test_get_ha_dynamic_address(self):
        self.handle.cli = Mock(return_value=MockResponse('a\n1 2 3 4 5'))
        self.assertIsNotNone(verify.get_ha_dynamic_address(
            self.handle, '1', '1'))

    def test_is_ip_in_db_file(self):
        self.handle.shell = Mock(return_value=MockResponse(
            '#add\n1'))
        self.assertIs(verify.is_ip_in_db_file(self.handle, '0.0.0.1'), True)
        self.assertIs(verify.is_ip_in_db_file(self.handle, '0.0.0.2'), False)

    def test_verify_ip_in_ha(self):
        orig_is_ip_in_db = verify.is_ip_in_db_file
        orig_get_ha_dynamic_address = verify.get_ha_dynamic_address

        try:
            verify.is_ip_in_db_file = Mock(return_value=True)
            verify.get_ha_dynamic_address = Mock(return_value=True)

            self.assertIs(verify.verify_ip_in_ha(
                self.handle, '1.1.1.1', 0.01), True)

            verify.is_ip_in_db_file = Mock(return_value=False)
            verify.get_ha_dynamic_address = Mock(return_value=False)

            with self.assertRaises(TimeoutError):
                verify.verify_ip_in_ha(self.handle, '1.1.1.1', 0.01)
        finally:
            verify.is_ip_in_db_file = orig_is_ip_in_db
            verify.get_ha_dynamic_address = orig_get_ha_dynamic_address

    def test_verify_secintel_feed_download(self):
        self.handle.cli = Mock(return_value=MockResponse(
            SECINTEL_FEED_DL_STATUS))
        self.assertIs(verify.verify_secintel_feed_download(self.handle, category="CC", feed="cc_ip_data"), True)

        self.handle.cli = Mock(return_value=MockResponse(
            SECINTEL_FEED_DL_STATUS_FAIL))
        self.assertIs(verify.verify_secintel_feed_download(self.handle, category="CC", feed="cc_ip_data"), False)

    def test_verify_secintel_stats(self):
        self.handle.cli = Mock(return_value=MockResponse(
            SECINTEL_STATS))

        self.assertIs(verify.verify_secintel_stats(self.handle, profile="cc_profile", action="permit"), True)
        self.assertIs(verify.verify_secintel_stats(self.handle, profile="cc_profile", action="block drop"), False)
        self.assertIsNotNone(verify.verify_secintel_stats(self.handle, profile="cc_profile", action="no action"))

    def test_verify_da_feed_loaded(self):
        self.handle.cli = Mock(return_value=MockResponse(
            SECINTEL_DA))

        self.assertIs(verify.verify_da_feed_loaded(self.handle, category="Whitelist"), True)

        self.handle.cli = Mock(return_value=MockResponse(
            SECINTEL_DA_NONE))

        self.assertIs(verify.verify_da_feed_loaded(self.handle, category="CC"), False)

if __name__ == '__main__':
    unittest.main()
