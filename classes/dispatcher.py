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

    def despachar_bloqueados(self):
        # print (f"DEBUG - FILA DE BLOQUEADOS: {[f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in self.fila_temp_bloqueados]}")

        fila_temp_bloqueados_SPN = sorted(self.fila_temp_bloqueados, key=lambda x: x.t_total_execucao)
        # print("")
        # print (f"DEBUG - FILA DE BLOQUEADOS_SPN: {[f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in fila_temp_bloqueados_SPN]}")
        # print("")
        for processo in fila_temp_bloqueados_SPN:
            # print(f"Processo {processo.identificador} foi bloqueado")
            self.fila_bloqueados.append(processo)
        self.fila_temp_bloqueados = []

        # print(f"DEBUG - FILA DE BLOQUEADOS REAL: {[f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in self.fila_bloqueados]}")

    
    def despachar_finalizados(self):
        for processo in self.fila_temp_finalizados:
            self.memoria.finalizar_processo(processo)
            # print(f"Processo {processo.identificador} foi finalizado")
            self.fila_de_finalizados.append(processo)
        self.fila_temp_finalizados = []

    def despachar_prontos(self):
        # print(f"DEBUG - FILA DE PRONTOS_TEMP 0: { [f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in self.fila_temp_prontos[0] ] }")
        # print(f"DEBUG - FILA DE PRONTOS_TEMP 1: { [f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in self.fila_temp_prontos[1] ] }")
        # print(f"DEBUG - FILA DE PRONTOS_TEMP 2: { [f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in self.fila_temp_prontos[2] ] }")
        # print(f"DEBUG - FILA DE PRONTOS_TEMP 3: { [f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in self.fila_temp_prontos[3] ] }")

        fila_prontos_SPN = []
        for fila in self.fila_temp_prontos:
            fila_prontos_SPN.append(sorted(fila, key=lambda x: x.t_total_execucao))

        # print("")
        # print(f"DEBUG - FILA DE PRONTOS_SPN 0: { [f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in fila_prontos_SPN[0] ] }")
        # print(f"DEBUG - FILA DE PRONTOS_SPN 1: { [f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in fila_prontos_SPN[1] ] }")
        # print(f"DEBUG - FILA DE PRONTOS_SPN 2: { [f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in fila_prontos_SPN[2] ] }")
        # print(f"DEBUG - FILA DE PRONTOS_SPN 3: { [f'Processo {processo.identificador} - {processo.t_total_execucao}' for processo in fila_prontos_SPN[3] ] }")
        # print("")



        for i in range(len(fila_prontos_SPN)):
            for processo in fila_prontos_SPN[i]:
                # print(f"Processo {processo.identificador} foi interrompido por fatia de tempo")
                self.filas[i].append(processo)
            self.fila_temp_prontos[i] = []

    # # fila_prontos_SPN = [[], [], [], []]
    #     for (i, fila) in enumerate(self.filas):
    #         print(f"DEBUG - Fila de Prontos REAL {i}: {[f'Processo {processo.identificador}' for processo in fila]}")


