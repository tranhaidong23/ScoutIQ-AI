"""Day 12 read-only date, age, exclusion and coverage audits.

Calendar ages are audit values only. No function replaces an engine input.
"""

from datetime import date
from math import isfinite
from numbers import Real
import re

import pandas as pd

from src.evaluation.metrics import _ids


DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}(?:[ T]00:00:00(?:\.0{1,6})?)?\Z")


def cutoff_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("cutoff must be an explicit YYYY-MM-DD calendar date")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Invalid cutoff calendar date") from exc


def parse_dob(value):
    """Allow ISO dates or midnight timestamps only; never guess day/month order."""
    if value is None or (not isinstance(value, str) and pd.isna(value)):
        return None, "missing_dob"
    if isinstance(value, str) and not value.strip():
        return None, "missing_dob"
    if not isinstance(value, str) or not DATE_PATTERN.fullmatch(value.strip()):
        return None, "invalid_dob_format"
    try:
        return date.fromisoformat(value.strip()[:10]), "valid"
    except ValueError:
        return None, "invalid_dob_calendar"


def age_values(dob_value, cutoff="2026-06-12"):
    """March-1 anniversary for Feb-29 births in non-leap years, by tuple order.

    This is an explicit data policy, not a claim about legal age conventions.
    """
    end = cutoff_date(cutoff)
    dob, status = parse_dob(dob_value)
    result = {"parsed_dob": dob.isoformat() if dob else None, "dob_status": status,
              "calendar_age": None, "legacy_approx_age": None, "days_lived": None,
              "birthday_on_cutoff": None, "leap_day_born": None}
    if dob is None:
        return result
    if dob > end:
        result["dob_status"] = "future_dob"
        return result
    days = (end - dob).days
    age = end.year - dob.year - ((end.month, end.day) < (dob.month, dob.day))
    result.update(calendar_age=age, legacy_approx_age=int(days / 365.2425), days_lived=days,
                  birthday_on_cutoff=(dob.month, dob.day) == (end.month, end.day),
                  leap_day_born=(dob.month, dob.day) == (2, 29))
    if age > 100:
        result["dob_status"] = "age_outside_0_100_policy"
    return result


def age_audit(candidates, raw_players, *, cutoff="2026-06-12"):
    """One row per candidate; preserve raw row evidence and classify problems."""
    cutoff_date(cutoff)
    if not {"player_id", "age"} <= set(candidates) or not {"player_id", "date_of_birth"} <= set(raw_players):
        raise ValueError("Missing age-audit columns")
    _ids(candidates.player_id.tolist(), "candidate IDs")
    if candidates.empty:
        raise ValueError("Age audit requires a nonempty candidate catalogue")
    source = raw_players.copy()
    source["source_csv_row"] = range(2, len(source) + 2)
    groups = {pid: group for pid, group in source.groupby("player_id", sort=False)}
    rows = []
    for r in candidates.sort_values("player_id").to_dict(orient="records"):
        pid = int(r["player_id"])
        group = groups.get(pid)
        raw = None if group is None else group.iloc[0].date_of_birth
        facts = age_values(raw, cutoff)
        # Conservative: differing literal DOB records need review even if they
        # normalize to the same date. No first-row conflict is hidden.
        unique = 0 if group is None else group.date_of_birth.fillna("").astype(str).nunique()
        saved = r["age"]
        valid_age = isinstance(saved, Real) and not isinstance(saved, bool) and isfinite(saved) and saved == int(saved) and 0 <= saved <= 100
        snapshot = int(saved) if valid_age else None
        reason = facts["dob_status"]
        if group is None:
            reason = "missing_raw_player"
        elif unique > 1:
            reason = "conflicting_source_dob"
        elif not valid_age:
            reason = "invalid_snapshot_age"
        elif reason == "valid":
            if snapshot == facts["calendar_age"] == facts["legacy_approx_age"]:
                reason = "consistent"
            elif snapshot == facts["legacy_approx_age"]:
                reason = "approximate_year_length"
            elif snapshot == facts["calendar_age"]:
                reason = "snapshot_differs_from_legacy_formula"
            else:
                reason = "unexplained_snapshot_age_mismatch"
        rows.append({"player_id": pid, "name": r.get("name", ""), "position": r.get("position", ""),
                     "snapshot_age": snapshot, "raw_dob": "" if raw is None or pd.isna(raw) else str(raw),
                     "source_csv_row": None if group is None else int(group.iloc[0].source_csv_row),
                     "source_rows": 0 if group is None else len(group), "distinct_raw_dob_values": int(unique),
                     "cutoff": cutoff, **facts,
                     "calendar_minus_snapshot": facts["calendar_age"] - snapshot if snapshot is not None and facts["calendar_age"] is not None else None,
                     "finding": reason, "correction_status": "PROPOSED" if reason == "approximate_year_length" else "NOT_PROPOSED",
                     "source_truth_status": "local_snapshot_not_externally_verified"})
    return pd.DataFrame(rows)


