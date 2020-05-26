#!/usr/bin/python
'''
Python wrapper funtion for Jsnap utility tool

Jsnap is a tool to compare snapshots on the system before and after an event
Jsnap works is to compare two xml files and evaluate the result against a configuration file to determine PASS/FAIL.
Below link will provide more info
https://www.juniper.net/techpubs/en_US/junos-snapshot1.0/topics/task/configuration/automation-junos-snapshot-using-on-single-device.html
'''
from robot.api import logger

#import os
import subprocess as sub
#import time
from datetime import datetime

class Jsnapshot(object):
    """Class to provide support for Jsnap in Toby framework
       -Prerequisites:
            To be run on a server where jsnap tool is installed.
            Junos device to be capable to be configured for responding over netconf sessions.

       -Supports XML based verification.
       -Supports user-installed server for remote execution.
       -Provided wrapper support for saving xml-based files for pre, post and compare validation
    """

    def __init__(self, **kwargs):
        self._target = kwargs.get('resource', None)
        self._username = kwargs.get('username', 'regress')
        self._password = kwargs.get('password', 'MaRtInI')

        print("Target: %s" %self._target)
        print("Username: %s" %self._username)

    @classmethod
    def get_identifier(cls, **kwargs):
        """Get identifier. This is to differentiate xml files between two different users.
            - Gets identifier by appending userdefined identifier + username + timestamp"""
        idf = kwargs.get('identifier', None)
        i = datetime.now()
        uid = sub.Popen(["whoami"], stdout=sub.PIPE).communicate()[0]
        ti1 = i.strftime('%y%m%d')
        timestamp = str(idf) + str(uid.rstrip()) + str(ti1)
        return timestamp

    def _clean_jsnap(self, **kwargs):
        """Clean Jsnap.
            -Cleanup jsnap created files after every run. User can explicitly set this option to not cleanup jsnap files
             This is useful if certain xml data needs to be retained across multiple testcases or across upgrades
        """
        _server = kwargs.get('server', None)
        _idf = kwargs.get('identifier', None)

        cmd_clean = 'rm -f ' + '*_' + _idf + '*' + '.xml'

        if _server:
            ccmd = 'ssh -o StrictHostKeyChecking=no ' + self._username + '@' + _server + ' ' + '\"' + cmd_clean + '\"'
            logger.info("Executing CLEANUP JSNAP CMD: %s" %ccmd)
            jcmd = sub.Popen(ccmd, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True, shell=True)
            (out, err) = jcmd.communicate()
        else:
            logger.info("Executing CLEANUP JSNAP CMD: %s" %cmd_clean)
            jcmd = sub.Popen(cmd_clean, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True, shell=True)
            (out, err) = jcmd.communicate()

        logger.info(out)
        logger.info(err)

    def jsnap_cleanup(self, **kwargs):
        """CleaningUP Jsnap files"""

        srvr = kwargs.get('server', None)
        idntf = kwargs.get('identifier', None)

        if not idntf:
            raise AssertionError("Identifier to be defined so as to differentiate snapshot files from other users\n")

        self._clean_jsnap(server=srvr, identifier=idntf)
        return True

    def get_snapshot(self, **kwargs):
        """Get Snapshot.
            - Get snapshot to get snapshot on the device.
            :param target: MANDATORY: Can be specified explicitly or called during initilization.
            :param tag: MANDATORY: Tag is referred to whether getting xml snapshot pre or post, supported tags pre,post
            :param test: MANDATORY: Config file to be specified against which XML data from the DUT is collected.
            :param section: OPTIONAL: Specific section in the config file against which XML data on the DUT is collected
            :param identifier: MANDATORY: Identifier needs to be specified to differentiate xml files.
            :param server: OPTIONAL: Server on which jsnap is installed.
                                     Execution will be remote execution on the server if specified.
            :param username: OPTIONAL: username to connect to device. Default: regress
            :param password: OPTIONAL: password to connect to device. Default: MaRtInI
            :clean_jsnap: OPTIONAL: To cleanup jsnap files after execution
                                    Default is to not cleanup jsnap files during get method
        """
        target = kwargs.get('resource', self._target)
        tag = kwargs.get('tag', None)
        test = kwargs.get('test', None)
        section = kwargs.get('section', None)
        identifier = kwargs.get('identifier', None)
        server = kwargs.get('server', None)
        #usrnme = kwargs.get('username', self._username)
        #passwd = kwargs.get('password', self._password)
        usrnme = kwargs.get('username', 'regress')
        passwd = kwargs.get('password', 'MaRtInI')
        clean_jsnap = kwargs.get('clean_jsnap', 1)

        if not target:
            raise AssertionError("Target DUT needs to be defined \n")
        if not test:
            raise AssertionError("Configuration file for getting snapshots on the device\n")
        if not identifier:
            raise AssertionError("Identifier to be defined so as to differentiate snapshot files from other users\n")
        if not tag:
            raise AssertionError("Tag should be defined as 'pre' or 'post' to identify the time of taking a snapshot\n")

        idtfer = self.get_identifier(identifier=identifier)

        cmd_tmp = 'jsnap --nostricthostkeycheck --snap ' +  tag + '_' + idtfer + ' -l ' + usrnme + ' -p ' + passwd + ' -t ' + target

        if section:
            cmd = cmd_tmp + ' -s ' + section + ' ' + test
        else:
            cmd = cmd_tmp + ' ' + test

        if server:
            scmd = 'ssh -o StrictHostKeyChecking=no ' + self._username + '@' + server + ' ' + '\"' + cmd + '\"'
            logger.info("Executing CMD: %s" %scmd)
            jcmd = sub.Popen(scmd, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True, shell=True)
            (out, err) = jcmd.communicate()
        else:
            logger.info("Executing CMD: %s" %cmd)
            jcmd = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True, shell=True)
            (out, err) = jcmd.communicate()

        logger.info(out)
        logger.info(err)

        errpat = ["Exiting.", "Unable to connect to device", "jsnap: not found", "appears to be missing", "command not found", "The authenticity of host", "FAIL"]

        #try:
        #    not cleanup_jsnap
        #except:
        #    logger.info("Jsnap cleanup is not happening and the file name with %s identifier is retatined" %idtfer)
        #else:
        #    self._clean_jsnap(_server=server, _idf=idtfer)

        if clean_jsnap != 0:
            logger.info("Jsnap cleanup is not happening and the file name with %s identifier is retatined" %idtfer)
        else:
            self._clean_jsnap(server=server, identifier=idtfer)

        for comp in errpat:
            if comp in err:
                raise AssertionError("Keyword failed due to following message in the output: %s" %comp)
        return True

    def check_snapshot(self, **kwargs):
        """Check Snapshot
            Check snapshot on the device by comparing pre,post xml files
            :param target: MANDATORY: Can be specified explicitly or called during initilization.
            :param test: MANDATORY: Config file to be specified against which XML data from the DUT is collected.
            :param section: OPTIONAL: Specific section in the config file against which XML data on the DUT is collected
            :param identifier: MANDATORY: Identifier needs to be specified to differentiate xml files.
            :param server: OPTIONAL: Server on which jsnap is installed.
                                    Execution will be remote execution on the server if specified.
            :param username: OPTIONAL: username to connect to device. Default: regress
            :param password: OPTIONAL: password to connect to device. Default: MaRtInI
            :clean_jsnap: OPTIONAL: To cleanup jsnap files after execution.
                                    Default is to cleanup jsnap files during check method
        """
        target = kwargs.get('resource', self._target)
        test = kwargs.get('test', None)
        section = kwargs.get('section', None)
        identifier = kwargs.get('identifier', None)
        server = kwargs.get('server', None)
        usrname = kwargs.get('username', self._username)
        passwd = kwargs.get('password', self._password)
        clean_jsnap = kwargs.get('clean_jsnap', 0)

        if not target:
            raise AssertionError("Target DUT needs to be defined \n")
        if not test:
            raise AssertionError("Configuration file for comparing snapshots on the device\n")
        if not identifier:
            raise AssertionError("Identifier to be defined so as to differentiate snapshot files from other users\n")

        idtfer = self.get_identifier(identifier=identifier)

        cmd_tmp = 'jsnap --nostricthostkeycheck --check ' + 'pre_' + idtfer + ',' + 'post_' + idtfer + ' -l ' + usrname + ' -p ' + passwd + ' -t ' + target

        if section:
            cmd = cmd_tmp + ' -s ' + section + ' ' + test
        else:
            cmd = cmd_tmp + ' ' + test

        if server:
            scmd = 'ssh -o StrictHostKeyChecking=no ' + self._username + '@' + server + ' ' + '\"' + cmd + '\"'
            logger.info("Executing CMD: %s" %scmd)
            jcmd = sub.Popen(scmd, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True, shell=True)
            (out, err) = jcmd.communicate()
        else:
            logger.info("Executing CMD: %s" %cmd)
            jcmd = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True, shell=True)
            (out, err) = jcmd.communicate()

        logger.info(out)
        logger.info(err)

        errpat = ["Exiting.", "Unable to connect to device", "jsnap: not found", "appears to be missing", "command not found", "The authenticity of host", "FAIL", "no snapfiles"]

        #try:
        #    not cleanup_jsnap
        #except:
        #    logger.info("Jsnap cleanup is not happening and the file name with %s identifier is retatined" %idtfer)
        #else:
        #    self._clean_jsnap(_server=server, _idf=idtfer)

        if clean_jsnap != 0:
            logger.info("Jsnap cleanup is not happening and the file name with %s identifier is retatined" %idtfer)
        else:
            self._clean_jsnap(server=server, identifier=idtfer)

        for comp in errpat:
            if comp in err:
                raise AssertionError("Keyword failed due to following message in the output: %s" %comp)

        #try:
        #    not ("ERROR" in err) or ("ERROR" in out)
        #except:
        #    logger.info("TESTS PASSED and Snapshot check has passed:%s" %err)
        #else:
        #    raise AssertionError("ERROR OBSERVED while comparing snapshot:%s" %err)

        if ("ERROR" in err) or ("ERROR" in out):
            raise AssertionError("ERROR OBSERVED while comparing snapshot:%s" %err)
        else:
            logger.info("TESTS PASSED and Snapshot check has passed:%s" %err)
            return True
