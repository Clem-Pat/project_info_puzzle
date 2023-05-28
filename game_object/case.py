
class Case():
    def __init__(cls, val, position):
        cls.valeur = val
        cls.position = position
        # return super().__new__(cls, val)

    def __repr__(self):
        return f'{self.valeur}'

    def __int__(self):
        return self.valeur
