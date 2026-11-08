"""Behaviour/stability metrics, not relevance-based scouting evaluation."""

from numbers import Integral

import numpy as np
import pandas as pd


def signature(response):
    return [(row["player_id"], row["similarity_score"]) for row in response["results"]]


def check_response(response, query, filters) -> dict:
    """Check every returned row; empty correctness is explicitly vacuous."""
    rows = response["results"]
    ids = [r["player_id"] for r in rows]
    checks = {
        "filter_correct": all(
            r["position"] == filters.position and
            filters.min_age <= r["age"] <= filters.max_age and
            r["minutes_played"] >= filters.min_minutes and
            (filters.max_budget_eur is None or r["market_value_in_eur"] <= filters.max_budget_eur)
            for r in rows),
        "score_valid": all(np.isfinite(r["similarity_score"]) and
                           -1 <= r["similarity_score"] <= 1 for r in rows),
        "unique_and_excludes_query": len(ids) == len(set(ids)) and query not in ids,
        "sorted_correctly": signature(response) == sorted(
            signature(response), key=lambda pair: (-pair[1], pair[0])),
        "explanations_sum_to_score": all(
            abs(sum(r["cosine_components"].values()) - r["similarity_score"]) < 1e-10
            for r in rows),
        "returned_all_rankable": len(rows) == (
            response["eligible_count"] - response["excluded_zero_vectors"])
            if response["status"] != "zero_reference_vector" else not rows,
    }
    if not all(checks.values()):
        raise ValueError(f"Recommendation contract failed: {checks}")
    return {**checks, "checked_rows": len(rows), "empty_checks_are_vacuous": not rows}


def stability_metrics(baseline, candidate, k=5) -> dict:
    """Overlap intersection/K; Spearman on full common rankable pool.

    Midranks of rounded scores account for score ties (ID tie-break is not
    mistaken for evidence of fine-grained similarity). Null for empty top-K,
    fewer than 2 common players, or constant ranks. K is never reduced silently.
    """
    if isinstance(k, bool) or not isinstance(k, Integral) or k <= 0:
        raise ValueError("k must be a positive integer")
    for response in (baseline, candidate):
        ids = [r["player_id"] for r in response["results"]]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate result IDs")
    left = {r["player_id"]: r["similarity_score"] for r in baseline["results"]}
    right = {r["player_id"]: r["similarity_score"] for r in candidate["results"]}
    if any(not np.isfinite(v) for d in (left, right) for v in d.values()):
        raise ValueError("Nonfinite score")
    a, b = list(left)[:k], list(right)[:k]
    intersection = len(set(a) & set(b))
    common = sorted(left.keys() & right.keys())
    rho, reason = None, None
    if len(common) < 2:
        reason = "fewer_than_two_common_candidates"
    else:
        x = pd.Series([left[i] for i in common]).rank(method="average")
        y = pd.Series([right[i] for i in common]).rank(method="average")
        if x.nunique() < 2 or y.nunique() < 2:
            reason = "constant_score_ranks"
        else:
            rho = float(np.clip(np.corrcoef(x, y)[0, 1], -1, 1))
    return {
        "k": int(k), "baseline_returned_at_k": len(a), "returned_at_k": len(b),
        "intersection_at_k": intersection,
        "overlap_at_k": intersection / k if a and b else None,
        "overlap_reason": None if a and b else "one_or_both_shortlists_empty",
        "common_rankable_candidates": len(common),
        "same_rankable_pool": left.keys() == right.keys(),
        "spearman_full_common": rho, "spearman_reason": reason,
    }

