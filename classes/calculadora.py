from classes.process import Process

class CalculadoraDeTempos:
    def __init__(self, processo: Process):
        self.processo = processo
    
    def calculaTurnaroundTime(self):
        tq = self.processo.t_total_execucao - self.processo.t_chegada
        return tq
    
    def calculaTempoNormalizado(self):
        tn = self.calculaTurnaroundTime() / self.processo.t_total_execucao

