from classes.process import Process

class CalculadoraDeTempos:
    @staticmethod
    def calculaTurnaroundTime(processo: Process):
        return processo.tempo_final - processo.t_chegada
    
    @staticmethod
    def calculaTempoNormalizado(processo: Process):
        return CalculadoraDeTempos.calculaTurnaroundTime(processo) / processo.t_total_execucao

