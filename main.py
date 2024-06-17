import time

from classes.cpu import Cpu
from classes.process import Process
from classes.dispatcher import Dispatcher
from classes.disk import Disk
from util.traceback import Traceback
from classes.memory import Memory
from classes.leitorArquivo import LeitorArquivo
from rich.console import Console
from rich.console import Group
from rich.panel import Panel

# * Variáveis de configuração

unidade_de_tempo = 0
clock_delay = 0.5
quantum = 2
numero_de_cpus = 1
numero_de_discos = 4
numero_de_filas = 3
id_inicial_de_processos = 1
capacidade_total_mb = 5000

fila_de_processos = []
lista_de_cpus = []
lista_de_discos = []
fila_de_novos = []
fila_de_bloqueados = []
fila_de_finalizados = []
bloqueados_em_execucao = []
fila_de_suspensos = []

filas = [[] for i in range(numero_de_filas)]


caminho_arquivo = r'\entrada.txt'
leitor = LeitorArquivo(caminho_arquivo, quantum, id_inicial_de_processos)
processos = leitor.carregar_processos()

memoria = Memory(capacidade_total_mb=capacidade_total_mb, processos=processos, tamanho_barra=100)

dispatcher = Dispatcher(filas, fila_de_bloqueados, bloqueados_em_execucao, fila_de_finalizados, memoria)

for i in range(numero_de_cpus):
    lista_de_cpus.append(Cpu(i, len(filas), dispatcher=dispatcher))

for i in range(numero_de_discos):
    lista_de_discos.append(Disk(i, dispatcher=dispatcher))
    
fila_de_processos = processos

traceback = Traceback(fila_de_processos=fila_de_processos) # * Para gerar tabela de escalonamento ao fim da execução

