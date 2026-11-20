from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QPushButton, QWidget


class AnimasyonluButon(QPushButton):
    """Metni, fare üzerine geldiğinde soluk renkten canlı (vurgu) renge
    yumuşakça geçen, fare uzaklaştığında da yumuşakça soluklaşan buton.

    QSS'in :hover durumu rengi anında değiştirir; burada bunun yerine
    0.0-1.0 arası bir "vurgu şiddeti" değerini QPropertyAnimation ile
    animasyonlayıp, iki renk arasında enterpolasyon yaparak metin
    rengini kendimiz (widget'a özel stylesheet ile) güncelliyoruz.
    """

    def __init__(
        self,
        metin: str = "",
        sonuk_renk: str = "#8b93a7",
        canli_renk: str = "#4338ca",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metin, parent)
        self._sonuk_renk = QColor(sonuk_renk)
        self._canli_renk = QColor(canli_renk)
        self._vurgu_siddeti: float = 0.0

        self._animasyon = QPropertyAnimation(self, b"vurguSiddeti", self)
        self._animasyon.setDuration(160)
        self._animasyon.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._metin_rengini_uygula(0.0)

    def _vurgu_siddeti_al(self) -> float:
        return self._vurgu_siddeti

    def _vurgu_siddeti_yaz(self, deger: float) -> None:
        self._vurgu_siddeti = deger
        self._metin_rengini_uygula(deger)

    vurguSiddeti = pyqtProperty(float, _vurgu_siddeti_al, _vurgu_siddeti_yaz)

    def _metin_rengini_uygula(self, oran: float) -> None:
        kirmizi = round(
            self._sonuk_renk.red() + (self._canli_renk.red() - self._sonuk_renk.red()) * oran
        )
        yesil = round(
            self._sonuk_renk.green() + (self._canli_renk.green() - self._sonuk_renk.green()) * oran
        )
        mavi = round(
            self._sonuk_renk.blue() + (self._canli_renk.blue() - self._sonuk_renk.blue()) * oran
        )
        self.setStyleSheet(f"color: rgb({kirmizi}, {yesil}, {mavi});")

    def _animasyonu_baslat(self, hedef: float) -> None:
        self._animasyon.stop()
        self._animasyon.setStartValue(self._vurgu_siddeti)
        self._animasyon.setEndValue(hedef)
        self._animasyon.start()

    def enterEvent(self, event) -> None:
        self._animasyonu_baslat(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._animasyonu_baslat(0.0)
        super().leaveEvent(event)