"""The module is used to retrieve and verify FreeRADIUS accounting records.

The following Toby keywords are provided:
    Init freeradius accounting
    Clear freeradius accounting file
    Get freeradius accounting records
    Verify freeradius accounting record

Sample usage:

Import the library into robot file
Library     jnpr.toby.bbe.radius.freeradiusaccouting

An instance of accounting should be initialized. If a radius server
is serving more than one clients or there are more than one radius server
in a test, each requires an instance.
    ${h0_handle}=    Get handle    resource=h0
    ${h0_acct} =     Init Freeradius Accounting    ${h0_handle}

If you want to clear the current radius accounting file, either you want clearer
files or the file grows bigger and old data is not relevant to further tests, you
can cleat the file.
    Clear freeradius accounting file(${h0_acct})


One method of testing it to get a radius accounting record and access its data by
keys, which are radius accounting record attributes. The data can be verified directly
in script by Robot/Toby keywords.

Another way is to use "Verify freeradius accounting record" keyword, e.g. Interim-Update from immediate-update:

    Log    Obtain subscriber acct id
    ${acctid}=     Get    info=get_subscriber_info:radius-accounting-id    devices=r0    args=&{arg}

    Log    Obtain radius acct record
    ${acct_rec_list}=     Get Freeradius Accounting Records      ${h0_acct}      asi=${acctid}    ast=Interim-Update
    ${acct_rec_list_len}=    Get Length    ${acct_rec_list}
    Should Be Equal As Integers    ${acct_rec_list_len}    1    Failed to get one radius Interim-Update record
    ${acct_interim}=    Get From List    ${acct_rec_list}    0

    Log    Verify accounting immedate-update record
    ${spec_d}=    Create Dictionary
    ${spec_l}=    Create List    0    >    5
    Set To Dictionary    ${spec_d}    Acct-Session-Time    ${spec_l}
    Set To Dictionary    ${spec_d}    Acct-Input-Octets=0
    ...                               Acct-Output-Octets=0
    ...                               Acct-Input-Packets=0
    ...                               Acct-Output-Packets=0
    ...                               IPv6-Acct-Input-Octets=0
    ...                               IPv6-Acct-Output-Octets=0
    ...                               IPv6-Acct-Input-Packets=0
    ...                               IPv6-Acct-Output-Packets=0

    ${acct_record_verify}=    Verify Freeradius Accounting Record    ${acct_interim}    ${spec_d}
    Should Be True    ${acct_record_verify}    Radius immediate-update triggered accounting interim-update stats wrong


Another example verifying radius accounting Stop:

    Log    Obtain radius acct stop record
    ${acct_rec_list}=     Get Freeradius Accounting Records      ${h0_acct}      asi=${acctid}    ast=Stop
    ${acct_rec_list_len}=    Get Length    ${acct_rec_list}
    Should Be Equal As Integers    ${acct_rec_list_len}    1    Could not get exactly one radius Stop record
    ${acct_stop}=    Get From List    ${acct_rec_list}    0

    Log    Verify accounting stop record
    ${spec_d}=         Create Dictionary
    ${spec_in}=        Create List    ${packet_count}       >    10
    ${spec_out}=       Create List    ${packet_count}       >    10
    ${spec_v6_in}=     Create List    ${packet_count_v6}    >    10
    ${spec_v6_out}=    Create List    ${packet_count_v6}    >    10

    Set To Dictionary    ${spec_d}    Acct-Input-Packets          ${spec_in}
    Set To Dictionary    ${spec_d}    Acct-Output-Packets         ${spec_out}
    Set To Dictionary    ${spec_d}    IPv6-Acct-Input-Packets     ${spec_v6_in}
    Set To Dictionary    ${spec_d}    IPv6-Acct-Output-Packets    ${spec_v6_out}

    ${acct_record_verify}=    Verify Freeradius Accounting Record    ${acct_stop}    ${spec_d}
    Should Be True    ${acct_record_verify}    Radius accounting stop stats wrong

"""
import re
import os
import time
from jnpr.toby.bbe.version import get_bbe_version

__author__ = ['Benjamin Schurman', 'Yong Wang']
__contact__ = ['bschurman@juniper.net', 'ywang@juniper.net']
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2018-01'
__version__ = get_bbe_version()

# For robot framework
ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
ROBOT_LIBRARY_VERSION = get_bbe_version()