def correction_proposal(audit, input_hashes):
    """Return a change specification only. There is deliberately no apply API."""
    eligible = audit[audit.finding.eq("approximate_year_length")]
    return {"proposal_version": "scoutiq.age-calendar.v2.proposed", "status": "PROPOSED",
            "applied": False, "approval": None, "input_sha256": dict(input_hashes),
            "policy": "completed_calendar_years; Feb29 anniversary March1 in non-leap years",
            "changes": [{"player_id": int(r.player_id), "field": "age", "old_value": int(r.snapshot_age),
                         "proposed_value": int(r.calendar_age), "dob": r.parsed_dob, "cutoff": r.cutoff,
                         "reason": r.finding} for r in eligible.itertuples(index=False)],
            "future_destination_pattern": "data/processed/versions/<approved-version>/ (not created)",
            "gates": ["explicit authorization and DOB evidence review", "unchanged input hashes",
                      "new output paths and manifest, preserve old snapshot", "ID/schema/per90 and dependent feature checks",
                      "quantify age-filter, scaler and ranking differences under separate version",
                      "explicit service configuration promotion; never overwrite baseline"],
            "current_ranking_impact": "not_applied_or_measured_with_corrected_data"}


def age_band(value):
    if not isinstance(value, Real) or not isfinite(value) or value < 0 or value > 100:
        return "MISSING_OR_INVALID"
    for upper, label in [(16, "0-16"), (20, "17-20"), (24, "21-24"), (28, "25-28"), (32, "29-32"), (36, "33-36")]:
        if value <= upper:
            return label
    return "37+"


def exclusion_audit(integrated, candidate_ids, *, cutoff="2026-06-12"):
    """Original Day 2 predicates, independently counted and in fixed stage order."""
    cutoff_date(cutoff)
    if integrated.player_id.duplicated().any():
        raise ValueError("Duplicate integrated IDs")
    days = (pd.Timestamp(cutoff) - pd.to_datetime(integrated.valuation_date, errors="coerce")).dt.days
    conditions = {
        "minutes_ge_900": integrated.minutes_played.ge(900),
        "market_value_positive": integrated.market_value_in_eur.gt(0),
        "valuation_age_0_365": days.between(0, 365),
        "position_nonempty": integrated.position.notna() & integrated.position.astype(str).str.strip().ne(""),
    }
    rows = integrated[["player_id"]].copy()
    keep = pd.Series(True, index=integrated.index)
    stages = []
    for name, condition in conditions.items():
        condition = condition.fillna(False)
        rows[name] = condition
        before = int(keep.sum())
        keep &= condition
        stages.append({"rule": name, "independent_failed": int((~condition).sum()),
                       "before": before, "after": int(keep.sum()), "removed_at_stage": before - int(keep.sum())})
    rows["eligible"] = keep
    rows["failed_rules"] = rows[list(conditions)].apply(lambda r: "|".join(k for k in conditions if not r[k]), axis=1)
    if set(integrated.loc[keep, "player_id"]) != set(candidate_ids):
        raise ValueError("Candidate universe differs from original eligibility predicates")
    return rows, stages


def coverage_analysis(integrated, candidates, raw_players):
    """Counts before/after eligibility, using unchanged snapshot age and club proxy."""
    raw = raw_players.drop_duplicates("player_id").set_index("player_id")
    frames = []
    for data in (integrated, candidates):
        f = data.copy()
        f["age_band_snapshot"] = f.age.map(age_band)
        f["current_club_league_proxy"] = f.player_id.map(raw.current_club_domestic_competition_id).replace("", pd.NA).fillna("MISSING")
        frames.append(f)
    rows = []
    for dimension in ("position", "age_band_snapshot", "current_club_league_proxy"):
        pre, post = [frame[dimension].fillna("MISSING").value_counts() for frame in frames]
        for category in sorted(set(pre.index) | set(post.index)):
            a, b = int(pre.get(category, 0)), int(post.get(category, 0))
            rows.append({"dimension": dimension, "category": category, "integrated_count": a,
                         "candidate_count": b, "excluded_count": a - b, "retention": b / a if a else None,
                         "integrated_share": a / len(integrated) if len(integrated) else None,
                         "candidate_share": b / len(candidates) if len(candidates) else None,
                         "basis": "original_snapshot_age; current_club_proxy_not_verified_historical_league"})
    return pd.DataFrame(rows)


