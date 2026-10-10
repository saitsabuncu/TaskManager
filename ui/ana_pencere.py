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
from ui.cop_kutusu_penceresi import CopKutusuPenceresi


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
        self.cop_kutusu_butonu = QPushButton("Çöp Kutusu")
        self.gorev_listesi = QListWidget()

        self.gorev_butonu.clicked.connect(self.gorev_ekle)
        self.guncelle_butonu.clicked.connect(self.gorev_guncelle)
        self.sil_butonu.clicked.connect(self.gorev_sil)
        self.cop_kutusu_butonu.clicked.connect(self.cop_kutusunu_ac)
        self.gorev_listesi.itemChanged.connect(self.gorev_durumu_degisti)

        duzen = QVBoxLayout()
        duzen.addWidget(self.bakiye_etiketi)
        duzen.addWidget(self.gorev_butonu)
        duzen.addWidget(self.guncelle_butonu)
        duzen.addWidget(self.sil_butonu)
        duzen.addWidget(self.cop_kutusu_butonu)
        duzen.addWidget(self.gorev_listesi)
        self.setLayout(duzen)

        self._listeyi_yenile()

    def _listeyi_yenile(self):
        # Listeyi gorev_yonetimi.gorevler ile tamamen yeniden doldurur
        # (ilk açılışta ve çöp kutusundan geri yükleme sonrası kullanılır).
        # itemChanged sinyalinin bu sırada tetiklenip gereksiz veritabanı
        # yazısı yapmaması için sinyalleri geçici kapatıyoruz.
        self.gorev_listesi.blockSignals(True)
        self.gorev_listesi.clear()
        for gorev in self.gorev_yonetimi.gorevler:
            item = self._liste_ogesi_olustur(gorev["ad"], gorev["tamamlandi"])
            self.gorev_listesi.addItem(item)
        self.gorev_listesi.blockSignals(False)

    def _liste_ogesi_olustur(self, ad: str, tamamlandi: bool) -> QListWidgetItem:
        item = QListWidgetItem(ad)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
            Qt.CheckState.Checked if tamamlandi else Qt.CheckState.Unchecked
        )
        if tamamlandi:
            font = item.font()
            font.setStrikeOut(True)
            item.setFont(font)
        return item

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

            item = self._liste_ogesi_olustur(eklenen["ad"], eklenen["tamamlandi"])
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
        mevcut_ad = self.gorev_yonetimi.gorevler[index]["ad"]

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
        gorev_adi = self.gorev_yonetimi.gorevler[index]["ad"]

        onay = QMessageBox.question(
            self,
            "Görevi Sil",
            f'"{gorev_adi}" görevi çöp kutusuna taşınacak (30 gün saklanır). '
            "Devam edilsin mi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if onay != QMessageBox.StandardButton.Yes:
            return

        self.gorev_yonetimi.gorev_sil(index)
        self.gorev_listesi.takeItem(index)

    def cop_kutusunu_ac(self):
        pencere = CopKutusuPenceresi(self.gorev_yonetimi, self)
        pencere.exec()

        # Çöp kutusundan geri yükleme sonrası listeyi yenile
        if pencere.degisiklik_oldu:
            self._listeyi_yenile()
         

    def gorev_durumu_degisti(self, item: QListWidgetItem):
        font = item.font()
        tamamlandi_mi = item.checkState() == Qt.CheckState.Checked
        font.setStrikeOut(tamamlandi_mi)
        item.setFont(font)

        index = self.gorev_listesi.row(item)
        self.gorev_yonetimi.gorev_tamamlanma_degistir(index, tamamlandi_mi)