def init_freeradius_accounting(host_handle, client_ip='100.0.0.1', path='/usr/local/var/log/radius/radacct/', clearlog=True):
    """Create FreeRadiusAccounting instance.

    :param host_handle: Radius server device handle, e.g., the return of "Get handle    resource=h0"
    :param client_ip: Radius client IP address, e.g., 100.0.0.1. client_ip is part of the
                      path to accounting files .
    :param path: Absolute path of the accounting data files on radius server, excluding the client ip part.
    :param clearlog: Whether to clear (Today's) accounting log if it exists when this is instantiated.
    :return: An instance of FreeRadiusAccounting.
    """
    return FreeRadiusAccounting(host_handle, client_ip, path, clearlog)


def clear_freeradius_accounting_file(handle):
    """Clear the current accounting file.

    In case when accounting file getting large and the test cases
    do not need old records anymore, the current accounting file
    can be cleared to improve performance.

    :param handle: Instance object returned by init_freeradius_accounting.
    """
    handle.clear_current_radius_accounting_file()



def get_freeradius_accounting_records(handle, asi=None, ast=None, acct_file=None):
    """Get accounting records.

    :param handle: Instance object returned by init_freeradius_accounting.
    :param asi: String. Acct-Session-Id value
    :param ast: String. Acct-Status-Type
                The value of ast can be:
                    Start
                    Stop
                    Interim-Update
                    Accounting-On
                    Accounting-Off
                ast only works together with asi. If ast is specified and asi is not,
                all records are returned.
    :param acct_file: String. An absolute path of accounting file other than default accounting files.
                      It could be space separated more than one files in a string, e.g.,
                      acct_file='/absolutepath/acct-file1 /absolutepath/acct-file2'
    :return:
            If asi and ast are not passed, return all accounting records. Returns empty dict {}
            if there is no record.

            If asi is given but not ast, return dictionary of accounting records. Top level keys
            are Start, Stop, Interim-Update, Accounting-On, and Accounting-Off. Each key has
            an list of dictionary of accounting records. The key does not exist if there is no
            record associated with the key. If there is no record for the asi, returns empty dict {}.

            If both asi and ast are passed, return a list of dictionary of accounting records.
            The list is empty [] if no record is matched.
    """
    return handle.get_radius_accounting_records(asi, ast, acct_file)


