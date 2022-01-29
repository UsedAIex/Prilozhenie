import sqlite3
from datetime import datetime


class Help_db():
    def __init__(self):
        self.bud_now()

    # удаение данных в БД (истории или избранного)
    def delete_db(self, name_tabel):
        con = sqlite3.connect("db/istr.sqlite")
        cur = con.cursor()
        if name_tabel == 'isbrannie':
            cur.execute("DELETE FROM isbrannie")
        elif name_tabel == 'istoria':
            cur.execute("DELETE FROM istoria")
        con.commit()
        con.close()

    # обновление данных о будильнике
    def budilnik(self, hour, minute, sos):
        con = sqlite3.connect("db/istr.sqlite")
        cur = con.cursor()
        cur.execute('''UPDATE for_budil
                    SET hour = ?''', (hour,))
        cur.execute('''UPDATE for_budil
                            SET minute = ?''', (minute,))
        cur.execute('''UPDATE for_budil
                                    SET sostoianie = ?''', (sos,))
        con.commit()
        con.close()

    # для отключения будильника
    def bu_nik_off(self):
        con = sqlite3.connect("db/istr.sqlite")
        cur = con.cursor()
        cur.execute('''UPDATE for_budil
                                            SET sostoianie = ?''', (False,))
        con.commit()
        con.close()

    # для вывода данных из БД
    def bud_now(self):
        con = sqlite3.connect("db/istr.sqlite")
        cur = con.cursor()
        asd = cur.execute('SELECT * FROM for_budil').fetchall()
        con.close()
        return asd[0][0], asd[0][1], asd[0][2]

    # добавление в базу данных
    def add_db(self, name_table, country):
        con = sqlite3.connect("db/istr.sqlite")
        cur = con.cursor()
        if name_table == 'isbrannie':
            dn = cur.execute("SELECT * FROM isbrannie").fetchall()
            result = cur.execute("SELECT * FROM isbrannie WHERE str=?", (country,)).fetchall()
            if len(result) >= 1:
                return 'YES'
            cur.execute(
                "INSERT INTO isbrannie(id_isbr, id_str, str) VALUES(?, (SELECT id_str FROM all_str WHERE str=?), ?)",
                (len(dn), country, country))
        elif name_table == 'istoria':
            data = str(datetime.now().time())[:8]
            se = cur.execute("SELECT * FROM istoria").fetchall()
            cur.execute('INSERT INTO istoria(id, str, kogda) VALUES(?, ?, ?)', (len(se) + 1, country, data))
        con.commit()
        con.close()

    # для отображения истории или избранных городов
    def otobrazh(self, table):
        global database
        self.con = sqlite3.connect("db/istr.sqlite")
        cur = self.con.cursor()
        if table == 'istoria':
            database = cur.execute("SELECT * FROM istoria").fetchall()
        elif table == 'isbrannie':
            database = cur.execute("SELECT * FROM isbrannie").fetchall()
        return database
