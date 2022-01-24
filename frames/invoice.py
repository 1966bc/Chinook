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
        super().__init__(name="invoice")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
    
        self.address = tk.StringVar()
        self.city = tk.StringVar()
        self.state = tk.StringVar()
        self.country = tk.StringVar()
        self.postal_code = tk.StringVar()
        self.total = tk.DoubleVar()
        self.status = tk.BooleanVar()

        self.val_float = self.master.engine.get_validate_float(self)
        
        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        w = self.master.engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(w, text="Customers:",).grid(row=r, sticky=tk.W)
        self.cbCustomers = ttk.Combobox(w,)
        self.cbCustomers.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Invoice Date:").grid(row=r, sticky=tk.N+tk.W)
        self.invoice_date = Calendarium(self,)
        self.invoice_date.get_calendarium(w, r, c)

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
        ttk.Label(w, text="Total:").grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, justify=tk.CENTER, width=8, textvariable=self.total)
        obj.configure(state='disabled')
        obj.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Status:").grid(row=r, sticky=tk.W)
        obj = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.status,)
        obj.grid(row=r, column=c, sticky=tk.W)

        self.master.engine.get_save_cancel(self, w)

    def on_open(self, selected_item=None):

        self.set_customers()

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Edit {0}".format(self.winfo_name().capitalize())
            self.set_values()
        else:
            msg = "Add {0}".format(self.winfo_name().capitalize())
            self.invoice_date.set_today()
            self.status.set(1)

        self.title(msg)
        self.invoice_date.focus()

    def set_customers(self, evt=None):

        sql = "SELECT customer_id, surname|| ' ' ||first_name\
               FROM customers\
               WHERE status =1\
               ORDER BY surname ASC;"
        
        index = 0
        self.dict_customers = {}
        values = []
        rs = self.master.engine.read(True, sql, ())

        if rs:
            for i in rs:
                self.dict_customers[index] = i[0]
                index += 1
                values.append(i[1])

        self.cbCustomers["values"] = values
        
    def set_values(self,):

        key = next(key
                   for key, value
                   in self.dict_customers.items()
                   if value == self.selected_item[1])
        self.cbCustomers.current(key)

        
        self.invoice_date.day.set(int(self.selected_item[2][8:10]))
        self.invoice_date.month.set(int(self.selected_item[2][5:7]))
        self.invoice_date.year.set(int(self.selected_item[2][0:4]))

        self.address.set(self.selected_item[3])
        self.city.set(self.selected_item[4])
        self.state.set(self.selected_item[5])
        self.country.set(self.selected_item[6])
        self.postal_code.set(self.selected_item[7])
        self.total.set(self.selected_item[8])
        self.status.set(self.selected_item[9])

    def get_values(self,):

        return [self.dict_customers[self.cbCustomers.current()],
                self.invoice_date.get_date(self),
                self.address.get(),
                self.city.get(),
                self.state.get(),
                self.country.get(),
                self.postal_code.get(),
                self.total.get(),
                self.status.get(),]

        
    def on_save(self, evt=None):

        if self.invoice_date.get_date(self) == False: return
        
        if self.master.engine.on_fields_control(self) == False: return

        if messagebox.askyesno(self.master.title(), 
                               self.master.engine.ask_to_save, 
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.master.engine.get_update_sql("invoices", "invoice_id")

                args.append(self.selected_item[0])

            else:

                sql = self.master.engine.get_insert_sql("invoices", len(args))

            last_id = self.master.engine.write(sql, args)
            self.parent.on_open()

            if self.index is not None:
                if self.selected_item[9] == self.status.get():
                    self.parent.lstItems.selection_set(self.index)
                    self.parent.lstItems.see(self.index)
                else:
                    self.parent.lstItems.selection_set(last_id)
                    self.parent.lstItems.see(last_id)

            self.on_cancel()

        else:
            messagebox.showinfo(self.master.title(),
                                self.master.engine.abort,
                                parent=self)
     
    def on_cancel(self, evt=None):
        self.destroy()
