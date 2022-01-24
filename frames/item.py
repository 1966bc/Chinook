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
        super().__init__(name="item")

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        self.unit_price = tk.DoubleVar()
        self.quantity = tk.IntVar()
        self.status = tk.BooleanVar()

        self.val_float = self.master.engine.get_validate_float(self)
        self.val_int = self.master.engine.get_validate_integer(self)

        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        w = self.master.engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(w, text="Tracks:",).grid(row=r, sticky=tk.W)
        self.cbTracks = ttk.Combobox(w,)
        self.cbTracks.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Unit Price:").grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, justify=tk.CENTER, width=8, validate="key",
                      validatecommand=self.val_float, textvariable=self.unit_price)
        obj.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Quantity:").grid(row=r, sticky=tk.W)
        obj = ttk.Entry(w, justify=tk.CENTER, width=8, validate="key",
                      validatecommand=self.val_int, textvariable=self.quantity)
        obj.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Status:").grid(row=r, sticky=tk.W)
        obj = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.status,)
        obj.grid(row=r, column=c, sticky=tk.W)

        self.master.engine.get_save_cancel(self, w)

    def on_open(self, item_iid,selected_invoice, selected_item=None):

        self.item_iid = item_iid
        self.selected_invoice = selected_invoice

        self.set_tracks()

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Edit {0}".format(self.winfo_name().capitalize())
            self.set_values()
        else:
            msg = "Add {0}".format(self.winfo_name().capitalize())
            self.status.set(1)

        self.title(msg)

    def set_tracks(self, evt=None):

        sql = "SELECT track_id, track_name FROM tracks WHERE status =1 ORDER BY track_name ASC;"
        index = 0
        self.dict_tracks = {}
        values = []
        rs = self.master.engine.read(True, sql, ())

        if rs:
            for i in rs:
                self.dict_tracks[index] = i[0]
                index += 1
                values.append(i[1])

        self.cbTracks["values"] = values

    def set_values(self,):

        key = next(key
                   for key, value
                   in self.dict_tracks.items()
                   if value == self.selected_item[2])
        self.cbTracks.current(key)

        self.unit_price.set(self.selected_item[3])
        self.quantity.set(self.selected_item[4])
        self.status.set(self.selected_item[5])

    def get_values(self,):

        return [self.selected_invoice[0],
                self.dict_tracks[self.cbTracks.current()],
                self.unit_price.get(),
                self.quantity.get(),
                self.status.get(),]


    def on_save(self, evt=None):

        if self.master.engine.on_fields_control(self) == False: return

        if messagebox.askyesno(self.master.title(),
                               self.master.engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.master.engine.get_update_sql("invoice_items", "invoice_line_id")

                args.append(self.selected_item[0])

            else:

                sql = self.master.engine.get_insert_sql("invoice_items", len(args))

            last_id = self.master.engine.write(sql, args)

            self.master.engine.set_total(self.selected_invoice)

            #update total on database and ivoices gui....;)
            self.master.nametowidget("invoices").on_reset()
            self.master.nametowidget("invoices").lstItems.selection_set(self.item_iid)
            self.master.nametowidget("invoices").lstItems.see(self.item_iid)

            self.parent.on_open(self.item_iid, self.selected_invoice)

            if self.index is not None:
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
