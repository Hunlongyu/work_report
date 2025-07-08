import json
import os.path
import qtmodern6.styles
import qt_themes

from .ui_home import Ui_Home
from PySide6.QtWidgets import QWidget, QApplication, QAbstractItemView, QTreeWidgetItem, QFileDialog, QMessageBox, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from git import Repo, InvalidGitRepositoryError
from src.config.config import Config


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
        self.init_project_wgt()

    def init_connect(self):
        self.ui.btn_settings.clicked.connect(self.ui.wgt_right_content.show)
        self.ui.btn_statistics.clicked.connect(self.ui.wgt_right_content.show)
        self.ui.cbb_theme.currentTextChanged.connect(self.change_theme)
        self.ui.cbb_date.currentTextChanged.connect(self.change_date)
        self.ui.btn_get.clicked.connect(self.get_commit_info)
        self.ui.btn_ai_repot.clicked.connect(self.ai_report)
        self.ui.btn_export.clicked.connect(self.export_report)
        self.ui.btn_project_add.clicked.connect(self.add_project)
        self.ui.twgt_project.itemChanged.connect(self.on_project_item_changed)
        self.ui.twgt_project.itemExpanded.connect(self.on_project_item_expanded)
        self.ui.twgt_project.itemCollapsed.connect(self.on_project_item_collapsed)
        self.ui.btn_account_add.clicked.connect(self.add_account)

    def init_theme(self):
        self.ui.cbb_theme.addItem('default_dark')
        self.ui.cbb_theme.addItem('default_light')
        themes_keys = qt_themes.get_themes().keys()
        for theme in themes_keys:
            self.ui.cbb_theme.addItem(theme)

        theme = Config().get('settings/theme', 'default_dark')
        self.ui.cbb_theme.setCurrentText(theme)
        self.change_theme(theme)

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

        Config().set('settings/theme', theme)
        app.setStyleSheet(app.styleSheet())

    @staticmethod
    def on_project_item_expanded(item: QTreeWidgetItem):
        if item.parent() is not None:
            return
        project_name = item.text(0)
        with Config().group("projects"):
            project_data = Config().get(project_name, "{}")
            try:
                project_data = json.loads(project_data)
            except json.JSONDecodeError:
                project_data = {}
            project_data["expanded"] = True
            Config().set(project_name, json.dumps(project_data))

    @staticmethod
    def on_project_item_collapsed(item: QTreeWidgetItem):
        if item.parent() is not None:
            return
        project_name = item.text(0)
        with Config().group("projects"):
            project_data = Config().get(project_name, "{}")
            try:
                project_data = json.loads(project_data)
            except json.JSONDecodeError:
                project_data = {}
            project_data["expanded"] = False
            Config().set(project_name, json.dumps(project_data))

    @staticmethod
    def on_project_item_changed(item: QTreeWidgetItem, column: int):
        parent = item.parent()
        if parent is None:
            return  # 项目节点本身不处理勾选变化

        # 找到顶层项目节点
        project_item = parent
        while project_item.parent() is not None:
            project_item = project_item.parent()

        project_name = project_item.text(0)
        checked = []

        for i in range(project_item.childCount()):
            child = project_item.child(i)
            if child.checkState(0) == Qt.CheckState.Checked:
                branch_data = child.data(0, Qt.ItemDataRole.UserRole)
                if branch_data:
                    if branch_data["type"] == "remote":
                        checked.append(f"remote/{branch_data['remote']}/{branch_data['name']}")
                    elif branch_data["type"] == "local":
                        checked.append(f"local/{branch_data['name']}")

        with Config().group("projects"):
            project_data = Config().get(project_name, "{}")
            try:
                project_data = json.loads(project_data)
            except json.JSONDecodeError:
                project_data = {}

            project_data["checked"] = checked
            Config().set(project_name, json.dumps(project_data))

    def init_project_wgt(self):
        """
        初始化项目视图的显示属性和行为。

        此方法配置了项目视图（twgt_project）的各项属性，包括隐藏表头、设置列数、
        选择模式和焦点策略，以确保视图按照预期的方式工作。此外，还设置了右键菜单
        和加载历史项目的功能。
        """
        # 隐藏表头
        self.ui.twgt_project.setHeaderHidden(True)
        # 设置列数为1
        self.ui.twgt_project.setColumnCount(1)
        # 禁止项目选择
        self.ui.twgt_project.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        # 移除焦点
        self.ui.twgt_project.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # 右键菜单
        self.ui.twgt_project.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.twgt_project.customContextMenuRequested.connect(self.show_project_context_menu)
        # 加载历史项目
        self.load_projects_to_tree()

    def show_project_context_menu(self, pos):
        item = self.ui.twgt_project.itemAt(pos)
        if not item:
            return

        # 只允许顶层项目节点可以删除（即没有父节点）
        if item.parent() is not None:
            return

        menu = QMenu(self)
        delete_action = QAction("删除项目", self)
        delete_action.triggered.connect(lambda: self.remove_project(item))
        menu.addAction(delete_action)
        menu.exec_(self.ui.twgt_project.viewport().mapToGlobal(pos))

    def remove_project(self, item):
        project_name = item.text(0)
        reply = QMessageBox.question(
            self, "确认删除",
            f"是否删除项目 [{project_name}]？此操作不可恢复！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        # 从配置中删除
        with Config().group("projects"):
            Config().remove(project_name)

        # 从界面中删除
        index = self.ui.twgt_project.indexOfTopLevelItem(item)
        if index >= 0:
            self.ui.twgt_project.takeTopLevelItem(index)

    def load_projects_to_tree(self):
        config = Config()
        with config.group('projects'):
            for project_name in config.child_keys():
                try:
                    project_json = config.get(project_name, "")
                    if not project_json:
                        continue

                    project_data = json.loads(project_json)
                    folder_path = project_data.get('path', '')
                    checked = set(project_data.get('checked', []))

                    if not os.path.exists(folder_path):
                        continue

                    project_item = self.add_project_to_tree(project_name)
                    self._add_branch_items(project_item, Repo(folder_path), checked)

                    project_item.setExpanded(project_data.get("expanded", True))
                except Exception as e:
                    print(f"加载项目失败 [{project_name}]：{e}")

    def add_project_to_tree(self, name):
        item = QTreeWidgetItem(self.ui.twgt_project)
        item.setText(0, name)
        item.setFlags(item.flags() |
                      Qt.ItemFlag.ItemIsUserCheckable |
                      Qt.ItemFlag.ItemIsAutoTristate)
        item.setCheckState(0, Qt.CheckState.Unchecked)
        return item

    @staticmethod
    def _add_branch_items(project_item, repo, checked_set=None):
        if checked_set is None:
            checked_set = set()

        remote_branch_names = set()

        # 添加远程分支
        for remote in repo.remotes:
            for ref in remote.refs:
                if ref.remote_head not in ["HEAD"]:
                    name = ref.remote_head
                    full_name = f"remote/{remote.name}/{name}"
                    remote_branch_names.add(name)
                    item = QTreeWidgetItem(project_item)
                    item.setText(0, name)
                    item.setData(0, Qt.ItemDataRole.UserRole, {
                        "type": "remote",
                        "remote": remote.name,
                        "name": name
                    })
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(0,
                                       Qt.CheckState.Checked if full_name in checked_set else Qt.CheckState.Unchecked)

        # 添加仅本地分支
        for branch in repo.branches:
            if branch.name not in remote_branch_names:
                full_name = f"local/{branch.name}"
                item = QTreeWidgetItem(project_item)
                item.setText(0, f"{branch.name}（仅本地）")
                item.setData(0, Qt.ItemDataRole.UserRole, {
                    "type": "local",
                    "name": branch.name
                })
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(0, Qt.CheckState.Checked if full_name in checked_set else Qt.CheckState.Unchecked)

    def add_project(self):
        last_dir = Config().get('settings/last_dir', os.path.expanduser('~'))
        folder_path = QFileDialog.getExistingDirectory(self, '择 Git 项目目录', last_dir,
                                                       QFileDialog.Option.ShowDirsOnly)
        if not folder_path:
            return
        try:
            Config().set('settings/last_dir', folder_path)
            repo = Repo(folder_path, search_parent_directories=True)
            project_name = os.path.basename(folder_path.rstrip(os.sep))
            project_item = self.add_project_to_tree(project_name)
            self._add_branch_items(project_item, repo)
            project_item.setExpanded(True)

            project_data = {
                'path': folder_path,
                'checked': []
            }
            Config().set(f"projects/{project_name}", json.dumps(project_data))

        except InvalidGitRepositoryError:
            QMessageBox.critical(self, "错误", "请选择有效的 Git 项目目录！")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def change_date(self):
        pass

    def get_commit_info(self):
        pass

    def ai_report(self):
        pass

    def export_report(self):
        pass


    def add_account(self):
        pass
