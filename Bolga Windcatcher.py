from pathlib import Path
import glob
import re
import os
import shutil
from tkinter import *
import pandas as pd
from typing import Optional, List
import folium as fl
import branca as bc
from tkinter import messagebox


root = Tk()
root.title('Bolga Windcatcher')

root.geometry('500x300')

topspace = Label(root, height='2')
topspace.grid()

label1 = Label(root, text='Logfiles Folder Path', fg='black', bg='grey')
logfiles_folder = Entry(root, width='50')
button1 = Button(root, text='Execute', fg='black', bg='gray', command=lambda: executeSorting(logfiles_folder.get()))
#button11 = Button(root, text='Quit', fg='black', bg='gray', command=root.destroy).pack(side=BOTTOM)
label1.grid(row=3, column=10)
logfiles_folder.grid(row=4, column=10, padx=120)
button1.grid(row=5, column=10)

middlespace=Label(root)
middlespace.grid(row=7, column=0)

label2 = Label(root, text='Map Folder Path', fg='black', bg='grey')
map_excel_folder = Entry(root, width='50')
button2 = Button(root, text='Generate', fg='black', bg='gray', command=lambda: Mapper(map_excel_folder.get()))
label2.grid(row=8, column=10, padx=90)
button2.grid(row=10, column=10)
map_excel_folder.grid(row=9, column=10)


def executeSorting(x):

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

    files = glob.glob(x + "/**/*.nmf", recursive=True)

    #check spelling of district folder
    for paths, dirs, f in os.walk(x):
        Districts = next(os.walk(x))[1]
    non_districts = []
    for d in Districts:
        if d not in districts_list:
            non_districts.append(d)
    if len(non_districts) > 0:
        #root = Tk()
        for r in non_districts:
            messagebox.showinfo("District Spelling", r + " is not a district, please check spelling!")
            #label = Label(root, text=str(r + ' ist not a district, please check spelling!'))
            #label.pack()
        #root.mainloop()
        exit()

    create_folders(x)

    #rename files
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


