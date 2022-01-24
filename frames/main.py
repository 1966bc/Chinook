# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  chinook
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
# -----------------------------------------------------------------------------
""" This is the main module of The Chinook Sample Database GUI."""
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import frames.license
import frames.track
import frames.albums
import frames.artists
import frames.customers
import frames.employees
import frames.genres
import frames.invoices
import frames.media_types
import frames.playlists

from engine import Engine

__author__ = "1966bc"
__copyright__ = "Copyleft"
__credits__ = ["hal9000", ]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "1.0"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "hiems MMXXI"
__status__ = "beta"
__icon__ = "https://icon-library.com/icon/database-icon-0.html.html>Database Icon # 95886"


class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.status_bar_text = tk.StringVar()
        self.init_menu()
        self.init_toolbar()
        self.init_status_bar()
        self.init_ui()
        self.center_ui()

    def init_menu(self):

        m_main = tk.Menu(self, bd=1)

        m_file = tk.Menu(m_main, tearoff=0, bd=1)
        m_tools = tk.Menu(m_main, tearoff=0, bd=1)
        s_databases = tk.Menu(m_tools)
        m_about = tk.Menu(m_main, tearoff=0, bd=1)

        items = (("File", m_file),
                 ("Tools", m_tools),
                 ("?", m_about),)

        for i in items:
            m_main.add_cascade(label=i[0], underline=0, menu=i[1])

        m_file.add_cascade(label="Database", menu=s_databases, underline=0)

        items = (("Dump", self.on_dump),
                 ("Vacuum", self.on_vacuum),)

        for i in items:
            s_databases.add_command(label=i[0], underline=0, command=i[1])

        m_file.add_command(label="Log", underline=1, command=self.on_log)

        m_file.add_separator()

        m_file.add_command(label="Exit", underline=0, command=self.parent.on_exit)


        m_tools.add_command(label="Albums", underline=0, command=lambda: self.on_opening_toplevel(frames.albums))
        m_tools.add_command(label="Artists", underline=1, command=lambda: self.on_opening_toplevel(frames.artists))
        m_tools.add_command(label="Customers", underline=0, command=lambda: self.on_opening_toplevel(frames.customers))
        m_tools.add_command(label="Employees", underline=0, command=lambda: self.on_opening_toplevel(frames.employees))
        m_tools.add_command(label="Genres", underline=0, command=lambda: self.on_opening_toplevel(frames.genres))
        m_tools.add_command(label="Invoices", underline=0, command=lambda: self.on_opening_toplevel(frames.invoices))
        m_tools.add_command(label="Media Types", underline=0, command=lambda: self.on_opening_toplevel(frames.media_types))
        m_tools.add_command(label="Playlists", underline=0, command=lambda: self.on_opening_toplevel(frames.playlists))

        items = (("About", self.on_about),
                 ("License", self.on_license),
                 ("Python", self.on_python_version),
                 ("Tkinter", self.on_tkinter_version),)

        for i in items:
            m_about.add_command(label=i[0], underline=0, command=i[1])

        for i in (m_main, m_file, ):
            i.config(bg=self.master.engine.get_rgb(240, 240, 237),)
            i.config(fg="black")

        self.master.config(menu=m_main)

    def init_toolbar(self):

        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)

        img_exit = tk.PhotoImage(data=self.master.engine.get_icon("exit"))
        img_info = tk.PhotoImage(data=self.master.engine.get_icon("info"))

        exitButton = tk.Button(toolbar, width=20, image=img_exit,
                               relief=tk.FLAT, command=self.parent.on_exit)
        infoButton = tk.Button(toolbar, width=20, image=img_info,
                               relief=tk.FLAT, command=self.on_about)

        exitButton.image = img_exit
        infoButton.image = img_info

        exitButton.pack(side=tk.LEFT, padx=2, pady=2)
        infoButton.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.config(bg=self.master.engine.get_rgb(240, 240, 237))
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def init_status_bar(self):

        self.status = tk.Label(self,
                               textvariable=self.status_bar_text,
                               bd=1,
                               fg=self.master.engine.get_rgb(0, 0, 0),
                               bg=self.master.engine.get_rgb(240, 240, 237),
                               relief=tk.SUNKEN,
                               anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def init_ui(self):
        """create widgets"""

        self.pack(fill=tk.BOTH, expand=1)

        f0 = self.master.engine.get_frame(self, 8)

        f1 = ttk.Frame(f0,)
        # artists
        cols = (["#0", "", "w", False, 200, 200],
                ["#1", "", "w", True, 0, 0],)
        self.Artists = self.master.engine.get_tree(f1, cols, show="tree")
        self.Artists.show = "tree"
        self.Artists.pack(fill=tk.BOTH, padx=2, pady=2)
        self.Artists.bind("<<TreeviewSelect>>", self.on_artist_selected)
        self.Artists.bind("<Double-1>", self.on_artist_activated)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=0)

        f2 = ttk.Frame(f0,)
        #tracks
        #-----------------------------------------------------------------------
        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Album", "w", True, 100, 100],
                ["#2", "Composer", "w", True, 100, 100],
                ["#3", "Milliseconds", "center", True, 20, 20],
                ["#4", "Price", "center", True, 20, 20],)

        self.lblTracks = ttk.LabelFrame(f2, text="Tracks",)
        self.lstTracks = self.master.engine.get_tree(self.lblTracks, cols,)
        self.lstTracks.bind("<<TreeviewSelect>>", self.on_track_selected)
        self.lstTracks.bind("<Double-1>", self.on_track_activated)
        self.lblTracks.pack(fill=tk.BOTH, expand=1)

        f2.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

        #buttons
        #-----------------------------------------------------------------------
        w = tk.LabelFrame(self, relief=tk.GROOVE, bd=1, padx=5, pady=5,)

        bts = (("Reset", self.on_reset, "<Alt-r>"),
               ("New", self.on_add, "<Alt-n>"),
               ("Edit", self.on_edit, "<Alt-e>"),
               ("Close", self.parent.on_exit, "<Alt-c>"))

        for btn in bts:
            self.master.engine.get_button(w, btn[0]).bind("<Button-1>", btn[1])
            self.parent.bind(btn[2], btn[1])

        w.pack(fill=tk.BOTH, side=tk.RIGHT)
        f0.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

    def center_ui(self):

        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        # calculate position x, y
        d = self.master.engine.get_dimensions()
        w = int(d["w"])
        h = int(d["h"])
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))


    def on_open(self, evt=None):

        self.on_reset()
        self.periodic_call()

    def on_reset(self, evt=None):

        self.set_artists()

    def on_opening_toplevel(self, obj):

        f = obj.UI(self)
        f.on_open()

    def set_artists(self):

        for i in self.Artists.get_children():
            self.Artists.delete(i)

        for i in self.lstTracks.get_children():
            self.lstTracks.delete(i)

        sql = "SELECT * FROM artists WHERE status =1 ORDER BY description;"

        rs = self.master.engine.read(True, sql, ())

        self.Artists.insert("", 0, 0, text="Artists")

        for i in rs:

            artists = self.Artists.insert("",
                                      i[0],
                                      text=i[1],
                                      values=(i[0], "artists"))
            rs_albums = self.load_albums(i[0])

            if rs_albums is not None:

                for album in rs_albums:

                    albums = self.Artists.insert(artists,
                                              album[0],
                                              text=album[1],
                                              values=(album[0], "albums"))

    def load_albums(self, i):

        sql = "SELECT album_id, description\
               FROM albums\
               WHERE artist_id =?\
               AND status =1;"

        return self.master.engine.read(True, sql, (i,))


    def on_artist_selected(self, evt=None):

        s = self.Artists.focus()
        d = self.Artists.item(s)

        if d["values"]:

            if d["values"][1] == "artists":

                pk = d["values"][0]

                self.selected_artist = self.master.engine.get_selected("artists", "artist_id", pk)


            elif d["values"][1] == "albums":

                pk = d["values"][0]

                self.selected_album = self.master.engine.get_selected("albums", "album_id", pk)

                sql = "SELECT track_id, track_name, composer, milliseconds,unit_price FROM tracks WHERE album_id =?;"

                args = (self.selected_album[0],)

                self.set_tracks(sql, args)

    def on_artist_activated(self, evt=None):

        s = self.Artists.focus()
        d = self.Artists.item(s)

        if d["values"]:

            if d["values"][1] == "albums":

                pk = d["values"][0]

                self.selected_album = self.master.engine.get_selected("albums", "album_id", pk)

                self.on_add()


    def on_add(self, evt=None):

        if self.Artists.focus():

            frames.track.UI(self).on_open(self.selected_artist)

        else:
            msg = "PLease, select an artist befor add a track."
            messagebox.showwarning(self.master.title(),
                                   msg,
                                   parent=self)


    def on_edit(self, evt):

        if self.lstTracks.focus():

            item_iid = self.lstTracks.selection()

            pk = int(item_iid[0])

            selected_track = self.master.engine.get_selected("tracks", "track_id", pk)

            frames.track.UI(self, item_iid).on_open(self.selected_artist, selected_track,)


    def on_track_activated(self, evt):

        self.on_edit(self)

    def on_track_selected(self, evt):

        if self.lstTracks.focus():
            item_iid = self.lstTracks.selection()
            pk = int(item_iid[0])
            self.selected_track = self.master.engine.get_selected("tracks", "track_id", pk)


    def set_tracks(self, sql, args):

        for i in self.lstTracks.get_children():
            self.lstTracks.delete(i)

        rs = self.master.engine.read(True, sql, args)

        if rs:

            for i in rs:

                self.lstTracks.insert("", tk.END, iid=i[0], text=i[0],
                                      values=(i[1], i[2], i[3], i[4]),)

        s = "{0} {1}".format("Tracks", len(self.lstTracks.get_children()))

        self.lblTracks["text"] = s

    def on_license(self):
        frames.license.UI(self).on_open()

    def on_python_version(self):
        s = self.master.engine.get_python_version()
        messagebox.showinfo(self.master.title(), s, parent=self)

    def on_tkinter_version(self):
        s = "Tkinter patchlevel\n{0}".format(self.master.tk.call("info", "patchlevel"))
        messagebox.showinfo(self.master.title(), s, parent=self)

    def on_about(self,):
        messagebox.showinfo(self.master.title(),
                            self.master.info,
                            parent=self)

    def on_dump(self):
        self.master.engine.dump()
        messagebox.showinfo(self.master.title(), "Dump executed.", parent=self)

    def on_vacuum(self):
        sql = "VACUUM;"
        self.master.engine.write(sql)
        messagebox.showinfo(self.master.title(), "Vacuum executed.", parent=self)

    def on_log(self,):
        self.nametowidget(".").engine.get_log_file()

    def periodic_call(self):

        self.parent.clock.check_queue(self.status_bar_text)

        if self.parent.clock.is_alive():
            self.after(1, self.periodic_call)
        else:
            pass


