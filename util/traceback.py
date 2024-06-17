from rich.console import Console
from rich.table import Table

# ! Classe que gera a tabela de execução dos processos
class Traceback():
    def __init__(self, fila_de_processos):
        self.dadosDoEscalonamento = []
        self.finalizacaoProcessos = []
        self.fila_de_processos = fila_de_processos


    def adicionar_finalizacao(self, processo, tempo):
        self.finalizacaoProcessos.append({
            "processo": processo.identificador,
            "tempo": tempo
        })

    def print_tabela(self):
        table = Table(title="Escalonador de Processos", show_lines=True, style="yellow")
        table.add_column("Processo", justify="center", style="magenta", no_wrap=True)

        for ciclo in self.dadosDoEscalonamento:
            table.add_column(f"{ciclo['tempo']}", justify="center", style="red", no_wrap=True)

        for processo in self.fila_de_processos:
            table.add_row(f"P{processo.identificador}", *[f"{'X' if processo.identificador in ciclo['executando'] else ''}" for ciclo in self.dadosDoEscalonamento])

        
        console = Console()
        console.print(table, justify="center")
        console.print("")

    def print_tnormalizado(self):
        console = Console()
        info_processos = {}
        for processo in self.fila_de_processos:
            info_processos[processo.identificador] = {
                "first": None,
                "last": None,
                "chegada": processo.t_chegada,
                "tservico": processo.t_total_execucao
            }
        
        for ciclo in self.dadosDoEscalonamento:
            for processo in ciclo["executando"]:
                if info_processos[processo]["first"] is None:
                    info_processos[processo]["first"] = ciclo["tempo"]
                info_processos[processo]["last"] = ciclo["tempo"]+1


        table = Table(title="Tempo Normalizado", style="yellow", show_lines=True)
        table.add_column("Processo", justify="center", style="magenta", no_wrap=True)
        table.add_column("Tempo Chegada", justify="center", style="red", no_wrap=True)
        table.add_column("Tempo Saída", justify="center", style="red", no_wrap=True)
        table.add_column("Tempo Serviço", justify="center", style="red", no_wrap=True)
        table.add_column("Turnaround", justify="center", style="red", no_wrap=True)
        table.add_column("Tempo Normalizado", justify="center", style="red", no_wrap=True)

        for processo in info_processos:
            lastExecution = None
            for finalizacao in self.finalizacaoProcessos:
                if finalizacao["processo"] == processo:
                    lastExecution = finalizacao["tempo"]
                    break


            turnaround = (lastExecution - info_processos[processo]["chegada"])
            tempo_normalizado = turnaround / info_processos[processo]["tservico"]
            table.add_row(f"P{processo}", 
                          f"{info_processos[processo]['chegada']}", 
                          f"{lastExecution}", 
                          f"{info_processos[processo]['tservico']}", 
                          f"{'%.0f' % turnaround}", 
                          f"{'%.2f' % tempo_normalizado}"
                          )

        console.print(table, justify="center")