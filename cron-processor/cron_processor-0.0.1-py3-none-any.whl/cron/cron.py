from dataclasses import dataclass, field
from enum import Enum
from typing import List, Callable, Any

from bookmark import Bookmarker
from shuttlis.pagination import Cursor, Paginator


@dataclass
class KeyedBookmarker:
    bookmarker: Bookmarker
    key: str

    def update_bookmark(self, value: str) -> None:
        self.bookmarker[self.key] = value

    def get_bookmark(self) -> str:
        return self.bookmarker.get(self.key)


class CronState(Enum):
    INIT = "INIT"
    START = "START"
    ITERATION_END = "ITERATION_END"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


@dataclass(frozen=True)
class Context:
    iteration: List[List[Any]] = field(default_factory=list)
    errors: List[Exception] = field(default_factory=list)

    def add_iteration(self, iteration: List) -> None:
        self.iteration.append(iteration)

    def add_error(self, error: Exception) -> None:
        self.errors.append(error)


class Cron:
    def __init__(
        self,
        keyed_bookmark: KeyedBookmarker,
        entity_fetcher: Callable[[Cursor], List],
        entity_processor: Callable[[List], None],
        context: Context,
        *,
        on_init_handlers: List[Callable[[Context], None]] = None,
        on_start_handlers: List[Callable[[Context], None]] = None,
        on_failure_handlers: List[Callable[[Context], None]] = None,
        on_single_iteration_completion: List[Callable[[Context], None]] = None,
        on_success_completion_handlers: List[Callable[[Context], None]] = None,
    ) -> None:
        self.entity_fetcher = entity_fetcher
        self.entity_processor = entity_processor
        self.bookmarker: KeyedBookmarker = keyed_bookmark
        self._handler_map = {
            CronState.INIT: on_init_handlers or [],
            CronState.START: on_start_handlers or [],
            CronState.FAILED: on_failure_handlers or [],
            CronState.SUCCESS: on_success_completion_handlers or [],
            CronState.ITERATION_END: on_single_iteration_completion or [],
        }
        self._context = context
        self.set_state(CronState.INIT)

    @property
    def state(self) -> CronState:
        return self._state

    def set_state(self, state: CronState) -> None:
        self._state = state
        for handler in self._handler_map[self.state]:
            handler(self._context)

    def process(self: "Cron") -> None:
        self.set_state(state=CronState.START)
        try:
            self._process()
        except StopIteration:
            self.set_state(state=CronState.SUCCESS)
        except Exception as e:
            self._context.add_error(e)
            self.set_state(state=CronState.FAILED)
            raise e
        else:
            self.set_state(state=CronState.SUCCESS)

    def process_all(self: "Cron") -> None:
        self.set_state(state=CronState.START)
        while True:
            try:
                self._process()
            except StopIteration:
                self.set_state(state=CronState.SUCCESS)
                break
            except Exception as e:
                self._context.add_error(e)
                self.set_state(state=CronState.FAILED)
                raise e
            else:
                self.set_state(state=CronState.ITERATION_END)

    def _process(self) -> None:
        present_bookmark = self.bookmarker.get_bookmark()
        cursor = Cursor.from_strings(present_bookmark)
        entities = self.entity_fetcher(cursor)

        if not entities:
            self.bookmarker.update_bookmark(value=present_bookmark)
            self._context.add_iteration([])
            raise StopIteration

        self.entity_processor(entities)
        self._update_bookmark(entities)
        self._context.add_iteration(entities)

    def _update_bookmark(self, events: List) -> None:
        paginator = Paginator.from_data(events)
        cursor = paginator.as_dict()["last"]
        self.bookmarker.update_bookmark(value=cursor)


def get_cron(
    keyed_bookmarker: KeyedBookmarker,
    entity_fetcher: Callable[[Cursor], List],
    entity_processor: Callable[[List], None],
    on_init_handlers: List[Callable[[Context], None]] = None,
    on_start_handlers: List[Callable[[Context], None]] = None,
    on_failure_handlers: List[Callable[[Context], None]] = None,
    on_single_iteration_completion: List[Callable[[Context], None]] = None,
    on_success_completion_handlers: List[Callable[[Context], None]] = None,
) -> Cron:
    return Cron(
        keyed_bookmark=keyed_bookmarker,
        entity_fetcher=entity_fetcher,
        entity_processor=entity_processor,
        context=Context(),
        on_init_handlers=on_init_handlers,
        on_start_handlers=on_start_handlers,
        on_success_completion_handlers=on_success_completion_handlers,
        on_failure_handlers=on_failure_handlers,
        on_single_iteration_completion=on_single_iteration_completion,
    )
