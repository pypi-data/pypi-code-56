"""
Module testcases_executor.tests.test_main .

Contain TestCase for testcases_executor.__main__ .

Classes:
    TestMain(TestCase)

Imports:
    from unittest: TestCase
    from unittest.mock: patch
    from testcases_executor.__main__: main
"""
from unittest import TestCase
from unittest.mock import patch, Mock
from testcases_executor.__main__ import main


class TestMainFunctions(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for __main__ functions, main.

    Methods
    ----------
    test_main():
        Assert if groups is constructed, parsed and testscases runned.
    """

    @patch('testcases_executor.__main__.TestCasesHtmlReport')
    @patch('testcases_executor.__main__.TestCasesGroups')
    @patch('testcases_executor.__main__.TestCasesParser')
    @patch('testcases_executor.__main__.TestCasesRunner')
    def test_main(self, mock_runner, mock_parser, mock_groups, mock_report):
        """
        Assert if groups is constructed, parsed and testscases runned.

        Call main and assert if a groups is initialized, ...

        Parameters:
        ----------
        mock_runner : Mock
            Mock of TestCasesRunner.
        mock_parser : Mock
            Mock of TestCasesParser.
        mock_groups : Mock
            Mock of TestCasesGroups.
        mock_report : Mock
            Mock of TestCasesHtmlReport.

        Assertions:
        ----------
        assertEqual:
            Assert if groups called once.
        assert_called_once_with:
            parser .parse_args, groups.construct_suites,
            runner .run, report called once with parameter
        """
        groups = Mock()
        mock_groups.return_value = groups
        runner = Mock()
        runner.run.return_value = 'Result'
        mock_runner.return_value = runner
        parse_args = Mock()
        parse_args.open = 'open'
        parser = Mock()
        parser.parse_args.return_value = parse_args
        mock_parser.return_value = parser
        main()
        self.assertEqual(mock_groups.call_count, 1)
        mock_parser.assert_called_once_with(groups)
        parser.parse_args.assert_called_once_with()
        groups.construct_suites.assert_called_once_with(parse_args)
        mock_runner.assert_called_once_with()
        runner.run.assert_called_once_with(groups)
        mock_report.assert_called_once_with('Result', 'open')
