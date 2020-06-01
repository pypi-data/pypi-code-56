import asyncio
import inspect
import sys
import threading
from typing import Any, AsyncIterator, Awaitable, Generator, Optional, Tuple, TypeVar


T = TypeVar("T")
QueueVal = Optional[Tuple[asyncio.Future, Awaitable[Any]]]


class AsyncioRunner:
    """ Run asyncio loop in the same thread as calling one. Allows to retain same=
    ContextVars for all calls by fixing the running task to a single one.
    """

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._loop_task: Optional[asyncio.Task[None]] = None
        self._call_queue: Optional["asyncio.Queue[QueueVal]"] = None
        self._loop_thread: Optional[threading.Thread] = None
        self._closed = False

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            if self._loop is not None:
                self._tear_down_loop()

    async def _process_queue(self, ready_fut: "asyncio.Future[None]") -> None:
        queue: "asyncio.Queue[QueueVal]" = asyncio.Queue()
        self._call_queue = queue
        ready_fut.set_result(None)

        while True:
            query = await queue.get()
            queue.task_done()
            if query is None:
                return
            fut, awaitable = query

            try:
                ret = await awaitable
                if not fut.cancelled():
                    fut.set_result(ret)
            except asyncio.CancelledError:
                raise
            except Exception as ex:
                if not fut.cancelled():
                    fut.set_exception(ex)

    def _setup_loop(self) -> None:
        assert self._loop is None
        self._loop = loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_debug(self._debug)
        self._set_up_loop_task()

    def _tear_down_loop(self) -> None:
        assert self._loop is not None
        self._tear_down_loop_task()

        loop = self._loop
        self._loop = None

        try:
            # cancel all other tasks if any
            cancel_all_tasks(loop)
            # shutdown asyncgens
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            asyncio.set_event_loop(None)
            loop.close()

    def _set_up_loop_task(self) -> None:
        assert self._loop is not None
        loop = self._loop
        fut = loop.create_future()
        self._loop_task = loop.create_task(self._process_queue(fut))
        loop.run_until_complete(fut)

    def _tear_down_loop_task(self) -> None:
        assert self._loop is not None
        # No need to wait gracefully for the tasks, as we work in a single thread and
        # come here, that means that nobody is waiting for any results.
        if self._loop_task and not self._loop_task.done():
            self._loop_task.cancel()
            try:
                self._loop.run_until_complete(self._loop_task)
            except asyncio.CancelledError:
                pass

    def run(self, coro: Awaitable[T]) -> T:
        if self._loop is None:
            self._setup_loop()
        assert self._loop is not None
        assert self._call_queue is not None
        assert inspect.isawaitable(coro)
        fut = self._loop.create_future()
        self._call_queue.put_nowait((fut, coro))
        try:
            return self._loop.run_until_complete(fut)
        finally:
            # In case of BaseException fut is not cancelled and _process_queue is
            # possibly stuck.
            if not fut.done():
                fut.cancel()
                self._tear_down_loop_task()
                self._set_up_loop_task()

    def run_iter(self, aiter: AsyncIterator[T]) -> Generator[T, Optional[bool], bool]:
        # Transform async iterator into a sync generator
        anxt = aiter.__anext__
        while True:
            try:
                chunk = self.run(anxt())
            except StopAsyncIteration:
                return True
            else:
                yield chunk
        return False


def cancel_all_tasks(loop: asyncio.AbstractEventLoop) -> None:
    if sys.version_info >= (3, 7):
        to_cancel = asyncio.all_tasks(loop)
    else:
        to_cancel = [t for t in asyncio.Task.all_tasks(loop) if not t.done()]
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(
        asyncio.gather(*to_cancel, loop=loop, return_exceptions=True)
    )
    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "unhandled exception during asyncio.run() shutdown",
                    "exception": task.exception(),
                    "task": task,
                }
            )
