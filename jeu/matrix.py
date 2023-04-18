import numpy as np
import random
from pynput import keyboard
import copy

from case import Case

class Matrix(list):
    # def __new__(cls, size=(3,3)):
    #     #cls = [[0 for j in range(size[1])] for i in range(size[0])]
    #     cls.size = size
    #     return super().__new__(cls, [[0 for j in range(size[1])] for i in range(size[0])])

    def __init__(self, size=(3,3)):
        """type(size) = tuple || ex : (2,3) (nbre_de_lignes, nbre_de_colonnes)"""
        #np.array.__init__(self, size)
        self.size = size
        list.__init__(self)
        self.random_cases = list(range(self.size[0]*self.size[1]))
        random.shuffle(self.random_cases)

        print(self.random_cases)
        k=0
        for i in range(self.size[0]):
            self.append([])
            for j in range(self.size[1]):
                valeur = self.random_cases[k]
                case = Case(valeur, (i,j))
                self[-1].append(case)
                k += 1
        print(self)

        self.position_vide = self.find_case(0)
        print(self.position_vide)

        with keyboard.Listener(on_press=self.listen) as self.listener:
            self.listener.join()

    def __repr__(self):
        try:
            return str(np.array([[self[i][j] for i in range(len(self))] for j in range(len(self[0]))]))
        except:
            return str([])

    def listen(self, key):

        if key == keyboard.Key.esc:
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys

        if k in ['up', 'down', 'left', 'right']:
            self.move_case(k)

        elif k in ['ctrl_l','ctrl_r','ctrl']:
            print('')
            print('Bravo vous avez gagné')
            self.listener.stop()

    def find_case(self, valeur):
        for i in range(len(self)):
            for j in range(len(self[0])):
                if self[i][j].valeur == valeur:
                    return (i,j)

    def move_case(self, k):
        a,b = self.position_vide

        if k == 'up' :
            if self.position_vide[1] != 0:
                a, b = self.position_vide[0], self.position_vide[1] - 1
            else: print('up impossible')
        if k == 'down' :
            if self.position_vide[1] != self.size[1]-1:
                a, b = self.position_vide[0], self.position_vide[1] + 1
            else: print('down impossible')
        if k == 'right' :
            if self.position_vide[0] != self.size[0]-1:
                a, b = self.position_vide[0] + 1, self.position_vide[1]
            else : print('right impossible')
        if k == 'left' :
            if self.position_vide[0] != 0:
                a, b = self.position_vide[0] - 1, self.position_vide[1]
            else : print('left impossible')

        self[a][b].position = self.position_vide
        self[self.position_vide[0]][self.position_vide[1]].position = (a, b)
        case_vide = self[self.position_vide[0]][self.position_vide[1]]
        case_pleine = self[a][b]
        self[self.position_vide[0]][self.position_vide[1]] = case_pleine
        self[a][b] = case_vide
        self.position_vide = (a, b)

        print('')
        print(self)
        if self.test_game_over():
            print('')
            print('Bravo vous avez gagné')
            self.listener.stop()

    def test_game_over(self):
        k = 1
        for i in range(len(self[0])):
            for j in range(len(self)):
                if self[j][i].valeur != k:
                    return False
                if k == self.size[0]*self.size[1] - 1:
                    return True
                k+=1
        return True
