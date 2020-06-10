"""
Module testcases_executor.tc_groups

Contain necessary classes and functions to make groups of TestCases.

Classes:
    GroupTestLoader
    TestCasesGroup
    TestCasesGroups

Functions:
    import_groups()

Imports:
    sys
    from fnmatch: fnmatchcase
    from unittest: TestCase, TestLoader, TestSuite
    from testcases_executor.tc_utils: raise_error, check_type
"""
import sys
from fnmatch import fnmatchcase
from unittest import TestCase, TestLoader, TestSuite
from testcases_executor.tc_utils import raise_error, check_type


def import_groups():
    """
    Try to import groups, raise errors or return it.

        Returns:
            object: groups.

        Raises:
            ModuleNotFoundError: testscases.py no exist or in it.
            ImportError: import error in testscases.py .
    """
    error_type = None
    try:
        from testcases import groups
    except ModuleNotFoundError as e:  # testscases.py no exist or in it
        if str(e) == "No module named 'testcases'":
            error_type = "No file named 'testcases.py' in root directory."
        else:
            error_type = f"{str(e)} in testcases.py ."
    except ImportError as e:  # import error in testscases.py
        error_type = "Import"
        if "cannot import name 'groups' from 'testcases'" in str(e):
            import_error = "Object groups not founded in testscases.py ."
        else:
            e_split = str(e).split(" ")
            e_split[-1] = "in testscases.py ."
            import_error = " ".join(e_split)
    except NameError as e:
        error_type = "Name"
        name_error = f"{str(e)} in testcases.py ."
    if error_type is not None:  # error during import
        if error_type == "Import":
            raise_error(
                ImportError, import_error)
        if error_type == "Name":
            raise_error(
                NameError, name_error)
        raise_error(ModuleNotFoundError, error_type)
    return groups


class GroupTestLoader(TestLoader):
    """
    A subclass of unittest.TestLoader .

    Used to load test methods of testcase.

    Methods
    ----------
    getTestCaseNames():
        Override original one to ordered test methods by declaration.
    """

    def getTestCaseNames(self, testCaseClass):
        """
        Override original one to ordered test methods by declaration.

        Parameters
        ----------
            testCaseClass: subclass of unittest.TestCase object
                testcase to load tests.

        Returns
        ----------
            list maked with vars(testCaseClass).keys(), not dir(testCaseClass).
        """
        def shouldIncludeMethod(attrname):
            if not attrname.startswith(self.testMethodPrefix):
                return False
            testFunc = getattr(testCaseClass, attrname)
            if not callable(testFunc):
                return False
            fullName = f'%s.%s.%s' % (
                testCaseClass.__module__, testCaseClass.__qualname__, attrname
            )
            return self.testNamePatterns is None or \
                any(fnmatchcase(
                    fullName, pattern) for pattern in self.testNamePatterns)
        return list(filter(
            shouldIncludeMethod, vars(testCaseClass).keys()))


class TestCasesGroup():
    """
    A class to represent a group of TestCases.

    A group with a name and a list of TestCases.

    Attributes
    ----------
    name : str
        string not empty.
    arg_name : str
        string name not empty and without space.
    testases : list
        instances subclass of unittest.TestCase .
    suites : list
        tuples (testcase, unittest.TestSuite object).

    Methods
    ----------
    update_suites(testcase, test_methods):
        Extend suites with a tuple maked with parameters.
    """

    def __init__(self, group_tup):
        """
        Constructs all the necessary attributes for the group object.

        Parameters
        ----------
            group_tup : tuple
                name, argument name and testcases's list or tuple.

        Raises
        ----------
            ValueError: name empty string, arg with space, class not used once.
            TypeError: testcase not a subclass of unittest.TestCase .
        """
        group_name, group_arg_name, group_tc = group_tup
        check_type(group_name, (str, ), "Group's name")
        if not group_name:  # name empty string
            raise_error(
                ValueError, "Group's name must be non empty string.")
        check_type(group_arg_name, (str, ), "Group's argument name")
        if not group_arg_name:  # arg name empty string
            raise_error(
                ValueError, "Group's argument name must be non empty string.")
        if " " in group_arg_name:  # arg name contain space
            raise_error(
                ValueError, "".join([
                    "Group's argument name must not contain space: ",
                    f"{group_arg_name}."]))
        if group_arg_name in ['h', 'o']:  # arg name h or o
            raise_error(
                ValueError, "".join([
                    "Group's argument name must not be 'h' or 'o': ",
                    f"{group_arg_name}."]))
        check_type(group_tc, (list, tuple), "Group's testcases")
        for testcase in group_tc:
            error_type = None
            try:  # item in testcases not
                if not issubclass(testcase, TestCase):  # a TestCase subclass
                    error_type = "unittest.TestCase subclass"
            except TypeError:  # a class
                error_type = "class (unittest.TestCase subclass)"
            if error_type is not None:  # TypeError for tc
                raise_error(TypeError, "".join([
                    "Item of group's testcases list or tuple must be ",
                    f"a {error_type}: {testcase}"]))
            if testcase.__name__ in ['h', 'o']:  # testcase name h or o
                raise_error(
                    ValueError, "".join([
                        "TestCase's name must not be 'h' or 'o': ",
                        f"{testcase.__name__}."]))
            if group_tc.count(testcase) != 1:  # testcase not used once
                raise_error(ValueError, "".join([
                    "Testcase's subclass must used once in group: ",
                    f"'{testcase.__name__}'."]))
        self.name, self.arg_name, self.testcases = group_tup
        if isinstance(self.testcases, tuple):  # convert to list
            self.testcases = list(self.testcases)
        self.suites = []

    def update_suites(self, testcase, test_methods=None):
        """
        Append a tuple maked with parameters to suites attribute.

        Parameters
        ----------
            testcase : Unittest.Testase subclass object
                first item of tuple.
            test_methods: list (default: None)
                names of test methods (str)
        """
        if test_methods is None:
            suite = GroupTestLoader().loadTestsFromTestCase(testcase)
        else:
            suite = TestSuite([testcase(t_name) for t_name in test_methods])
        self.suites.append((testcase, suite))


