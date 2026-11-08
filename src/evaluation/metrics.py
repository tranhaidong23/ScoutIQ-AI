"""Label-gated metrics over an explicitly declared eligible candidate universe.

Grades are external evidence, never inferred from rank or similarity. Provenance
is a declaration to audit, not proof that a human assessor is independent.
"""

import csv
from datetime import datetime
from math import log2


ANNOTATION_FIELDS = (
    "scenario_id", "player_id", "assessor_id", "timestamp", "relevance_grade",
    "evidence", "notes", "label_source",
)
LABEL_SOURCES = {"independent_human", "SYNTHETIC", "unlabeled"}


def load_annotations(path):
    """Read the version-1 CSV without coercing missing grades to zero.

    Returns typed records. Caller must validate scenario/pool and explicitly
    select assessor/provenance using assess_ranking; loading is not endorsement.
    """
    with open(path, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(ANNOTATION_FIELDS):
            raise ValueError("Annotation CSV must use the exact version-1 header")
        rows = []
        for row in reader:
            if set(row) != set(ANNOTATION_FIELDS) or any(v is None for v in row.values()):
                raise ValueError("Malformed CSV row")
            if not row["player_id"].isascii() or not row["player_id"].isdigit() or int(row["player_id"]) <= 0:
                raise ValueError("CSV player_id must be a positive integer")
            row["player_id"] = int(row["player_id"])
            grade = row["relevance_grade"]
            if grade not in ("", "0", "1", "2", "3"):
                raise ValueError("CSV grade must be blank or an integer 0..3")
            row["relevance_grade"] = None if grade == "" else int(grade)
            rows.append(row)
    return rows


def _ids(values, name):
    if not isinstance(values, (list, tuple)):
        raise ValueError(f"{name} must be an ordered list/tuple")
    if any(type(i) is not int or i <= 0 for i in values):
        raise ValueError(f"{name} requires positive integer IDs")
    if len(values) != len(set(values)):
        raise ValueError(f"Duplicate IDs in {name}")
    return list(values)


def _positive_int(value, name):
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def validate_annotations(rows, *, scenario_id, candidate_ids):
    """Validate typed records; CSV conversion is deliberately explicit upstream.

    Missing/abstained grades are None or empty, with label_source=unlabeled.
    Distinct assessors may judge the same pair; duplicate assessor records fail.
    """
    candidates = set(_ids(candidate_ids, "candidate_ids"))
    if not isinstance(scenario_id, str) or not scenario_id.strip():
        raise ValueError("scenario_id must be nonempty")
    if not isinstance(rows, (list, tuple)):
        raise ValueError("annotations must be a list/tuple")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(ANNOTATION_FIELDS) - row.keys():
            raise ValueError("Missing annotation fields")
        if row["scenario_id"] != scenario_id:
            raise ValueError("Annotation belongs to another scenario")
        _ids([row["player_id"]], "annotation player_id")
        if row["player_id"] not in candidates:
            raise ValueError("Annotation player is outside the declared candidate universe")
        if any(not isinstance(row[key], str) for key in
               ("assessor_id", "timestamp", "evidence", "notes", "label_source")):
            raise ValueError("Annotation text fields must be strings")
        source, grade = row["label_source"], row["relevance_grade"]
        if source not in LABEL_SOURCES:
            raise ValueError("Unknown label_source")
        key = (scenario_id, row["player_id"], row["assessor_id"])
        if key in seen:
            raise ValueError("Duplicate scenario/player/assessor annotation")
        seen.add(key)
        if source == "unlabeled":
            if grade is not None and grade != "":
                raise ValueError("Unlabeled rows cannot contain a grade")
            continue
        if type(grade) is not int or not 0 <= grade <= 3:
            raise ValueError("relevance_grade must be an integer from 0 to 3")
        if not row["assessor_id"].strip() or not row["evidence"].strip():
            raise ValueError("A grade requires assessor_id and evidence")
        try:
            timestamp = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("timestamp must be ISO 8601 with timezone") from exc
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("timestamp must have timezone")


def assess_ranking(ranked_ids, candidate_ids, annotations, *, scenario_id,
                   assessor_id, label_source="independent_human", k=5):
    """P@K uses grade>=2 and denominator K, including unfilled slots.

    P@K needs all returned top-K judged; empty retrieval needs a fully judged
    universe. Recall/NDCG need ALL eligible candidates judged. NDCG uses
    (2**grade-1)/log2(rank+1), ideal order across that same universe. Actual
    service tie order is preserved; we never sort using grades. No-label,
    empty-universe and zero relevant/ideal denominators return null + reason.
    """
    _positive_int(k, "k")
    ranked = _ids(ranked_ids, "ranked_ids")
    candidates = _ids(candidate_ids, "candidate_ids")
    if not set(ranked) <= set(candidates):
        raise ValueError("Ranking contains a player outside the eligible universe")
    if not isinstance(label_source, str) or label_source not in LABEL_SOURCES:
        raise ValueError("Unknown requested label_source")
    if not isinstance(assessor_id, str) or not assessor_id.strip():
        raise ValueError("Choose one explicit assessor; no implicit aggregation")
    validate_annotations(annotations, scenario_id=scenario_id, candidate_ids=candidates)
    labeled = [r for r in annotations if r["label_source"] != "unlabeled"]
    if any(r["label_source"] != label_source or r["assessor_id"] != assessor_id for r in labeled):
        raise ValueError("Select one assessor and one provenance source before evaluation")
    grades = {r["player_id"]: r["relevance_grade"] for r in labeled}
    top = ranked[:k]
    complete = bool(candidates) and set(grades) == set(candidates)
    values = {"precision_at_k": None, "recall_at_k": None, "ndcg_at_k": None}
    reasons = {key: "no_labels" for key in values}
    if not candidates:
        reasons = {key: "empty_candidate_universe" for key in values}
    elif grades:
        top_judged = set(top) <= grades.keys()
        hits = sum(grades.get(i, -1) >= 2 for i in top)
        if top_judged and (top or complete):
            values["precision_at_k"] = hits / k
            reasons["precision_at_k"] = None
        else:
            reasons["precision_at_k"] = "unjudged_top_k_or_empty_partial_ranking"
        if complete:
            relevant = sum(g >= 2 for g in grades.values())
            if relevant:
                values["recall_at_k"] = hits / relevant
                reasons["recall_at_k"] = None
            else:
                reasons["recall_at_k"] = "no_relevant_candidates"
            ideal = sorted(grades.values(), reverse=True)[:k]
            dcg = sum((2 ** grades[i] - 1) / log2(rank + 2) for rank, i in enumerate(top))
            idcg = sum((2 ** g - 1) / log2(rank + 2) for rank, g in enumerate(ideal))
            if idcg:
                values["ndcg_at_k"] = dcg / idcg
                reasons["ndcg_at_k"] = None
            else:
                reasons["ndcg_at_k"] = "zero_ideal_gain"
        else:
            reasons["recall_at_k"] = reasons["ndcg_at_k"] = "incomplete_candidate_labels"
    return {
        "scenario_id": scenario_id, "assessor_id": assessor_id,
        "label_source": label_source, "provenance_status": "declared_not_independently_verified",
        "k": k, "returned_at_k": len(top), "candidate_count": len(candidates),
        "judged_count": len(grades), "label_coverage": len(grades) / len(candidates) if candidates else None,
        "complete_candidate_labels": complete, "relevant_threshold": 2,
        "gain": "2**grade-1", "metrics": values, "unavailable_reasons": reasons,
        "interpretation": "SYNTHETIC_ONLY_NOT_SCOUTING_QUALITY" if label_source == "SYNTHETIC"
                          else "relevance_requires_independent_evidence_review",
    }


def ranking_stability(left_ids, right_ids, *, k=5):
    """Set intersection/K (fixed K) and order agreement; not scouting quality."""
    _positive_int(k, "k")
    left, right = _ids(left_ids, "left_ids")[:k], _ids(right_ids, "right_ids")[:k]
    available = bool(left and right)
    return {"k": k, "left_count": len(left), "right_count": len(right),
            "overlap_at_k": len(set(left) & set(right)) / k if available else None,
            "same_order": left == right if available else None,
            "reason": None if available else "one_or_both_shortlists_empty"}


def catalogue_coverage(shortlists, candidate_pools):
    """Union retrieved / union eligible, for paired queries in one experiment."""
    if not isinstance(shortlists, (list, tuple)) or not isinstance(candidate_pools, (list, tuple)):
        raise ValueError("Expected lists of shortlists and candidate pools")
    if len(shortlists) != len(candidate_pools):
        raise ValueError("Each shortlist needs its own candidate pool")
    retrieved, eligible = set(), set()
    nonempty = 0
    for shortlist, pool in zip(shortlists, candidate_pools):
        shortlist, pool = _ids(shortlist, "shortlist"), _ids(pool, "pool")
        if not set(shortlist) <= set(pool):
            raise ValueError("Retrieved player is not eligible for that query")
        retrieved.update(shortlist)
        eligible.update(pool)
        nonempty += bool(shortlist)
    return {"query_count": len(shortlists), "nonempty_query_count": nonempty,
            "retrieved_unique": len(retrieved), "eligible_union_count": len(eligible),
            "catalogue_coverage": len(retrieved) / len(eligible) if eligible else None,
            "request_coverage": nonempty / len(shortlists) if shortlists else None,
            "scope": "declared_query_pools_only_not_global_population_or_quality"}
