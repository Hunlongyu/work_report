from src.views.settings.ui_settings import Ui_Settings
from PySide6.QtWidgets import QDialog

class Settings(QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowTitle("设置")