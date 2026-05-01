from agents.base import BaseAgent
from orchestrator.protocols import AgentResult


class LogicAgent(BaseAgent):
    role = "logic"
    temperature = 0.4
    max_tokens = 8192
    system_prompt = "你是一名逻辑学专家。请检查段落中是否存在逻辑问题。"


_agent = LogicAgent()

LOGIC_RUBRIC = [
    "是否检查了论点与结论一致性",
    "是否检查了论据充分性",
    "是否检查了论证方式正确性",
    "是否检查了推理链条完整性",
    "每个发现是否引用了原文证据",
]


def check_logic_structured(parsed_structure: str, original_text: str) -> AgentResult:
    prompt = f"""请基于下面的段落结构分析，检查原始段落中是否存在以下逻辑问题：
- 论点与结论不一致（跑题）
- 论据无法支撑论点（证据不足）
- 论证方式错误（如错误因果、循环论证）
- 关键跳跃（推理链条缺失中间环节）

请输出具体问题列表，每条一行。如果没有问题，输出"未发现明显逻辑问题"。

原始段落：
{original_text}

结构分析：
{parsed_structure}"""
    return _agent.run(prompt)
