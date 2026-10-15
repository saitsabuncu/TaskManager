from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QInputDialog,
    QMessageBox,
)


class MagazaPenceresi(QDialog):
    """Mücevherlerin harcandığı ödül mağazasını gösterir.

    Kullanıcı kendi ödüllerini ekleyip düzenleyebilir ve silebilir; bir
    ödülü satın almak mücevher bakiyesinden maliyeti kadar düşer. Bakiye
    yetersizse satın alma reddedilir.
    """

    def __init__(self, gorev_yonetimi, parent=None):
        super().__init__(parent)
        self.gorev_yonetimi = gorev_yonetimi
        self.degisiklik_oldu = False

        self.setWindowTitle("Mağaza")
        self.resize(450, 400)

        self.bakiye_etiketi = QLabel(
            f"💎 Mücevher Bakiyesi: {self.gorev_yonetimi.mucevher_bakiyesi}"
        )

        self.liste = QListWidget()

        self.satin_al_butonu = QPushButton("Satın Al")
        self.odul_ekle_butonu = QPushButton("Ödül Ekle")
        self.duzenle_butonu = QPushButton("Düzenle")
        self.sil_butonu = QPushButton("Sil")

        self.satin_al_butonu.clicked.connect(self.odulu_satin_al)
        self.odul_ekle_butonu.clicked.connect(self.odul_ekle)
        self.duzenle_butonu.clicked.connect(self.odulu_duzenle)
        self.sil_butonu.clicked.connect(self.odulu_sil)

        buton_duzeni = QHBoxLayout()
        buton_duzeni.addWidget(self.odul_ekle_butonu)
        buton_duzeni.addWidget(self.duzenle_butonu)
        buton_duzeni.addWidget(self.sil_butonu)

        duzen = QVBoxLayout()
        duzen.addWidget(self.bakiye_etiketi)
        duzen.addWidget(self.liste)
        duzen.addWidget(self.satin_al_butonu)
        duzen.addLayout(buton_duzeni)
        self.setLayout(duzen)

        self._listeyi_doldur()

    def _listeyi_doldur(self):
        self.liste.clear()
        for odul in self.gorev_yonetimi.oduller:
            item = QListWidgetItem(f'{odul["ad"]}  —  {odul["mucevher_maliyeti"]} 💎')
            self.liste.addItem(item)

    def _bakiye_etiketini_guncelle(self):
        self.bakiye_etiketi.setText(
            f"💎 Mücevher Bakiyesi: {self.gorev_yonetimi.mucevher_bakiyesi}"
        )

    def _secili_index_al(self):
        item = self.liste.currentItem()
        if item is None:
            QMessageBox.information(self, "Ödül Seçilmedi", "Önce bir ödül seç.")
            return None
        return self.liste.row(item)

    def odulu_satin_al(self):
        index = self._secili_index_al()
        if index is None:
            return

        odul = self.gorev_yonetimi.oduller[index]

        onay = QMessageBox.question(
            self,
            "Ödülü Satın Al",
            f'"{odul["ad"]}" ödülünü {odul["mucevher_maliyeti"]} 💎 '
            "karşılığında satın almak istiyor musun?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if onay != QMessageBox.StandardButton.Yes:
            return

        try:
            satin_alinan = self.gorev_yonetimi.odul_satin_al(index)
        except ValueError as hata:
            QMessageBox.warning(self, "Yetersiz Bakiye", str(hata))
            return

        self.degisiklik_oldu = True
        self._bakiye_etiketini_guncelle()
        QMessageBox.information(
            self,
            "Afiyet Olsun!",
            f'"{satin_alinan["ad"]}" ödülünü satın aldın, tebrikler!',
        )

    def odul_ekle(self):
        while True:
            ad, tamam = QInputDialog.getText(self, "Yeni Ödül", "Ödül adı:")
            if not tamam:
                return

            maliyet, tamam2 = QInputDialog.getInt(
                self, "Yeni Ödül", "Mücevher maliyeti:", 50, 1, 1_000_000
            )
            if not tamam2:
                return

            try:
                self.gorev_yonetimi.odul_ekle(ad, maliyet)
            except ValueError as hata:
                QMessageBox.warning(self, "Geçersiz Ödül", str(hata))
                continue

            self.degisiklik_oldu = True
            self._listeyi_doldur()
            break

    def odulu_duzenle(self):
        index = self._secili_index_al()
        if index is None:
            return

        odul = self.gorev_yonetimi.oduller[index]

        while True:
            ad, tamam = QInputDialog.getText(
                self, "Ödülü Düzenle", "Ödül adı:", text=odul["ad"]
            )
            if not tamam:
                return

            maliyet, tamam2 = QInputDialog.getInt(
                self,
                "Ödülü Düzenle",
                "Mücevher maliyeti:",
                odul["mucevher_maliyeti"],
                1,
                1_000_000,
            )
            if not tamam2:
                return

            try:
                self.gorev_yonetimi.odul_guncelle(index, ad, maliyet)
            except ValueError as hata:
                QMessageBox.warning(self, "Geçersiz Ödül", str(hata))
                continue

            self.degisiklik_oldu = True
            self._listeyi_doldur()
            break

    def odulu_sil(self):
        index = self._secili_index_al()
        if index is None:
            return

        odul = self.gorev_yonetimi.oduller[index]

        onay = QMessageBox.question(
            self,
            "Ödülü Sil",
            f'"{odul["ad"]}" ödülü mağazadan kalıcı olarak silinecek. '
            "Devam edilsin mi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if onay != QMessageBox.StandardButton.Yes:
            return

        self.gorev_yonetimi.odul_sil(index)
        self.degisiklik_oldu = True
        self._listeyi_doldur()