import os
import shutil
from tkinter import *


root = Tk()
frame = Frame(root)
frame.pack(padx=100, pady=50)

label1 = Label(frame, text='Logfiles Folder Path', fg='black', bg='grey')
logfiles_folder = Entry(frame)
button1 = Button(frame, text='Execute', fg='black', bg='gray', command=lambda: execute(logfiles_folder.get()))  #runs execute fuction


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
    global mtn_folder
    mtn_folder = x.split('\\')[-1] + ' MTN'
    global voda_folder
    voda_folder = x.split('\\')[-1] + ' VODA'
    global at_folder
    at_folder = x.split('\\')[-1] + ' AT'
    global glo_folder
    glo_folder = x.split('\\')[-1] + ' GLO'

    try:
        os.makedirs(mtn_folder, exist_ok=False)
        os.makedirs(voda_folder, exist_ok=False)
        os.makedirs(at_folder, exist_ok=False)
        os.makedirs(glo_folder, exist_ok=False)

    except FileExistsError:
        return


def rename_files_voice(x):

    for f in os.listdir(x):
        file_name, file_ext = os.path.splitext(f)
        if file_name[-2:] == '.1':
            os.rename(f, 'MTN MOC '+f)
        elif file_name[-2:] == '.2':
            os.rename(f, 'VODA MOC '+f)
        elif file_name[-2:] == '.3':
            os.rename(f, 'AT MOC '+f)
        elif file_name[-2:] == '.4':
            os.rename(f, 'GLO MOC '+f)
        elif file_name[-2:] == '.5':
            os.rename(f, 'MTN MTC '+f)
        elif file_name[-2:] == '.6':
            os.rename(f, 'VODA MTC '+f)
        elif file_name[-2:] == '.7':
            os.rename(f, 'AT MTC '+f)
        elif file_name[-2:] == '.8':
            os.rename(f, 'GLO MTC '+f)
        elif file_name[-2:] == '.9':
            os.rename(f, 'MTN 3G '+f)
        elif file_name[-2:] == '10':
            os.rename(f, 'VODA 3G '+f)
        elif file_name[-2:] == '11':
            os.rename(f, 'AT 3G '+f)
        elif file_name[-2:] == '12':
            os.rename(f, 'GLO 3G ' + f)
        elif file_name[-2:] == '13':
            os.rename(f, 'MTN 4G ' + f)


def rename_files_data(x):
    for f in os.listdir(x):
        file_name, file_ext = os.path.splitext(f)
        if file_name[-2:] == '.1':
            os.rename(f, 'MTN Data '+f)
        elif file_name[-2:] == '.2':
            os.rename(f, 'VODA Data '+f)
        elif file_name[-2:] == '.3':
            os.rename(f, 'AT Data '+f)
        elif file_name[-2:] == '.4':
            os.rename(f, 'GLO Data '+f)
        elif file_name[-2:] == '.5':
            os.rename(f, '4G Data ' + f)


def move_files(x):

    for f in os.listdir(x):
        if f.startswith('MTN'):
            shutil.move(os.path.abspath(f), os.path.abspath(mtn_folder))
        elif f.startswith('VODA'):
            shutil.move(os.path.abspath(f), os.path.abspath(voda_folder))
        elif f.startswith('AT'):
            shutil.move(os.path.abspath(f), os.path.abspath(at_folder))
        elif f.startswith('GLO'):
            shutil.move(os.path.abspath(f), os.path.abspath(glo_folder))


# logfiles_folder = 'C:\\Users\\NCA\\Desktop\\Logfiles'  # input(str('Enter Logfiles Folder Address: '))


def execute(x):

    for paths, dirs, files in os.walk(x):
       for folder in dirs:
            if folder == 'Voice' or folder == 'voice:':
                current_folder = os.path.join(paths, folder)
                os.chdir(current_folder)
                rename_files_voice(current_folder)
                create_folders(current_folder)
                move_files(current_folder)

            elif folder == 'Data' or folder == 'data':
                current_folder = os.path.join(paths, folder)
                os.chdir(current_folder)
                rename_files_voice(current_folder)
                create_folders(current_folder)
                move_files(current_folder)


# *****widgets*****

root.mainloop()