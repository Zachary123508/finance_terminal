from rich.console import Console
import os
from datetime import datetime

console = Console()

def log_action(command, result_summary):
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", f"log_{datetime.now().date()}.txt")
    with open(log_path, "a") as log:
        log.write(f"{datetime.now()} | {command} | {result_summary}\n")

def print_table(title, data_dict):
    from rich.table import Table
    table = Table(title=title)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")
    for k, v in data_dict.items():
        table.add_row(str(k), str(v))
    console.print(table)
