from __future__ import annotations

import sqlite3
from pathlib import Path

VARSAYILAN_DB_YOLU = Path(__file__).resolve().parent.parent / "gorevler.db"
COP_KUTUSU_SAKLAMA_GUNU = 30
VARSAYILAN_KATEGORI = "Genel"


class VeriTabani:
    """Görevlerin SQLite üzerinde kalıcı saklanmasından sorumlu katman.

    UI ve iş mantığı katmanlarından bağımsızdır; sadece satır okuma/yazma
    yapar. Görev sırası eklenme sırasına (id) göre korunur.

    Silme işlemi "yumuşak silme" olarak uygulanır: görev tablodan
    kaldırılmaz, sadece silinme_tarihi damgalanır. Bu sayede görev
    Çöp Kutusu'nda COP_KUTUSU_SAKLAMA_GUNU (30) gün boyunca saklanıp
    geri yüklenebilir; süre dolunca her açılışta otomatik temizlenir.
    """

    def __init__(self, db_yolu: Path | str = VARSAYILAN_DB_YOLU):
        self.db_yolu = str(db_yolu)
        self._tablolari_olustur()
        self._eski_silinenleri_temizle()

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
                    olusturulma_tarihi TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    silinme_tarihi TEXT,
                    kategori TEXT NOT NULL DEFAULT 'Genel'
                )
                """
            )

            # Bu sütunlar daha sonra eklendi; önceden oluşturulmuş eski
            # veritabanı dosyalarında bozulmadan çalışabilmek için
            # eksikse burada ekleniyor.
            sutunlar = {
                satir[1]
                for satir in baglanti.execute("PRAGMA table_info(gorevler)").fetchall()
            }
            if "silinme_tarihi" not in sutunlar:
                baglanti.execute("ALTER TABLE gorevler ADD COLUMN silinme_tarihi TEXT")
            if "kategori" not in sutunlar:
                baglanti.execute(
                    f"ALTER TABLE gorevler ADD COLUMN kategori TEXT "
                    f"NOT NULL DEFAULT '{VARSAYILAN_KATEGORI}'"
                )

    def _eski_silinenleri_temizle(self):
        with self._baglanti_ac() as baglanti:
            baglanti.execute(
                """
                DELETE FROM gorevler
                WHERE silinme_tarihi IS NOT NULL
                  AND silinme_tarihi <= datetime('now', ?)
                """,
                (f"-{COP_KUTUSU_SAKLAMA_GUNU} days",),
            )

    def tum_gorevleri_getir(self) -> list[tuple[int, str, bool, str]]:
        with self._baglanti_ac() as baglanti:
            satirlar = baglanti.execute(
                "SELECT id, ad, tamamlandi, kategori FROM gorevler "
                "WHERE silinme_tarihi IS NULL ORDER BY id ASC"
            ).fetchall()
        return [
            (id_, ad, bool(tamamlandi), kategori)
            for id_, ad, tamamlandi, kategori in satirlar
        ]

    def gorev_ekle(self, ad: str, kategori: str = VARSAYILAN_KATEGORI) -> int:
        with self._baglanti_ac() as baglanti:
            imlec = baglanti.execute(
                "INSERT INTO gorevler (ad, tamamlandi, kategori) VALUES (?, 0, ?)",
                (ad, kategori),
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
        """Görevi kalıcı silmez; çöp kutusuna taşır (silinme_tarihi damgalar)."""
        with self._baglanti_ac() as baglanti:
            baglanti.execute(
                "UPDATE gorevler SET silinme_tarihi = CURRENT_TIMESTAMP WHERE id = ?",
                (gorev_id,),
            )

    def cop_kutusunu_getir(self) -> list[tuple[int, str, str]]:
        with self._baglanti_ac() as baglanti:
            return baglanti.execute(
                "SELECT id, ad, silinme_tarihi FROM gorevler "
                "WHERE silinme_tarihi IS NOT NULL ORDER BY silinme_tarihi DESC"
            ).fetchall()

    def gorev_geri_yukle(self, gorev_id: int):
        with self._baglanti_ac() as baglanti:
            baglanti.execute(
                "UPDATE gorevler SET silinme_tarihi = NULL WHERE id = ?",
                (gorev_id,),
            )

    def gorev_kalici_sil(self, gorev_id: int):
        with self._baglanti_ac() as baglanti:
            baglanti.execute("DELETE FROM gorevler WHERE id = ?", (gorev_id,))