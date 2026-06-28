"""DIVE-PL Stage 4 — build the aggregated, de-identified dashboard summary.

Reads a REDCap export (CSV), derives scores via ``scoring.py``, and writes a JSON
summary that contains **only aggregates** — counts, means, distributions — with
small-cell suppression (k-anonymity) so no rare combination can re-identify anyone.

RODO/GDPR: the public dashboard must show aggregates only. This script is the gate:
- never copies raw rows into the output,
- suppresses any cell with fewer than K respondents (default 5),
- refuses to run if the export still contains obvious identifier columns.

Usage:
    python aggregate.py --input export.csv --output summary.json [--k 5]

The input export lives OUTSIDE git (see repo .gitignore); only summary.json may be
published.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from collections import Counter
from pathlib import Path
from typing import Any

import scoring

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

DEFAULT_K = 5

# Columns that must NOT be present in a de-identified export. Refuse if seen.
FORBIDDEN_COLUMNS = {
    "ip", "ip_address", "email", "e_mail", "redcap_survey_identifier",
    "name", "imie", "nazwisko", "phone", "telefon", "pesel", "address", "adres",
}

# Continuous derived measures to summarise (mean/median/min/max + n).
CONTINUOUS = ["bmi_calc", "vo2max_estimated", "ipaq_total_met", "dasi_mets",
              "vsaq_mets", "knowledge_pct"]

# Categorical measures to summarise as suppressed distributions.
CATEGORICAL = ["bmi_category_num", "ipaq_category", "any_adverse_event",
               "any_adverse_event_24m", "confirmed_dcs", "cert_aowd_plus"]


def _read_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        cols = {c.strip().lower() for c in (reader.fieldnames or [])}
        leaked = cols & FORBIDDEN_COLUMNS
        if leaked:
            raise SystemExit(
                f"Refusing to aggregate: export contains identifier column(s) {sorted(leaked)}. "
                "Re-export a de-identified dataset (no IP / e-mail / identifiers)."
            )
        return list(reader)


def _continuous_summary(values: list[float], k: int) -> dict[str, Any] | None:
    n = len(values)
    if n < k:
        return None  # suppressed: too few respondents
    s = sorted(values)
    mid = n // 2
    median = s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2
    return {
        "n": n,
        "mean": round(sum(values) / n, 2),
        "median": round(median, 2),
        "min": round(s[0], 2),
        "max": round(s[-1], 2),
    }


def _categorical_summary(values: list[str], k: int) -> dict[str, Any]:
    counts = Counter(v for v in values if v != "")
    shown, suppressed = {}, 0
    for key, n in counts.items():
        if n >= k:
            shown[key] = n
        else:
            suppressed += n
    out: dict[str, Any] = {"n_total": sum(counts.values()), "distribution": shown}
    if suppressed:
        out["suppressed_n"] = suppressed  # report that small cells were hidden
    return out


def build_summary(rows: list[dict[str, Any]], k: int = DEFAULT_K) -> dict[str, Any]:
    """Derive scores per row, then return suppressed aggregates only."""
    enriched: list[dict[str, Any]] = []
    for row in rows:
        merged = dict(row)
        merged.update(scoring.score_record(row))
        enriched.append(merged)

    n = len(enriched)
    summary: dict[str, Any] = {
        "n_respondents": n,
        "k_anonymity_threshold": k,
        "note": "Aggregated, de-identified. Cells with n < k are suppressed (RODO/GDPR).",
        "continuous": {},
        "categorical": {},
    }
    if n < k:
        summary["note"] = f"Suppressed in full: only {n} respondents (< k={k})."
        return summary

    for field in CONTINUOUS:
        vals = [v for v in (scoring._num(r.get(field)) for r in enriched) if v is not None]
        summary["continuous"][field] = _continuous_summary(vals, k)

    for field in CATEGORICAL:
        vals = [str(r.get(field, "")).strip() for r in enriched]
        summary["categorical"][field] = _categorical_summary(vals, k)

    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description="Build de-identified dashboard summary.")
    ap.add_argument("--input", required=True, type=Path, help="REDCap export CSV (outside git)")
    ap.add_argument("--output", required=True, type=Path, help="summary.json to write")
    ap.add_argument("--k", type=int, default=DEFAULT_K, help=f"k-anonymity threshold (default {DEFAULT_K})")
    args = ap.parse_args()

    rows = _read_rows(args.input)
    log.info("Read %d rows from %s", len(rows), args.input)
    summary = build_summary(rows, k=args.k)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Wrote aggregated summary -> %s (n=%d, k=%d)", args.output, summary["n_respondents"], args.k)


if __name__ == "__main__":
    main()
