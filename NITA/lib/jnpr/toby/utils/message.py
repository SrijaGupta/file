# coding: UTF-8
# pylint: disable=invalid-name
"""Log related methods

TOBY platform provide t.log() to save and print log msg, and this module inherit from t.log() to
provide more features, such as show colorful string, title string, etc...

There is 2 types to create instance:

+   Inherit from TOBY t handler

    TOBY platform provide global object 't' to print log message (such as t.log, t.log_console, etc...). If import this module in TOBY platform, you
    should INIT like below:

    ```py
    from module.utils.Message import Message

    class MyClass(object):
        self.log = Message(t=t)
        self.log.display(level="INFO", msg="print log")
    ```

    Alternatively, you should inherit like below:

    ```py
    from module.utils.Message import Message

    class MyClass(Message):
        self.display(level="INFO", msg="print log")
    ```

    Above will use t.log() to print message.

+   Directly use this module without TOBY platform

    Below example will print log by "logging" module, it means you can use this module out of TOBY platform

In this module, these options are global that have same behavior:

1.  level - Log level

    Must be one of "INFO", "DEBUG", "ERR", "ERROR", "WARN", "WARNING", "CRITICAL". while
    "show_color=True", "INFO" and "DEBUG" level will print light green msg, and "WARN" print light
    yellow msg, others ("ERR", "CRITICAL", etc...) print red msg.

2.  msg - Log msg

3.  console - whther print to console

    This option is only implemented for TOBY environment. Without TOBY platform, log message always shown to console (stdout), but as default you
    cannot see it in console.
"""
__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import sys
import platform

from jnpr.toby.init.init import init


