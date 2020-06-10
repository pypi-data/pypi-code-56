from hodgepodge.helpers import ensure_type
from red_raccoon.commands import Command, CommandBlock, ExecutedCommand, ObservedProcess, \
    POWERSHELL, SH

import red_raccoon.commands
import hodgepodge.helpers
import multiprocessing
import dataclasses
import threading
import unittest
import psutil
import time
import copy
import os

KILLED = -9 if hodgepodge.helpers.platform_is_posix() else 15


def _get_sleep_command(duration, timeout=None, as_command_block=False):
    duration = ensure_type(duration, (int, float))
    constructor = CommandBlock if as_command_block else Command
    if hodgepodge.helpers.platform_is_windows():
        return constructor("Start-Sleep -Seconds {}".format(duration), command_type=POWERSHELL, timeout=timeout)
    else:
        return constructor("sleep {}".format(duration), command_type=SH, timeout=timeout)


def get_sleep_command(duration, timeout=None):
    return _get_sleep_command(duration, timeout)


def get_sleep_command_block(duration, timeout=None):
    return _get_sleep_command(duration, timeout, as_command_block=True)


def _sleepy_subprocess(duration):
    time.sleep(duration)


class CommandHelperTestCases(unittest.TestCase):
    def test_execute_command(self):
        command = get_sleep_command(0.01)
        result = red_raccoon.commands.execute_command(**dataclasses.asdict(command))
        self.assertIsInstance(result, ExecutedCommand)
        self.assertEqual(result.exit_status, 0)

    def test_execute_command_with_timeout(self):
        command = get_sleep_command(0.01, timeout=0.025)
        result = red_raccoon.commands.execute_command(**dataclasses.asdict(command))
        self.assertIsInstance(result, ExecutedCommand)
        self.assertEqual(result.exit_status, 0)

    def test_terminate_process(self):
        shutdown_event = threading.Event()
        process = multiprocessing.Process(target=_sleepy_subprocess, args=(5,))
        process.start()

        #: Wait for process to start.
        while not shutdown_event.is_set():
            if process.is_alive():
                break
            shutdown_event.wait(0.05)

        #: Terminate the process.
        red_raccoon.commands.terminate_process(process.pid)

        #: Wait for process to die.
        while not shutdown_event.is_set():
            if not process.is_alive():
                break
            shutdown_event.wait(0.05)

        #: Confirm the kill.
        self.assertEqual(process.exitcode, KILLED)

    def test_terminate_non_existent_process(self):
        shutdown_event = threading.Event()
        process = multiprocessing.Process(target=_sleepy_subprocess, args=(5,))
        process.start()

        #: Wait for process to start.
        while not shutdown_event.is_set():
            if process.is_alive():
                break
            shutdown_event.wait(0.05)

        #: Terminate the process.
        red_raccoon.commands.terminate_process(process.pid)

        #: Wait for process to die.
        while not shutdown_event.is_set():
            if not process.is_alive():
                break
            shutdown_event.wait(0.05)

        #: Confirm the kill.
        self.assertEqual(process.exitcode, KILLED)

        #: Confirm that the process was reaped.
        with self.assertRaises(psutil.NoSuchProcess):
            psutil.Process(process.pid)

        #: Since the process was reaped, it's (tremendously) unlikely that the PID is in use.
        red_raccoon.commands.terminate_process(pid=process.pid, include_children=True)

    def test_get_executable_path(self):
        process = psutil.Process()
        path = red_raccoon.commands.get_executable_path(process.name())
        self.assertIsInstance(path, str)
        self.assertTrue(path)

    def test_get_executable_name(self):
        process = psutil.Process()
        path = red_raccoon.commands.get_executable_name(process.name())
        self.assertIsInstance(path, str)
        self.assertTrue(path)


class CommandTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = get_sleep_command(0.01)
        cls.b = get_sleep_command(0.02)

    def test_type(self):
        if hodgepodge.helpers.platform_is_windows():
            self.assertEqual(self.a.type, POWERSHELL)
        else:
            self.assertEqual(self.a.type, SH)

    def test_executable_path(self):
        self.assertIsInstance(self.a.executable_path, str)
        self.assertTrue(self.a.executable_path)

    def test_executable_name(self):
        self.assertIsInstance(self.a.executable_name, str)
        self.assertTrue(self.a.executable_name)

    def test__call__(self):
        result = self.a()
        self.assertIsInstance(result, ExecutedCommand)

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.a)
        c = hash(self.b)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test__eq__(self):
        a = copy.copy(self.a)
        self.assertIsNot(a, self.a)
        self.assertEqual(a, self.a)
        self.assertNotEqual(self.a, self.b)


class CommandBlockTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = get_sleep_command_block(0.01)
        cls.b = get_sleep_command_block(0.02)

    def test_type(self):
        if hodgepodge.helpers.platform_is_windows():
            self.assertEqual(self.a.type, POWERSHELL)
        else:
            self.assertEqual(self.a.type, SH)

    def test__call__(self):
        result = self.a()
        self.assertIsInstance(result, ExecutedCommand)

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.a)
        c = hash(self.b)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test__eq__(self):
        a = copy.copy(self.a)
        self.assertIsNot(a, self.a)
        self.assertEqual(a, self.a)
        self.assertNotEqual(self.a, self.b)


class ObservedProcessTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = hodgepodge.helpers.dataclass_to_dataclass(get_sleep_command(0.01)(), ExecutedCommand, ObservedProcess)
        cls.b = hodgepodge.helpers.dataclass_to_dataclass(get_sleep_command(0.01)(), ExecutedCommand, ObservedProcess)

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.a)
        c = hash(self.b)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test__eq__(self):
        a = copy.copy(self.a)
        self.assertIsNot(a, self.a)
        self.assertEqual(a, self.a)
        self.assertNotEqual(self.a, self.b)


class ExecutedCommandTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = get_sleep_command(0.01)()
        cls.b = get_sleep_command(0.02)()

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.a)
        c = hash(self.b)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test__eq__(self):
        a = copy.copy(self.a)
        self.assertIsNot(a, self.a)
        self.assertEqual(a, self.a)
        self.assertNotEqual(self.a, self.b)

    def test__iter__(self):
        self.assertIsInstance(list(self.a), list)
