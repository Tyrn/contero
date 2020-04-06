"""Real time plotting of Microphone level using kivy
"""

import sys

if len(sys.argv) > 1:
    from kivy.app import App
else:
    from kivymd.app import MDApp as App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.graph import LinePlot
from kivy.clock import Clock
from math import sin


XMAX = 10


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
            x += 1
        return points

    return next


next_points = power_points()


class Logic(BoxLayout):
    def __init__(self, **kwargs):
        super(Logic, self).__init__(**kwargs)
        self.plot = LinePlot(line_width=3, color=[1, 0, 0, 1])

    def start(self):
        self.ids.graph.add_plot(self.plot)
        self.get_value()
        Clock.schedule_interval(self.get_value, 30.0 / XMAX)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt=None):
        self.plot.points = next_points()


class RealTimeMicrophone(App):
    def build(self):
        return Builder.load_file("graphlayout.kv")


if __name__ == "__main__":
    RealTimeMicrophone().run()
