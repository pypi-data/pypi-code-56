"""
Module testcases_executor.tests.test_tc_groups .

Contain TestCase for testcases_executor.tc_groups .

unittest.TestCase sublasses:
    TestGroupsFunctions
    TestLoader
    TestGroup
    TestGroups

Imports:
    from unittest: TestCase
    from unittest.mock: patch, Mock, call
    from testcases_executor.tc_groups: (
        import_groups, GroupTestLoader, TestCasesGroup, TestCasesGroups
"""
from unittest import TestCase
from unittest.mock import patch, Mock, call
from testcases_executor.tc_groups import (
    import_groups, GroupTestLoader, TestCasesGroup, TestCasesGroups)


class TestGroupsFunctions(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_groups functions, import_groups.

    Methods
    ----------
    test_import_groups():
        Assert if groups object imported from testscases.py is returned.
    """

    @patch('testcases_executor.tc_groups.raise_error')
    def test_import_groups(self, mock_raise_error):
        """
        Assert if groups object imported from testscases.py is returned.

        Call import_groups and assert if object is returned or an error raised.

        Parameters:
        ----------
        mock_raise_error : Mock
            Mock of tc_utils.raise_error function.

        Assertions:
        ----------
        assert_called_once_with:
            Assert if raise_error is called once with Error and error msg.
        assert_not_called:
            Assert if raise_error is not called for an import without error.
        assertEqual:
            Assert if groups is imported correctly.
        """
        mock_raise_error.side_effect = Exception("raise_error called")
        for tc_value, e_type, e_msg in [
                (  # simulate ModuleNotFoundError
                    None, ModuleNotFoundError, "".join([
                        'import of testcases halted; None ',
                        'in sys.modules in testcases.py .'])),
                (  # simulate ImportError
                    'groups not inside', ImportError, "".join([
                        "cannot import name 'groups' from '<unknown module ",
                        "name>' (unknown in testscases.py ."]))]:
            with patch.dict('sys.modules', {'testcases': tc_value}):
                try:
                    import_groups()
                except Exception:
                    mock_raise_error.assert_called_once_with(e_type, e_msg)
                    mock_raise_error.reset_mock()
        # import ok
        with patch.dict('sys.modules', {'testcases': Mock(groups='groups')}):
            groups_imported = import_groups()
            mock_raise_error.assert_not_called()
            self.assertEqual(groups_imported, 'groups')


class SubclassTCone(TestCase):
    """
    A subclass of unittest.TestCase .

    Used in testcases list or tuple.
    """

    def test_foo(self):
        pass

    def test_bar(self):
        pass


class TestLoader(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_groups.GroupTestLoader .

    Methods
    ----------
    test_getTestCaseNames():
        Assert if getTestCaseNames return methods list ordered by declaration.
    """

    def test_getTestCaseNames(self):
        """
        Assert if getTestCaseNames return methods list ordered by declaration.

        Assertions:
        ----------
        assertEqual:
            Assert if result items are ordered correctly.
        """
        result = GroupTestLoader().getTestCaseNames(SubclassTCone)
        self.assertEqual(result[0], 'test_foo')
        self.assertEqual(result[1], 'test_bar')


class SubclassTCtwo(TestCase):
    """
    A subclass of unittest.TestCase .

    Used in testcases list or tuple to init obj with success.
    """

    def test_bar_foo(self):
        pass

    def test_foo_bar(self):
        pass


class TestGroup(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_groups.TestCasesGroup .

    Methods
    ----------
    test_init_group():
        Assert TestCasesGroup's object is initialized with good attributes.
    test_update_suites():
        Assert tuple added to TestCasesGroup.suites .
    """

    @patch("testcases_executor.tc_groups.raise_error")
    @patch("testcases_executor.tc_utils.raise_error")
    def test_init_group(self, mock_error_one, mock_error_two):
        """
        Assert TestCasesGroup's object is initialized with good attributes.

        Parameters:
        ----------
        mock_error_one : Mock
            Mock of tc_utils.raise_error function (call in check_type in init).
        mock_error_two : Mock
            Mock of tc_groups.raise_error function (call in init).

        Assertions:
        ----------
        assert_called_once_with:
            Assert if raise_error is called once with Error and error msg.
        assert_not_called:
            Assert if raise_error is not called for init with success.
        assertEqual:
            Assert if obj name and arg name are correct.
        assertListEqual:
            Assert if properties testcases and suites are the correct list.
        """
        mock_error_one.side_effect = Exception("raise_error called")
        mock_error_two.side_effect = Exception("raise_error called")
        name_no_str = (  # group's name not str, tup[0]
            (1, 2, 3), mock_error_one,
            TypeError, "Group's name must be 'str', not 'int': 1")
        name_empty = (  # group's name empty str, tup[0]
            ("", 2, 3), mock_error_two,
            ValueError, "Group's name must be non empty string.")
        arg_name_no_str = (  # group's argument name not str, tup[1]
            ("group test", 1, 2), mock_error_one,
            TypeError, "Group's argument name must be 'str', not 'int': 1")
        arg_name_empty = (  # group's argument name empty str, tup[1]
            ("group test", "", 1), mock_error_two,
            ValueError, "Group's argument name must be non empty string.")
        arg_name_space = (  # group's argument name with space, tup[1]
            ("group test", "with space", 1), mock_error_two,
            ValueError,
            "Group's argument name must not contain space: with space.")
        arg_name_h = (  # group's argument name 'h', tup[1]
            ("group test", "h", 1), mock_error_two,
            ValueError,
            "Group's argument name must not be 'h' or 'o': h.")
        arg_name_o = (  # group's argument name 'o', tup[1]
            ("group test", "o", 1), mock_error_two,
            ValueError,
            "Group's argument name must not be 'h' or 'o': o.")
        tc_no_list_tup = (  # testcases not a list or tuple, tup[1]
            ("group test", "test", 2), mock_error_one,
            TypeError,
            "Group's testcases must be 'list' or 'tuple', not 'int': 2")
        item_no_class = (  # item of testcases not a class
            ("group test", "test", (1, )), mock_error_two,
            TypeError,
            "".join([
                "Item of group's testcases list or tuple must be ",
                "a class (unittest.TestCase subclass): 1"]))
        item_no_subclass = (  # item of testcases not a subclass
            ("group test", "test", [int, ]), mock_error_two,
            TypeError,
            "".join([
                "Item of group's testcases list or tuple must be ",
                "a unittest.TestCase subclass: <class 'int'>"]))

        class h(TestCase):
            pass

        item_name_h = (  # testcase name 'h'
            ("group test", "test", [SubclassTCone, h]),
            mock_error_two, ValueError,
            "TestCase's name must not be 'h' or 'o': h.")

        class o(TestCase):
            pass

        item_name_o = (  # testcase name 'o'
            ("group test", "test", [SubclassTCone, o]),
            mock_error_two, ValueError,
            "TestCase's name must not be 'h' or 'o': o.")
        item_no_used_once = (  # testcase not used once
            ("group test", "test", [SubclassTCone, SubclassTCone]),
            mock_error_two, ValueError,
            "Testcase's subclass must used once in group: 'SubclassTCone'.")
        for group_tup, mock_error, e_type, e_msg in [
                name_no_str, name_empty, arg_name_no_str, arg_name_empty,
                arg_name_space, arg_name_h, arg_name_o, tc_no_list_tup,
                item_no_class, item_no_subclass, item_name_o, item_name_h,
                item_no_used_once]:
            try:
                TestCasesGroup(group_tup)
            except Exception:
                mock_error.assert_called_once_with(e_type, e_msg)
                mock_error.reset_mock()
        # init success
        obj = TestCasesGroup(
            ("Group test", "test", (SubclassTCone, SubclassTCtwo)))
        mock_error_one.assert_not_called()
        mock_error_two.assert_not_called()
        self.assertEqual(obj.name, "Group test")
        self.assertEqual(obj.arg_name, "test")
        self.assertListEqual(obj.testcases, [SubclassTCone, SubclassTCtwo])
        self.assertListEqual(obj.suites, [])

    @patch("testcases_executor.tc_groups.TestSuite")
    @patch("testcases_executor.tc_groups.GroupTestLoader")
    def test_update_suites(self, mock_loader, mock_suite):
        """
        Assert tuple added to TestCasesGroup.suites .

        Parameters:
        ----------
        mock_loader : Mock
            Mock of tc_groups.GroupTestLoader .
        mock_error_two : Mock
            Mock of tc_groups.TestSuite (from unittest).

        Assertions:
        ----------
        assert_not_called:
            Assert if TestSuite or loader.loadTestsFromTestCase are not called.
        assert_called_once_with:
            Assert if TestSuite or loadTestsFromTestCase called once with arg.
        assertEqual:
            Assert if obj name and arg name are correct.
        assertTupleEqual:
            Assert if it's the good tuple added to suites property.
        """
        mock_loader().loadTestsFromTestCase.return_value = [
            "test_foo", "test_bar"]
        mock_suite.return_value = ["test_foo"]
        obj = TestCasesGroup(
            ("group test", "g_test", (SubclassTCone, SubclassTCtwo)))
        obj.update_suites(SubclassTCone)  # with just testcase
        mock_suite.assert_not_called()
        mock_loader().loadTestsFromTestCase.assert_called_once_with(
            SubclassTCone)
        self.assertTupleEqual(
            obj.suites[0], (SubclassTCone, ["test_foo", "test_bar"]))
        obj.suites = []
        mock_loader.reset_mock()
        obj.update_suites(SubclassTCone, ["test_foo"])  # with test method
        mock_loader().loadTestsFromTestCase.assert_not_called()
        mock_suite.assert_called_once_with([SubclassTCone('test_foo')])
        self.assertTupleEqual(obj.suites[0], (SubclassTCone, ["test_foo"]))


class TestGroups(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_groups.TestCasesGroups .

    Methods
    ----------
    test_init_groups():
        Assert if TestCasesGroups's object initialized is the desired list.
    test_construct_suites():
        Assert group.update_suites called with good parameter depending args.
    """

    @patch("testcases_executor.tc_groups.sys")
    @patch("testcases_executor.tc_groups.raise_error")
    @patch("testcases_executor.tc_utils.raise_error")
    def test_init_groups(self, mock_error_one, mock_error_two, mock_sys):
        """
        Assert if TestCasesGroups's object initialized is the desired list.

        Parameters:
        ----------
        mock_error_one : Mock
            Mock of tc_utils.raise_error function (call in check_type in init).
        mock_error_two : Mock
            Mock of tc_groups.raise_error function (call in init).
        mock_sys : Mock
            Mock of sys to keep default tracebacklimit.

        Assertions:
        ----------
        assert_called_once_with:
            Assert if raise_error is called once with Error and error msg.
        assert_not_called:
            Assert if raise_error is not called for init with success.
        assertIsInstance:
            Assert if obj is a list and items TestCasesGroup.
        assertEqual:
            Assert if len obj is 3, if obj[i] name and arg name are correct.
        assertListEqual:
            Assert if obj[i].testcases is the correct list.
        """
        mock_error_one.side_effect = Exception("raise_error called")
        mock_error_two.side_effect = Exception("raise_error called")
        groups_no_list_tup = (  # groups not a list or tuple
            2, mock_error_one,
            TypeError,
            "Object groups must be 'list' or 'tuple', not 'int': 2")
        item_no_tup = (  # groups's item not a tuple
            [2, ], mock_error_one,
            TypeError,
            "Item of groups must be 'tuple', not 'int': 2")
        item_no_three_items = (  # groups's item not contain 3 items
            [(1, 2, 3, 4), ], mock_error_two,
            IndexError, "".join([
                "Group tuple must contain 3 items (group's name, ",
                "group's argument name to run all of his testcases, ",
                "testcases list or tuple), not 4"]))
        name_no_used_once = (  # group's name not used once
            (
                ("group test", "test", [SubclassTCone, ]),
                ('group test', "test", (SubclassTCtwo, ))),
            mock_error_two, ValueError,
            "Group's name must used once, 'group test'.")
        arg_name_no_used_once = (  # group's arg name not used once
            (
                ("group test", "test", [SubclassTCone, ]),
                ('group test 2', "test", (SubclassTCtwo, ))),
            mock_error_two, ValueError,
            "Group's argument name must used once, 'test'.")
        tc_group_arg_names = (  # testcase and g arg names same
            (
                ("group test", "SubclassTCtwo", [SubclassTCone, ]),
                ('group test 2', "test2", (SubclassTCtwo, ))),
            mock_error_two, ValueError, "".join([
                "Group's argument and Testcase name must ",
                "be different, 'SubclassTCtwo'"]))
        tc_no_used_once = (  # testcase not used once
            (
                ("group test", "test", [SubclassTCone, ]),
                ('group test 2', "test2", (SubclassTCtwo, SubclassTCone))),
            mock_error_two, ValueError,
            "Testcase must used only in one group, 'SubclassTCone'")
        for tc_groups, mock_error, e_type, e_msg in [
                groups_no_list_tup, item_no_tup, item_no_three_items,
                name_no_used_once, arg_name_no_used_once, tc_group_arg_names,
                tc_no_used_once]:
            try:
                TestCasesGroups(tc_groups)
            except Exception:
                mock_error.assert_called_once_with(e_type, e_msg)
                mock_error.reset_mock()
        # init success
        obj = TestCasesGroups([
            ("Group test", "test", [SubclassTCone, ]),
            ('Group test 2', "test2", (SubclassTCtwo, ))])
        mock_error_one.assert_not_called()
        mock_error_two.assert_not_called()
        self.assertIsInstance(obj, list)
        self.assertEqual(len(obj), 2)
        for group in obj:
            self.assertIsInstance(group, TestCasesGroup)
        self.assertEqual(obj[0].name, "Group test")
        self.assertEqual(obj[0].arg_name, "test")
        self.assertListEqual(obj[0].testcases, [SubclassTCone, ])
        self.assertEqual(obj[1].name, "Group test 2")
        self.assertEqual(obj[1].arg_name, "test2")
        self.assertListEqual(obj[1].testcases, [SubclassTCtwo, ])

    @patch("builtins.vars")
    @patch("testcases_executor.tc_groups.TestCasesGroup.update_suites")
    @patch("testcases_executor.tc_groups.sys")
    def test_construct_suites(
            self, mock_sys, mock_update_suites, mock_vars):
        """
        Assert group.update_suites called with good parameter depending args.

        Parameters:
        ----------
        mock_sys : Mock
            Mock of sys to set value to sys.argv .
        mock_update_suites : Mock
            Mock of tc_groups.TestCasesGroup.update_suites .
        mock_vars : Mock
            Mock of vars to set return value for vars(args).

        Classes:
        ----------
        FakeArgs:
            A fake agrs with properties open and timestamp.

        Assertions:
        ----------
        assertEqual:
            Assert group.update_suites call count.
        assert_has_calls:
            Assert group.update_suites calls parameters.
        assert_called_once_with:
            Assert vars called once with 'args', groups.remove with group.
        """
        class FakeArgs():

            def __init__(self, a_open):
                self.open = a_open

        for argv, args in [  # all groups testcases
                ([1], FakeArgs(False)),
                ([1, 2], FakeArgs(True))]:
            mock_sys.argv = argv
            obj = TestCasesGroups([
                ("group test", "g_test", [SubclassTCone, ]),
                ('group test 2', "g_test2", (SubclassTCtwo, ))])
            group_one, group_two = obj[0], obj[1]
            obj.construct_suites(args)
            self.assertEqual(mock_update_suites.call_count, 2)
            mock_update_suites.assert_has_calls([
                call(SubclassTCone), call(SubclassTCtwo)])
            self.assertEqual(obj, [group_one, group_two])
            mock_update_suites.reset_mock()
        mock_sys.argv = [1, 2, 3]
        for vars_val, count_val, call_vals, new_obj in [  # depending args
                ((True, False, None, None), 1, (SubclassTCone, ), "one"),
                ((False, False, None, []), 1, (SubclassTCtwo, ), "two"),
                ((True, False, None, ['test_foo']), 2, (
                    SubclassTCone, (SubclassTCtwo, ['test_foo'])), "all")]:
            mock_vars.return_value = {
                'g_test': vars_val[0], 'g_test2': vars_val[1],
                'SubclassTCone': vars_val[2], 'SubclassTCtwo': vars_val[3]}
            obj = TestCasesGroups([
                ("group test", "g_test", [SubclassTCone, ]),
                ('group test 2', "g_test2", (SubclassTCtwo, ))])
            if new_obj == "one":
                obj[0].suites = [1]
            elif new_obj == "two":
                obj[1].suites = [1]
            else:
                obj[0].suites, obj[1].suites = [1], [1]
            group_one, group_two = obj[0], obj[1]
            obj.construct_suites('args')
            mock_vars.assert_called_once_with('args')
            self.assertEqual(mock_update_suites.call_count, count_val)
            call_list = []
            for tc in call_vals:
                if isinstance(tc, tuple):
                    t_class, t_methods = tc
                    call_list.append(call(t_class, t_methods))
                else:
                    call_list.append(call(tc))
            mock_update_suites.assert_has_calls(call_list)
            if new_obj == "one":
                self.assertEqual(obj, [group_one])
            elif new_obj == "two":
                self.assertEqual(obj, [group_two])
            else:
                self.assertEqual(obj, [group_one, group_two])
            mock_vars.reset_mock()
            mock_update_suites.reset_mock()
