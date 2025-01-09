import os
import sqlite3
import xml_json_export

xml_directory = "./data"
timestampFile = "./lastModified"
class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('PLZ.db')
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='PLZ';")
        load = False
        current_timestamp = os.path.getmtime(xml_directory)
        if os.path.exists(timestampFile):
            with open(timestampFile, 'r') as f:
                stored_timestamp = float(f.read().strip())

            # Vergleiche den gespeicherten Timestamp mit dem aktuellen
            if current_timestamp > stored_timestamp:
                # Wenn das aktuelle Änderungsdatum jünger ist
                load = True
            else:
                # Wenn das aktuelle Änderungsdatum nicht jünger ist
                load = False
        else:
            #Wenn die Textdatei nicht existiert, speichere den aktuellen Timestamp
            with open(timestampFile, 'w') as f:
                f.write(str(current_timestamp))
            load = True

        if load == False:
            pass
        else:
            self.create_plz_table()
            self.init_from_data()

    def create_plz_table(self):
        print("Create Table...")
        query = """
            CREATE TABLE IF NOT EXISTS "PLZ" (
                PLZ INTEGER PRIMARY KEY,
                PV INTEGER        
            );
        """
        self.conn.execute(query)

    def init_from_data(self):
        print("Init data from XML-Files")
        result=xml_json_export.calculate_bruttoleistung_per_postleitzahl(xml_directory)
        counter=0
        for plz,bruttoleistung in sorted(result.items()):
            query = f'insert into PLZ(PLZ,PV) values("{plz}","{bruttoleistung}") ON CONFLICT (PLZ) DO NOTHING'
            self.conn.execute(query)
            counter+=1
        self.conn.commit()
        print()


class PLZ_PVModel:
    def __init__(self):
        self.conn = sqlite3.connect('PLZ.db')

    def get_all(self):
        querry = """
        SELECT * 
        FROM PLZ
        """
        result = self.conn.execute(querry).fetchall()
        return result