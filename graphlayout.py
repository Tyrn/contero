from math import sin
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.widget import Widget
from kivy_garden.graph import Graph, MeshLinePlot


class SetGraph(Widget):
    def update_graph(self):
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.0)) for x in range(0, 101)]
        self.ids.graph_test.add_plot(plot)


class GraphLayoutApp(App):
    def build(self):
        disp = SetGraph()
        disp.update_graph()
        return disp


if __name__ == "__main__":
    GraphLayoutApp().run()
