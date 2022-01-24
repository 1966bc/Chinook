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
        super().__init__(name="track")

        self.parent = parent
        self.index = index
        self.resizable(0, 0)
        self.transient(parent)

        self.track = tk.StringVar()
        self.composer = tk.StringVar()
        self.milliseconds = tk.IntVar()
        self.bytes = tk.IntVar()
        self.unit_price = tk.DoubleVar()
        self.status = tk.BooleanVar()
        
        self.val_int = self.master.engine.get_validate_integer(self)
        self.val_float = self.master.engine.get_validate_float(self)
        self.set_style()
        self.master.engine.center_me(self)
        self.init_ui()

    def set_style(self):
        s = ttk.Style()
        s.configure("name.TLabel",
                    foreground=self.master.engine.get_rgb(0, 0, 255),
                    background=self.master.engine.get_rgb(255, 255, 255))

        s.configure("composer.TLabel",
                    foreground=self.master.engine.get_rgb(255, 0, 0),
                    background=self.master.engine.get_rgb(255, 255, 255))

    def init_ui(self):

        f = self.master.engine.get_init_ui(self)

        r = 0
        ttk.Label(f, text="Track:",).grid(row=r, sticky=tk.W)
        self.txtTrack = ttk.Entry(f,
                                    style="name.TLabel",
                                    textvariable=self.track)
        self.txtTrack.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, text="Albums:",).grid(row=r, sticky=tk.W)
        self.cbAlbums = ttk.Combobox(f,)
        self.cbAlbums.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, text="Media:",).grid(row=r, sticky=tk.W)
        self.cbMedia = ttk.Combobox(f,)
        self.cbMedia.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, text="Genre:",).grid(row=r, sticky=tk.W)
        self.cbGenres = ttk.Combobox(f,)
        self.cbGenres.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, text="Composer:").grid(row=r, sticky=tk.W)
        w = ttk.Entry(f, style="composer.TLabel", textvariable=self.composer)
        w.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, text="Milliseconds:").grid(row=r, sticky=tk.W)
        w = ttk.Entry(f, justify=tk.CENTER, width=8, validate="key",
                      validatecommand=self.val_int, textvariable=self.milliseconds)
        w.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, text="Bytes:").grid(row=r, sticky=tk.W)
        w = ttk.Entry(f, justify=tk.CENTER, width=8, validate="key",
                      validatecommand=self.val_int, textvariable=self.bytes)
        w.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, text="Unit Price:").grid(row=r, sticky=tk.W)
        w = ttk.Entry(f, justify=tk.CENTER, width=8, validate="key",
                      validatecommand=self.val_float, textvariable=self.unit_price)
        w.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(f, text="Status:").grid(row=r, sticky=tk.W)
        w = ttk.Checkbutton(f, onvalue=1, offvalue=0, variable=self.status,)
        w.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        self.master.engine.get_save_cancel(self, f)

    def on_open(self, selected_artist, selected_track=None):

        self.selected_artist = selected_artist
        self.set_albums()
        self.set_media()
        self.set_genre()
        

        if self.index is not None:
            self.selected_track = selected_track
            msg = "Update {0}".format(self.winfo_name().capitalize())
            self.set_values()
        else:
            msg = "Insert {0}".format(self.winfo_name().capitalize())
            self.status.set(1)

        self.title(msg)
        self.txtTrack.focus()

    def set_values(self,):

        self.track.set(self.selected_track[1])

        key = next(key
                   for key, value
                   in self.dict_albums.items()
                   if value == self.selected_track[2])
        self.cbAlbums.current(key)

        key = next(key
                   for key, value
                   in self.dict_media.items()
                   if value == self.selected_track[3])
        self.cbMedia.current(key)

        key = next(key
                   for key, value
                   in self.dict_genres.items()
                   if value == self.selected_track[4])
        self.cbGenres.current(key)

        self.composer.set(self.selected_track[5])
        self.milliseconds.set(self.selected_track[6])
        self.bytes.set(self.selected_track[7])
        self.unit_price.set(self.selected_track[8])
        self.status.set(self.selected_track[9])

    def get_values(self,):

        return [self.track.get(),
                self.dict_albums[self.cbAlbums.current()],
                self.dict_media[self.cbMedia.current()],
                self.dict_genres[self.cbGenres.current()],
                self.composer.get(),
                self.milliseconds.get(),
                self.bytes.get(),
                self.unit_price.get(),
                self.status.get()]

    def on_save(self, evt):

        if self.master.engine.on_fields_control(self) == False: return

        if messagebox.askyesno(self.master.title(), 
                               self.master.engine.ask_to_save, 
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.master.engine.get_update_sql("tracks", "track_id")

                args.append(self.selected_track[0])

            else:

                sql = self.master.engine.get_insert_sql("tracks", len(args))

            last_id = self.master.engine.write(sql, args)

            sql = "SELECT track_id, track_name, composer, milliseconds,unit_price FROM tracks WHERE album_id =?;"

            args = (self.dict_albums[self.cbAlbums.current()],)

            self.parent.on_artist_selected()

            if self.index is not None:
                if self.selected_track[2]  == self.dict_albums[self.cbAlbums.current()]:
                    self.parent.lstTracks.selection_set(self.index)
                    self.parent.lstTracks.see(self.index)
                else:
                    self.parent.lstTracks.selection_set(last_id)
                    self.parent.lstTracks.see(last_id)

            self.on_cancel()

    def set_albums(self):

        sql = "SELECT album_id, description FROM albums WHERE artist_id =? AND status =1 ORDER BY description ASC;"
        args = (self.selected_artist[0],)
        index = 0
        self.dict_albums = {}
        values = []
        rs = self.master.engine.read(True, sql, args)

        for i in rs:
            self.dict_albums[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbAlbums["values"] = values

    def set_media(self):

        sql = "SELECT * FROM media_types WHERE status =1 ORDER BY media_type ASC;"
        index = 0
        self.dict_media = {}
        values = []
        rs = self.master.engine.read(True, sql, ())

        for i in rs:
            self.dict_media[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbMedia["values"] = values

    def set_genre(self):

        sql = "SELECT * FROM genres WHERE status =1 ORDER BY description ASC;"
        index = 0
        self.dict_genres = {}
        values = []
        rs = self.master.engine.read(True, sql, ())

        for i in rs:
            self.dict_genres[index] = i[0]
            index += 1
            values.append(i[1])

        self.cbGenres["values"] = values        

    
    def on_cancel(self, evt=None):
        self.destroy()
