import os
from classes.process import Process

# ! Classe responsável por ler o arquivo de entrada e carregar os processos

class LeitorArquivo:
    def __init__(self, caminho_arquivo, quantum, id_inicial = 1):
        dir = os.path.realpath(".")
        self.localarquivo = (dir + caminho_arquivo)
        self.caminho_arquivo = caminho_arquivo
        self.id_inicial = id_inicial
        self.quantum = quantum
    
    def carregar_processos(self):
        processos = []
        with open(self.localarquivo, 'r') as arquivo:
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
                    quantum = self.quantum
                    )
                processos.append(processo)
                self.id_inicial += 1

        return processos