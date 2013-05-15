#
# All of the talk interpretation code
#

from focusbot.pomodoro import Pomodoro


def _isIn(list_a, list_b):
    result = set(list_a).intersection(list_b)
    return True if len(result) > 0 else False

START_WORDS = ["start", "begin", "now", "yes"]
STOP_WORDS = ["stop", "quit", "end"]


class ChatterBox:

    def __init__(self):
        self.pomodoro = None

    def startPomodoro(self):
        if not self.pomodoro:
            self.pomodoro = Pomodoro()
        return self.pomodoro.startPomodoro()

    def stopPomodoro(self):
        if not self.pomodoro:
            return
        return self.pomodoro.endPomodoro()

    def startPomodoroRest(self):
        if self.pomodoro and not self.pomodoro.inprogress:
            self.pomodoro.startRest()

    def stopPomodoroRest(self):
        if self.pomodoro and not self.pomodoro.inprogress:
            self.pomodoro.startRest()

    def process(self, text):
        text = text.lower().split()
        if "pomodoro" in text:
            if _isIn(START_WORDS, text):
                self.startPomodoro()
                return "Starting"
            elif _isIn(STOP_WORDS, text):
                self.stopPomodoro()
                return "Stoping"
        else:
            return "Huh?"
