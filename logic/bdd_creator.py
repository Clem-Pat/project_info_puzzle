import sqlite3
import os


class Bdd_manager():
    def __init__(self):
        self.init_bdd()

    def init_bdd(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(path[:-6] + "\\BDD\\entire_bdd.bd")
        self.cur = self.conn.cursor()

    def close_bdd(self):
        self.cur.close()
        self.conn.close()

    def add_table(self, name_table, column_names, data=None):
        """create users table"""
        if len(column_names) == 2:
            self.cur.execute(f'CREATE TABLE IF NOT EXISTS {name_table} ({column_names[0]} TEXT, {column_names[1]} TEXT)')
        elif len(column_names) == 3:
            self.cur.execute(f'CREATE TABLE IF NOT EXISTS {name_table} ({column_names[0]} TEXT, {column_names[1]} TEXT, {column_names[2]} TEXT)')

        if data != None : self.fill_table(name_table, column_names, data)
        self.conn.commit()

    def fill_table(self, name_table, column_names, data):
        if len(column_names) == 2:
            self.cur.executemany(f'INSERT INTO {name_table} ({column_names[0]},{column_names[1]}) VALUES (?,?)', data)
        elif len(column_names) == 3:
            self.cur.executemany(f'INSERT INTO {name_table} ({column_names[0]},{column_names[1]},{column_names[2]}) VALUES (?,?,?)', data)
        self.conn.commit()

    def read_all_table(self, name_table, order_by=None, want_printed=False):
        if order_by != None: users_data = self.cur.execute(f"SELECT * FROM {name_table} ORDER BY {order_by}")
        else: users_data = self.cur.execute(f"SELECT * FROM {name_table}")
        if want_printed : #l'utilisateur veut afficher la base de données
            for row in users_data:
                print(row)
        self.conn.commit()
        return users_data

    def read_column(self, name_table, name_column):
        users_data = self.cur.execute(f"SELECT {name_column} FROM {name_table};")
        L = []
        for row in users_data:
            L.append(row[0])
        self.conn.commit()
        return L

    def update_password(self, name_user_to_update, value):
        self.cur.execute(f"UPDATE users SET password='{value}' WHERE username='{name_user_to_update}';")
        self.conn.commit()

    def update_score(self, name_user_to_update, values):
        self.cur.execute(f"UPDATE scores SET games_won='{values[0]}', total_time='{values[1]}' WHERE username='{name_user_to_update}';")
        self.conn.commit()


bdd = Bdd_manager()

L_users = [("Clement", "1234"), ("Zoe", "0000"), ("Benjamin", "1234")]
bdd.add_table('users', column_names=['username', 'password'])
bdd.fill_table('users', column_names=['username', 'password'], data=L_users)

L_scores = [('Clement', '8', '1762'), ('Zoe', '6', '56789'), ('Benjamin', '2', '123456765432')]
bdd.add_table('scores', column_names=['username', 'games_won', 'total_time'])
bdd.fill_table('scores', column_names=['username', 'games_won', 'total_time'], data=L_scores)

bdd.read_all_table('users', order_by='username', want_printed=True)
bdd.update_score('Clement', ['9876', '4567'])
bdd.read_all_table('users', order_by='username', want_printed=True)

print(bdd.read_column('users', 'username'))
bdd.close_bdd()