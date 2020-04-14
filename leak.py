from functools import partial
import kivy

kivy.require("1.11.1")
from kivy.utils import platform

print(f"platform: {platform}")

from kivy.lang import Builder

from kivy.app import App
from kivy.uix.button import Button
import gc


class PowerListItem(Button):
    pass


class Contero(App):

    def build(self):
        return Builder.load_file("leak.kv")

    def on_start(self):
        pass

    def discover(self, cnt):
        ids = App.get_running_app().root.ids
        for i in range(cnt):
            item = PowerListItem(
                text="List Item" + f" {i + 1:>2}"
            )
            ids.ps_list.add_widget(item)

    def discovery_clean(self):
        for item in self.root.ids.ps_list.children:
            print(f"item: {item.text}")
        self.root.ids.ps_list.clear_widgets()
        gc.collect()

    def discovery_request(self, item_count=50):
        self.discovery_clean()
        self.discover(item_count)


if __name__ == "__main__":
    Contero().run()

