# Umsetzung des eigenen XML-Formats — Ideen

Sammelort für Vorschläge zur konkreten Umsetzung des LegalXML-Formats
in der Praxis. Kein endgültiges Konzept, sondern Diskussionsgrundlage.

## Bestand

Was schon vorhanden ist (Stand 26.04.2026):

- **Schemas** für BGer, OGer ZH, OGer BE, KGer LU, AppGer BS
- **Gemeinsame Bausteine** in `common-ch.xsd` (Chameleon-Pattern, ~70%
  Duplikation eliminiert)
- **Beispieldokumente** für BGer-Entscheid und BGer-Rechtsschrift
- **Argumentarium-PDF** für Drittpräsentation
- **Lorentzo-Datensatz** mit gecrawlten HTML+JSON-Urteilen
  (BL, CH-BGE, CH-BVGer, FR, GE, LU, OW, SG, TI, UR — je 10 Verzeichnisse)
- **XML-Viewer** (Svelte-App, in Entwicklung — Jans Bereich)

## 1 — Erstellung von XML-Dokumenten

Wie kommen die Daten ins XML rein?

### Optionen

| Variante | Wer ist die Zielgruppe? | Aufwand | Akzeptanz |
|---|---|---|---|
| **Form-basierter Web-Editor** | Anwälte, ohne XML-Kenntnis | mittel | hoch |
| **Word-Add-In** | Anwälte, die in Word bleiben wollen | hoch | sehr hoch |
| **LLM-assistierte Konversion** PDF/DOCX → XML | für Bestand und Schnellerfassung | mittel | hoch |
| **Direkter XML-Editor** (Oxygen, VS Code mit Schema) | Tech-affine Mitarbeitende | gering | niedrig |
| **Markdown-ähnliche DSL** mit Konverter | Mittelweg | hoch | mittel |

### Empfehlung

Zweistufig:
1. **Kurzfristig**: LLM-assistierte Konversion. PDF-Eingabe → strukturiertes
   XML mit Review-Schritt. Niedriger Initialaufwand, schnelles Ergebnis.
   Nutzt vorhandene Schemas als Constraint.
2. **Mittelfristig**: Form-basierter Web-Editor mit dynamisch generierten
   Formularen aus dem XSD. Felder pro Sektion (Rubrum, Rechtsbegehren,
   Begründung, Beilagen). Wiederverwendbare Bausteine.

Word-Add-In wäre der "richtige" Weg für höchste Akzeptanz, aber bindet
ans Microsoft-Ökosystem und vervielfacht den Aufwand.

## 2 — Speicherung und Versionierung

### Optionen

| Variante | Wann sinnvoll? |
|---|---|
| **Git + Dateisystem** | wenige hundert Dokumente, technisches Team, gute Diff-Sicht |
| **Native XML-DB** (eXist-DB, BaseX) | viele tausend Dokumente, XPath/XQuery direkt |
| **Postgres mit `xml`-Typ** | XML neben Stammdaten in derselben DB |
| **Hybrid**: Files in Git + Index in Postgres | Versionierung pro Dokument + schnelle Suche |

### Empfehlung

**Hybrid**. XML-Dateien im Dateisystem (eine Datei pro Dokument,
Verzeichnisstruktur nach Mandant/Fall/Datum). Git als Versionierung.
Parallel ein Postgres-Index, der bei jedem Schreiben mit relevanten
Metadaten und Volltext-Auszügen gefüttert wird (Trigger oder Worker).

Begründung: Dateien sind portierbar, archivfest, einfach zu sichern.
Postgres ergänzt für Suche und Statistik.

## 3 — Validierung

Drei Validierungs­ebenen:

1. **XSD-Validierung** (Struktur): kompiliert in jeden Schreibvorgang.
   `lxml.etree.XMLSchema` ist ausreichend.
