from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.icon_definitions import md_icons


class TabMain(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class TabList(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class TabDetails(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class Example(MDApp):
    def build(self):
        return Builder.load_file("main_a.kv")

    def on_start(self):
        self.root.ids.android_tabs.add_widget(TabMain(text="*TabMain*"))
        self.root.ids.android_tabs.add_widget(TabList(text="*TabList*"))
        self.root.ids.android_tabs.add_widget(TabDetails(text="*TabDetails*"))

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''

        instance_tab.ids.label.text = tab_text


Example().run()
