import sys
import os
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor

folders_dict = {
        "audio": ['.MP3', '.OGG', '.WAV', '.AMR'],
        "documents": ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'],
        "images": ['.JPEG', '.PNG', '.JPG', '.SVG'],
        "video": ['.AVI', '.MP4', '.MOV', '.MKV'],
        "archives": ['.ZIP', '.GZ', '.TAR'],
    }

def entrypoint():
    if len(sys.argv) == 1:
        print("No path entered.")
    elif len(sys.argv) > 2:
        print("Too many arguments entered.")
    else:
        path_to_organize = sys.argv[1]
        organize_files(Path(path_to_organize))

def normalize(text):
    translation_dict = str.maketrans('ĄąĆćĘęŁłÓóŚśŹźŻż', 'AaCcEeLlOoSsZzZz')
    text = text.translate(translation_dict)
    splitted_name = list(os.path.splitext(text))
    normalized_text = "".join(char if char.isalnum() else "_" for char in splitted_name[0])
    return normalized_text + splitted_name[1]

def organize_files_worker(args):
    p, folders_dict, files_list, known_extensions_list, unknown_extensions_list = args

    for folder_name in folders_dict.keys():
        path_folder = Path(p, folder_name)
        if not path_folder.exists():
            path_folder.mkdir()

    for i in p.iterdir():
        new_name = normalize(i.name)
        try:
            os.rename(Path(p, i.name), Path(p, new_name))
        except Exception as e:
            print(f"Error renaming file {i.name}: {e}")
            continue

    for i in p.iterdir():
        if i.name not in folders_dict:
            if i.is_dir():
                dir = Path(p, i.name)
                if not os.listdir(dir):
                    i.rmdir()
                else:
                    organize_files_worker((dir, folders_dict, files_list, known_extensions_list, unknown_extensions_list))
            elif i.is_file():
                splitted_name = list(os.path.splitext(i))
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
                    shutil.move(Path(p, i.stem), Path(p, "archives"))
                    os.remove(Path(p, i.name))
                else:
                    unknown_extensions_list.append(str(i.suffix))
                files_list.append(str(i.name))
                known_extensions_list.append(str(i.suffix))


def organize_files(p):
    global folders_dict
    files_list = []
    known_extensions_list = []
    unknown_extensions_list = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(organize_files_worker, [(p, folders_dict, files_list, known_extensions_list, unknown_extensions_list)])

    if files_list:
        print(f"List of all files: {files_list}\n")
        print(f"List of all extensions found: {set(known_extensions_list)}\n" if known_extensions_list else "List of all extensions found: 0\n")
        print(f"List of all unknown extensions: {set(unknown_extensions_list)}" if unknown_extensions_list else "List of all unknown extensions: 0\n")
    else:
        print("The folder is empty.")

if __name__ == "__main__":
    entrypoint()
