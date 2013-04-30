from nose.tools import assert_equals, assert_true
from mock import MagicMock as Mock

from focusbot.chatterbox import ChatterBox


class TestChatterBox():
    def setUp(self):
        self.cb = ChatterBox()

    def test_ChatterBox_init(self):
        assert_true(self.cb is not None)

    def test_startPomodoro(self):
        assert_true(self.cb.startPomodoro())

    def test_startPomodoro_via_message(self):
        self.cb.process("pomodoro start")
        assert_true(self.cb.pomodoro)

    def test_startPomodoro_via_message_check_output(self):
        assert_equals("Starting", self.cb.process("pomodoro start"))
