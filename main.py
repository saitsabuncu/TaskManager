
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QInputDialog,
    QMessageBox,
)

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
        gorev_listesi.setText("\n".join(gorevler))
        break


app = QApplication(sys.argv)

pencere = QWidget()
pencere.setWindowTitle("Görev Yöneticisi")
pencere.resize(600, 400)

bakiye_etiketi = QLabel("💎 Mücevher Bakiyesi: 1320")
gorev_butonu = QPushButton("Görev Ekle")
gorev_listesi = QLabel("Henüz görev eklenmedi.")

gorev_butonu.clicked.connect(gorev_ekle)

duzen = QVBoxLayout()
duzen.addWidget(bakiye_etiketi)
duzen.addWidget(gorev_butonu)
duzen.addWidget(gorev_listesi)

pencere.setLayout(duzen)
pencere.show()

sys.exit(app.exec())