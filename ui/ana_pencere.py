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
from ui.magaza_penceresi import MagazaPenceresi
from ui.islem_gecmisi_penceresi import IslemGecmisiPenceresi
# import bloğuna ekle:
from ui.istatistikler_penceresi import IstatistiklerPenceresi

TUM_KATEGORILER = "Tümü"


class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.gorev_yonetimi = GorevYonetimi()

        self.setWindowTitle("Görev Yöneticisi")
        self.resize(600, 400)

        self._kullanici_adini_gerekirse_sor()

        self.hosgeldin_etiketi = QLabel(
            f"👋 Hoş geldiniz, {self.gorev_yonetimi.kullanici_adi}!"
        )
        self.bakiye_etiketi = QLabel(
            f"💎 Mücevher Bakiyesi: {self.gorev_yonetimi.mucevher_bakiyesi}"
        )
        self.gorev_butonu = QPushButton("Görev Ekle")
        self.guncelle_butonu = QPushButton("Görev Güncelle")
        self.sil_butonu = QPushButton("Görev Sil")
        self.kategori_tasi_butonu = QPushButton("Kategori Taşı")
        self.tekrar_butonu = QPushButton("Tekrarı Aç/Kapat")
        self.kategorileri_duzenle_butonu = QPushButton("Kategorileri Düzenle")
        self.magaza_butonu = QPushButton("Mağaza")
        self.cop_kutusu_butonu = QPushButton("Çöp Kutusu")
        self.islem_gecmisi_butonu = QPushButton("İşlem Geçmişi")
        self.istatistikler_butonu = QPushButton("İstatistikler")
        self.gorev_listesi = QListWidget()
        self.gorev_listesi.setStyleSheet(
            """
            QListWidget::item:selected {
                background-color: #3b82f6;
                color: white;
            }
            QListWidget::item:selected:!active {
                background-color: #93c5fd;
                color: black;
            }
            """
        )

        self.kategori_etiketi = QLabel("Kategori Filtresi:")
        self.kategori_filtresi = QComboBox()

        self.gorev_butonu.clicked.connect(self.gorev_ekle)
        self.guncelle_butonu.clicked.connect(self.gorev_guncelle)
        self.sil_butonu.clicked.connect(self.gorev_sil)
        self.kategori_tasi_butonu.clicked.connect(self.kategori_tasi)
        self.tekrar_butonu.clicked.connect(self.tekrar_durumunu_degistir)
        self.kategorileri_duzenle_butonu.clicked.connect(self.kategorileri_duzenle)
        self.magaza_butonu.clicked.connect(self.magazayi_ac)
        self.cop_kutusu_butonu.clicked.connect(self.cop_kutusunu_ac)
        self.islem_gecmisi_butonu.clicked.connect(self.islem_gecmisini_ac)
        self.istatistikler_butonu.clicked.connect(self.istatistikleri_ac)
        self.gorev_listesi.itemChanged.connect(self.gorev_durumu_degisti)
        self.kategori_filtresi.currentTextChanged.connect(self.filtreyi_uygula)

        gorev_buton_duzeni = QHBoxLayout()
        gorev_buton_duzeni.addWidget(self.gorev_butonu)
        gorev_buton_duzeni.addWidget(self.guncelle_butonu)
        gorev_buton_duzeni.addWidget(self.sil_butonu)
        gorev_buton_duzeni.addWidget(self.kategori_tasi_butonu)
        gorev_buton_duzeni.addWidget(self.tekrar_butonu)
        

        yonetim_buton_duzeni = QHBoxLayout()
        yonetim_buton_duzeni.addWidget(self.kategorileri_duzenle_butonu)
        yonetim_buton_duzeni.addWidget(self.magaza_butonu)
        yonetim_buton_duzeni.addWidget(self.cop_kutusu_butonu)
        yonetim_buton_duzeni.addWidget(self.islem_gecmisi_butonu)
        yonetim_buton_duzeni.addWidget(self.istatistikler_butonu)

        filtre_duzeni = QHBoxLayout()
        filtre_duzeni.addWidget(self.kategori_etiketi)
        filtre_duzeni.addWidget(self.kategori_filtresi)

        duzen = QVBoxLayout()
        duzen.addWidget(self.hosgeldin_etiketi)
        duzen.addWidget(self.bakiye_etiketi)
        duzen.addLayout(gorev_buton_duzeni)
        duzen.addLayout(yonetim_buton_duzeni)
        duzen.addLayout(filtre_duzeni)
        duzen.addWidget(self.gorev_listesi)
        self.setLayout(duzen)

        self._kategori_filtresini_doldur()
        self._listeyi_yenile()

    def _kullanici_adini_gerekirse_sor(self):
        # İlk açılışta kullanıcı adı henüz kaydedilmemişse sorulur; bir kere
        # girildikten sonra veritabanında kalıcı saklanır ve bir daha sorulmaz.
        while self.gorev_yonetimi.kullanici_adi is None:
            ad, tamam = QInputDialog.getText(
                self,
                "Hoş Geldiniz",
                "Uygulamayı kullanmaya başlamadan önce adınızı girin:",
            )

            if not tamam:
                ad = "Misafir"

            try:
                self.gorev_yonetimi.kullanici_adini_kaydet(ad)
            except ValueError as hata:
                QMessageBox.warning(self, "Geçersiz Ad", str(hata))

    def _gorev_sec_dialog(self, baslik: str, mesaj: str) -> int | None:
        # Mevcut görevlerden birini seçtirmek için kullanılan ortak yardımcı.
        # Aynı isimli görevler olabileceğinden listede id de gösterilir.
        if not self.gorev_yonetimi.gorevler:
            return None

        secenekler = [
            f'{"🔁 " if gorev["tekrarlanan"] else ""}{gorev["ad"]}  '
            f'[{gorev["kategori"]}]  (#{gorev["id"]})'
            for gorev in self.gorev_yonetimi.gorevler
        ]

        secim, tamam = QInputDialog.getItem(
            self, baslik, mesaj, secenekler, 0, False
        )

        if not tamam:
            return None

        return secenekler.index(secim)

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
                gorev["ad"],
                gorev["tamamlandi"],
                gorev["kategori"],
                gorev["tekrarlanan"],
                gorev["id"],
            )
            self.gorev_listesi.addItem(item)
        self.gorev_listesi.blockSignals(False)
        self.filtreyi_uygula(self.kategori_filtresi.currentText())

    def _gorev_metni_olustur(
        self, ad: str, kategori: str, tekrarlanan: bool, gorev_id: int | None = None
    ) -> str:
        on_ek = ""
        if tekrarlanan:
            seri = (
                self.gorev_yonetimi.gorev_serisini_hesapla(gorev_id)
                if gorev_id is not None
                else 0
            )
            on_ek = f"↻ ({seri} gün) " if seri > 0 else "↻ "
        return f"{on_ek}{ad}  [{kategori}]"

    def _liste_ogesi_olustur(
        self,
        ad: str,
        tamamlandi: bool,
        kategori: str,
        tekrarlanan: bool = False,
        gorev_id: int | None = None,
    ) -> QListWidgetItem:
        item = QListWidgetItem(
            self._gorev_metni_olustur(ad, kategori, tekrarlanan, gorev_id)
        )
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

    # gorev_ekle metodunu değiştir (kategori seçiminden sonra tekrar sorusu eklendi):
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

            tekrar_yaniti = QMessageBox.question(
                self,
                "Günlük Tekrar",
                "Bu görev her gün tekrar etsin mi?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            tekrarlanan = tekrar_yaniti == QMessageBox.StandardButton.Yes

            try:
                eklenen = self.gorev_yonetimi.gorev_ekle(gorev, kategori, tekrarlanan)
            except ValueError as hata:
                QMessageBox.warning(self, "Geçersiz Görev", str(hata))
                continue

            item = self._liste_ogesi_olustur(
                eklenen["ad"],
                eklenen["tamamlandi"],
                eklenen["kategori"],
                eklenen["tekrarlanan"],
                eklenen["id"],
            )
            self.gorev_listesi.addItem(item)
            self.filtreyi_uygula(self.kategori_filtresi.currentText())

            devam = QMessageBox.question(
                self,
                "Görev Eklendi",
                "Yeni bir görev eklemek ister misiniz?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if devam != QMessageBox.StandardButton.Yes:
                return

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

        while True:
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

                on_ek = (
                    "🔁 " if self.gorev_yonetimi.gorevler[index]["tekrarlanan"] else ""
                )
                secili_item.setText(self._gorev_metni_olustur(
                        guncellenen,
                        kategori,
                        self.gorev_yonetimi.gorevler[index]["tekrarlanan"],
                        self.gorev_yonetimi.gorevler[index]["id"],
                    ))
                break

            devam = QMessageBox.question(
                self,
                "Görev Güncellendi",
                "Başka bir görev güncellemek ister misiniz?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if devam != QMessageBox.StandardButton.Yes:
                return

            yeni_index = self._gorev_sec_dialog(
                "Görev Seç", "Güncellemek istediğiniz görevi seçin:"
            )
            if yeni_index is None:
                return

            index = yeni_index
            secili_item = self.gorev_listesi.item(index)

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

        while True:
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

            if not self.gorev_yonetimi.gorevler:
                QMessageBox.information(
                    self, "Çöp Kutusu'na Taşındı", "Silinecek başka görev kalmadı."
                )
                return

            devam = QMessageBox.question(
                self,
                "Başka Görev Sil",
                "Başka bir görev silmek ister misiniz?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if devam != QMessageBox.StandardButton.Yes:
                return

            yeni_index = self._gorev_sec_dialog(
                "Görev Seç", "Silmek istediğiniz görevi seçin:"
            )
            if yeni_index is None:
                return

            index = yeni_index

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

        secili_item.setText(
            self._gorev_metni_olustur(
                gorev["ad"], yeni_kategori, gorev["tekrarlanan"], gorev["id"]
            )
        )
        secili_item.setData(Qt.ItemDataRole.UserRole, yeni_kategori)
        self.filtreyi_uygula(self.kategori_filtresi.currentText())

    # Yeni metod (kategori_tasi metodundan sonra):
    def tekrar_durumunu_degistir(self):
        secili_item = self.gorev_listesi.currentItem()
        if secili_item is None:
            QMessageBox.information(
                self,
                "Görev Seçilmedi",
                "Tekrar durumunu değiştirmek için önce bir görev seç."
            )
            return

        index = self.gorev_listesi.row(secili_item)
        gorev = self.gorev_yonetimi.gorevler[index]
        yeni_durum = not gorev["tekrarlanan"]

        self.gorev_yonetimi.gorev_tekrarlanmasini_degistir(index, yeni_durum)

        secili_item.setText(
            self._gorev_metni_olustur(
                gorev["ad"], gorev["kategori"], yeni_durum, gorev["id"]
            )
        )

        QMessageBox.information(
            self,
            "Tekrar Durumu Güncellendi",
            f'"{gorev["ad"]}" görevi artık '
            f'{"her gün tekrar ediyor." if yeni_durum else "tekrar etmiyor."}'
        )    

    def kategorileri_duzenle(self):
        pencere = KategoriDuzenlemePenceresi(self.gorev_yonetimi, self)
        pencere.exec()

        if pencere.degisiklik_oldu:
            self._kategori_filtresini_doldur()
            self._listeyi_yenile()

    def magazayi_ac(self):
        pencere = MagazaPenceresi(self.gorev_yonetimi, self)
        pencere.exec()

        # Satın alma sonrası bakiyeyi ana penceredeki etikette de güncelle
        if pencere.degisiklik_oldu:
            self._bakiye_etiketini_guncelle()        

    def cop_kutusunu_ac(self):
        pencere = CopKutusuPenceresi(self.gorev_yonetimi, self)
        pencere.exec()

        # Çöp kutusundan geri yükleme sonrası listeyi yenile
        if pencere.degisiklik_oldu:
            self._listeyi_yenile()

    def islem_gecmisini_ac(self):
        pencere = IslemGecmisiPenceresi(self.gorev_yonetimi, self)
        pencere.exec()

    def gorev_durumu_degisti(self, item: QListWidgetItem):
        font = item.font()
        tamamlandi_mi = item.checkState() == Qt.CheckState.Checked
        font.setStrikeOut(tamamlandi_mi)
        item.setFont(font)

        index = self.gorev_listesi.row(item)
        self.gorev_yonetimi.gorev_tamamlanma_degistir(index, tamamlandi_mi)
        self._bakiye_etiketini_guncelle()

        gorev = self.gorev_yonetimi.gorevler[index]
        item.setText(
            self._gorev_metni_olustur(
                gorev["ad"], gorev["kategori"], gorev["tekrarlanan"], gorev["id"]
            )
        )

    def _bakiye_etiketini_guncelle(self):
        self.bakiye_etiketi.setText(
            f"💎 Mücevher Bakiyesi: {self.gorev_yonetimi.mucevher_bakiyesi}"
        )

    
    def istatistikleri_ac(self):
        pencere = IstatistiklerPenceresi(self.gorev_yonetimi, self)
        pencere.exec()    