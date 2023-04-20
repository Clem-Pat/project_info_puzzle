import matrix
from command import Command


if __name__ == '__main__':
    matrice = matrix.Matrix(size=(3,3))
    Command(matrice).begin_listener()