"""DIVE-PL Stage 4 — derived-score functions.

Faithful Python mirror of the REDCap `calc` fields in
``../redcap/data_dictionary_v4.csv``. The REDCap project computes these on capture;
this module re-derives them for offline analysis and as an independently auditable
record of the scoring logic (the formulas are the contract, not hidden in REDCap).

Operates on a single respondent's **de-identified** field dict and returns the derived
values. No PII is read or produced. Pure functions, no I/O.

References (instrument scoring):
- IPAQ-SF scoring protocol (MET values 8.0 / 4.0 / 3.3; low/moderate/high categories).
- DASI: Hlatky et al. 1989; VO2peak = 0.43*DASI + 9.6; METs = VO2peak / 3.5.
- VSAQ: self-reported MET capacity (level == METs).
- Non-exercise VO2max: University of Houston model (Jackson et al. 1990),
  constants as encoded in REDCap `vo2max_estimated`.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

log = logging.getLogger(__name__)

# MET constants (IPAQ-SF) ----------------------------------------------------
MET_VIG = 8.0
MET_MOD = 4.0
MET_WALK = 3.3

# Knowledge answer key (q -> correct option code), from REDCap score formulas.
KNOWLEDGE_KEY: dict[str, str] = {
    "q29_kn_barotrauma": "1",
    "q30_kn_dcs": "2",
    "q31_kn_main_gas": "3",
    "q32_kn_dcs_action": "3",
    "q33_kn_mod_nitrox": "3",
    "q34_kn_baro_atypical": "3",
    "q35_kn_narcosis": "2",
    "q36_kn_dan_riskfactor": "2",
    "q37_kn_type2_dcs": "2",
    "q38_kn_lung_baro": "3",
}
KNOWLEDGE_BASIC = ["q29_kn_barotrauma", "q30_kn_dcs", "q31_kn_main_gas", "q32_kn_dcs_action"]
KNOWLEDGE_ADVANCED = ["q33_kn_mod_nitrox", "q34_kn_baro_atypical", "q35_kn_narcosis", "q36_kn_dan_riskfactor"]
KNOWLEDGE_EMERGENCY = ["q37_kn_type2_dcs", "q38_kn_lung_baro"]


def _num(value: Any) -> Optional[float]:
    """Parse a REDCap value to float; '' / None / non-numeric -> None."""
    if value is None:
        return None
    s = str(value).strip().replace(",", ".")
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def bmi(weight_kg: Any, height_cm: Any) -> Optional[float]:
    """REDCap bmi_calc: round(weight / (height_m**2), 2)."""
    w, h = _num(weight_kg), _num(height_cm)
    if w is None or h is None or h == 0:
        return None
    return round(w / ((h / 100) ** 2), 2)


def bmi_category(bmi_value: Optional[float]) -> Optional[int]:
    """REDCap bmi_category_num: 1 underweight, 2 normal, 3 overweight, 4 obese."""
    if bmi_value is None:
        return None
    if bmi_value < 18.5:
        return 1
    if bmi_value < 25:
        return 2
    if bmi_value < 30:
        return 3
    return 4


def vo2max_houston(pa_r_score: Any, age: Any, bmi_value: Optional[float], sex_bio: Any) -> Optional[float]:
    """REDCap vo2max_estimated — University of Houston non-exercise model.

    Defined only when sex_bio is 1 (male) or 2 (female); blank otherwise
    (mirrors 'wolę nie podawać' -> empty). sex term = 10.987 for female (code '2').
    NOTE: VO2max is *estimated*, not measured — a validity limitation to disclose.
    """
    par, a = _num(pa_r_score), _num(age)
    s = str(sex_bio).strip()
    if s not in {"1", "2"} or par is None or a is None or bmi_value is None:
        return None
    sex_term = 10.987 if s == "2" else 0.0
    return round(56.363 + 1.921 * par - 0.381 * a - 0.754 * bmi_value + sex_term, 2)


def ipaq(row: dict[str, Any]) -> dict[str, Any]:
    """IPAQ-SF MET-min/week per domain, total, and low/moderate/high category."""
    def met(days_key: str, min_key: str, factor: float) -> float:
        d, m = _num(row.get(days_key)), _num(row.get(min_key))
        if m is None or d is None:
            return 0.0  # REDCap returns 0 when minutes blank
        return factor * d * m

    vig = met("ipaq_vig_days", "ipaq_vig_min", MET_VIG)
    mod = met("ipaq_mod_days", "ipaq_mod_min", MET_MOD)
    walk = met("ipaq_walk_days", "ipaq_walk_min", MET_WALK)
    total = vig + mod + walk

    vig_days = _num(row.get("ipaq_vig_days")) or 0
    mod_days = _num(row.get("ipaq_mod_days")) or 0
    walk_days = _num(row.get("ipaq_walk_days")) or 0
    active_days = vig_days + mod_days + walk_days  # upper bound on distinct days

    # IPAQ-SF category (standard protocol)
    if (vig_days >= 3 and total >= 1500) or (active_days >= 7 and total >= 3000):
        category = "high"
    elif vig_days >= 3 or (mod_days + walk_days) >= 5 or active_days >= 5 or total >= 600:
        category = "moderate"
    else:
        category = "low"

    return {
        "ipaq_vig_met": round(vig, 1),
        "ipaq_mod_met": round(mod, 1),
        "ipaq_walk_met": round(walk, 1),
        "ipaq_total_met": round(total, 1),
        "ipaq_category": category,
    }


# DASI item weights (REDCap dasi_score), in field order.
_DASI_WEIGHTS = {
    "dasi_selfcare": 2.75, "dasi_walk_indoor": 1.75, "dasi_walk_block": 2.75,
    "dasi_stairs": 5.5, "dasi_run": 8.0, "dasi_light_house": 2.7,
    "dasi_mod_house": 3.5, "dasi_heavy_house": 8.0, "dasi_yard": 4.5,
    "dasi_sex": 5.25, "dasi_mod_rec": 6.0, "dasi_strenuous": 7.5,
}


def dasi(row: dict[str, Any]) -> dict[str, Any]:
    """DASI score (0–58.2), estimated VO2peak and METs."""
    score = 0.0
    for field, weight in _DASI_WEIGHTS.items():
        v = _num(row.get(field))
        if v is not None:
            score += weight * v
    score = round(score, 2)
    vo2peak = round(0.43 * score + 9.6, 2)
    mets = round(vo2peak / 3.5, 1)
    return {
        "dasi_score": score,
        "dasi_vo2peak": vo2peak,
        "dasi_mets": mets,
        "dasi_below_7met": int(mets < 7),
    }


def vsaq(row: dict[str, Any]) -> dict[str, Any]:
    """VSAQ self-reported MET capacity (level == METs)."""
    level = _num(row.get("vsaq_level"))
    if level is None:
        return {"vsaq_mets": None, "vsaq_below_7met": None, "vsaq_below_10met": None}
    return {
        "vsaq_mets": level,
        "vsaq_below_7met": int(level < 7),
        "vsaq_below_10met": int(level < 10),
    }


def knowledge(row: dict[str, Any]) -> dict[str, Any]:
    """Safety-knowledge score (0–10) from the answer key, plus subscales and %."""
    def correct(q: str) -> int:
        return int(str(row.get(q, "")).strip() == KNOWLEDGE_KEY[q])

    basic = sum(correct(q) for q in KNOWLEDGE_BASIC)
    advanced = sum(correct(q) for q in KNOWLEDGE_ADVANCED)
    emergency = sum(correct(q) for q in KNOWLEDGE_EMERGENCY)
    total = basic + advanced + emergency
    return {
        "knowledge_score_basic": basic,
        "knowledge_score_advanced": advanced,
        "knowledge_score_emergency": emergency,
        "knowledge_score_total": total,
        "knowledge_pct": round(total * 10, 1),
    }


def score_record(row: dict[str, Any]) -> dict[str, Any]:
    """Derive all scores for one de-identified respondent record.

    Returns a flat dict of derived fields. Input is a REDCap field dict; PII is
    neither expected nor used.
    """
    bmi_value = bmi(row.get("q6_weight_kg"), row.get("q7_height_cm"))
    pa_r = None if _num(row.get("q25_pa_r")) is None else _num(row.get("q25_pa_r")) - 1

    derived: dict[str, Any] = {
        "bmi_calc": bmi_value,
        "bmi_category_num": bmi_category(bmi_value),
        "pa_r_score": pa_r,
        "vo2max_estimated": vo2max_houston(pa_r, row.get("q5_age"), bmi_value, row.get("q4b_sex_bio")),
    }
    derived.update(ipaq(row))
    derived.update(dasi(row))
    derived.update(vsaq(row))
    derived.update(knowledge(row))
    return derived
