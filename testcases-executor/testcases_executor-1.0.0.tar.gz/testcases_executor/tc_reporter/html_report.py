"""
Module testcases_executor.tc_reporter.html_report

Contain necessary class to make html report of results for groups of TestCases.

Class:
    TestCasesHtmlReport

Imports:
    from os: getcwd
    from os.path: basename
    from jinja2: Environment, PackageLoader
    from webbrowser: open as browser_open
    from testcases_executor.tc_utils: BOLD, MUTED, S_RESET
    from testcases_executor.tc_reporter.contexts: ContextReport
"""
from os import getcwd
from os.path import basename
from jinja2 import Environment, PackageLoader
from webbrowser import open as browser_open
from testcases_executor.tc_utils import BOLD, MUTED, S_RESET
from testcases_executor.tc_reporter.contexts import ContextReport


class TestCasesHtmlReport():
    """
    A class to generate html report.

    Use result to get context datas and with a base template construct file.
    """

    def __init__(self, result, open_in_browser=False):
        """
        Init env, get template base and context to construct report file.

        Parameters
        ----------
            result: tc_result.TestCasesResult
                result of tests.
            open_in_browser: bool (default: False)
                open or not report in browser.
        """
        result.stream.writeln("Generating html report ...\n")
        env = Environment(
            loader=PackageLoader('testcases_executor.tc_reporter'),
            autoescape=True)    # load template base
        report_template = env.get_template('report_template.html')
        context_report = ContextReport(basename(getcwd()), result)
        with open('./tc_executor_report.html', 'w') as report_file:
            report_file.write(report_template.render(  # html report file
                title=context_report.title, header=context_report.header,
                groups=context_report.groups))
        result.stream.writeln(
            f"---> {BOLD}{MUTED}tc_executor_report.html{S_RESET}\n")
        if open_in_browser:
            browser_open('./tc_executor_report.html')
