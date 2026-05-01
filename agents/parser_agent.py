from agents.base import BaseAgent
from orchestrator.protocols import AgentResult


class ParserAgent(BaseAgent):
    role = "parser"
    temperature = 0.3
    max_tokens = 8192
    system_prompt = "你是一个文本结构分析专家。请对文本逐段分析其论证结构。"


_agent = ParserAgent()


def parse_paragraph_structured(text: str) -> AgentResult:
    prompt = f"""请对以下文本逐段分析其论证结构。

对于每个自然段（以空行分隔），识别：
- 论点：作者试图证明的核心观点
- 论据：支撑论点的事实、数据或引用（缺失则标注"缺失"）
- 论证方式：举例、因果、对比、演绎等（缺失则标注"缺失"）
- 结论：段落的最终落脚点（缺失则标注"缺失"）

文本内容：
{text}

请按以下格式逐段输出（保留原文段落顺序，每段编号标注）：
【段落1】
论点：...
论据：...
论证方式：...
结论：...

【段落2】
..."""
    return _agent.run(prompt)


def parse_paragraphs(paragraphs: list[str]) -> list[AgentResult]:
    return [parse_paragraph_structured(p) for p in paragraphs]
