from process import Process
from dispatcher import Dispatcher

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
                inicio_intervalo = i
                fim_intervalo = i
        
        if fim_intervalo != inicio_intervalo:
            intervalos_livres.append([inicio_intervalo, fim_intervalo])
        
        intervalos_livres = sorted(intervalos_livres, key=lambda x: (x[1] - x[0]))

        for intervalo in intervalos_livres:
            if((intervalo[1] - intervalo[0]) >= processo.tamanho):
                inicio_intervalo = intervalo[0]
                fim_intervalo = inicio_intervalo + processo.tamanho
                for i in range(inicio_intervalo, fim_intervalo):
                    self.memoria_principal[i] = True
                processo.indice_inicial_mp = inicio_intervalo
                processo.indice_final_mp = fim_intervalo
                processo.admitir()
                print(f"O processo {processo.identificador} foi alocado na memória entre as posições {inicio_intervalo} e {fim_intervalo}")
                return True
        
        print(f"O processo {processo.identificador} não pode ser alocado na memória nesse momento")
        return False
    
    def remover_processo(self, processo: Process):
        pass




def main():
    memoria = Memory()
    processo1 = Process(
        id=1,
        t_chegada=0,
        t_execucao_fase_1=4,
        t_disco=3,
        t_execucao_fase_2=6,
        tamanho=800,
        qtd_discos=2,
        quantum=3,
        dispatcher=Dispatcher([], [], [])
    )
    memoria.admite_processo(processo1)
    
if __name__ == '__main__':
    main()