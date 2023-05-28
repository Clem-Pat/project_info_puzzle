


class Bot():
    """Module de résolution du jeu"""

    def __init__(self, cmd_caller):
        self.cmd_caller = cmd_caller
        self.matrix = self.cmd_caller.matrix_caller
        self.moves = []
        self.find_case = self.matrix.find_case

    def __repr__(self):
        return self.moves

    def begin(self):
        (i, j) = self.find_case(1)
        print(i, j)
