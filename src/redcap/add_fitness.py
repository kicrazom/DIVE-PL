"""Dodaje moduly wydolnosci/aktywnosci do Data Dictionary REDCap (PID 42).

Baza: aktualny (zaimportowany) slownik POPRAWIONY.csv.
Dodaje: IPAQ-SF, VSAQ, pelny DASI-12, blok nurkowo-funkcjonalny + pola pochodne.
Usuwa: q26_weekly_exercise_h (zastapione przez IPAQ-SF).
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

SRC = Path("/sessions/zen-bold-ride/mnt/nurki/Nurkowanie_DataDictionary_POPRAWIONY.csv")
OUT = Path("/sessions/zen-bold-ride/mnt/nurki/Nurkowanie_DataDictionary_v3.csv")


def main() -> None:
    with SRC.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        header = list(reader.fieldnames or [])
        rows = [dict(r) for r in reader]

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
    BR = "Branching Logic (Show field only if...)"
    REQ = "Required Field?"
    ALN = "Custom Alignment"
    ANN = "Field Annotation"

    by_var = {r[V]: r for r in rows}

    def nr(var, type_, label, choices="", note="", val="", vmin="", vmax="",
           branch="", req="", ann="", sec="", form="aktywnosc_fizyczna"):
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
        d[ALN] = "LV" if type_ in ("radio", "checkbox", "yesno") else ""
        return d

    def insert_after(anchor_var, new_rows):
        for i, r in enumerate(rows):
            if r[V] == anchor_var:
                for off, nrow in enumerate(new_rows, start=1):
                    rows.insert(i + off, nrow)
                return
        raise KeyError(anchor_var)

    # ---- usun q26_weekly_exercise_h ----
    rows[:] = [r for r in rows if r[V] != "q26_weekly_exercise_h"]

    # ---- doprecyzuj note VO2max ----
    by_var["vo2max_estimated"][NOTE] = (
        "Wartosc SZACOWANA metoda non-exercise [Jackson 1990, Med Sci Sports "
        "Exerc 22(6):863-870], nie pomiar CPET. Liczone tylko dla plci "
        "biologicznej kobieta/mezczyzna."
    )

    # ====== nowe pytania (instrument: aktywnosc_fizyczna) ======
    new_q = []

    # --- IPAQ-SF (ostatnie 7 dni) ---
    new_q.append(nr("ipaq_vig_days", "text",
        "W ciagu ostatnich 7 dni, przez ile DNI wykonywal(a) Pan/Pani "
        "INTENSYWNA aktywnosc fizyczna (np. dzwiganie ciezarow, kopanie, "
        "aerobik, szybka jazda rowerem) przez co najmniej 10 minut?",
        val="integer", vmin="0", vmax="7", req="y",
        sec="G1. Aktywnosc fizyczna - ostatnie 7 dni (IPAQ-SF)"))
    new_q.append(nr("ipaq_vig_min", "text",
        "Ile zwykle MINUT dziennie trwala ta intensywna aktywnosc?",
        val="integer", vmin="0", vmax="960", branch="[ipaq_vig_days] > 0"))
    new_q.append(nr("ipaq_mod_days", "text",
        "Przez ile DNI wykonywal(a) Pan/Pani UMIARKOWANA aktywnosc fizyczna "
        "(np. niesienie lekkich ciezarow, rower w umiarkowanym tempie; "
        "NIE wliczaj chodzenia)?",
        val="integer", vmin="0", vmax="7", req="y"))
    new_q.append(nr("ipaq_mod_min", "text",
        "Ile zwykle MINUT dziennie trwala ta umiarkowana aktywnosc?",
        val="integer", vmin="0", vmax="960", branch="[ipaq_mod_days] > 0"))
    new_q.append(nr("ipaq_walk_days", "text",
        "Przez ile DNI chodzil(a) Pan/Pani co najmniej 10 minut bez przerwy?",
        val="integer", vmin="0", vmax="7", req="y"))
    new_q.append(nr("ipaq_walk_min", "text",
        "Ile zwykle MINUT dziennie zajmowalo to chodzenie?",
        val="integer", vmin="0", vmax="960", branch="[ipaq_walk_days] > 0"))
    new_q.append(nr("ipaq_sit_hours", "text",
        "Ile zwykle GODZIN dziennie spedza Pan/Pani siedzac (w dzien "
        "powszedni)?",
        val="integer", vmin="0", vmax="24", req="y"))

    # --- VSAQ (adaptacja, self-reported MET capacity) ---
    new_q.append(nr("vsaq_level", "radio",
        "Prosze wskazac NAJBARDZIEJ wymagajaca czynnosc, ktora jest Pan/Pani "
        "w stanie wykonac BEZ zatrzymania z powodu zmeczenia lub zadyszki:",
        choices=(
            "1, Jedzenie, ubieranie sie, praca przy biurku (~1 MET) | "
            "2, Spacer po domu, lekkie prace (~2 MET) | "
            "3, Wolny spacer ~3 km/h, prysznic (~3 MET) | "
            "4, Lekkie prace domowe (odkurzanie), szybszy spacer (~4 MET) | "
            "5, Lekkie prace ogrodowe, taniec towarzyski (~5 MET) | "
            "6, Umiarkowane prace fizyczne, wolny jogging (~6 MET) | "
            "7, Tenis (singiel), wnoszenie ciezkich zakupow po schodach (~7 MET) | "
            "8, Szybki jogging, wchodzenie po schodach bez przerwy (~8 MET) | "
            "9, Szybka jazda rowerem, umiarkowane plywanie (~9 MET) | "
            "10, Szybkie plywanie, bieg ~10 km/h (~10 MET) | "
            "11, Bieg szybki, narciarstwo biegowe (~11 MET) | "
            "12, Bieg ~12 km/h (~12 MET) | "
            "13, Sport wyczynowy, bieg > 12 km/h (~13 MET)"),
        note="Adaptacja VSAQ (self-reported MET capacity); skala nieobciazeniowa.",
        req="y",
        sec="G2. Wydolnosc funkcjonalna - tolerancja wysilku (VSAQ, adapt.)"))

    # --- pelny DASI-12 (Hlatky 1989) ---
    new_q.append(nr("dasi_selfcare", "yesno",
        "Czy jest Pan/Pani w stanie samodzielnie zadbac o siebie (jesc, "
        "ubierac sie, kapac sie, korzystac z toalety)?",
        sec="G3. Wydolnosc funkcjonalna (DASI)"))
    new_q.append(nr("dasi_walk_indoor", "yesno",
        "Czy jest Pan/Pani w stanie chodzic po domu (np. miedzy pokojami)?"))
    new_q.append(nr("dasi_walk_block", "yesno",
        "Czy jest Pan/Pani w stanie przejsc 1-2 przecznice po plaskim terenie?"))
    new_q.append(nr("dasi_stairs", "yesno",
        "Czy jest Pan/Pani w stanie wejsc po schodach na pietro lub wejsc "
        "na wzniesienie?"))
    new_q.append(nr("dasi_run", "yesno",
        "Czy jest Pan/Pani w stanie przebiec krotki dystans?"))
    new_q.append(nr("dasi_light_house", "yesno",
        "Czy jest Pan/Pani w stanie wykonywac lekkie prace domowe "
        "(scieranie kurzu, zmywanie naczyn)?"))
    new_q.append(nr("dasi_mod_house", "yesno",
        "Czy jest Pan/Pani w stanie wykonywac umiarkowane prace domowe "
        "(odkurzanie, zamiatanie, noszenie zakupow)?"))
    new_q.append(nr("dasi_heavy_house", "yesno",
        "Czy jest Pan/Pani w stanie wykonywac ciezkie prace domowe "
        "(szorowanie podlog, podnoszenie/przesuwanie ciezkich mebli)?"))
    new_q.append(nr("dasi_yard", "yesno",
        "Czy jest Pan/Pani w stanie wykonywac prace w ogrodzie (grabienie "
        "lisci, pielenie, pchanie kosiarki)?"))
    new_q.append(nr("dasi_sex", "yesno",
        "Czy jest Pan/Pani w stanie odbywac stosunki seksualne?",
        note="Pytanie nieobowiazkowe - mozna pominac."))
    new_q.append(nr("dasi_mod_rec", "yesno",
        "Czy uczestniczy Pan/Pani w umiarkowanych aktywnosciach "
        "rekreacyjnych (golf, kregle, taniec, tenis debel, rzucanie pilka)?"))
    new_q.append(nr("dasi_strenuous", "yesno",
        "Czy uczestniczy Pan/Pani w intensywnych sportach (plywanie, tenis "
        "singlowy, pilka nozna, koszykowka, narciarstwo)?"))

    # --- blok nurkowo-funkcjonalny (eksploracyjny) ---
    tnw = "1, Tak | 2, Nie | 3, Nie probowalem / nie wiem"
    new_q.append(nr("dive_swim200", "radio",
        "Czy jest Pan/Pani w stanie przeplynac 200 m po powierzchni w "
        "pletwach bez zatrzymywania?",
        choices=tnw, ann="[EKSPLORACYJNE]",
        sec="G4. Sprawnosc specyficzna dla nurkowania (eksploracyjne)"))
    new_q.append(nr("dive_exit_gear", "radio",
        "Czy jest Pan/Pani w stanie wyjsc z wody po drabince lub stromym "
        "brzegu z pelnym sprzetem?",
        choices=tnw, ann="[EKSPLORACYJNE]"))
    new_q.append(nr("dive_carry50", "radio",
        "Czy jest Pan/Pani w stanie niesc zestaw nurkowy przez co najmniej "
        "50 m?",
        choices=tnw, ann="[EKSPLORACYJNE]"))
    new_q.append(nr("dive_assist_buddy", "radio",
        "Czy jest Pan/Pani w stanie pomoc partnerowi w sytuacji awaryjnej "
        "(np. holowanie na krotkim dystansie)?",
        choices=tnw, ann="[EKSPLORACYJNE]"))
    new_q.append(nr("dive_stop_symptoms_24m", "radio",
        "Czy w ostatnich 24 miesiacach przerwal(a) Pan/Pani nurkowanie z "
        "powodu zmeczenia, dusznosci, kolatania serca, bolu w klatce "
        "piersiowej lub kurczow?",
        choices="1, Tak | 2, Nie", ann="[EKSPLORACYJNE]"))

    insert_after("q28_pre_dive_activity", new_q)

    # ====== pola pochodne (calc, @HIDDEN-SURVEY) ======
    derived = []
    derived.append(nr("ipaq_vig_met", "calc", "IPAQ: MET-min intensywna",
        choices="if([ipaq_vig_min] = \"\", 0, 8 * [ipaq_vig_days] * [ipaq_vig_min])",
        ann="@HIDDEN-SURVEY", form="pola_pochodne",
        sec="Aktywnosc / wydolnosc - pochodne"))
    derived.append(nr("ipaq_mod_met", "calc", "IPAQ: MET-min umiarkowana",
        choices="if([ipaq_mod_min] = \"\", 0, 4 * [ipaq_mod_days] * [ipaq_mod_min])",
        ann="@HIDDEN-SURVEY", form="pola_pochodne"))
    derived.append(nr("ipaq_walk_met", "calc", "IPAQ: MET-min chodzenie",
        choices="if([ipaq_walk_min] = \"\", 0, 3.3 * [ipaq_walk_days] * [ipaq_walk_min])",
        ann="@HIDDEN-SURVEY", form="pola_pochodne"))
    derived.append(nr("ipaq_total_met", "calc",
        "IPAQ-SF calkowity [MET-min/tydz.]",
        choices="[ipaq_vig_met] + [ipaq_mod_met] + [ipaq_walk_met]",
        note="Kategoria low/moderate/high - w post-processingu (Python).",
        ann="@HIDDEN-SURVEY", form="pola_pochodne"))
    derived.append(nr("vsaq_mets", "calc",
        "VSAQ: szacowana wydolnosc [MET]",
        choices="[vsaq_level]",
        ann="@HIDDEN-SURVEY", form="pola_pochodne"))
    derived.append(nr("vsaq_below_7met", "calc",
        "VSAQ < 7 MET (ponizej typowego obciazenia nurkowego)",
        choices="if([vsaq_level] < 7, 1, 0)",
        ann="@HIDDEN-SURVEY", form="pola_pochodne"))
    derived.append(nr("vsaq_below_10met", "calc",
        "VSAQ < 10 MET (ponizej rekomendowanej rezerwy)",
        choices="if([vsaq_level] < 10, 1, 0)",
        ann="@HIDDEN-SURVEY", form="pola_pochodne"))
    derived.append(nr("dasi_score", "calc", "DASI wynik (0-58.2)",
        choices=("2.75*[dasi_selfcare] + 1.75*[dasi_walk_indoor] + "
                 "2.75*[dasi_walk_block] + 5.5*[dasi_stairs] + 8*[dasi_run] + "
                 "2.7*[dasi_light_house] + 3.5*[dasi_mod_house] + "
                 "8*[dasi_heavy_house] + 4.5*[dasi_yard] + 5.25*[dasi_sex] + "
                 "6*[dasi_mod_rec] + 7.5*[dasi_strenuous]"),
        note="Suma wazona 12 itemow. Uwaga: pominiety item 'stosunki' zaniza wynik.",
        ann="@HIDDEN-SURVEY", form="pola_pochodne"))
    derived.append(nr("dasi_vo2peak", "calc",
        "DASI: szacowany VO2peak [ml/kg/min]",
        choices="0.43*[dasi_score] + 9.6",
        ann="@HIDDEN-SURVEY", form="pola_pochodne"))
    derived.append(nr("dasi_mets", "calc", "DASI: szacowane METy",
        choices="round((0.43*[dasi_score] + 9.6) / 3.5, 1)",
        ann="@HIDDEN-SURVEY", form="pola_pochodne"))
    derived.append(nr("dasi_below_7met", "calc",
        "DASI < 7 MET (ponizej typowego obciazenia nurkowego)",
        choices="if(((0.43*[dasi_score] + 9.6) / 3.5) < 7, 1, 0)",
        ann="@HIDDEN-SURVEY", form="pola_pochodne"))
    derived.append(nr("dive_func_limited", "calc",
        "Ograniczenie sprawnosci nurkowej (eksploracyjne, 0/1)",
        choices=("if([dive_swim200] = '2' or [dive_exit_gear] = '2' or "
                 "[dive_carry50] = '2' or [dive_assist_buddy] = '2' or "
                 "[dive_stop_symptoms_24m] = '1', 1, 0)"),
        ann="@HIDDEN-SURVEY [EKSPLORACYJNE]", form="pola_pochodne"))

    insert_after("vo2max_median_note", derived)

    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)

    log.info("Zapisano: %s", OUT)
    log.info("Pol razem: %d", len(rows))
    log.info("Nowych pytan: %d, nowych pochodnych: %d", len(new_q), len(derived))


if __name__ == "__main__":
    main()
