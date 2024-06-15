from classes.process import Process
from classes.dispatcher import Dispatcher
import copy


class Interval():
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim
        self.prox = None

    def __str__(self):
        intervalo = self
        resp = "["
        while intervalo.prox != None:
            resp += f"[{intervalo.inicio}, {intervalo.fim}], "
            intervalo = intervalo.prox
        resp += f"[{intervalo.inicio}, {intervalo.fim}]]"
        return resp

class Memory():
    def __init__(self, capacidade_celula_mb = 1, capacidade_total_mb = 32000):
        # vetor que representa a memória principal. célula False representa endereços de memória que não estão ocupados por processo
        self.memoria_principal = [False for _ in range(int(capacidade_total_mb/capacidade_celula_mb))]
        #self.memoria_principal = [False] * 798 + [True] + [False] * 799 + [True] + [False] * 4000
        self.intervalos_livres = Interval(0, len(self.memoria_principal) - 1)
        #self.inicializa_intervalos_livres()
    
    def printIntervalosLivres(self):
        #self.atualiza_intervalos_livres()
        print(f"Intervalos livres: {self.intervalos_livres}")

    def gera_lista(self, intervalo: Interval):
        resp = []
        while intervalo is not None:
            resp.append([intervalo.inicio, intervalo.fim])
            intervalo = intervalo.prox
        return resp

    def admite_processo(self, processo: Process, printarLogs=True):
        # política best fit: achar o menor espaço contínuo possível para alocar o processo
        copia = copy.deepcopy(self.intervalos_livres)
        intervalos_livres = self.gera_lista(copia)

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
                
                # atualizar os intervalos livres na admissão de um processo na mp
                self.atualiza_intervalos_livres_na_admissao(inicio_intervalo, fim_intervalo)

                return True
        if printarLogs:
            print(f"Processo {processo.identificador} não pode ser alocado na memória nesse momento")
        #processo.suspender()
        return False
    
    def remover_processo(self, processo: Process):
        for i in range(processo.indice_inicial_mp, processo.indice_final_mp):
            self.memoria_principal[i] = False
        
        # atualizar os intervalos livres na remoção de um processo da mp
        self.atualiza_intervalos_livres_na_remocao(processo.indice_inicial_mp, processo.indice_final_mp)

        print(f"O processo {processo.identificador} foi removido da memória principal")
        return

    def finalizar_processo(self, processo: Process):
        for i in range(processo.indice_inicial_mp, processo.indice_final_mp):
            self.memoria_principal[i] = False
        print(f"O processo {processo.identificador} foi finalizado e removido da memória principal")

        # atualiza os intervalos livres na remoção de um processo da mp
        self.atualiza_intervalos_livres_na_remocao(processo.indice_inicial_mp, processo.indice_final_mp)

        return

    def inicializa_intervalos_livres(self):
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
    
    def atualiza_intervalos_livres_na_remocao(self, indice_inicial, indice_final):
        intervalo = self.intervalos_livres
        ant = None
        while intervalo is not None and (intervalo.fim < indice_inicial):
            ant = intervalo
            intervalo = intervalo.prox
        
        # não existe nenhum intervalo livre que termine depois do começo do processo que acabou de ser removido
        if intervalo is None:
            if ant is None: # a mp estava totalmente cheia. O único intervalo livre será aquele que antes era ocupado pelo processo
                self.intervalos_livres = Interval(indice_inicial, indice_final)
                self.intervalos_livres.prox = None
            else:
                # se o processo que acabou de ser removido era imediatamente adjacente ao último intervalo livre
                if ant.fim == (indice_inicial - 1):
                    ant.fim = indice_inicial
                # existe algum processo em andamento alocado entre o último intervalo livre e o processo que acabou de ser removido
                else:
                    novo_intervalo = Interval(indice_inicial, indice_final)
                    novo_intervalo.prox = ant.prox
                    ant.prox = novo_intervalo
        else:
            # se o processo que foi removido estava alocado antes do primeiro intervalo livre
            if ant is None:
                if (indice_final + 1 == intervalo.inicio):
                    intervalo.inicio = indice_inicial
                else:
                    novo_intervalo = Interval(indice_inicial, indice_final)
                    novo_intervalo.prox = intervalo
                    self.intervalos_livres = novo_intervalo
            else:
                # se o intervalo livre e o processo removido eram imediatamente adjacentes
                if intervalo.inicio == (indice_final + 1):
                    ant.fim = intervalo.fim
                    ant.prox = intervalo.prox
                    intervalo = None
                # existe algum processo alocado entre o processo removido e o intervalo livre
                else:
                    novo_intervalo = Interval(indice_inicial, indice_final)
                    novo_intervalo.prox = intervalo
                    ant.prox = novo_intervalo

    def atualiza_intervalos_livres_na_admissao(self, indice_inicial, indice_final):
        intervalo = self.intervalos_livres
        ant = None

        while intervalo is not None and (indice_inicial < intervalo.inicio):
            ant = intervalo
            intervalo = intervalo.prox
        
        # não existiam intervalos livres depois de onde o processo foi alocado
        if intervalo is None:
            # não é possível que isso aconteca, porque significaria que um processo foi admitido com a mp estando totalmente cheia
            if ant is None:
                pass
            # processo foi admitido em algum lugar depois do último intervalo livre
            else:
                # o processo foi admitido em um intervalo exatamente do seu tamanho
                if (ant.fim == indice_final) and (ant.inicio == indice_inicial):
                    ant = None
                # o processo foi admitido nas últimas posições do intervalo livre
                elif ant.fim == indice_final:
                    ant.fim = indice_inicial - 1
                # o processo foi admitido nas primeiras posições do intervalo livre
                elif ant.inicio == indice_inicial:
                    ant.inicio = indice_inicial + 1
                # o processo foi admitido no meio de um intervalo livre
                else:
                    novo_intervalo = Interval(indice_final + 1, ant.fim)
                    novo_intervalo.prox = None
                    ant.fim = indice_inicial - 1
                    ant.prox = novo_intervalo
        # o processo foi admitido antes do fim do último intervalo livre
        else:
            # o processo foi admitido antes do fim do primeiro intervalo livre
            if ant is None:
                # o processo foi alocado no início de um intervalo livre
                if indice_inicial == intervalo.inicio:
                    # o processo foi alocado em um espaço com exatamente o seu tamanho
                    if indice_final == intervalo.fim:
                        self.intervalos_livres = self.intervalos_livres.prox
                    else:
                        intervalo.inicio = indice_final + 1
                # o processo foi alocado no meio de um intervalo livre
                else:
                    novo_intervalo = Interval(intervalo.inicio, indice_inicial - 1)
                    novo_intervalo.prox = intervalo.prox
                    intervalo.inicio = indice_final + 1
                    self.intervalos_livres = novo_intervalo
            # o processo foi admitido depois do fim do primeiro intervalo livre
            else:
               if indice_inicial == intervalo.inicio:
                   intervalo.inicio = indice_final + 1
               else:
                   novo_intervalo = Interval(indice_final + 1, intervalo.fim)
                   novo_intervalo.prox = ant.prox
                   ant.fim = indice_inicial - 1
                   ant.prox = novo_intervalo
    
if __name__ == "__main__":
    a = Interval(1, 4)
    b = Interval(6, 10)
    a.prox = b
    print(a)