from classes.process import Process
from classes.dispatcher import Dispatcher
import copy

class Memory():
    def __init__(self, capacidade_celula_mb = 1, capacidade_total_mb = 32000):
        # vetor que representa a memória principal. célula False representa endereços de memória que não estão ocupados por processo
        # self.memoria_principal = [False for _ in range(int(capacidade_total_mb/capacidade_celula_mb))]
        self.memoria_principal = [False] * 798 + [True] + [False] * 799 + [True] + [False] * 950
        self.intervalos_livres = []
        self.atualiza_intervalos_livres()
    
    def printIntervalosLivres(self):
        self.atualiza_intervalos_livres()
        print(f"Intervalos livres: {[f'[{intervalo[0]}, {intervalo[1]}] ({intervalo[1] - intervalo[0]+1}mb)' for intervalo in self.intervalos_livres]}")


    def admite_processo(self, processo: Process, printarLogs=True):
        # política best fit: achar o menor espaço contínuo possível para alocar o processo
        self.atualiza_intervalos_livres()

        intervalos_livres = copy.deepcopy(self.intervalos_livres)

        intervalos_livres = sorted(intervalos_livres, key=lambda x: (x[1] - x[0]))

        # print(f"Intervalos livres: {intervalos_livres}")
        for intervalo in intervalos_livres:
            if((intervalo[1] - intervalo[0] + 1) >= processo.tamanho):
                inicio_intervalo = intervalo[0]
                fim_intervalo = inicio_intervalo + processo.tamanho - 1 # processo.tamanho + inicio_intervalo + 1
                for i in range(inicio_intervalo, fim_intervalo + 1):
                    self.memoria_principal[i] = True
                processo.indice_inicial_mp = inicio_intervalo
                processo.indice_final_mp = processo.tamanho + inicio_intervalo
                processo.admitir()
                print(f"Processo {processo.identificador} foi alocado na Memória Principal no intervalo [{inicio_intervalo}, {fim_intervalo}]")
                return True
        if printarLogs:
            print(f"Processo {processo.identificador} não pode ser alocado na memória nesse momento")
        #processo.suspender()
        return False
    
    def remover_processo(self, processo: Process):
        for i in range(processo.indice_inicial_mp, processo.indice_final_mp):
            self.memoria_principal[i] = False
        #processo.suspender()
        processo.indice_final_mp = None
        processo.indice_inicial_mp = None

        self.atualiza_intervalos_livres()

        print(f"O processo {processo.identificador} foi removido da memória principal")
        return

    def finalizar_processo(self, processo: Process):
        for i in range(processo.indice_inicial_mp, processo.indice_final_mp):
            self.memoria_principal[i] = False

        processo.indice_final_mp = None
        processo.indice_inicial_mp = None

        # FALTOU ATUALIZAR OS INTERVALOS LIVRES AQUI
        self.atualiza_intervalos_livres()

        # print(f"Intervalos livres: {self.intervalos_livres}")
        print(f"O processo {processo.identificador} foi finalizado e removido da memória principal")
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

    def podeDesalocar(self, processoNovo: Process, processoAlocado: Process):
        tamanho_continuo_necessario = processoNovo.tamanho
        indice_inicial = processoAlocado.indice_inicial_mp
        indice_final = processoAlocado.indice_final_mp

        if (indice_inicial == None or indice_final == None):
            return False

        copia_memoria_principal = copy.deepcopy(self.memoria_principal)

        for i in range(indice_inicial, indice_final):
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

        print(f"DEBUG: Intervalos livres: {intervalos_livres}")
        print(f"DEBUG: Tamanhos dos intervalos livres: {[f'{intervalo[1] - intervalo[0] + 1}mb' for intervalo in intervalos_livres]}")

        intervalos_livres = sorted(intervalos_livres, key=lambda x: (x[1] - x[0]))

        for intervalo in intervalos_livres:
            if((intervalo[1] - intervalo[0] + 1) >= tamanho_continuo_necessario):
                return True
        return False