import logging
import time

from typing import Any, Callable, List, Tuple, Union

logger = logging.getLogger('until')


class Until:

    def __init__(
            self,
            delay_in_between: int = 0.01,
            dont_raise: bool = False,
            on_fail: Callable = None,
            on_raise: Union[Callable, List[Tuple[Exception, Callable]]] = None,
            retry_times: int = 0,
            logger=logger
    ):
        self._delay_in_between = delay_in_between
        self._dont_raise = dont_raise
        self._on_fail = on_fail
        self._on_raise = on_raise
        self._retry_times = retry_times
        self._exception_raised: Exception = None
        self._executed_successfully: bool = False
        self._returned_value: Any = None
        self._tried_times: int = 0
        self._logger = logger

    def __call__(self, fn):
        def wrapped_f(*args, **kwargs):

            if self._retry_times == 0:
                self._tried_times = 1
                self._returned_value = self.exec_fn(fn, *args, **kwargs)

            for _ in range(0, self._retry_times):
                self._tried_times += 1

                self._logger.debug(f'Execution attempt: {self._tried_times}')

                self._returned_value = self.exec_fn(fn, *args, **kwargs)

                if not self.exception_was_raised():
                    self._logger.debug('No exception raised')
                    break

                self.handle_on_raise()

                if self._delay_in_between > 0:
                    self._logger.debug(
                        f'Delaying {self._delay_in_between} seconds'
                    )
                    time.sleep(self._delay_in_between)

            if self.need_to_handle_failure():
                self.handle_on_fail()

            return self._returned_value

        return wrapped_f

    @property
    def tried_times(self):
        return self._tried_times

    def exec_fn(self, fn, *args, **kwargs):
        try:
            self._logger.debug(f'Executing function {fn.__name__}')

            returned_value = fn(*args, **kwargs)

            self._exception_raised = None
            self._executed_successfully = True

            return returned_value

        except Exception as ex:
            self._logger.debug(f'Exception raised: {ex}')
            self._exception_raised = ex

    def exception_was_raised(self):
        return self._exception_raised is not None

    def handle_on_fail(self):
        self._logger.debug('Handling on fail')

        if callable(self._on_fail):
            self._logger.debug(f'Calling {self._on_fail.__name__}')
            self._on_fail(self._exception_raised)

    def handle_on_raise(self):
        self._logger.debug('Handling on raise')

        if callable(self._on_raise):
            self._logger.debug(f'Calling {self._on_raise.__name__}')
            self._on_raise(self._exception_raised)

        if isinstance(self._on_raise, list):
            for item in self._on_raise:
                ex, fn = item
                if isinstance(self._exception_raised, ex):
                    self._logger.debug(
                        f'Handling excetion {ex.__name__} with function '
                        f'{ex.__name__}'
                    )
                    fn(self._exception_raised)

    def need_to_handle_failure(self):
        return not self._executed_successfully
