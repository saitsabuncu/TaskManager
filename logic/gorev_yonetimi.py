from __future__ import annotations
from enum import Enum

from data.veritabani import VeriTabani


GOREV_TAMAMLAMA_ODULU = 10

class IslemTuru(str, Enum):
    GOREV_EKLENDI = "gorev_eklendi"
    GOREV_GUNCELLENDI = "gorev_guncellendi"
    GOREV_SILINDI = "gorev_silindi"
    GOREV_GERI_YUKLENDI = "gorev_geri_yuklendi"
    GOREV_KALICI_SILINDI = "gorev_kalici_silindi"
    GOREV_TAMAMLANDI = "gorev_tamamlandi"
    GOREV_TAMAMLANMADI = "gorev_tamamlanmadi"
    KATEGORI_TASINDI = "kategori_tasindi"
    KATEGORI_YENIDEN_ADLANDIRILDI = "kategori_yeniden_adlandirildi"
    ODUL_EKLENDI = "odul_eklendi"
    ODUL_GUNCELLENDI = "odul_guncellendi"
    ODUL_SILINDI = "odul_silindi"
    ODUL_SATIN_ALINDI = "odul_satin_alindi"
    # IslemTuru enum'una ekle:
    GOREV_TEKRARI_ACILDI = "gorev_tekrari_acildi"
    GOREV_TEKRARI_KAPANDI = "gorev_tekrari_kapandi"