def feature_lineage(columns):
    """One declared lineage entry for every current output column; fail on drift."""
    definitions = {}
    def put(names, source, transform, unit, role, availability):
        for name in names.split():
            definitions[name] = {"feature": name, "source": source, "transformation": transform,
                                 "unit": unit, "engine_role": role, "cutoff_availability": availability}
    put("player_id", "appearances.player_id + players.player_id", "group/join ID", "ID", "identity", "stable ID; ingestion time unknown")
    put("matches_played", "appearances.game_id + games.season/date", "nunique game_id after event cutoff", "matches", "display", "event-date bounded; publication time unknown")
    put("minutes_played", "appearances.minutes_played + games", "sum valid appearances", "minutes", "eligibility/filter; Defender/GK context vector", "event-date bounded; publication time unknown")
    put("goals assists", "appearances + games", "sum valid appearances", "count", "display/derivation only", "event-date bounded; publication time unknown")
    put("goals_per90 assists_per90", "goals/assists, minutes_played", "count * 90 / minutes", "per90", "Attack/Midfield vector/filter", "inherits event and publication limitations")
    put("goal_contributions_per90", "goals, assists, minutes_played", "(goals+assists)*90/minutes", "per90", "not in engine vector", "inherits event limitations; redundant signal excluded")
    put("name position sub_position foot image_url", "players current snapshot", "first row per player_id", "metadata", "identity/filter; role/foot categorical vectors by position", "NO as-of version; historical availability unverified")
    put("height_in_cm", "players.height_in_cm", "first row, no imputation", "cm", "not in vector", "NO as-of version; known 19cm outlier not repaired")
    put("age", "players.date_of_birth + cutoff", "int(days/365.2425), calendar correction PROPOSED only", "years", "filter; Defender/GK context vector", "DOB publication unknown; one boundary arithmetic mismatch")
    put("current_club_id current_club_name", "players.current_club_*", "first row per player_id", "metadata", "club exclusion/display only", "current metadata; historical validity unverified")
    put("club_name_verified", "clubs.name joined current_club_id", "many-to-one lookup", "name", "display only", "verified lookup is NOT verification at cutoff")
    put("valuation_date", "player_valuations.date", "latest positive value date <= cutoff", "date", "eligibility/evidence", "date bounded; recording/publication time unknown")
    put("market_value_in_eur", "player_valuations.market_value_in_eur", "latest positive valuation <= cutoff", "EUR", "budget/display; never skill", "date bounded estimate; NOT transfer fee")
    put("valuation_age_days", "cutoff - valuation_date", "calendar day difference 0..365", "days", "eligibility/evidence", "inherits valuation limitations")
    put("goal_contributions", "goals+assists", "sum", "count", "not in vector", "redundant with per90; excluded from vector")
    put("market_value_m", "market_value_in_eur", "EUR/1000000", "million EUR", "display; not skill", "inherits valuation limitations")
    put("log1p_market_value_m", "market_value_m", "natural log(1+x)", "dimensionless", "not in vector", "inherits valuation limitations")
    put("minutes_reliability", "minutes_played", "min(minutes/2700,1)", "heuristic 0..1", "not in vector", "not statistical confidence or independent performance")
    put("goals_per90_position_percentile assists_per90_position_percentile goal_contributions_per90_position_percentile",
        "per90 across full eligible catalogue by position", "100 * average_rank / group_size", "percentile 0..100",
        "not in vector", "full-catalogue reference; must recompute train-only if ever used for temporal evaluation")
    for name, role in {"name": "display/identity only", "image_url": "display only",
                       "position": "hard filter and representation group", "sub_position": "hard filter; Attack/Midfield/Defender categorical vector",
                       "foot": "hard/soft preference; Defender/GK categorical vector"}.items():
        definitions[name]["engine_role"] = role
    if set(columns) != set(definitions):
        raise ValueError("Feature schema drift requires a reviewed lineage definition")
    return pd.DataFrame([definitions[c] for c in columns])
