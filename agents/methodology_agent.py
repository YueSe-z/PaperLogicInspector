from agents.base import BaseAgent
from orchestrator.protocols import AgentResult


class MethodologyAgent(BaseAgent):
    role = "methodology"
    temperature = 0.3
    max_tokens = 8192
    system_prompt = "你是一个研究方法论评审专家。请评估论文使用的研究方法是否合理、严谨、可复现。"


_agent = MethodologyAgent()

METHODOLOGY_RUBRIC = [
    "是否评估了方法选择合理性",
    "是否检查了实施细节充分性",
    "是否评估了可复现性",
    "是否讨论了局限性",
    "是否考虑了替代方案",
    "每个发现是否引用了原文证据",
]


def review_methodology(parsed_structure: str, original_text: str) -> AgentResult:
    prompt = f"""请评估以下论文段落的研究方法是否合理、严谨、可复现。

对每个段落，评估以下维度：
1. 方法选择合理性：方法是否适合研究问题
2. 实施细节充分性：是否描述了足够的实施步骤
3. 可复现性：其他研究者能否根据描述复现实验
4. 局限性讨论：作者是否讨论了方法的局限性
5. 替代方案考虑：是否考虑了其他可能的方法

对于发现的每个问题，请引用具体的原文段落作为证据。
如果没有发现明显问题，请明确说明"未发现方法论明显问题"。

原始段落：
{original_text}

结构分析：
{parsed_structure}"""
    return _agent.run(prompt)