def verify_freeradius_accounting_record(record, spec):
    """Verify an radius accounting record.

    To verify a given record like:
        record = {'User-Name': "ngs_pppoev4_tester", 'Acct-Input-Octets': '500096'}

    We may want the User-Name to be exact match, and Acct-Input-Octets to be exact or with some tolerance.

    Case 1: User-Name exact match,  Acct-Input-Octets exact match.
            The spec should be the same as the record, .e.g
            spec = {'User-Name': "ngs_pppoev4_tester", 'Acct-Input-Octets': '500096'}

    Case 2: Acct-Input-Octets can be 100 octets more than the value in record.
            spec = {'User-Name': "ngs_pppoev4_tester", 'Acct-Input-Octets': ['500102', '>', '100']}

    Case 3: Acct-Input-Octets can be 200 octets less than the value in record.
            spec = {'User-Name': "ngs_pppoev4_tester", 'Acct-Input-Octets': ['500102', '<', '200']}

    Case 4: Acct-Input-Octets can be 50 octets more or less than the value in record.
            spec = {'User-Name': "ngs_pppoev4_tester", 'Acct-Input-Octets': ['500102', '><', '50']}

    Case 5: Acct-Input-Octets can be 10% more than the value in record.
            spec = {'User-Name': "ngs_pppoev4_tester", 'Acct-Input-Octets': ['500102', '%>', '10']}

    Case 6: Acct-Input-Octets can be 10% less than the value in record.
            spec = {'User-Name': "ngs_pppoev4_tester", 'Acct-Input-Octets': ['500102', '%<', '10']}

    Case 7: Acct-Input-Octets can be 10% more or less than the value in record.
            spec = {'User-Name': "ngs_pppoev4_tester", 'Acct-Input-Octets': ['500102', '%', '10']}

    :param record: Dictionary of one acct record. A freeradius accounting record to be verified.
    :param spec: Dictionary. Specification used to verify the accounting record.
                 The keys should be acct attribute.
                 A value should be a string or list.
                 When the value is a string, it is verified for equality against the value in record.
                 When the value is a list, it is used to veirify agaisnt the value in record with
                 some tolerance, and the format should be as follow:
                     [value, operator, tolerance]
                     value: expected value to verify against the value in record.
                     operator: used to operate on the value with tolerance to allow some difference
                               when verifying the value in record.
                               To test for equal, no operation is needed, so there is no = operator.
                               Supported operation:
                                   %> The value in record can be x% bigger than the value in spec.
                                   %< The value in record can be x% smaller than the value in spec.
                                   %  The value in record can be x% larger or smaller than the value in spec.
                                   >  The value in record can be bigger than the value in spec by x
                                   <  The value in record can be smaller than the value in spec by x
                                   >< The value in record can be bigger or smaller than the value in spec by x
                     tolerance: a value for tolerance, its meaning depends on operation.

                 Note that the operators are only applicable to integer values.
    :return: True if verification succeeds.
             False if verification fails.
    :raise: Exception if the given record or spec is unexpected.
    """
    if not isinstance(record, dict):
        t.log('ERROR', 'Radius accounting record should be a dictionary')
        raise TypeError('Radius accounting record should be a dictionary')
    if not isinstance(spec, dict):
        t.log('ERROR', 'Radius accounting record verification spec should be a dictionary')
        raise TypeError('Radius accounting record verification spec should be a dictionary')

    for spec_k in spec.keys():
        if spec_k not in record:
            t.log('ERROR', 'Key {} in spec not found in accounting record'.format(spec_k))
            return False

        spec_v = spec[spec_k]
        record_v = record[spec_k]

        if isinstance(spec_v, int):
            spec_v = str(spec_v)

        if isinstance(spec_v, str):
            if not spec_v == record_v:
                t.log("No match: Key={}, spec={}, record={}".format(spec_k, spec_v, record_v))
                return False
            else:
                t.log("Match: Key={}, spec={}, record={}".format(spec_k, spec_v, record_v))
        elif isinstance(spec_v, list):
            if len(spec_v) != 3:
                t.log("ERROR", "list in spec must has exactly 3 items.")
                raise Exception('Parameter spec dictionary value list should have 3 items')

            value = int(spec_v[0])
            op = spec_v[1]
            tol = int(spec_v[2])
            record_v = int(record_v)

            if op not in ['%>', '%<', '%', '>', '<', '><']:
                t.log("ERROR", "Operator in spec not supported")
                raise TypeError('Unsupported operator in spec')

            msg = "Key={}, record={}, spec={}".format(spec_k, record_v, spec_v)
            if op == '%>':
                if record_v == 0:
                    t.log("ERROR", "Acct record value 0, cannot use percentage operator {}".format(msg))
                    raise ValueError("Acct record value 0, cannot use percentage operator {}".format(msg))
                if ((record_v - value) * 100 / value) > tol or record_v - value < 0:
                    t.log("No match: {}".format(msg))
                    return False
            if op == '%<':
                if record_v == 0:
                    t.log("ERROR", "Acct record value 0, cannot use percentage operator {}".format(msg))
                    raise ValueError("Acct record value 0, cannot use percentage operator {}".format(msg))
                if ((value - record_v) * 100 / value) > tol or value - record_v < 0:
                    t.log("No match: {}".format(msg))
                    return False
            if op == '%':
                if record_v == 0:
                    t.log("ERROR", "Acct record value 0, cannot use percentage operator {}".format(msg))
                    raise ValueError("Acct record value 0, cannot use percentage operator {}".format(msg))
                if  (abs((value - record_v) * 100) / value) > tol:
                    t.log("No match: {}".format(msg))
                    return False
            if op == '>':
                if record_v - value > tol or record_v - value < 0:
                    t.log("No match: {}".format(msg))
                    return False
            if op == '<':
                if value - record_v > tol or value - record_v < 0:
                    t.log("No match: {}".format(msg))
                    return False
            if op == '><':
                if abs(value - record_v) > tol:
                    t.log("No match: {}".format(msg))
                    return False

            t.log("Match: {}".format(msg))
        else:
            raise TypeError('Parameter spec dictionary value should be string or list')

    return True


