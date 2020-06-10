"""
Module testcases_executor.tc_reporter.contexts

Contain necessary Context classes used in template to construct html report.

Classes:
    ContextInfos
    ContextHeader
    ContextGroup
    ContextMethod
    ContextReport

Functions:
    make_errors_dict

Imports:
    from testcases_executor.tc_utils: format_duration
"""
from testcases_executor.tc_utils import format_duration


class ContextInfos(dict):
    """
    A subclass of dict.

    Represent infos context, used to init info_list.html .

    Keys - Values
    ----------
    status: str
        'PASSED' or 'FAILED'.
    status_color: str
        'success' or 'danger' (bootstrap4 colors names).
    n_tests: dict
        number of tests by type (fail, error...).
    duration: str
        duration formated in second or millisecond.
    """

    def __init__(self, status, n_tests, duration):
        """
        Init dict, add color depending of status, update with parameters.

        Parameters
        ----------
            status: str
                'PASSED' or 'FAILED'.
            n_tests: dict
                number of tests by type (fail, error...).
            duration: float
                duration of all tests in second.
        """
        super().__init__()
        if status == 'PASSED':
            self['status_color'] = 'success'
        else:
            self['status_color'] = 'danger'
        self.update({
            'status': status, 'n_tests': n_tests,
            'duration': format_duration(duration)})


class ContextHeader(ContextInfos):
    """
    A subclass of ContextInfos.

    Represent context header with datas needed in template header.html .

    Keys - Values
    ----------
    start_time: str
        start time formated (2020-03-30 12:00:00).
    """

    def __init__(self, status, start_time, n_tests, duration):
        """
        Init ContextInfos and add value for start_time key.

        Parameters
        ----------
            status: str
                'PASSED' or 'FAILED'.
            start_time: datetime
                when tests started.
            n_tests: dict
                number of tests by type (fail, error...).
            duration: float
                duration of all tests in second.
        """
        super().__init__(status, n_tests, duration)
        self['start_time'] = start_time.strftime("%Y-%m-%d %H:%M:%S")


class ContextGroup(ContextInfos):
    """
    A subclass of ContextInfos.

    Represent context group with datas needed in template groups.html .

    Keys - Values
    ----------
    name: str
        group's name.
    testcases: list
        ContextTestCase objects.
    """

    def __init__(self, g_name, status, n_tests, duration, testcases):
        """
        Init ContextInfos and add value for start_time key.

        Parameters
        ----------
            g_name: str
                group's name.
            status: str
                'PASSED' or 'FAILED'.
            n_tests: dict
                number of tests by type (fail, error...).
            duration: float
                duration of all group's tests in second.
            testcases: list
                ContextTestCase objects.
        """
        super().__init__(status, n_tests, duration)
        self.update({'name': g_name, 'testcases': testcases})


class ContextTestCase(dict):
    """
    A subclass of dict.

    Represent a testcase context with datas needed in template testcase.html .

    Keys - Values
    ----------
    name: str
        testcase's name.
    module: str
        module's name.
    t_methods: list
        ContextMethod objects.
    duration: str
        duration formated in second or millisecond.
    """

    def __init__(self, tc_name, tc_module, duration, t_methods):
        """
        Init dict and update with parameters.

        Parameters
        ----------
            tc_name: str
                testcase's name.
            tc_module: str
                module's name.
            duration: float
                duration of all testcase's tests in second.
            t_methods: list
                ContextMethod objects.
        """
        super().__init__()
        self.update({
            'name': tc_name, 'module': tc_module, 't_methods': t_methods,
            'duration': format_duration(duration)})


