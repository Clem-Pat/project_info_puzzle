import numpy as np
import random

from case import Case

class Matrix(list):

    def __init__(self, size=(3,3)):
        """
        Matrice de jeu, héritage de la classe Liste de python
        type(size) = tuple || ex : (2,3) (nbre_de_lignes, nbre_de_colonnes)"""

        self.size = size
        list.__init__(self)

        self.random_cases = list(range(self.size[0]*self.size[1]))
        random.shuffle(self.random_cases)

        #création de la matrice
        k=0
        for i in range(self.size[0]):
            self.append([])
            for j in range(self.size[1]):
                valeur = self.random_cases[k]
                case = Case(valeur, (i,j))
                self[-1].append(case)
                k += 1
        print(self)

        self.nbre_coups = 0
        self.position_vide = self.find_case(0)
        self.control = None

    def __repr__(self):
        """Représentation de la matrice. La fonction peut être appelée avec print"""
        try:
            return str(np.array([[self[i][j] for i in range(len(self))] for j in range(len(self[0]))]))
        except:
            return str([])

    def find_case(self, valeur):
        """Renvoie la position ligne-colonne de la case de valeur 'valeur' """
        for i in range(len(self)):
            for j in range(len(self[0])):
                if self[i][j].valeur == valeur:
                    return (i,j)

    def move_case(self, k):
        """Déplace la case zéro dans la matrice de jeu"""
        a,b = self.position_vide
        if k == 'up' :
            if self.position_vide[1] != 0:
                a, b = self.position_vide[0], self.position_vide[1] - 1
                self.nbre_coups += 1
            else: print('up impossible')
        if k == 'down' :
            if self.position_vide[1] != self.size[1]-1:
                a, b = self.position_vide[0], self.position_vide[1] + 1
                self.nbre_coups += 1
            else: print('down impossible')
        if k == 'right' :
            if self.position_vide[0] != self.size[0]-1:
                a, b = self.position_vide[0] + 1, self.position_vide[1]
                self.nbre_coups += 1
            else : print('right impossible')
        if k == 'left' :
            if self.position_vide[0] != 0:
                a, b = self.position_vide[0] - 1, self.position_vide[1]
                self.nbre_coups += 1
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
        print(f'nombre de coups : {self.nbre_coups}')

        self.control.test_game_over()

