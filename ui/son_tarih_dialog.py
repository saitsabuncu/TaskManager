from __future__ import annotations

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QCheckBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class SonTarihDialog(QDialog):
    """Görev için opsiyonel son tarih seçtiren diyalog.

    "Son tarih yok" kutusu işaretliyken tarih seçici devre dışı kalır;
    bu durumda secilen_tarih() None döner.
    """

    def __init__(
        self,
        baslik: str,
        mevcut_tarih: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(baslik)

        self._tarih_yok_kutusu = QCheckBox("Son tarih yok")
        self._tarih_secici = QDateEdit()
        self._tarih_secici.setCalendarPopup(True)
        self._tarih_secici.setDate(
            QDate.fromString(mevcut_tarih, "yyyy-MM-dd")
            if mevcut_tarih
            else QDate.currentDate()
        )

        self._tarih_yok_kutusu.setChecked(mevcut_tarih is None)
        self._tarih_secici.setEnabled(mevcut_tarih is not None)
        self._tarih_yok_kutusu.toggled.connect(
            lambda isaretli: self._tarih_secici.setEnabled(not isaretli)
        )

        butonlar = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        butonlar.accepted.connect(self.accept)
        butonlar.rejected.connect(self.reject)

        duzen = QVBoxLayout(self)
        duzen.addWidget(QLabel("Görevin son tarihi:"))
        duzen.addWidget(self._tarih_secici)
        duzen.addWidget(self._tarih_yok_kutusu)
        duzen.addWidget(butonlar)

    def secilen_tarih(self) -> str | None:
        if self._tarih_yok_kutusu.isChecked():
            return None
        return self._tarih_secici.date().toString("yyyy-MM-dd")