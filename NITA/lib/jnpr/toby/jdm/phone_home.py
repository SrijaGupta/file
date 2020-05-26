"""
Python Code for handling Phone Home Related functions. Code that talks to a Phone-Home Server
via HTTP Request commands.

Author(s): Sudhir Akondi (sudhira) with inputs from
                        Thripti Dhananjaya (thriptid)
                        Madhavan Sampath (msampath)

Dependencies:
  * PHS is provided by nginx

"""

import json
import requests

from time import sleep


class  phone_home:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __log_info__(self, message):
        t.log("INFO", "%s: %s" %(self.__class__.__name__, message))

    def __log_warning__(self, message):
        t.log("WARN", "%s: %s" %(self.__class__.__name__, message))

    def __log_error__(self, message):
        t.log("ERROR", "%s: %s" %(self.__class__.__name__, message))

    def __init__(self):
        pass

    def fetch_activation_state(self, dut_ip, webscript, interval=0, wait=0, state=""):
        """
        Function to fetch the activation status of a Phone Home Client using its web ip and
        web script that returns the activation status as json output

        Python Example:
          _state_ = fetch_activation_state(dut_ip='10.204.41.68', webscript='activation_page.py')

          _status_ = fetch_activation_state(dut_ip='10.204.41.68', webscript='activation_page.py'
                                            interval=10, wait=60, state='Bootstrap Complete')

        Robot Example:
          ${state}   Fetch Activation State   dut_ip=10.204.41.68  webscript=activation_page.py

          ${status}  Fetch Activation State   dut_ip=10.204.41.68  webscript=activation_page.py
                                              interval=${0}  wait=${60}  state=Bootstrap Complete

        :params str dut_ip:
          IP Address of the phone-home client i.e. typically a Junos DUT (JDM of nfx250 etc)

        :param str webscript:
          Script on web server of PHC that returns the activation status in json format

        :param int interval:
          Interval in seconds at which to check for status in case of polling method

        :param int wait:
          Total wait time in seconds until the activation state reaches the expected state

        :param str state:
          Expected Activation State of the Phone Home Client

        """
        try:

            self.__log_info__("Fetching Activation State from DUT IP: %s" % dut_ip)
            _state_ = str()
            _http_url_ = "http://%s/%s" % (dut_ip, webscript)

            interval = int(interval)
            wait = int(wait)

            if wait < interval:
                wait = interval

            if wait == 0:

                _res_ = requests.get(_http_url_)
                if _res_.status_code == 200:
                    _output_ = _res_.content
                    self.__log_info__("Type output: %s" % type(_output_))
                    _output_ = _output_.decode("utf-8")
                    self.__log_info__("Received Content: (json): %s" % _output_)
                    _json_data_ = json.loads(_output_)
                    _state_ = _json_data_['state']
                else:
                    raise Exception("Unable to fetch url: %s" % _http_url_)

                return _state_

            else:

                _time_ = 0
                while _time_ <= wait:

                    _res_ = requests.get(_http_url_)
                    if _res_.status_code == 200:
                        _output_ = _res_.content
                        _output_ = _output_.decode("utf-8")
                        self.__log_info__("Type output: %s" % type(_output_))
                        self.__log_info__("Received Content: (json): %s" % _output_)
                        if _output_ != "":
                            _json_data_ = json.loads(_output_)
                            _state_ = _json_data_['state']

                        if _state_ == state:
                            self.__log_info__("Expected State Reached")
                            return True
                    else:
                        raise Exception("Unable to fetch url: %s" % _http_url_)

                    _time_ += interval
                    sleep(interval)

                self.__log_error__("Wait time completed. State did not reach expected value")
                return False

        except Exception as _exception_:
            raise Exception("Exception raised in fetch_activation_status: %s : %s"
                            % (type(_exception_), _exception_))


    def provision_device_on_phs(self, phs_ip, device_serial_id, activation_code,
                                install_image, auth_user, auth_password,
                                prescript="", postscript="",):
        """
        Python function to send http restconf API to provision a Phone Home client on a Phone Home
        Server. This is typially used for provisioning a Junos device on the PHS before making use
        of the PHS to send config/images etc to the PHC

        Python Example:
            _status_ = provision_device_on_phs(phs_ip='10.204.38.161', device_serial_id='DCA00031A02',
                            activation_code='rightcode123', install_image='jinstall-nfx-2......tgz',
                                  auth_user='admin', auth_password='password', prescript='test data')

        Robot Example:
               ${status}  Provision Device On PHS
                          ...   phs_ip=10.204.38.161
                          ...   device_serial_id=DCA00031A02
                          ...   activation_code=rightcode123
                          ...   install_image=jinstall-nfx-2......tgz
                          ...   auth_user=admin
                          ...   auth_password=admin
                          ...   prescript=test data

               Should Be True      ${status}   Failed to Provision DUT on the Phone Home Server

        :param str phs_ip:
          IP Address of the Phone Home Server on which the phc is to be provisioned

        :param str device_serial_id:
          Serial ID of the PHC

        :param str activation_code:
          Activation Code / Secret of the PHC

        :param str install_image:
          Name of the Junos Image file name that is to be loaded on the PHC

        :param str auth_user:
          Authentication User on the PHS, usually administrator user

        :param str auth_password:
          Password for the authentcation user on the PHS

        :param str prescript:
          Script Code in base64 format / text if any. Can be any dummy text if none.

        :param str postscript:
          Script Code in base64 format / text if any. Can be any dummy text if none.
        """
        try:

            self.__log_info__("Attempting to Provision device in PHS")

            _data_ = """
    <device xmlns="http://juniper.net/bootstrap-server">
      <unique-id>{0}</unique-id>
      <activation-code>{1}</activation-code>
      <boot-image><name>{2}</name></boot-image>
      <configuration>
        <config><foobar xmlns="http://juniper.net/junos/12.3R9.4"/></config>
      </configuration>
      <pre-configuration-script>{3}</pre-configuration-script>
      <post-configuration-script>{4}</post-configuration-script>
      <web-hooks>
        <web-hook>
          <name>foo</name>
          <url>http://foo.example.com/handle-bootstrap-server-web-hook</url>
          <opaque-data>
            <bootstrap-device-info xmlns="http://example.com/bootstrap-device-info">
            <foo/></bootstrap-device-info>
          </opaque-data>
        </web-hook>
        <web-hook>
          <name>bar</name>
          <url>http://bar.example.com/handle-bootstrap-server-web-hook</url>
        </web-hook>
      </web-hooks>
    </device>
            """
            _data_ = str.format(_data_, device_serial_id, activation_code, install_image, prescript, postscript)

            _http_url_ = 'http://%s/restconf/data/juniper-bootstrap-server:devices' % phs_ip

            self.__log_info__("URL: %s" % _http_url_)
            self.__log_info__("POST data: %s" % _data_)

            res = requests.post(_http_url_, data=_data_,
                                headers={'Content-Type': 'type = application/yang.action+xml'},
                                auth=(auth_user, auth_password))

            if res.status_code != 201:
                raise Exception("Response Code is not 201 while privisioning device on PHS")

            return True

        except Exception as _exception_:
            raise Exception("Exception raised in provision_device_on_phs: %s : %s"
                            % (type(_exception_), _exception_))

    def remove_device_from_phs(self, phs_ip, device_serial_id, auth_user="admin", auth_password="admin"):
        """
        Function to remove an existing device provisioned on the Phone Home Server

        Python Example:
          _status_ = remove_device_from_phs(phs_ip='10.204.38.161', device_serial_id='DCA00031A02'
                                            auth_user='admin', auth_password='admin')

        Robot Example:
          ${status}  Remove Device From PHS  phs_ip=10.204.38.11  device_serial_id=DCA00031A02
                     ...                     auth_user=admin   auth_password=admin

        :param str phs_ip:
          IP Address of the Phone Home Server on which the phc is to be provisioned

        :param str device_serial_id:
          Serial ID of the PHC

        :param str auth_user:
          Authentication User on the PHS, usually administrator user

        :param str auth_password:
          Password for the authentcation user on the PHS

        """
        try:

            self.__log_info__("Attempting to remove device from PHS")

            _http_url_ = "http://%s/restconf/data/juniper-bootstrap-server:devices/device=%s" \
                         % (phs_ip, device_serial_id)
            self.__log_info__("Http URL in rest: %s" % _http_url_)
            res = requests.get(_http_url_, auth=(auth_user, auth_password))

            if res.status_code == 200:
                self.__log_info__("Device was found on the PHS")
                res = requests.delete(_http_url_, auth=('admin', 'admin'))
                if res.status_code != 204:
                    raise Exception("Failed to delete device from PHS")
                return True
            else:
                self.__log_info__("Device was not found on the PHS")
                return True

        except Exception as _exception_:
            raise Exception("Exception raised in remove_device_from_phs: %s : %s"
                            % (type(_exception_), _exception_))

    def check_status_from_notification_xml(self, phs_ip, device_serial_id, type_msg, status_message):
        try:
            self.__log_info__("Attempting to get the phc state from notification.xml from PHS")

            _status_ = False
            _count_ = 0
            _message_ = []

            cmd = 'http://%s/restconf/data/juniper-bootstrap-server:devices/device=%s/notifications' % (phs_ip, device_serial_id)
            
            while  (_status_ is False) and (_count_ != 20):
                _req_ = requests.get(cmd, auth=('admin', 'admin'))

                with open('/tmp/notification.xml', 'w') as fetch:
                    fetch.write(_req_.text)

                _tree_ = ET.parse('/tmp/notification.xml')
                _root_ = _tree_.getroot()

                if type_msg == 'notification':
                    for notification in _root_.findall('{http://juniper.net/bootstrap-server}notification'):
                        _message_.append(notification.find('{http://juniper.net/bootstrap-server}notification-type').text)
                elif type_msg == 'message':
                    for notification in _root_.findall('{http://juniper.net/bootstrap-server}notification'):
                        _message_.append(notification.find('{http://juniper.net/bootstrap-server}message').text)

                for message in _message_:
                    self.__log_info__("Expected %s is: '%s'" %(type_msg, status_message))
                    if status_message in message:
                        self.__log_info__("%s in notification.xml: '%s'" %(type_msg, status_message))
                        self.__log_info__("Match Found")
                        _status_ = True
                        break
                    self.__log_info__("%s in notification.xml: '%s'" %(type_msg, status_message))

                if _status_ != True:
                    sleep(10)
                    _count_ = _count_ + 1

            return _status_

        except Exception as _exception_:
            raise Exception("Exception raised in check_status_from_notification_XML: %s : %s"
                            % (type(_exception_), _exception_))

    def enter_activation_code_on_phc_webpage(self, dut_ip, webscript, act_code):
        """
        Function to send activation code as POST data to the web page presented by the PHC.

        Python Example:
            _status_ = enter_activation_code_on_phc_webpage(dut_ip='10.204.41.68',
                                                            webscript='activation_page.py',
                                                            act_code='rightcode123')

        Robot Example:
            ${status}  Enter Activation Code On PHC Webpage   dut_ip=10.204.41.68
                                                              webscript=activation_page.py
                       ...                                    act_code=rightcode123

        :param str dut_ip:
          IP Address of the Phone Home Client i.e. junos device

        :param str webscript:
          Web Script name to which POST data is to be sent

        :param str act_code:
          Activation Code to be entered as POST data

        """
        try:
            self.__log_info__("Entering activation code: %s on PHC page of DUT: %s"
                              % (act_code, dut_ip))

            _http_url_ = "http://%s/%s" % (dut_ip, webscript)
            self.__log_info__("Post URL: %s" % _http_url_)
            _post_data_ = {
                "activation_code" : act_code
            }


            _response_ = requests.post(_http_url_, data=_post_data_)
            return _response_

        except Exception as _exception_:
            raise Exception("Exception raised in enter_activation_code_on_phc_webpage: %s : %s"
                            % (type(_exception_), _exception_))
