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
        super().__init__(name="tracks")

        self.parent = parent
        self.index = index
        self.attributes("-topmost", True)
        self.master.engine.center_me(self)
        self.init_ui()

    def init_ui(self):

        f0 = self.master.engine.get_frame(self, 8)

        f1 = ttk.Frame(f0,)
        cols = (["#0", "", "w", False, 200, 200],
                ["#1", "", "w", True, 0, 0],)
        self.Artists = self.master.engine.get_tree(f1, cols, show="tree")
        self.Artists.show = "tree"
        self.Artists.pack(fill=tk.BOTH, padx=2, pady=2)
        self.Artists.bind("<<TreeviewSelect>>", self.on_artist_selected)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=0)
        
        f2 = ttk.Frame(f0,)
        cols = (["#0", "id", "w", False, 0, 0],
                     ["#1", "Album", "w", True, 100, 100],
                     ["#2", "Composer", "w", True, 100, 100],
                     ["#3", "Milliseconds", "center", True, 20, 20],
                     ["#4", "Price", "center", True, 20, 20],)
       
        self.lblTracks = ttk.LabelFrame(f2, text="Tracks",)
        self.lstTracks = self.master.engine.get_tree(self.lblTracks, cols,)
        #self.lstTracks.bind("<<TreeviewSelect>>", self.get_selected_track)
        self.lstTracks.bind("<Double-1>", self.on_track_activated)
        self.lblTracks.pack(fill=tk.BOTH, expand=1)
        f2.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1) 

       
        f0.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)
        
    def on_open(self, playlist_tracks_id, selected_playlist):

        self.playlist_tracks_id = playlist_tracks_id

        self.selected_playlist = selected_playlist

        msg = "Choose a song to add to your playlist {0}".format(selected_playlist[1])

        self.title(msg)

        self.set_artists()


    def set_artists(self):

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

            if d["values"][1] == "albums":

                pk = d["values"][0]

                self.selected_album = self.master.engine.get_selected("albums", "album_id", pk)

                sql = "SELECT track_id, track_name, composer, milliseconds,unit_price\
                       FROM tracks WHERE album_id =?\
                       ORDER BY track_name;"

                args = (self.selected_album[0],)

                self.set_tracks(sql, args)

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
        
    def get_selected_track(self, evt):

        if self.lstTracks.focus():
            item_iid = self.lstTracks.selection()
            pk = int(item_iid[0])
            self.selected_track = self.master.engine.get_selected(self.table, self.primary_key, pk)

    def on_track_activated(self, evt=None):

        if self.lstTracks.focus():

            item_iid = self.lstTracks.selection()

            pk = int(item_iid[0])

            if pk in (self.playlist_tracks_id):

                msg = "The selected song is already in the playlist."

                messagebox.showwarning(self.master.title(), msg, parent=self)
            else:
                
                selected_track = self.master.engine.get_selected("tracks", "track_id", pk)
                sql = "INSERT INTO playlist_track (playlist_id, track_id) values (?,?);"
                args = (self.selected_playlist[0], selected_track[0])
                self.master.engine.write(sql, args)
                self.playlist_tracks_id.append(selected_track[0])
                self.parent.set_tracks(self.selected_playlist)
                msg = "Selected track {0} add to the playlist.".format(selected_track[1])
                messagebox.showinfo(self.master.title(), msg, parent=self)
                
    def on_cancel(self, evt=None):
        self.destroy()
