from rich.console import Console
from rich.table import Table


class Traceback():
    def __init__(self, fila_de_processos):
        self.dadosDoEscalonamento = []
        self.fila_de_processos = fila_de_processos

    def print_tabela(self):
        table = Table(title="Escalonador de Processos", show_lines=True, style="yellow")
        table.add_column("Processo", justify="center", style="magenta", no_wrap=True)

        for ciclo in self.dadosDoEscalonamento:
            table.add_column(f"{ciclo['tempo']}", justify="center", style="red", no_wrap=True)

        for processo in self.fila_de_processos:
            table.add_row(f"P{processo.identificador}", *[f"{'X' if processo.identificador in ciclo['executando'] else ''}" for ciclo in self.dadosDoEscalonamento])

        
        console = Console()
        console.print(table)
