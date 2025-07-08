import sys
from PySide6 import QtWidgets
from views.home import Home
import qtmodern6.styles
import qtmodern6.windows

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    qtmodern6.styles.dark(app)
    home = Home()
    mw = qtmodern6.windows.ModernWindow(home)
    mw.show()
    sys.exit(app.exec())
