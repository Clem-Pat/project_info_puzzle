from pynput import keyboard
import os

class Command():
    """Module de logique pour le jeu"""

    def __init__(self, matrix_caller):
        """matrix_caller est la matrice de jeu appelant le module de commande"""
        self.matrix_caller = matrix_caller
        self.matrix_caller.control = self
        self.listener = None
        self.window = None

    def __repr__(self):
        return "module permettant de commander le jeu, écouter le clavier, envoyer les messages d'arrêt"

    def begin_listener(self):
        """ Commence à écouter les touches. Appelle 'listen' en cas de touche pressée"""
        with keyboard.Listener(on_press=self.listen) as self.listener:
            self.listener.join()

    def listen(self, key):
        """ détermine la nature de la touche clavier sur laquelle l'utilisateur appuie"""

        if self.listener:
            try: k = key.char  # normal char keys
            except: k = key.name  # other keys
        else:
            k = key.keysym.lower()

        if k in ['up', 'down', 'left', 'right']:
            self.matrix_caller.move_case(k)

        elif k in ['ctrl_l', 'ctrl_r', 'ctrl', 'control_l', 'control_r']: #test d'arrêt du listener et de l'affichage du message d'arrêt
            self.arret()

        elif key == keyboard.Key.esc or k == 'escape':
            print('Sortie du jeu')
            self.kill()

        else:
            print(key, k)

    def test_game_over(self):
        """ vérifie si l'utilisateur gagne """
        k = 1
        for i in range(len(self.matrix_caller[0])):
            for j in range(len(self.matrix_caller)):
                if self.matrix_caller[j][i].valeur != k:
                    return False #l'une des cases n'est pas bien placée, l'utilisateur n'a pas encore gagné
                if k == self.matrix_caller.size[0]*self.matrix_caller.size[1] - 1:
                    self.arret()
                    return True #l'utilisateur gagne
                k+=1
        self.arret()
        return True #l'utilisateur gagne

    def arret(self):
        """l'utilisateur a gagné, on renvoie des messages de victoire"""
        print('')
        print('Bravo vous avez gagné')
        print('Pour sortir du jeu, appuyez sur la touche échap')

    def kill(self, *args):
        """détruit la fenêtre si elle existe ou le listener sinon"""
        if self.window:
            self.window.destroy() #une interface graphique a été ouverte, il faut la détruire
        else:
            self.listener.stop()  #il n'y avait pas d'interface graphique, donc il y avait un listener qu'il faut arrêter
        os._exit(0)

    def reload(self):
        """recommence le jeu"""
        print("l'utilisateur veut recommencer")