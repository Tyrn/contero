"""
Power supply manager for Linux and Android.
"""
import kivy

kivy.require("2.2.1")
import gc
import sys
import weakref
from math import sin

import co_lang
from co_lang import T
from co_utils import rand_mac
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.utils import platform
from kivy_garden.graph import MeshStemPlot
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.tab import MDTabsBase

ACTION_ICON = "eye"


XMAX = 100


def power_readings():
    """Returns a provider of the next input data value."""
    chain = [sin(x / (XMAX * 0.1)) * 0.1 + 0.6 for x in range(0, XMAX + 1)]
    cnt = 0

    def next():
        nonlocal chain, cnt
        next_reading = chain[cnt % len(chain)]
        cnt += 1
        return next_reading

    return next


def power_points():
    """Returns a provider of the next renderable points set."""
    next_reading = power_readings()
    stretch = []

    def next():
        nonlocal stretch, next_reading
        stretch.append(next_reading())
        if len(stretch) > XMAX + 1:
            stretch.pop(0)
        x = XMAX + 1 - len(stretch)
        points = []
        for y in stretch:
            points.append((x, y))
            points.append((x, 0))
            x += 1
        return points

    return next


# class PowerPlot(ObjectProperty):
#    """Intended as a ListItem property."""
#    def __init__(self, **kwargs):
#        super(PowerPlot, self).__init__(**kwargs)
class PowerPlot:
    """Intended as a ListItem property."""

    def __init__(self):
        self._plot = MeshStemPlot(color=[1, 0, 1, 0.5])
        self._next_points = power_points()

    def __del__(self):
        print("*** *** PowerPlot.__del__ *** ***")

    def remove_all_plots(self):
        common_graph = MDApp.get_running_app().root.ids.graph_test
        for plot in common_graph.plots:
            common_graph.remove_plot(plot)

    def select_plot(self):
        self.remove_all_plots()
        common_graph = MDApp.get_running_app().root.ids.graph_test
        common_graph.add_plot(self._plot)

    def start_plot(self):
        self.get_next_points()
        Clock.schedule_interval(self.get_next_points, 3.0)

    def stop_plot(self):
        self.remove_all_plots()
        Clock.unschedule(self.get_next_points)

    def get_next_points(self, dt=None):
        self._plot.points = self._next_points()


class PowerGrid(GridLayout):
    """Layout containing a Graph."""


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    """Custom right container."""


class RightSelectButton(IRightBodyTouch, MDIconButton):
    """Custom right container."""

    def on_release(self):
        self.wm_select_details()()
        # .select_details()


class PowerListItem(TwoLineAvatarIconListItem, PowerPlot):
    """The engaged power supply item."""

    def select_details(self):
        ids = MDApp.get_running_app().root.ids
        ids.pd_main_label.text = self.text + f",  {T('co-output-current-l')}"
        ids.pd_mac_label.text = self.secondary_text
        self.select_plot()
        Contero.select_tab(ids.ps_tab_details)

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

    def discover(self, tab_details, cnt):
        ids = MDApp.get_running_app().root.ids
        ids.ps_toolbar.animate_action_button = False
        ids.pd_main_label.text = T("co-no-ps-selected")
        ids.pd_mac_label.text = ""
        for i in range(cnt):
            item = PowerListItem(
                text=T("co-ps-label-1") + f" {i + 1:>2}", secondary_text=rand_mac()
            )
            # item.details__plot = PowerPlot()
            item.start_plot()
            # Adding a button manually to the item
            # (and passing down the item handle).
            btn_to = RightSelectButton()
            btn_to.wm_select_details = weakref.WeakMethod(item.select_details)
            item.add_widget(btn_to)

            item.ids.item_left.icon = "flash"
            ids.ps_list.add_widget(item)


def trace_inhouse_events():
    events = Clock.get_events()
    for i, event in enumerate(events):
        junk = f"{event}"
        if (
            junk.find("get_next_points") >= 0
            or junk.find("animate_await") >= 0
            or junk.find("discover") >= 0
        ):
            print(f"({i}) Event (on_tab_switch): {event}")


class TabDetails(FloatLayout, MDTabsBase):
    """The engaged power supply details tab."""

    def surfacing(self, tab_text):
        trace_inhouse_events()


