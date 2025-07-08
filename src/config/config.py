import os
from contextlib import contextmanager
from PySide6.QtCore import QSettings, QStandardPaths
from PySide6.QtWidgets import QApplication

class Config:
    _instance = None
    _settings = None
    _current_group = ""  # 当前分组路径

    def __new__(cls):
        if cls._instance is None:
            if not QApplication.instance():
                raise RuntimeError("必须先创建QApplication实例")

            cls._instance = super().__new__(cls)
            cls._instance.init_settings()
        return cls._instance

    def init_settings(self):
        _config_path = os.path.join(os.getenv('APPDATA'), 'work_report', 'config.ini')
        os.makedirs(os.path.dirname(_config_path), exist_ok=True)
        self._settings = QSettings(_config_path, QSettings.Format.IniFormat)

    def get(self, key, default=None):
        """获取配置值（自动包含当前分组前缀）"""
        full_key = f"{self._current_group}/{key}" if self._current_group else key
        return self._settings.value(full_key, default)

    def set(self, key, value):
        """设置配置值（自动包含当前分组前缀）"""
        full_key = f"{self._current_group}/{key}" if self._current_group else key
        self._settings.setValue(full_key, value)
        self._settings.sync()

    @contextmanager
    def group(self, group_name):
        """分组上下文管理器"""
        original_group = self._current_group
        try:
            # 处理嵌套分组
            self._current_group = f"{original_group}/{group_name}" if original_group else group_name
            yield self
        finally:
            self._current_group = original_group

    def begin_group(self, group_name):
        """手动开始分组（需配合end_group使用）"""
        self._current_group = f"{self._current_group}/{group_name}" if self._current_group else group_name
        return self

    def end_group(self):
        """结束当前分组"""
        if '/' in self._current_group:
            self._current_group = self._current_group.rsplit('/', 1)[0]
        else:
            self._current_group = ""
        return self

    def contains(self, key):
        """检查键是否存在（考虑当前分组）"""
        full_key = f"{self._current_group}/{key}" if self._current_group else key
        return full_key in self._settings.allKeys()

    def remove(self, key):
        """删除键（考虑当前分组）"""
        full_key = f"{self._current_group}/{key}" if self._current_group else key
        self._settings.remove(full_key)
        self._settings.sync()

    def child_keys(self):
        """获取当前分组下的所有键"""
        self._settings.beginGroup(self._current_group)
        keys = self._settings.childKeys()
        self._settings.endGroup()
        return keys

    def child_groups(self):
        """获取当前分组下的所有子分组"""
        self._settings.beginGroup(self._current_group)
        groups = self._settings.childGroups()
        self._settings.endGroup()
        return groups
