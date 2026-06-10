"""LLM-judge scoring against rubric criteria.

The judge receives the question, the rubric (must_include / must_avoid), and the
candidate answer, and returns a structured verdict. This is adapted from the
``RAGCorrectnessLLMJudge`` pattern in the original W&B course notebook, tightened
to score against explicit clinical rubric criteria instead of free-form context.
"""
from __future__ import annotations

import json

from providers import OpenRouterClient

JUDGE_SYSTEM = """You are a strict dental-domain examiner grading a candidate answer.
You are given a clinical QUESTION, a RUBRIC with must_include criteria and must_avoid errors, and the candidate ANSWER.

Grade ONLY against the rubric. Do not reward fluent writing that misses required content, and do not penalize correct content that the rubric did not ask for.

Return a JSON object with exactly these keys:
- "criteria_met": integer, how many must_include criteria the answer satisfies
- "criteria_total": integer, total number of must_include criteria
- "violations": array of strings, each a must_avoid error the answer commits (empty if none)
- "correct": boolean, true only if the answer satisfies ALL must_include criteria AND commits NO must_avoid violations
- "explanation": one or two sentences justifying the verdict

Respond with the JSON object only, no surrounding prose or code fences."""

JUDGE_TEMPLATE = """QUESTION:
{question}

RUBRIC must_include ({n_include} criteria):
{must_include}

RUBRIC must_avoid:
{must_avoid}

CANDIDATE ANSWER:
{answer}

Return the JSON verdict now."""


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items) if items else "- (none)"


def _extract_json(text: str) -> dict:
    """Best-effort parse of a JSON object from judge output."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1].lstrip("json").strip()
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1:
        text = text[start : end + 1]
    return json.loads(text)


def judge_answer(
    client: OpenRouterClient,
    judge_model_id: str,
    question: str,
    rubric: dict,
    answer: str,
) -> dict:
    """Score one answer against its rubric. Returns the verdict dict (+ judge_error on failure)."""
    must_include = rubric.get("must_include", [])
    prompt = JUDGE_TEMPLATE.format(
        question=question,
        n_include=len(must_include),
        must_include=_bullets(must_include),
        must_avoid=_bullets(rubric.get("must_avoid", [])),
        answer=answer,
    )
    full_prompt = f"{JUDGE_SYSTEM}\n\n{prompt}"
    result = client.complete(judge_model_id, full_prompt, temperature=0.0)
    if not result["ok"]:
        return {"correct": False, "judge_error": result["error"], "criteria_met": 0,
                "criteria_total": len(must_include), "violations": [], "explanation": "judge call failed"}
    try:
        verdict = _extract_json(result["text"])
        verdict["correct"] = bool(verdict.get("correct", False))
        verdict["judge_latency_s"] = result["latency_s"]
        return verdict
    except Exception as e:  # noqa: BLE001
        return {"correct": False, "judge_error": f"unparseable judge output: {e}",
                "criteria_met": 0, "criteria_total": len(must_include),
                "violations": [], "explanation": result["text"][:200]}


def consistency_score(answers: list[str]) -> float:
    """Crude lexical consistency across trials: mean pairwise Jaccard of word sets.

    1.0 = identical wording every trial, 0.0 = no shared vocabulary. A proxy for
    'does this model say the same thing when asked twice', not a semantic measure.
    """
    valid = [a for a in answers if a]
    if len(valid) < 2:
        return 1.0
    sets = [set(a.lower().split()) for a in valid]
    sims, pairs = 0.0, 0
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            union = sets[i] | sets[j]
            sims += len(sets[i] & sets[j]) / len(union) if union else 1.0
            pairs += 1
    return round(sims / pairs, 3) if pairs else 1.0
