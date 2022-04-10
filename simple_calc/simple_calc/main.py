from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


kv_0 = """
<RootWidget>:
    
    size_hint: 1, 1
    orientation: 'vertical'

    MDLabel:
        size_hint: 1, .6
        id: id_resultado
        text: ''
        size: self.texture_size
        text_size: self.size
        halign: 'center'
        valign: 'center'

    MDBoxLayout:
        size_hint: 1, 1
        orientation: 'vertical'
        padding: [20,2,20,2]
        spacing: 1

        MDTextFieldCustom:
            hint_text: "Quantidade de aulas"
            id: id_aulas
        MDTextFieldCustom:
            hint_text: "Quantidade de faltas"
            id: id_faltas

        MDBoxLayout:
            size_hint: 1, 1
            orientation: 'horizontal'
            MDBoxLayout:
            MDRaisedButton:
                text: 'Calcular'
                on_release: root.simple_calc()
            MDBoxLayout:
    MDBoxLayout:
        size_hint: 1, .8

<MDTextFieldCustom@MDTextField>:
    mode: "rectangle"
    #size_hint_y: None
    #height: 44
    max_text_length: 2

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
    pass


class MixinMain(object):
    pass


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
