"""Failure-safe glue between live search results and the reusable reranker."""

from __future__ import annotations

from collections.abc import Callable

from llm_rerank.judge_client import ClaudeJudgeClient, JudgeClient
from llm_rerank.rerank import rerank_one


LLM_RERANK_TOP_N = 5


def _keep_original_order(list_results: list[dict]) -> list[dict]:
    for rank, result in enumerate(list_results, start=1):
        result["reranked"] = False
        result["rerank_rank"] = rank
    return list_results


def apply_llm_rerank(
    user_code: str,
    list_results: list[dict],
    *,
    client_factory: Callable[[], JudgeClient] = ClaudeJudgeClient,
    top_n: int = LLM_RERANK_TOP_N,
) -> list[dict]:
    """Rerank the top results while preserving every original result.

    External-provider failures degrade to the embedding order. Candidates
    without source content are not sent to Claude, but remain in the result
    set in their original relative order. Stable internal ids avoid losing
    entries when two search results happen to share the same label.
    """
    judged_window = list_results[:top_n]
    untouched_rest = list_results[top_n:]

    candidates = []
    result_by_candidate_id = {}
    for original_index, result in enumerate(judged_window):
        content = result.get("_content")
        if not content:
            continue
        candidate_id = f"candidate_{original_index}"
        candidates.append({"base_code_id": candidate_id, "code": content})
        result_by_candidate_id[candidate_id] = result

    if not candidates:
        return _keep_original_order(list_results)

    try:
        outcome = rerank_one(
            client_factory(),
            "live_query",
            "",
            user_code,
            candidates,
        )
    except Exception as error:
        print(
            "LLM rerank failed, keeping original embedding order: "
            f"{type(error).__name__}: {error}"
        )
        return _keep_original_order(list_results)

    if outcome.judge_error:
        print(
            "LLM rerank failed, keeping original embedding order: "
            f"{outcome.judge_error}"
        )
        return _keep_original_order(list_results)

    reranked_window = [
        result_by_candidate_id[candidate_id]
        for candidate_id in outcome.reranked_order
        if candidate_id in result_by_candidate_id
    ]
    reranked_object_ids = {id(result) for result in reranked_window}

    # Preserve top-N results that were not judged (for example, missing
    # source content) in their original relative order.
    reranked_window.extend(
        result
        for result in judged_window
        if id(result) not in reranked_object_ids
    )

    final_results = reranked_window + untouched_rest
    if len(final_results) != len(list_results):
        return _keep_original_order(list_results)

    judged_object_ids = {id(result) for result in result_by_candidate_id.values()}
    for rank, result in enumerate(final_results, start=1):
        result["reranked"] = id(result) in judged_object_ids
        result["rerank_rank"] = rank

    return final_results
