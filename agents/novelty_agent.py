from agents.base import BaseAgent
from orchestrator.protocols import AgentResult


class NoveltyAgent(BaseAgent):
    role = "novelty"
    temperature = 0.4
    max_tokens = 8192
    system_prompt = "你是一个学术创新性评审专家。请评估论文的创新贡献程度。"


_agent = NoveltyAgent()

NOVELTY_RUBRIC = [
    "是否评估了研究问题新颖性",
    "是否评估了与现有工作的差异",
    "是否检查了贡献清晰度",
    "是否区分了增量改进与突破性创新",
    "是否检查了过度声称",
    "每个发现是否引用了原文证据",
]


def review_novelty(parsed_structure: str, original_text: str) -> AgentResult:
    prompt = f"""请评估以下论文段落的创新贡献程度。

评估维度：
1. 研究问题新颖性：研究问题是否具有原创性
2. 与现有工作的差异：作者是否清晰区分了与 prior work 的差异
3. 贡献明确性：贡献是否被清晰陈述
4. 增量性 vs 突破性：贡献是增量改进还是突破性创新
5. 过度声称：作者是否做出了超出证据支持的声称

引用原文作为证据。如果没有明显问题，请说明"未发现创新性明显问题"。

原始段落：
{original_text}

结构分析：
{parsed_structure}"""
    return _agent.run(prompt)
