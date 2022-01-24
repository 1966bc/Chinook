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

import frames.item as ui

SQL = "SELECT invoice_items.invoice_line_id,\
              tracks.track_name AS track,\
              invoice_items.unit_price,\
              invoice_items.quantity,\
              invoice_items.status\
       FROM invoice_items\
       INNER JOIN tracks ON invoice_items.track_id = tracks.track_id\
       WHERE invoice_items.invoice_id = ?;"


class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="items")

        self.parent = parent
        self.attributes("-topmost", True)
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(600, 400)        
        self.count = tk.StringVar()
        self.obj = None
        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        f0 = self.master.engine.get_frame(self, 8)
        f1 = self.master.engine.get_frame(f0, 2)

        ttk.Label(f1, anchor=tk.W, textvariable=self.count).pack(fill=tk.X, padx=2, pady=2)

        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Track", "w", True, 100, 100],
                ["#2", "Unit Price", "center", True, 50, 50],
                ["#3", "Quantity", "center", True, 50, 50],)

        self.lstItems = self.master.engine.get_tree(f1, cols,)
        self.lstItems.tag_configure("status", background="light gray")
        self.lstItems.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-1>", self.on_item_activated)
   
        f2 = self.master.engine.get_label_frame(f0, "", 2)
        
        bts = [("Add", 0, self.on_add, "<Alt-a>"),
               ("Edit", 0, self.on_edit, "<Alt-e>"),
               ("Close", 0, self.on_cancel, "<Alt-c>")]

        for btn in bts:
            self.master.engine.get_button(f2, btn[0], btn[1]).bind("<Button-1>", btn[2])
            self.bind(btn[3], btn[2])

        f2.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        f0.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self, item_iid, selected_invoice):

        self.item_iid = item_iid
        self.selected_invoice = selected_invoice

        self.title("Invoice Items")

        rs = self.master.engine.read(True, SQL, (selected_invoice[0],))

        self.set_values(rs)

    def set_values(self, rs):

        count = 1
        
        for i in self.lstItems.get_children():
            self.lstItems.delete(i)

        if rs:
            for i in rs:
                if i[4] != 1:
                    tag_config = ("status",)
                else:
                    tag_config = ("",)
                          

                self.lstItems.insert("", tk.END, iid=i[0], text=i[0],
                                     values=(i[1], i[2], i[3],),
                                     tags = tag_config)
                count += 1

        s = "{0} {1}".format("Invoice Items", len(self.lstItems.get_children()))

        self.count.set(s)

    def on_item_selected(self, evt):

        if self.lstItems.focus():
            item_iid = self.lstItems.selection()
            pk = int(item_iid[0])
            self.selected_item = self.master.engine.get_selected("invoice_items", "invoice_line_id", pk)
            
    def on_item_activated(self, evt=None):

        if self.lstItems.focus():
            item_iid = self.lstItems.selection()
            self.obj = ui.UI(self, item_iid)
            self.obj.on_open(self.item_iid, self.selected_invoice, self.selected_item,)

        else:
            messagebox.showwarning(self.master.title(), self.master.engine.no_selected, parent=self)


    def on_add(self, evt=None):
        self.obj = ui.UI(self)
        self.obj.on_open(self.item_iid, self.selected_invoice)

    def on_edit(self, evt=None):
        self.on_item_activated()

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
