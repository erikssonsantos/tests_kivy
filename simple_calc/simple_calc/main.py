from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config


# Config.set("kivy", "keyboard_mode", 'dock')


kv_0 = """
#:import utils kivy.utils


<RootWidget>:
    
    orientation: 'vertical'
    
    
    StackLayout:
        # orientation: 'tb-lr'
        pos_hint: {'center_x': .5, 'y': .6}
        size_hint: .8, .6
        spacing: 5
        
        
        MDLabel:
            # pos_hint: {'center_x': .5, 'center_y': .2}
            # size_hint: 1, 1
            # minimum_height: 40
            # size_hint_x: 1
            id: id_resultado
            text: ''
            bold: True
            font_size: '35dp'
            size: self.texture_size
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
        
        MDTextFieldCustom:
            hint_text: "Quantidade de aulas"
            id: id_aulas
        MDTextFieldCustom:
            hint_text: "Quantidade de faltas"
            id: id_faltas
        MDRaisedButton:
            text: 'Calcular'
            on_release: root.simple_calc()
            font_size: '30dp'
            # size_hint_x: 1
            # size_hint_y: 1


<MDTextFieldCustom@MDTextField>:
    mode: "rectangle"
    max_text_length: 2
    input_filter: 'int'
    font_size: '40dp'
    halign: 'center'
    required: False
    helper_text_mode: "on_error"
    helper_text: ""
    multiline: False
    input_type: 'number'
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
                infrequendia = faltas / aulas * 100
                frequencia = int(100 - infrequendia)
                if frequencia < 75:
                    self.ids.id_resultado.text = f'Aluno com [color=FF0000]{frequencia}%[/color] de presença.'
                else:
                    self.ids.id_resultado.text = f'Aluno com [color=026A55]{frequencia}%[/color] de presença.'
        except:
            self.ids.id_resultado.text = "Valores não aceitáveis."    


class RootWidget(MixinRootWidget, MDFloatLayout):
    pass


class MixinMain(object):
    pass


class MainApp(MDApp, MixinMain):
    
    Window.softinput_mode = "below_target" # ['', 'below_target', 'pan', 'scale', 'resize'] comportamento do teclado do android
    
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        
        Builder.load_string(kv_0)
        self.theme_cls.primary_palette = "DeepPurple"
    
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    mainapp = MainApp()
    mainapp.title = 'Cálculo de frequência'
    mainapp.icon = r'icon.png'
    mainapp.run()
