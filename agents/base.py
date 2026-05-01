from anthropic import BadRequestError

from api_client import chat_completion
from orchestrator.protocols import AgentResult, AgentStatus

NON_RETRYABLE = (BadRequestError,)


class BaseAgent:
    role: str = "base"
    temperature: float = 0.3
    max_tokens: int = 8192
    system_prompt: str = ""

    def run(self, user_prompt: str) -> AgentResult:
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ]
            content = chat_completion(
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return AgentResult(status=AgentStatus.DONE, content=content)
        except NON_RETRYABLE as e:
            return AgentResult(
                status=AgentStatus.BLOCKED,
                content="",
                concerns=[f"{self.role} agent: bad request - {str(e)}"],
            )
        except Exception as e:
            return AgentResult(
                status=AgentStatus.BLOCKED,
                content="",
                concerns=[f"{self.role} agent failed: {str(e)}"],
            )
