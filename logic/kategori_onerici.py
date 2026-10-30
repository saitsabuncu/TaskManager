from __future__ import annotations

import re

import ollama

OLLAMA_MODELI = "llama3.2:3b"

# Kategori ADI yerine POZİSYONUNA (0=Genel, 1=İş, 2=Kişisel, 3=Alışveriş,
# 4=Sağlık) göre eşleştirilir. Uygulama şu an kategori eklemeyi değil
# sadece yeniden adlandırmayı desteklediği için sıra hep sabittir — bu
# yüzden kullanıcı kategorileri istediği dile/isme çevirse bile
# (örn. "Health", "iş" -> "work") eşleştirme bozulmaz.
ANAHTAR_KELIME_INDEKSLERI: dict[int, list[str]] = {
    1: ["rapor", "toplantı", "proje", "sunum", "müşteri", "dosya", "icra", "mail"],
    2: ["ara", "ziyaret", "görüş", "temizlik"],
    3: ["market", "alışveriş", "satın", "sipariş", "manav"],
    4: ["doktor", "ilaç", "hastane", "diş", "aşı", "eczane", "muayene"],
}

# Ollama few-shot örnekleri (bkz. _ollamadan_kategori_oner), aynı
# pozisyon mantığıyla.
ORNEK_GOREV_INDEKSLERI: dict[str, int] = {
    "rapor yaz": 1,
    "arkadaşımı ara": 2,
    "markete git": 3,
    "doktora git": 4,
}


def kategori_tahmin_et(gorev_adi: str, kategoriler: list[str]) -> str | None:
    """Görev adına bakarak mevcut kategorilerden birini önerir.

    Önce güvenilir anahtar kelime eşleşmesi denenir; sonuç bulunamazsa
    Ollama'dan öneri istenir. İkisi de sonuç veremezse None döner —
    çağıran taraf bu durumda normal (elle seçim) akışına devam etmelidir.
    """
    tahmin = _anahtar_kelimeyle_tahmin_et(gorev_adi, kategoriler)
    if tahmin is not None:
        return tahmin

    return _ollamadan_kategori_oner(gorev_adi, kategoriler)


def _anahtar_kelimeyle_tahmin_et(gorev_adi: str, kategoriler: list[str]) -> str | None:
    kelimeler_metinde = re.findall(r"\w+", gorev_adi.lower())

    for indeks, anahtarlar in ANAHTAR_KELIME_INDEKSLERI.items():
        if indeks >= len(kategoriler):
            continue
        for anahtar in anahtarlar:
            for kelime in kelimeler_metinde:
                if kelime.startswith(anahtar):
                    return kategoriler[indeks]

    return None


def _ollamadan_kategori_oner(gorev_adi: str, kategoriler: list[str]) -> str | None:
    numarali_liste = "\n".join(
        f"{i}) {kategori}" for i, kategori in enumerate(kategoriler, start=1)
    )

    def soru_metni(ad: str) -> str:
        return f"Kategoriler:\n{numarali_liste}\n\nGörev: \"{ad}\"\nNumara:"

    messages = [
        {
            "role": "system",
            "content": (
                "Bir görevin hangi kategoriye ait olduğunu belirliyorsun. "
                "SADECE kategorinin numarasını yaz (örnek: 3). Başka "
                "hiçbir kelime, açıklama veya noktalama ekleme."
            ),
        },
    ]

    for ornek_gorev, indeks in ORNEK_GOREV_INDEKSLERI.items():
        if indeks >= len(kategoriler):
            continue
        messages.append({"role": "user", "content": soru_metni(ornek_gorev)})
        messages.append({"role": "assistant", "content": str(indeks + 1)})

    messages.append({"role": "user", "content": soru_metni(gorev_adi)})

    try:
        yanit = ollama.chat(
            model=OLLAMA_MODELI,
            messages=messages,
            options={"temperature": 0},
        )
    except Exception:
        return None

    tahmin = yanit["message"]["content"].strip()

    for karakter in tahmin:
        if karakter.isdigit():
            index = int(karakter) - 1
            if 0 <= index < len(kategoriler):
                return kategoriler[index]
            break

    return None