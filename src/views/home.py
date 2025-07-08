from .ui_home import Ui_Home
from PySide6.QtWidgets import QWidget, QApplication
import qtmodern6.styles
import qt_themes

class Home(QWidget):
    def __init__(self):
        super(Home, self).__init__()
        self.ui = Ui_Home()
        self.ui.setupUi(self)
        self.init_ui()
        self.init_connect()

    def init_ui(self):
        self.setWindowTitle('工作总结报告')
        self.ui.hbl_body.setStretch(2, 0)
        self.ui.wgt_right_content.hide()
        self.ui.btn_export.hide()
        self.init_theme()

    def init_connect(self):
        self.ui.btn_settings.clicked.connect(self.ui.wgt_right_content.show)
        self.ui.btn_statistics.clicked.connect(self.ui.wgt_right_content.show)
        self.ui.cbb_theme.currentTextChanged.connect(self.change_theme)
        self.ui.cbb_date.currentTextChanged.connect(self.change_date)
        self.ui.btn_get.clicked.connect(self.get_commit_info)
        self.ui.btn_ai_repot.clicked.connect(self.ai_report)
        self.ui.btn_export.clicked.connect(self.export_report)

    def init_theme(self):
        self.ui.cbb_theme.addItem('default_dark')
        self.ui.cbb_theme.addItem('default_light')
        themes_keys = qt_themes.get_themes().keys()
        for theme in themes_keys:
            self.ui.cbb_theme.addItem(theme)

    @staticmethod
    def change_theme(theme: str):
        app = QApplication.instance()
        if theme == 'default_dark':
            if isinstance(app, QApplication):
                qtmodern6.styles.dark(app)
        elif theme == 'default_light':
            if isinstance(app, QApplication):
                qtmodern6.styles.light(app)
        else:
            qt_themes.set_theme(theme)

        app.setStyleSheet(app.styleSheet())

    def change_date(self):
        pass

    def get_commit_info(self):
        pass

    def ai_report(self):
        pass

    def export_report(self):
        pass

