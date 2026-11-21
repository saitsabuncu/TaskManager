from __future__ import annotations

from datetime import date, timedelta

import pytest

from logic.gorev_yonetimi import GOREV_TAMAMLAMA_ODULU, GorevYonetimi


def test_gorev_ekle_gecerli_ad_ile_gorev_olusturur(gorev_yonetimi: GorevYonetimi) -> None:
    gorev = gorev_yonetimi.gorev_ekle("Rapor yaz")

    assert gorev["ad"] == "Rapor yaz"
    assert gorev["tamamlandi"] is False
    assert gorev["oncelik"] == 2
    assert gorev["son_tarih"] is None
    assert gorev in gorev_yonetimi.gorevler


def test_gorev_ekle_bos_ad_value_error_firlatir(gorev_yonetimi: GorevYonetimi) -> None:
    with pytest.raises(ValueError):
        gorev_yonetimi.gorev_ekle("   ")


def test_gorev_ekle_gecersiz_kategori_ilk_kategoriye_duser(
    gorev_yonetimi: GorevYonetimi,
) -> None:
    gorev = gorev_yonetimi.gorev_ekle("Görev", kategori="Olmayan Kategori")

    assert gorev["kategori"] == gorev_yonetimi.kategoriler[0]


def test_gorev_tamamlanma_degistir_bakiyeyi_artirir(gorev_yonetimi: GorevYonetimi) -> None:
    gorev_yonetimi.gorev_ekle("Görev")
    baslangic_bakiye = gorev_yonetimi.mucevher_bakiyesi

    gorev_yonetimi.gorev_tamamlanma_degistir(0, True)

    assert gorev_yonetimi.mucevher_bakiyesi == baslangic_bakiye + GOREV_TAMAMLAMA_ODULU
    assert gorev_yonetimi.gorevler[0]["tamamlandi"] is True


def test_gorev_tamamlanma_geri_alinca_bakiye_azalir(gorev_yonetimi: GorevYonetimi) -> None:
    gorev_yonetimi.gorev_ekle("Görev")
    gorev_yonetimi.gorev_tamamlanma_degistir(0, True)
    bakiye_tamamlandiktan_sonra = gorev_yonetimi.mucevher_bakiyesi

    gorev_yonetimi.gorev_tamamlanma_degistir(0, False)

    assert (
        gorev_yonetimi.mucevher_bakiyesi
        == bakiye_tamamlandiktan_sonra - GOREV_TAMAMLAMA_ODULU
    )


def test_gorev_tamamlanma_degistir_ayni_durum_bakiyeyi_degistirmez(
    gorev_yonetimi: GorevYonetimi,
) -> None:
    gorev_yonetimi.gorev_ekle("Görev")
    gorev_yonetimi.gorev_tamamlanma_degistir(0, True)
    bakiye = gorev_yonetimi.mucevher_bakiyesi

    gorev_yonetimi.gorev_tamamlanma_degistir(0, True)

    assert gorev_yonetimi.mucevher_bakiyesi == bakiye


def test_gorev_sil_gorevi_listeden_cikarir(gorev_yonetimi: GorevYonetimi) -> None:
    gorev_yonetimi.gorev_ekle("Görev")

    gorev_yonetimi.gorev_sil(0)

    assert gorev_yonetimi.gorevler == []


def test_gorev_kategorisini_degistir_gecersiz_kategori_value_error(
    gorev_yonetimi: GorevYonetimi,
) -> None:
    gorev_yonetimi.gorev_ekle("Görev")

    with pytest.raises(ValueError):
        gorev_yonetimi.gorev_kategorisini_degistir(0, "Olmayan Kategori")


def test_gorev_onceligini_degistir_gecerli_deger(gorev_yonetimi: GorevYonetimi) -> None:
    gorev_yonetimi.gorev_ekle("Görev")

    gorev_yonetimi.gorev_onceligini_degistir(0, 3)

    assert gorev_yonetimi.gorevler[0]["oncelik"] == 3


def test_gorev_onceligini_degistir_gecersiz_deger_value_error(
    gorev_yonetimi: GorevYonetimi,
) -> None:
    gorev_yonetimi.gorev_ekle("Görev")

    with pytest.raises(ValueError):
        gorev_yonetimi.gorev_onceligini_degistir(0, 99)


def test_gorev_son_tarihini_degistir(gorev_yonetimi: GorevYonetimi) -> None:
    gorev_yonetimi.gorev_ekle("Görev")
    yeni_tarih = date.today().isoformat()

    gorev_yonetimi.gorev_son_tarihini_degistir(0, yeni_tarih)

    assert gorev_yonetimi.gorevler[0]["son_tarih"] == yeni_tarih


def test_gorev_gecikmis_mi_son_tarih_yoksa_false(gorev_yonetimi: GorevYonetimi) -> None:
    gorev_yonetimi.gorev_ekle("Görev")

    assert gorev_yonetimi.gorev_gecikmis_mi(gorev_yonetimi.gorevler[0]) is False


def test_gorev_gecikmis_mi_tamamlanmamis_ve_gecmis_tarihliyse_true(
    gorev_yonetimi: GorevYonetimi,
) -> None:
    gorev_yonetimi.gorev_ekle("Görev")
    gecmis_tarih = (date.today() - timedelta(days=1)).isoformat()
    gorev_yonetimi.gorev_son_tarihini_degistir(0, gecmis_tarih)

    assert gorev_yonetimi.gorev_gecikmis_mi(gorev_yonetimi.gorevler[0]) is True


def test_gorev_gecikmis_mi_tamamlanmissa_false(gorev_yonetimi: GorevYonetimi) -> None:
    gorev_yonetimi.gorev_ekle("Görev")
    gecmis_tarih = (date.today() - timedelta(days=1)).isoformat()
    gorev_yonetimi.gorev_son_tarihini_degistir(0, gecmis_tarih)
    gorev_yonetimi.gorev_tamamlanma_degistir(0, True)

    assert gorev_yonetimi.gorev_gecikmis_mi(gorev_yonetimi.gorevler[0]) is False