from pynput import keyboard
import os
import tkinter as tk
import hashlib
import numpy as np
import time

from game_object.matrix import Matrix
from logic.bdd_manager import Bdd_manager

class Command():
    """Module de logique pour le jeu"""

    def __init__(self, matrix_caller):
        """matrix_caller est la matrice de jeu appelant le module de commande"""
        self.matrix_caller = matrix_caller
        self.matrix_caller.control = self
        self.listener = None
        self.window = None
        self.nbre_coups = 0
        self.user = None
        self.full_screen = False
        self.bdd = Bdd_manager()
        self.t0 = time.time()

        while not self.test_solvable(): #tant que le jeu n'est pas solvable, on change la matrice
            print("la matrice n'est pas résolvable donc on change de matrice")
            self.matrix_caller = Matrix(size=self.matrix_caller.size)
            self.matrix_caller.control = self

    def __repr__(self):
        return "module permettant de commander le jeu, écouter le clavier, envoyer les messages d'arrêt"

    def sort_recursive(self, L, k):
        """Trie la liste L de façon récursive en suivant l'algorithme tri à bulles"""
        if k != len(L):
            i, j = L.index(k), k - 1
            if i != j:
                L[i], L[j] = L[j], L[i]
                self.count_switch += 1
            self.sort_recursive(L, k+1)

    def test_solvable(self):
        """teste si le jeu est résolvable"""
        #D'après ce qu'on a écrit dans le rapport, on peut savoir si le jeu est résolvable ou non
        (i, j) = self.matrix_caller.find_case(0)
        (i, j) = (i+1, j+1) #on ne compte plus comme dans une liste python mais comme dans une matrice mathématiques
        (k, l) = (self.matrix_caller.size[0]-i, self.matrix_caller.size[1]-j)
        self.n = k+l
        L_to_sort = list(np.copy(self.matrix_caller.random_cases))
        L_to_sort.pop((i-1)*self.matrix_caller.size[1] + j -1) #On doit trier la liste sans compter la case vide donc on enlève la case vide de la liste
        self.count_switch = 0 #On compte le nombre de permutations nécessaires pour trier la liste.
        self.sort_recursive(L_to_sort, 1)
        return self.n%2 == self.count_switch%2

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

        elif k in ['ctrl_l', 'ctrl_r', 'ctrl', 'control_l', 'control_r']: #test d'arret du jeu en cas de réussite du casse-tête
            self.game_over()

        elif k == 'r': #L'utilisateur veut recommencer
            self.reload()

        elif key == keyboard.Key.esc or k == 'escape': #L'utilisateur veut sortir du jeu sans avoir fini
            print('Sortie du jeu')
            self.kill()

        elif k == 'space': #L'utilisateur veut mettre le jeu en plein écran
            self.window.attributes('-fullscreen', not self.full_screen)
            self.full_screen = not self.full_screen

        # elif k == 's': #L'utilisateur veut résoudre le puzzle
        #     self.bot = Bot(self)
        #     self.bot.begin()

    def test_game_over(self):
        """ vérifie si l'utilisateur gagne """
        k = 1
        for i in range(len(self.matrix_caller[0])):
            for j in range(len(self.matrix_caller)):
                if self.matrix_caller[j][i].valeur != k:
                    return False #l'une des cases n'est pas bien placée, l'utilisateur n'a pas encore gagné
                if k == self.matrix_caller.size[0]*self.matrix_caller.size[1] - 1:
                    self.game_over()
                    return True #l'utilisateur gagne
                k+=1
        self.game_over()
        return True #l'utilisateur gagne

    def game_over(self):
        """l'utilisateur a gagné, on renvoie des messages de victoire"""
        print('')
        print(f'Bravo vous avez gagné en {self.nbre_coups} coups et {int(time.time()-self.t0)} secondes')
        print('Pour sortir du jeu, appuyez sur la touche échap')

        if self.window != None :
            for i in range(len(self.window.labels)):
                try:
                    self.window.labels[i].place_forget()
                except: pass
            self.window.cmd_buttons[2].place(x=self.window.cmd_buttons[2].x, y=self.window.cmd_buttons[2].y)
            self.window.labels[4]['text'] = f'Bravo vous avez gagné en {self.nbre_coups} coups et en {int(time.time() - self.t0)} secondes.'
            if self.user != None : self.window.labels[4]['text'] += '\nVotre partie est enregistrée'
            self.window.labels[4].place(x=self.window.labels[4].x, y=self.window.labels[4].y)
            for list_of_buttons in self.window.buttons_in_grid:
                for button in list_of_buttons:
                    button.config(state='disabled', disabledforeground='black', cursor='arrow')
            for button in self.window.cmd_buttons:
                if 'Bravo' not in button['text']:
                    button.config(state='disabled', disabledforeground='white', cursor='arrow')
            if self.user != None: #si on s'est connecté à un compte, on met à jour la base de données
                L = self.bdd.read_line('scores', self.user)
                self.bdd.update_score(self.user, [str(int(L[1])+1), str(int(L[2])+int(time.time()-self.t0)), str(int(L[3])+self.nbre_coups)])

    def kill(self, *args):
        """détruit la fenêtre si elle existe ou le listener sinon puis force l'arrêt du programme"""
        if self.window: self.window.destroy() #une interface graphique a été ouverte, il faut la détruire
        else: self.listener.stop()  #il n'y avait pas d'interface graphique, donc il y avait un listener qu'il faut arrêter

        try:
            ######On met à jour le classement######
            f = open('BDD/classement.txt', 'w')
            resu = '#### CLASSEMENT #### \n\n'
            titres = ['Nom', 'Nbre de parties gagnées', 'Temps total', 'Nbre de coups total', 'Score']
            for titre in titres:
                resu += titre
                for i in range(30 - len(list(str(titre)))): resu += ' '  # on rempli de zéros pour avoir un affichage correct
            resu += '\n'
            resu += '-----------------------------------------------------------------------------------------------------------------------------------------------------------\n'
            L = self.bdd.read_all_table('scores')
            # la liste L contient les données toutes en chaines de caractère. On ne peut pas la trier correctement donc on la crée en changeant le type des données (traduire en int)
            L_bis = []
            for row in L:
                L_bis.append([])
                for column in row:
                    if column.isdigit(): L_bis[-1].append(int(column))
                    else: L_bis[-1].append(column)
            #Maintenant on peut trier la liste sur le dernier caractère
            L_bis.sort(key=lambda x: x[-1])
            for row in L_bis:
                for column in row:
                    resu += str(column)
                    for i in range(30 - len(list(str(column)))): resu += ' ' #on rempli de zéros pour avoir un affichage correct
                resu += '\n'
            resu += '\n'
            f.write(resu)
            f.close()
            #### fin de la mise a jour du classement ####
        except:
            pass
        os._exit(0)

    def reload(self):
        """recommence le jeu"""
        size = self.matrix_caller.size
        #on crée une matrice avec la matrice initiale enregistrée dans la variable d'instance 'self.matrix_caller.initial_random_cases'
        self.matrix_caller = Matrix(size=size, list_of_cases=self.matrix_caller.initial_random_cases)
        self.matrix_caller.control = self
        if self.window:
            #On modifie la matrice suport du jeu, on notifie à la fenêtre qu'il faut afficher une autre matrice
            self.window.matrix_caller = self.matrix_caller
            self.window.reload_matrix()
        self.nbre_coups = 0 #On remet à zéro le nombre de coups
        if self.window:
            self.window.labels[2]['text'] = f'Nombre de coups : {self.nbre_coups}'
        print("########### l'utilisateur a recommencé ###########")
        print(self.matrix_caller)

    def get_logger_info(self):
        """fonction appelée après avoir cliqué sur le bouton 'Se connecter' on vérifie que l'utilisateur entré existe bien dans la BDD et que le mot de passe est correct"""
        self.id = [self.entry_user.get(), hashlib.sha256(self.entry_mdp.get().encode('utf-8')).hexdigest()]
        try:
            self.label_error.place_forget()
        except :
            pass
        names = self.bdd.read_column('users', 'username', 'username')
        passwords = self.bdd.read_column('users', 'password', 'username')
        nbre_parties = self.bdd.read_column('scores', 'games_won', 'username')
        scores = self.bdd.read_column('scores', 'score', 'username')

        if self.id[0] in names:
            i = names.index(self.id[0])
            if self.id[1] == passwords[i]:
                self.log_in_app.destroy()
                self.user = self.id[0]
                self.window.cmd_buttons[1]['text'] = self.user #le bouton de connexion affiche le nom du compte désormais connecté
                self.window.labels[3]['text'] = f'Historique du score de {self.user} : {nbre_parties[i]} parties réussies avec un score de {scores[i]}' #On affiche le score total de l'utilisateur
                self.t0 = time.time()
            else:
                self.label_error = tk.Label(self.log_in_app, text='mot de passe incorrect', fg='red', bg='light blue')
                self.label_error.place(x=50, y=125)
                #On supprime ce qu'il y a marqué dans les boîtes de texte :
                self.entry_user.delete(0, 'end')
                self.entry_user.focus_set()
                self.entry_mdp.delete(0, 'end')
        else:
            self.label_error = tk.Label(self.log_in_app, text="nom d'utilisateur inconnu", fg='red', bg='light blue')
            self.label_error.place(x=50, y=125)
            # On supprime ce qu'il y a marqué dans les boîtes de texte :
            self.entry_user.delete(0, 'end')
            self.entry_user.focus_set()
            self.entry_mdp.delete(0, 'end')


    def create_account(self):
        """fonction appelée après avoir cliqué sur le bouton d'inscription. Permet de passer dans la fenêtre d'inscription ou de créer un nouveau compte"""
        try:
            self.label_error.place_forget()
        except:
            pass
        if self.log_in_app['bg'] == 'light blue': #On rentre dans le mode d'inscription, on change la disposition de la fenêtre
            self.log_in_app.title('Inscription')
            self.log_in_app.configure(bg='navy')
            self.button_sign['bg'], self.button_sign['fg'] = 'white', 'black'
            self.button_log.grid_forget() #on supprime le bouton de connexion

        elif self.log_in_app['bg'] == 'navy': #On est déjà dans le mode d'inscription donc on crée l'utilisateur
            name, mdp = str(self.entry_user.get()), str(hashlib.sha256(self.entry_mdp.get().encode('utf-8')).hexdigest()) #on encode le mot de passe
            if name != '' and name != 'identifiant' and mdp != '' and mdp != 'mot de passe':  # On commence seulement un vrai nom d'utilisateur et un vrai mot de passe sont tapés
                names = self.bdd.read_column('users', 'username', 'username')
                if name not in names: #si le nom d'utilisateur n'existe pas déjà, on peut créer l'utilisateur
                    print(f"On crée l'utilisateur {name}")
                    self.bdd.add_row('users', [name, mdp])
                    self.bdd.add_row('scores', [name, 0, 0, 0, 0])
                    # On se connecte avec le compte de l'utilisateur
                    self.log_in_app.destroy()
                    self.user = str(name)
                    self.window.cmd_buttons[1]['text'] = self.user
                    self.window.labels[3]['text'] = f'Connecté à {self.user}'
                    self.t0 = time.time()
                else:  # Le nom d'utilisateur est déjà pris donc on renvoie un message d'erreur
                    self.label_error = tk.Label(self.log_in_app, text="Le nom d'utilisateur existe déjà", fg='red', bg='navy')
                    self.label_error.place(x=30, y=125)

    def log_in(self):
        """fonction appelée quand l'utilisateur veut se connecter : on crée une fenêtre de connexion"""
        def focus_on(event):
            """Lorsqu'on clique sur une boîte de texte, on efface ce qui était écrit dedans, et on commence à écrire en noir"""
            event.widget.delete(0, 'end')
            event.widget['textvariable'] = None
            event.widget['fg'] = 'black'

        print("L'utilisateur veut se connecter")
        self.log_in_app = tk.Tk() #On crée la fenêtre de connexion
        self.log_in_app.title('Connexion')
        self.log_in_app.x, self.log_in_app.y = 600, 300
        self.log_in_app.length, self.log_in_app.height = 230, 200
        self.log_in_app.configure(bg='light blue')
        self.log_in_app.geometry(f'{self.log_in_app.length}x{self.log_in_app.height}+{self.log_in_app.x}+{self.log_in_app.y}')
        self.log_in_app.resizable(width=True, height=True)
        self.button_log = tk.Button(self.log_in_app, text='Se connecter', command=self.get_logger_info)
        self.button_sign = tk.Button(self.log_in_app, text="S'inscrire", command=self.create_account, bg='navy', fg='white')
        self.entry_user = tk.Entry(self.log_in_app, textvariable=tk.StringVar(self.log_in_app, value='identifiant'), fg='grey')
        self.entry_mdp = tk.Entry(self.log_in_app, textvariable=tk.StringVar(self.log_in_app, value='mot de passe'), fg='grey')

        #Pour faciliter l'utilisation, on prévoit de passer d'une boîte de texte à une autre avec 'Tab' ou avec 'Entrée'
        #Pour entry_mdp.bind : Après avoir tapé dans la boîte de texte du mot de passe, et après avoir cliqué sur entrée : si on est dans la fenêtre de connexion, on appelle la fonction de vérification des identifiants. Si on est dans la fenêtre d'inscription, on appelle la fonction de création du compte
        self.entry_user.bind('<Return>', lambda event: self.entry_mdp.focus_set())
        self.entry_mdp.bind('<Return>', lambda event: self.get_logger_info() if self.log_in_app['bg']=='light blue' else self.create_account())
        self.entry_user.bind('<FocusIn>', focus_on)
        self.entry_mdp.bind('<FocusIn>', focus_on)

        #On affiche tout les objets les uns sous les autres en respectant un certain espace entre chaque
        self.entry_user.grid(padx=50, pady=10)
        self.entry_mdp.grid(padx=50, pady=10)
        self.button_log.grid(padx=50, pady=20)
        self.button_sign.grid(padx=50, pady=20)
        self.log_in_app.mainloop()