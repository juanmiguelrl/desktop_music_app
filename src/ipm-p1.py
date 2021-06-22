#!/usr/bin/env python3

import locale
import gettext
from pathlib import Path
import model
import controller
import view

if __name__ == "__main__":

    locale.setlocale(locale.LC_ALL, '')
    LOCALE_DIR = Path(__file__).parent / "locale"
    locale.bindtextdomain('MusicApp',LOCALE_DIR)
    gettext.bindtextdomain('MusicApp',LOCALE_DIR)
    gettext.textdomain('MusicApp')

    model = model.MusicModel()
    controller = controller.MusicController()
    view = view.MusicView()
    view.build()

    model.set_view(view)
    controller.set_model(model)
    view.set_controller(controller)

    view.run()
