import random
import time
import gettext
from gi.repository import GLib
from client import MusicClient

translate = gettext.translation('MusicApp', "locale", fallback=True)
_ = translate.gettext

####################
# MUSIC INFO
####################
# String representation
SHARP = u"\u266f"
FLAT = u"\u266D"

# Notes list
DO,RE,MI,FA,SOL,LA,SI = _("do"), _("re"), _("mi"), _("fa"), _("sol"), _("la"), _("si")
NOTES = [DO, f"{DO}{SHARP}/{RE}{FLAT}", RE, f"{RE}{SHARP}/{MI}{FLAT}", MI, FA, f"{FA}{SHARP}/{SOL}{FLAT}",
         SOL, f"{SOL}{SHARP}/{LA}{FLAT}", LA, f"{LA}{SHARP}/{SI}{FLAT}", SI]

# Abbreviations translations
ACRON_TRANS = { "2m":_("2m"), "2M":_("2M"), "3m":_("3m"), "3M":_("3M"), "4j":_("4j"), "4aum":_("4aum"),
                "5j":_("5j"), "6m":_("6m"), "6M":_("6M"), "7m":_("7m"), "7M":_("7M"), "8a":_("8a")}
# Interval map
ACRON_NAME_INTERVALS = { "2m":_("Segunda menor"), "2M":_("Segunda mayor"), "3m":_("Tercera menor"), 
                         "3M":_("Tercera mayor"), "4j":_("Cuarta justa"), "4aum":_("Cuarta aumentada"),
                         "5j":_("Quinta justa"), "6m":_("Sexta menor"), "6M":_("Sexta mayor"),
                         "7m":_("Septima menor"), "7M":_("Septima mayor"), "8a":_("Octava") }

####################
# MUSIC FUNCTIONS
####################

def translate_key(key):
    return ACRON_TRANS[key]

def original_key(translation):
    try:
        return list(ACRON_TRANS)[list(ACRON_TRANS.values()).index(translation)]
    except ValueError:
        return translation

def get_interval_name(key):
    return ACRON_NAME_INTERVALS[key]

def get_interval_full_name(key):
    return get_interval_name(key) + f" ({translate_key(key)})"

def get_interval_key_by_name(name):
    return list(ACRON_NAME_INTERVALS)[list(ACRON_NAME_INTERVALS.values()).index(name)]

def get_interval_key_by_full_name(full_name):
    name = full_name[0:full_name.index(" (")]
    return get_interval_key_by_name(name)

def example_notes(key, direction):
    index = random.randint(0, len(NOTES)-1)

    distance = list(ACRON_NAME_INTERVALS.keys()).index(original_key(key)) + 1  # in semitones
    distance *= -1 if direction == "des" else 1

    note1 = NOTES[index]
    note2 = NOTES[(index + distance) % len(NOTES)]

    return note1,note2

class MusicModel:
    
    direction = "asc"
    retrying_connection = False  # prevent from trying reconnections from various threads

    def __init__(self):
        self.client = MusicClient("http://localhost", 5000)

    def search_intervals(self, *args):
        data = self.client.get_avaliable_intervals()
        connected = (data != None)

        GLib.idle_add(self.view.update_infobar, connected)
        if connected:
            GLib.idle_add(self.view.update_interval_list, data)
        else:
            self.check_connectivity(self.search_intervals)

    def search_songs(self, *args):
        if len(args) == 2:  # search with entry
            key, direction = args[0], args[1]
        else:   # search with button
            key, direction = args[0], self.direction

        key = original_key(key)
        info = self.client.get_interval_info(key)
        songs = self.client.get_interval_songs(key, direction)
        
        connected = (info != None) and (songs != None)
        GLib.idle_add(self.view.update_infobar, connected)

        if connected:
            GLib.idle_add(self.view.update_results_data, f"{translate_key(key)}_{direction}", info, songs)
        else:
            self.check_connectivity(self.search_songs, *args)  # try to reconnect

    def check_connectivity(self, fun, *args):
        if self.retrying_connection:
            return

        print("Cheking connectivity...")
        self.retrying_connection = True

        response = self.client.get_avaliable_intervals()
        while response == None:
            response = self.client.get_avaliable_intervals()
            time.sleep(0.5)

        print("Connection established")
        self.retrying_connection = False

        GLib.idle_add(self.view.update_infobar, True)
        fun(*args)  # retry the operation that failed before

    def validate_query(self, query):
        args = query.split("_")
        
        if args == [""]:  # empty entry
            self.view.update_invalid_query(False)
            return None

        if len(args) != 2:
            self.view.update_invalid_query(True)
            return False

        key, direction = original_key(args[0]), args[1]
        if key in ACRON_NAME_INTERVALS.keys() and (direction == "asc" or direction == "des"):
            self.view.update_invalid_query(False)
            return True

        self.view.update_invalid_query(True)
        return False

    def set_view(self, view):
        self.view = view

    def set_interval_direction(self, direction):
        self.direction = direction

