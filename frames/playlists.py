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
import frames.tracks as ui

class UI(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(name="playlists")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(800, 400)
        self.obj = None
        self.init_ui()
        self.master.engine.center_me(self)
        
    def init_ui(self):

        f = self.master.engine.get_frame(self, 8)

        w = self.master.engine.get_frame(f, 2)

        lf = ttk.LabelFrame(w, text="Double cLick to add a track",)
         
        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Description", "w", True, 100, 100],)
        
        self.lstPlaylist = self.master.engine.get_tree(lf, cols,)
        self.lstPlaylist.tag_configure("status", background="light gray")
        self.lstPlaylist.bind("<<TreeviewSelect>>", self.on_playlist_selected)
        self.lstPlaylist.bind("<Double-1>", self.on_playlist_activated)

        lf.pack(fill=tk.BOTH, expand=1)

        w.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

        w = self.master.engine.get_frame(f, 2)

        lf = ttk.LabelFrame(w, text="Double cLick to remove a track",)

        cols = (["#0", "id", "w", False, 0, 0],
                ["#1", "Track", "w", True, 100, 100],
                ["#2", "Album", "w", True, 100, 100],
                ["#3", "Artist", "w", True, 100, 100],)

        self.lstTracks = self.master.engine.get_tree(lf, cols,)
        self.lstTracks.bind("<Double-Button-1>", self.on_track_activated)

        lf.pack(fill=tk.BOTH, expand=1)

        w.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

        f.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def on_open(self,):

        msg = "{0} Management".format(self.winfo_name().capitalize())
        self.title(msg)
        self.set_values()

    def set_values(self, evt=None):

        for i in self.lstPlaylist.get_children():
            self.lstPlaylist.delete(i)

        sql = "SELECT * FROM playlists;"

        rs = self.master.engine.read(True, sql, ())

        if rs:
            
            for i in rs:
                self.lstPlaylist.insert("", tk.END, iid=i[0], text=i[0], values=(i[1],))
            

    def set_tracks(self, selected_playlist):

        if self.lstPlaylist.focus():

            for i in self.lstTracks.get_children():
                self.lstTracks.delete(i)

            self.playlist_tracks_id = []               

            sql = "SELECT playlist_track.track_id,\
                          tracks.track_name,\
                          albums.description,\
                          artists.description,\
                          tracks.track_id\
                   FROM playlist_track\
                   INNER JOIN tracks ON playlist_track.track_id = tracks.track_id\
                   INNER JOIN albums ON tracks.album_id = albums.album_id\
                   INNER JOIN artists ON albums.artist_id = artists.artist_id\
                   WHERE playlist_track.playlist_id =?;"
            
            args = (selected_playlist[0],)
            
            rs = self.master.engine.read(True, sql, args)

            if rs:

                for i in rs:
                    self.lstTracks.insert("", tk.END, iid=i[0], text=i[0], values=(i[1], i[2], i[3],))
                    self.playlist_tracks_id.append(i[4])

    def on_playlist_selected(self, evt):

        if self.lstPlaylist.focus():
            item_iid = self.lstPlaylist.selection()
            pk = int(item_iid[0])
            self.selected_playlist = self.master.engine.get_selected("playlists", "playlist_id", pk)
            self.set_tracks(self.selected_playlist)
                    
    def on_playlist_activated(self, evt=None):

        if self.lstPlaylist.focus():
            item_iid = self.lstPlaylist.selection()
            self.obj = ui.UI(self, item_iid)
            self.obj.on_open(self.playlist_tracks_id, self.selected_playlist,)

        else:
            messagebox.showwarning(self.master.title(),
                                   self.master.engine.no_selected,
                                   parent=self)

    def on_track_activated(self, evt):

        if self.lstTracks.focus():

            item_iid = self.lstTracks.selection()
            pk = int(item_iid[0])
            selected_track = self.master.engine.get_selected("tracks", "track_id", pk)

            if messagebox.askyesno(self.master.title(), self.master.engine.ask_to_delete, parent=self) == True:
                sql = "DELETE FROM playlist_track WHERE playlist_id =? AND track_id =?;"
                args = (self.selected_playlist[0], selected_track[0],)
                self.master.engine.write(sql, args)
                self.set_tracks(self.selected_playlist)
                
    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
