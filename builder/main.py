#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sqlite3
import json

from tkinter import Tk
from tkinter import messagebox
from tkinter import ttk

from create_sql import SqlCreator

def create_sql():
    with open ('model.json', "r") as f:
        model = json.loads(f.read())
    con_to = sqlite3.connect('base.db')
    cur_to = con_to.cursor()
    q = SqlCreator(model, cur_to)
    q.make_sql()
    messagebox.showinfo("Повідомлення", "Таблиці бази данних створено")
    con_to.close()


root = Tk()
ttk.Button(root, text="Create Tables", command=create_sql).pack(expand=True, fill='both')
root.mainloop()