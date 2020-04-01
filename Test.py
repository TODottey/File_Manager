import os

x = 'C:\\Users\\NCA\\Desktop\\Logfiles(1) - Copy\\Asokwa\\Voice'

for file in os.listdir(x):
    file_name, file_ext = os.path.splitext(file)
    full_path = os.path.join(x).split('\\')[-1]+'_'+ os.path.join(x).split('\\')[-2]
    if file_name[-2:] == '.1':
        os.rename(file, full_path+' MTN MOC '+file)

