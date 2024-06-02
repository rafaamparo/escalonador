import time

from classes.cpu import Cpu
from classes.process import Process
from classes.dispatcher import Dispatcher
from util.traceback import Traceback


unidade_de_tempo = 0
clock_delay = 0.4
quantum = 3
numero_de_cpus = 2
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

filas = [fila_de_prontos_0, fila_de_prontos_1, fila_de_prontos_2, fila_de_prontos_3]
dispatcher = Dispatcher(filas, fila_de_bloqueados, fila_de_finalizados)

processo1 = Process(
    id=id_inicial_de_processos,
    t_chegada=1,
    t_execucao_fase_1=5,
    t_disco=3,
    t_execucao_fase_2=3,
    tamanho=800,
    qtd_discos=2,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    dispatcher=dispatcher
)
id_inicial_de_processos += 1
processo2 = Process(
    id=id_inicial_de_processos,
    t_chegada=0,
    t_execucao_fase_1=5,
    t_disco=4,
    t_execucao_fase_2=3,
    tamanho=950,
    qtd_discos=1,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    dispatcher=dispatcher
)
id_inicial_de_processos += 1
processo3 = Process(
    id=id_inicial_de_processos,
    t_chegada=2,
    t_execucao_fase_1=12,
    t_disco=3,
    t_execucao_fase_2=7,
    tamanho=1024,
    qtd_discos=3,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    dispatcher=dispatcher
)
id_inicial_de_processos += 1
processo4 = Process(
    id=id_inicial_de_processos,
    t_chegada=3,
    t_execucao_fase_1=5,
    t_disco=10,
    t_execucao_fase_2=3,
    tamanho=2048,
    qtd_discos=2,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    dispatcher=dispatcher
)


for i in range(numero_de_cpus):
    lista_de_cpus.append(Cpu(i, fila_de_prontos_0, fila_de_prontos_1, fila_de_prontos_2, fila_de_prontos_3, dispatcher=dispatcher))

fila_de_processos = [processo1, processo2]

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
        filas[0].append(processo)
        fila_de_novos.remove(processo)
        processo.admitir()
        print(f"Processo {processo.identificador} foi adicionado na fila de prontos 0")

    # ! Escalonamento de processos
    for (i, fila) in enumerate(filas):
        if (len(filas[i]) > 0):
            for cpu in lista_de_cpus:
                if cpu.obter_processo() is None and fila:
                    processo = fila[0]
                    fila.remove(processo)
                    cpu.escalonar_processo(processo, i)
                    print(f"Processo {processo.identificador} é escalonado para CPU {cpu.id}")
    
    # ! Printar Status dos Processos
    print(" ")
    print(f"Fila de Novos: {[f'Processo {processo.identificador}' for processo in fila_de_novos]}")
    for (i, fila) in enumerate(filas):
        print(f"Fila de Prontos {i}: {[f'Processo {processo.identificador}' for processo in fila]}")
    print(f"Fila de Bloqueados: {[f'Processo {processo.identificador}' for processo in fila_de_bloqueados]}")
    for cpu in lista_de_cpus:
        print(f"CPU {cpu.id}: {(f'Processo {cpu.obter_processo().identificador}' if cpu.obter_processo() is not None else None) or 'Livre'}")
    print(" ")


    print(f"Fila de Bloqueados NOVAMENTE: {[f'Processo {processo.identificador}' for processo in fila_de_bloqueados]}")
    # ! Execução do DMA
    for processo in fila_de_bloqueados.copy():
        print(f"Processo {processo.identificador} está na fila de bloqueados")
        # TO DO: Verificar se o processo pode ser executado (classe disk)
        processo.executar_disco()

    # ! Execução dos processos
    for cpu in lista_de_cpus:
        if cpu.obter_processo() is not None:
            dadoDoEscalonamentoAtual["executando"].append(cpu.obter_processo().identificador)
        cpu.executar_processo()
    
    traceback.dadosDoEscalonamento.append(dadoDoEscalonamentoAtual)

    dispatcher.despachar_finalizados()
    dispatcher.despachar_bloqueados()
    dispatcher.despachar_prontos()

    unidade_de_tempo += 1
    time.sleep(clock_delay)
    print("-"*40)

    if (len(fila_de_finalizados) == len(fila_de_processos)) and all(cpu.logRemanescente is None for cpu in lista_de_cpus):
        executando_escalonador = False

print(" ")
print("Fim da execução")
print(" ")

traceback.print_tabela()