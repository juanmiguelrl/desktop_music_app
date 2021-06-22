import random

####################
# CONSTANTS
####################

# String representation
SHARP = u"\u266f"
FLAT = u"\u266D"

# Notes list
NOTES = ["do", f"do{SHARP}/re{FLAT}", "re", f"re{SHARP}/mi{FLAT}", "mi", "fa", f"fa{SHARP}/sol{FLAT}",
         "sol", f"sol{SHARP}/la{FLAT}", "la", f"la{SHARP}/si{FLAT}", "si"]

# Interval map
ACRON_NAME_INTERVALS = { "2m":"Segunda menor", "2M":"Segunda mayor", "3m":"Tercera menor", 
                         "3M":"Tercera mayor", "4j":"Cuarta justa", "4aum":"Cuarta aumentada",
                         "5j":"Quinta justa", "6m":"Sexta menor", "6M":"Sexta mayor",
                         "7m":"Séptima menor", "7M":"Séptima mayor", "8a":"Octava" }

####################
# FUNCTIONS
####################
def get_interval_distance(key):
    return list(ACRON_NAME_INTERVALS.keys()).index(key) + 1  # in semitones

def get_interval_name(key):
    return ACRON_NAME_INTERVALS[key]

def get_interval_full_name(key):
    return get_interval_name(key) + f" ({key})"

def get_interval_key_by_name(name):
    return list(ACRON_NAME_INTERVALS)[list(ACRON_NAME_INTERVALS.values()).index(name)]

def get_interval_key_by_full_name(full_name):
    name = full_name[0:full_name.index(" (")]
    return get_interval_key_by_name(name)

def example_notes(key, direction):
    index = random.randint(0, len(NOTES)-1)

    note1 = NOTES[index]
    note2 = None

    if direction == 'asc':
        note2 = NOTES[(index + get_interval_distance(key)) % len(NOTES)]
    else:
        note2 = NOTES[(index - get_interval_distance(key)) % len(NOTES)]

    return note1,note2