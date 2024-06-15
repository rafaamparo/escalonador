from classes.process import Process
from classes.dispatcher import Dispatcher

class LeitorArquivo:
    def __init__(self, caminho_arquivo, dispatcher, quantum, id_inicial = 1):
        self.caminho_arquivo = caminho_arquivo
        self.id_inicial = id_inicial
        self.dispatcher = dispatcher
        self.quantum = quantum
    
    def carregar_processos(self):
        processos = []
        with open(self.caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                valores = linha.strip().split(', ')
                t_chegada = int(valores[0])
                t_execucao_fase_1 = int(valores[1])
                t_disco = int(valores[2])
                t_execucao_fase_2 = int(valores[3])
                tamanho = int(valores[4])
                qtd_discos = int(valores[5])

                processo = Process(
                    id=self.id_inicial,
                    t_chegada = t_chegada, 
                    t_execucao_fase_1 = t_execucao_fase_1, 
                    t_disco = t_disco, 
                    t_execucao_fase_2 = t_execucao_fase_2, 
                    tamanho = tamanho, 
                    qtd_discos = qtd_discos,
                    dispatcher = self.dispatcher,
                    quantum = self.quantum
                    )
                processos.append(processo)
                self.id_inicial += 1

        return processos