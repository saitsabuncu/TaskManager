from __future__ import annotations

from data.veritabani import VeriTabani


class GorevYonetimi:
    """Görev listesi ve mücevher bakiyesi gibi uygulama mantığını yönetir.

    Görevler SQLite üzerinden kalıcı olarak saklanır; bu sınıf veritabanı
    katmanıyla UI arasında bir köprü görevi görür. Her görev
    {"id", "ad", "tamamlandi"} şeklinde bir sözlükle temsil edilir.
    """

    def __init__(self, veritabani: VeriTabani | None = None, baslangic_bakiyesi: int = 1320):
        self.veritabani = veritabani or VeriTabani()
        self.gorevler: list[dict] = []
        self.mucevher_bakiyesi = baslangic_bakiyesi
        self.yukle()

    def yukle(self):
        self.gorevler = [
            {"id": id_, "ad": ad, "tamamlandi": tamamlandi}
            for id_, ad, tamamlandi in self.veritabani.tum_gorevleri_getir()
        ]

    def gorev_ekle(self, ad: str) -> dict:
        ad = ad.strip()
        if not ad:
            raise ValueError("Görev adı boş bırakılamaz!")

        gorev_id = self.veritabani.gorev_ekle(ad)
        gorev = {"id": gorev_id, "ad": ad, "tamamlandi": False}
        self.gorevler.append(gorev)
        return gorev

    def gorev_guncelle(self, index: int, yeni_ad: str) -> str:
        yeni_ad = yeni_ad.strip()
        if not yeni_ad:
            raise ValueError("Görev adı boş bırakılamaz!")

        if not (0 <= index < len(self.gorevler)):
            raise IndexError("Geçersiz görev seçildi.")

        gorev = self.gorevler[index]
        self.veritabani.gorev_guncelle(gorev["id"], yeni_ad)
        gorev["ad"] = yeni_ad
        return yeni_ad

    def gorev_sil(self, index: int) -> str:
        if not (0 <= index < len(self.gorevler)):
            raise IndexError("Geçersiz görev seçildi.")

        gorev = self.gorevler.pop(index)
        self.veritabani.gorev_sil(gorev["id"])
        return gorev["ad"]

    def gorev_tamamlanma_degistir(self, index: int, tamamlandi: bool):
        if not (0 <= index < len(self.gorevler)):
            raise IndexError("Geçersiz görev seçildi.")

        gorev = self.gorevler[index]
        self.veritabani.gorev_durumu_guncelle(gorev["id"], tamamlandi)
        gorev["tamamlandi"] = tamamlandi

    def cop_kutusunu_getir(self) -> list[dict]:
        return [
            {"id": id_, "ad": ad, "silinme_tarihi": silinme_tarihi}
            for id_, ad, silinme_tarihi in self.veritabani.cop_kutusunu_getir()
        ]

    def gorev_geri_yukle(self, gorev_id: int):
        self.veritabani.gorev_geri_yukle(gorev_id)
        self.yukle()

    def gorev_kalici_sil(self, gorev_id: int):
        self.veritabani.gorev_kalici_sil(gorev_id)        