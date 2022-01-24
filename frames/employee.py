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
from calendarium import Calendarium

class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="employee")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        self.surname = tk.StringVar()
        self.first_name = tk.StringVar()
        self.qualification = tk.StringVar()
        self.reports_to = tk.IntVar()
        self.address = tk.StringVar()
        self.city = tk.StringVar()
        self.state = tk.StringVar()
        self.country = tk.StringVar()
        self.postal_code = tk.StringVar()
        self.phone= tk.StringVar()
        self.fax= tk.StringVar()
        self.email= tk.StringVar()
        self.status = tk.BooleanVar()

        self.val_int = self.master.engine.get_validate_integer(self)
        
        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        w = self.master.engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(w, text="Surname:",).grid(row=r, sticky=tk.W)
        self.Surname = ttk.Entry(w, textvariable=self.surname,)
        self.Surname.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="First Name:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.first_name)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Qualification:",).grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, textvariable=self.qualification)
        obj.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Report to:").grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, justify=tk.CENTER, width=8, validate="key",
                      validatecommand=self.val_int, textvariable=self.reports_to)
        obj.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Dob:").grid(row=r, sticky=tk.N+tk.W)
        self.dob = Calendarium(self,)
        self.dob.get_calendarium(w, r, c)

        r += 1
        ttk.Label(w, text="Hire:").grid(row=r, sticky=tk.N+tk.W)
        self.hire_date = Calendarium(self,)
        self.hire_date.get_calendarium(w, r, c)

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
            self.dob.set_today()
            self.hire_date.set_today()
            self.status.set(1)

        self.title(msg)
        self.Surname.focus()
        
    def set_values(self,):

        self.surname.set(self.selected_item[1])
        self.first_name.set(self.selected_item[2])
        self.qualification.set(self.selected_item[3])
        self.reports_to.set(self.selected_item[4])

        self.dob.day.set(int(self.selected_item[5][8:10]))
        self.dob.month.set(int(self.selected_item[5][5:7]))
        self.dob.year.set(int(self.selected_item[5][0:4]))

        self.hire_date.day.set(int(self.selected_item[6][8:10]))
        self.hire_date.month.set(int(self.selected_item[6][5:7]))
        self.hire_date.year.set(int(self.selected_item[6][0:4]))
        
        self.address.set(self.selected_item[7])
        self.city.set(self.selected_item[8])
        self.state.set(self.selected_item[9])
        self.country.set(self.selected_item[10])
        self.postal_code.set(self.selected_item[11])
        self.phone.set(self.selected_item[12])
        self.fax.set(self.selected_item[13])
        self.email.set(self.selected_item[14])
        self.status.set(self.selected_item[15])
              
    def get_values(self,):

        return [self.surname.get(),
                self.first_name.get(),
                self.qualification.get(),
                self.reports_to.get(),
                self.dob.get_date(self),
                self.hire_date.get_date(self),
                self.address.get(),
                self.city.get(),
                self.state.get(),
                self.country.get(),
                self.postal_code.get(),
                self.phone.get(),
                self.fax.get(),
                self.email.get(),
                self.status.get(),]
        
    def on_save(self, evt=None):

        if self.dob.get_date(self) == False: return
        if self.hire_date.get_date(self) == False: return

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
