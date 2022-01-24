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
        super().__init__(name="customer")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        self.first_name = tk.StringVar()
        self.surname = tk.StringVar()
        self.company = tk.StringVar()
        self.address = tk.StringVar()
        self.city = tk.StringVar()
        self.state = tk.StringVar()
        self.country = tk.StringVar()
        self.postal_code = tk.StringVar()
        self.phone= tk.StringVar()
        self.fax= tk.StringVar()
        self.email= tk.StringVar()
        self.support_rep_id= tk.IntVar()
        self.status = tk.BooleanVar()

        self.fields = (self.first_name,
                       self.surname,
                       self.company,
                       self.address,
                       self.city,
                       self.state,
                       self.country,
                       self.postal_code,
                       self.phone,
                       self.fax,
                       self.email,
                       self.support_rep_id,
                       self.status)

        self.val_int = self.master.engine.get_validate_integer(self)
        
        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        w = self.master.engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(w, text="First Name:",).grid(row=r, sticky=tk.W)
        self.FirstName = ttk.Entry(w, textvariable=self.first_name,)
        self.FirstName.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Surname:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.surname)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Company:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.company)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Address:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.address)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="City:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.city)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="State:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.state)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Country:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.country)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Postal Code:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.postal_code)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Phone:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.phone)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Fax:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.fax)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Email:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.email)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Rep id:").grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, justify=tk.CENTER, width=8, validate="key",
                      validatecommand=self.val_int, textvariable=self.support_rep_id)
        obj.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Status:").grid(row=r, sticky=tk.W)
        obj = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.status,)
        obj.grid(row=r, column=c, sticky=tk.W)

        self.master.engine.get_save_cancel(self, w)

    def on_open(self, selected_item=None):

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Edit {0}".format(self.winfo_name().capitalize())
            self.set_values()
        else:
            msg = "Add {0}".format(self.winfo_name().capitalize())
            self.status.set(1)

        self.title(msg)
        self.FirstName.focus()
        
    def set_values(self,):

        for p,i in enumerate(self.fields):
            i.set(self.selected_item[p+1])
            
    def get_values(self,):

        ret = []

        for i in self.fields:
            ret.append(i.get())

        return ret

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
                #force focus on listbox
                idx = list(self.parent.dict_items.keys())[list(self.parent.dict_items.values()).index(last_id)]
                self.parent.lstItems.selection_set(idx)
                self.parent.lstItems.see(idx)

            self.on_cancel()

        else:
            messagebox.showinfo(self.master.title(),
                                self.master.engine.abort,
                                parent=self)
     
    def on_cancel(self, evt=None):
        self.destroy()
