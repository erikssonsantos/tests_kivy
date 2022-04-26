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
        size_hint: .9, .4
        pos_hint: {'center_x': .5, 'y': .27}
        hint_text: 'Resultados'
        multiline: True
        readonly: True
        line_anim: False
        active_line: False
        mode: "rectangle"
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
        size_hint: .9, .14
        hint_text: 'Expressão'
        pos_hint: {'center_x': .5, 'y': .11}
        line_anim: False
        active_line: False
        # input_filter: 'int'
        # multiline: True
        # input_type: 'number'
        font_size: '20sp'
        # mode: "fill"
        # max_height: "200dp"
        on_text_validate: root.clock_calc()
    
    MDRaisedButton:
        id: id_botao_calc
        name: 'name_botao_calc'
        #icon: "arrow-right-bold"
        text: 'calc'
        size_hint: .1, .09
        pos_hint: {"center_x": .5, "y": .01}
        on_press: root.clock_calc()
    
    CustomMDCheckbox:
        id: id_check_permitir_expressao_repetida
        name: 'name_check_permitir_expressao_repetida'
        pos_hint: {"x": .1, "y": .05}
        active: False


<CustomMDCheckbox@MDCheckbox>:
    # group: 'grupo_formato'
    size_hint: None, None
    size: dp(48), dp(48)

"""
    
    
    import kivy
    kivy.require('2.1.0')
    
    from kivymd.app import MDApp
    from kivy.core.window import Window
    from kivy.lang import Builder
    from kivymd.uix.floatlayout import MDFloatLayout
    from kprimes import *
    from time import time
    import threading
    from kivy.clock import Clock
    
    class MixinRootWidget(object):
    
        def atualizar_text_resultados(self, text_novo='', caso=''):
            if caso == 'novas_vars':
                self.ids.id_resultados.text = f'{self.ids.id_resultados.text}\n{f"{text_novo}"}: {globals()[text_novo]}' # altera gráfico
            elif caso == 'caso_padrao':
                self.ids.id_resultados.text = f'{self.ids.id_resultados.text}\n{f"r{text_novo}"}: {self.resultado, self.expressao, self.tempo_de_execucao}' # altera gráfico
            elif caso == 'erro_padrao':
                self.ids.id_resultados.text = f'{self.ids.id_resultados.text}\nERRO: "{self.expressao}"' # altera gráfico
        
        def clock_calc(self):
            
            self.event_calc = Clock.schedule_once(self.thread_calc, 0)
            self.event_ordens = Clock.schedule_interval(self.alterar_ordens, .5)
        
        def alterar_ordens(self, *args):
            
            if self.ordens['calc'] == 0:
                
                self.event_ordens.cancel()
                self.calc_finalizado = False
                
                if self.ordens['show_novas_vars'][0] == 1:
                    for i in self.novas_vars:
                        self.atualizar_text_resultados(i, 'novas_vars')
                    self.ordens['show_novas_vars'][0] = 0
                    self.calc_finalizado = True
                elif self.ordens['show_caso_padrao'][0] == 1:
                    self.atualizar_text_resultados(self.key_resultado, 'caso_padrao')
                    self.ordens['show_caso_padrao'][0] = 0
                    self.calc_finalizado = True
                elif self.ordens['show_erro_padrao'][0] == 1:
                    self.atualizar_text_resultados('erro_padrao')
                    self.ordens['show_erro_padrao'][0] = 0
                    self.calc_finalizado = True
                elif self.ordens['expressao_vazia'] == 1:
                    self.ordens['expressao_vazia'] = 0
                    self.calc_finalizado = True
            
            if self.calc_finalizado:
                self.event_calc.cancel()
                # self.resultado = None
                self.expressao_repetida = False
                self.permitir_expressao_repetida = False
                self.tempo_de_execucao = 0
                self.tempo_inicial = 0
                self.tempo_final = 0
                self.novas_vars = []
                self.key_resultado = ''
                self.ids.id_botao_calc.disabled = False
                self.ids.id_expressao.readonly = False
                
        
        def thread_calc(self, *args):
            
            self.task_calc = threading.Thread(target = self.calc)
            self.ordens['calc'] = 1
            self.ids.id_botao_calc.disabled = True
            self.ids.id_expressao.readonly = True
            self.task_calc.start()
            
        def _core_calc(self):
            try:
                for k, v in self.resultados_historico.items(): exec(f'{k}={v[0]}') # não lembro qual é a lógica dessa linha kk
                self.resultado = eval(self.expressao)
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
        
        def calc(self):
            
            self.expressao = self.ids.id_expressao.text
            
            palavra_proibida = False
            if 'exec' in self.expressao or 'eval' in self.expressao or 'system' in self.expressao or 'os' in self.expressao:
                palavra_proibida = True
            else:
                palavra_proibida = False
            
            expressoes_temp = []
            
            for i in self.resultados_historico.values():
                expressoes_temp.append(i[1])
                
            if self.expressao in expressoes_temp:
                self.expressao_repetida = True
            
            if self.ids.id_check_permitir_expressao_repetida.active:
                self.permitir_expressao_repetida = True
                
            
            
            self.tempo_inicial = time()
            
            if not palavra_proibida:
                print(self.expressao_repetida, self.permitir_expressao_repetida)
                if bool(self.expressao_repetida) or len(expressoes_temp) == 0: print('caso 1') # mistério do if assombrado
                else:
                    ...
                    '''
                    if self.permitir_expressao_repetida:
                        self._core_calc()
                    '''
                    
            del expressoes_temp
            
            self.tempo_final = time()
            self.tempo_de_execucao = self.tempo_final - self.tempo_inicial
            
            if not palavra_proibida:
                if self.expressao_valida:
                    
                    if self.expressao == '':
                        self.ordens['expressao_vazia'] = 1
                    
                    elif self.resultado != None:
                        
                        try:
                            if len(self.resultados_historico) == 0: self.key_resultado = 0
                            else: self.key_resultado = len(self.resultados_historico)
                        except:
                            self.key_resultado = 0
                        self.resultados_historico[f'r{self.key_resultado}'] = self.resultado, self.expressao, self.tempo_de_execucao
                        self.ordens['show_caso_padrao'][0] = 1
                        
                elif not self.expressao_valida:
                    if self.expressao != '':
                        self.ordens['show_erro_padrao'][0] = 1
            else:
                self.ordens['show_erro_padrao'][0] = 1
            
            
            self.ordens['calc'] = 0
    
    
    class RootWidget(MDFloatLayout, MixinRootWidget):
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            
            self.expressao = ''
            self.resultado = None
            self.resultados_historico = {}
            self.expressao_valida = False
            self.expressao_repetida = False
            self.permitir_expressao_repetida = False
            self.novas_vars = []
            self.event_calc = None
            self.task_calc = None
            self.tempo_de_execucao = 0
            self.tempo_inicial = 0
            self.tempo_final = 0
            self.key_resultado = ''
            self.ordens = {
                'show_novas_vars': [0,[]], 
                'show_caso_padrao': [0,[]], 
                'show_erro_padrao': [0,[]],
                'expressao_vazia':0,
                'calc': 0
                }
            self.calc_finalizado = False
    
    
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
