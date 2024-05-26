import time

from classes.cpu import Cpu
from classes.process import Process
from util.traceback import Traceback


unidade_de_tempo = 0
clock_delay = 0.2
quantum = 3
numero_de_cpus = 4
id_inicial_de_processos = 1
fila_de_processos = []
lista_de_cpus = []
fila_de_novos = []
fila_de_prontos_0 = []
fila_de_prontos_1 = []
fila_de_prontos_2 = []
fila_de_prontos_3 = []
fila_de_bloqueados = []
fila_de_finalizados = []

processo1 = Process(
    id=id_inicial_de_processos,
    t_chegada=0,
    t_execucao_fase_1=6,
    t_disco=2,
    t_execucao_fase_2=4,
    tamanho=800,
    qtd_discos=2,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    fila_de_prontos=fila_de_prontos_0
)
id_inicial_de_processos += 1
processo2 = Process(
    id=id_inicial_de_processos,
    t_chegada=0,
    t_execucao_fase_1=2,
    t_disco=6,
    t_execucao_fase_2=5,
    tamanho=950,
    qtd_discos=1,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    fila_de_prontos=fila_de_prontos_0
)
id_inicial_de_processos += 1
processo3 = Process(
    id=id_inicial_de_processos,
    t_chegada=0,
    t_execucao_fase_1=3,
    t_disco=3,
    t_execucao_fase_2=8,
    tamanho=1024,
    qtd_discos=3,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    fila_de_prontos=fila_de_prontos_0
)
id_inicial_de_processos += 1
processo4 = Process(
    id=id_inicial_de_processos,
    t_chegada=0,
    t_execucao_fase_1=7,
    t_disco=5,
    t_execucao_fase_2=3,
    tamanho=2048,
    qtd_discos=2,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    fila_de_prontos=fila_de_prontos_0
)
id_inicial_de_processos += 1
processo5 = Process(
    id=id_inicial_de_processos,
    t_chegada=0,
    t_execucao_fase_1=6,
    t_disco=1,
    t_execucao_fase_2=3,
    tamanho=4048,
    qtd_discos=1,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    fila_de_prontos=fila_de_prontos_0
)
id_inicial_de_processos += 1
processo6 = Process(
    id=id_inicial_de_processos,
    t_chegada=1,
    t_execucao_fase_1=4,
    t_disco=4,
    t_execucao_fase_2=3,
    tamanho=6098,
    qtd_discos=1,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    fila_de_prontos=fila_de_prontos_0
)

for i in range(numero_de_cpus):
    lista_de_cpus.append(Cpu(i, fila_de_prontos_0, fila_de_prontos_1, fila_de_prontos_2, fila_de_prontos_3, fila_de_bloqueados, fila_de_finalizados=fila_de_finalizados))

fila_de_processos = [processo1, processo2, processo3, processo4, processo5, processo6]

traceback = Traceback(fila_de_processos=fila_de_processos) #Para gerar tabela de escalonamento ao fim da execução


