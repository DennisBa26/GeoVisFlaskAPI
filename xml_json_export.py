import os
import re
import xml.etree.ElementTree as ET
from collections import defaultdict


def calculate_bruttoleistung_per_postleitzahl(directory):
    # Dictionary zur Speicherung der Ergebnisse
    bruttoleistung_per_plz = defaultdict(float)
    pattern_for_filename= re.compile(r"^EinheitenSolar_\d{1,2}\.xml$")

    #für ladebalken


    file_count = sum(1 for file in os.listdir(directory) if pattern_for_filename.match(file))

    counter = 1
    for filename in os.listdir(directory):
        if pattern_for_filename.match(filename):
            progress = int(50 * counter / file_count)
            percent = int(100/file_count*counter)
            bar = "#" * progress + "." * (50 - progress)
            print(f"\r[{bar}] {percent}%", end="", flush=True)

            if filename.endswith('.xml'):
                file_path = os.path.join(directory, filename)

                # XML-Datei parsen
                tree = ET.parse(file_path)
                root = tree.getroot()

                for einheit in root.findall('.//EinheitSolar'):
                    # Bundesland überprüfen (1402 = Baden-Württemberg)
                    bundesland = einheit.find('Bundesland')
                    if bundesland is not None and bundesland.text == '1402':

                        plz = einheit.find('Postleitzahl')

                        bruttoleistung = einheit.find('Bruttoleistung')

                        if plz is not None and bruttoleistung is not None:
                            try:
                                #Leistung in Text mit Tausenderpunkt wird fehlerhaft als dezimal punkt interpretiert
                                leistung = bruttoleistung.text.replace('.','')

                                bruttoleistung_per_plz[plz.text] += float(leistung)
                            except ValueError:
                                print(f"Ungültige Bruttoleistung in Datei {filename}: {bruttoleistung.text}")
        counter+=1

    return bruttoleistung_per_plz