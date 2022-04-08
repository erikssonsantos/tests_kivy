from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
import config


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        

    def _trigger_layout(self, *args, **kwargs):
        super(RootWidget, self).do_layout()
        
        width, height = Window.size

        if width > config.MAX_WIDTH:
            Window.size = config.MAX_WIDTH, Window.size[1]
        if height > config.MAX_HEIGHT:
            Window.size = Window.size[0], config.MAX_HEIGHT

        if width < config.MIN_WIDTH:
            Window.size = config.MIN_WIDTH, Window.size[1]
        if height < config.MIN_HEIGHT:
            Window.size = Window.size[0], config.MIN_HEIGHT

