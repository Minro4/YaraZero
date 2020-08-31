class WinCounter:
    def __init__(self):
        self.white = 0
        self.black = 0
        self.draw = 0

    def add(self, result):
        if result == 1:
            self.white += 1
        elif result == 0:
            self.black += 1
        else:
            self.draw += 1

    def __str__(self):
        return "White: " + str(self.white) + "\nBlack: " + str(self.black) + "\nDraw: " + str(self.draw)
