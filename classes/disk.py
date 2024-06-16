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
            if self.processo.pronto == True or self.processo.suspenso_pronto == True: # ! Se o processo foi desbloqueado
                if (self.processo.disco_finalizado == False):
                    self.logRemanescente = f'Processo {self.processo.identificador} foi desbloqueado'
                    self.dispatcher.remover_bloqueado(self.processo)
                    self.dispatcher.remover_bloqueado_em_execucao(self.processo)
                    if (self.processo.pronto == True):
                        if (self.processo.t_execucao_fase_2 == 0):
                            self.processo.finalizar()
                            self.dispatcher.organizar_finalizados(self.processo)
                        else:
                            self.dispatcher.organizar_prontos(self.processo, 0) # ! Adiciona o processo na fila de prontos 0
                    self.processo.disco_finalizado = True
                self.processo = None
        return

