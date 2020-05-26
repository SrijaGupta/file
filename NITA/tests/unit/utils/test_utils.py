import sys
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from time import sleep as wait
from jnpr.toby.init.init import init

from jnpr.toby.utils.utils import *
import builtins
builtins.t = MagicMock()

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'


def _target_sleep2(*args, **kwargs):
    wait(2)
    return (args, kwargs)

def _target_sleep1():
    wait(1)

def _target_nothing_fast():
    return None


@attr('unit')
class TestRunMultiple(unittest.TestCase):
    def test_run_multiple_backwards_compat(self):
        system = MagicMock(return_value=1)
        system.__name__ = MagicMock(return_value='system')
        list_of_dicts1 = [{'fname': system,
                           'args': ['ping -c 1 foo'],
                           'delay': 1},
                          {'fname': system,
                           'args': ['ping -c 1 foo'],
                           'delay': 1}]
        import builtins
        builtins.t = MagicMock(spec=init)
        t.background_logger = MagicMock()
        self.assertEqual(run_multiple(list_of_dicts1), [1, 1])

    def test_run_multiple_basic_success(self):
        targets = [{'target': _target_sleep2,
                    'args': [1, True, "string"],
                    'kwargs': {'foo': 'bar',
                               'bar': 42}},
                   {'target': _target_sleep1}]
        import builtins
        builtins.t = MagicMock(spec=init)
        t.background_logger = MagicMock()
        results = run_multiple(targets)
        self.assertEqual(results, [((1, True, 'string'),
                                    {'bar': 42, 'foo': 'bar'}),
                                   None])

    def test_run_multiple_basic_with_targets_success(self):
        targets = [{'target': _target_sleep2,
                    'args': [1, True, "string"],
                    'kwargs': {'foo': 'bar',
                               'bar': 42}},
                   {'target': _target_sleep1}]
        import builtins
        builtins.t = MagicMock(spec=init)
        t.background_logger = MagicMock()
        results = run_multiple(targets=targets)
        self.assertEqual(results, [((1, True, 'string'),
                                    {'bar': 42, 'foo': 'bar'}),
                                   None])

    def test_run_multiple_basic_with_list_of_dicts_success(self):
        targets = [{'target': _target_sleep2,
                    'args': [1, True, "string"],
                    'kwargs': {'foo': 'bar',
                               'bar': 42}},
                   {'target': _target_sleep1}]
        import builtins
        builtins.t = MagicMock(spec=init)
        t.background_logger = MagicMock()

        results = run_multiple(list_of_dicts=targets)
        self.assertEqual(results, [((1, True, 'string'),
                                    {'bar': 42, 'foo': 'bar'}),
                                   None])

    def test_run_multiple_timeout_exception(self):
        targets = [{'target': _target_sleep2,
                    'args': [1, True, "string"]},
                   {'target': _target_sleep1}]
        try:
            results = run_multiple(targets, timeout=1.5)
        except RunMultipleException as exc:
            self.assertEqual(exc.results[1], None)
            self.assertEqual(
                str(exc.results[0]),
                "RunMultipleTimeoutException('Timeout after 1.5 seconds. " +
                "Invoked: _target_sleep2(1, True, 'string') Delay: 0')")

    def test_run_multiple_not_callable_exception(self):
        targets = [{'fname': True,
                    'args': ['Ni!']}]
        try:
            results = run_multiple(targets)
        except RunMultipleException as exc:
            self.assertEqual(str(exc.results[0]),
                             "'bool' object is not callable")

    def test_run_multiple_failed_start_exception(self):
        targets = [{'target': _target_nothing_fast}]
        try:
            import builtins
            builtins.t = MagicMock(spec=init)
            t.background_logger = MagicMock()
            results = run_multiple(targets)
        except RunMultipleException as exc:
            self.assertEqual(
                str(exc.results[0]),
                "RunMultipleFailedStartException('Failed to start. " +
                "Invoked: _target_nothing_fast() Delay: 0')")

    def test_run_multiple_exception_print(self):
        targets = [{'fname': True,
                    'args': ['Ni!']}]
        try:
            results = run_multiple(targets)
        except RunMultipleException as exc:
            self.assertEqual(str(exc),
                             'RunMultipleException(\'[TypeError("\'bool\' object is not callable",)]\')')

    def test_run_multiple_missing_target_exception(self):
        targets = [{'not_target': _target_nothing_fast}]
        self.assertRaises(KeyError, run_multiple, targets)

    def test_run_multiple_no_targets(self):
        self.assertRaises(TypeError, run_multiple)
       

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRunMultiple)
    unittest.TextTestRunner(verbosity=2).run(suite)