class GorevYonetimi:
    """Görev listesi ve mücevher bakiyesi gibi uygulama mantığını yönetir.

    Görevler SQLite üzerinden kalıcı olarak saklanır; bu sınıf veritabanı
    katmanıyla UI arasında bir köprü görevi görür. Her görev
    {"id", "ad", "tamamlandi", "kategori"} şeklinde bir sözlükle temsil edilir.

    Kategoriler artık veritabanında saklanır (sabit bir Python listesi
    değil), böylece kullanıcı kategori adlarını yeniden adlandırabilir ve
    bu değişiklik ilgili tüm görevlere yansır.

    Mücevher bakiyesi de veritabanında kalıcı olarak saklanır. Bir görev
    tamamlandı olarak işaretlendiğinde GOREV_TAMAMLAMA_ODULU kadar mücevher
    kazanılır; işaret kaldırılırsa aynı miktar geri alınır. Böylece bir
    görevi işaretleyip kaldırarak bakiye sınırsızca artırılamaz.
    """

    def __init__(self, veritabani: VeriTabani | None = None):
        self.veritabani = veritabani or VeriTabani()
        self.gorevler: list[dict] = []
        self.kategoriler: list[str] = []
        self.oduller: list[dict] = []
        self.mucevher_bakiyesi = 0
        self.kullanici_adi: str | None = None
        self.kategorileri_yukle()
        self.yukle()
        self.bakiyeyi_yukle()
        self.kullanici_adini_yukle()
        self.odulleri_yukle()

    
    def _islem_kaydet(
        self, islem_turu: IslemTuru, aciklama: str, gorev_id: int | None = None
    ) -> None:
        self.veritabani.islem_kaydet(islem_turu.value, aciklama, gorev_id)

    def islem_gecmisini_getir(self) -> list[dict]:
        return [
            {
                "id": id_,
                "tarih": tarih,
                "islem_turu": islem_turu,
                "aciklama": aciklama,
                "gorev_id": gorev_id,
            }
            for id_, tarih, islem_turu, aciklama, gorev_id
            in self.veritabani.islem_gecmisini_getir()
        ]    

    def bakiyeyi_yukle(self):
        self.mucevher_bakiyesi = self.veritabani.bakiye_getir()

    def kullanici_adini_yukle(self):
        self.kullanici_adi = self.veritabani.kullanici_adini_getir()

    def kullanici_adini_kaydet(self, ad: str):
        ad = ad.strip()
        if not ad:
            raise ValueError("Adınız boş bırakılamaz!")

        self.veritabani.kullanici_adini_kaydet(ad)
        self.kullanici_adi = ad

    def yukle(self):
        self.gorevler = [
            {
                "id": id_,
                "ad": ad,
                "tamamlandi": tamamlandi,
                "kategori": kategori,
                "tekrarlanan": tekrarlanan,
            }
            for id_, ad, tamamlandi, kategori, tekrarlanan
            in self.veritabani.tum_gorevleri_getir()
        ]

    def kategorileri_yukle(self):
        self.kategoriler = self.veritabani.kategorileri_getir()

    def gorev_ekle(
        self, ad: str, kategori: str | None = None, tekrarlanan: bool = False
    ) -> dict:
        ad = ad.strip()
        if not ad:
            raise ValueError("Görev adı boş bırakılamaz!")

        if kategori not in self.kategoriler:
            kategori = self.kategoriler[0]

        gorev_id = self.veritabani.gorev_ekle(ad, kategori, tekrarlanan)
        gorev = {
            "id": gorev_id,
            "ad": ad,
            "tamamlandi": False,
            "kategori": kategori,
            "tekrarlanan": tekrarlanan,
        }
        self.gorevler.append(gorev)

        tekrar_notu = " [Günlük tekrarlanan]" if tekrarlanan else ""
        self._islem_kaydet(
            IslemTuru.GOREV_EKLENDI,
            f'"{ad}" görevi eklendi. [Kategori: {kategori}]{tekrar_notu}',
            gorev_id,
        )
        return gorev

    def gorev_guncelle(self, index: int, yeni_ad: str) -> str:
        yeni_ad = yeni_ad.strip()
        if not yeni_ad:
            raise ValueError("Görev adı boş bırakılamaz!")

        if not (0 <= index < len(self.gorevler)):
            raise IndexError("Geçersiz görev seçildi.")

        gorev = self.gorevler[index]
        eski_ad = gorev["ad"]
        self.veritabani.gorev_guncelle(gorev["id"], yeni_ad)
        gorev["ad"] = yeni_ad
        self._islem_kaydet(
            IslemTuru.GOREV_GUNCELLENDI,
            f'"{eski_ad}" → "{yeni_ad}" olarak güncellendi.',
            gorev["id"],
        )
        return yeni_ad

    def gorev_sil(self, index: int) -> str:
        if not (0 <= index < len(self.gorevler)):
            raise IndexError("Geçersiz görev seçildi.")

        gorev = self.gorevler.pop(index)
        self.veritabani.gorev_sil(gorev["id"])
        self._islem_kaydet(
            IslemTuru.GOREV_SILINDI,
            f'"{gorev["ad"]}" görevi çöp kutusuna taşındı.',
            gorev["id"],
        )
        return gorev["ad"]

    def gorev_tamamlanma_degistir(self, index: int, tamamlandi: bool):
        if not (0 <= index < len(self.gorevler)):
            raise IndexError("Geçersiz görev seçildi.")

        gorev = self.gorevler[index]
        onceki_durum = gorev["tamamlandi"]

        self.veritabani.gorev_durumu_guncelle(gorev["id"], tamamlandi)
        gorev["tamamlandi"] = tamamlandi

        # Bakiye sadece durum gerçekten değiştiğinde güncellenir; aynı
        # duruma tekrar set edilmesi (örn. listeyi_yenile sırasında) mükerrer
        # mücevher kazandırmaz veya eksiltmez.
        if tamamlandi and not onceki_durum:
            self.mucevher_bakiyesi += GOREV_TAMAMLAMA_ODULU
            self.veritabani.bakiye_guncelle(self.mucevher_bakiyesi)
            self.veritabani.mucevher_kazanim_guncelle(GOREV_TAMAMLAMA_ODULU)
            self._islem_kaydet(
                IslemTuru.GOREV_TAMAMLANDI,
                f'"{gorev["ad"]}" görevi tamamlandı olarak işaretlendi '
                f'(+{GOREV_TAMAMLAMA_ODULU} 💎).',
                gorev["id"],
            )

        elif not tamamlandi and onceki_durum:
            self.mucevher_bakiyesi -= GOREV_TAMAMLAMA_ODULU
            self.veritabani.bakiye_guncelle(self.mucevher_bakiyesi)
            self.veritabani.mucevher_kazanim_guncelle(-GOREV_TAMAMLAMA_ODULU)
            self._islem_kaydet(
                IslemTuru.GOREV_TAMAMLANMADI,
                f'"{gorev["ad"]}" görevin tamamlanma işareti kaldırıldı '
                f'(-{GOREV_TAMAMLAMA_ODULU} 💎).',
                gorev["id"],
            )

    def gorev_kategorisini_degistir(self, index: int, yeni_kategori: str):
        if not (0 <= index < len(self.gorevler)):
            raise IndexError("Geçersiz görev seçildi.")

        if yeni_kategori not in self.kategoriler:
            raise ValueError("Geçersiz kategori seçildi.")

        gorev = self.gorevler[index]
        eski_kategori = gorev["kategori"]
        self.veritabani.gorev_kategorisini_degistir(gorev["id"], yeni_kategori)
        gorev["kategori"] = yeni_kategori
        self._islem_kaydet(
            IslemTuru.KATEGORI_TASINDI,
            f'"{gorev["ad"]}" görevi "{eski_kategori}" kategorisinden '
            f'"{yeni_kategori}" kategorisine taşındı.',
            gorev["id"],
        )
    # Yeni metod (gorev_kategorisini_degistir metodundan sonra):
    def gorev_tekrarlanmasini_degistir(self, index: int, tekrarlanan: bool):
        if not (0 <= index < len(self.gorevler)):
            raise IndexError("Geçersiz görev seçildi.")

        gorev = self.gorevler[index]
        self.veritabani.gorev_tekrarlanmasini_degistir(gorev["id"], tekrarlanan)
        gorev["tekrarlanan"] = tekrarlanan

        self._islem_kaydet(
            IslemTuru.GOREV_TEKRARI_ACILDI
            if tekrarlanan
            else IslemTuru.GOREV_TEKRARI_KAPANDI,
            f'"{gorev["ad"]}" görevi için günlük tekrar '
            f'{"açıldı" if tekrarlanan else "kapatıldı"}.',
            gorev["id"],
        )    

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

        self._islem_kaydet(
            IslemTuru.KATEGORI_YENIDEN_ADLANDIRILDI,
            f'"{eski_ad}" kategorisi "{yeni_ad}" olarak yeniden adlandırıldı.',
        )        

    def cop_kutusunu_getir(self) -> list[dict]:
        return [
            {"id": id_, "ad": ad, "silinme_tarihi": silinme_tarihi}
            for id_, ad, silinme_tarihi in self.veritabani.cop_kutusunu_getir()
        ]

    def gorev_geri_yukle(self, gorev_id: int, ad: str):
        self.veritabani.gorev_geri_yukle(gorev_id)
        self.yukle()
        self._islem_kaydet(
            IslemTuru.GOREV_GERI_YUKLENDI,
            f'"{ad}" görevi çöp kutusundan geri yüklendi.',
            gorev_id,
        )

    def gorev_kalici_sil(self, gorev_id: int, ad: str):
        self.veritabani.gorev_kalici_sil(gorev_id)
        self._islem_kaydet(
            IslemTuru.GOREV_KALICI_SILINDI,
            f'"{ad}" görevi kalıcı olarak silindi.',
            gorev_id,
        )

    def odulleri_yukle(self):
        self.oduller = [
            {"id": id_, "ad": ad, "mucevher_maliyeti": maliyet}
            for id_, ad, maliyet in self.veritabani.odulleri_getir()
        ]

    def odul_ekle(self, ad: str, mucevher_maliyeti: int) -> dict:
        ad = ad.strip()
        if not ad:
            raise ValueError("Ödül adı boş bırakılamaz!")

        if mucevher_maliyeti <= 0:
            raise ValueError("Mücevher maliyeti pozitif bir sayı olmalıdır!")

        odul_id = self.veritabani.odul_ekle(ad, mucevher_maliyeti)
        odul = {"id": odul_id, "ad": ad, "mucevher_maliyeti": mucevher_maliyeti}
        self.oduller.append(odul)
        self.oduller.sort(key=lambda o: o["mucevher_maliyeti"])
        self._islem_kaydet(
            IslemTuru.ODUL_EKLENDI, f'"{ad}" ödülü eklendi ({mucevher_maliyeti} 💎).'
        )
        return odul

    def odul_guncelle(self, index: int, ad: str, mucevher_maliyeti: int):
        ad = ad.strip()
        if not ad:
            raise ValueError("Ödül adı boş bırakılamaz!")

        if mucevher_maliyeti <= 0:
            raise ValueError("Mücevher maliyeti pozitif bir sayı olmalıdır!")

        if not (0 <= index < len(self.oduller)):
            raise IndexError("Geçersiz ödül seçildi.")

        odul = self.oduller[index]
        eski_ad = odul["ad"]
        self.veritabani.odul_guncelle(odul["id"], ad, mucevher_maliyeti)
        odul["ad"] = ad
        odul["mucevher_maliyeti"] = mucevher_maliyeti
        self.oduller.sort(key=lambda o: o["mucevher_maliyeti"])
        self._islem_kaydet(
            IslemTuru.ODUL_GUNCELLENDI,
            f'"{eski_ad}" ödülü güncellendi → "{ad}" ({mucevher_maliyeti} 💎).',
        )

    def odul_sil(self, index: int):
        if not (0 <= index < len(self.oduller)):
            raise IndexError("Geçersiz ödül seçildi.")

        odul = self.oduller.pop(index)
        self.veritabani.odul_sil(odul["id"])
        self._islem_kaydet(
            IslemTuru.ODUL_SILINDI, f'"{odul["ad"]}" ödülü silindi.'
        )

    def odul_satin_al(self, index: int) -> dict:
        """Seçilen ödülü mücevher bakiyesinden düşerek satın alır.

        Bakiye yetersizse ValueError fırlatır ve bakiyeye dokunmaz.
        """
        if not (0 <= index < len(self.oduller)):
            raise IndexError("Geçersiz ödül seçildi.")

        odul = self.oduller[index]
        if self.mucevher_bakiyesi < odul["mucevher_maliyeti"]:
            raise ValueError(
                f'Yetersiz mücevher bakiyesi! "{odul["ad"]}" için '
                f'{odul["mucevher_maliyeti"]} 💎 gerekiyor, '
                f'bakiyenizde {self.mucevher_bakiyesi} 💎 var.'
            )

        self.mucevher_bakiyesi -= odul["mucevher_maliyeti"]
        self.veritabani.bakiye_guncelle(self.mucevher_bakiyesi)
        self.veritabani.mucevher_harcama_ekle(odul["mucevher_maliyeti"])
        self._islem_kaydet(
            IslemTuru.ODUL_SATIN_ALINDI,
            f'"{odul["ad"]}" ödülü satın alındı (-{odul["mucevher_maliyeti"]} 💎).',
        )
        return odul
    
    # Sınıfın sonuna yeni metod:
    def istatistikleri_getir(self) -> dict:
        kategori_dagilimi: dict[str, int] = {}
        for gorev in self.gorevler:
            kategori_dagilimi[gorev["kategori"]] = (
                kategori_dagilimi.get(gorev["kategori"], 0) + 1
            )

        toplam = len(self.gorevler)
        tamamlanan = sum(1 for g in self.gorevler if g["tamamlandi"])

        kazanilan, harcanan = self.veritabani.mucevher_istatistik_getir()

        return {
            "kategori_dagilimi": kategori_dagilimi,
            "tamamlanan": tamamlanan,
            "toplam": toplam,
            "mucevher_kazanilan": kazanilan,
            "mucevher_harcanan": harcanan,
            "mucevher_bakiye": self.mucevher_bakiyesi,
        }