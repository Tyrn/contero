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
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDIconButton
from kivymd.icon_definitions import md_icons
import co_lang

T = None


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    """Custom right container."""


class RightSelectButton(IRightBodyTouch, MDIconButton):
    """Custom right container."""

    def on_release(self):
        self.power__list_item.select_details()


class PowerListItem(OneLineAvatarIconListItem):
    """The engaged power supply item."""

    def select_details(self):
        self.tab__details.ids.pd_absence_label.text = (
            self.text + f",  {T['co-details-l']}"
        )
        Contero.select_tab(self.tab__details)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.select_details()
                return True
        return super(PowerListItem, self).on_touch_down(touch)


class TabList(FloatLayout, MDTabsBase):
    """The engaged power supplies tab."""

    def surfacing(self, tab_text):
        pass

    def discover(self, tab_details, cnt=30):
        self.ids.ps_discovery_spinner.active = False
        for i in range(cnt):
            item = PowerListItem(text=T["co-ps-label-1"] + f" {i + 1:>2}")
            # Adding a button manually to the item
            # (and passing down the item handle).
            btn_to = RightSelectButton()
            btn_to.power__list_item = item
            item.add_widget(btn_to)

            item.ids.item_left.icon = "flash"
            item.tab__details = tab_details
            self.ids.ps_list.add_widget(item)


class TabDetails(FloatLayout, MDTabsBase):
    """The engaged power supply details tab."""

    def surfacing(self, tab_text):
        self.ids.pd_icon.icon = "earth"


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

    @staticmethod
    def select_tab(destination_tab):
        tabs = MDApp.get_running_app().root.ids.ps_tabs
        # Just like your on_release.
        tabs.tab_bar.parent.dispatch(
            "on_tab_switch",
            destination_tab,
            destination_tab.tab_label,
            md_icons[destination_tab.text],
        )
        tabs.tab_bar.parent.carousel.load_slide(destination_tab)

    def build(self):
        global T
        T = co_lang.LANG["EN"]
        store = JsonStore("co_T.json")
        if store.exists("co-lang"):
            lng = store.get("co-lang")["name"]
            T = co_lang.LANG[lng]

        return Builder.load_file("main.kv")

    def on_start(self):
        self.theme_cls.primary_palette = "Gray"
        # self.theme_cls.primary_hue = '900'

        self.menu_lang_append()
        text = "flash"
        tab_list = TabList(text=text)
        self.power__supply_list = tab_list
        tab_list.surfacing(text)
        self.root.ids.ps_tabs.add_widget(tab_list)

        tab_details = TabDetails(text="equalizer")
        self.power__supply_details = tab_details
        self.root.ids.ps_tabs.add_widget(tab_details)
        tab_list.ids.ps_discovery_spinner.active = True
        Clock.schedule_once(lambda dt: tab_list.discover(tab_details), 5)

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

    def discovery_request(self, icon):
        tab_list = self.power__supply_list
        tab_list.ids.ps_list.clear_widgets()

        Contero.select_tab(tab_list)

        tab_list.ids.ps_discovery_spinner.active = True
        tab_details = self.power__supply_details
        Clock.schedule_once(lambda dt: tab_list.discover(tab_details, 5), 2)


Contero().run()
