# ! Classe responsável por organizar os processos nas filas de prontos, bloqueados e finalizados
class Dispatcher():
    def __init__(self, filas, fila_bloqueados, bloqueados_em_execucao, fila_de_finalizados, memoria):
        self.filas = filas
        self.fila_bloqueados = fila_bloqueados
        self.fila_de_finalizados = fila_de_finalizados
        self.bloqueados_em_execucao = bloqueados_em_execucao

        self.fila_temp_bloqueados = []
        self.fila_temp_finalizados = []
        self.fila_temp_prontos = []
        self.memoria = memoria


        for fila in self.filas:
            self.fila_temp_prontos.append([])


    def remover_bloqueado(self, processo):
        if processo in self.fila_bloqueados:
            self.fila_bloqueados.remove(processo)

    def remover_bloqueado_em_execucao(self, processo):
        if processo in self.bloqueados_em_execucao:
            self.bloqueados_em_execucao.remove(processo)

    def organizar_bloqueados(self, processo):
        self.fila_temp_bloqueados.append(processo)	

    def organizar_finalizados(self, processo):
        self.fila_temp_finalizados.append(processo)

    def organizar_prontos(self, processo, index_fila):
        self.fila_temp_prontos[index_fila].append(processo)

    def despachar_bloqueados(self): # ! Organiza os processos na fila de bloqueados considerando que os processos com menor tempo restante de execução ganharão prioridade de acesso ao disco
        fila_temp_bloqueados_SPN = sorted(self.fila_temp_bloqueados, key=lambda x: (x.t_disco + x.t_execucao_fase_2))
        for processo in fila_temp_bloqueados_SPN:
            self.fila_bloqueados.append(processo)
        self.fila_temp_bloqueados = []

    
    def despachar_finalizados(self):
        for processo in self.fila_temp_finalizados:
            self.memoria.finalizar_processo(processo)
            self.fila_de_finalizados.append(processo)
        self.fila_temp_finalizados = []

    def despachar_prontos(self):
        fila_prontos_SPN = []
        for fila in self.fila_temp_prontos:
            fila_prontos_SPN.append(sorted(fila, key=lambda x: x.t_total_execucao)) # ! Organiza os processos nas filas de prontos considerando que os processos com menor tempo total de execução ganharão prioridade de acesso à CPU

        for i in range(len(fila_prontos_SPN)):
            for processo in fila_prontos_SPN[i]:
                self.filas[i].append(processo)
            self.fila_temp_prontos[i] = []
