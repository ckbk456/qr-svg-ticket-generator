import xml.dom
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import pandas as pd

class Mapping:
    def pair(self):
        for item in self.gui_pairings:
            if item["entry"].get() != '':
                self.pairings.update({item["entry"].get():item["heading"]['text']})
                self.pairings_message = self.pairings_message + f'{item["entry"].get()} -> {item["heading"]['text']} \n'
        i = messagebox.askokcancel(title='Mappings saved', message=f"Confirm pairings:\n {self.pairings_message}")
        if i:
            self.root.destroy()
        else:
            self.pairings = {}
            self.pairings_message = ""

    def __init__(self, headers_list):
        self.gui_pairings = []
        self.pairings = {}
        self.pairings_message = ""
        self.root = Tk()

        Label(master=self.root, text="Keyword and column mapping", font=('courier', 12, "bold")).grid(column=0, columnspan=len(headers_list), row=0, padx=10)
        for item in headers_list:
            self.gui_pairings.append(
                {
                    "id": headers_list.index(item),
                    "heading": Label(master=self.root, text=item, font=('courier', 12, "bold")),
                    "entry": Entry(master=self.root, width=20)
                }
            )

        for item in self.gui_pairings:
            item['heading'].grid(column=item['id'], row=1)
            item['entry'].grid(column=item['id'], row=2)

        Button(master=self.root, text="save", command=self.pair).grid(column=0, columnspan=len(headers_list), row=3, padx=10)




