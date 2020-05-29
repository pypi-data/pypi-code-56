import time
from typing import Any, Callable, List, Tuple, Union


class Until:

    def __init__(
            self,
            delay_in_between: int = 0.01,
            dont_raise: bool = False,
            on_raise: Union[Callable, List[Tuple[Exception, Callable]]] = None,
            retry_times: int = 0
    ):
        self._delay_in_between = delay_in_between
        self._dont_raise = dont_raise
        self._on_raise = on_raise
        self._retry_times = retry_times
        self._exception_raised: Exception = None
        self._returned_value: Any = None
        self._tried_times: int = 0

    def __call__(self, fn):
        def wrapped_f(*args, **kwargs):

            if self._retry_times == 0:
                self._tried_times = 1
                self._returned_value = self.exec_fn(fn, *args, **kwargs)

            for _ in range(0, self._retry_times):
                self._tried_times += 1
                self._returned_value = self.exec_fn(fn, *args, **kwargs)

                if not self.exception_was_raised():
                    break

                self.handle_on_raise()

                if self._delay_in_between > 0:
                    time.sleep(self._delay_in_between)

            return self._returned_value

        return wrapped_f

    @property
    def tried_times(self):
        return self._tried_times

    def exec_fn(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)

        except Exception as ex:
            self._exception_raised = ex

    def exception_was_raised(self):
        return self._exception_raised is not None

    def handle_on_raise(self):
        if callable(self._on_raise):
            self._on_raise(self._exception_raised)

        if isinstance(self._on_raise, list):
            for item in self._on_raise:
                ex, fn = item
                if isinstance(self._exception_raised, ex):
                    fn(self._exception_raised)