# * Nosso escalonador de processos
executando_escalonador = True
console = Console()
while executando_escalonador:
    console.print("")
    console.rule(f"Tempo {unidade_de_tempo}")

    
    dispatcher.despachar_bloqueados()
    dispatcher.despachar_prontos()

    # * Dados do Escalonamento Atual para o Traceback (Gerar Tabela)
    dadoDoEscalonamentoAtual = {
        "tempo": unidade_de_tempo,
        "executando": [],
    }

    # * Printar Logs Remanescentes dos CPUs
    console.print(" ")
    for cpu in lista_de_cpus:
        cpu.remanescente()

    # * Printar Logs Remanescentes dos Discos
    for disco in lista_de_discos:
        disco.remanescente()
    console.print(" ")
    dispatcher.despachar_finalizados()

    # * Chegada de processos
    for processo in fila_de_processos:
        if processo.t_chegada == unidade_de_tempo:
            fila_de_novos.append(processo) # Adiciona o processo na fila de novos
            console.print(f"Processo {processo.identificador} foi adicionado na fila de novos")


    # * Volta de processos suspensos à MP
    for processo in fila_de_suspensos.copy():
        if memoria.admite_processo(processo, False): # Verifica se há espaço suficiente na MP para realocar um processo sem a necessidade de desalocar outro
            fila_de_suspensos.remove(processo)
            processo.voltar_para_mp()

            if (processo.pronto): # Processos suspensos-prontos voltam sempre para a fila de prontos 0
                filas[0].append(processo)
                console.print(f"Processo {processo.identificador} foi adicionado na fila de prontos 0")
            if (processo.bloqueado): # Processos suspensos-bloqueados voltam sempre para a fila de bloqueados
                fila_de_bloqueados.append(processo)
                console.print(f"Processo {processo.identificador} foi adicionado na fila de bloqueados")
        else:
            if (processo.suspenso_bloqueado):
                continue

            if (processo.suspenso_pronto): # Verifica se há processo bloqueado na MP que pode ser desalocado para dar espaço a um processo suspenso-pronto
                processos_bloqueados = [processo for processo in fila_de_bloqueados if processo.bloqueado == True]
                console.print(f"DEBUG: processos_bloqueados: {[f'Processo {processo.identificador} ({processo.tamanho}mb)' for processo in processos_bloqueados]}")

                for processo_bloq in processos_bloqueados:
                    # Verificar se o processo bloqueado está dentro de certas condições que tornam eficiente para o sistema desalocá-lo
                    if ((processo_bloq.t_disco >= 10) and ((processo_bloq.t_disco - processo_bloq.tempo_decorrido_disco >= (processo_bloq.t_disco/2)))):
                        console.print(f"DEBUG: Estamos tentando desalocar o processo {processo_bloq.identificador} ({processo_bloq.tamanho}mb) para adicionar o processo {processo.identificador} ({processo.tamanho}mb)")
                        if memoria.podeDesalocar(processo, processo_bloq): # Função que simula, na memória, o resultado de desalocar um processo, verificando se o intervalo de memória resultante é suficiente para alocar outro
                            memoria.remover_processo(processo_bloq)
                            processo_bloq.suspender()
                            fila_de_suspensos.append(processo_bloq) # Adiciona o processo desalocado na fila de suspensos
                            console.print(f"DEBUG: Processo {processo_bloq.identificador} foi removido ")
                            break

                if memoria.admite_processo(processo, False): # Volta do processo suspenso-pronto para a MP, no espaço em que hoiuve a desalocação do processo bloqueado
                    fila_de_suspensos.remove(processo)
                    processo.voltar_para_mp()

                    if (processo.pronto):
                        filas[0].append(processo)
                        console.print(f"Processo {processo.identificador} foi adicionado na fila de prontos 0")
                    if (processo.bloqueado):
                        fila_de_bloqueados.append(processo)
                        console.print(f"Processo {processo.identificador} foi adicionado na fila de bloqueados")
            
    # * Admissão de processos
    fila_de_novos_SPN = sorted(fila_de_novos, key=lambda x: x.t_total_execucao)   # Ordena a fila de novos seguindo o escalonamento Shortest Process Next - os menores processos possuem prioridade
    for processo in fila_de_novos_SPN:
        # Verificar se o processo pode ser admitido na MP
        if memoria.admite_processo(processo):
            filas[0].append(processo)
            fila_de_novos.remove(processo)
            processo.admitir()
            console.print(f"Processo {processo.identificador} foi adicionado na fila de prontos 0")
        else: # Verifica se há processo bloqueado que pode ser desalocado para dar espaço ao processo novo
            fila_total_bloqueados = fila_de_bloqueados + bloqueados_em_execucao
            console.print(f"DEBUG: fila_total_bloqueados: ", [f'Processo {processo.identificador} ({processo.indice_inicial_mp} - {processo.indice_final_mp})' for processo in fila_total_bloqueados])
            for processo_bloqueado in fila_total_bloqueados:
                if ((processo_bloqueado.suspenso_bloqueado or processo_bloqueado.suspenso_pronto)):
                    continue
                # Verificar se o processo bloqueado está dentro de certas condições que tornam eficiente para o sistema desalocá-lo
                if ((processo_bloqueado.t_disco >= 10) and ((processo_bloqueado.t_disco - processo_bloqueado.tempo_decorrido_disco >= (processo_bloqueado.t_disco/2)))):
                    console.print(f"DEBUG: Estamos tentando desalocar o processo {processo_bloqueado.identificador} ({processo_bloqueado.tamanho}mb) para adicionar o processo {processo.identificador} ({processo.tamanho}mb)")
                    if memoria.podeDesalocar(processo, processo_bloqueado): # Função que simula, na memória, o resultado de desalocar um processo, verificando se o intervalo de memória resultante é suficiente para alocar outro
                        memoria.remover_processo(processo_bloqueado)
                        processo_bloqueado.suspender()
                        fila_de_suspensos.append(processo_bloqueado)
                        console.print(f"DEBUG: Processo {processo_bloqueado.identificador} foi removido ")
                        break

            if memoria.admite_processo(processo): #  Se houver suspensão de processo bloqueado, o processo é admitido na MP e adicionado à fila de prontos 0
                filas[0].append(processo) 
                fila_de_novos.remove(processo)
                processo.admitir()
                console.print(f"Processo {processo.identificador} foi adicionado na fila de prontos 0")
            else: # Se não houver suspensão possível de processo bloqueado, o processo é suspenso
                fila_de_novos.remove(processo)
                processo.admitir()
                processo.suspender()
                fila_de_suspensos.append(processo)

    # * Escalonamento de processos
    for (i, fila) in enumerate(filas):
        if (len(filas[i]) > 0):
            for cpu in lista_de_cpus:
                if cpu.obter_processo() is None and fila:
                    processo = fila[0]
                    fila.remove(processo)
                    cpu.escalonar_processo(processo, i)
                    console.print(f"Processo {processo.identificador} é escalonado para CPU {cpu.id}")

    # * Escalonamento de Disco
    for processo in fila_de_bloqueados.copy():
        discos_livres = [disco for disco in lista_de_discos if disco.obter_processo() is None]
        if processo.qtd_discos <= len(discos_livres):
            for disco in discos_livres:
                if disco.obter_processo() is None and processo.qtd_discos > 0 and processo.qtd_disco_alocado != processo.qtd_discos:
                    processo.qtd_disco_alocado += 1
                    disco.escalonar_processo(processo)
                    console.print(f"Processo {processo.identificador} é escalonado para Disco {disco.id}")
            bloqueados_em_execucao.append(processo)
            fila_de_bloqueados.remove(processo)
            

    # * Printar Status dos Processos
    console.print(" ")
    memoria.printIntervalosLivres()

    panels_filas_prontos = [
        (f"Fila de Prontos {i}: {[f'Processo {processo.identificador}' for processo in fila]}")
        for i, fila in enumerate(filas)
    ]

    panels_lista_cpus = [
        (f"CPU {cpu.id}: {(f'Processo {cpu.obter_processo().identificador}' if cpu.obter_processo() is not None else None) or 'Livre'}")
        for cpu in lista_de_cpus
    ]

    panels_lista_disco = [
        (f"Disco {disco.id}: {(f'Processo {disco.obter_processo().identificador} (Bloqueado em execução de E/S) ({disco.obter_processo().t_disco - disco.obter_processo().tempo_decorrido_disco} u.t.)' if disco.obter_processo() is not None else None) or 'Livre'}")
        for disco in lista_de_discos
    ]

    panel_group = Group(
    Panel(f"Fila de Novos: {[f'Processo {processo.identificador}' for processo in fila_de_novos]}"),
    Panel(Group(*panels_filas_prontos)),
    Panel(Group(
        (f"Fila de Bloqueados: {[f'Processo {processo.identificador} ({processo.qtd_discos} discos)' for processo in (fila_de_bloqueados + bloqueados_em_execucao)]}"),
        (f"Fila de Suspensos-Prontos: {[f'Processo {processo.identificador}' for processo in fila_de_suspensos if processo.suspenso_pronto]}"),
        (f"Fila de Suspensos-Bloqueados: {[f'Processo {processo.identificador}' for processo in fila_de_suspensos if processo.suspenso_bloqueado]}")
    )),
    Panel(Group(*panels_lista_cpus)),
    Panel(Group(*panels_lista_disco))
    )

    console.print(Panel(panel_group, title="Status dos Processos"))
    console.print(" ")

    # * Execução dos processos
    for cpu in lista_de_cpus:
        if cpu.obter_processo() is not None:
            dadoDoEscalonamentoAtual["executando"].append(cpu.obter_processo().identificador)
        cpu.executar_processo()

    # * Incrementar tempo de bloqueio
    for processo in fila_de_bloqueados.copy():
        processo.incrementar_tempo_bloqueado()

    # * Execução do DMA
    for disco in lista_de_discos:
        disco.executar()     
    for processo in bloqueados_em_execucao.copy():
        processo.permitir_execucao_disco()
    
    traceback.dadosDoEscalonamento.append(dadoDoEscalonamentoAtual)
    unidade_de_tempo += 1
    time.sleep(clock_delay)

    # * Condição de parada
    if (len(fila_de_finalizados) == len(fila_de_processos)) and all(cpu.logRemanescente is None for cpu in lista_de_cpus):
        executando_escalonador = False

console.print(" ")
console.rule("Fim da execução")
console.print(" ")

traceback.print_tabela()