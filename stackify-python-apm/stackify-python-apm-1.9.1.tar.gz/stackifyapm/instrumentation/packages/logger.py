import json
import sys
import traceback

from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan
from stackifyapm.utils.helper import is_async_span


def get_stack_trace(exc_info):
    if not exc_info:
        type_, value, tb = sys.exc_info()
    else:
        type_, value, tb = exc_info

    stacks = traceback.extract_tb(tb)
    new_stacks = []

    for filename, lineno, method, text in reversed(stacks):
        new_stacks.append("file {}, line {} in {}: {}".format(filename, lineno, method, text))

    return json.dumps(new_stacks)


class LoggerInstrumentation(AbstractInstrumentedModule):
    name = "logger"

    instrument_list = [("logging", "Logger.handle")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        record = args[0]

        extra_data = {
            "provider": self.name,
            "type": "Log",
            "wrapped_method": "logger",
            "level": record.levelname.upper(),
            "message": record.getMessage(),
        }

        if record.exc_info:
            extra_data.update({"exception": get_stack_trace(record.exc_info)})

        with CaptureSpan("cpython.logging", extra_data, leaf=True, is_async=is_async_span()):
            return wrapped(*args, **kwargs)
