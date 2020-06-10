"""
Module testcases_executor.__main__

Contain main function that called when testcases_executor executed as module.

Functions:
    main()

Imports:
    from testcases_executor.tc_groups: TestCasesGroups
    from testcases_executor.tc_parser: TestCasesParser
    from testcases_executor.tc_runner: TestCasesRunner
    from testcases_executor.tc_reporter.html_report: TestCasesHtmlReport
"""
from testcases_executor.tc_groups import TestCasesGroups
from testcases_executor.tc_parser import TestCasesParser
from testcases_executor.tc_runner import TestCasesRunner
from testcases_executor.tc_reporter.html_report import TestCasesHtmlReport


def main():
    """
    Construct Groups, Parser and parse args, Suites and Runner tests, Report.
    """
    tc_groups = TestCasesGroups()
    parser = TestCasesParser(tc_groups)
    args = parser.parse_args()
    tc_groups.construct_suites(args)
    result = TestCasesRunner().run(tc_groups)
    TestCasesHtmlReport(result, args.open)


if __name__ == "__main__":
    main()