class ContextMethod(dict):
    """
    A subclass of dict.

    Represent a method context with datas needed in template test_line.html .

    Keys - Values
    ----------
    status_name: str
        SUCCESS, FAIL, ERROR, SKIP, Unexpected Success or Expected Fail
    status_icon: str
        name of Fontawesome icon.
    status_color: str
        success, warning, danger, or info (bootstrap4 colors names).
    name: str
        test method's name.
    doc: str
        test method's docstring.
    duration: str
        duration formated in second or millisecond.
    """

    def __init__(self, t_method, duration, t_errors):
        """
        Init dict, add status values by checking errors lists and update.

        Parameters
        ----------
            t_method: TestCase's method
                original test method used to construct self.
            duration: float
                duration of all tests in second.
            t_errors: dict
                key t_method -> error, key errors failures... -> list tests.
        """
        super().__init__()
        if t_method in t_errors['failures']:
            self.update({
                'status_name': "FAIL", 'status_icon': "thumbs-o-down",
                'status_color': "warning", 'error': t_errors[t_method]})
        elif t_method in t_errors['errors']:
            self.update({
                'status_name': "ERROR", 'status_icon': "times-circle",
                'status_color': "danger", 'error': t_errors[t_method]})
        elif t_method in t_errors['skipped']:
            self.update({
                'status_name': "SKIP", 'status_icon': "cut",
                'status_color': "info", 'error': t_errors[t_method]})
        elif t_method in t_errors['exp_fails']:
            self.update({
                'status_name': "Expected Fail", 'status_icon': "stop-circle-o",
                'status_color': "danger", 'error': t_errors[t_method]})
        else:
            self.update({'status_color': 'success', 'error': None})
            if t_method in t_errors['unex_suc']:
                self.update({
                    'status_name': "Unexpected Success",
                    'status_icon': 'hand-stop-o'})
            else:
                self.update({
                    'status_name': "SUCCESS", 'status_icon': 'thumbs-o-up'})
        self.update({
            'name': t_method._testMethodName, 'doc': t_method._testMethodDoc,
            'duration': format_duration(duration)})


def make_errors_dict(failures, errors, skipped, expFails, unexpSucc):
    """
    Construct t_errors dict used to init ContextMethod in init ContextReport.

    Parameters
    ----------
        failures, errors, skipped, expFails, unexpSucc: lists
            errors list from result

    Return
    ----------
        t_errors: dict
            key t_method -> error, key errors failures... -> list tests.
    """
    t_errors = {}
    for error_key, errors_list in [
            ('failures', failures), ('errors', errors),
            ('skipped', skipped),
            ('exp_fails', expFails)]:
        tests = []
        for test, err in errors_list:
            tests.append(test)
            t_errors[test] = err
        t_errors[error_key] = tests
    t_errors['unex_suc'] = unexpSucc
    return t_errors


class ContextReport():
    """
    A class to generate the context used to construct html report file.

    Use result to get necessary datas for header and groups html.

    Attributes
    ----------
    title: str
        report's title.
    header: ContextHeader
        necessary datas for header.html .
    groups: list
        ContextGroup instances with necessary datas for groups.html .
    """

    def __init__(self, project_name, result):
        """
        Constructs all attributes context used result object.

        Parameters
        ----------
            project_name: str
                name used in title.
            result: tc_result.TestCasesResult
                result of tests.
        """
        self.title = f"{project_name} Tests Results"  # title
        self.header = ContextHeader(  # header
            result.status['total'], result.start_time,
            result.n_tests['total'], result.durations['total'])
        t_errors = make_errors_dict(  # errors_dict
            result.failures, result.errors, result.skipped,
            result.expectedFailures, result.unexpectedSuccesses)
        self.groups = []  # groups
        for group, tc_tup in result.test_methods:
            g_testcases = []  # group's testcases
            for testcase, t_methods in tc_tup:
                tc_methods = []  # testcase's methods
                for t_method in t_methods:
                    t_context = ContextMethod(
                        t_method, result.durations['tests'][t_method],
                        t_errors)
                    tc_methods.append(t_context)
                tc_context = ContextTestCase(
                    testcase.__name__, testcase.__module__,
                    result.durations['testcases'][testcase], tc_methods)
                g_testcases.append(tc_context)
            group_context = ContextGroup(
                group.name, result.status['groups'][group],
                result.n_tests['groups'][group],
                result.durations['groups'][group], g_testcases)
            self.groups.append(group_context)
