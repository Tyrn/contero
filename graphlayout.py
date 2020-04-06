"""Real time plotting of Microphone level using kivy
"""

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.graph import LinePlot
from kivy_garden.graph import MeshLinePlot
from kivy_garden.graph import MeshStemPlot
from kivy_garden.graph import SmoothLinePlot
from kivy.clock import Clock
from math import sin


POINTS = [(x, sin(x / 1.0) * .3 + .5) for x in range(0, 11)]


def shift(points):
    global POINTS
    res = []

    for x, y in POINTS:
        res.append((x + 1.0, y))
    x, y = res.pop()
    res.insert(0, (0, y))
    POINTS = res
    return res


class Logic(BoxLayout):
    def __init__(self, **kwargs):
        super(Logic, self).__init__(**kwargs)
        self.plot = LinePlot(line_width=3, color=[1, 0, 0, 1])
        #self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        #self.plot = MeshStemPlot(color=[1, 0, 0, 1])
        #self.plot = SmoothLinePlot(color=[1, 0, 0, 1])

    def start(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 1.0)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        self.plot.points = shift(POINTS)


class RealTimeMicrophone(App):
    def build(self):
        return Builder.load_file("graphlayout.kv")


if __name__ == "__main__":
    RealTimeMicrophone().run()
