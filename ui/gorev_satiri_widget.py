from __future__ import annotations

from datetime import date

from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QWidget

# Kategori POZİSYONUNA göre renk (bkz. logic/kategori_onerici.py'deki aynı
# mantık: 0=Genel, 1=İş, 2=Kişisel, 3=Alışveriş, 4=Sağlık). Kategori adı
# yeniden adlandırılsa bile pozisyon sabit kaldığından renk bozulmaz.
_KATEGORI_RENKLERI: list[tuple[str, str]] = [
    ("#64748b", "#f1f5f9"),  # Genel
    ("#4f46e5", "#eef2ff"),  # İş
    ("#9333ea", "#f3e8ff"),  # Kişisel
    ("#ea580c", "#fff7ed"),  # Alışveriş
    ("#059669", "#ecfdf5"),  # Sağlık
]
_VARSAYILAN_RENK = _KATEGORI_RENKLERI[0]
_ONCELIK_RENKLERI: dict[int, tuple[str, str]] = {
    1: ("#64748b", "#f1f5f9"),  # Düşük
    2: ("#b45309", "#fffbeb"),  # Orta
    3: ("#dc2626", "#fef2f2"),  # Yüksek
}

class GorevSatiriWidget(QWidget):
    """Görev listesindeki tek bir satırı temsil eder.

    Kategori adını düz metin yerine renkli bir rozet (pill) olarak
    göstermek QListWidgetItem'ın yerleşik metin/checkbox desteğiyle
    mümkün olmadığından (tek satır = tek renkte düz metin), bu satırda
    kendi checkbox'ımızı ve etiketlerimizi kullanırız (bkz.
    ui/ana_pencere.py _satir_ekle / _satiri_guncelle).
    """

    tamamlanma_degisti = pyqtSignal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("gorevSatiri")
        self.setMinimumHeight(44)

        self._checkbox = QCheckBox()
        self._ad_etiketi = QLabel()
        self._seri_etiketi = QLabel()
        self._seri_etiketi.setObjectName("seriEtiketi")
        self._son_tarih_etiketi = QLabel()
        self._son_tarih_etiketi.setObjectName("sonTarihEtiketi")
        self._oncelik_rozeti = QLabel()

        self._kategori_rozeti = QLabel()
        self._kategori_rozeti.setObjectName("kategoriRozeti")

        self._checkbox.toggled.connect(self.tamamlanma_degisti.emit)

        duzen = QHBoxLayout(self)
        duzen.setContentsMargins(10, 6, 10, 6)
        duzen.setSpacing(10)
        duzen.addWidget(self._checkbox)
        duzen.addWidget(self._ad_etiketi, 1)
        duzen.addWidget(self._seri_etiketi)
        duzen.addWidget(self._son_tarih_etiketi)
        duzen.addWidget(self._oncelik_rozeti)
        duzen.addWidget(self._kategori_rozeti)

    def sizeHint(self) -> QSize:
        # Yükseklik her zaman sabit 44px döner; bu sayede ana_pencere.py
        # içindeki item.setSizeHint(widget.sizeHint()) çağrısı, widget
        # içeriği/layout'u henüz tam yerleşmemişken bile satırdan satıra
        # farklı bir değer üretmez. setMinimumHeight(44) sadece bir alt
        # sınırdı; asıl kullanılan değer bu metoddan gelir.
        taban_boyut = super().sizeHint()
        return QSize(taban_boyut.width(), 44)

    def gorevi_goster(
        self,
        ad: str,
        kategori_adi: str,
        kategori_indeksi: int,
        tamamlandi: bool,
        tekrarlanan: bool,
        seri: int,
        oncelik: int,
        oncelik_etiketi: str,
        son_tarih: str | None,
        gecikmis: bool,
    ) -> None:
        self._checkbox.blockSignals(True)
        self._checkbox.setChecked(tamamlandi)
        self._checkbox.blockSignals(False)

        font = self._ad_etiketi.font()
        font.setStrikeOut(tamamlandi)
        self._ad_etiketi.setFont(font)
        self._ad_etiketi.setStyleSheet("color: #a2a9ba;" if tamamlandi else "")
        self._ad_etiketi.setText(ad)

        self._seri_etiketi.setText(
            (f"↻ {seri} gün" if seri > 0 else "↻") if tekrarlanan else ""
        )

        renk_metin, renk_zemin = (
            _KATEGORI_RENKLERI[kategori_indeksi]
            if 0 <= kategori_indeksi < len(_KATEGORI_RENKLERI)
            else _VARSAYILAN_RENK
        )
        self._kategori_rozeti.setText(kategori_adi)
        self._kategori_rozeti.setStyleSheet(
            f"QLabel#kategoriRozeti {{"
            f"color: {renk_metin};"
            f"background-color: {renk_zemin};"
            f"border-radius: 9px;"
            f"padding: 3px 10px;"
            f"font-size: 8pt;"
            f"font-weight: 600;"
            f"}}"
        )
        renk_metin_o, renk_zemin_o = _ONCELIK_RENKLERI.get(
            oncelik, _ONCELIK_RENKLERI[2]
        )
        self._oncelik_rozeti.setText(oncelik_etiketi)
        self._oncelik_rozeti.setStyleSheet(
            f"QLabel#oncelikRozeti {{"
            f"color: {renk_metin_o};"
            f"background-color: {renk_zemin_o};"
            f"border-radius: 9px;"
            f"padding: 3px 10px;"
            f"font-size: 8pt;"
            f"font-weight: 600;"
            f"}}"
        )

        if son_tarih:
            tarih_metni = date.fromisoformat(son_tarih).strftime("%d.%m.%Y")
            self._son_tarih_etiketi.setText(f"📅 {tarih_metni}")
            self._son_tarih_etiketi.setStyleSheet(
                "color: #dc2626; font-weight: 600;" if gecikmis else "color: #64748b;"
            )
        else:
            self._son_tarih_etiketi.setText("")
            self._son_tarih_etiketi.setStyleSheet("") 


    def tamamlanma_durumunu_degistir(self) -> None:
        self._checkbox.toggle()           