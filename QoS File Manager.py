from pathlib import Path
import glob
import re
import os
import shutil
from tkinter import *

root = Tk()
frame = Frame(root)
frame.pack(padx=200, pady=100)

label1 = Label(frame, text='Logfiles Folder Path', fg='black', bg='grey')
logfiles_folder = Entry(frame)
button1 = Button(frame, text='Execute', fg='black', bg='gray', command=lambda: execute(logfiles_folder.get()))
button2 = Button(frame, text='Quit', fg='black', bg='gray', command=root.destroy).pack(side=BOTTOM)

label1.pack(expand=TRUE, fill=X)
button1.pack(side=BOTTOM)
logfiles_folder.pack(side=LEFT)

# *****menu**********
menu = Menu(frame)
root.config(menu=menu)

submenu = Menu(menu)
menu.add_cascade(label='File', menu=submenu)
submenu.add_command(label='New Project')
submenu.add_separator()
submenu.add_command(label='Exit')

editmenu = Menu(menu)
menu.add_cascade(label='Settings', menu=editmenu)
editmenu.add_command(label='Devices')

# ******toolbar******

toolbar = Frame(root, bg='gray')
insertButton = Button(toolbar, text='Insert Image')
insertButton.pack(side=LEFT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)


def create_folders(x):
    global MNOs
    MNOs = ['MTN', 'Vodafone', 'AirtelTigo', 'Glo']
    Services_Folders = ['MOC', 'MTC', '3GCov', '4GCov', '3GData', '4GData']

    for network in MNOs:
        for location in Districts:
            for folder in Services_Folders:
                parent = os.path.join(x, network, location, location + " " + network + folder)
                try:
                    os.makedirs(parent)

                except FileExistsError:
                    return


def rename_files_voice(filename_path):

    filename = filename_path.name
    for w in voicedictionary:
        if filename.endswith(w):
            new = district_name + " " + voicedictionary[w] + " " + new_address_1 + " " + filename
            filename_path.rename(Path(filename_path.parent, new))
            break


def rename_files_data(filename_path):

    filename = filename_path.name
    for w in datadictionary:
        if filename.endswith(w):
            new = district_name + " " + datadictionary[w] + " " + new_address_1 + " " + filename
            filename_path.rename(Path(filename_path.parent, new))
            break

def get_file_list(x):
    global file_list
    file_list = []
    for paths, folder, files in os.walk(x):
        for file in files:
            file_list.append(os.path.join(paths, file))


def get_folder_list(x):
    global folder_list
    folder_list = []
    for paths, folders, files in os.walk(x):
        for folder in folders:
            for network in MNOs:
                if folder == network:
                    for x, y, z in os.walk(os.path.join(paths, folder)):
                        for yy in y:
                            folder_list.append(os.path.join(x, yy))


def match_files_folders(x):
    for file in file_list:
        file_name = file.split("_")[2:5]
        file_name.sort()
        for folder in folder_list:
            folder_name_string = folder.split("\\")[-1]
            folder_name = folder_name_string.split('_')
            folder_name.sort()
            if file_name == folder_name:
                shutil.move(file, folder)
                break


# def match_files(x)

