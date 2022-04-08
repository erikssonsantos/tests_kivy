from kivymd.app import MDApp
from mixinmain import MixinMain
import config
import rootwidget
from kivy.properties import BooleanProperty


class MainApp(MDApp, MixinMain):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.borderless_status = BooleanProperty(config.borderless_status)

    def build(self):
        return rootwidget.RootWidget()


if __name__ == '__main__':
    mainapp = MainApp()
    mainapp.title = 'Config'
    mainapp.run()
