from rich.console import Console

class Cpu():
    def __init__(self,id, filas_qtd, dispatcher):
        self.id = id
        self.processo = None
        self.filas_qtd = filas_qtd
        self.filaAtual = None
        self.dispatcher = dispatcher
        self.logRemanescente = None
        self.console = Console()
        
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
            self.console.print(self.logRemanescente)
            self.logRemanescente = None
        return

    def executar_processo(self):
        if self.processo is not None:
            self.processo.executar()
            if self.processo.finalizado:
                self.dispatcher.organizar_finalizados(self.processo)
                self.processo = None
            elif self.processo.bloqueado:
                self.dispatcher.organizar_bloqueados(self.processo)

                self.logRemanescente = f"Processo {self.processo.identificador} foi bloqueado"
                self.processo = None
            elif self.processo.contador_quantum == self.processo.quantum:
                self.processo.preempcao() # ! Se o processo atingiu o quantum, ele é interrompido por fatia de tempo
                if (self.filaAtual + 1) < self.filas_qtd:
                    self.dispatcher.organizar_prontos(self.processo, (self.filaAtual + 1) % (self.filas_qtd)) # ! Após preempção, o processo vai para a fila de prontos seguinte
                else:
                    self.dispatcher.organizar_prontos(self.processo, self.filaAtual)
                self.logRemanescente = f"Processo {self.processo.identificador} foi interrompido por fatia de tempo"
                self.processo = None
        return
