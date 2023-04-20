

class Window():
    def __init__(self, cmd_caller):
        self.cmd_caller = cmd_caller

    def __repr__(self):
        return f'fenêtre graphique pour la matrice {self.cmd_caller.matrix_caller}'