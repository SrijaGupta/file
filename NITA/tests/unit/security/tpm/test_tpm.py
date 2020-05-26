import os
import unittest
from unittest.mock import MagicMock, patch
from jnpr.toby.security.tpm.tpm import *
from lxml import etree
import jxmlease

def get_file_path(file_name):
    """
    Method to get the full directory of the filename
    """
    path = os.path.dirname(__file__)
    file = os.path.join(path, file_name)
    in_file = open(file, 'rb')
    return in_file

def read_xml_file(file_name):
    """
    Method to parse the xml file
    """
    xml_obj = etree.parse(get_file_path(file_name))
    xml_data = etree.tostring(xml_obj)
    return xml_data

class TestTpm(unittest.TestCase):
    """
    Unit test for tpm.py
    """

    def test_get_tpm_status(self):
        """
        Method to test get_tpm_status
        """
        device_object = MagicMock()
        xml_data = read_xml_file('tpm_status.xml')
        device_object.node0.cli().response = MagicMock(return_value=xml_data)
        exp_dict = {'TPM': 'yes', 'MEK': 'configured', 'MBK': 'created'}

        self.assertEqual(get_tpm_status(device_object), exp_dict)
        self.assertEqual(get_tpm_status(device_object, parameter='TPM'), 'yes')
        self.assertEqual(get_tpm_status(device_object, parameter='MEK'), 'configured')

    @patch('jnpr.toby.security.tpm.tpm.get_tpm_status')
    def test_verify_tpm_status(self, tpm_status):
        """
        Method to test verify_tpm_status
        """
        device_object = MagicMock()
        tpm_status.return_value = {'TPM': 'yes', 'MEK': 'not-configured', 'MBK': 'not-created'}

        self.assertFalse(verify_tpm_status(device_object, tpm_dict={'TPM': 'yes', 'MEK': 'configured', 'MBK': 'created'}))

    def test_delete_mek(self):
        """
        Method to test delete_mek
        """
        device_object = MagicMock()
        self.assertTrue(delete_mek(device_object))
        self.assertTrue(delete_mek(device_object, node='node0'))

    def test_delete_keypair(self):
        """
        Method to test delete keypair
        """
        device_object = MagicMock()
        self.assertTrue(delete_keypair(device_object))
        self.assertTrue(delete_keypair(device_object, node='node0'))
        self.assertTrue(delete_keypair(device_object, node='node0', filetype='privenc'))

    def test_get_keypair_checksum(self):
        """
        Method to test get_keypair_checksum
        """
        device_object = MagicMock()
        device_object.node0.cli().response = MagicMock(return_value='MD5 (/var/db/certs/common/key-pair/mimosa.privenc) = 58902505f5f38e5b90935b9bb220083a')
        self.assertEqual(get_keypair_checksum(device_object, filename='mimosa.privenc'), '58902505f5f38e5b90935b9bb220083a')

    def test_list_keypair(self):
        """
        Method to test list_keypair
        """
        device_object = MagicMock()
        device_object.node0.shell().response = MagicMock(return_value='mimosa.privenc')

        self.assertEqual(list_keypair(device_object, node='node0'), ['mimosa.privenc', 'mimosa.privenc', 'mimosa.privenc'])

    def test_verify_keypair_is_encrypted(self):
        """
        Method to test verify_keypair_is_encrypted
        """
        device_object = MagicMock()
        device_object.node0.shell().response = MagicMock(return_value='mimosa.privenc')
        self.assertEqual(list_keypair(device_object, node='node0'), ['mimosa.privenc', 'mimosa.privenc', 'mimosa.privenc'])

    def test_set_mek(self):
        """
        Method to test set_mek
        """
        device_object = MagicMock()
        device_object.node0.cli().response = MagicMock(return_value='successfully')
        #self.assertTrue(set_mek(device_object, node='node0', new_pswd='abcdef'))

    def test_change_mek(self):
        """
        Method to test change_mek
        """
        device_object = MagicMock()
        device_object.node0.cli().response = MagicMock(return_value='successfully generated')
        #self.assertTrue(change_mek(device_object, node='node0', new_pswd='abcdef', current_pswd='dfss'))

if __name__ == '__main__':
    unittest.main()