def execute(x):
    global new_address
    global district_name
    global new_address_1
    global datadictionary
    global voicedictionary
    global Districts
    global non_districts


    voicedictionary = {".1.nmf": "MTNMOC", ".2.nmf": "VodafoneMOC", ".3.nmf": "AirtelTigoMOC",
                       ".4.nmf": "GloMTC", ".5.nmf": "MTNMTC", ".6.nmf": "VodafoneMTC",
                       ".7.nmf": "AirtelTigoMTC", ".8.nmf": "GloMTC", ".9.nmf": "MTN3GCov",
                       "10.nmf": "Vodafone3GCov", "11.nmf": "AirtelTigo3GCov", "12.nmf": "Glo3GCov",
                       "13.nmf": "MTN4GCov", "14.nmf": "Vodafone4GCov"}

    datadictionary = {".1.nmf": "MTN3GData", ".1.pcap": "MTN3GData", ".2.nmf": "Vodafone3GData",
                      ".2.pcap": "Vodafone3GData", ".3.nmf": "AirtelTigo3GData", ".3.pcap": "AirtelTigo3GData",
                      ".4.nmf": "Glo3GData", ".4.pcap": "Glo3GData", ".5.nmf": "MTN4GData", ".5.pcap": "MTN4GData",
                      ".6.nmf": "Vodafone4GData", ".6.pcap": "Vodafone4GData"}

    districts_list = ['Goaso', 'Kukuom', 'Kenyasi', 'Hwidiem', 'Duayaw', 'Nkwanta', 'Bechem', 'Adansi Asokwa',
                       'Akrofuom', 'Asokwa', 'Barekese', 'Boamang', 'Juaben', 'Kwadaso', 'Manso Adubia',
                        'Oforikrom', 'Old Tafo', 'Tafo', 'Suame', 'Tutuka', 'Twedie', 'Effiduase', 'Fomena', 'NewEdubiase',
                        'Kodie', 'Tepa', 'Mankranso', 'Jacobu', 'Manso Nkwanta', 'Konongo', 'Agogo',
                        'Juaso', 'Asokore Mampong', 'Nyinahin', 'Nkawie', 'Bekwai', 'Asiwa', 'Kuntanse', 'Ejisu',
                        'Ejura', 'Kumasi', 'Mamponteng', 'Mampong', 'Obuasi', 'Offinso', 'Akomadan', 'Drobonso', 'Nsuta', 
                        'Kumawu', 'Agona', 'Dwinyame', 'Adugyama', 'Jinijini', 'Banda Ahenkro', 'Berekum', 'Dormaa',
                        'Wemfie', 'Nkrankwanta', 'Sampa', 'Drobo', 'Sunyani', 'Odomasi', 'Nsawkaw', 'Wenchi', 'Prang', 
                        'Atebubu', 'Kintampo', 'Jema', 'Nkoranza', 'Busunya', 'Yeji', 'Kajaji', 'Kwame Danso', 'Techiman',
                        'Tuoabodom', 'Assin Bereku', 'Potsin', 'Dunkwa', 'Nsaba', 'Swedru', 'Ajumako', 'Breman Asikuma',
                        'Assin Fosu', 'Nsuaem-Kyekyewere', 'Kasoa', 'Awutu Breku', 'Cape Coast', 'Winneba', 'Apam',
                        'Afransi', 'Essarkyir', 'Elmina', 'Saltpond', 'Twifo Praso', 'Hemang', 'Dunkwa-On-Offin', 'Diaso',
                        'Achiase', 'Adukrom', 'Anyinam', 'Effiduase', 'Kukurantumi', 'Manso', 'Osino', 'Akropong', 'Aburi', 
                        'Ofoase', 'Atimpoku', 'Kwabeng', 'Coaltar', 'Akim Oda', 'New Abirim', 'Akim Swedru', 'Akwatia',
                        'Kibi', 'Begoro', 'Kade', 'Donkorkrom', 'Tease', 'Abetifi', 'Mpraeso', 'Nkawkaw', 'Odumase', 'Koforidua', 
                        'Nsawam', 'Suhum', 'Asesewa', 'Adeiso', 'Asamankese', 'Somanya', 'Accra New Town', 'Dansoman', 'Darkuman',
                        'Dzorwulu', 'Kokomlemle', 'Lartebiokorshie', 'Ngleshie Amanfro', 'Nima', 'Nungua', 'Ofankor', 'Osu', 'Tema Community 18',
                        'Tesano', 'Accra', 'Sege', 'Ada Foah', 'Adenta', 'Ashaima', 'Sowutuom', 'Abokobi', 'Amasaman',
                        'La', 'Teshie', 'Madina', 'Prampram', 'Dodowa', 'Tema', 'Kpone', 'Weija', 'Yunyoo', 'Bunkpurugu', 'Chereponi', 'Gambaga', 
                        'Yagaba', 'Walewale', 'Nanton', 'Gushegu', 'Karaga', 'Kpandai', 'Kumbungu', 'Sang', 'Bimbilla', 'Wulensi', 'Saboba', 
                        'Sagnarigu', 'Savelugu', 'Tamale', 'Tatale', 'Tolon', 'Yendi', 'Zabzugu', 'Nkonya', 'Jasikan', 'Kadjebi', 'Dambai', 'Chinderi', 
                        'Kete Krachi', 'Kpassa', 'Nkwanta', 'Kpalbe', 'Bole', 'Buipe', 'Salaga', 'Daboya', 'Sawla', 'Damango', 'Tempane', 'Zuarugu',
                        'Bawku', 'Zebilla', 'Binduri', 'Bolgatanga', 'Bongo', 'Sandema', 'Fumbisi', 'Garu', 'Navrongo', 'Paga', 'Nangodi', 'Pusiga', 
                        'Tongo', 'Issa', 'Jirapa', 'Lambussie', 'Lawra', 'Nadowli', 'Nandom', 'Tumu', 'Gwollu', 'Funsi', 'Wa', 'Weichiau', 'Anloga', 
                        'Adaklu Waya', 'Ve-Golokwati', 'Kpetoe', 'Ave', 'Dakpa', 'Akatsi', 'Adidome', 'Ho', 'Dzolokpuita', 'Hohoe', 'Keta', 'Dzodze',
                        'Denu', 'Kpando', 'Anfeoga', 'Battor Dugame', 'Kpeve', 'Sogakope', 'Kwesimintsim', 'Agona Ahanta', 'Manso Amenfi',
                        'Wassa-Akropong', 'Asankrangwa', 'Nkroful', 'Half Assini', 'Mpohor', 'Axim', 'Prestea', 'Sekondi', 'Shama', 'Tarkwa', 'Daboase',
                        'Enchi', 'Adabokrom', 'Essam', 'Bibiani', 'Bodi', 'Juaboso', 'Akontombra', 'Wiawso', 'Dadieso']

    files = glob.glob(x + "/**/*.nmf", recursive=True)

    for paths, dirs, f in os.walk(x):
        Districts = next(os.walk(x))[1]

    non_districts = []

    for d in Districts:
        if d not in districts_list:
            non_districts.append(d)


    if len(non_districts) > 0:
        root = Tk()
        for r in non_districts:
            label = Label(root, text=str(r + ' is not a district, please check spelling!'))
            label.pack()
        root.mainloop()
        exit()

    create_folders(x)

    for filename_address in files:
        filename_path = Path(filename_address)
        filename_parts = filename_path.parts
        district_name = filename_parts[-4]
        new_address_full = filename_parts[-4] + filename_parts[-3] + filename_parts[-2]
        new_address_1 = filename_parts[-3] + filename_parts[-2]
        new_address = new_address_full.split(" ")[0]

        if "Voice" in filename_parts:
            for w in voicedictionary:
                if filename_path.name.endswith(w):
                    if not filename_path.name.startswith(district_name + voicedictionary[w]):
                        rename_files_voice(filename_path)
                    break

        elif "Data" in filename_parts:
            for d in datadictionary:
                if filename_path.name.endswith(d):
                    if not filename_path.name.startswith(district_name + datadictionary[d]):
                        rename_files_data(filename_path)
                    break

    file_list = glob.glob(x + "/**/*.nmf", recursive=True)
    folder_list = glob.glob(x + "/**", recursive=True)

    for file in file_list:
        file_path = Path(file)
        file_path_stem = file_path.stem
        file_string = file_path_stem.split(" ")[0] + " " + file_path_stem.split(" ")[1]
        for folder in folder_list:
            folder_path = Path(folder)
            folder_path_stem = folder_path.stem
            if file_string == folder_path_stem:
                new_file = folder_path / file_path.name
                if new_file.exists():
                    break
                file_path.replace(new_file)
                break



# *****widgets*****


root.mainloop()
