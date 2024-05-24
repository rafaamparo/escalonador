import time

from classes.process import Process


unidade_de_tempo = 0
clock_delay = 1
numero_de_processos = 0

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
)
numero_de_processos += 1

# Nosso escalonador de processos
while True:
    print(f"[Tempo: {unidade_de_tempo}]")
    unidade_de_tempo += 1

    print(processo1)


    time.sleep(clock_delay)

