class Cpu():
    def __init__(self,id, filas_qtd, dispatcher):
        self.id = id
        self.processo = None
        self.filas_qtd = filas_qtd
        self.filaAtual = None
        self.dispatcher = dispatcher
        self.logRemanescente = None
        
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
                if (self.filaAtual + 1) < self.filas_qtd:
                    self.dispatcher.organizar_prontos(self.processo, (self.filaAtual + 1) % (self.filas_qtd))
                else:
                    self.dispatcher.organizar_prontos(self.processo, self.filaAtual)
                self.logRemanescente = f"Processo {self.processo.identificador} foi interrompido por fatia de tempo"
                self.processo = None
        return
