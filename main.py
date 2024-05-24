import time

from classes.cpu import Cpu
from classes.process import Process


unidade_de_tempo = 0
clock_delay = 2.5
quantum = 3
numero_de_cpus = 4
numero_de_processos = 1
fila_de_processos = []
lista_de_cpus = []
fila_de_novos = []
fila_de_prontos_0 = []
fila_de_prontos_1 = []
fila_de_prontos_2 = []
fila_de_prontos_3 = []
fila_de_bloqueados = []

processo1 = Process(
    id=numero_de_processos,
    t_chegada=0,
    t_execucao_fase_1=4,
    t_disco=2,
    t_execucao_fase_2=4,
    tamanho=800,
    qtd_discos=2,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    fila_de_prontos=fila_de_prontos_0
)
numero_de_processos += 1
processo2 = Process(
    id=numero_de_processos,
    t_chegada=0,
    t_execucao_fase_1=3,
    t_disco=6,
    t_execucao_fase_2=5,
    tamanho=950,
    qtd_discos=1,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    fila_de_prontos=fila_de_prontos_0
)
numero_de_processos += 1
processo3 = Process(
    id=numero_de_processos,
    t_chegada=0,
    t_execucao_fase_1=2,
    t_disco=3,
    t_execucao_fase_2=8,
    tamanho=1024,
    qtd_discos=3,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    fila_de_prontos=fila_de_prontos_0
)
numero_de_processos += 1
processo4 = Process(
    id=numero_de_processos,
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
numero_de_processos += 1
processo5 = Process(
    id=numero_de_processos,
    t_chegada=0,
    t_execucao_fase_1=6,
    t_disco=4,
    t_execucao_fase_2=3,
    tamanho=4048,
    qtd_discos=1,
    quantum=quantum,
    fila_de_bloqueados=fila_de_bloqueados,
    fila_de_prontos=fila_de_prontos_0
)
numero_de_processos += 1

for i in range(numero_de_cpus):
    lista_de_cpus.append(Cpu(i, fila_de_prontos_0, fila_de_prontos_1, fila_de_prontos_2, fila_de_prontos_3, fila_de_bloqueados))

fila_de_processos = [processo1, processo2, processo3, processo4, processo5]

# Nosso escalonador de processos
print(processo1)
while True:
    print(f"[Tempo: {unidade_de_tempo}]")

    # Chegada de processos
    for processo in fila_de_processos:
        if processo.t_chegada == unidade_de_tempo:
            fila_de_novos.append(processo) # Adiciona o processo na fila de novos
            print(f"Processo {processo.identificador} foi adicionado na fila de novos")

    # Admissão de processos
    print({processo.identificador for processo in fila_de_novos})
    for processo in fila_de_novos:
        # Verificar se o processo pode ser admitido (classe memory)
        fila_de_novos.remove(processo)
        fila_de_prontos_0.append(processo)
        processo.admitir()

    # Escalonamento de processos
    if (len(fila_de_prontos_0) > 0):
        for cpu in lista_de_cpus:
            if cpu.obter_processo() is None and fila_de_prontos_0:
                processo = fila_de_prontos_0[0]
                fila_de_prontos_0.remove(processo)
                cpu.escalonar_processo(processo, 0)
                print(f"Processo {processo.identificador} foi adicionado na CPU {cpu.id}")
                break
    if (len(fila_de_prontos_1) > 0):
        for cpu in lista_de_cpus:
            if cpu.obter_processo() is None and fila_de_prontos_1:
                processo = fila_de_prontos_1[0]
                fila_de_prontos_1.remove(processo)
                cpu.escalonar_processo(processo, 1)
                print(f"Processo {processo.identificador} foi adicionado na CPU {cpu.id}")
                break
    if (len(fila_de_prontos_2) > 0):
        for cpu in lista_de_cpus:
            if cpu.obter_processo() is None and fila_de_prontos_2:
                processo = fila_de_prontos_2[0]
                fila_de_prontos_2.remove(processo)
                cpu.escalonar_processo(processo, 2)
                print(f"Processo {processo.identificador} foi adicionado na CPU {cpu.id}")
                break
    if (len(fila_de_prontos_3) > 0):
        for cpu in lista_de_cpus:
            if cpu.obter_processo() is None and fila_de_prontos_3:
                processo = fila_de_prontos_3[0]
                fila_de_prontos_3.remove(processo)
                cpu.escalonar_processo(processo, 3)
                print(f"Processo {processo.identificador} foi adicionado na CPU {cpu.id}")
                break

    # Execução do DMA
    for processo in fila_de_bloqueados:
        processo.executar_disco()

    # Execução dos processos
    for cpu in lista_de_cpus:
        cpu.executar_processo()


    unidade_de_tempo += 1

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

    time.sleep(clock_delay)
    print("-"*10)


