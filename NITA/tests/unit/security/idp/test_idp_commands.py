import unittest2 as unittest
from mock import MagicMock, patch
from jnpr.toby.hldcl.juniper.security.srx import Srx
from jnpr.toby.security.idp.idp_commands import *
from jnpr.toby.utils.response import Response

class Response:
    def __init__(self, value=""):
        self.resp = value

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()


    def test_idp_remove_attack_in_sig_xml(self):
        self.mocked_obj.shell = MagicMock()
        try:
            idp_remove_attack_in_sig_xml()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        try:
            idp_remove_attack_in_sig_xml(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Missing mandatory argument attackname")

        device_response = ""
        self.mocked_obj.shell = MagicMock(return_value=Response(device_response))
        try:
            idp_remove_attack_in_sig_xml(device=self.mocked_obj, attackname="FTP:USER:ROOT")
        except Exception as err:
            self.assertEqual(err.args[0], "grep command output is not as expected: , hence not "
                                          "able to remove the attack : FTP:USER:ROOT")

        device_response = "139088-    <Entry>\n" + "139090:      <Name>FTP:USER:ROOT</Name>\n" +"139150-    </Entry>"
        self.mocked_obj.shell = MagicMock(return_value=Response(device_response))
        self.assertEqual(idp_remove_attack_in_sig_xml(device=self.mocked_obj,
                                                            attackname="FTP:USER:ROOT"), True)

    def test_get_idp_security_pkg_details(self):
        self.mocked_obj.shell = MagicMock()
        try:
            get_idp_security_pkg_details()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")
        sig_details = {'idp-security-package-information': {'detector-version': '12.6.130161014',
                                      'policy-template-version': 'N/A',
                                      'security-package-version': '2833(Tue '
                                                                  'Feb 28 '
                                                                  '18:36:06 '
                                                                  '2017 UTC)'}}
        sig_return_details = {'date': 'Feb 28 18:36:06 2017 ', 'templates': 'N/A', 'version': '2833', 'detector': '12.6.130161014'}

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=sig_details)
        self.assertEqual(get_idp_security_pkg_details(device=self.mocked_obj), sig_return_details)
        sig_details = {'idp-security-package-information': {'detector-version': '12.6.130161014',
                                      'policy-template-version': 'N/A',
                                      'security-package-version': 'N/A()'}}
        sig_return_details = {'date': 'N/A', 'templates': 'N/A', 'version': 'N/A', 'detector':
            '12.6.130161014'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=sig_details)
        self.assertEqual(get_idp_security_pkg_details(device=self.mocked_obj), sig_return_details)

    def test_get_idp_security_package_list(self):
        self.mocked_obj.shell = MagicMock()
        try:
            get_idp_security_package_list()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")
        sig_list_resp = {'idp-recent-security-package-information': {
        'recent-security-package-version':['2834', '2833', '2832', '2831', '2830', '2829',
                                           '2828', '2827', '2826', '2825']}}
        sig_list = ['2834', '2833', '2832', '2831', '2830', '2829', '2828', '2827', '2826', '2825']
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=sig_list_resp)
        self.assertEqual(get_idp_security_package_list(device=self.mocked_obj), sig_list)

    def test_get_idp_prev_sec_pkg_version(self):
        self.mocked_obj.shell = MagicMock()
        try:
            get_idp_prev_sec_pkg_version()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")
        sig_list_resp = {'idp-recent-security-package-information': {
        'recent-security-package-version':['2834', '2833', '2832', '2831', '2830', '2829',
                                           '2828', '2827', '2826', '2825']}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=sig_list_resp)
        self.assertEqual(get_idp_prev_sec_pkg_version(device=self.mocked_obj), "2833")
        sig_list_resp = {'idp-recent-security-package-information': {
        'recent-security-package-version':['2834']}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=sig_list_resp)
        self.assertEqual(get_idp_prev_sec_pkg_version(device=self.mocked_obj), "0")

    def offline_download_exception(self, msg):
        try:
            download_idp_offline_sec_pkg(device=self.mocked_obj, file="/root/offline.tar.gz")
        except Exception as err:
            self.assertEqual(err.args[0], msg)

    def test_download_idp_offline_sec_pkg(self):
        try:
            download_idp_offline_sec_pkg()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")
        try:
            download_idp_offline_sec_pkg(self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Missing IDP signature update file name")

        self.mocked_obj.cli = MagicMock(return_value=Response("Will be processed in async mode"))
        time.sleep = MagicMock()
        self.mocked_obj.is_ha = MagicMock(return_value=False)

        msg1 = {'offline-download-status': {'offline-download-status-detail': 'In '
                                                                           'progress:Performing Offline download...'}}
        msg2 = {'offline-download-status': {'offline-download-status-detail': 'Done;File '
                                                                              '</root/offline1.tar.gz> does not exist'}}
        msg3 = {'offline-download-status': {'offline-download-status-detail': 'Ready to accept a new request'}}
        msg4 = {'offline-download-status': {'offline-download-status-detail': 'Done;Signature package offline download Successful.'}}
        msg5 = {'offline-download-status': {'offline-download-status-detail': 'Done;Attack DB update : not performed'}}

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=msg1)
        self.offline_download_exception("Offline IDP Signature download failed. Message - Security package download timed out")
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=msg2)
        self.offline_download_exception("Offline IDP Signature download failed. Message - Done;File </root/offline1.tar.gz> does not exist")
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=msg3)
        self.offline_download_exception("Offline IDP Signature download failed. Message - Ready to accept a new request")
        self.assertEqual(download_idp_offline_sec_pkg(device=self.mocked_obj, file="test.gz",
                                              validate=False), {'message': "Ready to accept a new request", 'status': 'error'})


        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=msg4)
        status = {'status': 'success', 'message': "Done;Signature package offline download "
                                                  "Successful."}
        self.assertEqual(download_idp_offline_sec_pkg(device=self.mocked_obj, file="test.gz"), status)
        status = {'status': 'success', 'message': "Done;Attack DB update : not performed"}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=msg5)
        self.assertEqual(download_idp_offline_sec_pkg(device=self.mocked_obj, file="test.gz"), status)

        self.mocked_obj.is_ha = MagicMock(return_value=True)
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=msg4)
        status = {'status': 'success', 'node': "node1", 'message': "Done;Signature package offline download Successful."}
        self.assertEqual(download_idp_offline_sec_pkg(device=self.mocked_obj, file="test.gz"), status)

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=msg3)
        self.offline_download_exception("Offline IDP Signature download failed. Message - Ready to accept a new request")
        self.mocked_obj.execute_as_rpc_command = MagicMock(side_effect=[msg4, msg3])
        self.offline_download_exception("Offline IDP Signature download failed. Message - Ready to accept a new request")

    def download_idp_exception(self, msg, update_type=None, version=None):
        try:
            if update_type is None:
                if version is None:
                    download_idp_security_package(device=self.mocked_obj)
                else:
                    download_idp_security_package(device=self.mocked_obj, version=version)
            else:
                download_idp_security_package(device=self.mocked_obj, update_type=update_type)
        except Exception as err:
            self.assertEqual(err.args[0], msg)

    def test_download_idp_security_package(self):
        try:
            download_idp_security_package()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        self.mocked_obj.download_idp_security_package = MagicMock(return_value=True)
        self.download_idp_exception("Incorrect value for idp signature package download type", update_type="test")
        check_response = {'secpack-download-status': {'secpack-download-status-detail':
                                                        'Success retrieved from(https://signatures.juniper.net/cgi-bin/index.cgi)'}}
        msg1 = "Success retrieved from(https://signatures.juniper.net/cgi-bin/index.cgi)"
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=check_response)
        self.download_idp_exception("Check server is failed. Message " + msg1, update_type="check")
        self.assertEqual(download_idp_security_package(device=self.mocked_obj, update_type="check", validate=False), {'status':'error', 'message': msg1})
        check_response = {'secpack-download-status': {'secpack-download-status-detail':
                                                        'Successfully retrieved '
                                                               'from(https://signatures.juniper.net/cgi-bin/index.cgi). '
                                                               'Version info:2865(Detector=12.6.130161014, Templates=2865)'}}
        status = {'url': 'https://signatures.juniper.net/cgi-bin/index.cgi', 'detector': '12.6.130161014', 'message': 'Successfully retrieved from(https://signatures.juniper.net/cgi-bin/index.cgi). Version info:2865(Detector=12.6.130161014, Templates=2865)', 'version': '2865', 'status': 'success', 'templates': '2865'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=check_response)
        self.assertEqual(download_idp_security_package(device=self.mocked_obj,
                                                       update_type="check"), status)

        time.sleep = MagicMock()
        self.mocked_obj.is_ha = MagicMock(return_value = False)
        download_msg1 = {'secpack-download-status': {'secpack-download-status-detail': 'In progress: Downloading ...'}}
        download_msg2 = {'secpack-download-status': {'secpack-download-status-detail': 'Done;Successfully '
                            'downloaded from(https://signatures.juniper.net/cgi-bin/index.cgi). '
                        'Version info:2865(Sun Apr 16 01:14:09 2017 UTC, Detector=12.6.130161014)'}}
        status2 = {'message': 'Done;Successfully downloaded from('
                              'https://signatures.juniper.net/cgi-bin/index.cgi). Version info:2865(Sun Apr 16 01:14:09 2017 UTC, Detector=12.6.130161014)', 'detector': '', 'status': 'success', 'url': 'https://signatures.juniper.net/cgi-bin/index.cgi', 'version': '2865', 'date': 'Sun Apr 16 01:14:09 2017 UTC'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_msg1)
        self.download_idp_exception("Security package download timed out")

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_msg2)
        self.assertEqual(download_idp_security_package(device=self.mocked_obj), status2)

        download_msg3 = {'secpack-download-status': {'secpack-download-status-detail': 'Ready to accept a new request'}}
        status3 = "IDP Signature/template download is failed. Message Ready to accept a new request"
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_msg3)
        self.download_idp_exception(status3, version="full-update")

        download_msg4 = {'secpack-download-status': {'secpack-download-status-detail': 'Done;No Newer version available'}}
        status4 = {'message': "Done;No Newer version available", 'status':'success'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_msg4)
        self.assertEqual(download_idp_security_package(device=self.mocked_obj, version=100),
                         status4)

        download_msg5 = {'secpack-download-status': {'secpack-download-status-detail': 'error in downloading'}}
        status5 = {'message': "error in downloading", 'status': "error"}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_msg5)
        self.assertEqual(download_idp_security_package(device=self.mocked_obj, validate=False),
                         status5)

        download_msg6 = {'secpack-download-status': {'secpack-download-status-detail': 'test'}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_msg6)
        self.download_idp_exception("Unexpected status message: test")

        download_msg7 = {'secpack-download-status': {'secpack-download-status-detail': 'Done;Successfully downloaded '
                                                               'from(https://signatures.juniper.net/cgi-bin/index.cgi). Version info:2865'}}
        status7 = {'status': 'success', 'message': 'Done;Successfully downloaded from(https://signatures.juniper.net/cgi-bin/index.cgi). Version info:2865', 'version': '2865', 'url': 'https://signatures.juniper.net/cgi-bin/index.cgi'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_msg7)
        self.assertEqual(download_idp_security_package(device=self.mocked_obj,
                                                       update_type="templates"), status7)

        download_msg8 = {'secpack-download-status': {'secpack-download-status-detail':
                                                         'Done;Successfully downloaded'}}
        self.mocked_obj.is_ha = MagicMock(return_value = True)
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_msg8)
        self.download_idp_exception("IDP Signature/template download is failed. Message Done;Successfully downloaded")



    def install_exception_check(self, msg, update_type=None):
        try:
            if update_type is None:
                install_idp_security_package(device=self.mocked_obj)
            else:
                install_idp_security_package(device=self.mocked_obj, update_type=update_type)
        except Exception as err:
            self.assertEqual(err.args[0], msg)

    def test_install_idp_security_package(self):
        try:
            install_idp_security_package()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        install_msg1 = "invalid license"
        self.mocked_obj.is_ha = MagicMock(return_value=False)
        self.mocked_obj.cli = MagicMock(return_value=Response(install_msg1))
        self.install_exception_check("IDP Signature update failed due to license error - " +
                                     install_msg1)

        install_msg1 = "invalid license"
        self.mocked_obj.cli = MagicMock(return_value=Response(install_msg1))
        status = {'message': "invalid license", 'status': 'error'}
        self.assertEqual(install_idp_security_package(device=self.mocked_obj, validate=False),
                         status)

        self.mocked_obj.is_ha = MagicMock(return_value=True)
        install_msg3 = [{"secpack-update-status": "invalid license"},
                        {"secpack-update-status": "installation failed"}]
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=install_msg3)
        self.install_exception_check("IDP Signature update failed due to license error - " + install_msg1)

        install_msg4 = [{"secpack-update-status": "Will be processed in async mode. Check the status using the status checking CLI"},
                        {"secpack-update-status": "invalid license"}]
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=install_msg4)
        self.install_exception_check("IDP Signature update failed due to license error - " + install_msg1)


        # Check the install
        install_msg3 = "Will be processed in async mode. Check the status using the status checking CLI"
        status1 = {'secpack-update-status': {'secpack-status-detail': 'In progress'}}
        status2 = {'secpack-update-status': {'secpack-status-detail': 'error in install'}}
        status3 = {'secpack-update-status': {'secpack-status-detail': 'test msg'}}
        msg4 = "Done;Attack DB update : successful - [UpdateNumber=2865,ExportDate=Sun Apr 16 " \
              "01:14:09 2017 UTC,Detector=12.6.130161014]\nUpdating control-plane with new " \
              "detector : successful\nUpdating data-plane with new attack or detector : successful"
        status4 = {'secpack-update-status': {'secpack-status-detail': msg4}}
        msg5 = "Done;Attack DB update : successful - [UpdateNumber=2865,ExportDate=Sun Apr 16 " \
              "01:14:09 2017 UTC,Detector=12.6.130161014]\nUpdating control-plane with new " \
              "detector : successful"
        status5 = {'secpack-update-status': {'secpack-status-detail': msg5}}

        self.mocked_obj.is_ha = MagicMock(return_value=False)
        self.mocked_obj.cli = MagicMock(return_value=Response(install_msg3))
        time.sleep = MagicMock()
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status1)
        self.install_exception_check(
            "IDP Signature update install failed - IDP Security package install timed out")
        sig_return1 = {'message': 'IDP Security package install timed out', 'status': 'error'}
        self.assertEqual(install_idp_security_package(device=self.mocked_obj,
                                                      option="update-db-only", validate=False),
                         sig_return1)
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status2)
        self.install_exception_check("IDP Signature update install failed - error in install")
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status3)
        self.install_exception_check("Unexpected status message: test msg")
        self.install_exception_check("Incorrect value for idp signature package install type",
                                     update_type="test")
        sig_return4 = {'message': msg4, 'status': 'success', 'version': '2865', 'detector':
            '12.6.130161014', 'cp-status':'successful', 'dp-status':'successful', 'date':'Sun Apr 16 01:14:09 2017 UTC'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status4)
        self.assertEqual(install_idp_security_package(device=self.mocked_obj), sig_return4)

        sig_return5 = {'message': msg5, 'status': 'success', 'version': '2865', 'detector':
            '12.6.130161014', 'cp-status':'successful', 'date':'Sun Apr 16 01:14:09 2017 UTC'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status5)
        self.assertEqual(install_idp_security_package(device=self.mocked_obj,
                                                      option="update-db-only"), sig_return5)

        status6 = {'secpack-update-status': {'secpack-status-detail': "Done;Attack DB update : not "
                                                                      "performed"}}
        sig_return6 = {'message': "Done;Attack DB update : not performed", 'status': 'not performed'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status6)
        self.assertEqual(install_idp_security_package(device=self.mocked_obj), sig_return6)

        status7 = {'secpack-update-status': {'secpack-status-detail': "Done;AI installation failed"}}
        sig_return7 = {'message': "Done;AI installation failed", 'status': 'error'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status7)
        self.assertEqual(install_idp_security_package(device=self.mocked_obj, validate=False),
                         sig_return7)
        self.install_exception_check("IDP Signature update install failed on AI installation - " +
                                     "Done;AI installation failed")

        status8 = {'secpack-update-status': {'secpack-status-detail': "Done;installation failed"}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status8)
        self.install_exception_check("Unexpected status message: Done;installation failed")

        # Test HA
        self.mocked_obj.is_ha = MagicMock(return_value=True)
        install_msg9 = [{"secpack-update-status": "Will be processed in async mode. Check the "
                                                  "status using the status checking CLI"},
                        {"secpack-update-status": "Will be processed in async mode. Check the status using the status checking CLI"}]
        status9 = {"secpack-update-status": {'secpack-status-detail': "error in install"}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(side_effect=[install_msg9, status9,
                                                                        status9])
        self.install_exception_check("IDP Signature update install failed - error in install")
        self.mocked_obj.execute_as_rpc_command = MagicMock(side_effect=[install_msg9, status4,
                                                                status9])
        self.install_exception_check("IDP Signature update install failed - error in install")

        # Test Templates
        self.mocked_obj.is_ha = MagicMock(return_value=False)
        template_msg = "Done;policy-templates has been successfully updated into internal " \
                       "repository\n(=>/var/db/scripts/commit/templates.xsl)!"
        template_resp = {'secpack-update-status': {'secpack-status-detail': template_msg}}
        template_status = {'message': template_msg, 'status': 'success'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=template_resp)
        self.assertEqual(install_idp_security_package(device=self.mocked_obj,
                                                      update_type="templates"), template_status)

    @patch('jnpr.toby.security.idp.idp_commands.install_idp_security_package')
    @patch('jnpr.toby.security.idp.idp_commands.download_idp_security_package', autospec=True)
    @patch('jnpr.toby.security.idp.idp_commands.get_idp_security_pkg_details', autospec=True)
    def test_update_idp_signature_package(self, patched_get_idp_security_pkg_details=None,
                                          patched_download_idp_security_package=None,
                                          patched_install_idp_security_package=None):
        try:
            update_idp_signature_package()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")
        try:
            update_idp_signature_package(self.mocked_obj, update_type="test")
        except Exception as err:
            self.assertEqual(err.args[0], "Incorrect value for idp signature package type.")

        patched_get_idp_security_pkg_details.return_value =  {'date': 'Feb 28 18:36:06 2017 ',
                                                              'templates': '1000', 'version':
                                                                  '2000', 'detector':
                                                                  '12.6.130161014'}

        patched_download_idp_security_package.return_value = {'status': "success",
                                                              'version':'2000', 'templates': '1000'}

        # Templates
        self.assertEqual(update_idp_signature_package(device=self.mocked_obj,
                                                      update_type="templates", version=1000), True)
        self.assertEqual(update_idp_signature_package(device=self.mocked_obj,
                                                      update_type="templates"), True)
        self.assertEqual(update_idp_signature_package(device=self.mocked_obj,
                                                      update_type="templates", overwrite=True), True)

        # Signatures
        self.assertEqual(update_idp_signature_package(device=self.mocked_obj, version=2000), True)
        self.assertEqual(update_idp_signature_package(device=self.mocked_obj), True)
        self.assertEqual(update_idp_signature_package(device=self.mocked_obj, overwrite=True), True)
        self.assertEqual(update_idp_signature_package(device=self.mocked_obj,
                                                      version="full-update", overwrite=True), True)
        self.assertEqual(update_idp_signature_package(device=self.mocked_obj,
                                                      option="update-db-only", overwrite=True), True)

    def test_get_policy_commit_status(self):
        try:
            get_idp_policy_commit_status()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        msg1 = "Beginning policy compilation"
        msg2 = "Reading set file for compilation"
        msg3 = "Compiling policy"
        msg4 = "Generating compiled binary"
        msg5 = "Starting policy package"
        msg6 = "Starting policy load"
        msg7 = " IDP policy[/var/db/idpd/bins//occam.bin.gz.v] and detector[" \
               "/var/db/idpd/sec-repository/installed-detector/libidp-detector.so.tgz.v] loaded " \
               "successfully.\nThe loaded policy size is:32728949 Bytes"
        msg8 = "Active policy not configured or Active policy not modified"
        msg9 = "Running policy unloaded"
        msg10 = "error"
        msg11 = "test"
        msg12 = "Policy packaging completed successfully"

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg1}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status':
                                                                                  "started", 'message': msg1})

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg2}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status':
                                                                                  "started", 'message': msg2})

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg3}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status':
                                                                                 "compiling", 'message': msg3})

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg4}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status': "compiling", 'message': msg4})

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg5}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status': "loading", 'message': msg5})

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg12}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status': "loading", 'message': msg12})

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg6}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status': "loading", 'message': msg6})

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg7}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status': "success", 'message': msg7,
                                                                            'name': 'occam', 'size': '32728949'})

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg8}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status': "nochange", 'message': msg8})

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg9}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status': "unloaded", 'message': msg9})

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg10}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_commit_status(device=self.mocked_obj), {'status': "error", 'message': msg10})

        try:
            device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg11}}
            self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
            get_idp_policy_commit_status(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Policy commit status message not implemented: " + msg11)

    def test_get_policy_status_detail(self):
        try:
            get_idp_policy_status_detail()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        msg1 = "error in loading policy"
        msg2 = " IDP policy[/var/db/idpd/bins//Client-And-Server-Protection.bin.gz.v] and detector[/var/db/idpd/sec-repository/installed-detector/libidp-detector.so.tgz.v] loaded successfully.\nThe loaded policy size is:32999389 Bytes.\nDFA: PCRE\nPCRE converted patterns: 7383\nCompiler process Max RSS:74328KB"

        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg1}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value= device_msg)
        self.assertEqual(get_idp_policy_status_detail(device=self.mocked_obj), {'status': "error",
                                                                                'message': msg1})

        status = {'name': 'Client-And-Server-Protection', 'message': msg2, 'converted': '7383',
                  'max_rss': '74328', 'pattern': 'PCRE', 'status': 'success', 'size': '32999389'}
        device_msg = {'idp-policy-commit-status': {'policy-commit-status-detail': msg2}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=device_msg)
        self.assertEqual(get_idp_policy_status_detail(device=self.mocked_obj), status)

    def test_clear_idp_policy_commit_status(self):
        try:
            clear_idp_policy_commit_status()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        self.mocked_obj.cli = MagicMock()
        self.assertEqual(clear_idp_policy_commit_status(device=self.mocked_obj), None)


    def test_clear_idp_policy_commit_status(self):
        try:
            clear_idp_policy_commit_status()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        self.mocked_obj.cli = MagicMock()
        self.assertEqual(clear_idp_policy_commit_status(device=self.mocked_obj), None)

    def test_clear_idp(self):
        try:
            clear_idp()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        self.mocked_obj.cli = MagicMock()
        self.assertEqual(clear_idp(device=self.mocked_obj, what="all"), None)
        self.assertEqual(clear_idp(device=self.mocked_obj, what="attack-table"), None)
        self.assertEqual(clear_idp(device=self.mocked_obj, what="ssl-session-id-cache"), None)
        self.assertEqual(clear_idp(device=self.mocked_obj, what="applicatin-statistics"), None)
        self.assertEqual(clear_idp(device=self.mocked_obj, what="counter", counter_names=['flow']),
                         None)
        try:
            clear_idp(device=self.mocked_obj, what="counter")
        except Exception as err:
            self.assertEqual(err.args[0], "counter_names liest is mandatory argument with what is passed with value counter")
        try:
            clear_idp(device=self.mocked_obj, what="counter", counter_names=[])
        except Exception as err:
            self.assertEqual(err.args[0], "counter_names list doesn't have any value")

    def test_get_idp_attack_table(self):
        try:
            get_idp_attack_table()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=None)
        self.assertEqual(get_idp_attack_table(device=self.mocked_obj), {})

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value={'idp-attack-information': ''})
        self.assertEqual(get_idp_attack_table(device=self.mocked_obj), {})

        atk_table = {'idp-attack-information': {'idp-attack-statistics': [
            {'name': 'SSL:TLS-BRUTE-FORCE', 'value': '85035'},
            {'name': 'HTTP:REQERR:NULL-IN-HEADER', 'value': '19990'}]}}
        atk_list = {'SSL:TLS-BRUTE-FORCE': 85035, 'HTTP:REQERR:NULL-IN-HEADER': 19990}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=atk_table)
        self.assertEqual(get_idp_attack_table(device=self.mocked_obj), atk_list)
        atk_table = {'idp-attack-information': {'idp-attack-statistics': {'name': 'SSL:TLS-BRUTE-FORCE', 'value': '85035'}}}
        atk_list = {'SSL:TLS-BRUTE-FORCE': 85035}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=atk_table)
        self.assertEqual(get_idp_attack_table(device=self.mocked_obj, lsys="LSYS1"), atk_list)

    def verify_idp_exception_check(self, attacks, count, negate, msg):
        try:
            verify_idp_attack(device=self.mocked_obj, attacks=attacks, count=count, negate=negate)
        except Exception as err:
            self.assertEqual(err.args[0], msg)

    @patch('jnpr.toby.security.idp.idp_commands.get_idp_attack_table')
    def test_verify_idp_attack(self, patched_get_idp_attack_table=None):
        try:
            verify_idp_attack()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        self.verify_idp_exception_check(None, 0, False, "attacks variable is None, it is mandatory "
                                                     "argument")
        self.verify_idp_exception_check({"test"}, 0, False, "attacks variable is not type of list")
        self.verify_idp_exception_check([], 0, False, "attack list is empty, minimum one attack is "
                                                   "requried")
        patched_get_idp_attack_table.return_value = {}
        msg1 = "Attack table is empty and Attack is not detected. Count mismatch for negatee : Count - 1"
        self.verify_idp_exception_check(["FTP:USER:ROOT"], 1, True, msg1)

        self.assertEqual(verify_idp_attack(device=self.mocked_obj, attacks=["FTP:USER:ROOT"],
                                           negate=True), True)
        self.verify_idp_exception_check(["FTP:USER:ROOT"], 0, False, "Attack table is empty and "
                                                                     "Attack is not detected.")
        patched_get_idp_attack_table.return_value = {'SSL:TLS-BRUTE-FORCE': 100,
                                         'HTTP:REQERR:NULL-IN-HEADER': 200}
        msg2 = "Attack Detection failed"
        self.verify_idp_exception_check(["FTP:USER:ROOT"], 1, False, msg2)
        self.verify_idp_exception_check(["SSL:TLS-BRUTE-FORCE"], 1, False, msg2)
        self.assertEqual(verify_idp_attack(device=self.mocked_obj, attacks=["SSL:TLS-BRUTE-FORCE"]), True)
        self.assertEqual(verify_idp_attack(device=self.mocked_obj, attacks="SSL:TLS-BRUTE-FORCE"), True)
        self.assertEqual(verify_idp_attack(device=self.mocked_obj, attacks=["SSL:TLS-BRUTE-FORCE"], count=100), True)

        self.verify_idp_exception_check(["SSL:TLS-BRUTE-FORCE"], 0, True, msg2)
        self.verify_idp_exception_check(["SSL:TLS-BRUTE-FORCE"], 100, True, msg2)
        self.assertEqual(verify_idp_attack(device=self.mocked_obj, attacks=[
            "SSL:TLS-BRUTE-FORCE"], count=10, negate=True), True)
        self.verify_idp_exception_check(["FTP:USER:ROOT"], 10, True, msg2)
        self.assertEqual(verify_idp_attack(device=self.mocked_obj, attacks=[
            "FTP:USER:ROOT"], negate=True), True)

    def test_get_idp_counter(self, patched_get_idp_attack_table=None):
        try:
            get_idp_counter()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")
        try:
            get_idp_counter(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "counter_name is mandatory argument")
        device_stats = {'idp-counter-information': {'idp-counter-statistics': [{'name': 'None',
                                                             'value': '1000'},
                                                            {'name': 'Recommended',
                                                             'value': '0'},
                                                            {'name': 'Ignore',
                                                             'value': '30'}]}}
        stats = {'None': 1000, 'Recommended': 0, 'Ignore': 30 }
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=device_stats)
        self.assertEqual(get_idp_counter(device=self.mocked_obj, counter_name="action"), stats)

    def verify_idp_counter_exception(self, name, values, msg):
        try:
            verify_idp_counter(device=self.mocked_obj, counter_name=name, counter_values=values)
        except Exception as err:
            self.assertEqual(err.args[0], msg)

    @patch('jnpr.toby.security.idp.idp_commands.get_idp_counter')
    def test_verify_idp_counter(self, patched_get_idp_counter=None):
        try:
            verify_idp_counter()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        self.verify_idp_counter_exception(None, None, "counter_name is mandatory argument")
        self.verify_idp_counter_exception("action", None, "counter_values is None, it is mandatory argument")
        self.verify_idp_counter_exception("action", "test", "counter_values is not dict type")
        self.verify_idp_counter_exception("action", {}, "counter_values are empty, it is mandatory argument")

        patched_get_idp_counter.return_value = {'None': 1000, 'Recommended': 0, 'Ignore': 30 }
        self.assertEqual(verify_idp_counter(device=self.mocked_obj, counter_name="action",
                                            counter_values={'None': 1000}), True)
        self.verify_idp_counter_exception("action", {'None': 100}, "IDP Counter validation failed")
        self.verify_idp_counter_exception("action", {'Close': 10}, "IDP Counter validation failed")

    def test_get_idp_policy_templates_list(self):
        try:
            get_idp_policy_templates_list()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        device_list = {'output': "Web_Server\nDMZ_Services"}
        template_list = ['Web_Server', 'DMZ_Services']
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=device_list)
        self.assertEqual(get_idp_policy_templates_list(device=self.mocked_obj), template_list)

if __name__ == '__main__':
    unittest.main()