def Mapper(map_folderpath):

    def executeRSCP(excel):

        Excel_Path = Path(excel)
        excel_filename = Excel_Path.stem
        RSCP_panda = pd.read_excel(excel, sheet_name=1, index_col=0)

        RSCP_lats = list(RSCP_panda["Latitude"])
        RSCP_long = list(RSCP_panda["Longitude"])
        RSCP_list = list(RSCP_panda["RSCP"])
        RSCP_plot = zip(RSCP_lats, RSCP_long, RSCP_list)
        global Green_Count_RSCP
        global Yellow_Count_RSCP
        global Red_Count_RSCP
        global Black_Count_RSCP
        Green_Count_RSCP = []
        Yellow_Count_RSCP = []
        Red_Count_RSCP = []
        Black_Count_RSCP = []

        def add_categorical_legend(
                folium_map: fl.Map,
                title: str,
                colors: List[str],
                labels: List[str],
        ) -> fl.Map:
            """
            Given a Folium map, add to it a categorical legend with the given title, colors, and corresponding labels.
            The given colors and labels will be listed in the legend from top to bottom.
            Return the resulting map.

            Based on `this example <http://nbviewer.jupyter.org/gist/talbertc-usgs/18f8901fc98f109f2b71156cf3ac81cd>`_.
            """
            # Error check
            if len(colors) != len(labels):
                raise ValueError("colors and labels must have the same length.")

            color_by_label = zip(labels, colors, RSCPSamples, RSCPPercents)

            # Make legend HTML
            template = f"""
            {{% macro html(this, kwargs) %}}

            <!doctype html>
            <html lang="en">
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
            <div id='maplegend' class='maplegend'>
              <div class='legend-title'>{title}</div>
              <div class='legend-scale'>
                <ul class='legend-labels'>
            """

            for label, color, count, percent in color_by_label:
                template += f"<div class='clr' style='background:{color}'></div>"
                template += f"<span>{label}</span></span>{count}</span>{percent}"

            template += """
                </ul>
              </div>
            </div>

            </body>
            </html>

            <style type='text/css'>
              .maplegend {
                position: absolute;
                z-index:9999;
                background-color: rgba(255, 255, 255, 1);
                border-radius: 5px;
                border: 2px solid #bbb;
                padding: 10px;
                font-size:12px;
                right: 20px;
                top: 20px;
                width: 200px;
                opacity: 0.9;
              }
              .maplegend .legend-title {
                text-align: left;
                margin-bottom: 5px;
                font-weight: bold;
                font-size: 90%;
                }
              .maplegend .legend-scale ul {               #whole legend
                margin: 0;
                margin-bottom: 5px;
                padding: 0;
                float: left;
                list-style: none;
                }
              .maplegend .legend-scale ul li {             #descriptions 
                font-size: 80%;
                list-style: none;
                margin-left: 10;
                line-height: 18px;
                margin-bottom: 2px;
                width: auto;
                }
              .maplegend ul.legend-labels span {        #RSCP labels
                display: block;
                float: left;
                height: 16px;
                width: 90px;
                margin-right: 5px;
                margin-left: 0;
                border: 0px solid #ccc;
                }
               .maplegend .clr {        #colors
                display: block;
                float: left;
                height: 16px;
                width: 20px;
                margin-right: 5px;
                margin-left: 0;
                border: 0px solid #ccc;
                }
              .maplegend .legend-source {
                font-size: 80%;
                color: #777;
                clear: both;
                }
              .maplegend a {
                color: #777;
                }
            </style>
            {% endmacro %}
            """

            macro = bc.element.MacroElement()
            macro._template = bc.element.Template(template)
            folium_map.get_root().add_child(macro)

            return folium_map

        def legend(RSCP):
            if RSCP >= -85:
                Green_Count_RSCP.append(RSCP)
                return "green"
            elif RSCP < -85 and RSCP >= -95:
                Yellow_Count_RSCP.append(RSCP)
                return "yellow"
            elif RSCP < -95 and RSCP >= -105:
                Red_Count_RSCP.append(RSCP)
                return "red"
            elif RSCP < -105:
                Black_Count_RSCP.append(RSCP)
                return "black"

        my_map = fl.Map(location=[RSCP_lats[1], RSCP_long[1]], zoom_start=15)

        fg1 = fl.FeatureGroup(name="RSCP")
        for lat, long, RSCP in RSCP_plot:
            fg1.add_child(fl.Circle(location=[lat, long], popup=str(RSCP), radius=5, color=legend(RSCP)))
        my_map.add_child(fg1)

        RSCPSamples = ["(" + str(len(Green_Count_RSCP)) + ")", "(" + str(len(Yellow_Count_RSCP)) + ")",
                       "(" + str(len(Red_Count_RSCP)) + ")", "(" + str(len(Black_Count_RSCP)) + ")"]
        RSCPPercents = [str(round((len(Green_Count_RSCP) / len(RSCP_list)) * 100)) + "%",
                        str(round((len(Yellow_Count_RSCP) / len(RSCP_list)) * 100)) + "%",
                        str(round((len(Red_Count_RSCP) / len(RSCP_list)) * 100)) + "%",
                        str(round((len(Black_Count_RSCP) / len(RSCP_list)) * 100)) + "%"]

        colors = ['green', 'yellow', 'red', 'black']
        categories = ["0 to- 85", "-85 to -95", "-95 to -105", "-105 to -120"]
        # Add map legend
        my_map = add_categorical_legend(my_map, "UMTS Best Active RSCP (dBm)", colors=colors, labels=categories)
        # Add map title
        # my_map.get_root().html.add_child(fl.Element(f"<h1>Auckland Downtown SA1s</h1>"))
        fl.LayerControl(position="bottomright").add_to(my_map)
        my_map.save(excel_filename + ".html")

    def executeMOS(excel):

        Excel_Path = Path(excel)
        excel_filename = Excel_Path.stem
        MOS_panda = pd.read_excel(excel, sheet_name=1, index_col=0)
        lats_mos = list(MOS_panda["Latitude"])
        long_mos = list(MOS_panda["Longitude"])
        MOS_list = list(MOS_panda["MOS"])
        MOS_plot = zip(lats_mos, long_mos, MOS_list)
        global Green_Count_MOS
        global Blue_Count_MOS
        global Yellow_Count_MOS
        global Red_Count_MOS
        Green_Count_MOS = []
        Blue_Count_MOS = []
        Yellow_Count_MOS = []
        Red_Count_MOS = []

        def add_categorical_legend(
                folium_map: fl.Map,
                title: str,
                colors: List[str],
                labels: List[str],
        ) -> fl.Map:
            """
            Given a Folium map, add to it a categorical legend with the given title, colors, and corresponding labels.
            The given colors and labels will be listed in the legend from top to bottom.
            Return the resulting map.

            Based on `this example <http://nbviewer.jupyter.org/gist/talbertc-usgs/18f8901fc98f109f2b71156cf3ac81cd>`_.
            """
            # Error check
            if len(colors) != len(labels):
                raise ValueError("colors and labels must have the same length.")

            color_by_label = zip(labels, colors, MOSSamples, MOSPercents)

            # Make legend HTML
            template = f"""
            {{% macro html(this, kwargs) %}}

            <!doctype html>
            <html lang="en">
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
            <div id='maplegend' class='maplegend'>
              <div class='legend-title'>{title}</div>
              <div class='legend-scale'>
                <ul class='legend-labels'>
            """

            for label, color, count, percent in color_by_label:
                template += f"<div class='clr' style='background:{color}'></div>"
                template += f"<span>{label}</span></span>{count}</span>{percent}"

            template += """
                </ul>
              </div>
            </div>

            </body>
            </html>

            <style type='text/css'>
              .maplegend {
                position: absolute;
                z-index:9999;
                background-color: rgba(255, 255, 255, 1);
                border-radius: 5px;
                border: 2px solid #bbb;
                padding: 10px;
                font-size:12px;
                right: 20px;
                top: 20px;
                width: 200px;
                opacity: 0.9;
              }
              .maplegend .legend-title {
                text-align: left;
                margin-bottom: 5px;
                font-weight: bold;
                font-size: 90%;
                }
              .maplegend .legend-scale ul {               #whole legend
                margin: 0;
                margin-bottom: 5px;
                padding: 0;
                float: left;
                list-style: none;
                }
              .maplegend .legend-scale ul li {             #descriptions 
                font-size: 80%;
                list-style: none;
                margin-left: 10;
                line-height: 18px;
                margin-bottom: 2px;
                width: auto;
                }
              .maplegend ul.legend-labels span {        #RSCP labels
                display: block;
                float: left;
                height: 16px;
                width: 90px;
                margin-right: 5px;
                margin-left: 0;
                border: 0px solid #ccc;
                }
               .maplegend .clr {        #colors
                display: block;
                float: left;
                height: 16px;
                width: 20px;
                margin-right: 5px;
                margin-left: 0;
                border: 0px solid #ccc;
                }
              .maplegend .legend-source {
                font-size: 80%;
                color: #777;
                clear: both;
                }
              .maplegend a {
                color: #777;
                }
            </style>
            {% endmacro %}
            """

            macro = bc.element.MacroElement()
            macro._template = bc.element.Template(template)
            folium_map.get_root().add_child(macro)

            return folium_map

        def legendMOS(MOS):
            if MOS > 4.1:
                Green_Count_MOS.append(MOS)
                return "green"
            elif MOS < 4.1 and MOS > 3.5:
                Blue_Count_MOS.append(MOS)
                return "blue"
            elif MOS < 3.5 and MOS > 2.5:
                Yellow_Count_MOS.append(MOS)
                return "yellow"
            elif MOS < 2.5:
                Red_Count_MOS.append(MOS)
                return "red"

        my_map = fl.Map(location=[lats_mos[1], long_mos[1]], zoom_start=15)

        fg2 = fl.FeatureGroup(name="MOS")
        for lat, long, MOS in MOS_plot:
            fg2.add_child(fl.Circle(location=[lat, long], popup=str(MOS), radius=5, color=legendMOS(MOS)))
        my_map.add_child(fg2)

        MOSSamples = ["(" + str(len(Green_Count_MOS)) + ")", "(" + str(len(Blue_Count_MOS)) + ")",
                      "(" + str(len(Yellow_Count_MOS)) + ")", "(" + str(len(Red_Count_MOS)) + ")"]
        MOSPercents = [str(round((len(Green_Count_MOS) / len(MOS_list)) * 100)) + "%",
                       str(round((len(Blue_Count_MOS) / len(MOS_list)) * 100)) + "%",
                       str(round((len(Yellow_Count_MOS) / len(MOS_list)) * 100)) + "%",
                       str(round((len(Red_Count_MOS) / len(MOS_list)) * 100)) + "%"]

        colors = ['green', 'blue', 'yellow', 'red']
        categories = ["5 to 4.1", "4.1 to 3.5", "3.5 to 2.5", "2.5 to 0"]

        # Add map legend
        my_map = add_categorical_legend(my_map, "Speech Quality MOS", colors=colors, labels=categories)

        # my_map = add_categorical_legend(my_map, "UMTS Best Active RSCP (dBm)", colors=colors, labels=categories)
        # Add map title
        # my_map.get_root().html.add_child(fl.Element(f"<h1>Auckland Downtown SA1s</h1>"))
        fl.LayerControl(position="bottomright").add_to(my_map)
        my_map.save(excel_filename + ".html")

    def executeRSRP(excel):

        Excel_Path = Path(excel)
        excel_filename = Excel_Path.stem
        RSRP_panda = pd.read_excel(excel, sheet_name=1, index_col=0)

        RSRP_lats = list(RSRP_panda["Latitude"])
        RSRP_long = list(RSRP_panda["Longitude"])
        RSRP_list = list(RSRP_panda["RSRP"])
        RSRP_plot = zip(RSRP_lats, RSRP_long, RSRP_list)
        global Green_Count_RSRP
        global Yellow_Count_RSRP
        global Red_Count_RSRP
        global Black_Count_RSRP
        Green_Count_RSRP = []
        Yellow_Count_RSRP = []
        Red_Count_RSRP = []
        Black_Count_RSRP = []

        def add_categorical_legend(
                folium_map: fl.Map,
                title: str,
                colors: List[str],
                labels: List[str],
        ) -> fl.Map:
            """
            Given a Folium map, add to it a categorical legend with the given title, colors, and corresponding labels.
            The given colors and labels will be listed in the legend from top to bottom.
            Return the resulting map.

            Based on `this example <http://nbviewer.jupyter.org/gist/talbertc-usgs/18f8901fc98f109f2b71156cf3ac81cd>`_.
            """
            # Error check
            if len(colors) != len(labels):
                raise ValueError("colors and labels must have the same length.")

            color_by_label = zip(labels, colors, RSRPSamples, RSRPPercents)

            # Make legend HTML
            template = f"""
            {{% macro html(this, kwargs) %}}

            <!doctype html>
            <html lang="en">
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
            <div id='maplegend' class='maplegend'>
              <div class='legend-title'>{title}</div>
              <div class='legend-scale'>
                <ul class='legend-labels'>
            """

            for label, color, count, percent in color_by_label:
                template += f"<div class='clr' style='background:{color}'></div>"
                template += f"<span>{label}</span></span>{count}</span>{percent}"

            template += """
                </ul>
              </div>
            </div>

            </body>
            </html>

            <style type='text/css'>
              .maplegend {
                position: absolute;
                z-index:9999;
                background-color: rgba(255, 255, 255, 1);
                border-radius: 5px;
                border: 2px solid #bbb;
                padding: 10px;
                font-size:12px;
                right: 20px;
                top: 20px;
                width: 210px;
                opacity: 0.9;
              }
              .maplegend .legend-title {
                text-align: left;
                margin-bottom: 5px;
                font-weight: bold;
                font-size: 90%;
                }
              .maplegend .legend-scale ul {               #whole legend
                margin: 0;
                margin-bottom: 5px;
                padding: 0;
                float: left;
                list-style: none;
                }
              .maplegend .legend-scale ul li {             #descriptions 
                font-size: 80%;
                list-style: none;
                margin-left: 10;
                line-height: 18px;
                margin-bottom: 2px;
                width: auto;
                }
              .maplegend ul.legend-labels span {        #RSRP labels
                display: block;
                float: left;
                height: 16px;
                width: 90px;
                margin-right: 5px;
                margin-left: 0;
                border: 0px solid #ccc;
                }
               .maplegend .clr {        #colors
                display: block;
                float: left;
                height: 16px;
                width: 20px;
                margin-right: 5px;
                margin-left: 0;
                border: 0px solid #ccc;
                }
              .maplegend .legend-source {
                font-size: 80%;
                color: #777;
                clear: both;
                }
              .maplegend a {
                color: #777;
                }
            </style>
            {% endmacro %}
            """

            macro = bc.element.MacroElement()
            macro._template = bc.element.Template(template)
            folium_map.get_root().add_child(macro)

            return folium_map

        def legend(RSRP):
            if RSRP >= -90:
                Green_Count_RSRP.append(RSRP)
                return "green"
            elif RSRP < -90 and RSRP >= -105:
                Yellow_Count_RSRP.append(RSRP)
                return "yellow"
            elif RSRP < -105 and RSRP >= -120:
                Red_Count_RSRP.append(RSRP)
                return "red"
            elif RSRP < -120:
                Black_Count_RSRP.append(RSRP)
                return "black"



        fg1 = fl.FeatureGroup(name="RSRP")
        for lat, long, RSRP in RSRP_plot:
            fg1.add_child(fl.Circle(location=[lat, long], popup=str(RSRP), radius=5, color=legend(RSRP)))


        RSRPSamples = ["(" + str(len(Green_Count_RSRP)) + ")", "(" + str(len(Yellow_Count_RSRP)) + ")",
                       "(" + str(len(Red_Count_RSRP)) + ")", "(" + str(len(Black_Count_RSRP)) + ")"]
        RSRPPercents = [str(round((len(Green_Count_RSRP) / len(RSRP_list)) * 100)) + "%",
                        str(round((len(Yellow_Count_RSRP) / len(RSRP_list)) * 100)) + "%",
                        str(round((len(Red_Count_RSRP) / len(RSRP_list)) * 100)) + "%",
                        str(round((len(Black_Count_RSRP) / len(RSRP_list)) * 100)) + "%"]

        colors = ['green', 'yellow', 'red', 'black']
        categories = ["-20 to -90", "-90 to -105", "-105 to -120", "-120 to -150"]

        my_map = fl.Map(location=[RSRP_lats[1], RSRP_long[1]], zoom_start=15)
        my_map.add_child(fg1)

        # Add map legend
        my_map = add_categorical_legend(my_map, "LTE Dominant RSRP (dBm)", colors=colors, labels=categories)
        # Add map title
        # my_map.get_root().html.add_child(fl.Element(f"<h1>Auckland Downtown SA1s</h1>"))
        fl.LayerControl(position="bottomright").add_to(my_map)
        my_map.save(excel_filename + ".html")

    Map_Files = glob.glob(map_folderpath + "\*", recursive=True)

    for excel in Map_Files:
        Excel_Path = Path(excel)
        Excel_Path_Parts = Excel_Path.parts
        Excel_Path_Filename = Excel_Path.stem
        Excel_Path_Filename_Parts = Excel_Path_Filename.split(" ")

        if "RSCP" in iter(Excel_Path_Filename_Parts):
            executeRSCP(excel)
        elif "MOS" in Excel_Path_Filename_Parts:
            executeMOS(excel)
        elif "RSRP" in Excel_Path_Filename_Parts:
            executeRSRP(excel)

# *****widgets*****


root.mainloop()
