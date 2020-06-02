from typing import List
from unittest.mock import MagicMock, call
from uuid import uuid4

import pytest
from shuttlis.pagination import Cursor
from shuttlis.time import time_now

from cron.cron import KeyedBookmarker, Cron, CronState, Context, get_cron


class FakeBookmark:
    def __init__(self, bookmark_dict=None):
        self._bookmark_dict = bookmark_dict or {}

    def get(self, key: str):
        return self._bookmark_dict.get(key)

    def __setitem__(self, key: str, value: str):
        self._bookmark_dict[key] = value


class FakeEntity:
    def __init__(self, id=None, created_at=None):
        self.id = id or str(uuid4())
        self.created_at = created_at or time_now()


dummy_cursor_val = (
    "2020-05-29T05:31:58.424098+00:00|ddf22144-cdb3-44aa-84a0-2cc0071e11d4"
)
dummy_cursor = Cursor.from_dict({"after": dummy_cursor_val, "limit": 10})


fake_keyed_bookmarker = KeyedBookmarker(bookmarker=FakeBookmark(), key="lol")


def test_cron_context_iteration_update():
    context = Context()
    context.add_iteration([1, 2, 3])
    assert context.iteration == [[1, 2, 3]]


def test_cron_context_error_update():
    context = Context()
    context.add_error(Exception("dummy_error"))
    assert len(context.errors) == 1
    assert str(context.errors[0]) == "dummy_error"


def test_cron_state_change_works_using_set_state():
    cron = Cron(
        keyed_bookmark=None,
        entity_fetcher=None,
        entity_processor=MagicMock(),
        context=None,
    )
    cron.entity_processor.assert_not_called()


def test_cron_context_handler_is_called_on_initial_set_state():
    fake_init_handler = MagicMock()
    context = Context()
    Cron(
        keyed_bookmark=None,
        entity_fetcher=None,
        entity_processor=None,
        context=context,
        on_init_handlers=[fake_init_handler],
    )
    fake_init_handler.assert_called_with(context)


def test_cron_state_is_success_when_no_items_are_passed_without_calling_entity_processor():
    context = Context()

    def fake_entity_fetcher(_) -> List:
        return []

    fake_success_completion_handlers = MagicMock()
    cron = Cron(
        keyed_bookmark=fake_keyed_bookmarker,
        entity_fetcher=fake_entity_fetcher,
        entity_processor=MagicMock(),
        context=context,
        on_success_completion_handlers=[fake_success_completion_handlers],
    )

    cron.process()

    cron.entity_processor.assert_not_called()
    fake_success_completion_handlers.assert_called_once_with(context)
    assert context.iteration == [[]]
    assert cron.state == CronState.SUCCESS


def test_cron_state_is_failed_when_exception_in_entity_processor():
    exc = Exception("dummy_error")
    cntext = Context()

    def fake_entity_fetcher(_) -> List:
        return [FakeEntity()]

    def fake_entity_processor(_):
        raise exc

    fake_failure_handler = MagicMock()

    fake_success_completion_handlers = MagicMock()

    cron = Cron(
        keyed_bookmark=fake_keyed_bookmarker,
        entity_fetcher=fake_entity_fetcher,
        entity_processor=fake_entity_processor,
        context=cntext,
        on_failure_handlers=[fake_failure_handler],
        on_success_completion_handlers=[fake_success_completion_handlers],
    )

    with pytest.raises(Exception):
        cron.process()

    fake_failure_handler.assert_called_once_with(cntext)
    fake_success_completion_handlers.assert_not_called()
    assert cron.state == CronState.FAILED


def test_cron_state_is_success_when_one_item_is_passed():
    fake_entity = FakeEntity()
    context = Context()

    def fake_entity_fetcher(_) -> List:
        return [fake_entity]

    fake_success_completion_handlers = MagicMock()
    cron = Cron(
        keyed_bookmark=fake_keyed_bookmarker,
        entity_fetcher=fake_entity_fetcher,
        entity_processor=MagicMock(),
        context=context,
        on_success_completion_handlers=[fake_success_completion_handlers],
    )

    cron.process()

    cron.entity_processor.assert_called_with([fake_entity])
    fake_success_completion_handlers.assert_called_once_with(context)
    assert context.errors == []
    assert context.iteration == [[fake_entity]]
    assert cron.state == CronState.SUCCESS


def test_cron_process_all_success():
    context = Context()
    f1, f2 = FakeEntity(), FakeEntity()
    fake_success_completion_handlers = MagicMock()
    fakes = iter([f1, f2])

    def fake_entity_fetcher(_) -> List:
        try:
            return [next(fakes)]
        except StopIteration:
            return []

    cron = Cron(
        keyed_bookmark=fake_keyed_bookmarker,
        entity_fetcher=fake_entity_fetcher,
        entity_processor=MagicMock(),
        context=context,
        on_success_completion_handlers=[fake_success_completion_handlers],
    )

    cron.process_all()

    cron.entity_processor.assert_has_calls([call([f1]), call([f2])])
    fake_success_completion_handlers.assert_called_once_with(context)
    assert cron.state == CronState.SUCCESS


def test_cron_process_all_failure():
    context = Context()
    f1 = FakeEntity()
    exc = Exception("dummy_error")
    fakes = iter([f1])

    def fake_entity_fetcher(_) -> List:
        try:
            return [next(fakes)]
        except StopIteration:
            raise exc

    fake_success_completion_handlers = MagicMock()
    fake_failure_handler = MagicMock()
    fake_iter_handler = MagicMock()
    cron = Cron(
        keyed_bookmark=fake_keyed_bookmarker,
        entity_fetcher=fake_entity_fetcher,
        entity_processor=MagicMock(),
        context=context,
        on_success_completion_handlers=[fake_success_completion_handlers],
        on_failure_handlers=[fake_failure_handler],
        on_single_iteration_completion=[fake_iter_handler],
    )

    with pytest.raises(Exception):
        cron.process_all()

    fake_success_completion_handlers.assert_not_called()
    fake_failure_handler.assert_called_once()
    fake_iter_handler.assert_called_once()
    assert context.errors == [exc]
    assert context.iteration == [[f1]]
    assert cron.state == CronState.FAILED


def test_cron_getter():
    cron = get_cron(
        keyed_bookmarker=fake_keyed_bookmarker,
        entity_fetcher=MagicMock(),
        entity_processor=MagicMock(),
    )
    cron.process()
    cron.entity_fetcher.assert_called_once()
    cron.entity_processor.assert_called_once()
