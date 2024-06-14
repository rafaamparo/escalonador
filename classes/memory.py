from classes.process import Process
from classes.dispatcher import Dispatcher

class Memory():
    def __init__(self, capacidade_celula_mb = 1, capacidade_total_mb = 32000):
        # vetor que representa a memória principal. célula False representa endereços de memória que não estão ocupados por processo
        self.memoria_principal = [False for _ in range(int(capacidade_total_mb/capacidade_celula_mb))]
        self.memoria_principal = [False] * 798 + [True] + [False] * 799 + [True] + [False] * 4000
    
    def admite_processo(self, processo: Process):
        # achar o menor espaço contínuo possível para alocar o processo
        intervalos_livres = []
        inicio_intervalo = 0
        fim_intervalo = 0
        for i in range(len(self.memoria_principal)):
            if self.memoria_principal[i] == False:
                fim_intervalo = i
            else:
                if fim_intervalo != inicio_intervalo:
                    intervalos_livres.append([inicio_intervalo, fim_intervalo])
                inicio_intervalo = i+1
                fim_intervalo = i+1
        
        if fim_intervalo != inicio_intervalo:
            intervalos_livres.append([inicio_intervalo, fim_intervalo])
        
        intervalos_livres = sorted(intervalos_livres, key=lambda x: (x[1] - x[0]))

        print(f"Intervalos livres: {intervalos_livres}")
        for intervalo in intervalos_livres:
            if((intervalo[1] - intervalo[0]) >= processo.tamanho):
                inicio_intervalo = intervalo[0]
                fim_intervalo = inicio_intervalo + processo.tamanho
                for i in range(inicio_intervalo, processo.tamanho + inicio_intervalo + 1):
                    self.memoria_principal[i] = True
                processo.indice_inicial_mp = inicio_intervalo
                processo.indice_final_mp = processo.tamanho + inicio_intervalo
                processo.admitir()
                print(f"O processo {processo.identificador} foi alocado na memória entre as posições {inicio_intervalo} e {fim_intervalo}")
                return True
        
        print(f"O processo {processo.identificador} não pode ser alocado na memória nesse momento")
        processo.suspender()
        return False
    
    def remover_processo(self, processo: Process):
        for i in range(processo.indice_inicial_mp, processo.indice_final_mp + 1):
            self.memoria_principal[i] = False
        processo.suspender()
        print(f"O processo {processo.identificador} foi removido da memória principal")
        return

    def finalizar_processo(self, processo: Process):
        for i in range(processo.indice_inicial_mp, processo.indice_final_mp + 1):
            self.memoria_principal[i] = False
        print(f"O processo {processo.identificador} foi finalizado e removido da memória principal")
        return