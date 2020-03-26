from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.list import ImageLeftWidget
from kivymd.icon_definitions import md_icons


class PowerListItem(OneLineListItem):
    """The engaged power supply item."""
    def on_release(self):
        print("on release")
    #def on_touch_down(self, touch):
    #    if self.collide_point(*touch.pos):
    #        #self.pressed = touch.pos
    #        # we consumed the touch. return False here to propagate
    #        # the touch further to the children.
    #        print(f"touched down at {touch.pos}")
    #        return True
    #    return super(PowerListItem, self).on_touch_down(touch)

    #def on_touch_up(self, touch):
    #    if self.collide_point(*touch.pos):
    #        # we consumed the touch. return False here to propagate
    #        # the touch further to the children.
    #        print(f"touched up at {touch.pos}")
    #        return True
    #    return super(PowerListItem, self).on_touch_up(touch)

    #def on_pressed(self, instance, pos):
    #    print("pressed at {pos}".format(pos=pos))


class TabList(FloatLayout, MDTabsBase):
    """The engaged power supplies tab."""

    def surfacing(self, tab_text):
        pass

    def discover(self):
        for i in range(30):
            self.ids.container.add_widget(
                PowerListItem(text=f"Power supply {i + 1:>4}")
            )


class TabDetails(FloatLayout, MDTabsBase):
    """The engaged power supply details tab."""

    def surfacing(self, tab_text):
        self.ids.icon.icon = "equalizer"


class Contero(MDApp):
    def build(self):
        return Builder.load_file("main.kv")

    def on_start(self):
        text = "flash"
        main = TabList(text=text)
        main.surfacing(text)
        self.root.ids.android_tabs.add_widget(main)
        Clock.schedule_once(lambda dt: main.discover(), 2)
        self.root.ids.android_tabs.add_widget(TabDetails(text="equalizer"))

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        """

        instance_tab.surfacing(tab_text)


Contero().run()
