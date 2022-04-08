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
