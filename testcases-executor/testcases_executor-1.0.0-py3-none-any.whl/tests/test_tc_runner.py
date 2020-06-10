"""
Module testcases_executor.tests.test_tc_runner .

Contain TestCase for testcases_executor.tc_runner .

Classes:
    TestTestRunner(TestCase)

Imports:
    from unittest: TestCase, TextTestRunner
    from unittest.mock: patch, call, Mock
    from testcases_executor.tc_runner: TestCasesRunner
    from testcases_executor.tc_result: TestCasesResult
"""
from unittest import TestCase, TextTestRunner
from unittest.mock import patch, call, Mock
from testcases_executor.tc_runner import TestCasesRunner
from testcases_executor.tc_result import TestCasesResult


class TestTestRunner(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_runner.TestCasesRunner .

    Methods
    ----------
    test_init_runner():
        Assert if TestCasesRunner is initialized with good attributes.
    test_run_group_suites():
        Assert stream.writeln calls, if suites runned, properties updated.
    test_run():
        Assert stream.writeln calls, if groups suites runned, result updated.
    """

    @patch("testcases_executor.tc_runner.TextTestRunner.__init__")
    def test_init_runner(self, mock_runner_init):
        """
        Assert if TestCasesRunner is initialized with good attributes.

        Parameters:
        ----------
        mock_runner_init : Mock
            Mock of unittest.TextTestRunner.__init__ .

        Assertions:
        ----------
        assert_called_once_with:
            Assert if TextTestRunner.__init__ is called once with parameter.
        assertIsInstance:
            Assert if obj is instance TextTestRunner.
        """
        obj = TestCasesRunner()
        mock_runner_init.assert_called_once_with(resultclass=TestCasesResult)
        self.assertIsInstance(obj, TextTestRunner)

    def test_run_group_suites(self):
        """
        Assert stream.writeln calls, if suites runned, properties updated.

        Classes:
        ----------
        FakeResult:
            Fake a result to get properties to assert if updated correctly.
        FakeTestOne, FakeTestTwo:
            Fake tests to get __name__ and __module__ properties.
        FakeSuiteOne, FakeSuiteTwo:
            Fake suite with property _tests, to pass init during test.
        FakeGroup:
            Fake group with suites property.

        Assertions:
        ----------
        assertEqual:
            Assert stream.writeln calls, result durations and test_methods.
        assert_has_calls:
            Assert stream.writeln call parameters.
        assertTupleEqual:
            Assert tuple added to result.test_methods .
        """
        class FakeResult():

            def __init__(self):
                self.separator2 = 'separator2'
                self.durations = {
                    'tests': {
                        'test1': 0.3, 'test2': 0.2,
                        'test3': 0.2, 'test4': 0.6},
                    'testcases': {}}
                self.test_methods = []

        class FakeTestOne():
            pass

        class FakeTestTwo():
            pass

        class FakeSuiteOne():
            _tests = ['test1', 'test2', 'test3']

            def __init__(self, result):
                pass

        class FakeSuiteTwo():
            _tests = ['test4']

            def __init__(self, result):
                pass

        test_one, test_two = FakeTestOne, FakeTestTwo
        suite_one, suite_two = FakeSuiteOne, FakeSuiteTwo

        class FakeGroup():

            def __init__(self):
                self.suites = [
                    (test_one, suite_one), (test_two, suite_two)]

        result, group = FakeResult(), FakeGroup()
        obj = TestCasesRunner()
        obj.stream = Mock()
        obj.run_group_suites(result, group)
        self.assertEqual(8, obj.stream.writeln.call_count)
        obj.stream.writeln.assert_has_calls([
            call('separator2'),
            call('\n\x1b[1m --- FakeTestOne ---\x1b[0m'),
            call(
                '\x1b[2m testcases_executor.tests.test_tc_runner.py\x1b[0m\n'),
            call('\n ... \x1b[35m700.0 ms\x1b[0m\n'),
            call('separator2'),
            call('\n\x1b[1m --- FakeTestTwo ---\x1b[0m'),
            call(
                '\x1b[2m testcases_executor.tests.test_tc_runner.py\x1b[0m\n'),
            call('\n ... \x1b[35m600.0 ms\x1b[0m\n')])
        self.assertEqual(result.durations['testcases'][test_one], 0.7)
        self.assertEqual(result.durations['testcases'][test_two], 0.6)
        self.assertEqual(len(result.test_methods), 1)
        self.assertTupleEqual(result.test_methods[0], (
            group, [
                (test_one, ['test1', 'test2', 'test3']),
                (test_two, ['test4'])]))

    @patch("testcases_executor.tc_runner.datetime")
    def test_run(self, mock_datetime):
        """
        Assert stream.writeln calls, if groups suites runned, result updated.

        Classes:
        ----------
        FakeResult:
            Fake a result to get properties to assert if updated correctly.
        FakeGroup:
            Fake group with name property.

        Functions:
        ----------
        add_item_result(result, group):
            Use in run_group_suites.side_effect to update test_methods 2 times.

        Assertions:
        ----------
        assertEqual:
            Assert writeln, run_group_suites, printTotal calls and new result.
        assert_has_calls:
            Assert writeln, run_group_suites, printTotalcall parameters.
        assert_called_once_with:
            Assert resultclass, printErrors, printInfos called with parameter.
        """
        class FakeResult():

            def __init__(self):
                self.separator1 = 'separator1'
                self.separator2 = 'separator2'
                self.start_time = 0
                self.durations = {
                    'testcases': {
                        'TestOne': 3, 'TestTwo': 2,
                        'TestThree': 2, 'TestFour': 6},
                    'groups': {}}
                self.test_methods = []
                self.n_tests = {'groups': {}}
                self.failfast = None
                self.printTotal = Mock()
                self.printErrors = Mock()
                self.printInfos = Mock()
                self.testsRun = 7

        class FakeGroup():

            def __init__(self, g_name):
                self.name = g_name

        group_one, group_two = FakeGroup('group one'), FakeGroup('group two')
        mock_datetime.now.return_value = 'now'
        result = FakeResult()

        def add_item_result(result, group):
            if len(result.test_methods) == 0:
                result.test_methods.append(('group_one', [
                    ('TestOne', ['test1', 'test2', 'test3']),
                    ('TestTwo', ['test4']), ('TestThree', ['test5'])]))
            else:
                result.test_methods.append(('group_two', [
                    ('TestFour', ['test6', 'test7'])]))

        obj = TestCasesRunner()
        obj.resultclass = Mock()
        obj.resultclass.return_value = result
        obj.run_group_suites = Mock()
        obj.run_group_suites.side_effect = add_item_result
        obj.stream = Mock()
        new_result = obj.run([group_one, group_two])
        obj.resultclass.assert_called_once_with(obj.stream)
        self.assertEqual(13, obj.stream.writeln.call_count)
        obj.stream.writeln.assert_has_calls([
            call('\nRunning tests...\n'),
            call('separator1'),
            call('separator1\n'),
            call('\x1b[1m\x1b[2m group one\x1b[0m\n'),
            call('separator2\n \x1b[2m'),
            call('\nseparator1'),
            call('separator1\n'),
            call('\x1b[1m\x1b[2m group two\x1b[0m\n'),
            call('separator2\n \x1b[2m'),
            call('\nseparator1'),
            call('separator1'),
            call('\x1b[1mseparator1\nseparator1\n'),
            call('\n\x1b[1mseparator1\nseparator1\n\x1b[0m')])
        self.assertEqual(obj.run_group_suites.call_count, 2)
        obj.run_group_suites.assert_has_calls([
            call(result, group_one),
            call(result, group_two)])
        result.n_tests['groups'][group_one] = 5
        result.durations['groups'][group_one] = 7
        result.n_tests['groups'][group_two] = 2
        result.durations['groups'][group_two] = 6
        self.assertEqual(result.printTotal.call_count, 3)
        result.printTotal.assert_has_calls([
            call(5, 7), call(2, 6), call(7, 13)])
        result.printErrors.assert_called_once_with()
        self.assertEqual(result.printInfos.call_count, 3)
        result.printInfos.assert_has_calls([
            call((group_one, ['test1', 'test2', 'test3', 'test4', 'test5'])),
            call((group_two, ['test6', 'test7'])), call()])
        self.assertEqual(new_result, result)
