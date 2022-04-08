from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
import mixinrootwidget


class RootWidget(mixinrootwidget.MixinRootWidget, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        

    def _trigger_layout(self, *args, **kwargs):
        super(RootWidget, self).do_layout()
        
        width, height = Window.size

        


