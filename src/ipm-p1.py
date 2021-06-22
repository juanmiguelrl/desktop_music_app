#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import operator
import time
from threading import Thread

import music
from client import MusicClient

class MusicWindow:

    mode = "asc"

    retrying_connection = False     # Prevent from trying reconnect from various threads
    
    elements_screen1 = []
    elements_screen2 = []

    def __init__(self, title="Default title", width=400, height=500, resizable=True):
        self.client = MusicClient()

        self.main_window = Gtk.Window(title=title, resizable=resizable)
        self.main_window.set_default_size(width, height)
        self.main_window.connect('delete-event', Gtk.main_quit)
        self.main_window.show()

    ####################
    # ACTIONS
    ####################  

    def search_intervals(self, *args):
        data = self.client.get_avaliable_intervals()
        connected = (data != None)

        GLib.idle_add(self.update_infobar, connected)
        if connected:
            GLib.idle_add(self.update_interval_list, data)
        else:
            self.check_connectivity(self.search_intervals)

    def search_songs(self, *args):
        key, mode = args[0], args[1]
        info = self.client.get_interval_info(key)
        songs = self.client.get_interval_songs(key, mode)
        
        connected = (info != None) and (songs != None)
        GLib.idle_add(self.update_infobar, connected)

        if connected:
            GLib.idle_add(self.update_results_data, f"{key}_{mode}", info, songs)
        else:
            self.check_connectivity(self.search_songs, *args)  # try to recconect

    def on_button_search(self, widget):
        label = widget.get_label()
        key = music.get_interval_key_by_full_name(label)
        Thread(target=self.search_songs, args=(key,self.mode), daemon=True).start()

    def on_entry_search(self, widget):
        key, mode = self.validate_query(widget)

        if key != None and mode != None:
            Thread(target=self.search_songs, args=(key,mode), daemon=True).start()
        
    def on_mas_canciones_clicked(self, widget, box, info):
        widget.destroy()

        for song in info:
            self.add_song_to_list(box, song[0], song[1], song[2], False)

    def on_return_clicked(self, widget, screen):
        self.set_screen(screen)

    ####################
    # STATE
    ####################
    
    def check_connectivity(self, fun, *args):
        if self.retrying_connection:
            return

        self.retrying_connection = True
        response = self.client.get_avaliable_intervals()

        while response == None:
            print("Cheking connectivity...")
            response = self.client.get_avaliable_intervals()
            time.sleep(0.5)

        print("Connection established")
        self.retrying_connection = False

        GLib.idle_add(self.update_infobar, True)
        fun(*args)  # Retry the operation that failed before

    def set_interval_mode(self, widget, mode):
        self.mode = mode

    def set_sort_func(self, widget, fun):
        self.intervals_list.set_sort_func(self.compare_intervals, fun)

    ####################
    # VIEW
    ####################

    ##### Skeleton of the app
    def build(self):
        window_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=0)
        self.main_window.add(window_vbox)
        window_vbox.show()

        # Info bar
        self.infobar = Gtk.InfoBar()

        label = Gtk.Label(label="Lo sentimos, parece que hay un problema con el servidor")
        self.infobar.get_content_area().add(label)
        self.infobar.set_message_type(Gtk.MessageType.ERROR)

        self.infobar.connect("response", lambda widget,data: widget.hide())
        window_vbox.pack_start(self.infobar, expand=False, fill=False, padding=0)

        # Body vbox
        self.body_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        self.body_vbox.set_border_width(30)
        window_vbox.pack_start(self.body_vbox, expand=True, fill=True, padding=0)

        # Return button
        return_button = Gtk.Button()
        return_button.set_relief(Gtk.ReliefStyle.NONE)
        return_button.set_halign(Gtk.Align.START)

        return_arrow = Gtk.Image.new_from_file("../images/return_arrow.png")
        return_button.set_image(return_arrow)
        
        return_button.connect("clicked", self.on_return_clicked, 0)

        self.elements_screen2.append(return_button)
        self.body_vbox.add(return_button)

        # Search bar
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_margin_top(40)
        self.search_entry.set_placeholder_text("<abreviatura>_<asc_des> (e.g. '8a_des')")

        self.search_entry.connect("search-changed", self.validate_query)
        self.search_entry.connect("activate", self.on_entry_search)
        
        self.body_vbox.pack_start(self.search_entry, expand=False, fill=False, padding=0)

        # Search bar result subtext
        self.text_result = Gtk.Label()
        self.text_result.set_markup('<i>Resultados para "3m_asc"</i>')
        self.text_result.set_margin_bottom(20)

        self.text_result.set_halign(Gtk.Align.START)
        self.body_vbox.pack_start(self.text_result, expand=False, fill=False, padding=5)
        self.elements_screen2.append(self.text_result)

        # Selection text
        select_label = Gtk.Label()
        select_label.set_markup("<big>o selecciona</big>")
        self.elements_screen1.append(select_label)
        self.body_vbox.pack_start(select_label, expand=False, fill=False, padding=20)

        # Frame list container
        frame = Gtk.Frame()
        self.elements_screen1.append(frame)
        self.body_vbox.pack_start(frame, expand=True, fill=True, padding=0)

        frame_box = Gtk.VBox(homogeneous=False, spacing=5)
        frame.add(frame_box)

        # Header box
        header_box = Gtk.Box(homogeneous=False)
        frame_box.pack_start(header_box, expand=False, fill=False, padding=0)

        # Interval mode options
        ascendent_button = Gtk.RadioButton(label="Ascendente")

        descendent_button = Gtk.RadioButton.new_with_label_from_widget(ascendent_button, "Descendente")
        descendent_button.set_active(False)

        ascendent_button.connect("clicked", self.set_interval_mode, "asc")
        descendent_button.connect("clicked", self.set_interval_mode, "des")

        header_box.add(ascendent_button)
        header_box.add(descendent_button)

        # Intervals list sort buttons
        sort_asc_button = Gtk.Button()
        up_arrow = Gtk.Image.new_from_file("../images/up_arrow.png")
        sort_asc_button.set_image(up_arrow)
        sort_asc_button.set_margin_end(3)

        sort_des_button = Gtk.Button()
        down_arrow = Gtk.Image.new_from_file("../images/down_arrow.png")
        sort_des_button.set_image(down_arrow)

        sort_asc_button.connect("clicked", self.set_sort_func, operator.gt)
        sort_des_button.connect("clicked", self.set_sort_func, operator.lt)

        header_box.pack_end(sort_des_button, False, False, 0)
        header_box.pack_end(sort_asc_button, False, False, 0)

        # Intervals list buttons
        scroll_window = Gtk.ScrolledWindow()
        frame_box.add(scroll_window)

        self.intervals_list = Gtk.ListBox()
        self.intervals_list.set_sort_func(self.compare_intervals, operator.gt)
        Thread(target=self.search_intervals, daemon=True).start()
        scroll_window.add(self.intervals_list)

        # Results stack
        self.stack = Gtk.Stack() 
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT) 
        self.stack.set_transition_duration(1000) 
        self.elements_screen2.append(self.stack)

        # Stack tabs
        stacksw = Gtk.StackSwitcher()
        stacksw.set_stack(self.stack)
        stacksw.set_halign(Gtk.Align.CENTER)
        self.elements_screen2.append(stacksw)

        notes_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.stack.add_titled(notes_vbox, "notas", "Notas de ejemplo")

        distance_label = Gtk.Label()
        note_label = Gtk.Label()
        note_label2 = Gtk.Label()

        notes_vbox.pack_start(distance_label, False, False, padding=5)
        notes_vbox.pack_start(note_label, False, False, padding=5)
        notes_vbox.pack_start(note_label2, False, False, padding=5)

        songs_window = Gtk.ScrolledWindow()
        self.stack.add_titled(songs_window, "canciones", "Canción representativa")

        songs_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        songs_window.add(songs_vbox)

        self.body_vbox.pack_start(stacksw, False, False, 10)
        self.body_vbox.pack_start(self.stack, True, True, 10)  

    ##### Infobar
    def update_infobar(self, connected):
        if connected:
            self.infobar.hide()
        else:
            self.infobar.show_all()

    ##### List of avaliable intervals
    def update_interval_list(self, avaliable_intervals):
        # Clear the current list
        for element in self.intervals_list:
            element.destroy()

        # Create each button
        for key in avaliable_intervals:
            row = Gtk.ListBoxRow(selectable=False, activatable=False)

            button = Gtk.Button(label=music.get_interval_full_name(key))
            button.set_margin_top(5)
            button.connect("clicked", self.on_button_search)
            row.add(button)
            
            row.show_all()
            self.intervals_list.add(row)

    ##### List of notes
    def add_interval_info(self, key, mode, info):
        box = self.stack.get_child_by_name("notas")
        
        distance = box.get_children()[0]
        distance.set_markup(f"<i>Distancia: {info}</i>")

        note1 = box.get_children()[1]
        note2 = box.get_children()[2]

        sample1 = music.example_notes(key, mode)
        sample2 = sample1
        while sample2 == sample1:  # To not repeat the sample
            sample2 = music.example_notes(key, mode)

        note1.set_markup(f"<big>{sample1[0]}-{sample1[1]}</big>")
        note2.set_markup(f"<big>{sample2[0]}-{sample2[1]}</big>")

    ##### List of songs
    def add_song_to_list(self, list_box, title, link, fav, first):
        if not first:
            separator = Gtk.Separator()
            separator.show()
            list_box.pack_start(separator, False, False, 10)

        text = 'Título: '
        if link != '':
            text = text + '<a href="' + link +'"title="Abre el enlace en el navegador">' + title +'</a>' +'\n'
        else:
            text = text + f"{title} \n"
        text = text + f'Favorita: {"SI" if fav == "YES" else "NO"}'

        song_label = Gtk.Label()
        song_label.set_halign(Gtk.Align.START)
        song_label.set_markup(text)
        song_label.show()
        list_box.add(song_label)

    def add_interval_songs(self, info):
        tab = self.stack.get_child_by_name("canciones")
        box = tab.get_children()[0].get_children()[0]

        # Clear previous songs
        for obj in box:
            obj.destroy()

        # Get a favourite song
        fav = None
        for song in info:
            if song[2] == "YES":
                fav = song
                break
    
        if fav == None:  # If there are no favourite, choose the first one
            fav = info[0]

        info.remove(fav)
        self.add_song_to_list(box, fav[0], fav[1], fav[2], True)
        
        # Button to show more songs
        expand_button = Gtk.Button(label="Mostrar más canciones")
        expand_button.show()

        expand_button.connect('clicked', self.on_mas_canciones_clicked, box, info)
        box.pack_start(expand_button, False, False, 10)

    def add_image_no_song(self):
        tab = self.stack.get_child_by_name("canciones")
        box = tab.get_children()[0].get_children()[0]

        # Clear previous songs
        for obj in box:
            obj.destroy()

        image = Gtk.Image.new_from_file("images/cara.png")
        image.show()
        box.add(image)

    def update_results_data(self, query, info, songs):
        self.search_entry.set_text(query)
        self.text_result.set_markup(f'<i>Resultados para "{query}"</i>')

        fields = query.split("_")
        self.add_interval_info(fields[0], fields[1], info)

        if (songs == [""]):
            self.add_image_no_song()
        else:
            self.add_interval_songs(songs)

        self.set_screen(1)

    ##### Swap views
    def set_screen(self, screen):
        self.body_vbox.show_all()

        if screen == 0:
            for element in self.elements_screen2:
                element.hide()
        else:
            for element in self.elements_screen1:
                element.hide()

    ####################
    # UTILITIES
    ####################

    def validate_query(self, widget):
        widget.get_style_context().add_class("error")

        text = widget.get_text().split("_")
        if (text == [""]):
            widget.get_style_context().remove_class("error")
            return None, None

        if (len(text) != 2):
            return None, None

        key, mode = text[0], text[1]
        if key in music.ACRON_NAME_INTERVALS.keys() and mode in ("asc", "des"):
            widget.get_style_context().remove_class("error")
            return key, mode

        return None, None

    def compare_intervals(self, row1, row2, fun):
        interval1 = row1.get_children()[0].get_label()  # row->button->label
        interval2 = row2.get_children()[0].get_label()

        key_list = list(music.ACRON_NAME_INTERVALS)
        key1 = music.get_interval_key_by_full_name(interval1)
        key2 = music.get_interval_key_by_full_name(interval2)

        return fun(key_list.index(key1), key_list.index(key2))


if __name__ == "__main__":
    window = MusicWindow(title="MyMusicApp")
    window.build()
    window.set_screen(0)
    Gtk.main()