import json
import os.path

import qtmodern6.styles
import qt_themes
import pendulum

from src.components.add_account_dialog import AddAccountDialog
from src.utils.git_log_worker import GitLogManager
from src.views.home.ui_home import Ui_Home
from PySide6.QtWidgets import QWidget, QApplication, QAbstractItemView, QTreeWidgetItem, QFileDialog, QMessageBox, \
    QMenu, QDialog
from PySide6.QtCore import Qt, QDate, QThreadPool, QUrl
from PySide6.QtGui import QAction, QGuiApplication, QDesktopServices
from git import Repo, InvalidGitRepositoryError, GitCommandError
from src.config.config import Config
from src.views.settings.settings import Settings
from src.utils.ai_task import AITask


class Home(QWidget):
    def __init__(self):
        super(Home, self).__init__()
        pendulum.set_locale('zh')
        self.git_log_manager = None
        self.ui = Ui_Home()
        self.ui.setupUi(self)
        self.thread_pool = QThreadPool()
        self._date_changing_by_combo = False
        self.grouped_logs = {}
        self.init_ui()
        self.init_connect()

    def init_ui(self):
        self.setWindowTitle('AI 工作总结 - v0.0.3')
        self.ui.hbl_body.setStretch(2, 0)
        self.ui.wgt_right_content.hide()
        self.ui.btn_export.hide()
        self.init_theme()
        self.init_project_wgt()
        self.init_account_wgt()
        self.init_date()
        self.ui.pte_commit_log.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # TODO
        self.ui.btn_statistics.hide()
        self.ui.btn_filter.hide()
        self.ui.line_2.hide()

    def init_connect(self):
        self.ui.btn_homepage.clicked.connect(self.go_homepage)
        self.ui.btn_settings.clicked.connect(self.show_settings)
        self.ui.btn_statistics.clicked.connect(self.ui.wgt_right_content.show)
        self.ui.cbb_theme.currentTextChanged.connect(self.change_theme)
        self.ui.cbb_date.currentTextChanged.connect(self.change_date)
        self.ui.de_since.dateChanged.connect(self.on_date_edited)
        self.ui.de_until.dateChanged.connect(self.on_date_edited)
        self.ui.btn_get.clicked.connect(self.get_commit_info)
        self.ui.btn_ai_report.clicked.connect(self.ai_report)
        self.ui.btn_export.clicked.connect(self.export_report)
        self.ui.btn_project_add.clicked.connect(self.add_project)
        self.ui.twgt_project.itemChanged.connect(self.on_project_item_changed)
        self.ui.twgt_project.itemExpanded.connect(self.on_project_item_expanded)
        self.ui.twgt_project.itemCollapsed.connect(self.on_project_item_collapsed)
        self.ui.btn_account_add.clicked.connect(self.add_account)

    @staticmethod
    def go_homepage():
        QDesktopServices.openUrl(QUrl('https://github.com/Hunlongyu/work_report'))

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
    def on_project_item_changed(item: QTreeWidgetItem):
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
                    # if branch_data["type"] == "remote":
                    #     checked.append(f"remote/{branch_data['remote']}/{branch_data['name']}")
                    if branch_data["type"] == "local":
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
        # 检查是否是顶层项目节点
        if item.parent() is None:
            # 项目节点右键菜单：可以添加删除项目或者 fetch 所有远程的选项
            delete_action = QAction("删除项目", self)
            delete_action.triggered.connect(lambda: self.remove_project(item))
            menu.addAction(delete_action)

            fetch_all_remotes_action = QAction("获取所有远程更新", self)
            fetch_all_remotes_action.triggered.connect(lambda: self.fetch_project_all_remotes(item))
            menu.addAction(fetch_all_remotes_action)
        menu.exec_(self.ui.twgt_project.viewport().mapToGlobal(pos))

    def fetch_project_all_remotes(self, project_item: QTreeWidgetItem):
        """
        获取整个项目所有远程仓库的最新提交。
        """
        project_name = project_item.text(0)
        with Config().group("projects"):
            project_data_str = Config().get(project_name, "{}")
            try:
                project_config = json.loads(project_data_str)
                repo_path = project_config.get('path')
            except json.JSONDecodeError:
                QMessageBox.critical(self, "错误", f"无法解析项目 [{project_name}] 的配置。")
                return

        if not repo_path or not os.path.isdir(repo_path):
            QMessageBox.critical(self, "错误", f"项目 [{project_name}] 路径无效或不存在。")
            return

        try:
            repo = Repo(repo_path)
            for remote in repo.remotes:
                remote.fetch()  # fetch 所有远程

            QMessageBox.information(self, "更新成功", f"项目 [{project_name}] 已成功获取所有远程的最新提交。")

        except InvalidGitRepositoryError:
            QMessageBox.critical(self, "错误", f"路径 [{repo_path}] 不是一个有效的 Git 仓库。")
        except GitCommandError as e:
            QMessageBox.critical(self, "Git 错误", f"执行 Git Fetch 失败：\n{e.stderr.strip()}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取项目 [{project_name}] 更新失败：{e}")

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
                    project_item.setData(0, Qt.ItemDataRole.UserRole, folder_path)
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
        for branch in repo.branches:
            full_name = f"local/{branch.name}"
            item = QTreeWidgetItem(project_item)
            item.setText(0, branch.name)
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
            project_item.setData(0, Qt.ItemDataRole.UserRole, folder_path)
            self._add_branch_items(project_item, repo, checked_set=set())
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

    def init_account_wgt(self):
        self.ui.twgt_account.setColumnCount(2)
        self.ui.twgt_account.setRootIsDecorated(False)
        self.ui.twgt_account.setHeaderLabels(["用户名", "邮箱"])
        self.ui.twgt_account.itemChanged.connect(self.on_account_item_changed)
        self.ui.twgt_account.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.twgt_account.customContextMenuRequested.connect(self.show_account_context_menu)
        self.load_accounts()

    def show_account_context_menu(self, pos):
        item = self.ui.twgt_account.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)
        delete_action = QAction("删除账号", self)
        delete_action.triggered.connect(lambda: self.remove_account(item))
        menu.addAction(delete_action)
        menu.exec_(self.ui.twgt_account.viewport().mapToGlobal(pos))

    def remove_account(self, item: QTreeWidgetItem):
        """删除账号（JSON格式）"""
        name = item.text(0)
        reply = QMessageBox.question(
            self, "确认删除",
            f"是否删除账号 [{name}]？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        # 从配置中删除
        with Config().group("accounts"):
            accounts_json = Config().get("account_list", "{}")
            accounts = json.loads(accounts_json) if accounts_json else {}

            if name in accounts:
                del accounts[name]
                Config().set("account_list", json.dumps(accounts, ensure_ascii=False))

        # 从UI中删除
        self.ui.twgt_account.takeTopLevelItem(self.ui.twgt_account.indexOfTopLevelItem(item))

    def add_account(self):
        """添加新账号（保存为JSON格式）"""
        dialog = AddAccountDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, email = dialog.get_account_info()

            # 创建UI项
            item = QTreeWidgetItem([name, email])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Unchecked)  # 默认不勾选
            self.ui.twgt_account.addTopLevelItem(item)

            # 读取现有账号
            with Config().group("accounts"):
                accounts_json = Config().get("account_list", "{}")
                accounts = json.loads(accounts_json) if accounts_json else {}

                # 添加新账号（保留大小写）
                accounts[name] = {
                    "email": email,
                    "checked": False  # 默认未选中
                }

                # 保存回配置文件
                Config().set("account_list", json.dumps(accounts, ensure_ascii=False))

    def load_accounts(self):
        """从配置文件加载所有账号（JSON格式）"""
        self.ui.twgt_account.clear()
        with Config().group("accounts"):
            # 读取JSON格式的账号列表
            accounts_json = Config().get("account_list", "{}")
            try:
                accounts = json.loads(accounts_json)
            except json.JSONDecodeError:
                accounts = {}

            # 加载到UI
            for name, data in accounts.items():
                item = QTreeWidgetItem([name, data["email"]])
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(0, Qt.CheckState.Checked if data.get("checked", False) else Qt.CheckState.Unchecked)
                self.ui.twgt_account.addTopLevelItem(item)

    @staticmethod
    def on_account_item_changed(item: QTreeWidgetItem):
        """账号勾选状态变化时更新配置"""
        name = item.text(0)
        email = item.text(1)
        checked = item.checkState(0) == Qt.CheckState.Checked

        with Config().group("accounts"):
            accounts_json = Config().get("account_list", "{}")
            accounts = json.loads(accounts_json) if accounts_json else {}

            if name in accounts:
                accounts[name]["checked"] = checked
                Config().set("account_list", json.dumps(accounts, ensure_ascii=False))

    def init_date(self):
        date_options = [
            '今日', '昨日', '本周', '上周',
            '本月', '上个月', '本季度', '上季度',
            '上半年', '下半年', '今年', '自定义'
        ]
        self.ui.cbb_date.addItems(date_options)
        today = pendulum.today()
        self.ui.de_since.setDate(today)
        self.ui.de_until.setDate(today)

    @staticmethod
    def get_date_range(text: str) -> tuple[QDate, QDate]:
        now = pendulum.today()
        match text:
            case '今日':
                start = now.start_of('day')
                end = now.end_of('day')
            case '昨日':
                yesterday = now.subtract(days=1)
                start = yesterday.start_of('day')
                end = yesterday.end_of('day')
            case '本周':
                start = now.start_of('week')
                end = now.end_of('week')
            case '上周':
                last_week = now.subtract(weeks=1)
                start = last_week.start_of('week')
                end = last_week.end_of('week')
            case '本月':
                start = now.start_of('month')
                end = now.end_of('month')
            case '上个月':
                last_month = now.subtract(months=1)
                start = last_month.start_of('month')
                end = last_month.end_of('month')
            case '本季度':
                quarter = (now.month - 1) // 3 + 1
                start = pendulum.datetime(now.year, 3 * (quarter - 1) + 1, 1)
                end = start.add(months=3).subtract(days=1)
            case '上季度':
                quarter = (now.month - 1) // 3
                if quarter == 0:
                    start = pendulum.datetime(now.year - 1, 10, 1)
                else:
                    start = pendulum.datetime(now.year, 3 * (quarter - 1) + 1, 1)
                end = start.add(months=3).subtract(days=1)
            case '上半年':
                start = pendulum.datetime(now.year, 1, 1)
                end = pendulum.datetime(now.year, 6, 30)
            case '下半年':
                start = pendulum.datetime(now.year, 7, 1)
                end = pendulum.datetime(now.year, 12, 31)
            case '今年':
                start = now.start_of('year')
                end = now.end_of('year')
            case _:
                start = end = now

        return QDate(start.year, start.month, start.day), QDate(end.year, end.month, end.day)

    @staticmethod
    def get_datetime_range(text: str) -> tuple[str, str]:
        """返回用于 git log 的日期时间字符串格式"""
        now = pendulum.today()
        match text:
            case '今日':
                start = now.start_of('day')
                end = now.end_of('day')
            case '昨日':
                yesterday = now.subtract(days=1)
                start = yesterday.start_of('day')
                end = yesterday.end_of('day')
            case '本周':
                start = now.start_of('week')
                end = now.end_of('week')
            case '上周':
                last_week = now.subtract(weeks=1)
                start = last_week.start_of('week')
                end = last_week.end_of('week')
            case '本月':
                start = now.start_of('month')
                end = now.end_of('month')
            case '上个月':
                last_month = now.subtract(months=1)
                start = last_month.start_of('month')
                end = last_month.end_of('month')
            case '本季度':
                quarter = (now.month - 1) // 3 + 1
                start = pendulum.datetime(now.year, 3 * (quarter - 1) + 1, 1).start_of('day')
                end = start.add(months=3).subtract(days=1).end_of('day')
            case '上季度':
                quarter = (now.month - 1) // 3
                if quarter == 0:
                    start = pendulum.datetime(now.year - 1, 10, 1).start_of('day')
                else:
                    start = pendulum.datetime(now.year, 3 * (quarter - 1) + 1, 1).start_of('day')
                end = start.add(months=3).subtract(days=1).end_of('day')
            case '上半年':
                start = pendulum.datetime(now.year, 1, 1).start_of('day')
                end = pendulum.datetime(now.year, 6, 30).end_of('day')
            case '下半年':
                start = pendulum.datetime(now.year, 7, 1).start_of('day')
                end = pendulum.datetime(now.year, 12, 31).end_of('day')
            case '今年':
                start = now.start_of('year')
                end = now.end_of('year')
            case _:
                start = now.start_of('day')
                end = now.end_of('day')

        # 返回 ISO 格式的日期时间字符串，git log 可以直接使用
        return start.to_iso8601_string(), end.to_iso8601_string()

    def on_date_edited(self):
        if not self._date_changing_by_combo and self.ui.cbb_date.currentText() != "自定义":
            self.ui.cbb_date.setCurrentText("自定义")

    def change_date(self, text: str):
        self._date_changing_by_combo = True  # 设置标志
        try:
            if text != "自定义":
                start, end = self.get_date_range(text)
                self.ui.de_since.setDate(start)
                self.ui.de_until.setDate(end)
        finally:
            self._date_changing_by_combo = False  # 清除标志

    def get_commit_info_account(self):
        """获取选中的账号（从JSON加载的账号）"""
        selected_authors = set()
        for i in range(self.ui.twgt_account.topLevelItemCount()):
            item = self.ui.twgt_account.topLevelItem(i)
            if item.checkState(0) == Qt.CheckState.Checked:
                selected_authors.add(item.text(0))
        return selected_authors

    def get_commit_info_project_branch(self):
        project_map = {}
        tree = self.ui.twgt_project
        for i in range(tree.topLevelItemCount()):
            project_item = tree.topLevelItem(i)
            project_name = project_item.text(0).strip()
            repo_path = project_item.data(0, Qt.ItemDataRole.UserRole)
            if not repo_path or not os.path.exists(repo_path):
                continue

            branches = []
            for j in range(project_item.childCount()):
                branch_item = project_item.child(j)
                if branch_item.checkState(0) == Qt.CheckState.Checked:
                    branch_name = branch_item.text(0).strip()
                    if branch_name:
                        branches.append(branch_name)
            if branches:
                project_map[project_name] = {
                    "path": repo_path,
                    "branches": branches
                }
        return project_map

    def get_commit_info(self):
        selected_authors = self.get_commit_info_account()
        if not selected_authors:
            QMessageBox.warning(
                self,
                "错误",
                "请选择账号！"
            )
            return

        project_map = self.get_commit_info_project_branch()
        if not project_map:
            QMessageBox.warning(
                self,
                "错误",
                "请选择项目和分支！"
            )
            return

        self.grouped_logs.clear()
        since_date = self.ui.de_since.date()
        until_date = self.ui.de_until.date()

        # 转换为 pendulum 日期对象并设置时间
        since = pendulum.datetime(
            since_date.year(), since_date.month(), since_date.day(),
            0, 0, 0  # 00:00:00
        )
        until = pendulum.datetime(
            until_date.year(), until_date.month(), until_date.day(),
            23, 59, 59  # 23:59:59
        )
        self.git_log_manager = GitLogManager(max_threads=4)
        self.git_log_manager.log_collected.connect(self.on_log_collected)
        self.git_log_manager.error.connect(self.on_log_error)
        self.git_log_manager.progress.connect(self.on_progress)
        self.git_log_manager.finished.connect(self.on_all_finished)
        self.git_log_manager.start(project_map, selected_authors, since.to_iso8601_string(), until.to_iso8601_string())

    def on_log_collected(self, project, branch, author, logs):
        key = (project, branch, author)
        if key not in self.grouped_logs:
            self.grouped_logs[key] = []
        self.grouped_logs[key].extend(logs)

    def on_log_error(self, message):
        QMessageBox.warning(
            self,
            "错误",
            message
        )

    def on_progress(self, done, total):
        percentage = done / total * 100
        self.ui.progress.setValue(percentage)

    def on_all_finished(self):
        self.ui.pte_commit_log.clear()
        unique_commits = set()
        # 遍历每个项目分支账号组，先写标题，再写去重后的日志
        for (project, branch, author), logs in self.grouped_logs.items():
            self.ui.pte_commit_log.appendPlainText(f"【项目】{project}\n【分支】{branch}\n【账号】{author}")

            # 当前组去重
            unique_logs = []
            for log in logs:
                if log["commit"] not in unique_commits:
                    unique_commits.add(log["commit"])
                    unique_logs.append(log)

            for log in unique_logs:
                self.ui.pte_commit_log.appendPlainText(f"{log['date']} {log['message']}")
            self.ui.pte_commit_log.appendPlainText("")

    @staticmethod
    def show_settings():
        settings = Settings()
        settings.exec()

    def handle_success(self, msg):
        print("总结成功")
        self.ui.hbl_body.setStretch(2, 4)
        self.ui.wgt_right_content.show()
        self.ui.btn_export.show()
        self.ui.pte_ai_report.setPlainText(msg)
        self.ui.btn_ai_report.setText("AI 总结")
        self.ui.btn_ai_report.setEnabled(True)

    def handle_error(self, msg):
        self.ui.btn_ai_report.setText("AI 总结")
        self.ui.btn_ai_report.setEnabled(True)
        QMessageBox.critical(self, '错误', f"总结失败：\n{msg}")

    def ai_report(self):
        if not self.grouped_logs:
            QMessageBox.warning(
                self,
                "错误",
                "请先获取提交信息！"
            )
            return

        api_key = Config().get('settings/key', '')
        api_url = Config().get('settings/address', '')
        api_model = Config().get('settings/model', '')
        prompt = Config().get('settings/prompt', '')
        if not api_key or not api_url or not api_model or not prompt:
            QMessageBox.warning(
                self,
                "错误",
                "请先确认正确的填写了 ai 设置项。"
            )
            return

        git_log = self.ui.pte_commit_log.toPlainText()
        self.ui.btn_ai_report.setText("生成中...")
        self.ui.btn_ai_report.setEnabled(False)
        self.ui.pte_ai_report.clear()

        task = AITask(
            api_key,
            api_url,
            api_model,
            prompt,
            git_log
        )
        task.signals.success.connect(self.handle_success)
        task.signals.error.connect(self.handle_error)
        self.thread_pool.start(task)

    def export_report(self):
        report_text = self.ui.pte_ai_report.toPlainText()

        if not report_text.strip():
            QMessageBox.warning(
                self,
                "错误",
                "报告为空，请先生成！"
            )
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(report_text)

        QMessageBox.information(
            self,
            "成功",
            "AI 报告已复制到剪贴板！"
        )
