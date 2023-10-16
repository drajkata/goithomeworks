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

def organizacja_plikow(p):
    
    global folder_dict, lista_plikow, lista_znanych_rozszerzen, lista_nieznanych_rozszerzen

    # Tworzymy nowe foldery per typ
    for folder_name in list(folders_dict.keys()):
        path_folder = Path(p, folder_name)
        try:
            path_folder.mkdir()
        except:
            # Folder już istnieje
            continue
    
    # Iteruję po każdym elemencie i zmieniam nazwę
    for i in p.iterdir():
        #  Zmiana nazwy pliku na znormalizowaną
        new_name = i.name.replace(i.name, normalize(i.name))
        try:
            os.rename(Path(p,i.name), Path(p, new_name))
        except:
            continue
    
    # Iteruję po każdym elemencie i robię porządki
    for i in p.iterdir():       
        if i.name not in list(folders_dict.keys()):
            # Jeżli obiekt to folder, to:
            if i.is_dir():
                # Sprawdzenie, czy folder jest pusty
                dir = Path(p,i.name)
                if len(os.listdir(dir)) == 0: 
                    i.rmdir()
                else:
                    #wykonujemy tutaj rekurencję funkcji
                    organizacja_plikow(dir)
            # Jeżeli obiekt to plik, to:
            elif i.is_file():              
                # Rozdzielenie nazwy pliku od rozszerzenia, celem pogrupowania pliku
                splitted_name = list(os.path.splitext(i))
                # Segregacja pliku
                if splitted_name[1].upper() in folders_dict["audio"]:
                    shutil.move(Path(p, i.name), Path(p, "audio"))
                elif splitted_name[1].upper() in folders_dict["documents"]:
                    shutil.move(Path(p, i.name), Path(p, "documents"))
                elif splitted_name[1].upper() in folders_dict["images"]:
                    shutil.move(Path(p, i.name), Path(p, "images"))
                elif splitted_name[1].upper() in folders_dict["video"]:
                    shutil.move(Path(p, i.name), Path(p, "video"))
                elif splitted_name[1].upper() in folders_dict["archives"]:
                    shutil.unpack_archive(Path(p, i.name), Path(p, i.stem))
                    shutil.move(Path(p, i.stem), Path(p,"archives"))
                    os.remove(Path(p, i.name))

                else:
                    lista_nieznanych_rozszerzen.append(str(i.suffix))
                
                # Wylistowanie
                lista_plikow.append(str(i.name))
                lista_znanych_rozszerzen.append(str(i.suffix))


path_to_organize = sys.argv[1]
to_organize = Path(path_to_organize)
organizacja_plikow(to_organize)

# Wykaz wszystkich plikków
if lista_plikow:
    print(f"Wykaz wszystkich plików: {lista_plikow}\n")
    if lista_znanych_rozszerzen:
        print(f"Lista wszystkich znalezionych rozszerzeń: {set(lista_znanych_rozszerzen)}\n")
    else:
        print("Lista wszystkich znalezionych rozszerzeń: 0\n")
    if lista_nieznanych_rozszerzen:
        print(f"Lista wszystkich nieznanyhch rozszerzeń: {set(lista_nieznanych_rozszerzen)}")
    else:
        print("Lista wszystkich nieznanyhch rozszerzeń: 0\n")
else:
    print("Folder jest pusty")