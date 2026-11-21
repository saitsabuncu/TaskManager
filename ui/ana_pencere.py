from typing import Callable

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
    QToolButton,
    QMenu,
)
from PyQt6.QtCore import Qt

from logic.gorev_yonetimi import GorevYonetimi
from ui.cop_kutusu_penceresi import CopKutusuPenceresi
from ui.kategori_duzenleme_penceresi import KategoriDuzenlemePenceresi
from ui.magaza_penceresi import MagazaPenceresi
from ui.islem_gecmisi_penceresi import IslemGecmisiPenceresi
from ui.istatistikler_penceresi import IstatistiklerPenceresi

from logic.kategori_onerici import kategori_tahmin_et
from logic.kategori_onerici import kategori_tahmin_et
from ui.gorev_satiri_widget import GorevSatiriWidget
from ui.animasyonlu_buton import AnimasyonluButon

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
        self.hosgeldin_etiketi.setObjectName("hosgeldinEtiketi")
        self.bakiye_etiketi = QLabel(
            f"💎 Mücevher Bakiyesi: {self.gorev_yonetimi.mucevher_bakiyesi}"
        )
        self.bakiye_etiketi.setObjectName("bakiyeEtiketi")
        self.gorev_butonu = QPushButton("Görev Ekle")
        self.gorev_butonu.setProperty("role", "primary")
        self.gorev_listesi = QListWidget()

        self.kategori_etiketi = QLabel("Kategori Filtresi:")
        self.kategori_filtresi = QComboBox()

        self.gorev_butonu.clicked.connect(self.gorev_ekle)
        self.kategori_filtresi.currentTextChanged.connect(self.filtreyi_uygula)

        gorev_islemleri_butonu = self._menu_butonu_olustur(
            "Görev İşlemleri",
            [
                ("Görev Güncelle", self.gorev_guncelle),
                ("Görev Sil", self.gorev_sil),
                ("Kategori Taşı", self.kategori_tasi),
                ("Tekrarı Aç/Kapat", self.tekrar_durumunu_degistir),
            ],
        )

        yonetim_butonu = self._menu_butonu_olustur(
            "Yönetim",
            [
                ("Kategorileri Düzenle", self.kategorileri_duzenle),
                ("Mağaza", self.magazayi_ac),
                ("Çöp Kutusu", self.cop_kutusunu_ac),
                ("İşlem Geçmişi", self.islem_gecmisini_ac),
                ("İstatistikler", self.istatistikleri_ac),
            ],
        )

        arac_cubugu_duzeni = QHBoxLayout()
        arac_cubugu_duzeni.addWidget(self.gorev_butonu)
        arac_cubugu_duzeni.addWidget(gorev_islemleri_butonu)
        arac_cubugu_duzeni.addWidget(yonetim_butonu)
        arac_cubugu_duzeni.addStretch()

        filtre_duzeni = QHBoxLayout()
        filtre_duzeni.addWidget(self.kategori_etiketi)
        filtre_duzeni.addWidget(self.kategori_filtresi)

        duzen = QVBoxLayout()
        duzen.addWidget(self.hosgeldin_etiketi)
        duzen.addWidget(self.bakiye_etiketi)
        duzen.addLayout(arac_cubugu_duzeni)
        duzen.addLayout(filtre_duzeni)
        duzen.addWidget(self.gorev_listesi)
        self.setLayout(duzen)

        self._kategori_filtresini_doldur()
        self._listeyi_yenile()

    def _menu_butonu_olustur(
        self, baslik: str, eylemler: list[tuple[str, Callable[[], None]]]
    ) -> QToolButton:
        # Birden fazla eylemi tek bir açılır menü butonunda toplar; araç
        # çubuğunun yeni özelliklerle büyüdükçe buton çöplüğüne
        # dönüşmesini engeller (bkz. QToolButton/QMenu stil.qss kuralları).
        buton = QToolButton()
        buton.setText(f"{baslik} ▾")
        buton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        menu = QMenu(buton)
        for etiket, islev in eylemler:
            menu.addAction(etiket, islev)
        buton.setMenu(menu)

        return buton

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
        # sonrası kullanılır).
        self.gorev_listesi.clear()
        for _ in self.gorev_yonetimi.gorevler:
            self._satir_ekle()
        self.filtreyi_uygula(self.kategori_filtresi.currentText())

    def _satir_ekle(self) -> QListWidgetItem:
        # Yeni, boş bir satır oluşturup listeye ekler; görünür içeriği
        # hemen ardından _satiri_guncelle ile doldurur (tek kaynak,
        # tekrar yok).
        item = QListWidgetItem()
        self.gorev_listesi.addItem(item)

        widget = GorevSatiriWidget()
        widget.tamamlanma_degisti.connect(
            lambda tamamlandi_mi, oge=item: self._satir_tamamlandi_degisti(
                oge, tamamlandi_mi
            )
        )
        self.gorev_listesi.setItemWidget(item, widget)

        self._satiri_guncelle(item)
        return item

    def _satiri_guncelle(self, item: QListWidgetItem) -> None:
        # Bir satırın görünümünü gorev_yonetimi.gorevler'deki güncel
        # veriyle yeniden çizer. Görev güncelleme, kategori taşıma,
        # tekrar durumu değişikliği ve tamamlanma değişikliğinin hepsi
        # bu tek metoda yönlenir.
        index = self.gorev_listesi.row(item)
        gorev = self.gorev_yonetimi.gorevler[index]
        widget: GorevSatiriWidget = self.gorev_listesi.itemWidget(item)

        kategori_indeksi = (
            self.gorev_yonetimi.kategoriler.index(gorev["kategori"])
            if gorev["kategori"] in self.gorev_yonetimi.kategoriler
            else -1
        )
        seri = (
            self.gorev_yonetimi.gorev_serisini_hesapla(gorev["id"])
            if gorev["tekrarlanan"]
            else 0
        )

        widget.gorevi_goster(
            gorev["ad"],
            gorev["kategori"],
            kategori_indeksi,
            gorev["tamamlandi"],
            gorev["tekrarlanan"],
            seri,
        )
        item.setData(Qt.ItemDataRole.UserRole, gorev["kategori"])
        item.setSizeHint(widget.sizeHint())

    

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

            onerilen_kategori = kategori_tahmin_et(gorev, self.gorev_yonetimi.kategoriler)
            baslangic_index = (
                self.gorev_yonetimi.kategoriler.index(onerilen_kategori)
                if onerilen_kategori
                else 0
            )
            etiket = (
                f"🤖 AI önerisi: {onerilen_kategori}\n\nGörevin kategorisi:"
                if onerilen_kategori
                else "Görevin kategorisi:"
            )

            kategori, kategori_tamam = QInputDialog.getItem(
                self,
                "Kategori Seç",
                etiket,
                self.gorev_yonetimi.kategoriler,
                baslangic_index,
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

            self._satir_ekle()
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

                
                self._satiri_guncelle(secili_item)
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

        self._satiri_guncelle(secili_item)
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

        self._satiri_guncelle(secili_item)

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

    def _satir_tamamlandi_degisti(self, item: QListWidgetItem, tamamlandi_mi: bool) -> None:
        index = self.gorev_listesi.row(item)
        self.gorev_yonetimi.gorev_tamamlanma_degistir(index, tamamlandi_mi)
        self._bakiye_etiketini_guncelle()
        self._satiri_guncelle(item)

    def _bakiye_etiketini_guncelle(self):
        self.bakiye_etiketi.setText(
            f"💎 Mücevher Bakiyesi: {self.gorev_yonetimi.mucevher_bakiyesi}"
        )

    
    def istatistikleri_ac(self):
        pencere = IstatistiklerPenceresi(self.gorev_yonetimi, self)
        pencere.exec()    