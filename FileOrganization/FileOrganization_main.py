import os
from tkinter.filedialog import askdirectory

path = askdirectory(title="Enter the directory.")
list_archives = os.listdir(path)

dict_archives = {
    "Images": [".png", ".jpg", "jpeg"],
    "Sheets": [".xlsx", ".xls"],
    "PDFs": [".pdf"],
    "CSV": [".csv"],
    "Text": [".txt"],
}

for archive in dict_archives:
    name, extension = os.path.splitext(f"{path}/{archive}")
    for directory in dict_archives:
        if extension in dict_archives[archive]:
            if not os.path.exists(f"{path}/{directory}"):
                os.mkdir(f"{path}/{directory}")
            os.rename(f"{path}/{archive}", f"{path}/{directory}/{archive}")