2. **Schematron** (Geschäftsregeln): «Wenn `<spruchart>` = "urteil",
   dann muss `<dispositiv-urteil>` vorhanden sein.» «Wenn Streitwert
   > 30'000, dann ist Beschwerde in Zivilsachen zulässig.»
3. **Domänenprüfungen** (Custom Python/JS): Geschäftsnummer-Format
   gegen Kammer abgleichen, Datums-Plausibilität, Aktenstellen-Range.

### Empfehlung

XSD ab Tag 1, Schematron ab Phase 2 (sobald typische Fehler bekannt
sind), Custom-Checks als Sammelbecken für alles, was sich nicht in
Schematron ausdrücken lässt.

CI-Hook im Repo: jede `.xml` wird beim Commit gegen ihr Schema
geprüft, sonst Push-Verweigerung.

## 4 — Suche und Auswertung

### XPath/XQuery für strukturierte Anfragen

Direkt auf den XML-Files möglich (lxml). Beispiele:

- «Alle OGer-ZH-Strafurteile 2024 mit Streitwert > 100'000»
- «Welche BGE-Zitate werden in Strafkammer-Urteilen am häufigsten
  zitiert?»

### Volltextsuche

XML → JSON-Konversion → Elasticsearch oder Meilisearch. Felder werden
über XPath-Auszug gemappt. Mandanten-Trennung via Index-Aliase.

### Statistik / Reporting

Periodische Auswertung in Notebooks (Jupyter, marimo). Reports nach
HTML/PDF aus den Notebooks generieren.

## 5 — Ausgabe (XML → PDF/HTML/DOCX)

Aus dem XML lassen sich beliebige Ausgabeformate generieren:

| Ziel | Werkzeug |
|---|---|
| HTML (Webview) | XSLT 3.0 oder direkter Renderer in der Svelte-App |
| PDF (Akte/Versand) | XSL-FO (Apache FOP) ODER HTML+CSS → WeasyPrint |
| DOCX (Anwaltsbrief) | python-docx aus XML, mit kanzleieigener Vorlage |
| Klartext (E-Mail) | XSLT |

### Empfehlung

Für den Anfang: **HTML+CSS → WeasyPrint**. Dasselbe Stylesheet kann
sowohl die Web-Ansicht als auch die PDF-Generierung steuern. XSL-FO
ist mächtiger, aber Lernkurve.

Eine kanzleieigene Druckvorlage (Briefkopf, Adressfeld, Fußzeile)
einmal als HTML+CSS bauen, dann steht jede Rechtsschrift in
einheitlicher Form zur Verfügung.

## 6 — Migration des Bestands

Vorhandene Dokumente kommen aus drei Quellen:

1. **DOCX-Bestand** der Kanzlei: Konversion mit `python-docx` plus
   Stilvorlagen-Mapping (wenn vorhanden) plus LLM-Nachbearbeitung.
2. **PDF-Bestand**: OCR (wenn nötig) → LLM-Strukturierung gegen Schema.
3. **Crawl-Daten** (Lorentzo): HTML+JSON sind bereits semi-strukturiert,
   Mapping ins XML-Schema mit XSLT oder Python.

### Phasen

- **Phase A**: Migrations-Pipeline für Crawl-Daten zuerst (gut
  strukturiert, Testfall mit ~100 Dokumenten pro Instanz).
- **Phase B**: PDF-Bestand der Kanzlei (priorisiert nach Mandanten-
  relevanz).
- **Phase C**: Live-Erfassung neuer Dokumente.

## 7 — Workflow-Integration in der Kanzlei

### Aktenführung

XML-Dokument als Quelle der Wahrheit, Akte als Sammlung von XMLs +
Beilagen + Korrespondenz. Eine Akte hat eine `<aktenuebersicht>`-XML,
die alle Sub-Dokumente referenziert.

### Pre-Submission-Check

Vor Einreichung beim Gericht: automatischer Check
(Geschäftsnummer-Format, Frist-Plausibilität, Pflichtfelder, Beilagen
referenziert). Ergebnis als Checkliste im Web-UI.

