from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QInputDialog,
    QMessageBox,
)


class KategoriDuzenlemePenceresi(QDialog):
    """Sabit kategori listesindeki kategori adlarını yeniden adlandırmaya
    yarar. Bir kategori yeniden adlandırıldığında, o kategoriye sahip
    tüm görevler (aktif ve çöp kutusundakiler dahil) otomatik olarak
    yeni ada güncellenir.
    """

    def __init__(self, gorev_yonetimi, parent=None):
        super().__init__(parent)
        self.gorev_yonetimi = gorev_yonetimi
        self.degisiklik_oldu = False

        self.setWindowTitle("Kategorileri Düzenle")
        self.resize(400, 300)

        self.bilgi_etiketi = QLabel(
            "Bir kategoriyi yeniden adlandırmak, o kategorideki tüm "
            "görevleri de otomatik günceller."
        )
        self.bilgi_etiketi.setWordWrap(True)

        self.liste = QListWidget()
        self.yeniden_adlandir_butonu = QPushButton("Yeniden Adlandır")
        self.yeniden_adlandir_butonu.clicked.connect(self.kategoriyi_yeniden_adlandir)

        duzen = QVBoxLayout()
        duzen.addWidget(self.bilgi_etiketi)
        duzen.addWidget(self.liste)
        duzen.addWidget(self.yeniden_adlandir_butonu)
        self.setLayout(duzen)

        self._listeyi_doldur()

    def _listeyi_doldur(self):
        self.liste.clear()
        for kategori in self.gorev_yonetimi.kategoriler:
            self.liste.addItem(QListWidgetItem(kategori))

    def kategoriyi_yeniden_adlandir(self):
        secili_item = self.liste.currentItem()
        if secili_item is None:
            QMessageBox.information(
                self, "Kategori Seçilmedi", "Önce bir kategori seç."
            )
            return

        eski_ad = secili_item.text()

        while True:
            yeni_ad, tamam = QInputDialog.getText(
                self,
                "Kategoriyi Yeniden Adlandır",
                "Yeni kategori adı:",
                text=eski_ad,
            )

            if not tamam:
                return

            try:
                self.gorev_yonetimi.kategori_adini_guncelle(eski_ad, yeni_ad)
            except ValueError as hata:
                QMessageBox.warning(self, "Geçersiz Kategori Adı", str(hata))
                continue

            self.degisiklik_oldu = True
            self._listeyi_doldur()
            break