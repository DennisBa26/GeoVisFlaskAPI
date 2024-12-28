import sqlite3
class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('PLZ.db')
        self.create_plz_table()

    def create_plz_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS "PLZ" (
                PLZ INTEGER PRIMARY KEY,
                PV INTEGER        
            );
        """
        self.conn.execute(query)


class PLZ_PVModel:
    def __init__(self):
        self.conn = sqlite3.connect('PLZ.db')

    def create(self, plz, pv):
        query = f'insert into PLZ(PLZ,PV) values("{plz}","{pv}") ON CONFLICT (PLZ) DO NOTHING'
        result = self.conn.execute(query)
        self.conn.commit()
        return f"Ok {result.lastrowid}"

    def get_all(self):
        querry = """
        SELECT * 
        FROM PLZ
        """
        result = self.conn.execute(querry).fetchall()
        return result