### Anonymisierung

`<partei anonymisiert="true">` plus eine Schicht beim Export, die
Namen und Adressen ausblendet oder mit Platzhaltern ersetzt.
Anonymisierungsregeln im Schema dokumentiert (welche Felder, welcher
Platzhalter).

### Frist-Tracking

`<rechtsmittelbelehrung>` enthält Frist und Beginn. Worker rechnet
Fristen aus, schreibt in Kalender, alarmiert bei Annäherung.

## 8 — Schnittstellen und Standards

### Akoma Ntoso

OASIS LegalDocML — internationaler Standard. Für Interop sinnvoll, aber
im Vollumfang sehr umfangreich. **Vorschlag**: ein optionales
Akoma-Ntoso-Export-Mapping ergänzen (eigenes XML als Kanzlei-internes
Modell, Akoma Ntoso als Austausch-Format mit Drittparteien).

### Justitia 4.0 (CH)

Bundesweite Justizplattform-Initiative (Stand 2026: noch im Aufbau).
Format-Anforderungen sollten bei Schema-Erweiterungen mitgedacht
werden, sobald sie spezifiziert sind. Beobachten.

### BGer-Austauschformat

Das BGer publiziert Urteile als HTML/JSON. Mapping ins eigene Schema
ist unidirektional (BGer → wir), reicht aber für die Bestandsmigration.

## 9 — MVP / Phasenplan

Was ist die kleinste sinnvolle Version, die einen Mehrwert bringt?

### Phase 1 (1–2 Monate): Lesen und Validieren

- Schemas finalisieren (sind weitgehend da)
- Validierungs-Pipeline mit XSD
- Migration der Crawl-Daten als Testkorpus (~100 Dokumente pro Instanz)
- XPath-Auswertungen in Notebooks
- **Mehrwert**: Beweis, dass das Schema die reale Welt abbildet

### Phase 2 (2–4 Monate): Schreiben und Anzeigen

- LLM-assistierte PDF→XML-Konversion für die Kanzlei
- Web-Viewer (Svelte) mit Annotations- und Suchfunktion
- HTML→PDF-Pipeline für die Akte
- **Mehrwert**: erste Akten als XML, parallel zur DOCX-Welt

### Phase 3 (4–8 Monate): Erfassen und Validieren

- Form-basierter Editor (oder Word-Add-In, je nach Akzeptanz)
- Schematron-Regeln für typische Geschäftsregeln
- Pre-Submission-Check
- **Mehrwert**: produktive Erfassung, Qualitätssicherung

### Phase 4 (≥ 8 Monate): Statistik, Schnittstellen, Skalierung

- Suche / Statistik / KI-Integration
- Akoma-Ntoso-Export
- Mandanten-Self-Service-Portal

## Offene Fragen

- **Anwaltsgeheimnis und Cloud-LLM-Konversion**: PDF→XML via OpenAI/
  Anthropic? Lokales Modell (Llama, Mistral)? Hybrid mit
  Anonymisierung als Vorschritt?
- **Wer pflegt die Schemas?** Eine Person hauptverantwortlich, oder
  Schema-Änderungen via PR-Review?
- **Wie tief modellieren?** Schritt für Schritt erweitern oder eine
  einmalige Tiefenanalyse machen? Tendenz zu erstem (lebt mit der
  realen Datenbasis).
- **Mehrsprachigkeit**: BE, GE, TI, FR sind mehrsprachig. Schemas
  sprachneutral halten oder pro Sprache eigene Variante? Tendenz:
  ein Schema, `xml:lang` auf den Inhalts-Elementen.
- **Wer ist primärer Nutzer?** Eine einzelne Kanzlei (Lorentzo), eine
  Anwaltsgemeinschaft, oder ein potentielles Branchen-Tool? Beeinflusst
  Architektur und Lizenzmodell.

---

*Stand: 26.04.2026 · Diskussionsgrundlage, kein Beschluss.*
