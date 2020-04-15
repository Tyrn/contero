from functools import partial
import kivy

kivy.require("1.11.1")
from kivy.utils import platform

print(f"platform: {platform}")

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import TwoLineAvatarIconListItem
import gc
from memory_profiler import profile


#ACTION_ICON = "eye"


class PowerListItem(TwoLineAvatarIconListItem):
    """The engaged power supply item."""


class TabList(FloatLayout, MDTabsBase):
    """The engaged power supplies tab."""

    def surfacing(self, tab_text):
        pass

    def discover(self, cnt):
        ids = MDApp.get_running_app().root.ids
        for i in range(cnt):
            item = PowerListItem(
                text="List Item" + f" {i + 1:>2}", secondary_text="none"
            )
            ids.ps_list.add_widget(item)


class Contero(MDApp):

    def build(self):
        return Builder.load_file("leak_md.kv")

    def on_start(self):
        self.theme_cls.primary_palette = "Gray"

    @profile
    def discovery_clean(self):
        for item in self.root.ids.ps_list.children:
            pass
            #print(f"item: {item.text}")
        self.root.ids.ps_list.clear_widgets()
        gc.collect()

    def discovery_request(self, item_count=50):
        self.discovery_clean()

        tab_list = self.root.ids.ps_tab_list

        tab_list.discover(item_count)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        """

        instance_tab.surfacing(tab_text)


if __name__ == "__main__":
    Contero().run()
