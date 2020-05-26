from mock import patch
import unittest2 as unittest
from mock import MagicMock
import jxmlease
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.system.license.License import _validate_license_install, add_license_file, add_license_terminal, \
    delete_license, save_license_keys, configure_license_traceoptions, show_license, get_license_installed, \
    get_license_usage, get_id_from_key, get_license_identifiers, check_license_directory, verify_license_installed, \
    verify_license_usage, verify_utm_license_status


# To return response of cli() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()

    def test_validate_license_install(self):

        self.assertEqual(
            _validate_license_install(
                device=self.mocked_obj,
                response=" successfully added ",
                expected_status="success"),
            None)
        self.assertEqual(
            _validate_license_install(
                device=self.mocked_obj,
                response="  warning license already exists.* ",
                expected_status="exists"),
            None)
        self.assertEqual(
            _validate_license_install(
                device=self.mocked_obj,
                response=" invalid license data  ",
                expected_status="failure"),
            None)
        self.assertEqual(
            _validate_license_install(
                device=self.mocked_obj,
                response=" ",
                expected_status="failure"),
            None)

        try:
            _validate_license_install(
                device=self.mocked_obj, response=" ", expected_status="success")
        except Exception as err:
            self.assertEqual(err.args[0], "Failed to add license")

        try:
            _validate_license_install(
                device=self.mocked_obj, response=" ", expected_status="exists")
        except Exception as err:
            self.assertEqual(err.args[0], "License already exists message missing")

        try:
            _validate_license_install(
                device=self.mocked_obj,
                response=" successfully added ",
                expected_status="failure")
        except Exception as err:
            self.assertEqual(err.args[0], "License load is successful when failure expected")

    def test_add_license_file(self):

        try:
            add_license_file()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle or filename argument")

        p = patch("jnpr.toby.system.license.License._validate_license_install", new=MagicMock())
        p.start()

        r = Response("successfully added")
        rout = "successfully added"
        self.mocked_obj.cli = MagicMock(return_value=r)
        self.assertEqual(
            add_license_file(
                device=self.mocked_obj,
                filename="/tmp/abc.license",
                expected_status="success"),
            rout)

        p.stop()

    def test_add_license_terminal(self):

        try:
            add_license_terminal()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle or key argument")

        p = patch("jnpr.toby.system.license.License._validate_license_install", new=MagicMock())
        p.start()

        r = Response("successfully added")
        rout = "successfully added"
        self.mocked_obj.cli = MagicMock(return_value=r)
        self.assertEqual(
            add_license_terminal(
                device=self.mocked_obj,
                key="xyz",
                expected_status="success"),
            rout)

        p.stop()

    def test_delete_license(self):

        try:
            delete_license()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle or key identifiers argument")

        try:
            delete_license(device=self.mocked_obj, key_identifiers=" ")
        except Exception as err:
            self.assertEqual(err.args[0], "Keyidentifier has to be list")

        lst = []
        try:
            delete_license(device=self.mocked_obj, key_identifiers=lst)
        except Exception as err:
            self.assertEqual(err.args[0], "Size of key identifier list is zero")

        lst.append("abc")
        r = Response("license key does not exist")
        rout = "license key does not exist"
        self.mocked_obj.cli = MagicMock(return_value=r)
        self.assertEqual(delete_license(device=self.mocked_obj, key_identifiers=lst), rout)

        lst.append("abc")
        r = Response("deleted")
        rout = "deleted"
        self.mocked_obj.cli.return_value = r
        self.assertEqual(delete_license(device=self.mocked_obj, key_identifiers=lst), rout)

    def test_save_license_keys(self):

        try:
            save_license_keys()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle argument")

        r = Response("Wrote lines of license data")
        self.mocked_obj.cli = MagicMock(return_value=r)
        self.assertEqual(
            save_license_keys(
                device=self.mocked_obj,
                filename="/tmp/abc.license"),
            "Wrote lines of license data")

        r = "abc"
        self.mocked_obj.cli.return_value = r
        self.assertEqual(save_license_keys(device=self.mocked_obj), "abc")

        r = Response("")
        self.mocked_obj.cli.return_value = r
        try:
            save_license_keys(device=self.mocked_obj, filename="/tmp/abc.license")
        except Exception as err:
            self.assertEqual(err.args[0], "Failed to save license")

    def test_configure_license_traceoptions(self):

        try:
            configure_license_traceoptions()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing filename or device handle argument")

        self.mocked_obj.config = MagicMock()
        self.mocked_obj.commit = MagicMock()

        self.assertEqual(configure_license_traceoptions(
            device=self.mocked_obj, filename="/tmp/abc.license"), None)
        self.assertEqual(
            configure_license_traceoptions(
                device=self.mocked_obj,
                filename="/tmp/abc.license",
                mode="delete"),
            None)

    def test_show_license(self):
        try:
            show_license()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle argument")
        r = "abc"
        self.mocked_obj.cli = MagicMock(return_value=r)
        self.assertEqual(
            show_license(
                device=self.mocked_obj, what="usage"), r)
        self.assertEqual(
            show_license(
                device=self.mocked_obj, what="installed"), r)
        self.assertEqual(
            show_license(
                device=self.mocked_obj, what="keys"), r)
        self.assertEqual(
            show_license(
                device=self.mocked_obj), r)

    @patch('jnpr.toby.system.license.License.get_license_installed')
    def test_get_license_identifiers(self, patched_get):
        try:
            get_license_identifiers()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle argument")

        try:
            get_license_identifiers(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Missing feature_name argument")

        patched_get.return_value = [{'name': "123",
                                     'feature-block': {
                                         'feature': {'name': "idp", 'validity-information': {'end-date': "24041993"}}},
                                     'license-state': "valid",
                                     'license-version': "1",
                                     }, {'name': "456",
                                         'feature-block': {'feature': {'name': "idp", 'validity-information': {
                                             'end-date': "24041993"}}},
                                         'license-state': "valid",
                                         'license-version': "1",
                                         }]

        self.assertEqual(get_license_identifiers(device=self.mocked_obj, feature_name="idp", validate=False),
                         ["123", "456"])

        try:
            get_license_identifiers(device=self.mocked_obj, feature_name="sig", validate=True)
        except Exception as err:
            self.assertEqual(err.args[0], "Licensed feature : sig not found")

    def test_check_license_directory_exception(self):
        try:
            check_license_directory()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle argument")

        try:
            check_license_directory(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Missing license_id which is mandatory")

    def test_check_license_directory(self):

        r = Response("170412921")
        rout = "170412921"
        self.mocked_obj.shell = MagicMock(return_value=r)
        self.assertEqual(check_license_directory(device=self.mocked_obj, license_id="170412921", file_exist="yes"),
                         rout)
        try:
            check_license_directory(device=self.mocked_obj, license_id="170412421", file_exist="yes")
        except Exception as err:
            self.assertEqual(err.args[0], "File : 170412421 not found")

        try:
            check_license_directory(device=self.mocked_obj, license_id="170412921", file_exist="no")
        except Exception as err:
            self.assertEqual(err.args[0], "File : 170412921 found")

        o = Response("")
        out = ""
        self.mocked_obj.shell = MagicMock(return_value=o)
        self.assertEqual(check_license_directory(device=self.mocked_obj, license_id="170412921", file_exist="no"), out)

    def test_get_id_from_key_exception(self):
        try:
            get_id_from_key()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle argument")

        try:
            get_id_from_key(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "key is a mandatory argument")

    def test_get_id_from_key(self):

        self.assertEqual(get_id_from_key(device=self.mocked_obj, key="akjs ;981100790; dsaf"), "981100790")

        try:
            get_id_from_key(device=self.mocked_obj, key="bsac873qgc9")
        except Exception as err:
            self.assertEqual(err.args[0], "Not able to fetch ID")

    def test_verify_license_installed_exception(self):
        try:
            verify_license_installed()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle argument")

        try:
            verify_license_installed(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Missing license_id which is mandatory")

    @patch('jnpr.toby.system.license.License.get_license_installed')
    def test_verify_license_installed(self, patched_get):

        patched_get.return_value = [{'name': "123",
                                     'feature-block': {
                                         'feature': {'name': "idp", 'validity-information': {'end-date': "24041993"}}},
                                     'license-state': "valid",
                                     'license-version': "1",
                                     }, {'name': "456",
                                         'feature-block': {'feature': {'name': "idp", 'validity-information': {
                                             'end-date': "24041993"}}},
                                         'license-state': "valid",
                                         'license-version': "1",
                                         }]

        self.assertEqual(verify_license_installed(device=self.mocked_obj, license_id="123", feature_name="idp",
                                                  license_state="valid", license_version="1",
                                                  license_expiry="24041993"), True)

        try:
            verify_license_installed(device=self.mocked_obj, license_id="456",
                                     feature_name="iadp", license_state="valaid",
                                     license_version="12", license_expiry="240419293")
        except Exception as err:
            self.assertEqual(err.args[0], "Verify license installed failed")

        try:
            verify_license_installed(device=self.mocked_obj, license_id="4156",
                                     feature_name="iadp", license_state="valaid",
                                     license_version="12", license_expiry="240419293")
        except Exception as err:
            self.assertEqual(err.args[0], "License Identifier : 4156 not found")

    def test_verify_license_usage_exception(self):
        try:
            verify_license_usage()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle argument")

        try:
            verify_license_usage(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Missing license_name argument")

        try:
            verify_license_usage(device=self.mocked_obj, feature_name="idp")
        except Exception as err:
            self.assertEqual(err.args[0], "Missing license_used or license_needed or license_installed argument")

    @patch('jnpr.toby.system.license.License.get_license_usage')
    def test_verify_license_usage(self, patched_get):

        patched_get.return_value = [{'name': "idp",
                                     'used-licensed': "1",
                                     'needed': "0",
                                     'licensed': "2"},
                                    {'name': "idp1",
                                     'used-licensed': "1",
                                     'needed': "0",
                                     'licensed': "2"}
                                    ]

        self.assertEqual(
            verify_license_usage(device=self.mocked_obj, feature_name="idp", license_used="1", license_installed="2",
                                 license_needed="0"), True)

        try:
            verify_license_usage(device=self.mocked_obj, feature_name="idp1",
                                 license_used="12", license_installed="22",
                                 license_needed="02")
        except Exception as err:
            self.assertEqual(err.args[0], "Verify license usage failed")

        try:
            verify_license_usage(device=self.mocked_obj, feature_name="idp21",
                                 license_used="12", license_installed="22",
                                 license_needed="02")
        except Exception as err:
            self.assertEqual(err.args[0], "License for : idp21 not found")

    def test_verify_utm_license_status(self):
        try:
            verify_utm_license_status()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            verify_utm_license_status(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'utm_feature' is a mandatory argument")

        lst = [Response(""), Response(""), Response(""), Response("")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)

        try:
            verify_utm_license_status(device=self.mocked_obj, utm_feature="anti-virus", license_valid=False)
        except Exception as err:
            self.assertEqual(err.args[0], "Antivirus Update not disabled in case of Invalid license")

        lst = [Response("update disabled due to license invalidity"), Response(""), Response(""), Response("")]
        self.mocked_obj.cli.side_effect = lst

        try:
            verify_utm_license_status(device=self.mocked_obj, utm_feature="anti-virus", license_valid=False)
        except Exception as err:
            self.assertEqual(err.args[0], "Antivirus alarm not active in case of Invalid license")

        lst = [Response("update disabled due to license invalidity"),
               Response("Anti Virus with Sophos Engine usage requires a license"), Response(""), Response("")]
        self.mocked_obj.cli.side_effect = lst

        try:
            verify_utm_license_status(device=self.mocked_obj, utm_feature="anti-virus",
                                      license_valid=False)
        except Exception as err:
            self.assertEqual(err.args[0], "Update not disabled in case of Invalid license")

        lst = [Response("update disabled due to license invalidity"),
               Response("Anti Virus with Sophos Engine usage requires a license"), Response(""),
               Response("license invalidity")]
        self.mocked_obj.cli.side_effect = lst

        try:
            verify_utm_license_status(device=self.mocked_obj, utm_feature="anti-virus",
                                      license_valid=True)
        except Exception as err:
            self.assertEqual(err.args[0], "Antivirus status showing disabled in case of Valid license")

        lst = [Response(""),
               Response("Anti Virus with Sophos Engine usage requires a license"), Response(""),
               Response("license invalidity")]
        self.mocked_obj.cli.side_effect = lst

        try:
            verify_utm_license_status(device=self.mocked_obj, utm_feature="anti-virus",
                                      license_valid=True)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Antivirus alarm active in case of Valid license")

        lst = [Response(""),
               Response(""), Response(""),
               Response("license invalidity")]
        self.mocked_obj.cli.side_effect = lst

        try:
            verify_utm_license_status(device=self.mocked_obj, utm_feature="anti-virus",
                                      license_valid=True)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Update disabled in case of Valid license")

        lst = [Response(""),
               Response(""), Response(""),
               Response("")]
        self.mocked_obj.cli.side_effect = lst
        self.assertEqual(verify_utm_license_status(device=self.mocked_obj, utm_feature="anti-virus",
                                                   license_valid=True), True)

        lst = [Response("update disabled due to license invalidity"),
               Response("Anti Virus with Sophos Engine usage requires a license"), Response(""),
               Response("license invalidity")]
        self.mocked_obj.cli.side_effect = lst

        self.assertEqual(
            verify_utm_license_status(device=self.mocked_obj, utm_feature="anti-virus",
                                      license_valid=False), True)

        ## web filtering starts here
        lst = [Response("Server status: UP "), Response("Web Filtering EWF usage requires a license")]
        self.mocked_obj.cli.side_effect = lst
        try:
            verify_utm_license_status(device=self.mocked_obj, utm_feature="web-filtering",
                                      license_valid=False)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Web Filtering Status shows UP in case of Invalid license")

        lst = [Response(""),
               Response("")]
        self.mocked_obj.cli.side_effect = lst
        try:
            verify_utm_license_status(device=self.mocked_obj,
                                      utm_feature="web-filtering",
                                      license_valid=False)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Web filtering alarm not active in case of Invalid license")

        lst = [Response(""),
               Response("")]
        self.mocked_obj.cli.side_effect = lst
        try:
            verify_utm_license_status(device=self.mocked_obj,
                                      utm_feature="web-filtering",
                                      license_valid=True)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Web Filtering Status does not show UP in case of Valid license")

        lst = [Response("Server status: UP "),
               Response("Web Filtering EWF usage requires a license")]
        self.mocked_obj.cli.side_effect = lst
        try:
            verify_utm_license_status(device=self.mocked_obj,
                                      utm_feature="web-filtering",
                                      license_valid=True)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Web filtering alarm active in case of valid license")

        lst = [Response(""),
               Response("Web Filtering EWF usage requires a license")]
        self.mocked_obj.cli.side_effect = lst
        self.assertEqual(verify_utm_license_status(device=self.mocked_obj,
                                                   utm_feature="web-filtering",
                                                   license_valid=False), True)
        ####Anti spam starts here

        lst = [Response("Anti-Spam usage requires a license")]
        self.mocked_obj.cli.side_effect = lst
        try:
            verify_utm_license_status(device=self.mocked_obj,
                                      utm_feature="anti-spam",
                                      license_valid=False)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Anti Spam statistics are Non Zero in case of Invalid license")

        lst = [Response("")]
        self.mocked_obj.cli.side_effect = lst
        try:
            verify_utm_license_status(device=self.mocked_obj,
                                      utm_feature="anti-spam",
                                      license_valid=False)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Anti-spam alarm not active in case of Invalid license")

        lst = [Response("Anti-Spam usage requires a license")]
        self.mocked_obj.cli.side_effect = lst
        try:
            verify_utm_license_status(device=self.mocked_obj,
                                      utm_feature="anti-spam",
                                      license_valid=True)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Anti-spam alarm active in case of valid license")

        lst = [Response("")]
        self.mocked_obj.cli.side_effect = lst
        self.assertEqual(verify_utm_license_status(device=self.mocked_obj,
                                                   utm_feature="anti-spam",
                                                   license_valid=True), True)

        lst = [Response("Anti-Spam usage requires a license")]
        self.mocked_obj.cli.side_effect = lst
        self.assertEqual(verify_utm_license_status(device=self.mocked_obj,
                                                   utm_feature="anti-spam",
                                                   license_valid=False), True)

        try:
            verify_utm_license_status(device=self.mocked_obj, utm_feature="abc")
        except Exception as err:
            self.assertEqual(err.args[0], "Invalid utm_feature name")

    def test_get_license_installed(self):
        try:
            get_license_installed()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle argument")

        dict_to_return = {'license-information':
                              {'license': 1}
                          }

        dict_to_return_2 = {'license-information':
                                {'license': [1]}
                            }
        self.mocked_obj.get_rpc_equivalent = MagicMock()
        self.mocked_obj.execute_rpc = MagicMock()
        jxmlease.parse_etree = MagicMock(return_value=dict_to_return)

        self.assertEqual(get_license_installed(device=self.mocked_obj), [1])
        jxmlease.parse_etree = MagicMock(return_value=dict_to_return_2)
        self.assertEqual(get_license_installed(device=self.mocked_obj), [1])

    def test_get_license_usage(self):
        try:
            get_license_usage()
        except Exception as err:
            self.assertEqual(err.args[0], "Missing device handle argument")

        dict_to_return = {'license-usage-summary':
                              {'feature-summary': 1}
                          }

        dict_to_return_2 = {'license-usage-summary':
                                {'feature-summary': [1]}
                            }
        self.mocked_obj.get_rpc_equivalent = MagicMock()
        self.mocked_obj.execute_rpc = MagicMock()
        jxmlease.parse_etree = MagicMock(return_value=dict_to_return)

        self.assertEqual(get_license_usage(device=self.mocked_obj), [1])
        jxmlease.parse_etree = MagicMock(return_value=dict_to_return_2)
        self.assertEqual(get_license_usage(device=self.mocked_obj), [1])


if __name__ == '__main__':
    unittest.main()
