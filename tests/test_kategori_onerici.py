from __future__ import annotations

from unittest.mock import patch

from logic.kategori_onerici import _anahtar_kelimeyle_tahmin_et, kategori_tahmin_et

KATEGORILER = ["Genel", "İş", "Kişisel", "Alışveriş", "Sağlık"]


def test_anahtar_kelimeyle_tahmin_et_is_kategorisini_bulur() -> None:
    assert _anahtar_kelimeyle_tahmin_et("rapor yaz", KATEGORILER) == "İş"


def test_anahtar_kelimeyle_tahmin_et_saglik_kategorisini_bulur() -> None:
    assert _anahtar_kelimeyle_tahmin_et("doktora git", KATEGORILER) == "Sağlık"


def test_anahtar_kelimeyle_tahmin_et_eslesme_yoksa_none_doner() -> None:
    assert _anahtar_kelimeyle_tahmin_et("xyzabc123", KATEGORILER) is None


@patch("logic.kategori_onerici.ollama.chat")
def test_kategori_tahmin_et_eslesme_yoksa_ollamaya_sorar(mock_chat) -> None:
    mock_chat.return_value = {"message": {"content": "4"}}

    sonuc = kategori_tahmin_et("spor salonuna git", KATEGORILER)

    assert sonuc == "Alışveriş"
    mock_chat.assert_called_once()


@patch("logic.kategori_onerici.ollama.chat")
def test_kategori_tahmin_et_ollama_hata_firlatirsa_none_doner(mock_chat) -> None:
    mock_chat.side_effect = Exception("bağlantı hatası")

    sonuc = kategori_tahmin_et("bilinmeyen görev", KATEGORILER)

    assert sonuc is None


def test_anahtar_kelime_eslesirse_ollamaya_hic_gidilmez() -> None:
    with patch("logic.kategori_onerici.ollama.chat") as mock_chat:
        sonuc = kategori_tahmin_et("markete git", KATEGORILER)

    assert sonuc == "Alışveriş"
    mock_chat.assert_not_called()