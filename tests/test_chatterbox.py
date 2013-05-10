from nose.tools import assert_equals, assert_true, assert_false
from mock import MagicMock as Mock

from focusbot.chatterbox import ChatterBox, _isIn


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

    def test__isIn_true(self):
        a = ["word", "that", "might", "be"]
        b = ["might"]
        assert_true(_isIn(b, a))

    def test__isIn_false(self):
        a = ["word", "that", "might", "be"]
        b = ["airplane"]
        assert_false(_isIn(b, a))
