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
            
            palavra_proibida = False
            if 'exec' in self.expressao or 'eval' in self.expressao or 'system' in self.expressao or 'os' in self.expressao:
                palavra_proibida = True
            
            expressoes_temp = []
            
            for i in self.resultados_historico.values():
                expressoes_temp.append(i[1])
            
            if self.expressao in expressoes_temp:
                self.expressao_repetida = True
            elif palavra_proibida:
                ...
            else:
                try:
                    for k, v in self.resultados_historico.items(): exec(f'{k}={v[0]}')
                    self.resultados = eval(self.expressao)
                    self.expressao_valida = True
                except:
                    try:
                        globals_temp_1 = tuple(globals().keys())
                        exec(self.expressao, globals(), globals())
                        globals_temp_2 = tuple(globals().keys())
                        self.novas_vars = list(filter(lambda x: x not in globals_temp_1, globals_temp_2))
                        self.novas_vars = list(filter(lambda x: x != 'globals_temp_1', self.novas_vars))
                        del globals_temp_1
                        del globals_temp_2
                        self.expressao_valida = True
                    except:
                        self.expressao_valida = False
            
            del expressoes_temp
            
            if not palavra_proibida:
                if self.expressao_valida and not self.expressao_repetida:
                    
                    if len(self.novas_vars) > 0:
                        for i in self.novas_vars:
                            self.ids.id_resultados.text = f'{self.ids.id_resultados.text}\n{f"{i}"}: {globals()[i]}'
                    
                    if self.resultados != None:
                        key_resultado = None
                        try:
                            if len(self.resultados_historico) == 0: key_resultado = 0
                            else: key_resultado = len(self.resultados_historico)
                        except:
                            key_resultado = 0
                        self.resultados_historico[f'r{key_resultado}'] = self.resultados, self.expressao
                        self.ids.id_resultados.text = f'{self.ids.id_resultados.text}\n{f"r{key_resultado}"}: {self.resultados, self.expressao}'
                        
                elif not self.expressao_valida and not self.expressao_repetida:
                    if self.expressao != '':
                        self.ids.id_resultados.text = f'{self.ids.id_resultados.text}\nERRO: "{self.expressao}"'
            else:
                self.ids.id_resultados.text = f'{self.ids.id_resultados.text}\nERRO: "{self.expressao}"'
            
            
            self.resultados = None
            self.expressao_repetida = False
            self.novas_vars = []
    
    
    class RootWidget(MDFloatLayout, MixinRootWidget):
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            
            self.expressao = ''
            self.resultados = None
            self.resultados_historico = {}
            self.expressao_valida = False
            self.expressao_repetida = False
            self.novas_vars = []
    
    
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



# TODO: conseguir atualizar valor de variavel personalizada
# TODO: especificar os erros das expressões através de estilização
