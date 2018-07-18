import sqlite3
conn = sqlite3.connect('drone.db',check_same_thread=False)

class DbInitializeClass:
    @staticmethod
    def dbInit():
        a=0
        # c = conn.cursor()
        # #c.execute('''CREATE TABLE IF NOT EXISTS wp_status(id INTEGER PRIMARY KEY AUTOINCREMENT, uploaded int)''')
        # #c.execute("INSERT INTO wp_status VALUES (1,0)")
        # rows = [(0,1)]
        # c.executemany('insert into wp_status values (?,?)', rows)
        # conn.commit()
        # conn.close()
    @staticmethod
    def update_wp_status_false():
        c = conn.cursor()
        c.execute("UPDATE wp_status set uploaded=0 WHERE id=0")
        conn.commit()
        #conn.close()

    @staticmethod
    def update_wp_status_true():
        c = conn.cursor()
        c.execute("UPDATE wp_status set uploaded=1 WHERE id=0")
        conn.commit()
        #conn.close()

    @staticmethod
    def get_data_wp_status():
        c = conn.cursor()
        c.execute("SELECT * FROM wp_status")
        rows= c.fetchall()
        for row in rows:
            print(row[1])
            return row[1];
        #conn.close()