class FreeRadiusAccounting:
    """The class is used to retrieve FreeRADIUS accounting records.

    This class is not designed to be used in scaling tests as
    the accounting data could be large.

    By default, systest FreeRADIUS stores accounting data in
        detailfile = ${radacctdir}/%{Client-IP-Address}/detail-%Y%m%d
    For example, /usr/local/var/log/radius/radacct/100.0.0.1/detail-20180128

    Accounting detail files are crated daily, and date is possible to change
    during a test run. This class detects when date changes during test run and
    in this situation more than one accounting data files are used to retrieve accounting
    records accordingly.

    If accounting file name is in the format of detail-%Y%m%d but resides in non-default
    path, the path can be specified during instance construction and pass in non-default
    parameters of client_ip and path.

    If accounting file name is not in the format of detail-%Y%m%d, you must pass it
    explicitly to get_radius_accounting_records by acct_file parameter.

    One instance of this class is preferred for each radius client and server.
    For example, when a radius server is serving two clients, 100.0.0.1 and 101.0.0.1,
    two instances can be created like:
        h0 = t.get_handle(resource='h0')
        h0acct100 = freeradiusaccouting.FreeRadiusAccounting(h0)
        h0acct101 = freeradiusaccouting.FreeRadiusAccounting(h0, client_ip='101.0.0.1')
    When there are two radius servers in the same test serving clients 100.0.0.1 and
    101.0.0.1 respectively, two instances can be created like:
        h0 = t.get_handle(resource='h0')
        h1 = t.get_handle(resource='h1')
        h0acct100 = freeradiusaccouting.FreeRadiusAccounting(h0)
        h1acct101 = freeradiusaccouting.FreeRadiusAccounting(h1, client_ip='101.0.0.1')

    """

    bak_file_counter = 0

    def __init__(self,
                 server,
                 client_ip='100.0.0.1',
                 path='/usr/local/var/log/radius/radacct/',
                 clearlog=True,
                 backup=False):
        """Init.

        :param server: Radius server device handle, e.g., the return of "Get handle    resource=h0"
        :param client_ip: Radius client IP address, e.g., 100.0.0.1. client_ip is part of the
                          path to accounting files .
        :param path: Absolute path of the accounting data files on radius server, excluding the client ip part.
        :param clearlog: Whether to clear (Today's) accounting log if it exists when this is instantiated.
        :param clearlog: Back up readius record file before clear it up if True.
        """
        #import sys; import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        self.server = server
        self.client_ip = client_ip
        self.path = path
        self.backup_before_clear = backup

        # In case use provided path forget the ending sep
        if not self.path.endswith(os.sep):
            self.path += os.sep

        # Check if path is ok
        path_exists =  self.server.shell(command="ls {}".format(self.path)).resp
        if re.search("No such file or directory", path_exists):
            raise NotADirectoryError('Specified radius accounting data path {} does not exist'.format(self.path))

        # Add client IP to the path
        self.client_path = self.path + self.client_ip + os.sep

        # Time when this is instantiated, normally test suite start time.
        # The intention is to check if accounting file changes to another file if date moves during test run.
        # Only year, month, and day are of interests.
        self.last_time = self._get_server_current_ymd()

        # set it to today's file for now, may include more than one file later if date changes
        self.acct_file = self.client_path + 'detail-' + self.last_time

        # Current active accounting file in use
        self.current_acct_file = self.acct_file

        # It is recommended to clear the accounting log before test cases begin
        # such that leftover from other tests in the log won't cause side effect.
        if clearlog:
            self.clear_current_radius_accounting_file()

    def _get_server_current_ymd(self):
        """Get the radius server current time represented by %Y%m%d

        :return: string value of %Y%m%d
        """
        server_time = self.server.shell(command='date +%Y%m%d').resp

        m = re.match("\d{8}", server_time)
        if not m:
            raise Exception('Failed to get radius server time')

        return m.group(0).strip()

    def _detect_acct_file_change(self):
        """Detect if accounting file changes if day moves one.

        If date changes during test, update self.acct_file by chaining the
        old and new files together for cat.
        """
        ymd_now = self._get_server_current_ymd()

        if ymd_now != self.last_time:
            self.last_time = ymd_now
            new_acct_file = self.client_path + 'detail-' + ymd_now
            # The file is not created by radius server after date change
            # if there is no accounting data to write
            if self._file_exists(new_acct_file):
                self.acct_file = self.acct_file + ' ' + new_acct_file
                self.current_acct_file = new_acct_file

    def _file_exists(self, fname):
        """Tell if an accounting file exists.

        Radius server won't create an accounting file unless there are accounting data
        to be stores. So need to check if file exists.

        :param fname: Absolute path file name.
        :return: True if exists, False if not.
        """
        file_exists = self.server.shell(command="ls {}".format(fname)).resp
        if re.search("No such file or directory", file_exists):
            return False
        return True

    def clear_current_radius_accounting_file(self):
        """Clear the current accounting file.

        In case when accounting file getting large and the test cases
        do not need old records anymore, the current accounting file
        can be cleared to improve performance.
        """
        self._detect_acct_file_change()

        if self._file_exists(self.current_acct_file):
            if self.backup_before_clear:
                bak_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
                bak_file = self.acct_file + \
                           '-freeradiusaccounting-bak-' + \
                           bak_time + \
                           "." + \
                           str(FreeRadiusAccounting.bak_file_counter)
                FreeRadiusAccounting.bak_file_counter += 1
                self.server.shell(command="/bin/cp {} {}; cat /dev/null > {}".format(self.current_acct_file,
                                                                                     bak_file,
                                                                                     self.current_acct_file))
            else:
                self.server.shell(command="cat /dev/null > {}".format(self.current_acct_file))

    def get_radius_accounting_records(self, asi=None, ast=None, acct_file=None):
        """Retrieve accounting records.

        :param asi: String. Acct-Session-Id value
        :param ast: String. Acct-Status-Type
                                    The value of ast can be:
                                    Start
                                    Stop
                                    Interim-Update
                                    Accounting-On
                                    Accounting-Off
                    ast only works together with asi. If ast is specified and asi is not,
                    all records are returned.
        :param acct_file: String. An absolute path of accounting file other than default accounting files.
                          It could be space separated more than one files in a string, e.g.,
                          acct_file='/absolutepath/acct-file1 /absolutepath/acct-file2'
        :return:
                If asi is given, return dictionary of accounting records. Top level keys
                are Start, Stop, Interim-Update, Accounting-On, and Accounting-Off. Each key has
                an list of dictionary of accounting records.
                If both asi and ast are given, return a list of dictionary of accounting records.
                The list could be empty if no record is matched.
                If no match is found for the given asi, an empty dictionary is returned.
                If asi is NOT given, top level keys are values of Acct-Session-Id.
                Under each Acct-Session-Id value, it is the same as when asi is given.
        """

        self._detect_acct_file_change()

        # top level key in returned dictionary is the value of Acct-Session-Id in acct records
        top_key = 'Acct-Session-Id'
        type_key = 'Acct-Status-Type'

        # check if already root before su as acct data files are of permission 0600
        user = self.server.shell(command='whoami')
        if 'root' not in user.resp:
            self.server.su()

        cmd = "cat {}".format(self.acct_file)
        if acct_file:   # user could supply specific acct file instead of using default
            cmd = "cat {}".format(acct_file)

        input_file = self.server.shell(command=cmd).resp

        # Appending a blank line to make sure the last record is terminated
        input_file += '\n'
        tmp_record = {}
        records = {}

        for line in input_file.splitlines():
            #  blank line is the end of record
            if re.match(r'^\s*$', line):
                # Discard empty record
                if not tmp_record:
                    continue

                # If Accounting-On found ignore previous ones unless retrieving On is what is wanted
                if tmp_record[type_key] == 'Accounting-On' and ast != 'Accounting-On':
                    records = {}
                    tmp_record = {}
                    continue

                # print('end of record found, storing data')
                # store the record by type
                if tmp_record[top_key] not in records:
                    records[tmp_record[top_key]] = {}
                if tmp_record[type_key] not in records[tmp_record[top_key]]:
                    records[tmp_record[top_key]][tmp_record[type_key]] = []

                records[tmp_record[top_key]][tmp_record[type_key]].append(tmp_record)

                # reset tmp_record
                tmp_record = {}
            else:
                match_obj = re.match(r'^\s+(\S+)\s*=\s*(\S.*)$', line)
                if match_obj:
                    # put all the keys,value pairs into a dictionary and remove any quotes "
                    tmp_record[match_obj.group(1)] = match_obj.group(2).replace('"', '')

        if asi:
            if asi in records:
                if ast:
                    if ast in records[asi]:
                        return records[asi][ast]
                    else:
                        return []
                else:
                    return records[asi]
            else:
                return {}
        else:
            return records

