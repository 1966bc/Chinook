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

import frames.invoice as ui
import frames.items

DICT_OPTIONS = {0:"invoices.status =1 ",#paid
                1:"invoices.status =0 ",#no paid
                2:"invoices.status !=2",}#alll

class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="invoices")

        self.parent = parent
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(800, 400)        
        self.text_to_search = tk.StringVar()
        self.count = tk.StringVar()
        self.option_id = tk.IntVar()
        self.search_id = tk.IntVar()
        self.obj = None
        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        f0 = self.master.engine.get_frame(self, 8)
        f1 = self.master.engine.get_frame(f0, 2)
 
        ttk.Label(f1, anchor=tk.W, textvariable=self.count).pack(fill=tk.X, padx=2, pady=2)

        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Customer", "w", True, 100, 100],
                ["#2", "Date", "w", True, 100, 100],
                ["#3", "Country", "w", True, 80, 80],
                ["#4", "City", "w", True, 80, 80],
                ["#5", "Address", "w", True, 80, 80],
                ["#6", "Zip", "w", True, 80, 80],
                ["#7", "Total", "center", True, 80, 80],)

        self.lstItems = self.master.engine.get_tree(f1, cols,)
        self.lstItems.tag_configure("status", background="light gray")
        self.lstItems.tag_configure("odd", background="#EEFFD0")
        self.lstItems.tag_configure("even", background="#BFEAA3")
        self.lstItems.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-1>", self.on_item_activated)
   
        f2 = self.master.engine.get_label_frame(f0, "", 2)

        w = ttk.LabelFrame(f2, text="Search:")
        self.txSearch = ttk.Entry(w, width=8, textvariable=self.text_to_search)
        self.txSearch.bind("<Return>", self.on_search)
        self.txSearch.bind("<KP_Enter>", self.on_search)
        self.txSearch.pack(fill=tk.X, padx=2, pady=2)
        w.pack(fill=tk.X, padx=5,)
        
        bts = [("Reset", 0, self.on_reset, "<Alt-r>"),
               ("Add", 0, self.on_add, "<Alt-a>"),
               ("Edit", 0, self.on_edit, "<Alt-e>"),
               ("Items", 0, self.on_items, "<Alt-i>"),
               ("Close", 0, self.on_cancel, "<Alt-c>")]

        for btn in bts:
            self.master.engine.get_button(f2, btn[0], btn[1]).bind("<Button-1>", btn[2])
            self.bind(btn[3], btn[2])

        ops = ["Paid", "No paid", "All"]

        wdg = self.master.engine.get_radio_buttons(f2, "View by:",
                                            ops, self.option_id, self.on_reset)
        wdg.pack(side=tk.TOP, fill=tk.BOTH)

        ops = ["Customer", "Country", "City"]

        wdg = self.master.engine.get_radio_buttons(f2, "Search by:",
                                            ops, self.search_id, )
        wdg.pack(side=tk.TOP, fill=tk.BOTH)

        f2.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self,):

        self.title("Invoices")
        self.on_reset()

    def on_search(self, evt=None):

        search_type = self.search_id.get()

        s = self.text_to_search.get()+"%"

        if search_type == 0:

            fild = "customers.surname"
        
        elif search_type == 1:
            fild = "invoices.country"

        elif search_type == 2:
            fild = "invoices.city"
        
        sql = "SELECT invoices.invoice_id,\
                          customers.surname|| ' '||customers.first_name AS customer,\
                          strftime('%d-%m-%Y', invoices.invoice_date) AS invoice_date,\
                          invoices.country,\
                          invoices.city,\
                          invoices.address,\
                          invoices.postal_code,\
                          invoices.total,\
                          invoices.status\
                  FROM invoices\
                  INNER JOIN customers ON invoices.customer_id = customers.customer_id\
                  WHERE {0} LIKE ?\
                  ORDER BY invoices.country, customer ASC;".format(fild)

        args = (str(s.strip()),)
        rs = self.master.engine.read(True, sql, args)
        self.set_values(rs)

    def on_reset(self, evt=None):

        sql = "SELECT invoices.invoice_id,\
                      customers.surname|| ' '||customers.first_name AS customer,\
                      strftime('%d-%m-%Y', invoices.invoice_date) AS invoice_date,\
                      invoices.country,\
                      invoices.city,\
                      invoices.address,\
                      invoices.postal_code,\
                      invoices.total,\
                      invoices.status\
              FROM invoices\
              INNER JOIN customers ON invoices.customer_id = customers.customer_id\
              WHERE {0} ORDER BY invoices.country, customer ASC;".format(DICT_OPTIONS[self.option_id.get()])

        rs = self.master.engine.read(True, sql, ())

        self.set_values(rs)

    def set_values(self, rs):

        count = 1
        
        for i in self.lstItems.get_children():
            self.lstItems.delete(i)

        if rs:
            for i in rs:
                if i[8] != 1:
                    tag_config = ("status",)
                elif count % 2 == 0:
                    tag_config = ("odd",)
                else:
                    tag_config = ("even",)            

                self.lstItems.insert("", tk.END, iid=i[0], text=i[0],
                                     values=(i[1], i[2], i[3], i[4], i[5], i[6], i[7],),
                                     tags = tag_config)
                count += 1

        s = "{0} {1}".format("Invoices", len(self.lstItems.get_children()))

        self.count.set(s)

    def on_item_selected(self, evt):

        if self.lstItems.focus():
            self.item_iid = self.lstItems.selection()
            pk = int(self.item_iid[0])
            self.selected_item = self.master.engine.get_selected("invoices", "invoice_id", pk)
            
    def on_item_activated(self, evt=None):

        if self.lstItems.focus():
            self.item_iid = self.lstItems.selection()
            self.obj = ui.UI(self, self.item_iid)
            self.obj.on_open(self.selected_item)

        else:
            messagebox.showwarning(self.master.title(), self.master.engine.no_selected, parent=self)

    def on_items(self, evt=None):

        if self.lstItems.focus():
            self.obj = frames.items.UI(self,)
            self.obj.on_open(self.item_iid, self.selected_item)
        else:
            messagebox.showwarning(self.master.title(), self.master.engine.no_selected, parent=self)

    def on_add(self, evt=None):
        self.obj = ui.UI(self)
        self.obj.on_open()

    def on_edit(self, evt=None):
        self.on_item_activated()            

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
