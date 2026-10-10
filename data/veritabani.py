from __future__ import annotations

import sqlite3
from pathlib import Path

VARSAYILAN_DB_YOLU = Path(__file__).resolve().parent.parent / "gorevler.db"


class VeriTabani:
    """Görevlerin SQLite üzerinde kalıcı saklanmasından sorumlu katman.

    UI ve iş mantığı katmanlarından bağımsızdır; sadece satır okuma/yazma
    yapar. Görev sırası eklenme sırasına (id) göre korunur.
    """

    def __init__(self, db_yolu: Path | str = VARSAYILAN_DB_YOLU):
        self.db_yolu = str(db_yolu)
        self._tablolari_olustur()

    def _baglanti_ac(self) -> sqlite3.Connection:
        baglanti = sqlite3.connect(self.db_yolu)
        baglanti.execute("PRAGMA foreign_keys = ON")
        return baglanti

    def _tablolari_olustur(self):
        with self._baglanti_ac() as baglanti:
            baglanti.execute(
                """
                CREATE TABLE IF NOT EXISTS gorevler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ad TEXT NOT NULL,
                    tamamlandi INTEGER NOT NULL DEFAULT 0,
                    olusturulma_tarihi TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def tum_gorevleri_getir(self) -> list[tuple[int, str, bool]]:
        with self._baglanti_ac() as baglanti:
            satirlar = baglanti.execute(
                "SELECT id, ad, tamamlandi FROM gorevler ORDER BY id ASC"
            ).fetchall()
        return [(id_, ad, bool(tamamlandi)) for id_, ad, tamamlandi in satirlar]

    def gorev_ekle(self, ad: str) -> int:
        with self._baglanti_ac() as baglanti:
            imlec = baglanti.execute(
                "INSERT INTO gorevler (ad, tamamlandi) VALUES (?, 0)",
                (ad,),
            )
            return imlec.lastrowid

    def gorev_guncelle(self, gorev_id: int, yeni_ad: str):
        with self._baglanti_ac() as baglanti:
            baglanti.execute(
                "UPDATE gorevler SET ad = ? WHERE id = ?",
                (yeni_ad, gorev_id),
            )

    def gorev_durumu_guncelle(self, gorev_id: int, tamamlandi: bool):
        with self._baglanti_ac() as baglanti:
            baglanti.execute(
                "UPDATE gorevler SET tamamlandi = ? WHERE id = ?",
                (int(tamamlandi), gorev_id),
            )

    def gorev_sil(self, gorev_id: int):
        with self._baglanti_ac() as baglanti:
            baglanti.execute("DELETE FROM gorevler WHERE id = ?", (gorev_id,))