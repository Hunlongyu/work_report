from src.views.settings.ui_settings import Ui_Settings
from PySide6.QtWidgets import QDialog, QMessageBox, QLineEdit
from PySide6.QtCore import QThreadPool
from src.config.config import Config
from src.utils.ai_utils import AIKeyCheckTask


class Settings(QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowTitle('设置')
        self.thread_pool = QThreadPool()
        self.init_ui()
        self.init_connect()

    def init_ui(self):
        self.ui.le_key.setText(Config().get('settings/key', ''))
        self.ui.le_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.le_address.setText(Config().get('settings/address', ''))
        self.ui.le_model.setText(Config().get('settings/model', ''))
        self.ui.pte_prompt.appendPlainText(Config().get('settings/prompt', ''))

    def init_connect(self):
        self.ui.btn_check.clicked.connect(self.check_key)
        self.ui.btn_save.clicked.connect(self.save_settings)
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_show.clicked.connect(self.show_key)

    def show_key(self):
        if self.ui.le_key.echoMode() == QLineEdit.EchoMode.Password:
            self.ui.le_key.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.btn_show.setText('隐藏')
        else:
            self.ui.le_key.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.btn_show.setText('显示')

    def check_key(self):
        print("Checking key...")
        if not all([
            self.ui.le_key.text().strip(),
            self.ui.le_address.text().strip(),
            self.ui.le_model.text().strip()
        ]):
            QMessageBox.warning(
                self,
                '错误',
                '请填写完整的 Key、API地址和模型名称！'
            )
            return False
        self.ui.btn_check.setEnabled(False)
        self.ui.btn_check.setText("验证中...")

        task = AIKeyCheckTask(
            self.ui.le_key.text(),
            self.ui.le_address.text(),
            self.ui.le_model.text()
        )

        def handle_success(valid):
            self.ui.btn_check.setEnabled(True)
            self.ui.btn_check.setText("验证 Key")
            if valid:
                QMessageBox.information(self, '成功', '✅ Key 验证成功！')
            else:
                QMessageBox.warning(self, '无效', '❌ Key 无效或无返回内容。')

        def handle_error(msg):
            self.ui.btn_check.setEnabled(True)
            self.ui.btn_check.setText("验证 Key")
            QMessageBox.critical(self, '错误', f"验证失败：\n{msg}")

        task.signals.success.connect(handle_success)
        task.signals.error.connect(handle_error)
        self.thread_pool.start(task)

    def save_settings(self):
        Config().begin_group('settings')
        Config().set('key', self.ui.le_key.text())
        Config().set('address', self.ui.le_address.text())
        Config().set('model', self.ui.le_model.text())
        Config().set('prompt', self.ui.pte_prompt.toPlainText())
        Config().end_group()
        self.close()
