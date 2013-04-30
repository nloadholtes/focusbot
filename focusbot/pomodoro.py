#
#
#


class Pomodoro:
    def __init__(self):
        self.inprogress = False

    def startPomodoro(self):
        if not self.inprogress:
            self.inprogress = True
        return self.inprogress

    def endPomodoro(self):
        if self.inprogress:
            self.inprogress = False
        return self.inprogress
