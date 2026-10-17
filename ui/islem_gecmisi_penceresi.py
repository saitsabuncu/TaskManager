from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
)

from data.veritabani import ISLEM_GECMISI_SAKLAMA_GUNU


class IslemGecmisiPenceresi(QDialog):
    """Görev, kategori ve mağaza işlemlerinin salt okunur dökümünü gösterir.

    Kayıtlar en yeniden en eskiye sıralanır ve ISLEM_GECMISI_SAKLAMA_GUNU gün
    sonra uygulama açılışında otomatik temizlenir
    (bkz. VeriTabani._eski_islemleri_temizle).
    """

    def __init__(self, gorev_yonetimi, parent=None):
        super().__init__(parent)
        self.gorev_yonetimi = gorev_yonetimi

        self.setWindowTitle("İşlem Geçmişi")
        self.resize(550, 400)

        self.bilgi_etiketi = QLabel(
            f"İşlemler en yeniden en eskiye sıralanır ve "
            f"{ISLEM_GECMISI_SAKLAMA_GUNU} gün sonra otomatik temizlenir."
        )
        self.bilgi_etiketi.setWordWrap(True)

        self.liste = QListWidget()

        duzen = QVBoxLayout()
        duzen.addWidget(self.bilgi_etiketi)
        duzen.addWidget(self.liste)
        self.setLayout(duzen)

        self._listeyi_doldur()

    def _listeyi_doldur(self):
        self.liste.clear()
        for islem in self.gorev_yonetimi.islem_gecmisini_getir():
            item = QListWidgetItem(f'[{islem["tarih"]}] {islem["aciklama"]}')
            self.liste.addItem(item)