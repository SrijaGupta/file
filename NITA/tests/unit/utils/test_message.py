# coding: UTF-8
"""All unit test cases for Message module"""
# pylint: disable=attribute-defined-outside-init

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import unittest
from jnpr.toby.utils.message import message
from mock import MagicMock

class TestMessage(unittest.TestCase):
    """All unit test cases for Message module"""
    def setUp(self):
        """setup before all cases"""
        self.ins = message(name="MESSAGE")
        self.default_os_type = self.ins.os_type
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    def teardown_class(self):
        """teardown after all cases"""
        pass


    @staticmethod
    def test_init_object():
        """test init object with different option"""
        ins = message(level="INFO")
        assert isinstance(ins, message)

    def test_display(self):
        """test display method"""
        all_level_list = ("INFO", "DEBUG", "TRACE", "WARN", "WARNING", "ERR", "ERROR", "CRITICAL")

        for keyword in all_level_list:
            assert self.ins.display(msg="This is a {} message for no terminal color".format(keyword), level=keyword, show_color=False)

        for keyword in all_level_list:
            assert self.ins.display(msg="This is a {} message with terminal color".format(keyword), level=keyword, show_color=True)

        for keyword in all_level_list:
            assert self.ins.display(msg="This is a {} message with color mode not set".format(keyword), level=keyword)

        for keyword in all_level_list:
            assert self.ins.display(msg="This is a {} message print to ROBOT console".format(keyword), level=keyword, console=True)

        assert self.ins.display(msg=True, level="INFO")

        self.ins.os_type = "REDSTAR"
        assert self.ins.display(level="INFO", msg="Unknown OS treat like Linux", show_color=True)
        self.ins.os_type = self.default_os_type

    def test_display_title(self):
        """test display title method"""
        # No title string that only have boundary characters
        assert self.ins.display_title(width=100, boundary_char='-', show_color=False, arround_newline=True)

        # Have title string with option 'title'
        assert self.ins.display_title(msg="This is a title", show_color=True, arround_newline=False)

        # Have title string both by option 'msg'
        assert self.ins.display_title(msg="I'm a title")

        # Have \n around title
        assert self.ins.display_title(msg="I'm a title with arround_newline", arround_newline=True)

        assert self.ins.display_title(msg=True, level="INFO")

    def test_display_step(self):
        """test display step method"""
        msg = self.ins.display_step(level="INFO", msg="This is first step", new_step=True)
        match = re.search(r"Step\s+(\d+):\s+PASS", msg)
        assert match
        assert int(match.group(1)) == 1

        msg = self.ins.display_step(level="INFO", msg="This is first step", first_step=True)
        match = re.search(r"Step\s+(\d+):\s+PASS", msg)
        assert match
        assert int(match.group(1)) == 1

        msg = self.ins.display_step(level="ERR", msg="This is first step")
        match = re.search(r"Step\s+(\d+):\s+FAIL", msg)
        assert match
        assert int(match.group(1)) == 1

        msg = self.ins.display_step(level="WARN", msg="This is new step", new_step=True)
        match = re.search(r"Step\s+(\d+):\s+WARN", msg)
        assert match
        assert int(match.group(1)) == 2

        msg = self.ins.display_step(level="WARN", msg="This is new step", set_step_index=21)
        match = re.search(r"Step\s+(\d+):\s+WARN", msg)
        assert match
        assert int(match.group(1)) == 21

        msg = self.ins.display_step(msg="This is first step with no result checking", level="INFO", first_step=True, show_result=False)
        match = re.search(r"Step\s+\d+:\s+PASS", msg)
        assert not match

        msg = self.ins.display_step(msg="No step index checking", level="INFO", first_step=True, show_result=True, show_step_index=False)
        match = re.search(r"step\s+\d+", msg, re.I)
        assert not match

if __name__ == '__main__':
    #SUITE = unittest.TestLoader().loadTestsFromTestCase(TestMessage)
    #unittest.TextTestRunner(verbosity=2).run(SUITE)
    unittest.main()
