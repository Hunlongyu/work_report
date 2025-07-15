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
你是一个资深的项目经理和技术文档撰写专家。请根据我提供的 Git 提交信息，为每个开发者生成简洁、结构清晰的工作总结（如日报、周报或月报）。每条提交记录包含提交者、提交时间、项目名称、分支、提交信息（commit message）。你需要：

1. 按照开发者分类。
2. 将同类的提交合并，归纳为功能开发、BUG修复、优化改进、文档更新等工作项。
3. 使用自然语言写作，适当润色技术细节，使其更适合作为工作汇报。
4. 如果可能，推测工作目标和成果。
5. 输出格式可参考以下结构：

---

【开发者】：张三  
【汇报周期】：2024年7月第2周  
【参与项目】：项目A、项目B

【本周工作总结】  
- ✅ 在项目A中完成了登录功能的开发，包括前端表单验证与后端接口联调。  
- 🐞 修复了项目B中的用户无法上传头像的问题，涉及文件上传模块的权限处理。  
- 🔧 优化了项目A中的首页加载速度，通过延迟加载图表组件提升了首次渲染性能。  
- 📝 更新了项目A的接口文档，补充了接口参数说明与错误码定义。

【备注】  
- 下周计划继续进行项目B的权限模块开发。

---

以下是本周期的 Git 提交信息，请帮我整理工作总结：
''')

    def save_settings(self):
        Config().begin_group('settings')
        Config().set('key', self.ui.le_key.text())
        Config().set('address', self.ui.le_address.text())
        Config().set('model', self.ui.le_model.text())
        Config().set('prompt', self.ui.pte_prompt.toPlainText())
        Config().end_group()
        self.close()
