import xml.dom
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
import pandas as pd
from mapping import Mapping
from bs4 import BeautifulSoup
from xml_modifier import overlay_modifier, get_qr_attributes, qr_modifier
from xml_merger import merge_svg
from handle_qrcode import generate_qr

global save_path
save_path = "/Users/ckbk/Desktop/untitled folder"
global template_path
template_path = "/Users/ckbk/Desktop/SVGTEMPLATE.svg"
global overlay_path
overlay_path = "/Users/ckbk/Desktop/overlay.svg"

def browseSave():
    global save_path
    save_path = askdirectory()
    if save_path:
        Label(master=app, text=save_path, font=('courier', 14)).grid(column=2, row=4, padx=20, pady=5)
    else:
        save_path = False
        messagebox.showerror(title='Error', message='Please select a folder to export')

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
    try:
        global csv_path
        global overlay_path
        global template_path
        global df
        global map

        if csv_path and overlay_path and template_path:
            with open(csv_path) as file:
                df = pd.read_csv(file)
        else:
            messagebox.showerror(title='Error', message='Please select all necessary files')
    except Exception as e:
        messagebox.showerror(title='Error', message=str(e))
    else:
        df_headers = df.columns.values.tolist()
        map = Mapping(headers_list=df_headers)


def generate_tickets():
    # try:
        global map
        global df
        global save_path
        replacements = map.pairings

        with open(overlay_path, "r") as f:
            overlay_str = f.read()
            print(overlay_str)
            modified_overlay_str = overlay_modifier(overlay_str)
            qr_attributes = get_qr_attributes(overlay_str)
        with open(template_path, "r") as f:
            template_str = f.read()

        with open("./modified_qr_test.svg", "r") as f:
            qr = f.read()

        for row in df.iterrows():
            overlay_str = modified_overlay_str
            # GENERATE QR CODE HERE
            qr_data = "".join(str(i) for i in row[1].to_list())
            og_qr = generate_qr(qr_data)

            qr = qr_modifier(og_qr, qr_attributes)

            for placeholder,replacement in replacements.items():
                overlay_str = overlay_str.replace(placeholder, row[1][replacement])

            output_str = merge_svg(overlay=overlay_str, template=template_str, qr=qr)
            with open(f"{save_path}/{row[0]}.svg", "w") as file:
                file.write(output_str)
    #
    # except AttributeError:
    #     messagebox.showerror(title='Error', message='Please assign pairings')
    # except Exception as e:
    #     messagebox.showerror(title='Error', message=str(e))


# GUI
app = Tk()
app.title('Ticket Generator')
app.configure(padx=20, pady=20)

Label(master=app, text="Ticket generator", font=('courier', 24, "bold")).grid(column=0, columnspan=3, row=0, pady=5)
Label(master=app, text="CSV path:", font=('courier', 14)).grid(column=0, row=1, padx=20, pady=5)
Label(master=app, text="Overlay SVG path:", font=('courier', 14)).grid(column=0, row=2, padx=20, pady=5)
Label(master=app, text="Template SVG path:", font=('courier', 14)).grid(column=0, row=3, padx=20, pady=5)
Button(app, text="Browse", command=browseCSV).grid(column=1, row=1, padx=20, pady=5)
Button(app, text="Browse", command=browseOverlay).grid(column=1, row=2, padx=20, pady=5)
Button(app, text="Browse", command=browseTemplate).grid(column=1, row=3, padx=20, pady=5)
Label(master=app, text="Export folder path:", font=('courier', 14)).grid(column=0, row=4, padx=20, pady=5)
Button(app, text="Browse", command=browseSave).grid(column=1, row=4, padx=20, pady=5)
Button(app, text="Upload", command=get_files).grid(column=0, columnspan=3, row=5, pady=5)
Button(app, text="Generate ticket", command=generate_tickets).grid(column=0, columnspan=3, row=6, pady=5)

app.mainloop()
