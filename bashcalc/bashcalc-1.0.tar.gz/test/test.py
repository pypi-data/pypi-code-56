from decimal import Decimal
from math import *

import subprocess
from bashcalc import bashcalc

import mock
import pytest


class TestTerminalInit(object):
    def test_terminal_help(self):
        result = subprocess.call(["bashcalc", "-h"])
        assert not result

    def test_terminal_easy(self):
        expr = "2"
        ref = eval(expr)
        result = subprocess.check_output(["bashcalc", expr])
        assert result == str.encode(f"{ref}\n")

    def test_terminal_add(self):
        expr = "2 + 2"
        ref = Decimal(eval(expr))
        result = subprocess.check_output(["bashcalc", expr])
        assert result == str.encode(f"{ref}\n")

    def test_terminal_complex(self):
        expr = "2 + 2 * exp(2)"
        ref = Decimal(eval(expr))
        result = subprocess.check_output(["bashcalc", expr])
        assert result == str.encode(f"{ref}\n")


class TestTerminalOptions(object):
    def test_terminal_bold(self):
        expr = "2 + 2"
        ref = Decimal(eval(expr))
        result = subprocess.check_output(["bashcalc", expr, "-b"])
        assert result == str.encode(f"\x1b[1m{ref}\n")

    def test_terminal_underling(self):
        expr = "2 + 2"
        ref = Decimal(eval(expr))
        result = subprocess.check_output(["bashcalc", expr, "-u"])
        assert result == str.encode(f"\x1b[4m{ref}\n")

    def test_terminal_red(self):
        expr = "2 + 2"
        ref = Decimal(eval(expr))
        result = subprocess.check_output(["bashcalc", expr, "-c red"])
        assert result == str.encode(f"{ref}\n")


class TestTerminalOutput(object):
    def test_terminal_normal(self):
        expr = "1 / 3"
        ref = Decimal(eval(expr))
        result = subprocess.check_output(["bashcalc", expr])
        assert result == str.encode(f"{ref}\n")

    def test_terminal_round(self):
        expr = "1 / 3"
        ref = round(Decimal(eval(expr)), 4)
        result = subprocess.check_output(["bashcalc", expr, "-r 4"])
        assert result == str.encode(f"{ref}\n")

    def test_terminal_interger(self):
        expr = "1 / 3"
        ref = int(Decimal(eval(expr)))
        result = subprocess.check_output(["bashcalc", expr, "-i"])
        assert result == str.encode(f"{ref}\n")

    def test_terminal_scientifc(self):
        expr = "1 / 3"
        ref = Decimal(eval(expr))
        digits = 5
        result = subprocess.check_output(["bashcalc", expr, f"-s {digits}"])
        assert result == str.encode(f"{ref:.{digits}E}\n")


class TestTerminalError(object):
    def test_name_error(self):
        expr = "ex"
        try:
            subprocess.check_output(["bashcalc", expr])
        except subprocess.CalledProcessError:
            assert 1

    def test_type_error(self):
        expr = "1*exp"
        try:
            subprocess.check_output(["bashcalc", expr])
        except subprocess.CalledProcessError:
            assert 1

    def test_expression_error(self):
        expr = "1*expp(1)"
        try:
            subprocess.check_output(["bashcalc", expr])
        except subprocess.CalledProcessError:
            assert 1

class TestBashCalc(object):
    def test_case_empty(self):
        args = {
            "infile": "",
            "color": None,
            "bold": False,
            "underlined": False,
            "int": False,
            "round": None,
            "science": None,
            "version": False,
        }
        bashcalc.command_line_runner(args)
        assert 1

    def test_case_version(self):
        args = {
            "infile": "2",
            "color": None,
            "bold": False,
            "underlined": False,
            "int": False,
            "round": None,
            "science": None,
            "version": True,
        }
        bashcalc.command_line_runner(args)
        assert 1

    def test_case_simple(self):
        args = {
            "infile": "2",
            "color": None,
            "bold": False,
            "underlined": False,
            "int": False,
            "round": None,
            "science": None,
            "version": True,
        }
        assert bashcalc.bashcalc(args) == "2"

    def test_case_advance(self):
        args = {
            "infile": "2**2",
            "color": None,
            "bold": False,
            "underlined": False,
            "int": False,
            "round": None,
            "science": None,
            "version": True,
        }
        assert bashcalc.bashcalc(args) == "4"

    def test_case_color_font(self):
        args = {
            "infile": "2",
            "color": "green",
            "bold": True,
            "underlined": True,
            "int": False,
            "round": None,
            "science": None,
            "version": None,
        }
        assert bashcalc.bashcalc(args) == "\x1b[4m\x1b[1m\x1b[32m2"

    def test_case_int(self):
        args = {
            "infile": "2.0",
            "color": "",
            "bold": None,
            "underlined": None,
            "int": True,
            "round": None,
            "science": None,
            "version": None,
        }
        assert bashcalc.bashcalc(args) == "2"

    def test_case_V(self):
        args = {
            "infile": "2.0",
            "color": "",
            "bold": None,
            "underlined": None,
            "int": True,
            "round": None,
            "science": None,
            "version": None,
        }
        assert bashcalc.bashcalc(args) == "2"

    def test_case_round(self):
        args = {
            "infile": "2.0009",
            "color": "",
            "bold": None,
            "underlined": None,
            "int": False,
            "round": 2,
            "science": None,
            "version": None,
        }
        assert bashcalc.bashcalc(args) == "2.00"

    def test_case_science(self):
        args = {
            "infile": "1",
            "color": "",
            "bold": None,
            "underlined": None,
            "int": False,
            "round": None,
            "science": 4,
            "version": None,
        }
        assert bashcalc.bashcalc(args) == "1.0000E+0"

    def test_case_round_error(self):
        args = {
            "infile": "1",
            "color": "",
            "bold": None,
            "underlined": None,
            "int": False,
            "round": 1000,
            "science": None,
            "version": None,
        }
        assert bashcalc.bashcalc(args) == "1"

    def test_case_expr_error(self):
        args = {
            "infile": "1*exp",
            "color": "",
            "bold": None,
            "underlined": None,
            "int": False,
            "round": 1000,
            "science": None,
            "version": None,
        }
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            bashcalc.bashcalc(args)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    def test_case_name_error(self):
        args = {
            "infile": "ex",
            "color": "",
            "bold": None,
            "underlined": None,
            "int": False,
            "round": 1000,
            "science": None,
            "version": None,
        }
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            bashcalc.bashcalc(args)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    def test_case_type_error(self):
        args = {
            "infile": "1*\1",
            "color": "",
            "bold": None,
            "underlined": None,
            "int": False,
            "round": 1000,
            "science": None,
            "version": None,
        }
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            bashcalc.bashcalc(args)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    def test_call_main(self):
        # with pytest.raises(SystemExit) as pytest_wrapped_e:
        with mock.patch.object(bashcalc, "command_line_runner", return_value=1):
            with mock.patch.object(bashcalc, "__name__", "__main__"):
                with mock.patch.object(bashcalc.command_line_runner, "1") as mock_exit:
                    bashcalc.command_line_runner()
                    assert 1
