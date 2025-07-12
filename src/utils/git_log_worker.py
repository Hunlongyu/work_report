from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool
import subprocess


class GitLogSignals(QObject):
    finished = Signal(str, str, str, list)  # project, branch, author, logs
    error = Signal(str)
    progress = Signal(int, int)  # done_count, total_count
    all_finished = Signal()


class GitLogTask(QRunnable):
    def __init__(self, repo_path, project_name, branch, author, since, until, signals):
        super().__init__()
        self.repo_path = repo_path
        self.project_name = project_name
        self.branch = branch
        self.author = author
        self.since = since
        self.until = until
        self.signals = signals

    def run(self):
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            if not self.branch.startswith("origin/"):
                # 获取所有分支，包含 remote 的
                result = subprocess.run(['git', 'branch', '-a'], cwd=self.repo_path,
                                        stdout=subprocess.PIPE, text=True, startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
                all_branches = result.stdout
                possible_remote = f"remotes/origin/{self.branch}"
                if possible_remote in all_branches:
                    self.branch = f"origin/{self.branch}"
            cmd = [
                'git', 'log',
                f'--author={self.author}',
                f'--since={self.since}',
                f'--until={self.until}',
                '--pretty=format:%h%x1f%ad%x1f%s%x1e',
                '--date=iso',
                self.branch
            ]
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode != 0:
                self.signals.error.emit(
                    f"{self.project_name} 分支 {self.branch} 获取失败：{result.stderr.strip()}"
                )
                return

            raw_output = result.stdout.strip('\x1e').split('\x1e')
            logs = []
            for entry in raw_output:
                if not entry.strip():
                    continue
                parts = entry.strip().split('\x1f')
                if len(parts) == 3:
                    logs.append({
                        "commit": parts[0],
                        "date": parts[1],
                        "message": parts[2]
                    })

            self.signals.finished.emit(self.project_name, self.branch, self.author, logs)

        except Exception as e:
            self.signals.error.emit(f"[{self.project_name}:{self.branch}] 异常：{e}")


class GitLogManager(QObject):
    """
    管理所有 GitLogTask 并发执行，统计进度。
    """
    finished = Signal()
    progress = Signal(int, int)  # done, total
    log_collected = Signal(str, str, str, list)  # project, branch, author, logs
    error = Signal(str)

    def __init__(self, max_threads=None):
        super().__init__()
        self.thread_pool = QThreadPool.globalInstance()
        if max_threads:
            self.thread_pool.setMaxThreadCount(max_threads)
        self.total_tasks = 0
        self.done_tasks = 0
        self.signals = GitLogSignals()
        self.signals.finished.connect(self._on_task_finished)
        self.signals.error.connect(self._on_task_error)

    def start(self, project_map, selected_authors, since, until):
        self.total_tasks = 0
        self.done_tasks = 0

        # 预处理日期字符串
        if hasattr(since, 'toString'):
            since = since.toString("yyyy-MM-dd")
        if hasattr(until, 'toString'):
            until = until.toString("yyyy-MM-dd")

        # 提交所有任务
        for project_name, project_info in project_map.items():
            repo_path = project_info["path"]
            for branch in project_info["branches"]:
                for author in selected_authors:
                    task = GitLogTask(repo_path, project_name, branch, author, since, until, self.signals)
                    self.thread_pool.start(task)
                    self.total_tasks += 1

        if self.total_tasks == 0:
            # 无任务时直接发完成信号
            self.finished.emit()
        else:
            self.progress.emit(self.done_tasks, self.total_tasks)

    def _on_task_finished(self, project, branch, author, logs):
        self.done_tasks += 1
        self.log_collected.emit(project, branch, author, logs)
        self.progress.emit(self.done_tasks, self.total_tasks)
        if self.done_tasks == self.total_tasks:
            self.finished.emit()

    def _on_task_error(self, message):
        self.done_tasks += 1
        self.error.emit(message)
        self.progress.emit(self.done_tasks, self.total_tasks)
        if self.done_tasks == self.total_tasks:
            self.finished.emit()
