"""
Module testcases_executor.tests.test_tc_parser .

Contain TestCase for testcases_executor.tc_parser .

Classes:
    TestHelpFormatter(TestCase)
    TestParser(TestCase)

Imports:
    from unittest: TestCase
    from unittest.mock: patch
    from argparse: HelpFormatter
    from testcases_executor.tc_parser: TestCasesHelpFormatter, TestCasesParser
"""
from unittest import TestCase
from unittest.mock import patch, call
from argparse import HelpFormatter, ArgumentParser
from testcases_executor.tc_parser import (
    TestCasesHelpFormatter, TestCasesParser)


class TestHelpFormatter(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_parser.TestCasesHelpFormatter .

    Methods
    ----------
    test_init_formatter():
        Assert if TestCasesHelpFormatter is initialized with good kwargs.
    test_add_usage():
        Assert if TestCasesHelpFormatter.add_usage -> HelpFormatter.add_usage .
    test_format_args():
        Assert the return TestCasesHelpFormatter._format_args .
    test_join_parts()
        Assert the return TestCasesHelpFormatter._join_parts .
    """

    @patch("testcases_executor.tc_parser.HelpFormatter.__init__")
    def test_init_formatter(self, mock_formatter_init):
        """
        Assert if TestCasesHelpFormatter is initialized with good kwargs.

        Parameters:
        ----------
        mock_formatter_init : Mock
            Mock of argparse.HelpFormatter.__init__ .

        Assertions:
        ----------
        assert_called_once_with:
            Assert if HelpFormatter.__init__ is called once with good kwargs.
        assertIsInstance:
            Assert if obj is instance HelpFormatter.
        """
        obj = TestCasesHelpFormatter(prog='foo', max_help_position=10)
        mock_formatter_init.assert_called_once_with(
            max_help_position=5,
            prog='\x1b[2mpython -m testcases_executor\x1b[0m\x1b[2m')
        self.assertIsInstance(obj, HelpFormatter)

    @patch("testcases_executor.tc_parser.HelpFormatter.add_usage")
    def test_add_usage(self, mock_formatter_add_usage):
        """
        Assert if TestCasesHelpFormatter.add_usage -> HelpFormatter.add_usage .

        Parameters:
        ----------
        mock_formatter_add_usage : Mock
            Mock of argparse.HelpFormatter.add_usage .

        Assertions:
        ----------
        assert_called_once_with:
            Assert if HelpFormatter.add_usage is called once with good kwargs.
        assertEqual:
            Assert the return of TestCasesHelpFormatter.add_usage .
        """
        mock_formatter_add_usage.return_value = "add_usage called"
        result = TestCasesHelpFormatter().add_usage('usg', 'act', 'grp')
        mock_formatter_add_usage.assert_called_once_with(
            'usg', 'act', 'grp', '\x1b[1m')
        self.assertEqual(result, "add_usage called")

    def test_format_args(self):
        """
        Assert the return TestCasesHelpFormatter._format_args .

        Assertions:
        ----------
        assertEqual:
            Assert if TestCasesHelpFormatter._format_args return '...' .
        """
        self.assertEqual(
            TestCasesHelpFormatter()._format_args('act', 'met'), "...")

    def test_join_parts(self):
        """
        Assert the return TestCasesHelpFormatter._join_parts .

        Assertions:
        ----------
        assertEqual:
            Assert if TestCasesHelpFormatter._format_args have good return.
        """
        for parameter, result in [
                (['foo', ], '\n\x1b[2mfoo\x1b[0m'),
                (['', 'foo\nbar'], '\n\x1b[2m\x1b[0mfoo\nbar'),
                (['', 'foo:\n'], '\n\x1b[2m\x1b[0m\x1b[1mfoo:\n\x1b[0m')]:
            self.assertEqual(
                TestCasesHelpFormatter()._join_parts(parameter), result)


class TestParser(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_parser.TestCasesParser .

    Methods
    ----------
    test_init_parser():
        Assert if TestCasesParser is initialized correctly.
    test_add_args_options():
        Assert if options arguments are added to parser.
    test_add_args_groups():
        Assert groups and testcases arguments are added to parser.
    """

    @patch("testcases_executor.tc_parser.TestCasesParser.add_args_groups")
    @patch("testcases_executor.tc_parser.TestCasesParser.add_args_options")
    @patch("testcases_executor.tc_parser.ArgumentParser.__init__")
    def test_init_parser(self, mock_parser_init, mock_options, mock_groups):
        """
        Assert if TestCasesParser is initialized correctly.

        Parameters:
        ----------
        mock_parser_init : Mock
            Mock of argparse.ArgumentParser.__init__ .
        mock_options: Mock
            Mock of TestCasesParser.add_args_options
        mock_groups: Mock
            Mock of TestCasesParser.add_args_groups

        Assertions:
        ----------
        assert_called_once_with:
            Assert if mocks are called once with good kwargs.
        assertIsInstance:
            Assert if obj is instance ArgumentParser.
        """
        obj = TestCasesParser('tc_groups')
        mock_parser_init.assert_called_once_with(
            formatter_class=TestCasesHelpFormatter, description=''.join([
                'Without argument to run all tests, or with optionnal ',
                'one(s) without option to run group or TestCase tests, or ',
                'with method names in options to a TestCase arg to run ',
                'specific test methods.']),
            epilog='-\n', allow_abbrev=False)
        mock_options.assert_called_once_with()
        mock_groups.assert_called_once_with('tc_groups')
        self.assertIsInstance(obj, ArgumentParser)

    @patch("testcases_executor.tc_parser.TestCasesParser.add_args_groups")
    @patch("testcases_executor.tc_parser.ArgumentParser.add_argument")
    def test_add_args_options(self, mock_add_argument, mock_groups):
        """
        Assert if options arguments are added to parser.

        Parameters:
        ----------
        mock_add_argument : Mock
            Mock of argparse.ArgumentParser.add_argument .
        mock_groups: Mock
            Mock of TestCasesParser.add_args_groups

        Assertions:
        ----------
        assertEqual:
            Assert add_argument called 2 times, optionnals title > Options
        assert_has_calls:
            Assert if add_argument called with good kwargs.
        assertIsInstance:
            Assert if obj is instance ArgumentParser.
        """
        obj = TestCasesParser('tc_groups')
        self.assertEqual(mock_add_argument.call_count, 2)
        mock_add_argument.assert_has_calls([
            call(
                '-h', '--help', action='help', default='==SUPPRESS==',
                help='show this help message and exit'),
            call(
                "-o", "--open", action='store_true',
                help="Open html report in browser after tests.")])
        self.assertEqual(obj._optionals.title, 'Options')

    @patch("testcases_executor.tc_parser.TestCasesParser.add_args_options")
    @patch("testcases_executor.tc_parser.ArgumentParser.add_argument_group")
    def test_add_args_groups(self, mock_add_group, mock_options):
        """
        Assert groups and testcases arguments are added to parser.

        Parameters:
        ----------
        mock_add_group : Mock
            Mock of argparse.ArgumentParser.add_argument_group .
        mock_options: Mock
            Mock of TestCasesParser.add_args_options

        Classes:
        ----------
        FakeTestA:
            A fake testcase with necessary keys in __dict__ for test.
        FakeTestB:
            A fake testcase with necessary keys in __dict__ for test.
        FakeGroup:
            A fake group with necessary attributes to make groups testcases.

        Assertions:
        ----------
        assertEqual:
            Assert mock_add_group.add_argument called 5 times.
        assert_has_calls:
            Assert if mock_add_group.add_argument called with good kwargs.
        """
        class FakeTestA():

            def __init__(self, tc_name):
                self.__dict__ = {
                    '__name__': tc_name, 'test_a': '', 'test_b': '',
                    'no_test': ''}

        class FakeTestB():

            def __init__(self, tc_name):
                self.__dict__ = {
                    '__name__': tc_name, 'test_1': '', 'test_2': '',
                    'test_a': ''}

        class FakeGroup():

            def __init__(self, g_name, g_arg_name, testcases):
                self.name = g_name
                self.arg_name = g_arg_name
                self.testcases = testcases

        tc_groups = [
            FakeGroup('fake group one', 'one', [
                FakeTestA("FakeTest1"), FakeTestB('FakeTest2')]),
            FakeGroup('fake group two', 'two', [
                FakeTestB('FakeTest3')]),
        ]
        TestCasesParser(tc_groups)
        self.assertEqual(mock_add_group().add_argument.call_count, 5)
        mock_add_group().add_argument.assert_has_calls([
            call(
                '-one', action='store_true',
                help='Run all fake group one TestCases.'),
            call(
                '-FakeTest1', choices=['test_a', 'test_b'],
                help='test_a test_b', nargs='*'),
            call(
                '-FakeTest2', choices=['test_1', 'test_2', 'test_a'],
                help='test_1 test_2 test_a', nargs='*'),
            call(
                '-two', action='store_true',
                help='Run all fake group two TestCases.'),
            call(
                '-FakeTest3', choices=['test_1', 'test_2', 'test_a'],
                help='test_1 test_2 test_a', nargs='*')])
