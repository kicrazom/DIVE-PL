# Szkielet pracy inżynierskiej / methods paper (PL)

> Robocza struktura. Język pracy: polski; cytowania IEEE; DOI/URL przy każdym źródle.
> Pozycjonowanie: praca **metodologiczna (framework) z wdrożeniowym studium przypadku** — nie odkrycie pojedynczej techniki.

## Streszczenie / Abstract
- Problem, luka, propozycja (zintegrowany pipeline AI + open science), studium przypadku, główny wkład.

## 1. Wstęp
- 1.1. Kontekst: rosnące użycie LLM w badaniach ankietowych.
- 1.2. Luka badawcza: komponenty opisane osobno; brak zintegrowanej, odtwarzalnej metodyki end-to-end.
- 1.3. Cel pracy i pytania badawcze.
- 1.4. Wkład: (i) framework 4-komponentowy, (ii) warstwa open-science, (iii) implementacja referencyjna, (iv) studium przypadku.

## 2. Przegląd literatury (related work)
- 2.1. LLM tworzące narzędzia ankietowe.
- 2.2. LLM-as-judge / recenzent pozycji.
- 2.3. REDCap + AI.
- 2.4. AI-dashboardy w badaniach.
- 2.5. Ramy koncepcyjne i czego im brakuje.
- (Tabela: komponent -> precedens -> różnica — zob. docs/related-work.md.)

## 3. Metodyka frameworku DIVE-PL
- 3.1. Założenia (human-in-the-loop, rozdzielenie ról, odtwarzalność, RODO/sovereignty, transparentność).
- 3.2–3.5. Etapy 1–4 (agent, recenzent, REDCap, dashboardy).
- 3.6. Warstwa open-science (GitHub, Zenodo, OSF, Pages).
- 3.7. Diagram architektury.

## 4. Studium przypadku: nurkowie rekreacyjni w Polsce
- 4.1. Cel i hipotezy (H1–H3).
- 4.2. Zastosowanie każdego etapu frameworku.
- 4.3. Etyka i rejestracja (komisja bioetyczna, ClinicalTrials.gov, RODO).
- 4.4. Uwaga: VO2max szacowany vs mierzony (ograniczenie trafności).

## 5. Wyniki / Ewaluacja frameworku
- 5.1. Mierniki procesu (czas, liczba iteracji recenzenta, wykryte problemy pozycji).
- 5.2. Odtwarzalność (czy osoba trzecia odtworzy pipeline).
- 5.3. (Opcjonalnie) wstępne wyniki ankiety jako dowód działania.

## 6. Dyskusja
- 6.1. Wkład względem literatury.
- 6.2. Ograniczenia: dowód częściowo preprintowy; AI = wsparcie, nie zastępstwo; ryzyko biasu LLM.
- 6.3. Implikacje dla suwerenności cyfrowej i nauki otwartej.

## 7. Wnioski i dalsze prace.

## Bibliografia (IEEE)
## Załączniki: prompty, data dictionary REDCap, kod analizy, link do dashboardu.
