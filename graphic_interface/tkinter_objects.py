import tkinter as tk

from pynput.mouse import Button, Controller
import time
import os

class Tkinter_frame(tk.Frame):
    """Frame dans la fenêtre du jeu, analogue à la matrice, elle contient les boutons_case_button"""
    def __init__(self, window, id):
        tk.Button.__init__(self, window, bg='navy')
        self.window = window
        self.id = id
        if self.id == 0:
            self.x, self.y = 100, 75

class Tkinter_case_button(tk.Button):
    '''Créer les boutons correspondant aux cases de la matrice'''
    def __init__(self, window, id, position):
        tk.Button.__init__(self, window.frames[0])
        self.window = window
        self.parent = window.frames[0]
        self.id, self.position = id, position
        self.width, self.height = 6, 2
        if self.id == '0':
            self.config(width=self.width, height=self.height, bg="light blue", fg='black',
                        font="GROBOLD.ttf 30", relief=tk.RAISED, cursor='arrow', command=self.move_case)

        else:
            self.bg = 'blue'
            self.config(text=self.id, width=self.width, height=self.height, bg="blue", fg='black', font="GROBOLD.ttf 30",
                        relief=tk.RAISED, cursor='hand2', command=self.move_case)

    def move_case(self):
        position_vide = self.window.matrix_caller.position_vide
        if self.position[0] == position_vide[0] - 1 and self.position[1] == position_vide[1]:
            self.window.matrix_caller.move_case('left')
        elif self.position[0] == position_vide[0] + 1 and self.position[1] == position_vide[1]:
            self.window.matrix_caller.move_case('right')
        elif self.position[0] == position_vide[0] and self.position[1] == position_vide[1] - 1:
            self.window.matrix_caller.move_case('up')
        elif self.position[0] == position_vide[0] and self.position[1] == position_vide[1] + 1:
            self.window.matrix_caller.move_case('down')

class Tkinter_command_button(tk.Button):
    '''Créer les boutons de commande du jeu, pas ceux de la matrice'''

    def __init__(self, window, id, text='Aucun texte'):
        tk.Button.__init__(self, window)
        self.window = window
        self.text = text
        self.id = id
        if self.id == 0:
            self.text = 'Recommencer'
            self.bg, self.hover_bg = 'red', 'pink'
            self.x, self.y = 1300, 50
            self.config(text=self.text, width=12, height=1, bg=self.bg, fg='white', font="GROBOLD.ttf 10",
                    relief=tk.RAISED, cursor='hand2', command=self.window.cmd_caller.reload)
        elif self.id == 1:
            self.text = 'Se connecter'
            self.bg, self.hover_bg = 'blue', 'navy'
            self.x, self.y = 1300, 10
            self.config(text=self.text, width=12, height=1, bg=self.bg, fg='white', font="GROBOLD.ttf 10",
                        relief=tk.RAISED, cursor='hand2', command=self.window.cmd_caller.log_in)
        elif self.id == 2:
            self.text = 'Bravo !! Vous avez gagné'
            self.bg, self.hover_bg = 'green', 'light green'
            self.x, self.y = 800, 200
            self.config(text=self.text, width=20, height=3, bg=self.bg, fg='black', font="GROBOLD.ttf 25",
                        relief=tk.RAISED, cursor='hand2', command=self.window.cmd_caller.kill)
        self.bind("<Enter>", self.hover) #effet de style lorsqu'on survole le bouton
        self.bind("<Leave>", self.hover) #idem

    def hover(self,event):
        '''change la couleur lorsqu'on passe au dessus du bouton'''
        try:
            if self['bg']==self.bg:
                self.configure(bg=self.hover_bg)
            elif self['bg']==self.hover_bg:
                self.configure(bg=self.bg)
        except:
            pass


class Tkinter_label(tk.Label):

    def __init__(self, window, id):
        tk.Label.__init__(self, window)

        self.id = id
        self.window = window

        if self.id == 0:
            self.config(text='Puzzle - Taquin', bg='light blue', fg='blue', font='Arial 30 bold')
            self.x, self.y = 820, 200
        elif self.id == 1:
            self.config(text="Remettez les pièces dans l'ordre",
                        bg='light blue', fg='black', font='Arial 15')
            self.x, self.y = 820, 300
        elif self.id == 2:
            self.config(text=f'Nombre de coups : {self.window.cmd_caller.nbre_coups}', bg='light blue', fg='blue',
                        font='Arial 15 bold')
            self.x, self.y = 820, 400
        elif self.id == 3: #historique des parties de l'utilisateur
            self.config(text='', bg='light blue', fg='blue',
                        font='Arial 11 bold')
            self.x, self.y = 820, 500
        elif self.id == 4: #message d'arrêt
            self.config(text='Bravo, vous avez gagné', bg='light blue', fg='blue',
                        font='Arial 15 bold')
            self.x, self.y = 820, 400