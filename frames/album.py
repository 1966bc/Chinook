# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# project:  chinook
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="album")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        self.description = tk.StringVar()
        self.status = tk.BooleanVar()
        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        w = self.master.engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(w, text="Description:",).grid(row=r, sticky=tk.W)
        self.txTitle = ttk.Entry(w, textvariable=self.description)
        self.txTitle.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Artists:",).grid(row=r, sticky=tk.W)
        self.cbArtists = ttk.Combobox(w,)
        self.cbArtists.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Status:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.status,)
        chk.grid(row=r, column=c, sticky=tk.W)

        self.master.engine.get_save_cancel(self, w)

    def on_open(self, selected_item=None):

        self.set_artists()

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Edit {0}".format(self.winfo_name().capitalize())
            self.set_values()
        else:
            msg = "Add {0}".format(self.winfo_name().capitalize())
            self.status.set(1)

        self.title(msg)
        self.txTitle.focus()

    def set_values(self,):

        key = next(key
                   for key, value
                   in self.dict_artists.items()
                   if value == self.selected_item[1])
        self.cbArtists.current(key)

        self.description.set(self.selected_item[2])
        
        self.status.set(self.selected_item[3])

    def get_values(self,):

        return [self.dict_artists[self.cbArtists.current()],
                self.description.get(),
                self.status.get()]

    def on_save(self, evt=None):

        if self.master.engine.on_fields_control(self) == False: return

        if messagebox.askyesno(self.master.title(), 
                               self.master.engine.ask_to_save, 
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.master.engine.get_update_sql(self.parent.table, self.parent.primary_key)

                args.append(self.selected_item[0])

            else:

                sql = self.master.engine.get_insert_sql(self.parent.table, len(args))

            last_id = self.master.engine.write(sql, args)
            self.parent.on_open()

            if self.index is not None:
                self.parent.lstItems.see(self.index)
                self.parent.lstItems.selection_set(self.index)
            else:
                #force focus on listbox using dict
                idx = list(self.parent.dict_items.keys())[list(self.parent.dict_items.values()).index(last_id)]
                self.parent.lstItems.selection_set(idx)
                self.parent.lstItems.see(idx)

            self.on_cancel()

        else:
            messagebox.showinfo(self.master.title(),
                                self.master.engine.abort,
                                parent=self)

    def set_artists(self, evt=None):

        index = 0
        self.dict_artists = {}
        values = []
        sql = "SELECT * FROM artists WHERE status =1 ORDER BY description ASC;"
        rs = self.master.engine.read(True, sql, ())

        if rs:
            for i in rs:
                self.dict_artists[index] = i[0]
                index += 1
                values.append(i[1])

        self.cbArtists["values"] = values
        
    def on_cancel(self, evt=None):
        self.destroy()
