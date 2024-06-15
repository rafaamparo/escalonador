import time

from classes.cpu import Cpu
from classes.process import Process
from classes.dispatcher import Dispatcher
from classes.disk import Disk
from util.traceback import Traceback
from classes.memory import Memory
from classes.leitorArquivo import LeitorArquivo

unidade_de_tempo = 0
clock_delay = 0.4
quantum = 2
numero_de_cpus = 1 
numero_de_discos = 4
numero_de_filas = 4
id_inicial_de_processos = 1

fila_de_processos = []
lista_de_cpus = []
lista_de_discos = []
fila_de_novos = []
fila_de_bloqueados = []
fila_de_finalizados = []
bloqueados_em_execucao = []
fila_de_suspensos = []

filas = [[] for i in range(numero_de_filas)]

memoria = Memory()

dispatcher = Dispatcher(filas, fila_de_bloqueados, bloqueados_em_execucao, fila_de_finalizados, memoria)

caminho_arquivo = r'C:\Users\Anderson\Documents\MeusProjetos\escalonador\entrada.txt'
leitor = LeitorArquivo(caminho_arquivo, dispatcher)
processos = leitor.carregar_processos()

for processo in processos:
    processo.quantum = quantum

for i in range(numero_de_cpus):
    lista_de_cpus.append(Cpu(i, len(filas), dispatcher=dispatcher))

for i in range(numero_de_discos):
    lista_de_discos.append(Disk(i, dispatcher=dispatcher))
    
fila_de_processos = processos

traceback = Traceback(fila_de_processos=fila_de_processos) #Para gerar tabela de escalonamento ao fim da execução


# Nosso escalonador de processos
executando_escalonador = True
while executando_escalonador:
    print(f"[Tempo: {unidade_de_tempo}]")

    
    dispatcher.despachar_finalizados()
    dispatcher.despachar_bloqueados()
    dispatcher.despachar_prontos()

    # ! Dados do Escalonamento Atual para o Traceback (Gerar Tabela)
    dadoDoEscalonamentoAtual = {
        "tempo": unidade_de_tempo,
        "executando": [],
    }

    # ! Printar Logs Remanescentes dos CPUs
    print(" ")
    for cpu in lista_de_cpus:
        cpu.remanescente()

    # ! Printar Logs Remanescentes dos Discos
    for disco in lista_de_discos:
        disco.remanescente()
    print(" ")

    # ! Chegada de processos
    for processo in fila_de_processos:
        if processo.t_chegada == unidade_de_tempo:
            fila_de_novos.append(processo) # Adiciona o processo na fila de novos
            print(f"Processo {processo.identificador} foi adicionado na fila de novos")


    # ! Volta de processos suspensos à MP
    for processo in fila_de_suspensos.copy():
        if memoria.admite_processo(processo, False):
            fila_de_suspensos.remove(processo)
            processo.voltar_para_mp()

            if (processo.pronto):
                filas[0].append(processo)
                print(f"Processo {processo.identificador} foi adicionado na fila de prontos 0")
            if (processo.bloqueado):
                fila_de_bloqueados.append(processo)
                print(f"Processo {processo.identificador} foi adicionado na fila de bloqueados")


    #!  Admissão de processos
    fila_de_novos_SPN = sorted(fila_de_novos, key=lambda x: x.t_total_execucao)   # ordena a fila de novos seguindo o escalonamento Shortest Process Next - os menores processos possuem prioridade
    for processo in fila_de_novos_SPN:
        # TO DO: Verificar se o processo pode ser admitido (classe memory)
        if memoria.admite_processo(processo):
            filas[0].append(processo)
            fila_de_novos.remove(processo)
            #processo.admitir()
            print(f"Processo {processo.identificador} foi adicionado na fila de prontos 0")
        else:
            # tentar suspender um processo bloqueado para liberar espaço necessário na MP
            fila_de_novos.remove(processo)
            processo.admitir()
            processo.suspender()
            fila_de_suspensos.append(processo)

    # ! Escalonamento de processos
    for (i, fila) in enumerate(filas):
        if (len(filas[i]) > 0):
            for cpu in lista_de_cpus:
                if cpu.obter_processo() is None and fila:
                    processo = fila[0]
                    fila.remove(processo)
                    cpu.escalonar_processo(processo, i)
                    print(f"Processo {processo.identificador} é escalonado para CPU {cpu.id}")

    # ! Escalonamento de Disco
    for processo in fila_de_bloqueados.copy():

        discos_livres = [disco for disco in lista_de_discos if disco.obter_processo() is None]

        if processo.qtd_discos <= len(discos_livres):
            for disco in discos_livres:
                if disco.obter_processo() is None and processo.qtd_discos > 0 and processo.qtd_disco_alocado != processo.qtd_discos:
                    processo.qtd_disco_alocado += 1
                    disco.escalonar_processo(processo)
                    print(f"Processo {processo.identificador} é escalonado para Disco {disco.id}")
            bloqueados_em_execucao.append(processo)
            fila_de_bloqueados.remove(processo)
            

    # ! Printar Status dos Processos
    print(" ")
    memoria.printIntervalosLivres()
    print(f"Fila de Novos: {[f'Processo {processo.identificador}' for processo in fila_de_novos]}")
    for (i, fila) in enumerate(filas):
        print(f"Fila de Prontos {i}: {[f'Processo {processo.identificador}' for processo in fila]}")
    print(f"Fila de Bloqueados: {[f'Processo {processo.identificador} ({processo.qtd_discos} discos)' for processo in fila_de_bloqueados]}")
    print(f"Fila de Suspensos-Prontos: {[f'Processo {processo.identificador}' for processo in fila_de_suspensos if processo.suspenso_pronto]}")
    print(f"Fila de Suspensos-Bloqueados: {[f'Processo {processo.identificador}' for processo in fila_de_suspensos if processo.suspenso_bloqueado]}")
    for cpu in lista_de_cpus:
        print(f"CPU {cpu.id}: {(f'Processo {cpu.obter_processo().identificador}' if cpu.obter_processo() is not None else None) or 'Livre'}")
    for disco in lista_de_discos:
        print(f"Disco {disco.id}: {(f'Processo {disco.obter_processo().identificador} (Bloqueado em execução de E/S) ({disco.obter_processo().t_disco - disco.obter_processo().tempo_decorrido_disco} u.t.)' if disco.obter_processo() is not None else None) or 'Livre'}")
    print(" ")



    # ! Execução dos processos
    for cpu in lista_de_cpus:
        if cpu.obter_processo() is not None:
            dadoDoEscalonamentoAtual["executando"].append(cpu.obter_processo().identificador)
        cpu.executar_processo()

    # ! Incrementar tempo de bloqueio
    for processo in fila_de_bloqueados.copy():
        processo.incrementar_tempo_bloqueado()

    # ! Execução do DMA
    for disco in lista_de_discos:
        disco.executar()
        
    for processo in bloqueados_em_execucao.copy():
        processo.permitir_execucao_disco()
    
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