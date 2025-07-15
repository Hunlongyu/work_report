import sys
import os
import qtmodern6.windows
import qtmodern6.styles
from PySide6.QtGui import QIcon
from PySide6 import QtWidgets
from src.views.home.home import Home

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    qtmodern6.styles.dark(app)
    home = Home()
    mw = qtmodern6.windows.ModernWindow(home)
    icon_path = resource_path("src/resources/app.ico")
    mw.setWindowIcon(QIcon(str(icon_path)))
    mw.move(
        QtWidgets.QApplication.primaryScreen().geometry().center() - mw.rect().center()
    )
    mw.show()
    sys.exit(app.exec())
