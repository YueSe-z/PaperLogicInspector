from agents.base import BaseAgent
from orchestrator.protocols import AgentResult


class RewriteAgent(BaseAgent):
    role = "rewrite"
    temperature = 0.3
    max_tokens = 8192
    system_prompt = "你是一名学术写作顾问。请根据逻辑问题对原文进行精准修改。"


_agent = RewriteAgent()


def suggest_rewrite_structured(original_text: str, issues: str) -> AgentResult:
    prompt = f"""请根据下面列出的逻辑问题，对原文进行精准修改。

关键要求：
- 严格保持原文的段落结构、换行、标点格式不变
- 只修改存在逻辑问题的句段，其他部分一字不动
- 修改后仍然保持原文的写作风格和语气
- 在被修改的位置用【】标注原句，后面用 → 引出修改后的句子

原始文本：
{original_text}

逻辑问题：
{issues}

请输出（保持原文格式）：
【修改后的完整文本】
...
---
改动清单：
1. 原句【...】→ 改为【...】，原因：...
2. ..."""
    return _agent.run(prompt)
