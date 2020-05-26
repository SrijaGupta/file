import unittest2 as unittest
from mock import MagicMock, patch
from jnpr.toby.hldcl.juniper.security.srx import Srx
from jnpr.toby.security.appsecure.appid_commands import *


class Response:
    def __init__(self, value=""):
        self.resp = value

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=Srx)
    mocked_obj.log = MagicMock()

    def test_get_appid_sig_package_version(self):
        try:
            get_appid_sig_package_version()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        response = {'appid-package-version': {'version-detail': '1000'}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response)
        self.assertEqual(get_appid_sig_package_version(device=self.mocked_obj), "1000")

    def test_check_app_sig_installed(self):
        try:
            check_app_sig_installed()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        response = {'appid-package-version': {'version-detail': '1000'}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response)
        self.assertEqual(check_app_sig_installed(device=self.mocked_obj), True)

        try:
            response = {'appid-package-version': {'version-detail': '0'}}
            self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response)
            self.assertEqual(check_app_sig_installed(device=self.mocked_obj), True)
        except Exception as err:
            self.assertEqual(err.args[0], "Application signature package is not installed")

    def download_exception_check(self, msg, update_type=None):
        try:
            if update_type is not None:
                download_appid_sig_package(device=self.mocked_obj, update_type=update_type)
            else:
                download_appid_sig_package(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], msg)

    def test_download_appid_sig_package(self):
        try:
            download_appid_sig_package()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        self.download_exception_check("Incorrect value for AppID signature package download "
                                      "update_type", update_type=True)

        self.mocked_obj.configure_appid_sig_package = MagicMock(return_value=True)
        # Testing Check-server
        check_msg = {'apppack-server-status': {'apppack-server-status-detail': 'Download server '
                                                                               'URL: https://signatures.juniper.net/cgi-bin/index.cgi Sigpack Version: '
                                                                               '2862 Protobundle version: 1.270.0-40.005 Build Time = Mar 30 2017 10:00:46'}}
        check_return = {'status': 'success', 'date': 'Mar 30 2017 10:00:46', 'protobundle':
            '1.270.0-40.005', 'url': 'https://signatures.juniper.net/cgi-bin/index.cgi',
                        'message': 'Download server URL: https://signatures.juniper.net/cgi-bin/index.cgi Sigpack Version: 2862 Protobundle version: 1.270.0-40.005 Build Time = Mar 30 2017 10:00:46',
                        'version': '2862'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=check_msg)
        self.assertEqual(download_appid_sig_package(device=self.mocked_obj, update_type="check"),
                         check_return)

        check_msg = {
            'apppack-server-status': {'apppack-server-status-detail': 'error in downloading'}}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=check_msg)
        self.download_exception_check("Check server is failed. Message - error in downloading",
                                      update_type="check")

        check_msg = {'apppack-server-status': {'apppack-server-status-detail': 'download failed'}}
        check_return = {'status': 'error', 'message': 'download failed'}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=check_msg)
        self.assertEqual(download_appid_sig_package(device=self.mocked_obj, update_type="check",
                                                    validate=False), check_return)

        # Test for Signature download
        download_error = "Download failed. Error: Require application identification license"
        self.mocked_obj.cli = MagicMock(return_value=Response(download_error))
        download_resp = {'status' : 'error', 'message': download_error}
        self.assertEqual(download_appid_sig_package(device=self.mocked_obj, validate=False),
                         download_resp)
        self.download_exception_check("Application Signature download failed : " + download_error)

        self.mocked_obj.cli = MagicMock(return_value=Response("Please use command"))
        time.sleep = MagicMock()
        self.mocked_obj.get_rpc_equivalent = MagicMock(
            return_value="<request-appid-application-package-download-status/>")
        download_status1 = {'apppack-download-status': {
            'apppack-download-status-detail': 'Downloading application package failed'}}
        download_status2 = {'apppack-download-status': {
            'apppack-download-status-detail': 'error in donloading application package'}}
        download_status3 = {'apppack-download-status': {'apppack-download-status-detail':
                                                            'Fetching/Uncompressing '
                                                            'https://signatures.juniper.net/xmlupdate/244/Applications/2862/applications.xsd'}}
        download_status4 = {'apppack-download-status': {
            'apppack-download-status-detail': 'Downloading application package 2862 succeeded.'}}
        sig_return = {'status': 'success', 'version': '2862',
                      'message': 'Downloading application package 2862 succeeded.'}
        # Checking error conditions
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_status1)
        self.download_exception_check("Application Signature package download is failed. "
                                      "Message - Downloading application package failed")

        sig_return1 = {'message': 'Downloading application package failed', 'status': 'error'}
        self.assertEqual(download_appid_sig_package(device=self.mocked_obj, validate=False),
                         sig_return1)
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_status2)
        self.download_exception_check("Unexpected status messsage: "
                                      "error in donloading application package")

        # Checking timeout
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_status3)
        self.download_exception_check("Application Signature package download timed out")

        # Checking download
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=download_status4)
        self.assertEqual(download_appid_sig_package(device=self.mocked_obj, version=100),
                         sig_return)

    def install_exception_check(self, msg):
        try:
            install_app_sig_package(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], msg)

    def test_install_app_sig_package(self):
        try:
            install_app_sig_package()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        install_msg1 = "Require application identification license"
        install_msg2 = "installation failed"
        # Check Error conditions
        self.mocked_obj.is_ha = MagicMock(return_value=False)
        self.mocked_obj.cli = MagicMock(return_value=Response(install_msg1))
        self.install_exception_check("Application Signature update failed - " + install_msg1)

        self.mocked_obj.cli = MagicMock(return_value=Response(install_msg2))
        self.install_exception_check("Application Signature update failed - " + install_msg2)
        self.assertEqual(install_app_sig_package(device=self.mocked_obj, validate=False),
                         {'message': install_msg2, 'status': "error"})

        self.mocked_obj.is_ha = MagicMock(return_value=True)
        install_msg3 = [{"apppack-install-status": {
            'apppack-install-status-detail': "Require application identification license"}},
                        {"apppack-install-status": {
                            'apppack-install-status-detail': "installation failed"}}]
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=install_msg3)
        self.install_exception_check("Application Signature update failed - " + install_msg1)

        install_msg4 = [{"apppack-install-status": {
            'apppack-install-status-detail': "Please use command\nrequest services application-identification install status to check install status"}},
                        {"apppack-install-status": {
                            'apppack-install-status-detail': "installation failed"}}]
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=install_msg4)
        self.install_exception_check("Application Signature update failed - " + install_msg2)

        # Check the install
        install_msg3 = "Please use command\nrequest services application-identification install status to check install status"
        status1 = {'apppack-install-status': {
            'apppack-install-status-detail': 'Checking compatibility of application package version 2862 ...'}}
        status2 = {'apppack-install-status': {'apppack-install-status-detail': 'In progress'}}
        status3 = {'apppack-install-status': {'apppack-install-status-detail': 'error in install'}}
        status4 = {'apppack-install-status': {'apppack-install-status-detail': 'test msg'}}
        status5 = {'apppack-install-status': {
            'apppack-install-status-detail': 'Installed Application package (2862) and Protocol bundle successfully'}}
        status6 = {'apppack-install-status': {
            'apppack-install-status-detail': 'Installed Application package  and Protocol bundle successfully'}}
        sig_return = {
            'message': 'Installed Application package (2862) and Protocol bundle successfully',
            'status': 'success', 'version': '2862'}
        self.mocked_obj.is_ha = MagicMock(return_value=False)
        self.mocked_obj.cli = MagicMock(return_value=Response(install_msg3))
        time.sleep = MagicMock()
        self.mocked_obj.get_rpc_equivalent = MagicMock(
            return_value="<request-appid-application-package-install-status/>")
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status1)
        self.install_exception_check(
            "AppID Signature update install failed - Application signature package install timed out")
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status2)
        self.install_exception_check(
            "AppID Signature update install failed - Application signature package install timed out")
        sig_return1 = {'message': 'Application signature package install timed out', 'status': 'error'}
        self.assertEqual(install_app_sig_package(device=self.mocked_obj, validate=False),
                         sig_return1)
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status3)
        self.install_exception_check("AppID Signature update install failed - error in install")
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status4)
        self.install_exception_check("Unexpected status message: test msg")

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status5)
        self.assertEqual(install_app_sig_package(device=self.mocked_obj), sig_return)
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status6)
        self.install_exception_check(
            "Unknown version of application signature: Installed Application package  and Protocol bundle successfully")

        # Test for HA
        self.mocked_obj.is_ha = MagicMock(return_value=True)
        install_msg4 = [{"apppack-install-status": {
            'apppack-install-status-detail': "Please use command\nrequest services application-identification install status to check install status"}},
                        {"apppack-install-status": {
                            'apppack-install-status-detail': "Please use command\nrequest services application-identification install status to check install status"}}]
        self.mocked_obj.execute_as_rpc_command = MagicMock(side_effect=[install_msg4, status3,
                                                                        status3])
        self.install_exception_check("AppID Signature update install failed - error in install")

    def uninstall_exception_check(self, msg):
        try:
            uninstall_app_sig_package(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], msg)

    def test_uninstall_app_sig_package(self):
        try:
            uninstall_app_sig_package()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")

        uninstall_msg1 = "Uninstall Application package and Protocol bundle failed"
        # Check Error conditions
        self.mocked_obj.is_ha = MagicMock(return_value=False)
        self.mocked_obj.cli = MagicMock(return_value=Response(uninstall_msg1))
        self.uninstall_exception_check("Application Signature uninstall failed - " + uninstall_msg1)
        self.assertEqual(uninstall_app_sig_package(device=self.mocked_obj, validate=False),
                         {'message': uninstall_msg1, 'status': "error"})


        self.mocked_obj.is_ha = MagicMock(return_value=True)
        install_msg2 = [
            {"apppack-uninstall-status": {'apppack-uninstall-status-detail': "Uninstall "
                                                                             "Application package and Protocol bundle failed"}},
            {"apppack-uninstall-status": {'apppack-uninstall-status-detail': "Uninstall "
                                                                             "Application package and Protocol bundle failed"}}]
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=install_msg2)
        self.uninstall_exception_check("Application Signature uninstall failed - " + uninstall_msg1)

        install_msg3 = [
            {"apppack-uninstall-status": {'apppack-uninstall-status-detail': "Please use "
                                                                             "command\nrequest services application-identification uninstall status to check uninstall status"}},
            {"apppack-uninstall-status": {'apppack-uninstall-status-detail': "Uninstall "
                                                                             "Application package and Protocol bundle failed"}}]
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=install_msg3)
        self.uninstall_exception_check("Application Signature uninstall failed - " + uninstall_msg1)

        # Check the uninstall
        install_msg4 = "Please use command\nrequest services application-identification uninstall status to check uninstall status"
        status1 = {'apppack-uninstall-status': {
            'apppack-uninstall-status-detail': 'Checking dependency for application package version 2862 ...'}}
        status2 = {'apppack-uninstall-status': {
            'apppack-uninstall-status-detail': 'Uninstalled Application package (2862) and '
                                               'Protocol bundle successfully'}}
        status3 = {'apppack-uninstall-status': {'apppack-uninstall-status-detail': 'error in '
                                                                                   'uninstall'}}
        status4 = {'apppack-uninstall-status': {
            'apppack-uninstall-status-detail': 'Uninstalled Application package  and Protocol '
                                               'bundle successfully'}}
        sig_return = {'message': 'Uninstalled Application package (2862) and Protocol bundle '
                                 'successfully', 'status': 'success', 'version': '2862'}
        self.mocked_obj.is_ha = MagicMock(return_value=False)
        self.mocked_obj.cli = MagicMock(return_value=Response(install_msg4))
        time.sleep = MagicMock()
        self.mocked_obj.get_rpc_equivalent = MagicMock(
            return_value="<request-appid-application-package-uninstall-status/>")
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status1)
        sig_return1 = {'message': 'Application signature package uninstall timed out', 'status': 'error'}
        self.assertEqual(uninstall_app_sig_package(device=self.mocked_obj, validate=False),
                         sig_return1)
        self.uninstall_exception_check("AppID Signature update uninstall failed - Application "
                                       "signature package uninstall timed out")

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status2)
        self.assertEqual(uninstall_app_sig_package(device=self.mocked_obj), sig_return)
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=status4)
        self.uninstall_exception_check("Unknown version of application package: Uninstalled "
                                       "Application package  and Protocol bundle successfully")

        # Test for HA
        self.mocked_obj.is_ha = MagicMock(return_value=True)
        install_msg5 = [{"apppack-uninstall-status": {
            'apppack-uninstall-status-detail': "Please use command\nrequest services application-identification uninstall status to check uninstall status"}},
                        {"apppack-uninstall-status": {
                            'apppack-uninstall-status-detail': "Please use command\nrequest services application-identification uninstall status to check uninstall status"}}]
        self.mocked_obj.execute_as_rpc_command = MagicMock(side_effect=[install_msg5, status3,
                                                                        status3])
        self.uninstall_exception_check("AppID Signature update uninstall failed - error in "
                                       "uninstall")

    @patch('jnpr.toby.security.appsecure.appid_commands.uninstall_app_sig_package')
    @patch('jnpr.toby.security.appsecure.appid_commands.install_app_sig_package')
    @patch('jnpr.toby.security.appsecure.appid_commands.download_appid_sig_package', autospec=True)
    @patch('jnpr.toby.security.appsecure.appid_commands.get_appid_sig_package_version', autospec=True)
    def test_update_app_sig_package(self, patched_get_appid_sig_package_version=None,
                                    patched_download_appid_sig_package=None,
                                    patched_uninstall_app_sig_package=None,
                                    patced_install_app_sig_package=None):
        try:
            update_app_sig_package()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is mandatory argument")
        patched_get_appid_sig_package_version.return_value = 100
        patched_download_appid_sig_package.return_value = {'status': "success", 'version': '100'}
        self.assertEqual(update_app_sig_package(device=self.mocked_obj, version=100), True)
        self.assertEqual(update_app_sig_package(device=self.mocked_obj), True)
        self.assertEqual(update_app_sig_package(device=self.mocked_obj, version=100,
                                                overwrite=True), True)
        self.assertEqual(update_app_sig_package(device=self.mocked_obj, overwrite=True), True)
        patched_get_appid_sig_package_version.return_value = 200
        self.assertEqual(update_app_sig_package(device=self.mocked_obj), True)

    def test_verify_appid_stats_application_basic_exception(self):
        try:
            verify_appid_stats_application()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            verify_appid_stats_application(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'application' is a mandatory argument")



    def test_verify_appid_stats_application(self):


        dict_to_return = {'a':1}

        try:
            verify_appid_stats_application(device=self.mocked_obj, application="abc", statistics_dict=dict_to_return)
        except Exception as err:
            self.assertEqual(err.args[0], "No application Statistics Info available")
        self.assertEqual(verify_appid_stats_application(device=self.mocked_obj, application="abc", validate=False, statistics_dict=dict_to_return), False)

        dict_to_return = {'appid-application-statistics':
                            {'application-name':"xx"}
                         }

        try:
            verify_appid_stats_application(device=self.mocked_obj, application="abc", statistics_dict=dict_to_return)
        except Exception as err:
            self.assertEqual(err.args[0], "Application name not found")
        self.assertEqual(verify_appid_stats_application(device=self.mocked_obj, application="abc", validate=False, statistics_dict=dict_to_return), False)

        dict_to_return = {'appid-application-statistics':
                                   [{'application-name': "xx"}, {'application-name': "xz"}]
                         }


        p = patch("jnpr.toby.security.appsecure.appid_commands.get_appid_stats_application", new=MagicMock(return_value=dict_to_return))
        p.start()
        try:
            verify_appid_stats_application(device=self.mocked_obj, application="abc")
        except Exception as err:
            self.assertEqual(err.args[0], "Application name not found")
        p.stop()
        self.assertEqual(verify_appid_stats_application(device=self.mocked_obj, application="abc", validate=False, statistics_dict=dict_to_return),
                         False)


        dict_to_return = {'appid-application-statistics-usp':
                                   {'application-name': "xx", 'sessions': '10', 'bytes': '10', 'is_encrypted': 'Yes'}
                               }

        self.assertEqual(verify_appid_stats_application(device=self.mocked_obj, application="xx", session_count="10", bytes="10", encrypted="Yes", statistics_dict=dict_to_return), True)
        self.assertEqual(verify_appid_stats_application(device=self.mocked_obj, application="xx", statistics_dict=dict_to_return), True)

        dict_to_return = {'appid-application-statistics-usp':
                                   [{'application-name': "xx", 'sessions': '5', 'bytes': '10', 'is_encrypted': 'Yes'},
                                    {'application-name': "xx", 'sessions': '10', 'bytes': '2', 'is_encrypted': 'Yes'},
                                    {'application-name': "xx", 'sessions': '10', 'bytes': '10', 'is_encrypted': 'No'}]
                               }

        self.assertEqual(verify_appid_stats_application(device=self.mocked_obj, application="xx",
                                                        session_count="10", bytes="10",
                                                        encrypted="Yes", validate=False, statistics_dict=dict_to_return), False)
        try:
            verify_appid_stats_application(device=self.mocked_obj, application="xx",
                                           session_count="10", bytes="10",
                                           encrypted="Yes", statistics_dict=dict_to_return)
        except Exception as err:
            self.assertEqual(err.args[0], "Statistics are not matching")


    def test_get_appid_stats_application(self):
        try:
            get_appid_stats_application()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        dict_to_return = {'appid-application-statistics-information': 1}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=dict_to_return)
        self.assertEqual(get_appid_stats_application(device=self.mocked_obj), 1)


    def test_get_appid_stats_application_grp(self):
        try:
            get_appid_stats_application_grp()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        dict_to_return = {'appid-application-group-statistics-information': 1}
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=dict_to_return)
        self.assertEqual(get_appid_stats_application_grp(device=self.mocked_obj), 1)


    def test_verify_appid_stats_application_grp_basic_exception(self):
        try:
            verify_appid_stats_application_grp()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            verify_appid_stats_application_grp(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'application_group' is a mandatory argument")



    def test_verify_appid_stats_application_grp(self):


        dict_to_return = {'a':1}

        try:
            verify_appid_stats_application_grp(device=self.mocked_obj, application_group="abc", statistics_dict=dict_to_return)
        except Exception as err:
            self.assertEqual(err.args[0], "No application group Statistics Info available")
        self.assertEqual(verify_appid_stats_application_grp(device=self.mocked_obj, application_group="abc", validate=False, statistics_dict=dict_to_return), False)


        dict_to_return = {'appid-application-group-statistics':
                            {'application-name':"xx"}
                         }

        try:
            verify_appid_stats_application_grp(device=self.mocked_obj, application_group="abc", statistics_dict=dict_to_return)
        except Exception as err:
            self.assertEqual(err.args[0], "Application Group name not found")
        self.assertEqual(verify_appid_stats_application_grp(device=self.mocked_obj, application_group="abc", validate=False, statistics_dict=dict_to_return), False)

        dict_to_return = {'appid-application-group-statistics-usp':
                                   [{'application-name': "xx"}, {'application-name': "xz"}]
                         }


        p = patch("jnpr.toby.security.appsecure.appid_commands.get_appid_stats_application_grp", new=MagicMock(return_value=dict_to_return))
        p.start()
        try:
            verify_appid_stats_application_grp(device=self.mocked_obj, application_group="abc")
        except Exception as err:
            self.assertEqual(err.args[0], "Application Group name not found")

        self.assertEqual(verify_appid_stats_application_grp(device=self.mocked_obj, application_group="xx"), True)
        p.stop()
        self.assertEqual(verify_appid_stats_application_grp(device=self.mocked_obj, application_group="abc", validate=False, statistics_dict=dict_to_return),
                         False)

        dict_to_return_2 = {'appid-application-group-statistics-usp': {'application-name': "xx", 'sessions': '10', 'bytes': '10'}}

        self.assertEqual(verify_appid_stats_application_grp(device=self.mocked_obj, application_group="xx", session_count="10", bytes="10", statistics_dict=dict_to_return_2), True)
        self.assertEqual(
            verify_appid_stats_application_grp(device=self.mocked_obj, application_group="xx",
                                               statistics_dict=dict_to_return_2), True)
        self.assertEqual(
            verify_appid_stats_application_grp(device=self.mocked_obj, application_group="xx",
                                               session_count="1", bytes="2",
                                               statistics_dict=dict_to_return_2, validate=False), False)

        try:
            verify_appid_stats_application_grp(device=self.mocked_obj, application_group="xx",
                                               session_count="1", bytes="2",
                                               statistics_dict=dict_to_return_2)
        except Exception as err:
            self.assertEqual(err.args[0], "Statistics are not matching")


    def test_verify_apptrack_counters(self):
        try:
            verify_apptrack_counters()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            verify_apptrack_counters(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "counter_values is None, it is mandatory argument")


        x = {'avt-counters' :
                 {'avt-counter-statistics' : {'name' : ['a', 'b', 'c'], 'value': ['1', '2', '3']

                                             }

                }
             }
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=x)
        self.assertEqual(verify_apptrack_counters(device=self.mocked_obj, counter_values={'a':1, 'c':3}), True)

        try:
            verify_apptrack_counters(device=self.mocked_obj, counter_values={'a': 1, 'c': 4})
        except Exception as err:
            self.assertEqual(err.args[0], "Apptrack Counter verification failed")

        try:
            verify_apptrack_counters(device=self.mocked_obj, counter_values={'a': 1, 'd': 4})
        except Exception as err:
            self.assertEqual(err.args[0], "Apptrack Counter verification failed")

    def test_get_appid_application_system_cache(self):
        try:
            get_appid_application_system_cache()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")



        response1 = {'appid-application-system-cache-information':
                         {'appid-application-system-cache-pic':
                            {'appid-application-system-cache-usp':
                                 {'appid-application': 'HTTP',
                                  'classification-path': 'IP:TCP:HTTP',
                                  'ipv6-address': '5.0.0.1',
                                  'is_encrypted': 'No',
                                  'port': '80',
                                  'protocol': 'TCP',
                                  'virtual-system-identifier': '0'},
                            'pic': '0/0'}}}

        response2 = {'appid-application-system-cache-information': {'a':1}}



        result1 = {'appid-application': 'HTTP',
                   'classification-path': 'IP:TCP:HTTP',
                   'ipv6-address': '5.0.0.1',
                   'is_encrypted': 'No',
                   'pic': '0/0',
                   'port': '80',
                   'protocol': 'TCP',
                   'virtual-system-identifier': '0'}
        a = [result1]
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=response1)
        self.assertEqual(get_appid_application_system_cache(device=self.mocked_obj), a)
        self.mocked_obj.execute_as_rpc_command.return_value = response2
        self.assertEqual(get_appid_application_system_cache(device=self.mocked_obj), {})


    @patch('jnpr.toby.security.appsecure.appid_commands.get_appid_application_system_cache')
    def test_verify_appid_application_system_cache(self, patched_get_appid_application_system_cache=None):
        try:
            verify_appid_application_system_cache()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            verify_appid_application_system_cache(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'application' is a mandatory argument")


        self.assertEqual(verify_appid_application_system_cache(device=self.mocked_obj, application="FTP", negate=True), True)

        try:
            verify_appid_application_system_cache(device=self.mocked_obj, application="FTP")
        except Exception as err:
            self.assertEqual(err.args[0], "Application is not found in cache")

        # Verify from get_appid_application_system_cache getting value
        patched_get_appid_application_system_cache.return_value = [{'appid-application': 'HTTP',
                                                                   'classification-path': 'IP:TCP:HTTP',
                                                                   'ipv6-address': '5.0.0.1',
                                                                   'is_encrypted': 'No',
                                                                   'pic': '0/0',
                                                                   'port': '80',
                                                                   'protocol': 'TCP',
                                                                   'virtual-system-identifier': '0'}]


        self.assertEqual(verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP", ip_adress="5.0.0.1", port="80", encrypted="No",
                                              proto="TCP", virtual_sysid="0", pic="0/0",classification_path="IP:TCP:HTTP"), True)



        self.assertEqual(
            verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP",
                                                  ip_adress="5.0.0.2", negate=True), True)

        self.assertEqual(
            verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP",
                                                  ip_adress="5.0.0.1", encrypted="Yes", negate=True),
            True)

        self.assertEqual(
            verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP",
                                                  ip_adress="5.0.0.1", port="10", encrypted="No",
                                                  proto="TCP", virtual_sysid="1", pic="0/0",
                                                  classification_path="IP:TCP:HTTP", negate=True),
            True)

        self.assertEqual(
            verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP",
                                                  ip_adress="5.0.0.1", port="80", encrypted="No",
                                                  proto="TCP", virtual_sysid="1", pic="0/1",
                                                  classification_path="IP:TCP:HTTP", negate=True),
            True)

        self.assertEqual(
            verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP",
                                                  ip_adress="5.0.0.1", port="80", encrypted="No",
                                                  proto="UDP", virtual_sysid="1", pic="0/0",
                                                  classification_path="IP:TCP:HTTP", negate=True),
            True)

        self.assertEqual(
            verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP",
                                                  ip_adress="5.0.0.1", port="80", encrypted="No",
                                                  proto="TCP", virtual_sysid="1", pic="0/0",
                                                  classification_path="IP:HTTP", negate=True),
            True)

        self.assertEqual(
            verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP",
                                                  ip_adress="5.0.0.1", port="80", encrypted="No",
                                                  proto="TCP", virtual_sysid="2", pic="0/0",
                                                  classification_path="IP:TCP:HTTP", negate=True),
            True)



        try:
            verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP",
                                                  ip_adress="5.0.0.1", port="80", encrypted="No",
                                                  proto="TCP", virtual_sysid="1", pic="0/1",
                                                  classification_path="IP:TCP:HTTP")
        except Exception as err:
            self.assertEqual(err.args[0], "Application system caches are not matching")

        patched_get_appid_application_system_cache.return_value = {}
        self.assertEqual(
            verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP",
                                                  classification_path="IP:TCP:HTTP", negate=True), True)

        try:
            verify_appid_application_system_cache(device=self.mocked_obj, application="HTTP",
                                                  classification_path="IP:TCP:HTTP")
        except Exception as err:
            self.assertEqual(err.args[0], "Application is not found in cache")




if __name__ == '__main__':
    unittest.main()

