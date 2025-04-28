import json

import ollama

from utils.settings import settings


class OllaMa:
    def __init__(self, host: str = "http://127.0.0.1:11434"):
        self.host = host

    def generate_content(self, prompt: str,  model: str = "gemma3:4b"):
        client = ollama.Client(
            host=self.host
        )

        try:
            result = client.generate(
                model=model,
                prompt=prompt,
                options=dict(num_ctx=settings.OLLAMA_MAX_PROMPT)
            )
        except Exception as exc:
            print(exc)
            raise exc

        if result.done is not True:
            raise Exception(f"Model generate error: {json.dumps(result.__dict__)}")

        return result