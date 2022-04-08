from kivymd.app import MDApp
from mixinmain import MixinMain
import rootwidget


class MainApp(MDApp, MixinMain):

    def build(self):
        return rootwidget.RootWidget()


if __name__ == '__main__':
    mainapp = MainApp()
    mainapp.title = 'Cálculo de frequência'
    mainapp.icon = r'icon.png'
    mainapp.run()
