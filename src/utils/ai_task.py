from PySide6.QtCore import QObject, Signal, QRunnable
from openai import OpenAI


class AITaskSignals(QObject):
    success = Signal(str)
    error = Signal(str)


class AITask(QRunnable):
    def __init__(self, api_key: str, base_url: str = '', model: str = 'deepseek-chat', prompt: str = '',
                 content: str = ''):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.prompt = prompt
        self.content = content
        self.signals = AITaskSignals()

    def run(self):
        try:
            if not self.content.strip():
                raise ValueError("用户输入内容不能为空！")
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.prompt},
                    {'role': 'user', 'content': self.content}
                ],
                stream=False,
                timeout=60
            )
            if not response.choices:
                raise ValueError("API 返回无有效结果！")

            reply = response.choices[0].message.content
            if not reply.strip():
                raise ValueError("API 返回内容为空！")
            self.signals.success.emit(reply)

        except Exception as e:
            self.signals.error.emit(f'{type(e).__name__}: {e}')
