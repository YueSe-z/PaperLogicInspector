import time
import anthropic
from config import API_KEY, BASE_URL, MODEL_NAME

client = anthropic.Anthropic(api_key=API_KEY, base_url=BASE_URL, timeout=300)

RETRYABLE = (
    anthropic.APIConnectionError,
    anthropic.APITimeoutError,
    anthropic.RateLimitError,
    anthropic.APIStatusError,
)


def chat_completion(messages: list, temperature: float = 0.3, max_tokens: int = 4096) -> str:
    last_error = None

    system = ""
    user_messages = []
    for msg in messages:
        if msg["role"] == "system":
            system = msg["content"]
        else:
            user_messages.append(msg)

    for attempt in range(5):
        try:
            resp = client.messages.create(
                model=MODEL_NAME,
                max_tokens=max_tokens,
                system=system,
                messages=user_messages,
                temperature=temperature,
            )
            for block in resp.content:
                if block.type == "text":
                    return block.text or ""
            return ""
        except RETRYABLE as e:
            last_error = e
            if attempt < 4:
                time.sleep(3 ** attempt)
    raise last_error
