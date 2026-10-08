
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QInputDialog,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

gorevler = []


def gorev_ekle():
    while True:
        gorev, tamam = QInputDialog.getText(
            pencere,
            "Yeni Görev",
            "Görev adını gir:"
        )

        if not tamam:
            return

        gorev = gorev.strip()

        if not gorev:
            QMessageBox.warning(
                pencere,
                "Geçersiz Görev",
                "Görev adı boş bırakılamaz!"
            )
            continue

        gorevler.append(gorev)

        item = QListWidgetItem(gorev)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Unchecked)
        gorev_listesi.addItem(item)
        break

def gorev_durumu_degisti(item):
    font = item.font()
    tamamlandi_mi = item.checkState() == Qt.CheckState.Checked
    font.setStrikeOut(tamamlandi_mi)
    item.setFont(font)

app = QApplication(sys.argv)

pencere = QWidget()
pencere.setWindowTitle("Görev Yöneticisi")
pencere.resize(600, 400)

bakiye_etiketi = QLabel("💎 Mücevher Bakiyesi: 1320")
gorev_butonu = QPushButton("Görev Ekle")
gorev_listesi = QListWidget()
gorev_listesi.itemChanged.connect(gorev_durumu_degisti)

gorev_butonu.clicked.connect(gorev_ekle)

duzen = QVBoxLayout()
duzen.addWidget(bakiye_etiketi)
duzen.addWidget(gorev_butonu)
duzen.addWidget(gorev_listesi)

pencere.setLayout(duzen)
pencere.show()

sys.exit(app.exec())