#
# All of the talk interpretation code
#

from focusbot.pomodoro import Pomodoro


class ChatterBox:
    def __init__(self):
        self.pomodoro = None

    def startPomodoro(self):
        if not self.pomodoro:
            self.pomodoro = Pomodoro()
        return self.pomodoro.startPomodoro()

    def process(self, text):
        if "pomodoro" in text.lower():
            self.startPomodoro()
            return "Starting"
        else:
            return "Huh?"
