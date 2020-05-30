import time

from abzar.timer import Timer


def test_timer_returns_correct_value():

    with Timer() as timer:
        time.sleep(1)

    assert 1000 <= timer.total <= 1050
