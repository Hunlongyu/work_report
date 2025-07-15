import sys
import os
from src.views.settings.ui_settings import Ui_Settings
from PySide6.QtWidgets import QDialog, QMessageBox, QLineEdit
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIcon
from src.config.config import Config
from src.utils.ai_utils import AIKeyCheckTask


class Settings(QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowTitle('设置')
        self.thread_pool = QThreadPool()
        self.check_task = None
        self.init_ui()
        self.init_connect()

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)

    def init_ui(self):
        icon_path = self.resource_path("src/resources/app.ico")
        self.setWindowIcon(QIcon(str(icon_path)))
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
        self.ui.btn_default.clicked.connect(self.show_default_prompt)

    def show_key(self):
        if self.ui.le_key.echoMode() == QLineEdit.EchoMode.Password:
            self.ui.le_key.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.btn_show.setText('隐藏')
        else:
            self.ui.le_key.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.btn_show.setText('显示')

    def handle_success(self, valid):
        self.ui.btn_check.setEnabled(True)
        self.ui.btn_check.setText("验证 Key")
        if valid:
            QMessageBox.information(self, '成功', '✅ Key 验证成功！')
        else:
            QMessageBox.warning(self, '无效', '❌ Key 无效或无返回内容。')

    def handle_error(self, msg):
        self.ui.btn_check.setEnabled(True)
        self.ui.btn_check.setText("验证 Key")
        QMessageBox.critical(self, '错误', f"验证失败：\n{msg}")

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

        self.check_task = AIKeyCheckTask(
            self.ui.le_key.text(),
            self.ui.le_address.text(),
            self.ui.le_model.text()
        )

        self.check_task.signals.success.connect(self.handle_success)
        self.check_task.signals.error.connect(self.handle_error)
        self.thread_pool.start(self.check_task)

    def show_default_prompt(self):
        self.ui.pte_prompt.clear()
        self.ui.pte_prompt.appendPlainText(
'''
你是一位经验丰富的项目经理兼技术文档撰写专家。请根据我提供的 Git 提交记录，为每位开发者撰写简洁、条理清晰的工作总结。总结将用于日常或阶段性工作汇报，请严格按照以下要求生成内容：

提交记录包含以下字段：

提交者

提交时间

项目名称

分支名称

提交信息（commit message）

请按照以下要求进行整理和撰写：

按照开发者对提交记录进行分类，为每位开发者分别撰写工作总结。

合并和归纳提交信息，将内容整理为以下几类工作项：
功能开发（标注为“功能开发”）
Bug 修复（标注为“Bug 修复”）
性能优化或功能改进（标注为“优化改进”）
文档更新（标注为“文档更新”）

用自然语言撰写总结内容，适当润色技术细节，使其更正式、更适合向团队或管理层汇报。

根据提交时间自动判断汇报周期（日报、周报、月报、季度报或年报），并在总结中体现。

输出为纯文本格式，不使用 Markdown 或特殊符号，保持清晰、简洁、可复制粘贴。

请参照以下格式撰写总结：

开发者：张三
汇报周期：周报
参与项目：项目 A、项目 B

本周工作总结：

功能开发：完成了项目 A 的登录功能开发，包含前端表单校验和后端接口联调。

Bug 修复：解决了项目 B 中头像上传失败的问题，修复了文件权限配置。

优化改进：优化了项目 A 的首页加载速度，引入延迟加载机制改善渲染性能。

文档更新：补充了项目 A 接口文档的参数说明与错误码定义。

现在请根据下面的 Git 提交记录，整理并输出符合上述格式的工作总结。

（以下为提交信息）
''')

    def save_settings(self):
        Config().begin_group('settings')
        Config().set('key', self.ui.le_key.text())
        Config().set('address', self.ui.le_address.text())
        Config().set('model', self.ui.le_model.text())
        Config().set('prompt', self.ui.pte_prompt.toPlainText())
        Config().end_group()
        self.close()
