from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config


Config.set('graphics', 'resizable', '0')
Config.write()


class MainApp(MDApp):
    
    title = "Settings"
    Builder.load_file('main.kv')


if __name__ == '__main__':
    MainApp().run()
