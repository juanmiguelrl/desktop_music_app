from threading import Thread

class MusicController:

    def on_update_avaliable_intervals(self):
        Thread(target=self.model.search_intervals, daemon=True).start()
        
    def on_entry_changed(self, widget):
        self.model.validate_query(widget.get_text())

    def on_entry_search(self, widget):
        query = widget.get_text()
        if self.model.validate_query(query):
            Thread(target=self.model.search_songs, args=(query.split("_")), daemon=True).start()

    def on_direction_changed(self, widget, direction):
        self.model.set_interval_direction(direction)

    def on_button_search(self, widget, key):
        Thread(target=self.model.search_songs, args=(key,), daemon=True).start()

    def set_model(self, model):
        self.model = model