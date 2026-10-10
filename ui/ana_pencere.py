from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QInputDialog,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QComboBox,
)
from PyQt6.QtCore import Qt

from logic.gorev_yonetimi import GorevYonetimi
from ui.cop_kutusu_penceresi import CopKutusuPenceresi
from ui.kategori_duzenleme_penceresi import KategoriDuzenlemePenceresi

TUM_KATEGORILER = "Tümü"


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
        self.kategori_tasi_butonu = QPushButton("Kategori Taşı")
        self.kategorileri_duzenle_butonu = QPushButton("Kategorileri Düzenle")
        self.cop_kutusu_butonu = QPushButton("Çöp Kutusu")
        self.gorev_listesi = QListWidget()

        self.kategori_etiketi = QLabel("Kategori Filtresi:")
        self.kategori_filtresi = QComboBox()

        self.gorev_butonu.clicked.connect(self.gorev_ekle)
        self.guncelle_butonu.clicked.connect(self.gorev_guncelle)
        self.sil_butonu.clicked.connect(self.gorev_sil)
        self.kategori_tasi_butonu.clicked.connect(self.kategori_tasi)
        self.kategorileri_duzenle_butonu.clicked.connect(self.kategorileri_duzenle)
        self.cop_kutusu_butonu.clicked.connect(self.cop_kutusunu_ac)
        self.gorev_listesi.itemChanged.connect(self.gorev_durumu_degisti)
        self.kategori_filtresi.currentTextChanged.connect(self.filtreyi_uygula)

        filtre_duzeni = QHBoxLayout()
        filtre_duzeni.addWidget(self.kategori_etiketi)
        filtre_duzeni.addWidget(self.kategori_filtresi)

        duzen = QVBoxLayout()
        duzen.addWidget(self.bakiye_etiketi)
        duzen.addWidget(self.gorev_butonu)
        duzen.addWidget(self.guncelle_butonu)
        duzen.addWidget(self.sil_butonu)
        duzen.addWidget(self.kategori_tasi_butonu)
        duzen.addWidget(self.kategorileri_duzenle_butonu)
        duzen.addWidget(self.cop_kutusu_butonu)
        duzen.addLayout(filtre_duzeni)
        duzen.addWidget(self.gorev_listesi)
        self.setLayout(duzen)

        self._kategori_filtresini_doldur()
        self._listeyi_yenile()

    def _kategori_filtresini_doldur(self):
        # Mevcut seçimi koru (varsa), kategori listesi değiştiğinde de
        # (örn. yeniden adlandırma sonrası) tutarlı kalsın.
        mevcut_secim = self.kategori_filtresi.currentText()

        self.kategori_filtresi.blockSignals(True)
        self.kategori_filtresi.clear()
        self.kategori_filtresi.addItem(TUM_KATEGORILER)
        self.kategori_filtresi.addItems(self.gorev_yonetimi.kategoriler)

        if mevcut_secim in self.gorev_yonetimi.kategoriler or mevcut_secim == TUM_KATEGORILER:
            self.kategori_filtresi.setCurrentText(mevcut_secim)
        else:
            self.kategori_filtresi.setCurrentText(TUM_KATEGORILER)
        self.kategori_filtresi.blockSignals(False)

    def _listeyi_yenile(self):
        # Listeyi gorev_yonetimi.gorevler ile tamamen yeniden doldurur
        # (ilk açılışta, kategori işlemleri ve çöp kutusundan geri yükleme
        # sonrası kullanılır). itemChanged sinyalinin bu sırada tetiklenip
        # gereksiz veritabanı yazısı yapmaması için sinyalleri geçici
        # kapatıyoruz.
        self.gorev_listesi.blockSignals(True)
        self.gorev_listesi.clear()
        for gorev in self.gorev_yonetimi.gorevler:
            item = self._liste_ogesi_olustur(
                gorev["ad"], gorev["tamamlandi"], gorev["kategori"]
            )
            self.gorev_listesi.addItem(item)
        self.gorev_listesi.blockSignals(False)
        self.filtreyi_uygula(self.kategori_filtresi.currentText())

    def _liste_ogesi_olustur(
        self, ad: str, tamamlandi: bool, kategori: str
    ) -> QListWidgetItem:
        item = QListWidgetItem(f"{ad}  [{kategori}]")
        item.setData(Qt.ItemDataRole.UserRole, kategori)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
            Qt.CheckState.Checked if tamamlandi else Qt.CheckState.Unchecked
        )
        if tamamlandi:
            font = item.font()
            font.setStrikeOut(True)
            item.setFont(font)
        return item

    def filtreyi_uygula(self, secilen_kategori: str):
        for i in range(self.gorev_listesi.count()):
            item = self.gorev_listesi.item(i)
            kategori = item.data(Qt.ItemDataRole.UserRole)
            gizli = secilen_kategori != TUM_KATEGORILER and kategori != secilen_kategori
            item.setHidden(gizli)

    def gorev_ekle(self):
        while True:
            gorev, tamam = QInputDialog.getText(
                self,
                "Yeni Görev",
                "Görev adını gir:"
            )

            if not tamam:
                return

            kategori, kategori_tamam = QInputDialog.getItem(
                self,
                "Kategori Seç",
                "Görevin kategorisi:",
                self.gorev_yonetimi.kategoriler,
                0,
                False,
            )
            if not kategori_tamam:
                kategori = self.gorev_yonetimi.kategoriler[0]

            try:
                eklenen = self.gorev_yonetimi.gorev_ekle(gorev, kategori)
            except ValueError as hata:
                QMessageBox.warning(self, "Geçersiz Görev", str(hata))
                continue

            item = self._liste_ogesi_olustur(
                eklenen["ad"], eklenen["tamamlandi"], eklenen["kategori"]
            )
            self.gorev_listesi.addItem(item)
            self.filtreyi_uygula(self.kategori_filtresi.currentText())
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
        kategori = self.gorev_yonetimi.gorevler[index]["kategori"]

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

            secili_item.setText(f"{guncellenen}  [{kategori}]")
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

    def kategori_tasi(self):
        secili_item = self.gorev_listesi.currentItem()
        if secili_item is None:
            QMessageBox.information(
                self,
                "Görev Seçilmedi",
                "Taşımak için önce bir görev seç."
            )
            return

        index = self.gorev_listesi.row(secili_item)
        gorev = self.gorev_yonetimi.gorevler[index]
        mevcut_kategori = gorev["kategori"]

        mevcut_index = (
            self.gorev_yonetimi.kategoriler.index(mevcut_kategori)
            if mevcut_kategori in self.gorev_yonetimi.kategoriler
            else 0
        )

        yeni_kategori, tamam = QInputDialog.getItem(
            self,
            "Kategori Taşı",
            f'"{gorev["ad"]}" görevini hangi kategoriye taşımak istersin?',
            self.gorev_yonetimi.kategoriler,
            mevcut_index,
            False,
        )

        if not tamam or yeni_kategori == mevcut_kategori:
            return

        self.gorev_yonetimi.gorev_kategorisini_degistir(index, yeni_kategori)

        secili_item.setText(f'{gorev["ad"]}  [{yeni_kategori}]')
        secili_item.setData(Qt.ItemDataRole.UserRole, yeni_kategori)
        self.filtreyi_uygula(self.kategori_filtresi.currentText())

    def kategorileri_duzenle(self):
        pencere = KategoriDuzenlemePenceresi(self.gorev_yonetimi, self)
        pencere.exec()

        if pencere.degisiklik_oldu:
            self._kategori_filtresini_doldur()
            self._listeyi_yenile()

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