class TestCasesGroups(list):
    """
    A class to represent a list of TestCasesGroup object.

    A list with TestCasesGroup's objects for items.

    Self
    ----------
    [TestCasesGroup1, TestCasesGroup2, ...]

    Methods
    ----------
    construct_suites(args):
        Check args, update group's testsuites and remove group without suite.
    """

    def __init__(self, tc_groups=None):
        """
        Constructs list of TestCasesGroup's objects initialized with tc_groups.

        Parameters
        ----------
            tc_groups : list or tuple (default: None)
                tuples with 3 items each for items

        Raises
        ----------
            IndexError: group tup not contain 3 items.
            ValueError: group's name or testcase not used once.
        """
        sys.tracebacklimit = 0
        if tc_groups is None:
            tc_groups = import_groups()
        check_type(tc_groups, (list, tuple), "Object groups")
        super().__init__()
        for group_item in tc_groups:
            check_type(group_item, (tuple, ), "Item of groups")
            if len(group_item) != 3:
                raise_error(IndexError, "".join([  # not contain 3 items
                    "Group tuple must contain 3 items (group's name, ",
                    "group's argument name to run all of his testcases, ",
                    f"testcases list or tuple), not {len(group_item)}"]))
            self.append(TestCasesGroup(group_item))
        error_value = None
        g_names = [g.name for g in self]
        for g_name in g_names:
            if g_names.count(g_name) != 1:  # arg name not used once
                error_value = f"Group's name must used once, '{g_name}'."
                break
        if error_value is None:
            g_arg_names = [g.arg_name for g in self]
            for g_arg_name in g_arg_names:
                if g_arg_names.count(g_arg_name) != 1:  # argname not used once
                    error_value = "".join([
                        "Group's argument name must used once, ",
                        f"'{g_arg_name}'."])
                    break
        if error_value is None:
            all_testcases = []
            for group in self:
                all_testcases.extend(group.testcases)
            for testcase in all_testcases:
                if testcase.__name__ in g_arg_names:
                    error_value = "".join([  # tc and g arg names same
                        "Group's argument and Testcase name must be ",
                        f"different, '{testcase.__name__}'"])
                    break
                elif all_testcases.count(testcase) != 1:
                    error_value = "".join([  # testcase not used once
                        "Testcase must used only in one group, ",
                        f"'{testcase.__name__}'"])
                    break
        if error_value is not None:
            raise_error(ValueError, error_value)
        sys.tracebacklimit = 1000

    def construct_suites(self, args):
        """
        Check args, update group's testsuites and remove group without suite.

        Parameters
        ----------
            args :
                result of TestCasesParser.parse_args() .
        """
        if (len(sys.argv) == 1) or ((len(sys.argv) == 2) and args.open):
            for tc_group in self:  # no arg or open timesatamp -> all tests
                for testcase in tc_group.testcases:
                    tc_group.update_suites(testcase)
        else:
            args_dict = vars(args)
            for tc_group in self:
                if args_dict[tc_group.arg_name]:  # group name arg, group tests
                    for testcase in tc_group.testcases:
                        tc_group.update_suites(testcase)
                else:
                    for testcase in tc_group.testcases:
                        t_names = args_dict[testcase.__name__]
                        if isinstance(t_names, list):  # test case's name arg
                            if not t_names:  # no param -> test case's tests
                                tc_group.update_suites(testcase)
                            else:  # method name(s) param -> methods's tests
                                tc_group.update_suites(testcase, t_names)
            groups_to_remove = [g for g in self if not g.suites]
            for group in groups_to_remove:  # remove group without suite
                self.remove(group)
