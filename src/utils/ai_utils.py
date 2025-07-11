from PySide6.QtCore import QObject, Signal, QRunnable
from openai import OpenAI


class ApiKeyCheckSignals(QObject):
    success = Signal(bool)
    error = Signal(str)


class AIKeyCheckTask(QRunnable):
    def __init__(self, api_key: str, base_url: str = "", model: str = "deepseek-chat"):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.signals = ApiKeyCheckSignals()

    def run(self):
        try:
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=1,
                timeout=10
            )
            result = bool(response.choices[0].message.content)
            self.signals.success.emit(result)

        except Exception as e:
            self.signals.error.emit(f"{type(e).__name__}: {e}")
