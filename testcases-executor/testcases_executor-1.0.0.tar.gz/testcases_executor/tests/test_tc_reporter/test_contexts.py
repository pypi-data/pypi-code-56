"""
Module testcases_executor.tests.test_tc_reporter.test_contexts .

Contain TestCase for testcases_executor.tc_reporter.contexts .

unittest.TestCase sublasses:
    TestContextInfos
    TestContextHeader
    TestContextGroup
    TestContextTestCase
    TestContextMethod
    TestContextsFunctions
    TestContextReport

Imports:
    from unittest: TestCase
    from unittest.mock: patch, Mock, call
    from testcases_executor.tc_reporter.contexts: (
        ContextInfos, ContextHeader, ContextGroup, ContextTestCase,
        ContextMethod, make_errors_dict, ContextReport)
"""
from unittest import TestCase
from unittest.mock import patch, Mock, call
from testcases_executor.tc_reporter.contexts import (
    ContextInfos, ContextHeader, ContextGroup, ContextTestCase, ContextMethod,
    make_errors_dict, ContextReport)


class TestContextInfos(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextInfos .

    Methods
    ----------
    test_init_context_infos():
        Assert ContextInfos (dict) is initialized with good keys / values.
    """

    @patch("testcases_executor.tc_reporter.contexts.format_duration")
    def test_init_context_infos(self, mock_format_duration):
        """
        Assert ContextInfos (dict) is initialized with good keys / values.

        Parameters:
        ----------
        mock_format_duration : Mock
            Mock of tc_utils.format_duration .

        Assertions:
        ----------
        assert_called_once_with:
            Assert format_duration called once with 'duration'.
        assertDictEqual:
            Assert if obj is the desired dict.
        assertEqual:
            If FAILED, assert values for keys status and status_color.
        """
        mock_format_duration.return_value = 'duration formated'
        obj = ContextInfos('PASSED', 'n_tests', 'duration')
        mock_format_duration.assert_called_once_with('duration')
        self.assertDictEqual(obj, {
            'status': 'PASSED', 'n_tests': 'n_tests',
            'duration': 'duration formated', 'status_color': 'success'})
        obj = ContextInfos('FAILED', 'n_tests', 'duration')
        self.assertEqual(obj['status'], 'FAILED')
        self.assertEqual(obj['status_color'], 'danger')


class TestContextHeader(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextHeader .

    Methods
    ----------
    test_init_context_header():
        Assert ContextHeader (dict) is initialized with good keys / values.
    """

    @patch("testcases_executor.tc_reporter.contexts.ContextInfos.__init__")
    def test_init_context_header(self, mock_context_infos):
        """
        Assert ContextHeader (dict) is initialized with good keys / values.

        Parameters:
        ----------
        mock_context_infos : Mock
            Mock of tc_reporter.contexts.ContextInfos.__init__ .

        Assertions:
        ----------
        assert_called_once_with:
            Assert ContextInfos, strftime called once with parameters.
        assertDictEqual:
            Assert if obj is the desired dict.
        """
        mock_context_infos.return_value = {}
        mock_start_time = Mock()
        mock_start_time.strftime.return_value = 'datetime formatted'
        obj = ContextHeader('status', mock_start_time, 'n_tests', 'duration')
        mock_context_infos.assert_called_once_with(
            'status', 'n_tests', 'duration')
        mock_start_time.strftime.assert_called_once_with("%Y-%m-%d %H:%M:%S")
        self.assertDictEqual(obj, {'start_time': 'datetime formatted'})


class TestContextGroup(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextGroup .

    Methods
    ----------
    test_init_context_group():
        Assert ContextGroup (dict) is initialized with good keys / values.
    """

    @patch("testcases_executor.tc_reporter.contexts.ContextInfos.__init__")
    def test_init_context_group(self,  mock_context_infos):
        """
        Assert ContextGroup (dict) is initialized with good keys / values.

        Parameters:
        ----------
        mock_context_infos : Mock
            Mock of tc_reporter.contexts.ContextInfos.__init__ .

        Assertions:
        ----------
        assert_called_once_with:
            Assert ContextInfos.__init__ called once with parameters.
        assertDictEqual:
            Assert if obj is the desired dict.
        """
        mock_context_infos.return_value = {}
        obj = ContextGroup(
            'group name', 'status', 'n_tests', 'duration', 'TestCases')
        mock_context_infos.assert_called_once_with(
            'status', 'n_tests', 'duration')
        self.assertDictEqual(
            obj, {'name': 'group name', 'testcases': 'TestCases'})


class TestContextTestCase(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextTestCase .

    Methods
    ----------
    test_init_context_testcase():
        Assert ContextTestCase (dict) is initialized with good keys / values.
    """

    @patch("testcases_executor.tc_reporter.contexts.format_duration")
    def test_init_context_testcase(self, mock_format_duration):
        """
        Assert ContextTestCase (dict) is initialized with good keys / values.

        Parameters:
        ----------
        mock_format_duration : Mock
            Mock of tc_utils.format_duration .

        Assertions:
        ----------
        assert_called_once_with:
            Assert format_duration called once with 'duration'.
        assertDictEqual:
            Assert if obj is the desired dict.
        """
        mock_format_duration.return_value = 'duration formated'
        obj = ContextTestCase('TestCase name', 'module', 'duration', 'methods')
        mock_format_duration.assert_called_once_with('duration')
        self.assertDictEqual(obj, {
            'name': 'TestCase name', 'module': 'module',
            't_methods': 'methods', 'duration': 'duration formated'})


class TestContextMethod(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextMethod .

    Methods
    ----------
    test_init_context_method():
        Assert ContextMethod (dict) is initialized with good keys / values.
    """

    @patch("testcases_executor.tc_reporter.contexts.format_duration")
    def test_init_context_method(self, mock_format_duration):
        """
        Assert ContextMethod (dict) is initialized with good keys / values.

        Parameters:
        ----------
        mock_format_duration : Mock
            Mock of tc_utils.format_duration .

        Class:
        ----------
        FakeTestMethod:
            objet with needed test's argument to init ContextMethod.

        Assertions:
        ----------
        assert_called_once_with:
            Assert format_duration called once with 'duration'.
        assertDictEqual:
            Assert if obj is the desired dict depending of test.
        """
        class FakeTestMethod():

            def __init__(self, t_name):
                self._testMethodName = t_name
                self._testMethodDoc = f"{t_name} doc"

        t1, t2 = FakeTestMethod('t1'), FakeTestMethod('t2'),
        t3, t4 = FakeTestMethod('t3'), FakeTestMethod('t4')
        t5, t6 = FakeTestMethod('t5'), FakeTestMethod('t6')
        t_errors = {
            'failures': [t2], 'errors': [t4],
            'skipped': [t1], 'exp_fails': [t6], 'unex_suc': [t3],
            t1: 'error t1', t2: 'error t2', t6: 'error t6', t4: 'error t4'}
        mock_format_duration.return_value = 'duration formated'
        obj = ContextMethod(t2, 'duration', t_errors)  # failures
        mock_format_duration.assert_called_once_with('duration')
        self.assertDictEqual(obj, {
            'status_name': "FAIL", 'status_icon': "thumbs-o-down",
            'status_color': "warning", 'error': 'error t2',
            'name': 't2', 'doc': 't2 doc', 'duration': 'duration formated'})
        obj = ContextMethod(t4, 'duration', t_errors)  # error
        self.assertDictEqual(obj, {
            'status_name': "ERROR", 'status_icon': "times-circle",
            'status_color': "danger", 'error': 'error t4',
            'name': 't4', 'doc': 't4 doc', 'duration': 'duration formated'})
        obj = ContextMethod(t1, 'duration', t_errors)  # skip
        self.assertDictEqual(obj, {
            'status_name': "SKIP", 'status_icon': "cut",
            'status_color': "info", 'error': 'error t1',
            'name': 't1', 'doc': 't1 doc', 'duration': 'duration formated'})
        obj = ContextMethod(t6, 'duration', t_errors)  # Expected Fail
        self.assertDictEqual(obj, {
            'status_name': "Expected Fail", 'status_icon': "stop-circle-o",
            'status_color': "danger", 'error': 'error t6',
            'name': 't6', 'doc': 't6 doc', 'duration': 'duration formated'})
        obj = ContextMethod(t3, 'duration', t_errors)  # Unexpected Success"
        self.assertDictEqual(obj, {
            'status_name': "Unexpected Success", 'status_color': 'success',
            'status_icon': 'hand-stop-o', 'error': None,
            'name': 't3', 'doc': 't3 doc', 'duration': 'duration formated'})
        obj = ContextMethod(t5, 'duration', t_errors)  # Success
        self.assertDictEqual(obj, {
            'status_name': "SUCCESS", 'status_color': 'success',
            'status_icon': 'thumbs-o-up', 'error': None,
            'name': 't5', 'doc': 't5 doc', 'duration': 'duration formated'})


class TestContextsFunctions(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts function make_errors_dict.

    Methods
    ----------
    test_make_errors_dict():
        Assert if make_errors_dict return desired dict.
    """

    def test_make_errors_dict(self):
        """
        Assert if make_errors_dict return desired dict.

        Assertions:
        ----------
        assertDictEqual:
            Assert if t_errors is the desired dict.
        """
        failures = [('t1', 'fail t1')]
        errors = [('t3', 'error t3')]
        skipped = [('t2', 'skip t2')]
        expFails = [('t6', 'fail t6')]
        unexpSucc = [('t7', 'fail t7')]
        t_errors = make_errors_dict(
            failures, errors, skipped, expFails, unexpSucc)
        self.assertDictEqual(t_errors, {  # make_errors_dict
            't1': 'fail t1', 'failures': ['t1'], 't3': 'error t3',
            'errors': ['t3'], 't2': 'skip t2', 'skipped': ['t2'],
            't6': 'fail t6', 'exp_fails': ['t6'],
            'unex_suc': [('t7', 'fail t7')]})


class TestContextReport(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextReport .

    Methods
    ----------
    test_init_context_report():
        Assert ContextReport object is initialized with good attributes.
    """

    @patch("testcases_executor.tc_reporter.contexts.ContextHeader")
    @patch("testcases_executor.tc_reporter.contexts.make_errors_dict")
    @patch("testcases_executor.tc_reporter.contexts.ContextMethod")
    @patch("testcases_executor.tc_reporter.contexts.ContextTestCase")
    @patch("testcases_executor.tc_reporter.contexts.ContextGroup")
    def test_init_context_report(
            self, mock_group, mock_tc, mock_method, mock_errors_dict,
            mock_header):
        """
        Assert ContextReport object is initialized with good attributes.

        Parameters:
        ----------
        mock_group : Mock
            Mock of ContextGroup .
        mock_tc : Mock
            Mock of ContextTestCase .
        mock_method : Mock
            Mock of ContextMethod .
        mock_errors_dict : Mock
            Mock of make_errors_dict .
        mock_header : Mock
            Mock of ContextHeader .

        Classes:
        ----------
        FakeGroup:
            Fake group with name property.
        FakeTestCase 1 2 3 4:
            Fake TestCase to get __name__ and __module__ properties.
        FakeResult:
            Fake a result to get needed properties to init obj correctly.

        Assertions:
        ----------
        assertEqual:
            Assert title header content, mocks group tc method call count.
        assert_called_once_with:
            Assert ContextHeader make_errors_dict called once with parameter.
        assert_has_calls:
            Assert mocks group tc method calls parameters.
        assertListEqual:
            Assert groups attribute value ( obj.groups).
        """
        class FakeGroup():

            def __init__(self, g_name):
                self.name = g_name

        group_one, group_two = FakeGroup('group one'), FakeGroup('group two')

        class FakeTestCase1():
            pass

        class FakeTestCase2():
            pass

        class FakeTestCase3():
            pass

        class FakeTestCase4():
            pass

        class FakeResult():

            def __init__(self):
                self.status = {
                    'total': 'status total', 'groups': {
                        group_one: 'status group 1',
                        group_two: 'status group 2'}}
                self.start_time = 'start time'
                self.durations = {
                    'testcases': {
                        FakeTestCase1: 3, FakeTestCase2: 2,
                        FakeTestCase3: 2, FakeTestCase4: 8},
                    'tests': {
                        't1': 5, 't2': 12, 't3': 1, 't4': 3, 't5': 2,
                        't6': 0, 't7': 4},
                    'groups': {
                        group_one: 'duration group 1',
                        group_two: 'duration group 2'},
                    'total': 'duration total'}
                self.test_methods = [
                    (group_one, [
                        (FakeTestCase1, ['t1', 't4', 't3']),
                        (FakeTestCase2, ['t7']), (FakeTestCase3, ['t5'])]),
                    (group_two, [
                        (FakeTestCase4, ['t6', 't2'])])]
                self.n_tests = {'groups': {
                    group_one: 'n_tests group 1',
                    group_two: 'n_tests group 2'}, 'total': 'n_tests total'}
                self.failures = 'failures'
                self.errors = 'errors'
                self.skipped = 'skipped'
                self.expectedFailures = 'expFails'
                self.unexpectedSuccesses = 'unexpSucc'

        result = FakeResult()
        mock_header.return_value = 'Context Header'
        mock_errors_dict.return_value = 'Errors dict'
        mock_method.return_value = 'Context Method'
        mock_tc.return_value = 'Context TestCase'
        mock_group.return_value = 'Context Group'
        obj = ContextReport('project name', result)
        self.assertEqual(obj.title, 'project name Tests Results')
        mock_errors_dict.assert_called_once_with(
            'failures', 'errors', 'skipped', 'expFails', 'unexpSucc')
        mock_header.assert_called_once_with(
            'status total', 'start time', 'n_tests total', 'duration total')
        self.assertEqual(obj.header, 'Context Header')
        self.assertEqual(mock_method.call_count, 7)
        mock_method.assert_has_calls([
            call('t1', 5, 'Errors dict'), call('t4', 3, 'Errors dict'),
            call('t3', 1, 'Errors dict'), call('t7', 4, 'Errors dict'),
            call('t5', 2, 'Errors dict'), call('t6', 0, 'Errors dict'),
            call('t2', 12, 'Errors dict')])
        self.assertEqual(mock_tc.call_count, 4)
        mock_tc.assert_has_calls([
            call(
                'FakeTestCase1',
                'testcases_executor.tests.test_tc_reporter.test_contexts',
                3, ['Context Method', 'Context Method', 'Context Method']),
            call(
                'FakeTestCase2',
                'testcases_executor.tests.test_tc_reporter.test_contexts',
                2, ['Context Method']),
            call(
                'FakeTestCase3',
                'testcases_executor.tests.test_tc_reporter.test_contexts',
                2, ['Context Method']),
            call(
                'FakeTestCase4',
                'testcases_executor.tests.test_tc_reporter.test_contexts',
                8, ['Context Method', 'Context Method'])])
        self.assertEqual(mock_group.call_count, 2)
        mock_group.assert_has_calls([
            call(
                'group one', 'status group 1', 'n_tests group 1',
                'duration group 1',
                ['Context TestCase', 'Context TestCase', 'Context TestCase']),
            call(
                'group two', 'status group 2', 'n_tests group 2',
                'duration group 2', ['Context TestCase'])])
        self.assertListEqual(obj.groups, ['Context Group', 'Context Group'])
