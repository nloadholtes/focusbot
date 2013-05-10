#
# All of the talk interpretation code
#

from focusbot.pomodoro import Pomodoro


def _isIn(list_a, list_b):
    result = set(list_a).intersection(list_b)
    return True if len(result) > 0 else False


class ChatterBox:
    def __init__(self):
        self.pomodoro = None

    def startPomodoro(self):
        if not self.pomodoro:
            self.pomodoro = Pomodoro()
        return self.pomodoro.startPomodoro()

    def process(self, text):
        text = text.lower().split()
        if "pomodoro" in text:
            self.startPomodoro()
            return "Starting"
        else:
            return "Huh?"
