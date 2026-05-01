from concurrent.futures import ThreadPoolExecutor, as_completed

from config import MAX_RUBRIC_RETRIES, MAX_PARAGRAPH_CHARS, MAX_WORKERS
from orchestrator.protocols import AgentStatus, AgentResult, ParagraphAnalysis, ReviewDimension
from orchestrator.paragraph_splitter import split_paragraphs
from agents.parser_agent import parse_paragraph_structured
from agents.rubric_reviewer import review_rubric
from agents.rewrite_agent import suggest_rewrite_structured
from agents.logic_agent import check_logic_structured, LOGIC_RUBRIC
from agents.methodology_agent import review_methodology, METHODOLOGY_RUBRIC
from agents.novelty_agent import review_novelty, NOVELTY_RUBRIC
from agents.evidence_agent import review_evidence, EVIDENCE_RUBRIC
from agents.clarity_agent import review_clarity, CLARITY_RUBRIC


class ReviewPipeline:

    def __init__(self, dimensions: list[ReviewDimension] = None, max_workers: int = None):
        self.dimensions = dimensions or self._default_dimensions()
        self.max_workers = max_workers or MAX_WORKERS
        self.progress_callback: callable = None

    @staticmethod
    def _default_dimensions() -> list[ReviewDimension]:
        return [
            ReviewDimension(name="logic", worker=check_logic_structured, rubric_items=LOGIC_RUBRIC),
            ReviewDimension(name="methodology", worker=review_methodology, rubric_items=METHODOLOGY_RUBRIC),
            ReviewDimension(name="novelty", worker=review_novelty, rubric_items=NOVELTY_RUBRIC),
            ReviewDimension(name="evidence", worker=review_evidence, rubric_items=EVIDENCE_RUBRIC),
            ReviewDimension(name="clarity", worker=review_clarity, rubric_items=CLARITY_RUBRIC),
        ]

    def run(self, text: str) -> dict:
        paragraphs = split_paragraphs(text, max_chars=MAX_PARAGRAPH_CHARS)
        self._emit("split", {"paragraph_count": len(paragraphs)})

        paragraph_analyses = self._stage_parse(paragraphs)

        dimension_results = self._stage_review(paragraphs, paragraph_analyses)

        rewrites = self._stage_rewrite(paragraphs, dimension_results)

        return self._assemble_report(text, paragraphs, paragraph_analyses,
                                     dimension_results, rewrites)

    def _stage_parse(self, paragraphs: list[str]) -> list[ParagraphAnalysis]:
        analyses = [ParagraphAnalysis(index=i, text=p) for i, p in enumerate(paragraphs)]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(parse_paragraph_structured, p.text): i
                for i, p in enumerate(analyses)
            }
            for future in as_completed(futures):
                i = futures[future]
                result = future.result()
                analyses[i].structure = result.content if result.status == AgentStatus.DONE else (result.concerns[0] if result.concerns else "解析失败")
                self._emit("parse", {"paragraph": i, "total": len(paragraphs)})

        return analyses

    def _stage_review(self, paragraphs: list[str],
                      analyses: list[ParagraphAnalysis]) -> dict:
        all_text = "\n\n".join(paragraphs)
        structures = "\n\n".join(
            f"【段落{a.index + 1}】\n{a.structure}" for a in analyses
        )

        results = {}
        for dim in self.dimensions:
            if not dim.enabled:
                continue

            current_text = all_text

            worker_result = dim.worker(structures, current_text)
            self._emit("review_worker", {"dimension": dim.name, "status": worker_result.status.value})

            if worker_result.status == AgentStatus.DONE:
                rubric_result = review_rubric(worker_result.content, dim.rubric_items)
                self._emit("review_rubric", {
                    "dimension": dim.name,
                    "status": rubric_result.status.value,
                })

                retry = 0
                while rubric_result.status != AgentStatus.DONE and retry < MAX_RUBRIC_RETRIES:
                    retry += 1
                    self._emit("review_rubric", {
                        "dimension": dim.name,
                        "status": "retrying",
                        "attempt": retry,
                        "reasons": rubric_result.concerns,
                    })
                    feedback = "以下是上一轮审查中未覆盖的评分项，请补充审查：\n" + \
                               "\n".join(f"- {c}" for c in rubric_result.concerns)
                    current_text = f"{feedback}\n\n{all_text}"

                    worker_result = dim.worker(structures, current_text)
                    self._emit("review_worker", {
                        "dimension": dim.name,
                        "status": worker_result.status.value,
                        "attempt": retry + 1,
                    })

                    if worker_result.status != AgentStatus.DONE:
                        break

                    rubric_result = review_rubric(worker_result.content, dim.rubric_items)
                    self._emit("review_rubric", {
                        "dimension": dim.name,
                        "status": rubric_result.status.value,
                        "attempt": retry + 1,
                    })

                final_status = rubric_result.status
                concerns = rubric_result.concerns
            else:
                final_status = worker_result.status
                concerns = worker_result.concerns

            results[dim.name] = AgentResult(
                status=final_status,
                content=worker_result.content,
                concerns=concerns,
            )

        return results

    def _stage_rewrite(self, paragraphs: list[str],
                       dimension_results: dict) -> dict:
        all_issues = []
        for dim_name, result in dimension_results.items():
            if result.status != AgentStatus.DONE:
                all_issues.append(f"【{dim_name}维度问题】\n{result.content}")

        if not all_issues:
            return {"rewritten": None, "change_log": ""}

        issues_text = "\n\n".join(all_issues)
        original_text = "\n\n".join(paragraphs)
        result = suggest_rewrite_structured(original_text, issues_text)
        self._emit("rewrite", {"status": result.status.value})
        return {"rewritten": result.content, "change_log": ""}

    def _emit(self, event_type: str, data: dict):
        if self.progress_callback:
            self.progress_callback({"event": event_type, **data})

    def _assemble_report(self, text: str, paragraphs: list[str],
                         analyses: list[ParagraphAnalysis],
                         dimension_results: dict, rewrites: dict) -> dict:
        return {
            "paragraphs": [
                {
                    "index": a.index,
                    "text": a.text,
                    "structure": a.structure,
                }
                for a in analyses
            ],
            "dimensions": {
                name: {
                    "status": result.status.value,
                    "content": result.content,
                    "concerns": result.concerns,
                }
                for name, result in dimension_results.items()
            },
            "rewrite": rewrites,
        }
