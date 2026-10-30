import sys
from pathlib import Path


from PyQt6.QtWidgets import QApplication

from ui.ana_pencere import AnaPencere

STIL_DOSYASI = Path(__file__).resolve().parent / "ui" / "stil.qss"

def _stili_yukle(app: QApplication):
    try:
        app.setStyleSheet(STIL_DOSYASI.read_text(encoding="utf-8"))
    except FileNotFoundError:
        pass


def main():
    app = QApplication(sys.argv)
    
    _stili_yukle(app)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()