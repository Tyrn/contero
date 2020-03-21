from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.icon_definitions import md_icons


class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


IS_ICO = True
TAB_N = 3


class Example(MDApp):
    icons = list(md_icons.keys())[15:30]

    def build(self):
        return Builder.load_file("main_b.kv" if IS_ICO else "main_a.kv")

    def on_start(self):
        if IS_ICO:
            for i, name_tab in enumerate(self.icons):
                if i >= TAB_N: break
                self.root.ids.android_tabs.add_widget(Tab(text=name_tab))
        else:
            for i in range(TAB_N):
                self.root.ids.android_tabs.add_widget(Tab(text=f"Tab {i}"))

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''

        if IS_ICO:
            count_icon = [k for k, v in md_icons.items() if v == tab_text]
            instance_tab.ids.icon.icon = count_icon[0]
        else:
            instance_tab.ids.label.text = tab_text


Example().run()
