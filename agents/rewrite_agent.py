from api_client import chat_completion


def suggest_rewrite(original_text: str, issues: str) -> str:
    prompt = f"""你是一名学术写作顾问。请根据下面列出的逻辑问题，对原始段落进行改写。要求：
- 保留原意，但修复所有指出的逻辑问题
- 给出2种不同风格的改写版本（版本1：严谨学术风；版本2：清晰举例风）
- 每个版本后面用一句话说明改动了哪里

原始段落：
{original_text}

逻辑问题：
{issues}

输出格式：
版本1（严谨学术风）：
[改写内容]
改动说明：...

版本2（清晰举例风）：
[改写内容]
改动说明：..."""
    return chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )
