import time

from classes.process import Process


unidade_de_tempo = 0
clock_delay = 1
quantum = 3
numero_de_processos = 1
fila_de_processos = []
fila_de_novos = []
fila_de_execucao = []
fila_de_prontos_0 = []
fila_de_prontos_1 = []
fila_de_prontos_2 = []
fila_de_prontos_3 = []
fila_de_bloqueados = []

processo1 = Process(
    id=numero_de_processos,
    t_chegada=12,
    t_execucao_fase_1=4,
    t_disco=2,
    t_execucao_fase_2=4,
    tamanho=800,
    qtd_discos=2,
    contador_quantum=quantum
)
numero_de_processos += 1
processo2 = Process(
    id=numero_de_processos,
    t_chegada=14,
    t_execucao_fase_1=3,
    t_disco=6,
    t_execucao_fase_2=5,
    tamanho=950,
    qtd_discos=1,
    contador_quantum=quantum
)
numero_de_processos += 1
processo3 = Process(
    id=numero_de_processos,
    t_chegada=1,
    t_execucao_fase_1=2,
    t_disco=1,
    t_execucao_fase_2=8,
    tamanho=1024,
    qtd_discos=3,
    contador_quantum=quantum
)
numero_de_processos += 1
processo4 = Process(
    id=numero_de_processos,
    t_chegada=3,
    t_execucao_fase_1=7,
    t_disco=5,
    t_execucao_fase_2=3,
    tamanho=2048,
    qtd_discos=2,
    contador_quantum=quantum
)
numero_de_processos += 1

fila_de_processos = [processo1, processo2, processo3, processo4]

# Nosso escalonador de processos
print(processo1)
while True:
    print(f"[Tempo: {unidade_de_tempo}]")

    for processo in fila_de_processos:
        if processo.t_chegada == unidade_de_tempo:
            fila_de_novos.append(processo) # Adiciona o processo na fila de novos
            print(f"Processo {processo.identificador} foi adicionado na fila de novos")

    for processo in fila_de_novos:
        # Verificar se o processo pode ser admitido (classe memory)
        
        fila_de_novos.remove(processo)
        fila_de_prontos_0.append(processo)
        # print(f"Processo {processo.identificador} foi adicionado na fila de prontos 0")
        processo.admitir()

    if (len(fila_de_prontos_0) > 0):
        # Verificar se o processo pode ser executado (classe cpu)

        processo = fila_de_prontos_0[0]
        fila_de_prontos_0.remove(processo)
        fila_de_execucao.append(processo)
        print(f"Processo {processo.identificador} foi adicionado na fila de execução")
    elif (len(fila_de_prontos_1) > 0):

        # Verificar se o processo pode ser executado (classe cpu)

        processo = fila_de_prontos_1[0]
        fila_de_prontos_1.remove(processo)
        fila_de_execucao.append(processo)
        print(f"Processo {processo.identificador} foi adicionado na fila de execução")
    elif (len(fila_de_prontos_2) > 0):
        processo = fila_de_prontos_2[0]
        fila_de_prontos_2.remove(processo)
        fila_de_execucao.append(processo)
        print(f"Processo {processo.identificador} foi adicionado na fila de execução")


    for processo in fila_de_execucao:
        processo.executar()

    unidade_de_tempo += 1
    time.sleep(clock_delay)

