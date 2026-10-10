from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import Qt


class CopKutusuPenceresi(QDialog):
    """Silinen (yumuşak silinmiş) görevleri gösterir.

    Görevler buradan geri yüklenebilir veya kalıcı olarak silinebilir.
    30 günü dolan görevler uygulama açılışında otomatik temizlenir
    (bkz. VeriTabani._eski_silinenleri_temizle).
    """

    def __init__(self, gorev_yonetimi, parent=None):
        super().__init__(parent)
        self.gorev_yonetimi = gorev_yonetimi
        self.degisiklik_oldu = False

        self.setWindowTitle("Çöp Kutusu")
        self.resize(500, 350)

        self.bilgi_etiketi = QLabel(
            "Silinen görevler burada 30 gün saklanır, ardından kalıcı olarak silinir."
        )
        self.bilgi_etiketi.setWordWrap(True)

        self.liste = QListWidget()

        self.geri_yukle_butonu = QPushButton("Geri Yükle")
        self.kalici_sil_butonu = QPushButton("Kalıcı Olarak Sil")

        self.geri_yukle_butonu.clicked.connect(self.gorevi_geri_yukle)
        self.kalici_sil_butonu.clicked.connect(self.gorevi_kalici_sil)

        buton_duzeni = QHBoxLayout()
        buton_duzeni.addWidget(self.geri_yukle_butonu)
        buton_duzeni.addWidget(self.kalici_sil_butonu)

        duzen = QVBoxLayout()
        duzen.addWidget(self.bilgi_etiketi)
        duzen.addWidget(self.liste)
        duzen.addLayout(buton_duzeni)
        self.setLayout(duzen)

        self._listeyi_doldur()

    def _listeyi_doldur(self):
        self.liste.clear()
        for gorev in self.gorev_yonetimi.cop_kutusunu_getir():
            item = QListWidgetItem(f'{gorev["ad"]}  (silindi: {gorev["silinme_tarihi"]})')
            item.setData(Qt.ItemDataRole.UserRole, gorev["id"])
            self.liste.addItem(item)

    def _secili_id_al(self):
        item = self.liste.currentItem()
        if item is None:
            QMessageBox.information(self, "Görev Seçilmedi", "Önce bir görev seç.")
            return None
        return item.data(Qt.ItemDataRole.UserRole)

    def gorevi_geri_yukle(self):
        gorev_id = self._secili_id_al()
        if gorev_id is None:
            return

        self.gorev_yonetimi.gorev_geri_yukle(gorev_id)
        self.degisiklik_oldu = True
        self._listeyi_doldur()

    def gorevi_kalici_sil(self):
        gorev_id = self._secili_id_al()
        if gorev_id is None:
            return

        onay = QMessageBox.question(
            self,
            "Kalıcı Olarak Sil",
            "Bu görev kalıcı olarak silinecek ve geri alınamayacak. Devam edilsin mi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if onay != QMessageBox.StandardButton.Yes:
            return

        self.gorev_yonetimi.gorev_kalici_sil(gorev_id)
        self._listeyi_doldur()