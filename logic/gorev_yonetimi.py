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