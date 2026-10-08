import sys

from PyQt6.QtWidgets import QApplication

from ui.ana_pencere import AnaPencere


def main():
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()