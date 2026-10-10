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
        self.guncelle_butonu = QPushButton("Görev Güncelle")
        self.sil_butonu = QPushButton("Görev Sil")
        self.gorev_listesi = QListWidget()

        self.gorev_butonu.clicked.connect(self.gorev_ekle)
        self.guncelle_butonu.clicked.connect(self.gorev_guncelle)
        self.sil_butonu.clicked.connect(self.gorev_sil)
        self.gorev_listesi.itemChanged.connect(self.gorev_durumu_degisti)

        duzen = QVBoxLayout()
        duzen.addWidget(self.bakiye_etiketi)
        duzen.addWidget(self.gorev_butonu)
        duzen.addWidget(self.guncelle_butonu)
        duzen.addWidget(self.sil_butonu)
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

    def gorev_guncelle(self):
        secili_item = self.gorev_listesi.currentItem()
        if secili_item is None:
            QMessageBox.information(
                self,
                "Görev Seçilmedi",
                "Güncellemek için önce bir görev seç."
            )
            return

        index = self.gorev_listesi.row(secili_item)
        mevcut_ad = self.gorev_yonetimi.gorevler[index]

        while True:
            yeni_ad, tamam = QInputDialog.getText(
                self,
                "Görevi Güncelle",
                "Yeni görev adı:",
                text=mevcut_ad,
            )

            if not tamam:
                return

            try:
                guncellenen = self.gorev_yonetimi.gorev_guncelle(index, yeni_ad)
            except ValueError as hata:
                QMessageBox.warning(self, "Geçersiz Görev", str(hata))
                continue

            secili_item.setText(guncellenen)
            break    

    def gorev_sil(self):
        secili_item = self.gorev_listesi.currentItem()
        if secili_item is None:
            QMessageBox.information(
                self,
                "Görev Seçilmedi",
                "Silmek için önce bir görev seç."
            )
            return
        index = self.gorev_listesi.row(secili_item)
        gorev_adi = self.gorev_yonetimi.gorevler[index]

        onay = QMessageBox.question(
            self,
            "Görevi Sil",
            f"'{gorev_adi}' görevini silmek istediğine emin misin?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if onay != QMessageBox.StandardButton.Yes:
            return
        self.gorev_yonetimi.gorev_sil(index)
        self.gorev_listesi.takeItem(index)
        
    def gorev_durumu_degisti(self, item: QListWidgetItem):
        font = item.font()
        tamamlandi_mi = item.checkState() == Qt.CheckState.Checked
        font.setStrikeOut(tamamlandi_mi)
        item.setFont(font)