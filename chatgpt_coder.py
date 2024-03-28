import openai


class ChatGPTCoder:
    def __init__(self, openai_api_key):
        self.client = openai.OpenAI(api_key=openai_api_key)
        openai.api_key = openai_api_key
