
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

def gorev_ekle():
    print("Görev Ekle butonuna tıklandı!")

# Uygulamayı başlat
app = QApplication(sys.argv)

# Ana pencereyi oluştur
pencere = QWidget()
pencere.setWindowTitle("Görev Yöneticisi")
pencere.resize(600, 400)

# Mücevher bakiyesi yazısı
bakiye_etiketi = QLabel("💎 Mücevher Bakiyesi: 1320")

# Buton oluştur
gorev_butonu = QPushButton("Görev Ekle")

# Butona tıklama olayını bağla
gorev_butonu.clicked.connect(gorev_ekle)

# Arayüz düzeni oluştur
duzen = QVBoxLayout()
duzen.addWidget(bakiye_etiketi)
duzen.addWidget(gorev_butonu)

# Düzeni pencereye bağla
pencere.setLayout(duzen)

# Pencereyi göster
pencere.show()

# Uygulamayı çalıştır
sys.exit(app.exec())