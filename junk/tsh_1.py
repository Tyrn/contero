from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ListProperty, NumericProperty

KV = """
#:import RGBA kivy.utils.rgba

<Row@BoxLayout>:
    text: ''
    rv_key: 0

    CheckBox:
        active: root.rv_key in app.current_selection
        on_active: app.select_row(root.rv_key, self.active)

    Label:
        text: root.text

FloatLayout:
    RecycleView:
        size_hint: .8, .8
        pos_hint: {'center': (.5, .5)}
        data: app.data
        viewclass: 'Row'

        canvas.before:
            Color:
                rgba: RGBA('#212121')

            Rectangle:
                pos: self.pos
                size: self.size

        RecycleBoxLayout:
            orientation: 'vertical'
            size: self.minimum_size
            size_hint_y: None
            default_size_hint: 1, None
            default_size: 0, 50
"""


class TestApp(App):
    data = ListProperty()
    current_selection = ListProperty([])

    def build(self):
        self.data = [dict(text="key {}".format(i), rv_key=i,) for i in range(100)]
        return Builder.load_string(KV)

    def select_row(self, rv_key, active):
        if active and rv_key not in self.current_selection:
            self.current_selection.append(rv_key)
        elif not active and rv_key in self.current_selection:
            self.current_selection.remove(rv_key)


if __name__ == "__main__":
    TestApp().run()
