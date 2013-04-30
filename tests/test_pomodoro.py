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
