import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL") or None
MODEL_NAME = os.getenv("MODEL_NAME", "claude-sonnet-4-5-20250929")

MAX_PARAGRAPH_CHARS = int(os.getenv("MAX_PARAGRAPH_CHARS", "3000"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "6"))
MAX_RUBRIC_RETRIES = int(os.getenv("MAX_RUBRIC_RETRIES", "2"))

if not API_KEY:
    raise RuntimeError(
        "未检测到 API_KEY。请在 .env 文件中配置 API_KEY。"
    )
