import os
from classes.process import Process
from rich.console import Console

# ! Classe responsável por ler o arquivo de entrada e carregar os processos

class LeitorArquivo:
    def __init__(self, caminho_arquivo, quantum, memoria, id_inicial = 1):
        dir = os.path.realpath(".")
        self.localarquivo = (dir + caminho_arquivo)
        self.caminho_arquivo = caminho_arquivo
        self.id_inicial = id_inicial
        self.quantum = quantum
        self.memoria = memoria
    
    def carregar_processos(self):
        console = Console(stderr=True, style='bold red')
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

                pode_ignorar = False

                if t_execucao_fase_1 == 0 and t_disco == 0 and t_execucao_fase_2 == 0:
                    pode_ignorar = True
                    console.print(f'Processo {self.id_inicial} ignorado, pois não possui tempo de execução')
                elif t_execucao_fase_1 < 0 or t_disco < 0 or t_execucao_fase_2 < 0:
                    pode_ignorar = True
                    console.print(f'Processo {self.id_inicial} ignorado, pois possui tempo de execução negativo')
                elif t_execucao_fase_1 == 0:
                    pode_ignorar = True
                    console.print(f'Processo {self.id_inicial} ignorado, pois não possui tempo de execução na fase 1')
                elif t_disco > 0 and qtd_discos <= 0:
                    pode_ignorar = True
                    console.print(f'Processo {self.id_inicial} ignorado, pois possui tempo de E/S mas não especifica quantidade de discos válida')
                elif t_disco == 0 and qtd_discos > 0:
                    pode_ignorar = True
                    console.print(f'Processo {self.id_inicial} ignorado, pois não possui tempo de E/S mas especifica quantidade de discos')
                elif tamanho <= 0:
                    pode_ignorar = True
                    console.print(f'Processo {self.id_inicial} ignorado, pois possui tamanho inválido')
                elif tamanho > self.memoria:
                    pode_ignorar = True
                    console.print(f'Processo {self.id_inicial} ignorado, pois possui tamanho maior que a memória disponível')

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
                if (pode_ignorar == False):
                    processos.append(processo)
                self.id_inicial += 1

        return processos