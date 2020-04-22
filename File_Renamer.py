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

    for paths, dirs, files in os.walk(x):
        districts = next(os.walk(x))[1]

    MNOs = ['_MTN', '_Voda', '_AT', '_Glo']
    Services_Folders = ['MOC', 'MTC', '3G Coverage', '4G Coverage', '3G Data', '4G Data']

    for network in MNOs:
        for location in districts:
            for folder in Services_Folders:
                parent = os.path.join(x, network, network+'_'+location, network+'_'+location+'_'+folder)
                try:
                    os.makedirs(parent)

                except FileExistsError:
                    return

def rename_files_voice(x):

    for file in os.listdir(x):
        file_name, file_ext = os.path.splitext(file)
        full_path = os.path.abspath(x).split('\\')[-2]+'_'+ os.path.abspath(x).split('\\')[-1]+'_'+os.path.abspath(x).split('\\')[-3]
        if file_name[-2:] == '.1':
            os.rename(file, full_path+'_MTN_MOC_'+file)
        elif file_name[-2:] == '.2':
            os.rename(file, full_path+'_VODA_MOC_'+file)
        elif file_name[-2:] == '.3':
            os.rename(file, full_path+'_AT_MOC_'+file)
        elif file_name[-2:] == '.4':
            os.rename(file, full_path+'_GLO_MOC_'+file)
        elif file_name[-2:] == '.5':
            os.rename(file, full_path+'_MTN_MTC_'+file)
        elif file_name[-2:] == '.6':
            os.rename(file, full_path+'_VODA_MTC_'+file)
        elif file_name[-2:] == '.7':
            os.rename(file, full_path+'_AT_MTC_'+file)
        elif file_name[-2:] == '.8':
            os.rename(file, full_path+'_GLO_MTC_'+file)
        elif file_name[-2:] == '.9':
            os.rename(file, full_path+'_MTN_3G Coverage_'+file)
        elif file_name[-2:] == '10':
            os.rename(file, full_path+'_VODA_3G Coverage_'+file)
        elif file_name[-2:] == '11':
            os.rename(file, full_path+'_AT_3G Coverage_'+file)
        elif file_name[-2:] == '12':
            os.rename(file, full_path+'_GLO_3G Coverage_'+file)
        elif file_name[-2:] == '13':
            os.rename(file, full_path+'_MTN_4G Coverage_'+file)


def rename_files_data(x):
    for file in os.listdir(x):
        file_name, file_ext = os.path.splitext(file)
        full_path = os.path.abspath(x).split('\\')[-2]+'_'+ os.path.abspath(x).split('\\')[-1]+'_'+os.path.abspath(x).split('\\')[-3]
        if file_name[-2:] == '.1':
            os.rename(file, full_path + '_MTN_3G Data_' + file)
        elif file_name[-2:] == '.2':
            os.rename(file, full_path + '_Voda_3G Data_' + file)
        elif file_name[-2:] == '.3':
            os.rename(file, full_path + '_AT_3G Data_' + file)
        elif file_name[-2:] == '.4':
            os.rename(file, full_path + '_Glo_3G Data_' + file)
        elif file_name[-2:] == '.5':
            os.rename(file, full_path + '_MTN_4G Data_' + file)


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
            folder_name = folder.split("_")[-3:]
            if len(folder_name) >= 3:
                folder_list.append(os.path.join(paths, folder))


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


def execute(x):

    create_folders(x)

    for paths, dirs, files in os.walk(x):
       for folder in dirs:
            if folder == 'Voice' or folder == 'voice:':
                current_folder = os.path.join(paths, folder)
                os.chdir(current_folder)
                rename_files_voice(current_folder)

            elif folder == 'Data' or folder == 'data':
                current_folder = os.path.join(paths, folder)
                os.chdir(current_folder)
                rename_files_data(current_folder)

    get_file_list(x)
    get_folder_list(x)
    match_files_folders(x)

# *****widgets*****

root.mainloop()
