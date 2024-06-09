# crie a classe Process com o tamanho do processo, o tempo de chegada e o tempo de execução

class Process:
    def __init__(self, id, t_chegada, t_execucao_fase_1, t_disco,  t_execucao_fase_2,  tamanho, qtd_discos, dispatcher, quantum=3):
        self.identificador = id
        self.tamanho = tamanho
        self.t_chegada = t_chegada
        self.t_execucao_fase_1 = t_execucao_fase_1
        self.t_execucao_fase_2 = t_execucao_fase_2
        self.t_disco = t_disco
        self.t_total_execucao = t_execucao_fase_1 + t_execucao_fase_2 + t_disco
        self.qtd_discos = qtd_discos
        self.qtd_disco_alocado = 0
        self.quantum = quantum

        self.executou_disco = False
        self.disco_finalizado = False

        self.contador_quantum = 0
        self.dispatcher = dispatcher
        self.t_bloqueado = 0
        self.tempo_decorrido_disco = 0
        self.tempo_executado = 0

        self.novo = True
        self.bloqueado = False
        self.finalizado = False
        self.executando = False
        self.pronto = False
        self.suspenso_bloqueado = False
        self.suspenso_pronto = False

        self.fila_atual = None

        self.indice_inicial_mp = None
        self.indice_final_mp = None

    def __str__(self):
        status = {
            'Bloqueado': self.bloqueado,
            'Finalizado': self.finalizado,
            'Executando': self.executando,
            'Pronto': self.pronto,
            'Suspenso_bloqueado': self.suspenso_bloqueado,
            'Suspenso_pronto': self.suspenso_pronto
        }

        actual_status = [key for key, value in status.items() if value == True]

        return f"Processo {self.identificador} | Chegada: {self.t_chegada} | Execução fase 1: {self.t_execucao_fase_1} u.t. | Tempo de E/S: {self.t_disco} u.t. | Execução fase 2: {self.t_execucao_fase_2} u.t. | Tamanho: {self.tamanho}mb | Qtd. Discos: {self.qtd_discos} | Status: {actual_status or 'Novo'}"
    
    def mudar_estado(self):
        self.bloqueado = False
        self.finalizado = False
        self.executando = False
        self.pronto = False
        self.suspenso_bloqueado = False
        self.suspenso_pronto = False
        self.novo = False
        return

    def admitir(self):
        if not self.novo:
            return
        
        self.mudar_estado()
        self.pronto = True

        print(f"Processo {self.identificador} foi admitido na Memória Principal")

    def bloquear(self):
        if not self.executando:
            return
        
        if self.bloqueado:
            return

        self.mudar_estado()
        self.bloqueado = True
        self.contador_quantum = 0

        # print(f"Processo {self.identificador} será bloqueado")

    def desbloquear(self):	
        if (not self.bloqueado):
            return
        
        self.mudar_estado()
        self.pronto = True
        # self.fila_de_bloqueados.remove(self)
        # self.fila_de_prontos.append(self)
        # print(f"Processo {self.identificador} foi desbloqueado")
    
    def preempcao(self):
        if not self.executando:
            return
        
        self.contador_quantum = 0
        self.mudar_estado()
        self.pronto = True
        
        # print(f"Processo {self.identificador} foi interrompido por fatia de tempo")

    def finalizar(self):
        if not self.executando:
            return
        
        if self.finalizado:
            return

        self.mudar_estado()
        self.finalizado = True

        # print(f"Processo {self.identificador} foi finalizado")

    def suspender(self):
        if self.suspenso_bloqueado or self.suspenso_pronto:
            return
        
        if (not self.bloqueado) and (not self.pronto) and (not self.novo):
            return

        if self.bloqueado:
            self.mudar_estado()
            self.suspenso_bloqueado = True
            print(f"Processo {self.identificador} foi suspenso-bloqueado")

        else:
            self.mudar_estado()
            self.suspenso_pronto = True
            print(f"Processo {self.identificador} foi suspenso-pronto")

    def voltar_para_mp(self):
        if (not self.suspenso_bloqueado) and (not self.suspenso_pronto):
            return

        if self.suspenso_bloqueado:
            self.mudar_estado()
            self.bloqueado = True

            print(f"Processo {self.identificador} voltou para a fila de prontos da Memória Principal")

        else:
            self.mudar_estado()
            self.pronto = True

            print(f"Processo {self.identificador} voltou para a fila de bloqueados da Memória Principal")

    def executar(self):
        if self.suspenso_bloqueado or self.suspenso_pronto or self.finalizado or self.bloqueado:
            return

        self.mudar_estado()
        self.executando = True

        self.tempo_executado += 1
        self.contador_quantum += 1

        print(f"Processo {self.identificador} em execução | Fase: { 1 if self.tempo_executado <= self.t_execucao_fase_1 else 2} | {self.tempo_executado}/{self.t_execucao_fase_1 + self.t_execucao_fase_2}")

        if self.tempo_executado == self.t_execucao_fase_1:
            self.bloquear()
            return
        
        if self.tempo_executado == self.t_execucao_fase_1 + self.t_execucao_fase_2:
            self.finalizar()
            return

    def incrementar_tempo_bloqueado(self):
        if self.bloqueado:
            self.t_bloqueado += 1


    def permitir_execucao_disco(self):
        self.executou_disco = False
    

    def executar_disco(self):
        if self.executou_disco or self.suspenso_pronto or self.finalizado or self.pronto or self.executando or self.novo:
            return
    
        if self.bloqueado:
            self.mudar_estado()
            self.bloqueado = True
        else:
            self.mudar_estado()
            self.suspenso_bloqueado = True
        

        self.tempo_decorrido_disco += 1
        self.executou_disco = True
        
        print(f"Processo {self.identificador} está sendo executado em disco: {self.tempo_decorrido_disco}/{self.t_disco}")
        
        if self.tempo_decorrido_disco == self.t_disco:
            self.desbloquear()
            return
        
    