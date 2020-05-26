"""
    Selenium Class
"""
import re
import time
from jnpr.toby.hldcl.windows.windows import Windows
from jnpr.toby.exception.toby_exception import TobyException


class Selenium(Windows):
    """

    """
    def __init__(self, **kwargs):
        """
        :param host:
            **REQUIRED** hostname or IP address of device to telnet to
        :param user:
            *OPTIONAL* Login user name. If not provided will be derived from
            Toby framework defaults.
        :param password:
            *OPTIONAL* Login Password. If not provided will be derived from
            Toby framework defaults.
        :param connect_mode:
            *OPTIONAL* Connection mode to device. Default is telnet. Supported
            value is telnet.
        """
        self.selenium = kwargs.get('selenium', 'disable')
        self.selenium_jar_version = kwargs.get('selenium_jar_version', '3.5.2')
        self.selenium_jar_major_version = ".".join(self.selenium_jar_version.split('.')[:2])
        self.nssm_interactive = kwargs.get('nssm_interactive', 'enable')
        super(Selenium, self).__init__(**kwargs)
        if self.selenium == "enable":
            self.log(message="Trying to start the selenium service")
            self.__start_service_selenium()

    def __download_selenium_jar(self):

        selenium_jar_path = "C:/selenium/selenium-server-standalone-%s.jar" %self.selenium_jar_version
        file_status = self.shell(command="IF EXIST " + selenium_jar_path + " ECHO file found successfully").response()
        if re.search("file found successfully", file_status, re.I):
            grid_path = selenium_jar_path
        else:
            self.log("file not found on device, now attempting to download")
            download_status = self.shell(command='wget http://selenium-release.storage.googleapis.com'
                                                 '/%s/selenium-server-standalone-%s.jar -P '
                                                 'C:/selenium/ 2>&1 | FINDSTR /I /R "error '
                                                 'failed"' % (self.selenium_jar_major_version,
                                                              self.selenium_jar_version),
                                         timeout=180).response()
            if re.search("not recognized as an internal or external command", download_status, re.I) is not None:
                raise TobyException("wget utility not installed, now exiting", host_obj=self)
            elif re.search('(error|failed)', download_status, re.I) is not None:
                raise TobyException("Unable to download selenium-server-standalone-%s.jar"%self.selenium_jar_version,
                                    host_obj=self)
            else:
                grid_path = selenium_jar_path
        return grid_path

    def __create_selenium_script(self):

        script_path = 'C:/selenium/service_script.py'
        service_path = None
        file_status = self.shell(command="IF EXIST " + script_path + " ECHO file found successfully").response()
        if re.search("file found successfully", file_status, re.I):
            service_path = script_path
        else:
            try:
                self.shell(command="type NUL > C:/selenium/service_script.py")
                cmd_list = ['from subprocess import Popen, PIPE',
                            'file_path = "C:/selenium/selenium-server-standalone-%s.jar"'%self.selenium_jar_version,
                            'cmd = "java -jar " + file_path + " -port 5566"', 'cmd_taskkill = "cd C:/windows/system32"',
                            'java_kill_cmd = "taskkill /IM java.exe /F"',
                            'javaaw_kill_cmd = "taskkill /IM javaw.exe /F"',
                            'geckokill_cmd = "taskkill /F /IM geckodriver.exe"',
                            'chromekill_cmd = "taskkill /F /IM chromedriver.exe"',
                            'iekill_cmd = "taskkill /F /IM IEDriverServer.exe"',
                            'taskkill_cmd = Popen(cmd_taskkill,shell=True, stdout=PIPE)',
                            'print(taskkill_cmd.stdout.read())',
                            'kill_java = Popen(java_kill_cmd,shell=True, stdout=PIPE)',
                            'print(kill_java.stdout.read())',
                            'kill_javaaw = Popen(javaaw_kill_cmd, shell=True, stdout=PIPE)',
                            'print(kill_javaaw.stdout.read())',
                            'kill_gecko = Popen(geckokill_cmd, shell=True, stdout=PIPE)',
                            'print(kill_gecko.stdout.read())',
                            'kill_chrome = Popen(chromekill_cmd, shell=True, stdout=PIPE)',
                            'print(kill_chrome.stdout.read())',
                            'kill_ie = Popen(iekill_cmd, shell=True, stdout=PIPE)',
                            'print(kill_ie.stdout.read())',
                            'res = Popen(cmd, shell=True, stdout=PIPE)', 'print(res.stdout.read())']
                for cmd in cmd_list:
                    self.shell(command='echo ' + cmd + ' >> C:/selenium/service_script.py')
                    service_path = script_path
            except Exception as exp:
                raise TobyException("Unable to create service file", host_obj=self)
        return service_path

    def __delete_service_selenium(self):
        try:
            self.shell(command="nssm stop selenium_toby")
            self.shell(command="nssm remove selenium_toby confirm")
            return True
        except Exception as exp:
            raise TobyException("unable to delete service", host_obj=self)

    def __install_selenium_service(self, service_name=None):
        if service_name is None:
            service_name = "selenium_toby"
        service_path = self.__create_selenium_script()
        python_path = self.__check_python_path()
        self.__download_selenium_jar()
        resp = self.shell(command="nssm install " + service_name + " " + python_path + "  " + service_path).response()
        start_resp = self.shell(command="nssm start " + service_name).response()
        started = re.search("SERVICE_RUNNING|The operation completed successfully", start_resp, re.I)
        stopped = re.search("The specified service already exists", resp, re.I)
        if started:
            if self.nssm_interactive == 'enable':
                self.shell(command="nssm set selenium_toby Type SERVICE_INTERACTIVE_PROCESS")
                return True
            else:
                self.shell(command="nssm restart selenium_toby")
                time.sleep(1)
                return True
        elif stopped:
            self.log("service is stopped, Now attempting to cleanup and create new service")
        return False

    def __check_selenium_status(self):

        self.shell(command="cd C:/windows/system32")
        status = self.shell(command="nssm status selenium_toby").response()
        if re.search("SERVICE_RUNNING", status, re.I):
            if self.nssm_interactive == 'enable':
                self.shell(command="nssm set selenium_toby Type SERVICE_INTERACTIVE_PROCESS")
            return 1
        if re.search("SERVICE_STOPPED", status, re.I):
            return 0
        if re.search("not recognized as an internal or external command", status, re.I):
            raise TobyException("nssm utility not installed, exiting now", host_obj=self)
        return -1

    def __start_service_selenium(self):

        status = self.__check_selenium_status()
        if status == 1:
            self.log('Service Already running, Run your tests on port 5566')
            return True
        elif status == 0:
            self.__delete_service_selenium()
            time.sleep(60)
            resp = self.__install_selenium_service()
            return bool(resp)
        else:
            # try to restart the service
            spawn_status = self.__install_selenium_service()
            if spawn_status:
                self.log("Service spawned successfully")
                return True
            else:
                raise TobyException("Unable to create selenium service", host_obj=self)

    def __check_python_path(self):
        try:
            self.shell(command="cd C:/windows/system32")
            resp = self.shell(command="where python").response()
            python_path = resp.splitlines()[0]
            return python_path
        except Exception as exp:
            raise TobyException("Unable to find python path", host_obj=self)