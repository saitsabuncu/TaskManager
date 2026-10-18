from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class IstatistiklerPenceresi(QDialog):
    """Görev ve mücevher verilerinin özet grafiklerini gösterir (salt okunur)."""

    def __init__(self, gorev_yonetimi, parent=None):
        super().__init__(parent)
        self.gorev_yonetimi = gorev_yonetimi

        self.setWindowTitle("İstatistikler")
        self.resize(650, 450)

        veri = self.gorev_yonetimi.istatistikleri_getir()

        self.mucevher_etiketi = QLabel(
            f'💎 Toplam Kazanılan: {veri["mucevher_kazanilan"]}   |   '
            f'Toplam Harcanan: {veri["mucevher_harcanan"]}   |   '
            f'Güncel Bakiye: {veri["mucevher_bakiye"]}'
        )

        self.figure = Figure(figsize=(6, 3.5))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self._grafikleri_ciz(veri)

        duzen = QVBoxLayout()
        duzen.addWidget(self.mucevher_etiketi)
        duzen.addWidget(self.canvas)
        self.setLayout(duzen)

    def _grafikleri_ciz(self, veri: dict):
        pasta_ekseni = self.figure.add_subplot(1, 2, 1)
        cubuk_ekseni = self.figure.add_subplot(1, 2, 2)

        tamamlanan = veri["tamamlanan"]
        tamamlanmayan = veri["toplam"] - tamamlanan

        if veri["toplam"] > 0:
            pasta_ekseni.pie(
                [tamamlanan, tamamlanmayan],
                labels=["Tamamlanan", "Tamamlanmayan"],
                autopct="%1.0f%%",
                colors=["#3b82f6", "#d1d5db"],
            )
        else:
            pasta_ekseni.text(0.5, 0.5, "Görev yok", ha="center", va="center")
        pasta_ekseni.set_title("Tamamlanma Oranı")

        kategoriler = list(veri["kategori_dagilimi"].keys())
        sayilar = list(veri["kategori_dagilimi"].values())

        if kategoriler:
            cubuk_ekseni.bar(kategoriler, sayilar, color="#3b82f6")
            cubuk_ekseni.tick_params(axis="x", rotation=30)
        else:
            cubuk_ekseni.text(0.5, 0.5, "Görev yok", ha="center", va="center")
        cubuk_ekseni.set_title("Kategoriye Göre Dağılım")

        self.figure.tight_layout()