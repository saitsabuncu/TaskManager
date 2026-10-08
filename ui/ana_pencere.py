from PyQt6.QtWidgets import (
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

from logic.gorev_yonetimi import GorevYonetimi


class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.gorev_yonetimi = GorevYonetimi()

        self.setWindowTitle("Görev Yöneticisi")
        self.resize(600, 400)

        self.bakiye_etiketi = QLabel(
            f"💎 Mücevher Bakiyesi: {self.gorev_yonetimi.mucevher_bakiyesi}"
        )
        self.gorev_butonu = QPushButton("Görev Ekle")
        self.gorev_listesi = QListWidget()

        self.gorev_butonu.clicked.connect(self.gorev_ekle)
        self.gorev_listesi.itemChanged.connect(self.gorev_durumu_degisti)

        duzen = QVBoxLayout()
        duzen.addWidget(self.bakiye_etiketi)
        duzen.addWidget(self.gorev_butonu)
        duzen.addWidget(self.gorev_listesi)
        self.setLayout(duzen)

    def gorev_ekle(self):
        while True:
            gorev, tamam = QInputDialog.getText(
                self,
                "Yeni Görev",
                "Görev adını gir:"
            )

            if not tamam:
                return

            try:
                eklenen = self.gorev_yonetimi.gorev_ekle(gorev)
            except ValueError as hata:
                QMessageBox.warning(self, "Geçersiz Görev", str(hata))
                continue

            item = QListWidgetItem(eklenen)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.gorev_listesi.addItem(item)
            break

    def gorev_durumu_degisti(self, item: QListWidgetItem):
        font = item.font()
        tamamlandi_mi = item.checkState() == Qt.CheckState.Checked
        font.setStrikeOut(tamamlandi_mi)
        item.setFont(font)