from functools import partial
import kivy

kivy.require("1.11.1")
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.icon_definitions import md_icons
import co_lang

T = None


class PowerListItem(OneLineListItem):
    """The engaged power supply item."""

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                tabs = MDApp.get_running_app().root.ids.android_tabs
                # Just like your on_release.
                tabs.tab_bar.parent.dispatch(
                    "on_tab_switch",
                    self.tab_details,
                    self.tab_details.tab_label,
                    md_icons[self.tab_details.text],
                )
                tabs.tab_bar.parent.carousel.load_slide(self.tab_details)
                return True
        return super(PowerListItem, self).on_touch_down(touch)


class TabList(FloatLayout, MDTabsBase):
    """The engaged power supplies tab."""

    def surfacing(self, tab_text):
        pass

    def discover(self, tab_details):
        for i in range(30):
            item = PowerListItem(text=T["co-ps-label-1"] + f" {i + 1:>4}")
            item.tab_details = tab_details
            self.ids.container.add_widget(item)


class TabDetails(FloatLayout, MDTabsBase):
    """The engaged power supply details tab."""

    def surfacing(self, tab_text):
        self.ids.icon.icon = "equalizer"


class Contero(MDApp):
    menu_lang = ObjectProperty()

    def menu_lang_callback(self, lng):
        global T
        T = co_lang.LANG[lng]
        store = JsonStore("co_T.json")
        store.put("co-lang", name=lng)

    def menu_lang_append(self):
        self.menu_lang = MDDropdownMenu(width_mult=2)
        for lng in co_lang.LANG:
            self.menu_lang.items.append(
                {
                    "viewclass": "MDMenuItem",
                    "text": lng,
                    "callback": self.menu_lang_callback,
                }
            )

    def build(self):
        global T
        T = co_lang.LANG["RU"]
        store = JsonStore("co_T.json")
        if store.exists("co-lang"):
            lng = store.get("co-lang")["name"]
            T = co_lang.LANG[lng]

        return Builder.load_file("main.kv")

    def on_start(self):
        self.theme_cls.primary_palette = "Green"
        # self.theme_cls.primary_hue = '900'

        self.menu_lang_append()
        text = "flash"
        main = TabList(text=text)
        main.surfacing(text)
        self.root.ids.android_tabs.add_widget(main)

        details = TabDetails(text="equalizer")
        self.root.ids.android_tabs.add_widget(details)
        Clock.schedule_once(lambda dt: main.discover(details), 4)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        """

        print(f"\ninstance_tab: {instance_tab}")
        print(f"instance_tab_label: {instance_tab_label}")
        print(f"tab_text: {tab_text}")
        instance_tab.surfacing(tab_text)


Contero().run()
