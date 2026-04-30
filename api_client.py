from anthropic import Anthropic
from config import API_KEY, BASE_URL, MODEL_NAME

client = Anthropic(api_key=API_KEY, base_url=BASE_URL)


def chat_completion(messages: list[dict], temperature: float = 0.3, max_tokens: int = 4096) -> str:
    system_prompt = None
    user_msgs = []
    for m in messages:
        if m["role"] == "system":
            system_prompt = m["content"]
        else:
            user_msgs.append(m)

    kwargs = {
        "model": MODEL_NAME,
        "max_tokens": max_tokens,
        "messages": user_msgs,
        "temperature": temperature,
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    resp = client.messages.create(**kwargs)
    return resp.content[0].text
