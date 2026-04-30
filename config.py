import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.deepseek.com/anthropic")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-v4-pro[1m]")

if not API_KEY:
    raise RuntimeError(
        "未检测到 API_KEY。请复制 .env.example 为 .env，"
        "并将 your-deepseek-api-key 替换为你的真实 DeepSeek API Key。"
    )
