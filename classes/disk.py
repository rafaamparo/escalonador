class Disk():
    def __init__(self, id, dispatcher):
        self.id = id
        self.dispatcher = dispatcher
        self.processo = None
        self.logRemanescente = None
        

    def __str__(self):
        return f'DISCO {self.id}'

    def obter_processo(self):
        return self.processo

    def escalonar_processo(self, processo):
        self.processo = processo
        return

    def remanescente(self):
        if self.logRemanescente is not None:
            print(self.logRemanescente)
            self.logRemanescente = None
        return

    def executar(self):
        if self.processo is not None:
            self.processo.executar_disco()
            if self.processo.pronto == True:
                self.logRemanescente = f'Processo {self.processo.id} foi desbloqueado'
                self.dispatcher.remover_bloqueado(self, self.processo)
                self.dispatcher.organizar_prontos(self, 0)
                self.processo = None
        return
