import xml.dom
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import pandas as pd
from mapping import Mapping
from bs4 import BeautifulSoup

global template_path
template_path = "/Users/ckbk/Desktop/SVGTEMPLATE.svg"
global overlay_path
overlay_path = "/Users/ckbk/Desktop/TESTSVG.svg"


def browseCSV():
    global csv_path
    csv_path = askopenfilename()
    if csv_path.lower().endswith('.csv'):
        Label(master=app, text=csv_path, font=('courier', 14)).grid(column=2, row=1, padx=20, pady=5)

    else:
        csv_path = False
        messagebox.showerror(title='Error', message='Please select a CSV file')


def browseOverlay():
    global overlay_path
    overlay_path = askopenfilename()
    if overlay_path.lower().endswith(".svg"):
        Label(master=app, text=overlay_path, font=('courier', 14)).grid(column=2, row=2, padx=20, pady=5)
    else:
        overlay_path = False
        messagebox.showerror(title='Error', message='Please select a SVG file')


def browseTemplate():
    global template_path
    template_path = askopenfilename()
    if template_path.lower().endswith(".svg"):
        Label(master=app, text=template_path, font=('courier', 14)).grid(column=2, row=3, padx=20, pady=5)

    else:
        template_path = False
        messagebox.showerror(title='Error', message='Please select a SVG file')


def get_files():
    global csv_path
    global overlay_path
    global template_path
    global df
    global overlay_xml
    global template_xml
    if csv_path and overlay_path and template_path:
        print(csv_path, overlay_path, template_path)

        with open(csv_path) as file:
            global df
            df = pd.read_csv(file)

        with open(overlay_path, "rb") as file:
            global overlay_xml
            overlay_xml = file.read()

        with open(template_path, "rb") as file:
            global template_xml
            template_xml = file.read()
    else:
        messagebox.showerror(title='Error', message='Please select all necessary files')

    df_headers = df.columns.values.tolist()
    # print(overlay_xml)
    # print(template_xml)

    global map
    map = Mapping()
    Mapping.init(self=map, headings_list=df_headers)

def generate_tickets():
    global map
    global df
    replacements = map.pairings
    global overlay_xml
    overlay_decoded = overlay_xml.decode('utf-8')
    global template_xml

    # print(type(overlay_xml), overlay_xml, replacements)
    for row in df.iterrows():
        for placeholder,replacement in replacements.items():
            new_str = overlay_decoded.replace(placeholder,row[1][replacement])
        with open(f"{row}test.svg", "w") as file:
            file.write(new_str)




# GUI
app = Tk()

Label(master=app, text="Ticker generator", font=('courier', 24, "bold")).grid(column=0, columnspan=3, row=0, padx=20, pady=20)
Label(master=app, text="CSV path:", font=('courier', 14)).grid(column=0, row=1, padx=20, pady=5)
Label(master=app, text="Overlay SVG path:", font=('courier', 14)).grid(column=0, row=2, padx=20, pady=5)
Label(master=app, text="Template SVG path:", font=('courier', 14)).grid(column=0, row=3, padx=20, pady=5)
Button(app, text="Browse", command=browseCSV).grid(column=1, row=1, padx=20, pady=5)
Button(app, text="Browse", command=browseOverlay).grid(column=1, row=2, padx=20, pady=5)
Button(app, text="Browse", command=browseTemplate).grid(column=1, row=3, padx=20, pady=5)
Button(app, text="Upload", command=get_files).grid(column=1, row=4)
Button(app, text="Generate ticket", command=generate_tickets).grid(column=1, row=5)

app.mainloop()
