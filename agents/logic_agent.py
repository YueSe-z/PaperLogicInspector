from api_client import chat_completion


def check_logic(parsed_structure: str, original_text: str) -> str:
    prompt = f"""你是一名逻辑学专家。请基于下面的段落结构分析，检查原始段落中是否存在以下逻辑问题：
- 论点与结论不一致（跑题）
- 论据无法支撑论点（证据不足）
- 论证方式错误（如错误因果、循环论证）
- 关键跳跃（推理链条缺失中间环节）

请输出具体问题列表，每条一行。如果没有问题，输出"未发现明显逻辑问题"。

原始段落：
{original_text}

结构分析：
{parsed_structure}"""
    return chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
