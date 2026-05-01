from agents.base import BaseAgent
from orchestrator.protocols import AgentResult, AgentStatus


class RubricReviewer(BaseAgent):
    role = "rubric_reviewer"
    temperature = 0.2
    max_tokens = 4096
    system_prompt = "你是一个评审质量审核员。请检查评审报告是否完整覆盖了所有要求的评审维度。"


_agent = RubricReviewer()


def review_rubric(report: str, rubric_items: list[str]) -> AgentResult:
    items_text = "\n".join(f"- {item}" for item in rubric_items)
    prompt = f"""请检查以下评审报告是否完整覆盖了所有要求的评审维度。

评审报告：
{report}

要求的评审维度：
{items_text}

请逐个检查每个维度：
- 如果已覆盖：标记为 ✓
- 如果部分覆盖但有不足：标记为 ⚠ 并说明缺失了什么
- 如果完全未覆盖：标记为 ✗ 并说明需要补充什么

最后给出整体状态：
- 全部 ✓ → DONE
- 有 ⚠ 但无 ✗ → DONE_WITH_CONCERNS（在 concerns 中列出 ⚠ 项）
- 有 ✗ → BLOCKED（在 concerns 中列出 ✗ 项）

请按以下格式输出：
状态：[DONE/DONE_WITH_CONCERNS/BLOCKED]
缺失项：（如有）具体列出"""
    result = _agent.run(prompt)
    status = _parse_status(result.content)
    return AgentResult(
        status=status,
        content=result.content,
        concerns=result.concerns,
        metadata=result.metadata,
    )


def _parse_status(content: str) -> AgentStatus:
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("状态：") or line.startswith("状态:"):
            value = line.split("：", 1)[-1].split(":", 1)[-1].strip()
            if value == "BLOCKED":
                return AgentStatus.BLOCKED
            if value == "DONE_WITH_CONCERNS":
                return AgentStatus.DONE_WITH_CONCERNS
    return AgentStatus.DONE
