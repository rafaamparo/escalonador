class Cpu():
    def __init__(self,id, fila_0, fila_1, fila_2, fila_3, dispatcher):
        self.id = id
        self.processo = None
        self.fila_0 = fila_0
        self.fila_1 = fila_1
        self.fila_2 = fila_2
        self.fila_3 = fila_3
        self.filaAtual = None
        self.dispatcher = dispatcher
        self.logRemanescente = None

        self.filas = [self.fila_0, self.fila_1, self.fila_2, self.fila_3]
        
    def __str__(self):
        return f'CPU {self.id}'
    
    def obter_processo(self):
        return self.processo
    
    def escalonar_processo(self, processo, filaAtual):
        self.processo = processo
        self.filaAtual = filaAtual
        return

    def remanescente(self):
        if self.logRemanescente is not None:
            print(self.logRemanescente)
            self.logRemanescente = None
        return

    def executar_processo(self):
        if self.processo is not None:
            self.processo.executar()
            if self.processo.finalizado:
                self.dispatcher.organizar_finalizados(self.processo)

                self.logRemanescente = f"Processo {self.processo.identificador} foi finalizado"
                self.processo = None
            elif self.processo.bloqueado:
                self.dispatcher.organizar_bloqueados(self.processo)

                self.logRemanescente = f"Processo {self.processo.identificador} foi bloqueado"
                self.processo = None
            elif self.processo.contador_quantum == self.processo.quantum:
                self.processo.preempcao()
                if (self.filaAtual + 1) < len(self.filas):
                    self.dispatcher.organizar_prontos(self.processo, (self.filaAtual + 1) % (len(self.filas)))
                else:
                    self.dispatcher.organizar_prontos(self.processo, self.filaAtual)
                self.logRemanescente = f"Processo {self.processo.identificador} foi interrompido por fatia de tempo"
                self.processo = None
        return
