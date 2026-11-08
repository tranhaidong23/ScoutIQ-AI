"""Read-only snapshot probes. Never import preprocessing scripts with side effects."""

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

from src.features.build_features import CUTOFF, validate_features


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def audit_snapshot(root):
    root = Path(root)
    raw, processed = root / "data/raw", root / "data/processed"
    features = pd.read_csv(processed / "scoutiq_features_2025_26.csv")
    validate_features(features)
    integrated = pd.read_csv(processed / "scoutiq_players_2025_26.csv")
    games = pd.read_csv(raw / "games.csv.gz", usecols=["game_id", "season", "date", "competition_id", "competition_type"])
    games["game_date"] = pd.to_datetime(games.date, errors="coerce")
    season = games[games.season.astype(str).eq("2025") & games.game_date.le(CUTOFF)].copy()
    apps = pd.read_csv(raw / "appearances.csv.gz", usecols=["appearance_id", "game_id", "player_id", "date", "minutes_played", "goals", "assists"])
    joined = apps.merge(season[["game_id", "game_date", "competition_id"]].drop_duplicates("game_id"), on="game_id", validate="many_to_one")
    joined["appearance_date"] = pd.to_datetime(joined.date, errors="coerce")
    selected = joined.dropna(subset=["player_id", "game_id"]).copy()
    for col in ("minutes_played", "goals", "assists"):
        selected[col] = pd.to_numeric(selected[col], errors="coerce")
    selected = selected.dropna(subset=["minutes_played", "goals", "assists"])
    selected = selected[selected.minutes_played.gt(0) & selected.goals.ge(0) & selected.assists.ge(0)]
    before_dedup = len(selected)
    selected = selected.drop_duplicates("appearance_id")
    aggregate = selected.groupby("player_id")[["minutes_played", "goals", "assists"]].sum()
    aggregate["matches_played"] = selected.groupby("player_id").game_id.nunique()
    actual = features.set_index("player_id")
    errors = {}
    for col in ("minutes_played", "goals", "assists", "matches_played"):
        expected = aggregate[col].reindex(actual.index)
        errors[col] = {"missing_source": int(expected.isna().sum()),
                       "mismatched_players": int((~np.isclose(expected, actual[col], rtol=0, atol=1e-9)).sum()),
                       "max_abs_error": float((expected - actual[col]).abs().max())}
    values = pd.read_csv(raw / "player_valuations.csv.gz", usecols=["player_id", "date", "market_value_in_eur"])
    values["valuation_date"] = pd.to_datetime(values.date, errors="coerce")
    values["market_value_in_eur"] = pd.to_numeric(values.market_value_in_eur, errors="coerce")
    historical = values[values.valuation_date.le(CUTOFF)].copy()
    positive = historical[historical.market_value_in_eur.gt(0)].sort_values(["player_id", "valuation_date"])
    latest = positive.drop_duplicates("player_id", keep="last").set_index("player_id").reindex(actual.index)
    latest_any = historical.sort_values(["player_id", "valuation_date"]).drop_duplicates("player_id", keep="last").set_index("player_id").reindex(actual.index)
    dates = pd.to_datetime(actual.valuation_date)
    ages = (CUTOFF - pd.to_datetime(integrated.valuation_date)).dt.days
    mask = (integrated.minutes_played.ge(900) & integrated.market_value_in_eur.gt(0) &
            ages.between(0, 365) & integrated.position.notna() & integrated.position.fillna("").str.strip().ne(""))
    positions = sorted(set(integrated.position.dropna()) | set(features.position))
    position_rows = [{"position": pos, "integrated": int(integrated.position.eq(pos).sum()),
                      "eligible": int(features.position.eq(pos).sum())} for pos in positions]
    for row in position_rows:
        row["retention_fraction"] = row["eligible"] / row["integrated"] if row["integrated"] else None
    players = pd.read_csv(raw / "players.csv.gz", usecols=["player_id", "date_of_birth", "current_club_domestic_competition_id"])
    metadata = players.drop_duplicates("player_id").set_index("player_id").reindex(actual.index)
    dob = pd.to_datetime(metadata.date_of_birth, errors="coerce")
    exact_age = CUTOFF.year - dob.dt.year - ((dob.dt.month.gt(CUTOFF.month)) | (dob.dt.month.eq(CUTOFF.month) & dob.dt.day.gt(CUTOFF.day))).astype(int)
    ids = set(actual.index)
    paths = sorted(raw.glob("*.csv.gz")) + sorted(processed.glob("*.csv"))
    hashes = {p.relative_to(root).as_posix(): digest(p) for p in paths}
    metadata_competitions = metadata.current_club_domestic_competition_id.fillna("MISSING").value_counts()
    return {
        "scope": "read_only_snapshot_audit_not_temporal_validation_or_source_truth",
        "cutoff": str(CUTOFF.date()), "dataset_sha256": hashes["data/processed/scoutiq_features_2025_26.csv"],
        "input_sha256": hashes, "shape": list(features.shape),
        "missing_values": {k: int(v) for k, v in features.isna().sum().items()},
        "duplicate_feature_ids": int(features.player_id.duplicated().sum()),
        "integrated_rows": len(integrated), "eligibility_reconstruction_count": int(mask.sum()),
        "eligibility_ids_exact": set(integrated.loc[mask, "player_id"]) == ids,
        "integrated_below_900_minutes": int(integrated.minutes_played.lt(900).sum()),
        "position_retention": position_rows,
        "games": {"raw_rows": len(games), "selected_rows": len(season),
                  "selected_max_date": str(season.game_date.max().date()),
                  "invalid_raw_dates": int(games.game_date.isna().sum()),
                  "competition_types": {str(k): int(v) for k, v in season.competition_type.fillna("MISSING").value_counts().items()}},
        "appearances": {"raw_rows": len(apps), "joined_rows": len(joined),
                        "retained_rows": len(selected), "duplicate_appearance_ids_removed": before_dedup - len(selected),
                        "retained_duplicate_player_game_pairs": int(selected.duplicated(["player_id", "game_id"]).sum()),
                        "joined_invalid_dates": int(joined.appearance_date.isna().sum()),
                        "joined_after_cutoff": int(joined.appearance_date.gt(CUTOFF).sum()),
                        "joined_game_date_disagreements": int((joined.appearance_date.notna() & joined.appearance_date.ne(joined.game_date)).sum()),
                        "feature_aggregate_check": errors},
        "valuations": {"raw_rows": len(values), "invalid_raw_dates": int(values.valuation_date.isna().sum()),
                       "feature_dates_after_cutoff": int(dates.gt(CUTOFF).sum()),
                       "feature_dates_older_than_365_days": int((CUTOFF - dates).dt.days.gt(365).sum()),
                       "missing_positive_source": int(latest.market_value_in_eur.isna().sum()),
                       "value_mismatches": int(latest.market_value_in_eur.ne(actual.market_value_in_eur).sum()),
                       "date_mismatches": int(latest.valuation_date.ne(dates).sum()),
                       "latest_any_nonpositive_for_candidates": int(latest_any.market_value_in_eur.le(0).sum()),
                       "same_date_conflicting_positive_value_groups": int((positive.groupby(["player_id", "valuation_date"]).market_value_in_eur.nunique() > 1).sum())},
        "age_calendar_check": {"missing_dob": int(dob.isna().sum()),
                               "different_from_calendar_age": int((dob.notna() & exact_age.ne(actual.age)).sum())},
        "current_club_competition_proxy": {str(k): int(v) for k, v in metadata_competitions.items()},
        "competition_proxy_warning": "Current club metadata, not verified league at cutoff; games include cups. No league-strength correction.",
        "unverified": ["historical validity of club/role/foot metadata", "source event completeness and correctness",
                       "independent relevance judgments", "temporal holdout quality", "fresh-machine reproduction"],
    }