class message(object):
    """Message class"""
    def __init__(self, name="", level="INFO", show_color=False, console=False):
        """Init
        :param str name:
            *OPTIONAL* log prefix string such as device name, module name to separate log type

        :param bool show_color:
            *OPTIONAL* default value to set whether print colorful message

        :param bool console:
            *OPTIONAL* default value to set whether print message to console. This option is important for TOBY platform. As default, TOBY platform
                       will not display log to console because all logs shown in .html report. If you want print to console, just set this option True
        """
        self.toby_init = init()

        self.level = level
        self.console = console

        self.show_color = show_color
        self.os_type = platform.platform().split(r'-')[0].upper()
        self.linux_color_set = {
            "INFO":             "1;36m",       # Light green
            "TRACE":            "1;36m",       # Light green
            "DEBUG":            "1;36m",       # Light green
            "WARN":             "1;35m",       # Pink and bold
            "WARNING":          "1;35m",       # Pink and bold
            "ERR":              "1;31m",       # Red and bold
            "ERROR":            "1;31m",       # Red and bold
            "CRITICAL":         "1;31m",       # Red and bold
        }

        self.windows_color_set = {
            "INFO":             0x0B,          # Light green
            "TRACE":            0x0B,          # Light green
            "DEBUG":            0x0B,          # Light green
            "WARN":             0x0D,          # Pink and bold
            "WARNING":          0x0D,          # Pink and bold
            "ERR":              0x0C,          # Red and bold
            "ERROR":            0x0C,          # Red and bold
            "CRITICAL":         0x0C,          # Red and bold
        }

        self.step_num = 0

    def display(self, msg=None, level="INFO", **kwargs):
        """Print colorful string on screen

        All level are as below, the importance from top to bottom. Low level will display all
        higher level's message. For example: default level 'info' will print 'CRITICAL',
        'ERROR', 'WARNING' and 'INFO' messages.

            + CRITICAL
            + ERROR or ERR
            + WARNING or WARN
            + INFO
            + DEBUG
            + TRACE

        :param str msg/message:
            **REQUIRED** string will be print

        :param bool show_color:
            *OPTIONAL* If True, log will displayed with color. and False will print plain-text.
                       default is None, it means this option same as self.show_color attribute

        :return: Return pring msg string or False
        """
        options = {}
        options["msg"] = msg
        options["level"] = str(level).upper()
        options["show_color"] = kwargs.get("show_color", self.show_color)
        options["console"] = kwargs.get("console", self.console)

        assert options["level"] in ('INFO', 'WARN', 'WARNING', 'ERR', 'ERROR', 'CRITICAL', 'DEBUG', "TRACE")

        if options["level"] in ("ERR", "CRITICAL"):
            options["level"] = "ERROR"

        if options["level"] == "TRACE":
            options["level"] = "DEBUG"

        if options["level"] == "WARNING":
            options["level"] = "WARN"

        # default behavior is linux like
        if self.os_type not in ("LINUX", "FREEBSD", "WIN"):
            self.os_type = "LINUX"

        if self.os_type in ("LINUX", "FREEBSD"):
            if options["show_color"] is True:
                msg = "\x1B[{}{}\x1B[0m".format(self.linux_color_set[level], str(options["msg"]))
            self.toby_init.log(message=msg, level=options["level"], console=options["console"])

        return msg

    def display_title(self, msg=None, **kwargs):
        """print given string like a title

        What's title line? It means given string in center and have many special character around,
        and title line always upper case

        :param str msg:
            *OPTIONAL* msg string. if no given string, this method just print boundary_char

        :param int width:
            *OPTIONAL* line length. it must be an integer

        :param bool show_color:
            *OPTIONAL* like display method to decide whether display colorful title

        :param str boundary_char:
            *OPTIONAL* around char

        :param arround_new_line:
            *OPTIONAL* add '\\n' to add blank line

        :return: Return pring msg string or False
        """
        options = {}
        options["msg"] = msg
        options["show_color"] = kwargs.get("show_color", self.show_color)
        options["width"] = kwargs.get("width", 80)
        options["boundary_char"] = kwargs.get("boundary_char", "=")
        options["arround_newline"] = kwargs.get("arround_newline", False)
        options["console"] = kwargs.get("console", self.console)

        if options["msg"] is None:
            msg = options["boundary_char"] * options["width"]
        else:
            # add space around title
            msg = " {} ".format(str(options["msg"]))
            msg = msg.upper().center(options["width"], options["boundary_char"])

            if options["arround_newline"] is True:
                msg = "\n{}\n".format(msg)

        self.display(msg=msg, show_color=options["show_color"], console=options["console"])
        return msg

    def display_step(self, msg, level="INFO", **kwargs):
        """Print message with step info

        Will print message like below:

            self.display_step(level="INFO", msg="Testing something", first_step=True)
            => "step  1: PASS - Testing something."

            self.display_step(level="ERR", msg="Testing something", new_step=True)
            => "step  2: FAIL - Testing something."

            self.display_step(level="WARN", msg="Testing something", new_step=True)
            => "step  3: WARNING - Testing something."

            self.display_step(level="INFO", msg="Testing something", set_step_index=10)
            => "step 10: PASS - Testing something."

            self.display_step(level="INFO", msg="Do Testing", set_step_index=10, no_result=True)
            => "step 10: Testing something."

        Default step number is 0, but you can set "first_step=True" to set it to 1.

        :param str msg:
            **REQUIRED** message string.

        :param str level:
            *OPTIONAL* Default: INFO

        :param bool first_step:
            *OPTIONAL* Set True means step index restart from 1. Default: False

        :param bool new_step:
            *OPTIONAL* Set True means step index +1. Default: False

        :param bool show_result:
            *OPTIONAL* Set True to show "PASS", "FAIL" "WARNING" in middle of msg. Default: True

        :param bool show_step_index:
            *OPTIONAL* Set True to show "Step 1: " front of msg. Default: True

        :param int step_index:
            *OPTIONAL* Set step index. Default: None

        :return: displayed msg
        """
        options = {}
        options["msg"] = msg
        options["level"] = str(level).upper()
        options["first_step"] = kwargs.get("first_step", False)
        options["new_step"] = kwargs.get("new_step", False)
        options["show_result"] = kwargs.get("show_result", True)
        options["show_step_index"] = kwargs.get("show_step_index", True)
        options["set_step_index"] = kwargs.get("set_step_index", None)
        options["console"] = kwargs.get("console", self.console)

        if options["level"] in ("ERR", "ERROR"):
            result = "FAIL"
        elif options["level"] in ("WARN", "WARNING"):
            result = "WARN"
        else:
            result = "PASS"

        if options["first_step"] is True:
            self.step_num = 1

        if options["new_step"] is True:
            self.step_num += 1

        if options["set_step_index"] is not None:
            self.step_num = int(options["set_step_index"])

        msg_frag = []
        if options["show_step_index"] is True:
            msg_frag.append("Step {:>2d}:".format(self.step_num))

        if options["show_result"] is True:
            msg_frag.append(result)
            msg_frag.append("-")

        msg_frag.append(str(options["msg"]))
        msg = " ".join(msg_frag)

        self.display(level=options["level"], msg=msg, console=options["console"])
        return msg
