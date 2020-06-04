from __future__ import annotations

import datetime as dt
from abc import abstractmethod
from concurrent.futures._base import Future
from concurrent.futures.process import ProcessPoolExecutor
from dataclasses import dataclass
from functools import reduce
from itertools import count
from operator import or_
from pathlib import Path
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union

from atomic_write_path import atomic_write_path
from dateutil.rrule import rrule
from dateutil.tz import EPOCH  # type: ignore
from dateutil.tz import gettz
from dateutil.tz import UTC

from pyworkflows.errors import BeforeTheEpochError
from pyworkflows.errors import RunTasksError
from pyworkflows.task import Task


T = TypeVar("T")
_DEFAULT_EXIST_OK = False
_DEFAULT_OVERWRITE = False
_DEFAULT_PARALLEL = False


class FileTask(Task[T]):
    def __call__(
        self: FileTask[T],
        *,
        overwrite: bool = _DEFAULT_OVERWRITE,
        exist_ok: bool = _DEFAULT_EXIST_OK,
    ) -> T:
        path = self.path()
        if overwrite:
            out = self.compute()
            with atomic_write_path(path, overwrite=True) as temp:
                self.write(out, temp)
            return out
        else:
            try:
                return self.read(path)
            except OSError:
                out = self.compute()
                try:
                    with atomic_write_path(path, overwrite=False) as temp:
                        self.write(out, temp)
                except FileExistsError:
                    if exist_ok:
                        return out
                    else:
                        raise
                else:
                    return out

    @abstractmethod
    def compute(self: FileTask[T]) -> T:
        raise NotImplementedError

    @abstractmethod
    def path(self: FileTask) -> Path:
        raise NotImplementedError

    @abstractmethod
    def read(self: FileTask[T], path: Path) -> T:
        raise NotImplementedError(path)

    @abstractmethod
    def write(self: FileTask, value: T, path: Path) -> None:
        raise NotImplementedError(value, path)

    @classmethod
    def run(
        cls: Type[FileTask],
        tasks: Iterable[FileTask],
        *,
        overwrite: bool = _DEFAULT_OVERWRITE,
        exist_ok: bool = _DEFAULT_EXIST_OK,
        parallel: bool = _DEFAULT_PARALLEL,
    ) -> None:
        as_set: Set[FileTask] = reduce(
            or_,
            ({task} | task.get_dependencies(recurse=True) for task in tasks),
            set(),
        )
        if not overwrite:
            as_set = {task for task in as_set if not task.path().exists()}
        if parallel:
            futures: Dict[Task, Future] = {}
            with ProcessPoolExecutor() as executor:
                while as_set:
                    completed: Set[Task] = set()
                    for task in as_set:
                        try:
                            future = futures[task]
                        except KeyError:
                            if all(
                                dep not in as_set
                                for dep in task.get_dependencies(recurse=True)
                            ) and (task not in futures):
                                futures[task] = executor.submit(
                                    task,
                                    overwrite=overwrite,
                                    exist_ok=exist_ok,
                                )
                        else:
                            if future.done():
                                maybe_exception = future.exception()
                                if maybe_exception is None:
                                    completed.add(task)
                                else:
                                    try:
                                        raise RunTasksError(
                                            f"Task {task} failed",
                                        )
                                    except RunTasksError as error:
                                        raise maybe_exception from error
                    as_set -= completed
        else:
            while as_set:
                task = next(iter(as_set))
                task(overwrite=overwrite, exist_ok=exist_ok)
                as_set.remove(task)


def floor_datetime(
    freq: int,
    *,
    as_of: Union[
        dt.datetime, Callable[..., dt.datetime],
    ] = lambda: dt.datetime.now(tz=UTC),
    interval: int = 1,
    wkst: Optional[int] = None,
    bysetpos: Optional[Union[int, Sequence[int]]] = None,
    bymonth: Optional[Union[int, Sequence[int]]] = None,
    bymonthday: Optional[Union[int, Sequence[int]]] = None,
    byyearday: Optional[Union[int, Sequence[int]]] = None,
    byeaster: Optional[Union[int, Sequence[int]]] = None,
    byweekno: Optional[Union[int, Sequence[int]]] = None,
    byweekday: Optional[Union[int, Sequence[int]]] = None,
    byhour: Optional[Union[int, Sequence[int]]] = None,
    byminute: Optional[Union[int, Sequence[int]]] = None,
    bysecond: Optional[Union[int, Sequence[int]]] = None,
    tz: Union[str, dt.tzinfo] = UTC,
) -> dt.datetime:
    if isinstance(as_of, dt.datetime):
        as_of_use = as_of
    else:
        as_of_use = as_of()
    epoch_utc = EPOCH.replace(tzinfo=UTC)
    if as_of_use < epoch_utc:
        raise BeforeTheEpochError(
            f"{as_of_use} is before the Epoch ({epoch_utc})",
        )

    def get_rrule(
        dtstart: dt.datetime,
        interval: int,
        *,
        count: Optional[int] = None,
        until: Optional[dt.datetime] = None,
        cache: bool = False,
    ) -> rrule:
        return rrule(
            freq,
            dtstart=dtstart,
            interval=interval,
            wkst=wkst,
            count=count,
            until=until,
            bysetpos=bysetpos,
            bymonth=bymonth,
            bymonthday=bymonthday,
            byyearday=byyearday,
            byeaster=byeaster,
            byweekno=byweekno,
            byweekday=byweekday,
            byhour=byhour,
            byminute=byminute,
            bysecond=bysecond,
            cache=cache,
        )

    @dataclass
    class Period:
        start: dt.datetime
        end: dt.datetime
        scale: int

    def get_period(dtstart: dt.datetime) -> Period:
        for scale in (2 ** i for i in count()):
            _, end = get_rrule(
                dtstart=dtstart, interval=scale * interval, count=2,
            )
            if dtstart <= as_of_use <= end:
                break
            else:
                dtstart = end
        return Period(dtstart, end, scale)

    def bisect_period(period: Period) -> dt.datetime:
        if period.scale == 1:
            r = get_rrule(dtstart=period.start, interval=interval, count=100)
            *_, end = r
            if period.start <= as_of_use <= end:
                return r.before(as_of_use, inc=True)
            else:
                return inner(period.start)
        else:
            half_scale, _ = divmod(period.scale, 2)
            _, mid, _ = get_rrule(
                dtstart=period.start, interval=half_scale * interval, count=3,
            )
            if period.start <= as_of_use <= mid:
                start, end = period.start, mid
            else:
                start, end = mid, period.end
            return bisect_period(Period(start, end, half_scale))

    def inner(start: dt.datetime) -> dt.datetime:
        period = get_period(start)
        result = bisect_period(period)
        if isinstance(tz, dt.tzinfo):
            tz_use: Optional[dt.tzinfo] = tz
        else:
            tz_use = gettz(tz)
        return result.astimezone(tz_use)

    return inner(epoch_utc)