class App(tk.Tk):
    """Application start here"""
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.engine = Engine()

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.set_option_db()
        self.set_style(kwargs["style"])
        self.set_title(kwargs["title"])
        self.set_icon()
        self.set_info()
        #set clock and start it.
        self.set_clock()
        w = Main(self)
        w.on_open()
        
    def set_clock(self,):
        self.clock = self.engine.get_clock()
        self.clock.start()

    def set_option_db(self):
        file = self.engine.get_file("optionDB")
        self.option_readfile(file)

    def set_style(self, which):
        self.style = ttk.Style()
        self.style.theme_use(which)
        self.style.configure(".", background=self.engine.get_rgb(240, 240, 237))

    def set_title(self, title):
        s = "{0}".format(title)
        self.title(s)

    def set_icon(self):
        icon = tk.PhotoImage(data=self.engine.get_icon("app"))
        self.call("wm", "iconphoto", self._w, "-default", icon)

    def set_info(self,):
        msg = "{0}\nauthor: {1}\ncopyright: {2}\ncredits: {3}\nlicense: {4}\nversion: {5}\
               \nmaintainer: {6}\nemail: {7}\ndate: {8}\nstatus: {9}"
        info = msg.format(self.title(), __author__, __copyright__, __credits__, __license__, __version__, __maintainer__, __email__, __date__, __status__)
        self.info = info

    def on_exit(self, evt=None):
        if messagebox.askokcancel(self.title(), "Do you want to quit?", parent=self):
            self.engine.con.close()
            if self.clock is not None:
                self.clock.stop()
            self.destroy()

def main():
    #if you want pass a number of arbitrary args or kwargs...
    args = []

    for i in sys.argv:
        args.append(i)

    kwargs = {"style":"clam", "title":"The Chinook Sample Database GUI",}

    app = App(*args, **kwargs)

    app.mainloop()


if __name__ == "__main__":
    main()
