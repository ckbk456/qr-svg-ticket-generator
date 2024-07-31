import xml.dom
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import pandas as pd

class Mapping:
    object_pairings = []
    pairings = {}
    map = Tk()
    def pair(self):
        for item in self.object_pairings:
            if item["entry"].get() != '':
                self.pairings.update({item["entry"].get():item["heading"]['text']})
                # print(self.pairings)
        messagebox.showinfo(title='Mappings saved', message=f"{self.pairings}")

    def init(self,headings_list):
        Label(master=self.map, text="Keyword and column mapping", font=('courier', 12, "bold")).grid(column=0, columnspan=len(headings_list),row=0, padx=10)
        for item in headings_list:
            self.object_pairings.append(
                {
                    "id": headings_list.index(item),
                    "heading": Label(master=self.map, text=item, font=('courier', 12, "bold")),
                    "entry": Entry(master=self.map, width=20)
                }
            )
        # print(self.object_pairings)
        for item in self.object_pairings:
            item['heading'].grid(column=item['id'], row=1)
            item['entry'].grid(column=item['id'], row=2)
        # print(self.object_pairings)
        Button(master=self.map, text="save", command=self.pair).grid(column=0, columnspan=len(headings_list),row=3, padx=10)




