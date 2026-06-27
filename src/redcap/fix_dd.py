"""Transformacja Data Dictionary REDCap (PID 42, 'Nurkowanie').

Stosuje uzgodnione poprawki metodologiczne i techniczne, zachowując
strukturę pliku eksportu REDCap (kolejnosc kolumn, format CSV).
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

SRC = Path("/sessions/zen-bold-ride/mnt/nurki/Nurkowanie_DataDictionary_2026-06-21.csv")
OUT = Path("/sessions/zen-bold-ride/mnt/nurki/Nurkowanie_DataDictionary_POPRAWIONY.csv")


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Wczytuje DD jako listę słowników (zachowuje puste stringi, nie NaN)."""
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        header = list(reader.fieldnames or [])
        rows = [dict(r) for r in reader]
    return header, rows


def main() -> None:
    header, rows = load_rows(SRC)
    V = "Variable / Field Name"
    FORM = "Form Name"
    SEC = "Section Header"
    TYPE = "Field Type"
    LAB = "Field Label"
    CH = "Choices, Calculations, OR Slider Labels"
    NOTE = "Field Note"
    VAL = "Text Validation Type OR Show Slider Number"
    MIN = "Text Validation Min"
    MAX = "Text Validation Max"
    IDN = "Identifier?"
    BR = "Branching Logic (Show field only if...)"
    REQ = "Required Field?"
    ALN = "Custom Alignment"
    QN = "Question Number (surveys only)"
    MG = "Matrix Group Name"
    MR = "Matrix Ranking?"
    ANN = "Field Annotation"

    by_var = {r[V]: r for r in rows}

    def new_row(var, form, type_, label, choices="", note="", val="", vmin="",
                vmax="", branch="", req="", ann="", sec=""):
        d = {c: "" for c in header}
        d[V] = var
        d[FORM] = form
        d[TYPE] = type_
        d[LAB] = label
        d[CH] = choices
        d[NOTE] = note
        d[VAL] = val
        d[MIN] = vmin
        d[MAX] = vmax
        d[BR] = branch
        d[REQ] = req
        d[ANN] = ann
        d[SEC] = sec
        d[ALN] = "LV" if type_ in ("radio", "checkbox") else ""
        return d

    def insert_after(anchor_var, row):
        for i, r in enumerate(rows):
            if r[V] == anchor_var:
                rows.insert(i + 1, row)
                return
        raise KeyError(anchor_var)

    pii_note = ("Prosimy nie wpisywać danych umożliwiających identyfikację "
                "(imię, nazwisko, adres, telefon, e-mail).")

    # ---- 1) Tytuł + rozbudowana informacja RODO ----
    by_var["intro_text"][LAB] = (
        "<b>Stan zdrowia, aktywność fizyczna i wiedza z zakresu bezpieczeństwa "
        "jako czynniki związane ze zdarzeniami niepożądanymi wśród nurków "
        "rekreacyjnych w Polsce</b>\n\n"
        "Badanie realizowane przez Uniwersytet Medyczny w Białymstoku. "
        "Ankieta jest anonimowa, dobrowolna, czas wypełnienia: 12-18 minut.\n\n"
        "<b>Informacja dla uczestnika (RODO):</b>\n"
        "• Administrator danych: Uniwersytet Medyczny w Białymstoku, "
        "ul. Jana Kilińskiego 1, 15-089 Białystok.\n"
        "• Badanie uzyskało zgodę Komisji Bioetycznej UMB (nr APK.002.228.2026).\n"
        "• Udział jest dobrowolny i w pełni anonimowy; nie zbieramy adresu IP "
        "ani danych identyfikujących.\n"
        "• Dane będą przechowywane do 10 lat i wykorzystane wyłącznie w celach "
        "naukowych.\n"
        "• Z uwagi na pełną anonimowość, po przesłaniu ankiety nie jest możliwe "
        "wycofanie pojedynczych odpowiedzi.\n"
        "• Prosimy NIE wpisywać w polach tekstowych imienia, nazwiska, adresu, "
        "telefonu ani innych danych umożliwiających identyfikację.\n"
        "• Ankieta nie stanowi porady medycznej. W razie objawów po nurkowaniu "
        "skontaktuj się z lekarzem lub infolinią DAN.\n"
        "• Kontakt: Łukasz Minarowski, lukasz.minarowski@umb.edu.pl\n\n"
        "Autorzy: Łukasz Minarowski, Jakub Matuk, Maksymilian Lech\n"
        "Zakład Fizjopatologii Oddychania, Uniwersytet Medyczny w Białymstoku"
    )

    # ---- 1b) Masa ciała: dopuść liczby całkowite i z przecinkiem ----
    by_var["q6_weight_kg"][VAL] = "number_comma_decimal"
    by_var["q6_weight_kg"][NOTE] = "Można podać np. 65 lub 65,0 lub 72,5."

    # ---- 2) Płeć biologiczna do VO2max ----
    insert_after("q4_sex_other", new_row(
        "q4b_sex_bio", "dane_demograficzne", "radio",
        "Płeć biologiczna (wykorzystywana wyłącznie do oszacowania VO₂max):",
        choices="1, Kobieta | 2, Mężczyzna | 3, Wolę nie podawać",
        req="y",
    ))
    by_var["vo2max_estimated"][CH] = (
        "if([q4b_sex_bio]='1' or [q4b_sex_bio]='2', "
        "round(56.363 + 1.921*[pa_r_score] - 0.381*[q5_age] - 0.754*[bmi_calc] "
        "+ 10.987*if([q4b_sex_bio]='2', 1, 0), 2), '')"
    )
    by_var["vo2max_estimated"][NOTE] = (
        "Wzór regresyjny [Jackson 1990, Med Sci Sports Exerc 22(6):863-870]. "
        "Liczone tylko dla płci biologicznej kobieta/mężczyzna."
    )

    # ---- 3) PII noty przy polach tekstowych ----
    for var in ["q4_sex_other", "q12_other_cert", "q17_other_location",
                "q24_medications_list", "q40_baro_other", "q42_dcs_other",
                "q43_other_desc"]:
        by_var[var][NOTE] = pii_note

    # ---- 4) Checklisty chorób: @NONEOFTHEABOVE + wymagane ----
    none_codes = {
        "q19_cv_diseases": "8",
        "q20_resp_diseases": "7",
        "q21_neuro_diseases": "7",
        "q22_ent_problems": "6",
    }
    for var, code in none_codes.items():
        ann = by_var[var][ANN]
        tag = "@NONEOFTHEABOVE='%s'" % code
        by_var[var][ANN] = (ann + " " + tag).strip() if ann else tag
        by_var[var][REQ] = "y"

    # ---- 5) cert_aowd_plus numerycznie + pytanie dla "Inny" ----
    insert_after("q12_other_cert", new_row(
        "q12b_other_aowd", "ekspozycja_nurkowa", "radio",
        "Czy ten stopień odpowiada co najmniej poziomowi AOWD (Advanced) "
        "lub wyższemu?",
        choices="1, Tak | 2, Nie | 3, Nie wiem",
        branch="[q12_certification] = '7'",
    ))
    by_var["cert_aowd_plus"][CH] = (
        "if(([q12_certification] >= 3 and [q12_certification] <= 6) or "
        "([q12_certification] = '7' and [q12b_other_aowd] = '1'), 1, 0)"
    )

    # ---- 6) Branching DCS jawny ----
    by_var["q42_dcs_symptoms"][BR] = (
        "[q41_dcs_history] = '1' or [q41_dcs_history] = '2' or "
        "[q41_dcs_history] = '4'"
    )

    # ---- 7) q36: wymiana spornego pytania ----
    by_var["q36_kn_dan_riskfactor"][LAB] = (
        "Które zachowanie zwiększa ryzyko choroby dekompresyjnej (DCS)? "
        "[poziom: zaawansowany]"
    )
    by_var["q36_kn_dan_riskfactor"][CH] = (
        "1, Przestrzeganie przystanku bezpieczeństwa | "
        "2, Wielokrotne głębokie nurkowania z krótkimi przerwami "
        "powierzchniowymi | 3, Powolne wynurzanie | "
        "4, Korzystanie z komputera nurkowego"
    )
    by_var["q36_kn_dan_riskfactor"][NOTE] = "Poprawna: opcja 2."
    by_var["q36_score_dan_riskfactor"][CH] = (
        "if([q36_kn_dan_riskfactor] = '2', 1, 0)"
    )

    # ---- 8) Rozdział outcome lifetime vs 24 mies. + ciężkość ----
    yn24 = "1, Tak | 2, Nie | 3, Nie pamiętam"
    insert_after("q40_baro_other", new_row(
        "q39b_baro_24m", "zdarzenia_niepozadane", "radio",
        "Czy objawy barotraumy wystąpiły w ostatnich 24 miesiącach?",
        choices=yn24, branch="[q39_baro_history] = '1'",
    ))
    insert_after("q42_dcs_other", new_row(
        "q41b_dcs_24m", "zdarzenia_niepozadane", "radio",
        "Czy objawy DCS wystąpiły w ostatnich 24 miesiącach?",
        choices=yn24,
        branch="[q41_dcs_history] = '1' or [q41_dcs_history] = '2'",
    ))
    insert_after("q43_other_desc", new_row(
        "q43b_other_24m", "zdarzenia_niepozadane", "radio",
        "Czy te inne problemy zdrowotne wystąpiły w ostatnich 24 miesiącach?",
        choices=yn24, branch="[q43_other_problems] = '1'",
    ))
    insert_after("q44_vision_problems", new_row(
        "q44b_vision_24m", "zdarzenia_niepozadane", "radio",
        "Czy zaburzenia widzenia pod wodą wystąpiły w ostatnich 24 miesiącach?",
        choices=yn24, branch="[q44_vision_problems] = '1'",
    ))
    insert_after("q44b_vision_24m", new_row(
        "q_event_care", "zdarzenia_niepozadane", "checkbox",
        "Czy którekolwiek ze zdarzeń niepożądanych związanych z nurkowaniem "
        "wymagało: (wielokrotny wybór)",
        choices=("1, Konsultacji lekarskiej | 2, Podania tlenu | "
                 "3, Leczenia w komorze hiperbarycznej | 4, Hospitalizacji | "
                 "5, Przerwania nurkowania / rezygnacji | "
                 "6, Żadne z powyższych"),
        branch=("[q39_baro_history] = '1' or [q41_dcs_history] = '1' or "
                "[q41_dcs_history] = '2' or [q43_other_problems] = '1' or "
                "[q44_vision_problems] = '1'"),
        ann="@NONEOFTHEABOVE='6'",
    ))
    insert_after("q45_freediver_lmc", new_row(
        "q45b_freediver_24m", "zdarzenia_niepozadane", "radio",
        "Czy samba/LMC lub blackout wystąpiły w ostatnich 24 miesiącach?",
        choices=yn24,
        branch=("[q45_freediver_lmc] = '1' or [q45_freediver_lmc] = '2' or "
                "[q45_freediver_lmc] = '3'"),
    ))
    insert_after("q46_freediver_taravana", new_row(
        "q46b_taravana_24m", "zdarzenia_niepozadane", "radio",
        "Czy objawy taravany wystąpiły w ostatnich 24 miesiącach?",
        choices=yn24, branch="[q46_freediver_taravana] = '1'",
    ))

    # ---- 9) Punkty końcowe ----
    by_var["any_adverse_event"][LAB] = (
        "Punkt końcowy (lifetime): jakiekolwiek zdarzenie niepożądane "
        "kiedykolwiek (0/1)"
    )
    by_var["any_adverse_event"][CH] = (
        "if([q39_baro_history] = '1' or [q41_dcs_history] = '1' or "
        "[q41_dcs_history] = '2' or [q43_other_problems] = '1' or "
        "[q44_vision_problems] = '1' or [q45_freediver_lmc] = '1' or "
        "[q45_freediver_lmc] = '2' or [q45_freediver_lmc] = '3' or "
        "[q46_freediver_taravana] = '1', 1, 0)"
    )
    by_var["any_adverse_event"][NOTE] = (
        "Obejmuje barotraumę, DCS (pot./pod.), inne problemy, zaburzenia "
        "widzenia oraz zdarzenia freedivingowe (LMC/blackout/taravana)."
    )
    insert_after("any_adverse_event", new_row(
        "any_adverse_event_24m", "pola_pochodne", "calc",
        "Punkt końcowy (24 mies.): jakiekolwiek zdarzenie w ostatnich "
        "24 miesiącach (0/1)",
        choices=("if([q39b_baro_24m] = '1' or [q41b_dcs_24m] = '1' or "
                 "[q43b_other_24m] = '1' or [q44b_vision_24m] = '1' or "
                 "[q45b_freediver_24m] = '1' or [q46b_taravana_24m] = '1', "
                 "1, 0)"),
        note="Glowny punkt koncowy do analizy determinant (spojny czasowo z ekspozycja).",
        ann="@HIDDEN-SURVEY",
    ))
    insert_after("any_adverse_event_24m", new_row(
        "serious_adverse_event", "pola_pochodne", "calc",
        "Ciężkie zdarzenie niepożądane (0/1)",
        choices=("if([q_event_care(1)] = '1' or [q_event_care(2)] = '1' or "
                 "[q_event_care(3)] = '1' or [q_event_care(4)] = '1' or "
                 "[q_event_care(5)] = '1', 1, 0)"),
        note=("Wymagalo konsultacji / tlenu / komory / hospitalizacji / "
              "przerwania nurkowania."),
        ann="@HIDDEN-SURVEY",
    ))
    insert_after("serious_adverse_event", new_row(
        "confirmed_dcs", "pola_pochodne", "calc",
        "DCS potwierdzona medycznie (0/1)",
        choices="if([q41_dcs_history] = '1', 1, 0)",
        ann="@HIDDEN-SURVEY",
    ))
    insert_after("confirmed_dcs", new_row(
        "suspected_dcs", "pola_pochodne", "calc",
        "DCS podejrzewana, bez diagnozy (0/1)",
        choices="if([q41_dcs_history] = '2', 1, 0)",
        ann="@HIDDEN-SURVEY",
    ))

    # ---- 10) KRYTYCZNE: klucz odpowiedzi -> Field Annotation ----
    kn_fields = [r for r in rows if r[FORM] == "test_wiedzy"
                 and r[V].startswith("q") and "_kn_" in r[V]]
    moved = 0
    for r in kn_fields:
        if r[NOTE].strip():
            key = "[KLUCZ: %s]" % r[NOTE].strip()
            r[ANN] = (r[ANN] + " " + key).strip() if r[ANN] else key
            r[NOTE] = ""
            moved += 1

    # ---- 11) @HIDDEN-SURVEY na calc + intro_scoring ----
    hidden = 0
    for r in rows:
        is_calc = r[TYPE] == "calc"
        is_scoring_desc = r[V] == "intro_scoring"
        if (is_calc or is_scoring_desc) and "@HIDDEN-SURVEY" not in r[ANN]:
            r[ANN] = (r[ANN] + " @HIDDEN-SURVEY").strip() if r[ANN] else "@HIDDEN-SURVEY"
            hidden += 1

    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)
    log.info("Zapisano: %s", OUT)
    log.info("Wierszy (pol) razem: %d", len(rows))
    log.info("Klucz odpowiedzi przeniesiony: %d pol", moved)
    log.info("@HIDDEN-SURVEY dodane: %d pol", hidden)


if __name__ == "__main__":
    main()
