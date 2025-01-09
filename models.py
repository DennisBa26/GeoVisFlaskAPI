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
        # Initialisiere die Variable, um das neueste Änderungsdatum zu speichern
        latest_mod_time = 0

        for file in os.listdir(xml_directory):
            file_path = os.path.join(xml_directory, file)

            if os.path.isfile(file_path):
                mod_time = os.path.getmtime(file_path)

                # Wenn das Änderungsdatum aktueller ist als das gespeicherte, aktualisieren
                if mod_time > latest_mod_time:
                    latest_mod_time = mod_time

        if os.path.exists(timestampFile):
            with open(timestampFile, 'r') as f:
                stored_timestamp = float(f.read().strip())

            # Vergleiche den gespeicherten Timestamp mit dem aktuellen
            if latest_mod_time > stored_timestamp:
                # Wenn das aktuelle Änderungsdatum jünger ist
                load = True
                with open(timestampFile, 'w') as f:
                    f.write(str(latest_mod_time))
            else:
                # Wenn das aktuelle Änderungsdatum nicht jünger ist
                load = False
        else:
            #Wenn die Textdatei nicht existiert, speichere den aktuellen Timestamp
            with open(timestampFile, 'w') as f:
                f.write(str(latest_mod_time))
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