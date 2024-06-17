from classes.process import Process
from classes.dispatcher import Dispatcher
import copy
from rich.text import Text
from rich.progress import Progress, BarColumn
from rich.console import Console
from rich.bar import Bar
from rich.measure import Measurement
from rich.panel import Panel
from rich.console import Group

class Memory():
    def __init__(self, capacidade_celula_mb = 1, capacidade_total_mb = 32000, processos = [], tamanho_barra=200):
        # ! Vetor que representa a memória principal. célula False representa endereços de memória que não estão ocupados por processo
        self.memoria_principal = [False for _ in range(int(capacidade_total_mb/capacidade_celula_mb))]
        self.intervalos_livres = []
        self.atualiza_intervalos_livres()
        self.console = Console()
        self.tamanho_barra = tamanho_barra
        self.processos = processos



    
    def printIntervalosLivres(self):
        self.atualiza_intervalos_livres()
        
        def getColorIndex(id):
            color_index = id + 1
            if color_index > 8:
                color_index = color_index % 8

            if color_index == 3:
                color_index = 125
            if color_index == 2:
                color_index = 172
            return color_index                    

        memory_text = Text(justify="center")
        tamanho = self.tamanho_barra
        segment_size = len(self.memoria_principal) // tamanho  # Tamanho de cada segmento

        for i in range(tamanho):
            start_index = i * segment_size
            end_index = min((i + 1) * segment_size, len(self.memoria_principal))
            
            segment = self.memoria_principal[start_index:end_index]
            occupied_count = sum(segment)
            free_count = segment_size - occupied_count

            if occupied_count > free_count:

                for processo in self.processos:
                    if processo.indice_inicial_mp is not None:
                        if start_index >= processo.indice_inicial_mp and end_index <= processo.indice_final_mp:
                            memory_text.append('█', style=f'color({getColorIndex(processo.identificador) })')
                            break
            else:
                memory_text.append('█', style='bright_green')


        text_espaco_alocado_processos = Text.assemble(
                *[
                    (f"Processo {processo.identificador}: [{processo.indice_inicial_mp}, {processo.indice_final_mp-1}] ({processo.indice_final_mp - processo.indice_inicial_mp}mb) ", f"bold color({getColorIndex(processo.identificador)})")
                    for processo in self.processos
                    if processo.indice_inicial_mp is not None
                ], justify="center")
        self.console.print(Panel(
            Group(
                Panel(memory_text), 
                Panel(
                    Text(" | ".join([f'[{intervalo[0]}, {intervalo[1]}] ({intervalo[1] - intervalo[0]+1}mb)' for intervalo in self.intervalos_livres]), justify="center", style="bright_green"), title="[white]Intervalos Livres"
                    ),
                Panel(text_espaco_alocado_processos, title="[white]Espaço Alocado por Processos", style="yellow")
                ),
                 title="[white]Memória Principal", style="yellow"))


    def admite_processo(self, processo: Process, printarLogs=True):
        # ! Política best fit: achar o menor espaço contínuo possível para alocar o processo
        self.atualiza_intervalos_livres()

        intervalos_livres = copy.deepcopy(self.intervalos_livres)

        intervalos_livres = sorted(intervalos_livres, key=lambda x: (x[1] - x[0]))

        for intervalo in intervalos_livres:
            if((intervalo[1] - intervalo[0] + 1) >= processo.tamanho):
                inicio_intervalo = intervalo[0]
                fim_intervalo = inicio_intervalo + processo.tamanho - 1
                for i in range(inicio_intervalo, fim_intervalo + 1):
                    self.memoria_principal[i] = True # ! Ocupa o espaço no vetor que representa a MP
                processo.indice_inicial_mp = inicio_intervalo
                processo.indice_final_mp = processo.tamanho + inicio_intervalo
                processo.admitir()
                self.console.print(f"Processo {processo.identificador} foi alocado na Memória Principal no intervalo [{inicio_intervalo}, {fim_intervalo}]")
                return True
        if printarLogs:
            self.console.print(f"Processo {processo.identificador} não pode ser alocado na memória nesse momento (Processo precisa de {processo.tamanho}mb)")
        return False
    
    def remover_processo(self, processo: Process):
        for i in range(processo.indice_inicial_mp, processo.indice_final_mp):
            self.memoria_principal[i] = False
        processo.indice_final_mp = None
        processo.indice_inicial_mp = None
        self.atualiza_intervalos_livres()
        self.console.print(f"Processo {processo.identificador} foi suspenso e removido da memória principal")
        return

    def finalizar_processo(self, processo: Process):
        for i in range(processo.indice_inicial_mp, processo.indice_final_mp):
            self.memoria_principal[i] = False # ! Libera o espaço no vetor que representa a MP
        processo.indice_final_mp = None
        processo.indice_inicial_mp = None
        self.atualiza_intervalos_livres()
        self.console.print(f"Processo {processo.identificador} foi finalizado e removido da memória principal")
        return

    def atualiza_intervalos_livres(self):
        self.intervalos_livres = []
        inicio = None
        # Percorre a memória principal para encontrar os intervalos livres
        for i in range(len(self.memoria_principal)):
            if self.memoria_principal[i] == False:  # Se a célula está livre
                if inicio is None:
                    inicio = i  # Marca o início do intervalo livre
            else:  # Se a célula está ocupada (True)
                if inicio is not None:
                    self.intervalos_livres.append([inicio, i - 1])  # Adiciona o intervalo livre encontrado
                    inicio = None
    
         # Caso haja um intervalo livre até o final da memória principal
        if inicio is not None:
            self.intervalos_livres.append([inicio, len(self.memoria_principal) - 1])

    def podeDesalocar(self, processoNovo: Process, processoAlocado: Process): # ! Verifica se é possível desalocar o processo alocado para alocar o processo novo
        tamanho_continuo_necessario = processoNovo.tamanho
        indice_inicial = processoAlocado.indice_inicial_mp
        indice_final = processoAlocado.indice_final_mp
        if (indice_inicial == None or indice_final == None):
            return False
        
        copia_memoria_principal = copy.deepcopy(self.memoria_principal)
        for i in range(indice_inicial, indice_final): # ! Simula a desalocação do processo alocado
            copia_memoria_principal[i] = False
        
        intervalos_livres = []
        inicio = None

        for i in range(len(copia_memoria_principal)):
            if copia_memoria_principal[i] == False:
                if inicio is None:
                    inicio = i
            else:
                if inicio is not None:
                    intervalos_livres.append([inicio, i - 1])
                    inicio = None
        if inicio is not None:
            intervalos_livres.append([inicio, len(copia_memoria_principal) - 1])

        intervalos_livres = sorted(intervalos_livres, key=lambda x: (x[1] - x[0]))

        for intervalo in intervalos_livres:
            if((intervalo[1] - intervalo[0] + 1) >= tamanho_continuo_necessario): # ! Verifica se o intervalo livre encontrado é suficiente para alocar o processo novo
                return True
        return False