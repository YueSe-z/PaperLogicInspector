from agents.base import BaseAgent
from orchestrator.protocols import AgentResult


class EvidenceAgent(BaseAgent):
    role = "evidence"
    temperature = 0.3
    max_tokens = 8192
    system_prompt = "你是一个实验设计与数据审核专家。请评估论文中的实验证据是否有效、充分。"


_agent = EvidenceAgent()

EVIDENCE_RUBRIC = [
    "是否评估了实验设计合理性",
    "是否检查了数据质量",
    "是否评估了统计方法正确性",
    "是否检查了结果解释合理性",
    "是否检查了对照组设置",
    "是否检查了混淆因素控制",
    "每个发现是否引用了原文证据",
]


def review_evidence(parsed_structure: str, original_text: str) -> AgentResult:
    prompt = f"""请评估以下论文段落的实验证据是否有效、充分。

评估维度：
1. 实验设计合理性：实验设置是否能够回答研究问题
2. 数据质量：数据来源、样本量、数据清洗是否合理
3. 统计方法正确性：使用的统计检验是否恰当
4. 结果解释的合理性：从数据到结论的推理是否合理
5. 对照组设置：是否有恰当的基线/对照组
6. 混淆因素控制：是否控制了潜在的混淆变量

在每个发现中引用原文。如果没有明显问题，请说明"未发现证据明显问题"。

原始段落：
{original_text}

结构分析：
{parsed_structure}"""
    return _agent.run(prompt)
