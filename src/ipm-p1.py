#!/usr/bin/env python3

import model
import controller
import view

if __name__ == "__main__":
    model = model.MusicModel()
    controller = controller.MusicController()
    view = view.MusicView()
    view.build()

    model.set_view(view)
    controller.set_model(model)
    view.set_controller(controller)

    view.run()