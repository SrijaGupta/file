import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.utils.linux import chaosreader
from jnpr.toby.hldcl.unix.unix import UnixHost
#import chaosreader



# To return response of shell() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.execute = MagicMock()



    def test_find_md5checksum(self):
        try:
            chaosreader.find_md5checksum()
        except Exception as err:
            self.assertEqual(err.args[0], "device and file_name are mandatory arguments")

        lst = [Response("cbahksb")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            chaosreader.find_md5checksum(device=self.mocked_obj, file_name="/tmp/abc.html")
        except Exception as err:
            self.assertEqual(err.args[0], "Not able to find the checksum")

        lst = [Response("8071eb3199b06efef29a2166ef685062  /tmp/abc.html")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        self.assertEqual(chaosreader.find_md5checksum(device=self.mocked_obj, file_name="/tmp/abc.html"), "8071eb3199b06efef29a2166ef685062")



    def test_extract_from_pcap(self):
        try:
            chaosreader.extract_from_pcap()
        except Exception as err:
            self.assertEqual(err.args[0], "device and pcap are mandatory arguments")

        lst = [Response(""), Response("cbahksb")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            chaosreader.extract_from_pcap(device=self.mocked_obj, pcap="/tmp/mirror.pcap")
        except Exception as err:
            self.assertEqual(err.args[0], "Chaosreader ran into an error")

        lst = [Response(""), Response("aslj Creating files a")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        self.assertEqual(chaosreader.extract_from_pcap(device=self.mocked_obj, pcap="/tmp/mirror.pcap"), True)



    def test_extract_html_from_raw_file(self):
        try:
            chaosreader.extract_HTML_from_raw_file()
        except Exception as err:
            self.assertEqual(err.args[0], "device and raw_file are mandatory arguments")

        lst = [Response("cbahksb"), Response("ad")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            chaosreader.extract_HTML_from_raw_file(device=self.mocked_obj, raw_file="/tmp/abc.txt")
        except Exception as err:
            self.assertEqual(err.args[0], "wc -l got an unexpected output")

        lst = [Response(""), Response("10 /tmp/abc.txt"), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            chaosreader.extract_HTML_from_raw_file(device=self.mocked_obj, raw_file="/tmp/abc.txt")
        except Exception as err:
            self.assertEqual(err.args[0], "HTML pattern not found")

        lst = [Response(""), Response("10 /tmp/abc.txt"), Response("20"), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(chaosreader.extract_HTML_from_raw_file(device=self.mocked_obj, raw_file="/tmp/abc.txt"), "/tmp/testing.html")



if __name__ == '__main__':
    unittest.main()