# Nosso escalonador de processos
executando_escalonador = True
while executando_escalonador:
    print(f"[Tempo: {unidade_de_tempo}]")

    # ! Dados do Escalonamento Atual para o Traceback (Gerar Tabela)
    dadoDoEscalonamentoAtual = {
        "tempo": unidade_de_tempo,
        "executando": [],
    }

    # ! Printar Logs Remanescentes
    print(" ")
    for cpu in lista_de_cpus:
        cpu.remanescente()
    print(" ")


    # ! Chegada de processos
    for processo in fila_de_processos:
        if processo.t_chegada == unidade_de_tempo:
            fila_de_novos.append(processo) # Adiciona o processo na fila de novos
            print(f"Processo {processo.identificador} foi adicionado na fila de novos")

    #!  Admissão de processos
    fila_de_novos_SPN = sorted(fila_de_novos, key=lambda x: x.t_total_execucao)   # ordena a fila de novos seguindo o escalonamento Shortest Process Next - os menores processos possuem prioridade
    for processo in fila_de_novos_SPN:
        # TO DO: Verificar se o processo pode ser admitido (classe memory)
        fila_de_prontos_0.append(processo)
        fila_de_novos.remove(processo)
        processo.admitir()
        print(f"Processo {processo.identificador} foi adicionado na fila de prontos 0")

    # ! Escalonamento de processos
    if (len(fila_de_prontos_0) > 0):
        for cpu in lista_de_cpus:
            if cpu.obter_processo() is None and fila_de_prontos_0:
                processo = fila_de_prontos_0[0]
                fila_de_prontos_0.remove(processo)
                cpu.escalonar_processo(processo, 0)
                print(f"Processo {processo.identificador} é escalonado para CPU {cpu.id}")

    if (len(fila_de_prontos_1) > 0):
        for cpu in lista_de_cpus:
            if cpu.obter_processo() is None and fila_de_prontos_1:
                processo = fila_de_prontos_1[0]
                fila_de_prontos_1.remove(processo)
                cpu.escalonar_processo(processo, 1)
                print(f"Processo {processo.identificador} é escalonado para CPU {cpu.id}")
                
    if (len(fila_de_prontos_2) > 0):
        for cpu in lista_de_cpus:
            if cpu.obter_processo() is None and fila_de_prontos_2:
                processo = fila_de_prontos_2[0]
                fila_de_prontos_2.remove(processo)
                cpu.escalonar_processo(processo, 2)
                print(f"Processo {processo.identificador} é escalonado para CPU {cpu.id}")
                
    if (len(fila_de_prontos_3) > 0):
        for cpu in lista_de_cpus:
            if cpu.obter_processo() is None and fila_de_prontos_3:
                processo = fila_de_prontos_3[0]
                fila_de_prontos_3.remove(processo)
                cpu.escalonar_processo(processo, 3)
                print(f"Processo {processo.identificador} é adicionado na CPU {cpu.id}")
                
    
    # ! Printar Status dos Processos
    print(" ")
    print(f"Fila de Novos: {[f'Processo {processo.identificador}' for processo in fila_de_novos]}")
    print(f"Fila de Prontos 0: {[f'Processo {processo.identificador}' for processo in fila_de_prontos_0]}")
    print(f"Fila de Prontos 1: {[f'Processo {processo.identificador}' for processo in fila_de_prontos_1]}")
    print(f"Fila de Prontos 2: {[f'Processo {processo.identificador}' for processo in fila_de_prontos_2]}")
    print(f"Fila de Prontos 3: {[f'Processo {processo.identificador}' for processo in fila_de_prontos_3]}")
    print(f"Fila de Bloqueados: {[f'Processo {processo.identificador}' for processo in fila_de_bloqueados]}")
    for cpu in lista_de_cpus:
        print(f"CPU {cpu.id}: {(f'Processo {cpu.obter_processo().identificador}' if cpu.obter_processo() is not None else None) or 'Livre'}")
    print(" ")



    # ! Execução do DMA
    for processo in fila_de_bloqueados:
        # TO DO: Verificar se o processo pode ser executado (classe disk)
        processo.executar_disco()

    # ! Execução dos processos
    for cpu in lista_de_cpus:
        # Antes de executar o processo, sabemos que ele está na CPU
        if cpu.obter_processo() is not None:
            dadoDoEscalonamentoAtual["executando"].append(cpu.obter_processo().identificador)
        cpu.executar_processo()
        # Depois de executar o processo, pode acontecer de ele ser finalizado ou bloqueado
    
    traceback.dadosDoEscalonamento.append(dadoDoEscalonamentoAtual)

    unidade_de_tempo += 1
    time.sleep(clock_delay)
    print("-"*40)

    if (len(fila_de_finalizados) == len(fila_de_processos)) and all(cpu.logRemanescente is None for cpu in lista_de_cpus):
        executando_escalonador = False

print(" ")
print("Fim da execução")
print(" ")

traceback.print_tabela()