class Contero(MDApp):
    menu_main = ObjectProperty()

    def menu_main_open(self, button):
        self.menu_main.caller = button
        self.menu_main.open()

    about_dialog = ObjectProperty()

    def about_dialog_close(self, *args):
        self.about_dialog.dismiss(force=True)

    def menu_item_about_callback(self, text):
        self.menu_main.dismiss()
        self.about_dialog = MDDialog(
            title=T("co-app-name"),
            size_hint=(0.8, 0.3),
            text=T("co-app-running-on") + f" {platform}, {sys.byteorder}-endian",
            buttons=[
                MDFlatButton(
                    text=T("co-close-button"),
                    on_release=self.about_dialog_close,
                ),
            ],
        )
        self.about_dialog.open()

    def menu_main_build(self):
        items = [
            {
                "viewclass": "OneLineListItem",
                "text": T("co-about"),
                "height": dp(48),
                "on_release": lambda x=T("co-about"): self.menu_item_about_callback(x),
            }
        ]
        self.menu_main = MDDropdownMenu(
            width_mult=3,
            items=items,
            caller=self.root.ids.ps_toolbar.ids.right_actions.children[2],
        )

    menu_lang = ObjectProperty()

    def menu_locale_open(self, button):
        self.menu_lang.caller = button
        self.menu_lang.open()

    def menu_item_lang_callback(self, lng):
        self.menu_lang.dismiss()
        co_lang.set_language(lng)
        store = JsonStore("co_T.json")
        store.put("co-lang", name=lng)

    def menu_locale_build(self):
        items = []
        for lng in co_lang.languages():
            items.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": lng,
                    "height": dp(48),
                    "on_release": lambda x=lng: self.menu_item_lang_callback(x),
                }
            )
        self.menu_lang = MDDropdownMenu(
            width_mult=2,
            items=items,
            caller=self.root.ids.ps_toolbar.ids.right_actions.children[1],
        )

    @staticmethod
    def select_tab(destination_tab):
        tabs = MDApp.get_running_app().root.ids.ps_tabs
        # Just like your on_release.
        tabs.tab_bar.parent.dispatch(
            "on_tab_switch",
            destination_tab,
            destination_tab.tab_label,
            "Tab Text",
        )
        tabs.tab_bar.parent.carousel.load_slide(destination_tab)

    def pulse_icon_counter(self):
        icons = "reply", "reply-all"
        i = 0

        def next():
            nonlocal icons, i
            icon = icons[i % len(icons)]
            i += 1
            return icon

        return next

    def animate_await(self):
        toolbar = MDApp.get_running_app().root.ids.ps_toolbar
        if toolbar.animate_action_button:
            toolbar.icon = toolbar.next_icon()
            return True
        toolbar.icon = ACTION_ICON
        return False

    def build(self):
        co_lang.set_language("EN")
        store = JsonStore("co_T.json")
        if store.exists("co-lang"):
            lng = store.get("co-lang")["name"]
            co_lang.set_language(lng)

        return Builder.load_file("main.kv")

    def on_start(self):
        self.theme_cls.primary_palette = "Gray"
        # self.theme_cls.primary_hue = '900'
        if platform != "android":
            self.root.ids.ps_tabs.lock_swiping = True

        def on_start(interval):
            self.menu_main_build()
            self.menu_locale_build()

        Clock.schedule_once(on_start)
        # Clock.schedule_once(lambda dt: self.discovery_request(30, 5), 5)

    def discovery_clean(self):
        for item in self.root.ids.ps_list.children:
            print(f"item: {item.text}")
            item.stop_plot()
        self.root.ids.ps_list.clear_widgets()
        self.root.ids.pd_main_label.text = T("co-no-ps-selected")
        self.root.ids.pd_mac_label.text = ""
        gc.collect()

    def discovery_request(self, item_count=9, delay=3):
        self.discovery_clean()

        tab_list = self.root.ids.ps_tab_list
        Contero.select_tab(tab_list)

        self.root.ids.ps_toolbar.animate_action_button = True
        self.animate_await()
        Clock.schedule_interval(lambda dt: self.animate_await(), 1.0)

        tab_details = self.root.ids.ps_tab_details
        Clock.schedule_once(
            lambda dt: tab_list.discover(tab_details, item_count), delay
        )

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
