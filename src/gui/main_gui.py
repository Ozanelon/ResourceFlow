import sys
import sys
import psutil
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QUrl
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
#        self.setWindowIcon(QIcon("icon.ico"))  # Burada 'icon.ico' yerine ikon dosyanızın yolunu yazın.
        self.setWindowTitle("ResourceFlow")  # İsim güncellendi
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        # CPU, RAM ve Disk kullanımını gösterecek animasyonlar
        self.cpu_usage = 0
        self.ram_usage = 0
        self.disk_usage = 0

        # Timer ile sürekli güncelleme yapma (interval 500ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_usage)
        self.timer.start(500)  # Interval kısaltıldı, 500 ms

        # Başlangıç animasyonu
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setStartValue(QPoint(100, 100))
        self.animation.setEndValue(QPoint(200, 100))
        self.animation.setDuration(1500)
        self.animation.start()

        # Font ayarları
        self.font = QFont()
        self.font.setPointSize(12)

        # Ozanelon yazısı için özel font
        self.ozanelon_font = QFont("Arial", 16, QFont.Bold)

    def update_usage(self):
        # Sistem kaynaklarını al
        self.cpu_usage = round(psutil.cpu_percent(interval=0.5), 1)  # Round yapıldı
        self.ram_usage = round(psutil.virtual_memory().percent, 1)  # Round yapıldı
        self.disk_usage = round(psutil.disk_usage('/').percent, 1)  # Round yapıldı
        self.update()  # Ekranı yeniden çiz

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Arka plan rengi
        painter.fillRect(self.rect(), QColor(30, 30, 30))

        # Widget genişlik ve yükseklik bilgisi
        width = self.width()
        height = self.height()

        # Çubukların yer alacağı kutu
        box_x, box_y, box_width, box_height = 50, 50, width - 100, 200
        painter.setBrush(QColor(50, 50, 50))  # Kutu rengi
        painter.drawRect(box_x, box_y, box_width, box_height)  # Düz kutu

        # CPU kullanımını göster
        cpu_width = int(self.cpu_usage / 100 * (width - 100))  # Genişliği orantılayarak hesapla
        painter.setBrush(QColor(0, 255, 0))  # Yeşil renk
        painter.drawRect(50, 100, cpu_width, 30)

        # RAM kullanımını göster
        ram_width = int(self.ram_usage / 100 * (width - 100))  # Genişliği orantılayarak hesapla
        painter.setBrush(QColor(0, 0, 255))  # Mavi renk
        painter.drawRect(50, 150, ram_width, 30)

        # Disk kullanımını göster
        disk_width = int(self.disk_usage / 100 * (width - 100))  # Genişliği orantılayarak hesapla
        painter.setBrush(QColor(255, 165, 0))  # Turuncu renk
        painter.drawRect(50, 200, disk_width, 30)

        # Yazıları düzgün yerleştir
        painter.setPen(QColor(255, 255, 255))  # Beyaz renk
        painter.setFont(self.font)

        # CPU metni
        painter.drawText(width // 2 - 100, 120, f"CPU Usage: {self.cpu_usage}%")

        # RAM metni
        painter.drawText(width // 2 - 100, 170, f"RAM Usage: {self.ram_usage}%")

        # Disk metni
        painter.drawText(width // 2 - 100, 220, f"Disk Usage: {self.disk_usage}%")

        # Alt kısımda yazıyı ekle (Ozanelon ve Github linki)
        painter.setFont(self.ozanelon_font)
        painter.drawText(width // 2 - 50, height - 50, "Ozanelon")

        # Github linkini ekle
        painter.setFont(QFont("Arial", 10))
        painter.setPen(QColor(0, 255, 255))  # Mavi renk
        painter.drawText(width // 2 - 60, height - 30, "github.com/Ozanelon")

        painter.end()

    def mousePressEvent(self, event):
        # Fare tıklamasını kontrol et
        if event.pos().x() > self.width() // 2 - 110 and event.pos().x() < self.width() // 2 + 110 and \
           event.pos().y() > self.height() - 20 and event.pos().y() < self.height():
            QDesktopServices.openUrl(QUrl("https://github.com/Ozanelon"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec_())
