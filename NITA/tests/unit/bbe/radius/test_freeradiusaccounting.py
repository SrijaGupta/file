import unittest
import builtins
import itertools
from unittest.mock import MagicMock
from unittest.mock import patch
import jnpr.toby.bbe.radius.freeradiusaccounting as freeradiusaccounting

builtins.t = MagicMock()
builtins.t.log = MagicMock()


class TestFreeRadiusAccounting(unittest.TestCase):
    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting")
    def test_init_freeradius_accounting(self, patch_free_radius_accounting):
        self.assertIsInstance(freeradiusaccounting.init_freeradius_accounting(MagicMock()), MagicMock)

    def test_clear_freeradius_accounting_file(self):
        self.assertEqual(freeradiusaccounting.clear_freeradius_accounting_file(MagicMock()), None)

    def test_get_freeradius_accounting_records(self):
        self.assertIsInstance(freeradiusaccounting.get_freeradius_accounting_records(MagicMock()), MagicMock)

    def test_verify_freeradius_accounting_record(self):
        record = {
            "key": "100"
        }
        spec = {
            "different_key": "100"
        }
        self.assertFalse(freeradiusaccounting.verify_freeradius_accounting_record(record, spec))
        del spec["different_key"]
        spec["key"] = 100
        self.assertTrue(freeradiusaccounting.verify_freeradius_accounting_record(record, spec))
        spec["key"] = 105
        self.assertFalse(freeradiusaccounting.verify_freeradius_accounting_record(record, spec))
        spec["key"] = [100, "><", 5]
        self.assertTrue(freeradiusaccounting.verify_freeradius_accounting_record(record, spec))
        spec["key"] = [90, "%>", 5]
        self.assertFalse(freeradiusaccounting.verify_freeradius_accounting_record(record, spec))
        spec["key"] = [110, "%<", 5]
        self.assertFalse(freeradiusaccounting.verify_freeradius_accounting_record(record, spec))
        spec["key"] = [110, "%", 5]
        self.assertFalse(freeradiusaccounting.verify_freeradius_accounting_record(record, spec))
        spec["key"] = [90, ">", 5]
        self.assertFalse(freeradiusaccounting.verify_freeradius_accounting_record(record, spec))
        spec["key"] = [110, "<", 5]
        self.assertFalse(freeradiusaccounting.verify_freeradius_accounting_record(record, spec))
        spec["key"] = [110, "><", 5]
        self.assertFalse(freeradiusaccounting.verify_freeradius_accounting_record(record, spec))

        record["key"] = 0
        spec["key"] = [100, "%", 5]
        with self.assertRaises(ValueError) as context:
            freeradiusaccounting.verify_freeradius_accounting_record(record, spec)
        self.assertIn("Acct record value 0, cannot use percentage operator ", context.exception.args[0])
        spec["key"] = [100, "%>", 5]
        with self.assertRaises(ValueError) as context:
            freeradiusaccounting.verify_freeradius_accounting_record(record, spec)
        self.assertIn("Acct record value 0, cannot use percentage operator ", context.exception.args[0])
        spec["key"] = [100, "%<", 5]
        with self.assertRaises(ValueError) as context:
            freeradiusaccounting.verify_freeradius_accounting_record(record, spec)
        self.assertIn("Acct record value 0, cannot use percentage operator ", context.exception.args[0])

        spec["key"] = [100, "not an operation", 5]
        with self.assertRaises(TypeError) as context:
            freeradiusaccounting.verify_freeradius_accounting_record(record, spec)
        self.assertIn("Unsupported operator in spec", context.exception.args[0])
        spec["key"] = ["wrong num", "of arguments"]
        with self.assertRaises(Exception) as context:
            freeradiusaccounting.verify_freeradius_accounting_record(record, spec)
        self.assertIn("Parameter spec dictionary value list should have 3 items", context.exception.args[0])
        spec["key"] = MagicMock()
        with self.assertRaises(TypeError) as context:
            freeradiusaccounting.verify_freeradius_accounting_record(record, spec)
        self.assertIn("Parameter spec dictionary value should be string or list", context.exception.args[0])
        spec = "Not a dictionary"
        with self.assertRaises(TypeError) as context:
            freeradiusaccounting.verify_freeradius_accounting_record(record, spec)
        self.assertIn("Radius accounting record verification spec should be a dictionary", context.exception.args[0])
        record = "Not a dictionary"
        with self.assertRaises(TypeError) as context:
            freeradiusaccounting.verify_freeradius_accounting_record(record, spec)
        self.assertIn("Radius accounting record should be a dictionary", context.exception.args[0])

    # Test FreeRadiusAccounting class methods

    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting.clear_current_radius_accounting_file")
    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting._get_server_current_ymd")
    def test_init(self, patch_get_server_current_ymd, patch_clear_current_radius_accounting_file):
        server = MagicMock()
        server.shell.return_value.resp = "No such file or directory"
        with self.assertRaises(NotADirectoryError) as context:
            freeradiusaccounting.FreeRadiusAccounting(server)
        self.assertIn("Specified radius accounting data path ", context.exception.args[0])
        server.shell.return_value.resp = ""
        path = "/usr/loca/var/log/radius/redirect"
        freeradiusaccounting.FreeRadiusAccounting(server, path=path)

    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting.clear_current_radius_accounting_file")
    def test_get_server_current_ymd(self, patch_clear_current_radius_accounting_file):
        server = MagicMock()
        server.shell.return_value.resp = "19970908"
        fra = freeradiusaccounting.FreeRadiusAccounting(server)

        fra.server.shell.return_value.resp = "19970908"
        self.assertEqual(fra._get_server_current_ymd(), "19970908")

        fra.server.shell.return_value.resp = ""
        with self.assertRaises(Exception) as context:
            fra._get_server_current_ymd()
        self.assertIn("Failed to get radius server time", context.exception.args[0])

    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting.clear_current_radius_accounting_file")
    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting._file_exists")
    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting._get_server_current_ymd")
    def test_detect_acct_file_change(self, patch_get_server_current_ymd, patch_file_exists, patch_clear_current_radius_accounting_file):
        server = MagicMock()
        server.shell.return_value.resp = ""
        fra = freeradiusaccounting.FreeRadiusAccounting(server)

        fra.last_time = MagicMock()
        self.assertEqual(fra._detect_acct_file_change(), None)

    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting.clear_current_radius_accounting_file")
    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting._get_server_current_ymd")
    def test_file_exists(self, patch_get_server_current_ymd, patch_clear_current_radius_accounting_file):
        server = MagicMock()
        server.shell.return_value.resp = ""
        fra = freeradiusaccounting.FreeRadiusAccounting(server)

        fra.server.shell.return_value.resp = ""
        self.assertTrue(fra._file_exists(MagicMock()))
        fra.server.shell.return_value.resp = "No such file or directory"
        self.assertFalse(fra._file_exists(MagicMock()))

    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting._get_server_current_ymd")
    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting._detect_acct_file_change")
    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting._file_exists")
    def test_clear_current_radius_accounting_file(self, patch_file_exists, patch_detect_acct_file_change, patch_get_server_current_ymd):
        server = MagicMock()
        server.shell.return_value.resp = ""
        fra = freeradiusaccounting.FreeRadiusAccounting(server)

        fra.backup_before_clear = True
        self.assertEqual(fra.clear_current_radius_accounting_file(), None)
        fra.backup_before_clear = False
        self.assertEqual(fra.clear_current_radius_accounting_file(), None)

    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting.clear_current_radius_accounting_file")
    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting._detect_acct_file_change")
    @patch("jnpr.toby.bbe.radius.freeradiusaccounting.FreeRadiusAccounting._get_server_current_ymd")
    def test_get_radius_accounting_records(self, patch_get_server_current_ymd, patch_detect_acct_file_change, patch_clear_current_radius_accounting_file):
        server = MagicMock()
        server.shell.return_value.resp = ""
        fra = freeradiusaccounting.FreeRadiusAccounting(server)

        acct_file = "/path/to/here"
        fra.server.shell.return_value.resp = "\n Acct-Status-Type=Accounting-On\n Acct-Session-Id=value\n\n Acct-Status-Type=Accounting-Off\n Acct-Session-Id=value\n\n"
        self.assertIsInstance(fra.get_radius_accounting_records(acct_file=acct_file), dict)
        self.assertIsInstance(fra.get_radius_accounting_records(asi="value", ast="Accounting-On", acct_file=acct_file), list)
        self.assertEqual(fra.get_radius_accounting_records(asi="value", ast="wrong value", acct_file=acct_file), [])
        self.assertIsInstance(fra.get_radius_accounting_records(asi="value", acct_file=acct_file), dict)
        self.assertEqual(fra.get_radius_accounting_records(asi="wrong value", acct_file=acct_file), {})

if __name__ == "__main__":
    unittest.main()
