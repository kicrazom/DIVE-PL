"""DIVE-PL Stage 4 — minimal Streamlit dashboard.

Renders the **aggregated, de-identified** summary produced by ``aggregate.py``.
It reads only ``summary.json`` — never raw participant data — so it is safe to run
locally or publish. Charts use Streamlit's built-ins (no extra plotting dependency).

Run:
    streamlit run app.py -- --summary summary.json

The static GitHub Pages site under ``../../docs/`` is the public face; this app is the
interactive reference implementation an investigator runs locally over an export.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import streamlit as st

CONTINUOUS_LABELS = {
    "bmi_calc": "BMI [kg/m²]",
    "vo2max_estimated": "VO₂max (estimated) [ml/kg/min]",
    "ipaq_total_met": "IPAQ-SF total [MET-min/week]",
    "dasi_mets": "DASI [MET]",
    "vsaq_mets": "VSAQ [MET]",
    "knowledge_pct": "Safety knowledge [%]",
}
CATEGORICAL_LABELS = {
    "bmi_category_num": "BMI category (1–4)",
    "ipaq_category": "IPAQ activity category",
    "any_adverse_event": "Any adverse event (lifetime)",
    "any_adverse_event_24m": "Any adverse event (24 months)",
    "confirmed_dcs": "Confirmed DCS",
    "cert_aowd_plus": "Certification AOWD+",
}


def _load_summary() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", default="summary.json")
    args, _ = parser.parse_known_args(sys.argv[1:])
    path = Path(args.summary)
    if not path.exists():
        st.error(f"Summary file not found: {path}. Run `python aggregate.py` first.")
        st.stop()
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    st.set_page_config(page_title="DIVE-PL — aggregate dashboard", layout="wide")
    st.title("DIVE-PL — case-study dashboard")
    st.caption("Recreational divers in Poland · aggregated, de-identified data only (RODO/GDPR)")

    summary = _load_summary()
    n = summary.get("n_respondents", 0)
    k = summary.get("k_anonymity_threshold", "?")

    c1, c2 = st.columns(2)
    c1.metric("Respondents (n)", n)
    c2.metric("k-anonymity threshold", k)
    st.info(summary.get("note", ""))

    if n < (k if isinstance(k, int) else 0):
        st.warning("Too few respondents — all cells suppressed.")
        return

    st.subheader("Continuous measures")
    cont = summary.get("continuous", {})
    rows = []
    for field, stats in cont.items():
        label = CONTINUOUS_LABELS.get(field, field)
        if stats is None:
            rows.append({"Measure": label, "n": "suppressed", "Mean": "", "Median": "", "Min": "", "Max": ""})
        else:
            rows.append({"Measure": label, "n": stats["n"], "Mean": stats["mean"],
                         "Median": stats["median"], "Min": stats["min"], "Max": stats["max"]})
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)

    st.subheader("Categorical distributions")
    cat = summary.get("categorical", {})
    for field, stats in cat.items():
        label = CATEGORICAL_LABELS.get(field, field)
        dist = stats.get("distribution", {})
        st.markdown(f"**{label}** — n = {stats.get('n_total', 0)}"
                    + (f" · {stats['suppressed_n']} suppressed (small cells)" if stats.get("suppressed_n") else ""))
        if dist:
            st.bar_chart(dist)
        else:
            st.caption("All cells suppressed.")


if __name__ == "__main__":
    main()
