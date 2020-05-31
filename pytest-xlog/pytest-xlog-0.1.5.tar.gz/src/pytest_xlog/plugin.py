import json
from os import path
from time import time
from _pytest.pathlib import Path
from _pytest.mark.structures import Mark
import pytest
import re
import yaml


def pytest_addoption(parser):
    group = parser.getgroup("reporting", "xlog plugin options")
    group.addoption(
        "--xlog",
        action="store",
        metavar="path",
        default=None,
        help="Path to YAML file containing of test results",
    )
    group.addoption(
        "--xopt",
        action="append",
        default=[],
        help="Various options added to xlog formatted as key=value",
    )


def pytest_configure(config):
    xlog = config.option.xlog
    if xlog and not hasattr(config, "slaveinput"):
        config._xlog_plugin = XLogPlugin(config)
        config.pluginmanager.register(config._xlog_plugin)
    config.addinivalue_line(
        "markers", "case: Test Case Id"
    )


def pytest_unconfigure(config):
    xlog_plugin = getattr(config, "_xlog_plugin", None)
    if xlog_plugin:
        xlog_plugin.close()
        del config._xlog_plugin

class XLogPluginException(Exception):
    pass

class XLogPlugin:

    def __init__(self, config):
        self._config = config
        log_path = Path(config.option.xlog)
        self._log_path = log_path
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self._file = log_path.open("w", buffering=1, encoding="UTF-8")
        self._always_report = {}
        for item in config.option.xopt:
            if '=' in item:
                keytree = item.split('=')[0]
                key = keytree
                cur = self._always_report
                for key in keytree.split('.'):
                    if not cur.get(key):
                        cur[key] = {}
                    if key != keytree.split('.')[-1]:
                        cur = cur[key]
                cur[key] = item.split('=')[1]
        self._always_report['session_id'] = int(time())
        self._results = {}

    def close(self):
        if self._file is not None:
            self._file.close()
            self._file = None

    def _write_yaml(self):
        yaml.dump(self._results, self._file)
        self._file.flush()

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        # execute all other hooks to obtain the report object
        outcome = yield
        # Full path to called test function
        call_path = '{}::{}'.format(str(item.fspath), item.name).replace('\\', '/')
        # Get @pytest.mark.case decorator data
        tr_decorator_data = item.get_closest_marker('case')
        # Get @pytest.mark.parametrize data
        tr_param_data = item.get_closest_marker('parametrize')
        # Get skip decorator data
        tr_skip_data = item.get_closest_marker('skip')
        # Make fake decorator to report such tests also
        if not tr_decorator_data:
            tr_decorator_data = Mark(
                'case',
                [re.sub('[^0-9a-zA-Z]+', '_', 'no_case_{}'.format(call_path))],
                {}
            )
        # Get case id
        case_data = tr_decorator_data.args[0]
        if isinstance(case_data, dict):
            if not tr_param_data:
                raise XLogPluginException('@pytest.mark.case points out in dictionary but @pytest.mark.parametrize not found')
            for case_id, params in case_data.items():
                if params == list(item.funcargs.values()):
                    break
        else:
            case_id = case_data
        # Prepare teh record for test
        if call.when == 'setup':
            if not self._results.get(case_id):
                self._results[case_id] = []
            self._results[case_id].append(
                {
                    'started': time(),
                    'setup_status': None,
                    'call_status': None,
                    'teardown_status': None,
                    'call_path': call_path
                }
            )
            idx = len(self._results[case_id])-1
            # Add static options passed via command line --xopt key=value
            self._results[case_id][idx].update(self._always_report)
            # Add case decorator options
            if len(tr_decorator_data.kwargs) > 0:
                for name, value in tr_decorator_data.kwargs.items():
                    self._results[case_id][idx][name] = value
            if tr_skip_data:
                if len(tr_skip_data.args) > 0:
                    self._results[case_id][idx]['skip'] = tr_skip_data.args[0]
                elif tr_skip_data.kwargs.get('reason'):
                    self._results[case_id][idx]['skip'] = tr_skip_data.kwargs['reason']
                else:
                    raise XLogPluginException('Skip message not found in args nor kwargs ')
        elif call.when == 'teardown':
            self._results[case_id][len(self._results[case_id])-1]['finished'] = time()
        # Add the result
        self._results[case_id][len(self._results[case_id])-1]['{}_status'.format(call.when)] = outcome.get_result().outcome

    def pytest_sessionfinish(self):
        # Save collected results
        self._write_yaml()
