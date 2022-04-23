#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Elm Santos'
__version__ = '0.0.1'
__last_modification__ = '2022.04.22'


if __name__ == '__main__':
    
    kv_0 = """
#:import utils kivy.utils

<RootWidget>:

    MDTextField:
        id: id_resultados
        name: 'name_resultados'
        size_hint: .95, .7
        pos_hint: {'center_x': .5, 'y': .25}
        multiline: True
        readonly: True
        #canvas.before:
        #    Color:
        #        rgba: utils.get_color_from_hex('#ffffff')
        #    Rectangle:
        #        size: self.width, self.height
        #        pos: self.x, self.y
        
    MDTextField:
        id: id_expressao
        name: 'name_expressao'
        hint_text: ''
        size_hint: .9, .15
        pos_hint: {'center_x': .5, 'y': .11}
        # input_filter: 'int'
        # multiline: True
        # input_type: 'number'
        font_size: '20sp'
        # mode: "fill"
        # max_height: "200dp"
        on_text_validate: root.calc()
    
    MDRaisedButton:
        id: id_botao_calc
        name: 'name_botao_calc'
        #icon: "arrow-right-bold"
        text: 'calc'
        size_hint: .1, .1
        pos_hint: {"center_x": .5, "y": .01}
        on_press: root.calc()

"""
    
    
    import kivy
    kivy.require('2.1.0')
    
    from kivymd.app import MDApp
    from kivy.core.window import Window
    from kivy.lang import Builder
    from kivymd.uix.floatlayout import MDFloatLayout
    from kprimes import *
    
    
    class MixinRootWidget(object):
    
        def calc(self):
            
            self.expressao = self.ids.id_expressao.text
            try:
                self.resultados = eval(self.expressao)
                self.expressao_valida = True
            except:
                # self.resultados = None
                self.expressao_valida = False
                
            if self.expressao_valida:
                key_resultado = None
                try:
                    if len(self.resultados_historico) == 0: key_resultado = 0
                    else: key_resultado = len(self.resultados_historico)
                except:
                    key_resultado = 0
                self.resultados_historico[f'r{key_resultado}'] = self.resultados
                self.ids.id_resultados.text = f'{self.ids.id_resultados.text}\n{f"r{key_resultado}"}: {self.resultados, self.expressao}'
            elif not self.expressao_valida:
                if self.expressao != '':
                    self.ids.id_resultados.text = f'{self.ids.id_resultados.text}\nERRO: "{self.expressao}"'
            
                
            
            # print(self.resultados, self.expressao_valida)
    
    
    class RootWidget(MDFloatLayout, MixinRootWidget):
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            
            self.expressao = ''
            self.resultados = None
            self.resultados_historico = {}
            self.expressao_valida = None
    
    
    class MainApp(MDApp):
        
        Window.softinput_mode = "below_target"
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            
            Builder.load_string(kv_0)
            self.title = 'Simple Calc 2'
            self.theme_cls.theme_style="Light"
            self.theme_cls.primary_palette = 'Gray'
            self.theme_cls.primary_hue = "A700"
            # self.icon = r'icon.png'

        def build(self):
            return RootWidget()
    

    MainApp().run()


# TODO: prevenir que haja expressão idêntica
# TODO: pegar resultado apartir de chave do dicionáro de resultados


