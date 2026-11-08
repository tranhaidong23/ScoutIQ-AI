"""Reproducible unlabeled pilot, strict annotation contract and readiness gates.

No model scores are inputs to sampling. Registry declarations require external
review: code cannot establish that two IDs represent independent humans.
"""

import csv
from datetime import datetime
import hashlib
from itertools import combinations
import re

from src.evaluation.integrity import age_band
from src.evaluation.metrics import ANNOTATION_FIELDS, _ids, _positive_int, validate_annotations


PILOT_VERSION = "scoutiq.annotation-pilot.v1"
RUBRIC_VERSION = "scoutiq.relevance.v1"
PILOT_FIELDS = ANNOTATION_FIELDS + (
    "pilot_version", "dataset_sha256", "rubric_version", "assessment_scope",
    "decision_status", "uncertainty", "missing_evidence",
)
ASSESSOR_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_-]{2,63}\Z")


def build_pilot(scenarios, catalogue, dataset_sha256, *, seed=12, per_scenario=8):
    """Age-stratified round robin, hash order within strata, stable under reorder."""
    _positive_int(per_scenario, "per_scenario")
    if type(seed) is not int or seed < 0:
        raise ValueError("seed must be a nonnegative integer")
    if not isinstance(dataset_sha256, str) or not re.fullmatch(r"[a-f0-9]{64}", dataset_sha256):
        raise ValueError("Expected SHA-256")
    _ids(catalogue.player_id.tolist(), "catalogue IDs")
    indexed = catalogue.set_index("player_id")
    cases, seen = [], set()
    for scenario in sorted(scenarios, key=lambda s: s["scenario_id"]):
        name = scenario["scenario_id"]
        if not isinstance(name, str) or not name.strip() or name in seen:
            raise ValueError("Scenario IDs must be unique nonempty strings")
        seen.add(name)
        ids = _ids(scenario["candidate_ids"], "candidate IDs")
        if not set(ids) <= set(indexed.index):
            raise ValueError("Candidate IDs absent from catalogue")
        positions = set(indexed.loc[ids, "position"])
        if ids and (len(positions) != 1 or not positions <= {"Attack", "Midfield", "Defender", "Goalkeeper"}):
            raise ValueError("A pilot scenario must have one supported position")
        position = next(iter(positions)) if positions else None
        scope = "context_profile_only" if position in ("Defender", "Goalkeeper") else "attack_output_and_role"
        def key(pid):
            return hashlib.sha256(f"{PILOT_VERSION}|{seed}|{name}|{pid}".encode()).hexdigest(), pid
        strata = {}
        for pid in ids:
            strata.setdefault(age_band(indexed.at[pid, "age"]), []).append(pid)
        for values in strata.values():
            values.sort(key=key)
        selected = []
        depth = 0
        while len(selected) < min(per_scenario, len(ids)):
            for band in sorted(strata):
                if depth < len(strata[band]) and len(selected) < per_scenario:
                    selected.append(strata[band][depth])
            depth += 1
        selected.sort(key=key)  # display order independent of model scores
        cases.append({"scenario_id": name, "position": position, "assessment_scope": scope,
                      "candidate_ids": sorted(ids), "selected_ids": selected,
                      "pool_size": len(ids), "selected_count": len(selected),
                      "strata": {band: {"pool": len(v), "selected": sum(i in selected for i in v)}
                                 for band, v in sorted(strata.items())}})
    return {"pilot_version": PILOT_VERSION, "rubric_version": RUBRIC_VERSION,
            "dataset_sha256": dataset_sha256, "seed": seed, "per_scenario": per_scenario,
            "selection": "age strata round-robin; SHA256(seed,scenario,ID); no ranks/scores",
            "scope": "process_calibration_pilot_not_representative_quality_test", "scenarios": cases}


def annotation_template(manifest):
    rows = []
    for case in manifest["scenarios"]:
        for pid in case["selected_ids"]:
            rows.append({"scenario_id": case["scenario_id"], "player_id": pid, "assessor_id": "",
                         "timestamp": "", "relevance_grade": None, "evidence": "", "notes": "",
                         "label_source": "unlabeled", "pilot_version": manifest["pilot_version"],
                         "dataset_sha256": manifest["dataset_sha256"], "rubric_version": manifest["rubric_version"],
                         "assessment_scope": case["assessment_scope"], "decision_status": "pending",
                         "uncertainty": "", "missing_evidence": ""})
    return rows


