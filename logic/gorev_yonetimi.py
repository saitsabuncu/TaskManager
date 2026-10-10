class GorevYonetimi:
    """Görev listesi ve mücevher bakiyesi gibi uygulama mantığını yönetir.

    Qt'den bağımsız tutulur ki UI katmanı olmadan da test edilebilsin.
    """

    def __init__(self, baslangic_bakiyesi: int = 1320):
        self.gorevler: list[str] = []
        self.mucevher_bakiyesi = baslangic_bakiyesi

    def gorev_ekle(self, ad: str) -> str:
        ad = ad.strip()
        if not ad:
            raise ValueError("Görev adı boş bırakılamaz!")

        self.gorevler.append(ad)
        return ad

    def gorev_guncelle(self, index: int, yeni_ad: str) -> str:
        yeni_ad = yeni_ad.strip()
        if not yeni_ad:
            raise ValueError("Görev adı boş bırakılamaz!")

        if not (0 <= index < len(self.gorevler)):
            raise IndexError("Geçersiz görev seçildi.")

        self.gorevler[index] = yeni_ad
        return yeni_ad