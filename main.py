from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.icon_definitions import md_icons


class TabMain(FloatLayout, MDTabsBase):
    """The discovery tab."""

    def surfacing(self, tab_text):
        self.ids.icon.icon = "eye"


class TabList(FloatLayout, MDTabsBase):
    """The engaged power supplies tab."""

    def surfacing(self, tab_text):
        self.ids.icon.icon = "flash"


class TabDetails(FloatLayout, MDTabsBase):
    """The engaged power supply details tab."""

    def surfacing(self, tab_text):
        self.ids.icon.icon = "details"


class Contero(MDApp):
    def build(self):
        return Builder.load_file("main.kv")

    def on_start(self):
        text = "eye"
        main = TabMain(text=text)
        main.surfacing(text)
        self.root.ids.android_tabs.add_widget(main)
        self.root.ids.android_tabs.add_widget(TabList(text="flash"))
        self.root.ids.android_tabs.add_widget(TabDetails(text="details"))

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        """

        instance_tab.surfacing(tab_text)


Contero().run()
