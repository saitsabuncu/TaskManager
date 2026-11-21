from __future__ import annotations

from pathlib import Path

import pytest

from data.veritabani import VeriTabani
from logic.gorev_yonetimi import GorevYonetimi


@pytest.fixture
def veritabani(tmp_path: Path) -> VeriTabani:
    # ":memory:" kullanılmaz: VeriTabani her metodda yeni bir bağlantı
    # açar (_baglanti_ac). ":memory:" ile her yeni bağlantı sıfırdan boş
    # bir veritabanı demektir, bu yüzden veriler çağrılar arasında
    # kaybolur. Bunun yerine geçici bir dosya kullanılır.
    return VeriTabani(tmp_path / "test_gorevler.db")


@pytest.fixture
def gorev_yonetimi(veritabani: VeriTabani) -> GorevYonetimi:
    return GorevYonetimi(veritabani)