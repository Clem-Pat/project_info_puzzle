import tkinter as tk
import time

from graphic_interface.tkinter_objects import Tkinter_frame, Tkinter_case_button, Tkinter_command_button, Tkinter_label

class Window(tk.Tk):
    def __init__(self, cmd_caller, name='Puzzle'):
        tk.Tk.__init__(self)
        self.cmd_caller = cmd_caller
        self.cmd_caller.window = self
        self.matrix_caller = self.cmd_caller.matrix_caller
        self.name = name
        self.t0 = time.time()
        self.x, self.y = 0, 0
        self.length, self.height = 1500, 500

        self.config()

    def __repr__(self):
        return f'fenêtre graphique pour la matrice {self.cmd_caller.matrix_caller}'

    def config(self):
        self.title(self.name)
        self.configure(bg='light blue')
        self.minsize(1270, 300)
        self.geometry(f'{self.length}x{self.height}+{self.x}+{self.y}')
        self.resizable(width=True, height=True)

        self.frames = [Tkinter_frame(self, i) for i in range(1)]
        self.cmd_buttons = [Tkinter_command_button(self, i) for i in range(1)]
        self.labels = [Tkinter_label(self, i) for i in range(3)]
        self.objects = [self.frames, self.cmd_buttons, self.labels]

        for list_object in self.objects:
            for object in list_object:
                object.place(x=object.x, y=object.y)

        matrix_size = self.matrix_caller.size
        self.buttons_in_grid = []
        k = 0
        for i in range(matrix_size[0]):
            self.buttons_in_grid.append([])
            for j in range(matrix_size[1]):
                button = Tkinter_case_button(self, str(self.matrix_caller[i][j]), (i,j))
                button.grid(row=j, column=i, padx=2, pady=2)
                self.buttons_in_grid[-1].append(button)
                k += 1

        self.update()

        self.bind('<KeyPress>', lambda event: self.cmd_caller.listen(event))
        self.protocol('WM_DELETE_WINDOW', self.cmd_caller.kill)
