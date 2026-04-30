from api_client import chat_completion


def parse_paragraph(text: str) -> str:
    prompt = f"""你是一个文本结构分析专家。请将以下段落拆解为四个部分：
1. 论点：作者试图证明的核心观点
2. 论据：支撑论点的事实、数据或引用
3. 论证方式：举例、因果、对比、演绎等
4. 结论：段落的最终落脚点

如果某部分缺失，请明确标注"缺失"。

段落内容：
{text}

请用以下格式输出（不要输出额外解释）：
论点：...
论据：...
论证方式：...
结论：..."""
    return chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
