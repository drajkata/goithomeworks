import sys
import os
from pathlib import Path
import shutil

# Funkcja normalize
def normalize(tekst):
    slownik = str.maketrans('ĄąĆćĘęŁłÓóŚśŹźŻż', 'AaCcEeLlOoSsZzZz')
    tekst = tekst.translate(slownik)
    splitted_name = list(os.path.splitext(tekst))
    normalized_tekst = ""
    for char in splitted_name[0]:
        if not char.isalnum():
            char = "_"
        normalized_tekst +=char
    splitted_name[0] = normalized_tekst
    file_name = "".join(splitted_name)
    return file_name

folders_dict = {
    "audio" : ['.MP3', '.OGG', '.WAV', '.AMR'], 
    "documents" : ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'], 
    "images" : ['.JPEG', '.PNG', '.JPG', '.SVG'],
    "video" : ['.AVI', '.MP4', '.MOV', '.MKV'],
    "archives" : ['.ZIP', '.GZ', '.TAR'],
}

lista_plikow = []
lista_znanych_rozszerzen = []
lista_nieznanych_rozszerzen = []

def organizacja_plikow(sciezka):
    global folder_dict, lista_plikow, lista_znanych_rozszerzen, lista_nieznanych_rozszerzen
    p = Path(sciezka)

    # Tworzymy nowe foldery per typ
    for folder_name in list(folders_dict.keys()):
            path_folder = p / folder_name
            path_folder.mkdir()
    for i in p.iterdir():
        # Jeżli obiekt to folder, to:
        if i.name not in list(folders_dict.keys()):
            if i.is_dir():
                # Sprawdzenie, czy folder jest pusty
                dir = os.listdir( path + "/" + i.name) 
                if len(dir) == 0: 
                    i.rmdir()
                else:
                    #wykonujemy tutaj rekurencję funkcji
                    organizacja_plikow(str(sciezka + "/" + i.name))
            # Jeżeli obiekt to plik, to:
            elif i.is_file():
                # Zmiana nazwy pliku na znormalizowaną
                new_name = i.name.replace(i.name, normalize(i.name))
                shutil.move(p / i.name, p / new_name)
                
                lista_plikow.append(str(i.name))
                lista_znanych_rozszerzen.append(str(i.suffix))
                # Rozdzielenie nazwy pliku od rozszerzenia, celem pogrupowania pliku
                splitted_name = list(os.path.splitext(i))

                # Segregacja pliku
                if splitted_name[1].upper() in folders_dict["audio"]:
                    shutil.move(p / i.name, p / "audio")
                elif splitted_name[1].upper() in folders_dict["documents"]:
                    shutil.move(p / i.name, p / "documents")
                elif splitted_name[1].upper() in folders_dict["images"]:
                    shutil.move(p / i.name, p / "images")
                elif splitted_name[1].upper() in folders_dict["video"]:
                    shutil.move(p / i.name, p / "video")
                elif splitted_name[1].upper() in folders_dict["archives"]:
                    shutil.unpack_archive(p / i.name, p / i.stem)
                    shutil.move(p / i.stem, p / "archives")
                    shutil.rmtree(p / i.name)
                else:
                    lista_nieznanych_rozszerzen.append(str(i.suffix))

path = sys.argv[1]
organizacja_plikow(path)
# Wykaz wszystkich plikków
print(f"Wykaz wszystkich plików: {lista_plikow}\nLista wszystkich znalezionych rozszerzeń: {set(lista_znanych_rozszerzen)}\nLista wszystkich nieznanyhch rozszerzeń: {set(lista_nieznanych_rozszerzen)}")