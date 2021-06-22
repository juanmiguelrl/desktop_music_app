import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import gettext
import operator
import model    # needed to use global music information in order to sort interval buttons

_ = gettext.gettext

class MusicView:

    elements_screen1 = []
    elements_screen2 = []

    def run(self):
        self.main_window.show_all()
        self.infobar.hide()
        self.set_screen(0)
        self.controller.on_update_avaliable_intervals()
        Gtk.main()

    def build(self):
        self.main_window = Gtk.Window(title="MyMusicApp")
        self.main_window.set_default_size(400, 500)
        self.main_window.connect('delete-event', Gtk.main_quit)
        self.main_window.show()

        window_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=0)
        self.main_window.add(window_vbox)
        window_vbox.show()

        # Info bar
        self.infobar = Gtk.InfoBar()

        label = Gtk.Label(label=_("Lo sentimos, parece que hay un problema con el servidor"))
        self.infobar.get_content_area().add(label)
        self.infobar.set_message_type(Gtk.MessageType.ERROR)

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
        
        return_button.connect("clicked", lambda widget: self.set_screen(0))

        self.elements_screen2.append(return_button)
        self.body_vbox.add(return_button)

        # Search bar
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_margin_top(40)
        self.search_entry.set_placeholder_text(_("<abreviatura>_<asc_des> (e.g. '8a_des')"))
        self.body_vbox.pack_start(self.search_entry, expand=False, fill=False, padding=0)

        # Search bar result subtext
        self.text_result = Gtk.Label()
        self.text_result.set_margin_bottom(20)

        self.text_result.set_halign(Gtk.Align.START)
        self.body_vbox.pack_start(self.text_result, expand=False, fill=False, padding=5)
        self.elements_screen2.append(self.text_result)

        # Selection text
        select_label = Gtk.Label()
        text_select = _("o selecciona")
        select_label.set_markup(f"<big>{text_select}</big>")
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
        self.ascendent_button = Gtk.RadioButton(label=_("Ascendente"))

        self.descendent_button = Gtk.RadioButton.new_with_label_from_widget(self.ascendent_button, _("Descendente"))
        self.descendent_button.set_active(False)

        header_box.add(self.ascendent_button)
        header_box.add(self.descendent_button)

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
        self.stack.add_titled(notes_vbox, ("notas"), _("Notas de ejemplo"))

        distance_label = Gtk.Label()
        note_label = Gtk.Label()
        note_label2 = Gtk.Label()

        notes_vbox.pack_start(distance_label, False, False, padding=5)
        notes_vbox.pack_start(note_label, False, False, padding=5)
        notes_vbox.pack_start(note_label2, False, False, padding=5)

        songs_window = Gtk.ScrolledWindow()
        self.stack.add_titled(songs_window, ("canciones"), _("Cancion representativa"))

        self.songs_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        songs_window.add(self.songs_vbox)

        self.body_vbox.pack_start(stacksw, False, False, 10)
        self.body_vbox.pack_start(self.stack, True, True, 10)

    ##### Infobar
    def update_infobar(self, connected):
        if connected:
            self.infobar.hide()
        else:
            self.infobar.show_all()

    ##### Search entry
    def update_invalid_query(self, value):
        if value:
            self.search_entry.get_style_context().add_class("error")
        else:
            self.search_entry.get_style_context().remove_class("error")

    ##### List of avaliable intervals     
    def update_interval_list(self, avaliable_intervals):
        # Clear the current list
        for element in self.intervals_list:
            element.destroy()

        # Create each button
        for key in avaliable_intervals:
            row = Gtk.ListBoxRow(selectable=False, activatable=False)
            button = Gtk.Button(label=model.get_interval_full_name(key))
            button.set_margin_top(5)
            button.connect("clicked", self.controller.on_button_search, model.translate_key(key))
            row.add(button)
            
            row.show_all()
            self.intervals_list.add(row)

    ##### List of notes
    def add_interval_info(self, key, mode, info):
        box = self.stack.get_child_by_name("notas")
        
        distance = box.get_children()[0]
        distance_text = _("Distancia")
        distance.set_markup(f"<i>{distance_text}: {info}</i>")

        note1 = box.get_children()[1]
        note2 = box.get_children()[2]

        sample1 = model.example_notes(key, mode)
        sample2 = sample1
        while sample2 == sample1:  # To not repeat the sample
            sample2 = model.example_notes(key, mode)

        note1.set_markup(f"<big>{sample1[0]}-{sample1[1]}</big>")
        note2.set_markup(f"<big>{sample2[0]}-{sample2[1]}</big>")

    ##### List of songs
    def add_song_to_list(self, title, link, fav, first=False):
        if not first:
            separator = Gtk.Separator()
            separator.show()
            self.songs_vbox.pack_start(separator, False, False, 10)

        text = _('Titulo: ')
        if link != '':
            help_text = _("Abre el enlace en el navegador")
            text = text + '<a href="' + link + f'" title="{help_text}">'+ title +'</a>' +'\n'
        else:
            text = text + f"{title} \n"

        favourite_text = _("Favorita")
        yes_text = _("SI")
        no_text = _("NO")
        text = text + f'{favourite_text}: {yes_text if fav == "YES" else no_text}'

        song_label = Gtk.Label()
        song_label.set_halign(Gtk.Align.START)
        song_label.set_markup(text)
        song_label.show()
        self.songs_vbox.add(song_label)

    def add_interval_songs(self, songs):
        tab = self.stack.get_child_by_name("canciones")

        # Clear previous songs
        for obj in self.songs_vbox:
            obj.destroy()

        # Get a favourite song
        fav = None
        for song in songs:
            if song[2] == "YES":
                fav = song
                break
    
        if fav == None:  # If there are no favourite, choose the first one
            fav = songs[0]

        songs.remove(fav)
        self.add_song_to_list(fav[0], fav[1], fav[2], True)
        
        # Button to show more songs
        expand_button = Gtk.Button(label=_("Mostrar mas canciones"))
        expand_button.show()

        expand_button.connect("clicked", self.expand_songs, songs)
        self.songs_vbox.pack_start(expand_button, False, False, 10)

    def add_image_no_song(self):
        tab = self.stack.get_child_by_name("canciones")
        box = tab.get_children()[0].get_children()[0]

        # Clear previous songs
        for obj in box:
            obj.destroy()

        image = Gtk.Image.new_from_file("../images/cara.png")
        image.show()
        box.add(image)

    def update_results_data(self, query, info, songs):
        self.search_entry.set_text(query)
        text_results = _("Resultados para")
        self.text_result.set_markup(f'<i>{text_results} "{query}"</i>')

        fields = query.split("_")
        self.add_interval_info(fields[0], fields[1], info)

        if (songs == [""]):
            self.add_image_no_song()
        else:
            self.add_interval_songs(songs)

        self.set_screen(1)

    def expand_songs(self, widget, songs):
        widget.destroy()
        for song in songs:
            self.add_song_to_list(song[0], song[1], song[2])

    ##### Swap screens
    def set_screen(self, screen):
        self.body_vbox.show_all()

        hide_list = self.elements_screen1 if screen == 1 else self.elements_screen2
        for element in hide_list:
            element.hide()

    def set_controller(self, controller):
        self.controller = controller
        self.search_entry.connect("search-changed", controller.on_entry_changed)
        self.search_entry.connect("activate", controller.on_entry_search)
        self.ascendent_button.connect("clicked", controller.on_direction_changed, "asc")
        self.descendent_button.connect("clicked", controller.on_direction_changed, "des")
        # connection button->controller is done in the creation moment of the button, in update_interval_list 

    def set_sort_func(self, widget, fun):
        self.intervals_list.set_sort_func(self.compare_intervals, fun)

    def compare_intervals(self, row1, row2, fun):
        interval1 = row1.get_children()[0].get_label()  # row->button->label
        interval2 = row2.get_children()[0].get_label()

        key_list = list(model.ACRON_NAME_INTERVALS)
        key1 = model.get_interval_key_by_full_name(interval1)   # using global music information, not a model instance
        key2 = model.get_interval_key_by_full_name(interval2)

        return fun(key_list.index(key1), key_list.index(key2))

