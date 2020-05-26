"""
Chaosreader0.94 utilities
Tool needs to be copied on the VM before running these keywords
Tool location =: '/volume/labtools/lib/Testsuites/SRX/IPS/programs/'
"""
import re


def find_md5checksum(device=None, file_name=None):
    """
    TO find the MD5 Checksum of a file on linux.
    Example :
    Find MD5checksum  device=${server}  file=/var/www/html/1kb.html

    :param str device:
        **REQUIRED** Device handle of the Linux PC
    :param str file_name:
        **REQUIRED** File name with its path whose MD5 checksum needs to be found.
    :return: Returns the MD5 checksum of the given file
    :rtype: str
    """
    if device is None or file_name is None:
        raise Exception("device and file_name are mandatory arguments")

    resp = device.shell(command="md5sum " + file_name).response()
    match = re.search("([a-fA-F\d]{32})\\s+" + file_name +".*", resp, re.DOTALL)

    if not match:
        device.log(level='ERROR', message="Not able to find the checksum")
        raise Exception("Not able to find the checksum")

    md5sum = match.group(1)
    return md5sum


def extract_from_pcap(device=None, pcap=None, flags="-v -r", path_to_chaosreader="/tmp/"):
    """
    To extract Data from the PCAP file using Chaosreader to different raw files.
    Example :
    Extract from PCAP   device=${mirrorpc}    pcap=/tmp/mirror.pcap

    :param str device:
        **REQUIRED** Device handle of the Linux device
    :param str pcap:
        **REQUIRED** Path with the name of the PCAP from which data has to be extracted
    :param str flags:
        *OPTIONAL* Send the required flags for chaosreader in a string.
                   Default = "-v -r"
    :param str path_to_chaosreader:
        *OPTIONAL* Path to the chaosreader file. (just the path)
                   Default = "/tmp/"
    :return: returns True or False
    :rtype: bool
    """
    if device is None or pcap is None:
        raise Exception("device and pcap are mandatory arguments")
    device.shell(command="cd /tmp")

    cmd = path_to_chaosreader + "chaosreader0.94 " + flags + " " + pcap
    output = device.shell(command=cmd)

    if not re.match(".*Creating files.*", output.response(), re.DOTALL):
        device.log(level="ERROR", message="Chaosreader ran into an error")
        raise Exception("Chaosreader ran into an error")

    return True



def extract_HTML_from_raw_file(device=None, raw_file=None, html_file_name="/tmp/testing.html",
                               html_pattern=".*HTML.*"):
    """
    To extract the HTML file from the raw file (which was extracted using the abvove keyword)
    (assuming the HTML file starts with pattern "<!DOCTYPE HTML". Otherwise you can specify a
    different pattern.
    Example :
    Extract HTML from Raw file   device=${mirrorpc}  raw_file=/tmp/session_0001.https.raw1

    :param str device:
        **REQUIRED** Device handle of the Linux device
    :param str raw_file:
        **REQUIRED** Path with the name of the Raw file from which HTML has to be extracted
    :param str html_file_name:
        *OPTIONAL* Name of the new HTML file with the path which is to be extracted.
                   Default : "/tmp/testing.html"
    :param str html_pattern:
        *OPTIONAL* The pattern to send, according to how the HTML file starts. Default assumption
                   is first line starts with ".*HTML.*" Hence the default pattern.
                   Default = ".*HTML.*"
    :return: Returns the name of the HTML file (with path)
    :rtype: str
    """
    if device is None or raw_file is None:
        raise Exception("device and raw_file are mandatory arguments")

    device.shell(command="touch " + html_file_name)

    resp = device.shell(command="wc -l " + raw_file).response()
    match = re.search("([0-9]*)\\s*"+raw_file+".*", resp, re.DOTALL)
    if match is None:
        device.log(level="ERROR", message="wc -l got an unexpected output")
        raise Exception("wc -l got an unexpected output")
    length = int(match.group(1))

    resp = device.shell(command="sed -n '/" + html_pattern + "/=' " + raw_file).response()
    match = re.search("([0-9]+).*", resp, re.DOTALL)
    if match is None:
        device.log(level="ERROR", message="HTML pattern not found")
        raise Exception("HTML pattern not found")
    html_starts = int(match.group(1))

    cmd = "tail -n " + str(length - html_starts + 1) + " " + raw_file + " > " + html_file_name
    device.shell(command=cmd)

    return html_file_name

