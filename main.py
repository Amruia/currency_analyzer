import sys
from PyQt6.QtWidgets import QApplication
from gui.hlavni_okno import HlavniOkno

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = HlavniOkno()
    okno.show()
    sys.exit(app.exec())