from llm_rerank.judge_client import CandidateJudgment, JudgeClient, JudgeResult
from llm_rerank.live import apply_llm_rerank


def _result(label, content):
    return {
        "label": label,
        "_content": content,
        "reranked": False,
        "rerank_rank": 0,
    }


class _ScriptedJudge(JudgeClient):
    def judge_candidates(self, query_code, candidates):
        ids = [candidate["base_code_id"] for candidate in candidates]
        return JudgeResult(
            judgments=[
                CandidateJudgment(ids[-1], True, 0.95, "same logic"),
                CandidateJudgment(ids[0], False, 0.9, "different logic"),
            ]
        )


class _FailingJudge(JudgeClient):
    def judge_candidates(self, query_code, candidates):
        raise TimeoutError("provider timed out")


def test_partial_missing_content_never_drops_a_result():
    results = [
        _result("first", "def unrelated(): pass"),
        _result("missing-content", ""),
        _result("correct", "def answer(): return 42"),
        _result("rest", "def later(): pass"),
    ]

    reranked = apply_llm_rerank(
        "def query(): return 42",
        results,
        client_factory=_ScriptedJudge,
        top_n=3,
    )

    assert [result["label"] for result in reranked] == [
        "correct",
        "first",
        "missing-content",
        "rest",
    ]
    assert len(reranked) == len(results)
    assert reranked[2]["reranked"] is False


def test_unexpected_provider_failure_preserves_original_order():
    results = [
        _result("first", "def a(): pass"),
        _result("second", "def b(): pass"),
    ]

    reranked = apply_llm_rerank(
        "def query(): pass",
        results,
        client_factory=_FailingJudge,
    )

    assert [result["label"] for result in reranked] == ["first", "second"]
    assert [result["rerank_rank"] for result in reranked] == [1, 2]
    assert all(result["reranked"] is False for result in reranked)


def test_duplicate_labels_are_preserved_as_distinct_results():
    results = [
        _result("same-label", "def a(): pass"),
        _result("same-label", "def b(): return 42"),
    ]

    reranked = apply_llm_rerank(
        "def query(): return 42",
        results,
        client_factory=_ScriptedJudge,
    )

    assert len(reranked) == 2
    assert {id(result) for result in reranked} == {id(result) for result in results}
