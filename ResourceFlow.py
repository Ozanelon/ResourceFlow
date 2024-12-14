import psutil
import time
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel

# Konsol çıktısı
console = Console()

def display_system_info():
    progress = Progress()
    cpu_bar = progress.add_task("[cyan]CPU Kullanımı", total=100)
    ram_bar = progress.add_task("[green]RAM Kullanımı", total=100)
    disk_bar = progress.add_task("[magenta]Disk Kullanımı", total=100)

    while True:
        # Sistem bilgilerini al
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        # Animasyonlu güncellemeler
        progress.update(cpu_bar, completed=cpu_usage)
        progress.update(ram_bar, completed=ram_usage)
        progress.update(disk_bar, completed=disk_usage)

        # Ekranı temizle
        console.clear()

        # Panel ile şık gösterim
        console.print(Panel(f"CPU: {cpu_usage}%"))
        console.print(Panel(f"RAM: {ram_usage}%"))
        console.print(Panel(f"Disk: {disk_usage}%"))

        time.sleep(1)

if __name__ == '__main__':
    display_system_info()
