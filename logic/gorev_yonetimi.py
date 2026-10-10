from __future__ import annotations

from data.veritabani import VeriTabani


class GorevYonetimi:
    """Görev listesi ve mücevher bakiyesi gibi uygulama mantığını yönetir.

    Görevler SQLite üzerinden kalıcı olarak saklanır; bu sınıf veritabanı
    katmanıyla UI arasında bir köprü görevi görür. Her görev
    {"id", "ad", "tamamlandi", "kategori"} şeklinde bir sözlükle temsil edilir.

    Kategoriler artık veritabanında saklanır (sabit bir Python listesi
    değil), böylece kullanıcı kategori adlarını yeniden adlandırabilir ve
    bu değişiklik ilgili tüm görevlere yansır.
    """

    def __init__(self, veritabani: VeriTabani | None = None, baslangic_bakiyesi: int = 1320):
        self.veritabani = veritabani or VeriTabani()
        self.gorevler: list[dict] = []
        self.kategoriler: list[str] = []
        self.mucevher_bakiyesi = baslangic_bakiyesi
        self.kategorileri_yukle()
        self.yukle()

    def yukle(self):
        self.gorevler = [
            {"id": id_, "ad": ad, "tamamlandi": tamamlandi, "kategori": kategori}
            for id_, ad, tamamlandi, kategori in self.veritabani.tum_gorevleri_getir()
        ]

    def kategorileri_yukle(self):
        self.kategoriler = self.veritabani.kategorileri_getir()

    def gorev_ekle(self, ad: str, kategori: str | None = None) -> dict:
        ad = ad.strip()
        if not ad:
            raise ValueError("Görev adı boş bırakılamaz!")

        if kategori not in self.kategoriler:
            kategori = self.kategoriler[0]

        gorev_id = self.veritabani.gorev_ekle(ad, kategori)
        gorev = {"id": gorev_id, "ad": ad, "tamamlandi": False, "kategori": kategori}
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
        """Görevi aktif listeden kaldırır; veritabanında çöp kutusuna taşınır."""
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

    def gorev_kategorisini_degistir(self, index: int, yeni_kategori: str):
        if not (0 <= index < len(self.gorevler)):
            raise IndexError("Geçersiz görev seçildi.")

        if yeni_kategori not in self.kategoriler:
            raise ValueError("Geçersiz kategori seçildi.")

        gorev = self.gorevler[index]
        self.veritabani.gorev_kategorisini_degistir(gorev["id"], yeni_kategori)
        gorev["kategori"] = yeni_kategori

    def kategori_adini_guncelle(self, eski_ad: str, yeni_ad: str):
        yeni_ad = yeni_ad.strip()
        if not yeni_ad:
            raise ValueError("Kategori adı boş bırakılamaz!")

        if eski_ad not in self.kategoriler:
            raise ValueError("Geçersiz kategori.")

        if yeni_ad != eski_ad and yeni_ad in self.kategoriler:
            raise ValueError(f'"{yeni_ad}" adında bir kategori zaten var.')

        self.veritabani.kategori_adi_guncelle(eski_ad, yeni_ad)

        index = self.kategoriler.index(eski_ad)
        self.kategoriler[index] = yeni_ad

        for gorev in self.gorevler:
            if gorev["kategori"] == eski_ad:
                gorev["kategori"] = yeni_ad

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