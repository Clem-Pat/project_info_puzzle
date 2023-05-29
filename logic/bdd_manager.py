import sqlite3
import os
import hashlib

class Bdd_manager():
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        already_exists = os.path.exists(self.path[:-6] + "\\BDD\\entire_bdd.bd")
        self.init_bdd()
        if not already_exists:
            print('the data base does not exist on your computer so we will fill it')
            mdps = ['1234', '0000', '9876']
            mdps_sha = []
            for mdp in mdps:
                mdps_sha.append(str(hashlib.sha256(mdp.encode('utf-8')).hexdigest()))
            L_users = [("Clement",mdps_sha[0]) , ("Zoe", mdps_sha[1]), ("Benjamin", mdps_sha[2])]
            self.add_table('users', column_names=['username', 'password'])
            self.fill_table('users', column_names=['username', 'password'], data=L_users)

            L_scores = [('Clement', '8', '1762', '4567', f'{1762+4567}'), ('Zoe', '6', '56789', '6789', f'{56789+6789}'), ('Benjamin', '2', '123456789', '123456789', f'{123456789 + 123456789}')]
            self.add_table('scores', column_names=['username', 'games_won', 'total_time', 'total_number_of_clicks', 'score'])
            self.fill_table('scores', column_names=['username', 'games_won', 'total_time', 'total_number_of_clicks', 'score'], data=L_scores)

    def __repr__(self):
        resu = '\n'
        tables_names = self.get_tables_names()
        for name in tables_names:
            resu += '#### ' + name + ' ####' + '\n'
            L = self.read_all_table(name)
            for row in L:
                for column in row:
                    resu += column
                    for i in range(20-len(list(column))):
                        resu += ' '
                resu += '\n'
            resu += '\n'
        return resu

    def init_bdd(self):
        self.conn = sqlite3.connect(self.path[:-6] + "\\BDD\\entire_bdd.bd")
        self.cur = self.conn.cursor()

    def close_bdd(self):
        self.cur.close()
        self.conn.close()

    def get_tables_names(self):
        names = self.cur.execute(f"SELECT name FROM sqlite_schema WHERE type = 'table' ORDER BY name;")
        L = []
        for name in names:
            L.append(name[0])
        self.conn.commit()
        return L

    def add_table(self, name_table, column_names, data=None):
        """create a table"""
        if name_table == 'users':
            self.cur.execute(f'CREATE TABLE IF NOT EXISTS {name_table} ({column_names[0]} TEXT, {column_names[1]} TEXT);')
        elif name_table == 'scores':
            self.cur.execute(f'CREATE TABLE IF NOT EXISTS {name_table} ({column_names[0]} TEXT, {column_names[1]} TEXT, {column_names[2]} TEXT, {column_names[3]} TEXT, {column_names[4]} TEXT);')

        if data != None : self.fill_table(name_table, column_names, data)
        self.conn.commit()

    def fill_table(self, name_table, column_names, data):
        if name_table == 'users':
            self.cur.executemany(f'INSERT INTO {name_table} ({column_names[0]},{column_names[1]}) VALUES (?,?);', data)
        elif name_table == 'scores':
            self.cur.executemany(f'INSERT INTO {name_table} ({column_names[0]},{column_names[1]},{column_names[2]},{column_names[3]},{column_names[4]}) VALUES (?,?,?,?,?);', data)
        self.conn.commit()

    def read_all_table(self, name_table, order_by=None):
        if order_by != None: users_data = self.cur.execute(f"SELECT * FROM '{name_table}' ORDER BY '{order_by}'")
        else: users_data = self.cur.execute(f"SELECT * FROM '{name_table}'")
        L = []
        for row in users_data:
            L.append(row)
        self.conn.commit()
        return L

    def read_column(self, name_table, name_column, order_by=None):
        if order_by != None : users_data = self.cur.execute(f"SELECT {name_column} FROM '{name_table}' ORDER BY '{order_by}';")
        else: users_data = self.cur.execute(f"SELECT {name_column} FROM '{name_table}';")
        L = []
        for row in users_data:
            L.append(row[0])
        self.conn.commit()
        return L

    def read_line(self, name_table, username_to_read):
        data = self.cur.execute(f"SELECT * FROM {name_table} WHERE username = '{username_to_read}'")
        L = []
        for column in data:
            L.append(column)
        self.conn.commit()
        return L[0]

    def update_password(self, name_user_to_update, value):
        self.cur.execute(f"UPDATE users SET password='{value}' WHERE username='{name_user_to_update}';")
        self.conn.commit()

    def update_score(self, name_user_to_update, values):
        self.cur.execute(f"UPDATE scores SET games_won='{values[0]}', total_time='{values[1]}', total_number_of_clicks='{values[2]}', score='{int(int(values[1])+int(values[2])/int(values[0]))}' WHERE username='{name_user_to_update}';")
        self.conn.commit()

    def add_row(self, name_table, data):
        data_table = self.cur.execute(f'select * from {name_table}')
        column_names = list(map(lambda x: x[0], data_table.description))
        example_name_in_bdd = self.read_column(name_table, 'username')[0]
        if len(self.read_line(name_table, example_name_in_bdd)) == len(data):
            if name_table == 'users':
                self.cur.execute(f'INSERT INTO {name_table} ({column_names[0]},{column_names[1]}) VALUES (?,?);', data)
            elif name_table == 'scores':
                self.cur.execute(f'INSERT INTO {name_table} ({column_names[0]},{column_names[1]},{column_names[2]},{column_names[3]},{column_names[4]}) VALUES (?,?,?,?,?);',data)
        self.conn.commit()


if __name__ == '__main__':
    #test de création de la BDD uniquement
    bdd = Bdd_manager()
    print(bdd)
    bdd.close_bdd()