#
# Basic guts of a pomodoro
#


class Pomodoro:
    def __init__(self):
        self.inprogress = False
        self.interruption_count = 0

    def startPomodoro(self):
        if not self.inprogress:
            self.inprogress = True
        return self.inprogress

    def endPomodoro(self):
        if self.inprogress:
            self.inprogress = False
        return self.inprogress

    def markInterruption(self):
        self.interruption_count += 1
        return self.interruption_count

    def getInterruptionCount(self):
        return self.interruption_count
