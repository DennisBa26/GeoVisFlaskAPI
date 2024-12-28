import sqlite3
class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('PLZ.db')
        self.create_plz_table()

    def create_plz_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS "PLZ" (
                id INTEGER PRIMARY KEY,
                PLZ INTEGER,
                PV INTEGER        
            );
        """
        self.conn.execute(query)


class PLZ_PVModel:
    def __init__(self):
        self.conn = sqlite3.connect('PLZ.db')

    def create(self, plz, pv):
        query = f'insert into PLZ(PLZ,PV) values("{plz}","{pv}")'
        result = self.conn.execute(query)
        self.conn.commit()
        return f"Ok {result.lastrowid}"