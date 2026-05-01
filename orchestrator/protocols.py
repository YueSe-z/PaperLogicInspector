from enum import Enum
from dataclasses import dataclass, field


class AgentStatus(str, Enum):
    DONE = "DONE"
    DONE_WITH_CONCERNS = "DONE_WITH_CONCERNS"
    BLOCKED = "BLOCKED"


@dataclass
class AgentResult:
    status: AgentStatus
    content: str
    concerns: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class ParagraphAnalysis:
    index: int
    text: str
    structure: str | None = None


@dataclass
class ReviewDimension:
    name: str
    worker: callable
    rubric_items: list[str]
    enabled: bool = True
