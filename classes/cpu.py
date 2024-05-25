class Cpu():
    def __init__(self,id, fila_0, fila_1, fila_2, fila_3, fila_bloqueados, fila_de_finalizados):
        self.id = id
        self.processo = None
        self.fila_0 = fila_0
        self.fila_1 = fila_1
        self.fila_2 = fila_2
        self.fila_3 = fila_3
        self.filaAtual = None
        self.fila_de_finalizados = fila_de_finalizados

        self.filas = [self.fila_0, self.fila_1, self.fila_2, self.fila_3]
        self.fila_bloqueados = fila_bloqueados
        
    def __str__(self):
        return f'CPU {self.id}'
    
    def obter_processo(self):
        return self.processo
    
    def escalonar_processo(self, processo, filaAtual):
        self.processo = processo
        self.filaAtual = filaAtual
        return

    def executar_processo(self):
        if self.processo is not None:
            self.processo.executar()
            if self.processo.finalizado:
                self.fila_de_finalizados.append(self.processo)
                self.processo = None
            elif self.processo.bloqueado:
                self.fila_bloqueados.append(self.processo)
                self.processo = None
            elif self.processo.contador_quantum == self.processo.quantum:
                self.processo.preempcao()
                self.filas[(self.filaAtual + 1) % (len(self.filas))].append(self.processo)
                self.processo = None
        return