def load_pilot_annotations(path):
    """Parse exact v1 pilot CSV; missing labels remain None, never zero."""
    with open(path, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(PILOT_FIELDS):
            raise ValueError("Incorrect pilot CSV header")
        rows = []
        for row in reader:
            if set(row) != set(PILOT_FIELDS) or any(v is None for v in row.values()):
                raise ValueError("Malformed pilot CSV row")
            if not re.fullmatch(r"[0-9]+", row["player_id"]) or int(row["player_id"]) <= 0:
                raise ValueError("Invalid CSV player ID")
            row["player_id"] = int(row["player_id"])
            if row["relevance_grade"] not in ("", "0", "1", "2", "3"):
                raise ValueError("Grade must be blank or 0..3")
            row["relevance_grade"] = None if row["relevance_grade"] == "" else int(row["relevance_grade"])
            rows.append(row)
    return rows


def validate_registry(registry):
    if not isinstance(registry, dict):
        raise ValueError("Assessor registry must be an object")
    normalized = set()
    for identifier, record in registry.items():
        if not isinstance(identifier, str) or not ASSESSOR_PATTERN.fullmatch(identifier) or identifier.casefold() in normalized:
            raise ValueError("Invalid or case-aliased assessor ID")
        normalized.add(identifier.casefold())
        if not isinstance(record, dict) or set(record) != {"label_source", "independence_confirmed", "review_evidence"}:
            raise ValueError("Invalid registry record")
        if record["label_source"] not in ("independent_human", "SYNTHETIC") or type(record["independence_confirmed"]) is not bool:
            raise ValueError("Invalid provenance declaration")
        if not isinstance(record["review_evidence"], str) or (record["independence_confirmed"] and not record["review_evidence"].strip()):
            raise ValueError("Independence confirmation requires review evidence")


def _timestamp(text):
    try:
        value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Invalid annotation timestamp") from exc
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Annotation timestamp needs timezone")


def validate_pilot_annotations(rows, manifest, registry):
    validate_registry(registry)
    if not isinstance(rows, (list, tuple)):
        raise ValueError("Annotations must be a list/tuple")
    cases = {s["scenario_id"]: s for s in manifest["scenarios"]}
    seen = set()
    for r in rows:
        if not isinstance(r, dict) or set(r) != set(PILOT_FIELDS):
            raise ValueError("Pilot annotation fields must match schema exactly")
        if any(not isinstance(r[f], str) for f in PILOT_FIELDS if f not in ("player_id", "relevance_grade")):
            raise ValueError("Expected annotation text fields")
        case = cases.get(r["scenario_id"])
        if case is None:
            raise ValueError("Unknown scenario")
        validate_annotations([r], scenario_id=r["scenario_id"], candidate_ids=case["selected_ids"])
        key = r["scenario_id"], r["player_id"], r["assessor_id"]
        if key in seen:
            raise ValueError("Duplicate scenario/player/assessor row")
        seen.add(key)
        for field in ("pilot_version", "dataset_sha256", "rubric_version"):
            if r[field] != manifest[field]:
                raise ValueError(f"Mismatched {field}; cannot mix annotation versions")
        if r["assessment_scope"] != case["assessment_scope"]:
            raise ValueError("Mismatched assessment scope")
        status, assessor = r["decision_status"], r["assessor_id"]
        if status not in ("pending", "abstain", "graded"):
            raise ValueError("Invalid decision_status")
        if assessor and assessor not in registry:
            raise ValueError("Unknown assessor; require reviewed registry identity")
        if status == "pending":
            if r["label_source"] != "unlabeled" or r["relevance_grade"] not in (None, "") or r["timestamp"] or r["uncertainty"]:
                raise ValueError("Pending rows must not claim grades, timestamps or uncertainty")
        else:
            if not assessor or r["uncertainty"] not in ("low", "medium", "high"):
                raise ValueError("Completed decisions require registered assessor and uncertainty")
            _timestamp(r["timestamp"])
            if status == "abstain":
                if r["label_source"] != "unlabeled" or r["relevance_grade"] not in (None, "") or not (r["notes"].strip() or r["missing_evidence"].strip()):
                    raise ValueError("Abstain requires blank grade and a reason")
            elif r["label_source"] == "unlabeled" or r["label_source"] != registry[assessor]["label_source"]:
                raise ValueError("Graded provenance must match the assessor registry")
    return {"rows": len(rows), "graded": sum(r["decision_status"] == "graded" for r in rows),
            "abstain": sum(r["decision_status"] == "abstain" for r in rows),
            "pending": sum(r["decision_status"] == "pending" for r in rows)}


def agreement_report(rows, manifest, registry, *, scenario_id, label_source="independent_human"):
    """Pairwise exact agreement and linear-weighted Cohen kappa, per scenario.

    Only common graded items; report coverage/abstentions rather than filling
    missing grades. At least two common items are required even for a pilot.
    """
    validate_pilot_annotations(rows, manifest, registry)
    if label_source not in ("independent_human", "SYNTHETIC"):
        raise ValueError("Invalid agreement provenance")
    case = next((s for s in manifest["scenarios"] if s["scenario_id"] == scenario_id), None)
    if case is None:
        raise ValueError("Unknown scenario")
    people = sorted(a for a, r in registry.items() if r["label_source"] == label_source and r["independence_confirmed"])
    grades = {a: {r["player_id"]: r["relevance_grade"] for r in rows
                  if r["scenario_id"] == scenario_id and r["assessor_id"] == a and r["decision_status"] == "graded"}
              for a in people}
    people = [a for a in people if grades[a]]
    pairs = []
    for left, right in combinations(people, 2):
        common = sorted(grades[left].keys() & grades[right].keys())
        result = {"assessors": [left, right], "paired_items": len(common),
                  "paired_fraction_of_pilot": len(common) / len(case["selected_ids"]) if case["selected_ids"] else None,
                  "exact_agreement": None, "linear_weighted_kappa": None,
                  "reason": "fewer_than_two_common_graded_items", "disagreements": []}
        if len(common) >= 2:
            x, y = [grades[left][i] for i in common], [grades[right][i] for i in common]
            n = len(common)
            observed = sum(abs(a - b) / 3 for a, b in zip(x, y)) / n
            expected = sum((abs(a - b) / 3) * (x.count(a) / n) * (y.count(b) / n) for a in range(4) for b in range(4))
            result.update(exact_agreement=sum(a == b for a, b in zip(x, y)) / n,
                          linear_weighted_kappa=1 - observed / expected if expected else None,
                          reason=None if expected else "zero_expected_disagreement_constant_labels",
                          disagreements=[{"player_id": i, "left_grade": grades[left][i], "right_grade": grades[right][i]}
                                         for i in common if grades[left][i] != grades[right][i]])
        pairs.append(result)
    return {"scenario_id": scenario_id, "assessment_scope": case["assessment_scope"],
            "label_source": label_source, "status": "PAIRS_AVAILABLE" if any(p["paired_items"] >= 2 for p in pairs) else "BLOCKED",
            "reason": None if any(p["paired_items"] >= 2 for p in pairs) else "need_two_independent_compatible_label_sets",
            "pairs": pairs, "interpretation": "SYNTHETIC_ONLY" if label_source == "SYNTHETIC" else "agreement_not_relevance_quality; independence_declared_requires_external_audit"}


def readiness_report(scenarios, rows, manifest, registry, *, k=5):
    """Readiness of declared frozen rankings/universes; no real labels invented."""
    _positive_int(k, "k")
    if k > 5:
        raise ValueError("Frozen Day 11 records contain only Top 5; k must be <=5")
    counts = validate_pilot_annotations(rows, manifest, registry)
    cases = []
    manifest_cases = {s["scenario_id"]: s for s in manifest["scenarios"]}
    if len({s["scenario_id"] for s in scenarios}) != len(scenarios) or set(manifest_cases) != {s["scenario_id"] for s in scenarios}:
        raise ValueError("Readiness scenarios must match the frozen pilot manifest")
    for scenario in scenarios:
        name = scenario["scenario_id"]
        universe = set(_ids(scenario["candidate_ids"], "candidate IDs"))
        selected = manifest_cases[name]
        if universe != set(selected["candidate_ids"]):
            raise ValueError("Readiness universe must match pilot source universe")
        for record in scenario["methods"].values():
            ranked = _ids(record["top5_ids"], "ranked IDs")
            if len(ranked) > 5 or not set(ranked) <= universe:
                raise ValueError("Invalid frozen Top 5 ranking")
        assessments = []
        for assessor, registration in sorted(registry.items()):
            if registration["label_source"] != "independent_human" or not registration["independence_confirmed"]:
                continue
            grades = {r["player_id"]: r["relevance_grade"] for r in rows if r["scenario_id"] == name and r["assessor_id"] == assessor and r["decision_status"] == "graded"}
            for method, record in scenario["methods"].items():
                top = _ids(record["top5_ids"], "ranked IDs")[:k]
                if not set(top) <= universe:
                    raise ValueError("Ranking contains ineligible candidates")
                full = bool(universe) and grades.keys() == universe
                assessments.append({"assessor_id": assessor, "method": method, "judged": len(grades),
                                    "label_coverage": len(grades) / len(universe) if universe else None,
                                    "precision_at_k_ready": bool(grades) and set(top) <= grades.keys() and (bool(top) or full),
                                    "recall_at_k_ready": full and any(g >= 2 for g in grades.values()),
                                    "ndcg_at_k_ready": full and any(g > 0 for g in grades.values()),
                                    "full_candidate_labels": full})
        cases.append({"scenario_id": name, "candidate_count": len(universe), "pilot_count": selected["selected_count"],
                      "status": "ASSESSOR_SPECIFIC_GATES" if assessments else "BLOCKED_NO_REVIEWED_HUMAN_LABELS",
                      "assessments": assessments,
                      "agreement": agreement_report(rows, manifest, registry, scenario_id=name)})
    return {"schema_version": "scoutiq.evaluation-readiness.v1", "annotation_counts": counts, "k": k,
            "cases": cases, "coverage_status": "COMPUTABLE_WITH_FROZEN_QUERY_POOLS; not quality",
            "temporal_evaluation_status": "BLOCKED_NO_ASOF_METADATA_OR_VALID_TEMPORAL_SPLIT",
            "actual_relevance_metrics": None, "actual_agreement_summary": None,
            "synthetic_metrics_are_real_quality": False}
