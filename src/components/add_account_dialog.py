from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QDialogButtonBox, QMessageBox
import re

class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加账号")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("请输入用户名")
        layout.addWidget(QLabel("用户名:"))
        layout.addWidget(self.name_edit)

        self.email_edit = QLineEdit(self)
        self.email_edit.setPlaceholderText("请输入邮箱")
        layout.addWidget(QLabel("邮箱:"))
        layout.addWidget(self.email_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def validate_and_accept(self):
        name = self.name_edit.text().strip()
        email = self.email_edit.text().strip()

        if not name or not email:
            QMessageBox.warning(self, "输入错误", "账号和邮箱不能为空！")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.warning(self, "邮箱格式错误", "请输入正确的邮箱地址！")
            return

        self.accept()

    def get_account_info(self):
        return self.name_edit.text().strip(), self.email_edit.text().strip()
