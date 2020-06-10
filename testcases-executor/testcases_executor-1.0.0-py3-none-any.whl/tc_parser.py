"""
Module testcases_executor.tc_parser

Contain necessary classes to make a parser for groups of TestCases.

Classes:
    TestCasesHelpFormatter
    TestCasesParser

Imports:
    from argparse import ArgumentParser, HelpFormatter
    from testcases_executor.tc_utils: MUTED, BOLD, S_RESET
"""
from argparse import ArgumentParser, HelpFormatter
from testcases_executor.tc_utils import MUTED, BOLD, S_RESET


class TestCasesHelpFormatter(HelpFormatter):
    """
    A subclass of argparse.HelpFormatter .

    Use to format help message with color and style.

    Methods
    ----------
    add_usage():
        Override original one to change a prefix.
    _format_args():
        Override original one to change how to display nargs.
    _join_parts():
        Override original one to add space between args.
    """

    def __init__(self, **kwargs):
        """
        Change prog and max_help_position before init HelpFormatter.

        Parameters
        ----------
            **kwargs : prog, indent_increment, max_help_position, width
                default kwargs passed to construct HelpFormatter
        """
        kwargs['prog'] = f"{MUTED}python -m testcases_executor{S_RESET}{MUTED}"
        kwargs['max_help_position'] = 5
        super().__init__(**kwargs)

    def add_usage(self, usage, actions, groups, prefix=None):
        """
        Override original one to change prefix.

        Parameters
        ----------
            usage, actions, groups:
                default args passed.
            prefix : str (default: None)
                used in usage as title.

        Return
        ----------
            result of original add_usage() with prefix changed.
        """
        return super(TestCasesHelpFormatter, self).add_usage(
            usage, actions, groups, f'{BOLD}')

    def _format_args(self, action, default_metavar):
        """
        Override original one to change how to display nargs.

        Parameters
        ----------
            action, default_metavar:
                default args passed.

        Return
        ----------
            string to represent nargs.
        """
        return "..."

    def _join_parts(self, part_strings):
        """
        Override original one to add in string style and space between args.

        Parameters
        ----------
            part_strings : list of str
                default list of part string.

        Return
        ----------
            string constructed with the new part string.
        """
        if part_strings:  # add style for group name ang args
            if len(part_strings) > 1:
                if part_strings[1]:
                    if part_strings[1].split('\n')[0]:
                        if part_strings[1].split('\n')[0][-1] == ":":
                            part_strings[1] = (
                                f"{BOLD}{part_strings[1]}{S_RESET}")
            part_strings[0] = f"\n{MUTED}{part_strings[0]}{S_RESET}"
        return ''.join([
            part for part in part_strings if part and part != '==SUPPRESS=='])


class TestCasesParser(ArgumentParser):
    """
    A subclass of argparse.ArgumentParser .

    A custom ArgumentParser for groups of TestCases.

    Methods
    ----------
    add_args_options:
        Add default options arguments.
    add_args_groups:
        Add groups of arguments for each TestCasesGroup.
    """

    def __init__(self, tc_groups):
        """
        Set attribute, init Parser with parameters and call add_args methods.

        Parameters
        ----------
            tc_groups : TestCasesGroups
                list with instances of TestCasesGroup for items.
        """
        super().__init__(
            formatter_class=TestCasesHelpFormatter, description=''.join([
                'Without argument to run all tests, or with optionnal ',
                'one(s) without option to run group or TestCase tests, or ',
                'with method names in options to a TestCase arg to run ',
                'specific test methods.']),
            epilog="-\n", allow_abbrev=False)
        self.add_args_options()
        self.add_args_groups(tc_groups)

    def add_args_options(self):
        """
        Add default options arguments.

        Arguments
        ----------
            o, open : store_true
                arg to open html report in browser after tests.
        """
        self._optionals.title = "Options"  # title for options
        self.add_argument(  # arg to open report diretly in browser
            "-o", "--open", action='store_true',
            help="Open html report in browser after tests.")

    def add_args_groups(self, tc_groups):
        """
        Add groups of arguments for each TestCasesGroup.

        Parameters
        ----------
            tc_groups : TestCasesGroups
                list with instances of TestCasesGroup for items.

        Arguments
        ----------
            group's arg_names : store_true
                to run all group's testcases
            testcase's names : nargs (choices: method test's names).
                to run all testcase's tests or tests specified im parameter.
        """
        for tc_group in tc_groups:
            arg_group = self.add_argument_group(f"{tc_group.name}")
            arg_group.add_argument(  # group name to run all group's testcases
                f"-{tc_group.arg_name}", action='store_true',
                help=f"Run all {tc_group.name} TestCases.")
            for tc in tc_group.testcases:
                t_names = [n for n in tc.__dict__.keys() if n[:5] == 'test_']
                arg_group.add_argument(  # arg with testcase's name
                    f"-{tc.__name__}", help=f"{' '.join(t_names)}",
                    nargs='*', choices=t_names)  # tests's names for params
