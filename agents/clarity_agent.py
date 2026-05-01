from agents.base import BaseAgent
from orchestrator.protocols import AgentResult


class ClarityAgent(BaseAgent):
    role = "clarity"
    temperature = 0.3
    max_tokens = 8192
    system_prompt = "你是一个学术写作清晰度评审专家。请评估论文的表达是否清晰、准确、易于理解。"


_agent = ClarityAgent()

CLARITY_RUBRIC = [
    "是否检查了术语定义清晰度",
    "是否评估了逻辑流畅性",
    "是否检查了句子结构合理性",
    "是否检查了图表引用准确性",
    "是否检查了歧义性表述",
    "是否检查了摘要与结论一致性",
    "每个发现是否引用了原文证据",
]


def review_clarity(parsed_structure: str, original_text: str) -> AgentResult:
    prompt = f"""请评估以下论文段落的表达是否清晰、准确、易于理解。

评估维度：
1. 术语定义清晰度：专业术语是否在首次使用时定义
2. 逻辑流畅性：段落之间和段落内部的过渡是否自然
3. 句子结构：是否存在过长或结构混乱的句子
4. 歧义性：是否存在可能引起歧义的表述
5. 摘要与结论一致性：摘要和结论的表述是否一致

引用原文作为证据。如果没有明显问题，请说明"未发现清晰度明显问题"。

原始段落：
{original_text}

结构分析：
{parsed_structure}"""
    return _agent.run(prompt)
