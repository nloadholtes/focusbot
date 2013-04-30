from nose.tools import assert_equals, assert_true
from mock import MagicMock as Mock

from focusbot.pomodoro import Pomodoro


class TestPomodoro():
    def setUp(self):
        self.p = Pomodoro()

    def test_Pomodoro_init(self):
        assert_true(self.p is not None)

    def test_startPomodoro(self):
        assert_equals(True, self.p.startPomodoro())

    def test_startPomodoro_already_started(self):
        self.p.startPomodoro()
        assert_equals(True, self.p.startPomodoro())

    def test_markInterruption(self):
        assert_equals(1, self.p.markInterruption())

    def test_markInterruption_twice(self):
        self.p.markInterruption()
        assert_equals(2, self.p.markInterruption())

    def test_getInterruptionCount(self):
        self.p.markInterruption()
        assert_equals(1, self.p.getInterruptionCount())
