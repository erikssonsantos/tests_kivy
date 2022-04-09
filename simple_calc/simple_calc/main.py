from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


kv_0 = """
<RootWidget>:
    
    size_hint: 1, 1
    orientation: 'vertical'

    MDBoxLayout:
        size_hint: 1, 1
        orientation: 'vertical'
        padding: [20,20,20,20]
        spacing: 10

        MDLabel:
            id: id_resultado
            text: ''
            size: self.texture_size
            text_size: self.size
            halign: 'center'
            valign: 'center'

        MDTextField:
            hint_text: "Quantidade de aulas"
            mode: "rectangle"
            id: id_aulas
        MDTextField:
            hint_text: "Quantidade de faltas"
            mode: "rectangle"
            id: id_faltas

        MDBoxLayout:
            size_hint: 1, 1
            orientation: 'horizontal'
            MDBoxLayout:
            MDRaisedButton:
                text: 'Calcular'
                on_release: root.simple_calc()
            MDBoxLayout:
"""


class MixinRootWidget(object):

    def simple_calc(self):

        aulas = self.ids.id_aulas.text
        faltas = self.ids.id_faltas.text
        
        try:
            aulas = int(aulas)
            faltas = int(faltas)
            if faltas > aulas:
                self.ids.id_resultado.text = "Valores não aceitáveis."
            else:
                self.ids.id_resultado.text = f'Aluno com {int(100 - (faltas / aulas * 100))}% de frequência.'
        except:
            self.ids.id_resultado.text = "Valores não aceitáveis."    


class RootWidget(MixinRootWidget, BoxLayout):
    ...


class MixinMain(object):
    ...


class MainApp(MDApp, MixinMain):
    
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        
        Builder.load_string(kv_0)
        self.root_widget = RootWidget()
        self.theme_cls.primary_palette = "DeepPurple"
    
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    mainapp = MainApp()
    mainapp.title = 'Cálculo de frequência'
    mainapp.icon = r'icon.png'
    mainapp.run()
