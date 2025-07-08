import sys
import qtmodern6.windows
import qtmodern6.styles

from PySide6 import QtWidgets
from src.views.home import Home

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    qtmodern6.styles.dark(app)
    home = Home()
    mw = qtmodern6.windows.ModernWindow(home)
    mw.move(
        QtWidgets.QApplication.primaryScreen().geometry().center() - mw.rect().center()
    )
    mw.show()
    sys.exit(app.exec())
