"""
Module testcases_executor.tc_result

Contain necessary class to make result for groups of TestCases.

Class:
    TestCasesResult

Imports:
    time
    from unittest: TestResult
    from testcases_executor.tc_utils: (
        format_duration, GREEN, BLUE, RED, YELLOW, MAGENTA, C_RESET,
        BOLD, MUTED, S_RESET)
"""
import time
from unittest import TestResult
from testcases_executor.tc_utils import (
    format_duration, GREEN, BLUE, RED, YELLOW, MAGENTA, C_RESET,
    BOLD, MUTED, S_RESET)


class TestCasesResult(TestResult):
    """
    A subclass of unittest.TestResult .

    Use to save and display tests result.

    Attributes
    ----------
    separator1 (2): str
        Used to separate parts in shell display
    stream: unittest.runner._WritelnDecorator
        object passed in init parameter -> TestCasesRunner.stream
    start_time: datetime (default=0)
        Used to save start datetime.
    test_methods: list
        [(group, [(testcase, test methods), ...]), ...]
    durations: dict
        {'groups': {g: dur}, 'testcases': {tc: dur}, 'tests': {t: dur}}
    n_tests: dict
        {group: {status: number of tests}}

    Methods
    ----------
    startTest(test):
        Called before execute each method test, set test start time.
    addFoo(test_t_stop, test, status):
        Calcul and save test duration, display it with status.
    addSuccess(test):
        Called when a test has completed successfully.
    addError(test, err):
        Called when an error has occurred.
    addFailure(test, err):
        Called when a fail has occurred.
    addSkip(test, reason):
        Called when a test is skipped.
    addExpectedFailure(test, err):
        Called when an expected failure/error occurred.
    addUnexpectedSuccess(test):
        Called when a test was expected to fail, but succeed.
    printErrors():
        Display errors and failures.
    printErrorList(flavour, errors, e_color):
        Display errors or failures list.
    printTotal(run, duration):
        Display total, number of tests and duration.
    get_n_tests(group_tests):
        Get and return all numbers tests by status depending if group or final.
    printInfos(group_tests=None):
        Display at the end, PASS or FAILED and infos (number failed...).
    """

    def __init__(self, stream):
        """
        Init TestResult, constructs all attributes for group result object.

        Parameters
        ----------
            stream: unittest.runner._WritelnDecorator
                sys.stderr with 'writeln' method.
        """
        super().__init__()
        self.separator1 = '=' * 70
        self.separator2 = '-' * 70
        self.stream = stream
        self.start_time = 0
        self.test_methods = []
        self.durations = {'groups': {}, 'testcases': {}, 'tests': {}}
        self.n_tests = {'groups': {}}
        self.status = {'groups': {}}

    def startTest(self, test):
        """
        Called before execute each method test, set test start time.

        Parameters
        ----------
            test: TestCase method
                the test method runned.
        """
        super().startTest(test)
        self.stream.write(test._testMethodName)
        self.stream.write(" ... ")
        self.stream.flush()
        self.test_t_start = time.time()

    def addFoo(self, test_t_stop, test, status):
        """
        Calcul and save test duration, display it with status.

        Parameters
        ----------
            test_t_stop: time
                test time stop.
            test: TestCase method
                the test method runned.
            status: str
                OK, ERROR, FAIL, SKIP....
        """
        t_duration = test_t_stop - self.test_t_start
        self.durations['tests'][test] = round(t_duration, 6)
        duration_str = format_duration(t_duration)
        self.stream.writeln(
            f"{status} ... {MAGENTA}{duration_str}{C_RESET}")
        self.stream.flush()

    def addSuccess(self, test):
        """
        Called when a test has completed successfully.

        Parameters
        ----------
            test: TestCase method
                the test method runned.
        """
        self.addFoo(time.time(), test, f"{GREEN}OK{C_RESET}")

    def addError(self, test, err):
        """
        Called when an error has occurred.

        Parameters
        ----------
            test: TestCase method
                the test method runned.
            err: tuple
                values as returned by sys.exc_info().
        """
        self.addFoo(time.time(), test, f"{RED}ERROR{C_RESET}")
        super().addError(test, err)

    def addFailure(self, test, err):
        """
        Called when a fail has occurred.

        Parameters
        ----------
            test: TestCase method
                the test method runned.
            err: tuple
                values as returned by sys.exc_info().
        """
        self.addFoo(time.time(), test, f"{YELLOW}FAIL{C_RESET}")
        super().addFailure(test, err)

    def addSkip(self, test, reason):
        """
        Called when a test is skipped.

        Parameters
        ----------
            test: TestCase method
                the test method runned.
            reason: str
                represent the reason of skipped.
        """
        self.addFoo(time.time(), test, f"{BLUE}SKIP{C_RESET}")
        super().addSkip(test, reason)

    def addExpectedFailure(self, test, err):
        """
        Called when an expected failure/error occurred.

        Parameters
        ----------
            test: TestCase method
                the test method runned.
            err: tuple
                values as returned by sys.exc_info().
        """
        self.addFoo(time.time(), test, f"{RED}expected failure{C_RESET}")
        super().addExpectedFailure(test, err)

    def addUnexpectedSuccess(self, test):
        """
        Called when a test was expected to fail, but succeed.

        Parameters
        ----------
            test: TestCase method
                the test method runned.
        """
        self.addFoo(time.time(), test, f"{GREEN}unexpected success{C_RESET}")
        super().addUnexpectedSuccess(test)

    def printErrors(self):
        """
        Display errors and failures.
        """
        self.stream.writeln()
        self.printErrorList('ERROR', self.errors, RED)
        self.printErrorList('FAIL', self.failures, YELLOW)

    def printErrorList(self, flavour, errors, e_color):
        """
        Display errors or failures list.

        Parameters
        ----------
            flavour: str
                'ERROR' or 'FAIL'.
            errors: list
                tuples with test in 1st item, err(str) in 2nd.
            e_color: str
                represent a color, green for succces, ...
        """
        for test, err in errors:
            tc_name = test.__class__.__name__
            method_name = test._testMethodName
            test_str = f"{BOLD}{tc_name}{S_RESET}.{method_name}"
            self.stream.writeln(self.separator1)
            self.stream.writeln(
                f"{e_color}{flavour}{S_RESET}: {test_str}")
            self.stream.writeln(self.separator2)
            self.stream.writeln(
                f"{e_color}{err.splitlines()[-1]}{C_RESET}")
            self.stream.writeln(self.separator2)
            self.stream.writeln(f"{MUTED}{err}{S_RESET}")

    def printTotal(self, run, duration):
        """
        Display total, number of tests and duration.

        Parameters
        ----------
            run: int
                number of tests runned.
            duration: time
                duration for all tests.
        """
        s_test = "test"
        if run > 1:
            s_test += "s"
        ran_text = f"Ran {run} {s_test}{S_RESET}"
        self.stream.writeln(
            f"{ran_text} in {MAGENTA}{format_duration(duration)}{C_RESET}")

    def get_n_tests(self, group_tests):
        """
        Get and return all numbers tests by status depending if group or final.

        Parameters
        ----------
            group_tests: tuple or None
                group for first item, associated tests methods for second one.

        Return
        ----------
            dict
                numbers of tests for each status.
        """
        if group_tests is not None:  # for a group
            test_methods = group_tests[1]
            failed, errors, exp_fails, unexp_succ, skipped = 0, 0, 0, 0, 0
            for t_method in test_methods:
                if t_method in [fail[0] for fail in self.failures]:
                    failed += 1
                elif t_method in [err[0] for err in self.errors]:
                    errors += 1
                elif t_method in [efail[0] for efail in self.expectedFailures]:
                    exp_fails += 1
                elif t_method in self.unexpectedSuccesses:
                    unexp_succ += 1
                elif t_method in [skp[0] for skp in self.skipped]:
                    skipped += 1
        else:  # for final total
            failed, errors, exp_fails, unexp_succ, skipped = map(len, (
                self.failures, self.errors, self.expectedFailures,
                self.unexpectedSuccesses, self.skipped))
        return {
            'failed': failed, 'errors': errors, 'skipped': skipped,
            'expectedFails': exp_fails, 'unexpectedSuccesses': unexp_succ}

    def printInfos(self, group_tests=None):
        """
        Save and display for group or final, status and infos.

        Parameters
        ----------
            group_tests: tuple (default: None)
                group for first item, associated tests methods for second one.
        """
        total_dict = self.get_n_tests(group_tests)
        if group_tests is not None:  # save number of tests by category
            self.n_tests['groups'][group_tests[0]].update(total_dict)
        else:
            self.n_tests['total'].update(total_dict)
        infos = []
        errors, failed = total_dict['errors'], total_dict['failed']
        if errors or failed:  # status not successful
            status, status_color = 'FAILED', RED
            if failed:
                infos.append(f"{YELLOW}Failures={failed}{C_RESET}")
            if errors:
                infos.append(f"{RED}Errors={errors}{C_RESET}")
        else:  # status success
            status, status_color = 'PASSED', GREEN
        if group_tests is not None:
            self.status['groups'][group_tests[0]] = status
        else:
            self.status['total'] = status
        self.stream.writeln(f"{status_color}{status}{C_RESET}")
        skipped = total_dict['skipped']
        if skipped:
            infos.append(f"{BLUE}Skipped={skipped}{C_RESET}")
        exp_fails = total_dict['expectedFails']
        if exp_fails:
            infos.append(f"{RED}Expected Failures={exp_fails}{C_RESET}")
        unexp_succ = total_dict['unexpectedSuccesses']
        if unexp_succ:
            infos.append(f"{GREEN}Unexpected Successes={unexp_succ}{C_RESET}")
        if infos:
            self.stream.writeln(f" ({' , '.join(infos)})")
