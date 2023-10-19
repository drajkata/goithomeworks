import sys
import os
from pathlib import Path
import shutil


# Normalize function
def normalize(text):
    dictionary = str.maketrans('ĄąĆćĘęŁłÓóŚśŹźŻż', 'AaCcEeLlOoSsZzZz')
    text = text.translate(dictionary)
    splitted_name = list(os.path.splitext(text))
    normalized_text = ""
    for char in splitted_name[0]:
        if not char.isalnum():
            char = "_"
        normalized_text +=char
    splitted_name[0] = normalized_text
    file_name = "".join(splitted_name)
    return file_name

# File extension dictionary
folders_dict = {
    "audio" : ['.MP3', '.OGG', '.WAV', '.AMR'], 
    "documents" : ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'], 
    "images" : ['.JPEG', '.PNG', '.JPG', '.SVG'],
    "video" : ['.AVI', '.MP4', '.MOV', '.MKV'],
    "archives" : ['.ZIP', '.GZ', '.TAR'],
}

files_list = []
known_extensions_list = []
unknown_extensions_list = []

# A function that organizes files in a folder
def organize_files(p):
    
    global folder_dict, files_list, known_extensions_list, unknown_extensions_list

    # We create new folders per type
    for folder_name in list(folders_dict.keys()):
        path_folder = Path(p, folder_name)
        try:
            path_folder.mkdir()
        except:
            # The folder already exists
            continue
    
    # I iterate over each element and change the name
    for i in p.iterdir():
        #  Changing the file name to a normalized one
        new_name = i.name.replace(i.name, normalize(i.name))
        try:
            os.rename(Path(p,i.name), Path(p, new_name))
        except:
            continue
    
    # I iterate over each element and clean up
    for i in p.iterdir():       
        if i.name not in list(folders_dict.keys()):
            # If the object is a folder, then:
            if i.is_dir():
                # Checking if the folder is empty
                dir = Path(p,i.name)
                if len(os.listdir(dir)) == 0: 
                    i.rmdir()
                else:
                    # I'm doing function recursion here
                    organize_files(dir)
            # If the object is a file, then:
            elif i.is_file():              
                # Separating the file name from the extension to group the file
                splitted_name = list(os.path.splitext(i))
                # File segregation
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
                    unknown_extensions_list.append(str(i.suffix))
                # Listing
                files_list.append(str(i.name))
                known_extensions_list.append(str(i.suffix))

# Verify that an argument is provided
if len(sys.argv) == 1:
    print("No path entered.") 
elif len(sys.argv) >2:
    print("Too many arguments entered.")
else:
    path_to_organize = sys.argv[1]
    to_organize = Path(path_to_organize)
    organize_files(to_organize)

# List of all files
if files_list:
    print(f"List of all files: {files_list}\n")
    if known_extensions_list:
        print(f"List of all extensions found: {set(known_extensions_list)}\n")
    else:
        print("List of all extensions found: 0\n")
    if unknown_extensions_list:
        print(f"List of all unknown extensions: {set(unknown_extensions_list)}")
    else:
        print("List of all unknown extensions: 0\n")
else:
    print("The folder is empty.")