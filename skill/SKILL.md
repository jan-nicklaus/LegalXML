---
name: legal-xml-converter
description: >
  Konvertiert Schweizer Rechtsdokumente (Rechtsschriften und Gerichtsentscheide) in ein
  standardisiertes XML-Format und analysiert inhaltliche Bezüge zwischen zwei Dokumenten.
  Verwende diesen Skill immer wenn: (1) der Benutzer ein oder zwei Rechtsdokumente hochlädt
  und eine XML-Konvertierung wünscht, (2) eine Rechtsschrift und ein Entscheid verglichen
  oder verknüpft werden sollen, (3) ref-Attribute zwischen zwei juristischen Dokumenten
  gesetzt werden sollen, (4) ein amtliches Bundesgerichts-XML erstellt werden soll,
  (5) Begriffe wie "Rechtsschrift", "Entscheid", "Beschwerde", "Dispositiv", "Rubrum",
  "Erwägungen" oder "Konvertierung" im Kontext von Rechtsdokumenten fallen.
  Auch triggern bei: "in XML umwandeln", "Verknüpfung zwischen Dokumenten", "ref setzen",
  "Absätze verlinken", "Dokumentenanalyse Gericht".
---

# Legal XML Converter

Dieser Skill konvertiert Schweizer Rechtsdokumente (Rechtsschriften und Gerichtsentscheide)
in ein standardisiertes XML-Format, vergibt eindeutige IDs und analysiert inhaltliche
Bezüge zwischen zwei Dokumenten.

## Schnellübersicht

1. **Eingabe einlesen** → Dateityp erkennen, Inhalt extrahieren
2. **Dokumenttyp bestimmen** → `rechtsschrift` oder `entscheid`
3. **UUID-Register aufbauen** → Python-Skript generiert alle IDs vorab; bildet Mapping alter→neuer IDs
4. **XML-Struktur aufbauen** → Schema anwenden, UUIDs aus Register einsetzen
5. **ref-Analyse** → Bezüge erkennen; nur validierte IDs aus dem Register verwenden
6. **Output** → 2 XML-Dateien

---

## Schritt 1: Dateien einlesen

Unterstützte Formate: **HTML, XML, PDF, DOCX, TXT**

### Vorgehen nach Dateityp

| Format | Methode |
|--------|---------|
| HTML/XML | Direkt parsen; vorhandene Tags als Strukturhinweise nutzen |
| PDF | `pdftotext` oder Python `pdfplumber`; Textblöcke extrahieren |
| DOCX | Python `python-docx`; Absätze und Überschriften extrahieren |
| TXT | Zeilenweise einlesen; Struktur aus Einrückung/Leerzeilen ableiten |

Bei **PDF und DOCX**: Lies zuerst `/mnt/skills/public/pdf-reading/SKILL.md` bzw. `/mnt/skills/public/file-reading/SKILL.md` für detaillierte Anweisungen.

---

## Schritt 2: Dokumenttyp erkennen

Bestimme automatisch, ob es sich um eine **Rechtsschrift** (Parteidokument) oder einen **Entscheid** (Gerichtsdokument) handelt.

### Erkennungsregeln (in Prioritätsreihenfolge)

1. **XML-Attribut vorhanden**: `doctype="rechtsschrift"` oder `doctype="entscheid"` → direkt verwenden
2. **Schlüsselwörter im Titel/Header**:
   - Rechtsschrift: „Beschwerde", „Berufung", „Klage", „Rekurs", „Rechtsschrift", „Eingabe", „beantragt"
   - Entscheid: „Urteil", „Beschluss", „Verfügung", „Entscheid", „erkennt", „Das Gericht"
3. **Strukturmerkmale**:
   - Rechtsschrift: enthält Rechtsbegehren/Anträge in Ich/Wir-Form, Parteibehauptungen, keine `<Eroeffnung>`
   - Entscheid: enthält `<Eroeffnung>`, Zusammensetzung des Gerichts (`<Kammer>`, `<Mitglied>`), Entscheid-Block
4. **Verfasser**: Anwalt/Partei → Rechtsschrift; Gericht → Entscheid

Vermerke den erkannten Typ kurz im Chat (eine Zeile), bevor du weitermachst.

---

## Schritt 3: UUID-Register aufbauen (ZWINGEND VOR XML-Erstellung)

**Führe dieses Python-Skript aus, bevor du irgendeinen XML-Inhalt schreibst.** Es generiert alle UUIDs zentral und stellt sicher, dass `ref`-Attribute ausschliesslich auf existierende IDs zeigen.

```python
import uuid, json, re

def build_uuid_registry(doc1_absatz_count, doc2_absatz_count,
                        doc1_dispositiv_count, doc2_dispositiv_count,
                        doc1_partei_count, doc1_attachment_count):
    """
    Generiert alle UUIDs vorab und gibt ein Registry-Dict zurück.
    Elemente in Dok 1 (Rechtsschrift): Parteien, DispositivZiffern, Absätze, Attachments
    Elemente in Dok 2 (Entscheid): Parteien (gleiche wie Dok1!), DispositivZiffern, Absätze
    """
    registry = {
        # Dok 1
        "doc1_parteien": [str(uuid.uuid4()) for _ in range(doc1_partei_count)],
        "doc1_dispositiv": [str(uuid.uuid4()) for _ in range(doc1_dispositiv_count)],
        "doc1_absaetze": [str(uuid.uuid4()) for _ in range(doc1_absatz_count)],
        "doc1_attachments": [str(uuid.uuid4()) for _ in range(doc1_attachment_count)],
        # Dok 2 (Parteien-IDs identisch mit Dok 1, da gleiche Personen)
        "doc2_dispositiv": [str(uuid.uuid4()) for _ in range(doc2_dispositiv_count)],
        "doc2_absaetze": [str(uuid.uuid4()) for _ in range(doc2_absatz_count)],
    }
    # Validierungsset: alle gültigen Ziel-IDs für ref-Attribute
    registry["valid_ref_targets"] = set(registry["doc1_absaetze"])
    return registry

# Beispielaufruf – Zahlen an das konkrete Dokument anpassen:
reg = build_uuid_registry(
    doc1_absatz_count=9,   # Anzahl <Absatz> in Rechtsschrift
    doc2_absatz_count=6,   # Anzahl <Absatz> in Entscheid
    doc1_dispositiv_count=5,
    doc2_dispositiv_count=2,
    doc1_partei_count=2,
    doc1_attachment_count=7
)

def make_ref(ids: list[str], registry: dict) -> str | None:
    """
    Erstellt ein valides ref-Attribut. Wirft einen Fehler wenn eine ID
    nicht im valid_ref_targets-Set existiert (verhindert Phantomreferenzen).
    Gibt None zurück wenn die Liste leer ist.
    """
    for id_ in ids:
        if id_ not in registry["valid_ref_targets"]:
            raise ValueError(f"UNGÜLTIGE REF-ID: {id_} existiert nicht in Dok 1!")
    return ",".join(ids) if ids else None

print(json.dumps({k: v for k, v in reg.items() if k != "valid_ref_targets"}, indent=2))
```

**Wichtig**: Weise den Absätzen die UUIDs aus dem Register **in der Reihenfolge** zu, in der sie im Dokument erscheinen. Nutze `reg["doc1_absaetze"][0]` für den ersten Absatz, `[1]` für den zweiten usw. So bleibt die Zuordnung deterministisch und nachvollziehbar.

## Schritt 4: XML aufbauen

### Vollständiges Schema

Detaillierte Schema-Referenz: `references/schema.md`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Dok doctype="[rechtsschrift|entscheid]">

  <Rubrum>
    <Verfahren>
      <Aktenzeichen/>           <!-- z.B. 6B_650/2025 -->
      <Parteien>
        <Partei id="[UUID]">
          <Rollen><Rolle/></Rollen>    <!-- Beschwerdeführer, Beschwerdegegnerin etc. -->
          <Name/>
          <Anschrift/>
          <Stellvertretung/>
          <Rechtsvertretung/>
        </Partei>
      </Parteien>
      <Vorinstanz>              <!-- NUR bei Rechtsschrift -->
        <Name/>
        <Anschrift/>
      </Vorinstanz>
    </Verfahren>
    <Dokument>
      <DokumentUeberschrift/>  <!-- Urteil, Beschluss etc. -->
      <Datum/>                 <!-- ISO 8601: YYYY-MM-DD -->
      <Spruchkoerper>
        <Gericht/>
        <Adresse/>
        <Kammer/>              <!-- NUR bei Entscheid -->
        <Zusammensetzung>      <!-- NUR bei Entscheid -->
          <Mitglied role="[presiding judge|judge|clerk]"/>
        </Zusammensetzung>
      </Spruchkoerper>
    </Dokument>
  </Rubrum>

  <Main>
    <Dispositiv>
      <DispositivZiffer
        id="[UUID]"
        type="[hauptsache|hauptsache-eventualiter|kosten]"/>
    </Dispositiv>

    <Eroeffnung>               <!-- NUR bei Entscheid -->
      <!-- adrid verweist auf Partei-ID, adrname für externe Empfänger -->
      <EroeffnungZiffer adrid="[Partei-UUID]"/>
      <EroeffnungZiffer adrname="[Freitext]"/>
    </Eroeffnung>

    <Begruendung>
      <Prozessuales>
        <Section>
          <Absatz id="[UUID]" [tag="facts|legal"] [ref="[UUID in Dok1]"]/>
        </Section>
      </Prozessuales>

      <Formelles>
        <Section>
          <Absatz id="[UUID]" [tag="facts|legal"] [ref="[UUID in Dok1]"]/>
        </Section>
      </Formelles>

      <Ruegegruende>           <!-- NUR bei Rechtsschrift -->
        <Section>
          <Absatz id="[UUID]"/>
        </Section>
      </Ruegegruende>

      <Materielles>
        <Section type="ruege" title="[Titel der Rüge]">
          <Absatz id="[UUID]" [tag="facts|legal"] [ref="[UUID in Dok1]"]/>
        </Section>
      </Materielles>
    </Begruendung>

    <Entscheid/>               <!-- NUR bei Entscheid: Kurzfassung der Entscheidbegründung -->

    <Postfix/>                 <!-- NUR bei Rechtsschrift: Abschlussformel -->

  </Main>

  <Attachments>                <!-- NUR bei Rechtsschrift -->
    <Attachment id="[UUID]"/>  <!-- Freitext: Beilagenbezeichnung -->
  </Attachments>

</Dok>
```

### ID-Vergabe (ZWINGEND via Registry aus Schritt 3)

- **Alle** folgenden Elemente erhalten eine UUID v4 aus dem Registry: `<Partei>`, `<DispositivZiffer>`, `<Absatz>`, `<Attachment>`
- UUIDs werden **immer neu generiert** – bestehende IDs aus Quelldokumenten werden nicht übernommen
- **Parteien-IDs** sind in Dok 1 und Dok 2 identisch (dieselben Personen), d.h. `reg["doc1_parteien"]` wird für beide Dokumente verwendet
- Format: `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx` (Standard UUID v4)

### Strukturelle Unterschiede Rechtsschrift vs. Entscheid

| Element | Rechtsschrift | Entscheid |
|---------|--------------|-----------|
| `<Vorinstanz>` | ✅ Pflicht | ❌ Nicht vorhanden |
| `<Kammer>` / `<Zusammensetzung>` | ❌ | ✅ Pflicht |
| `<Eroeffnung>` | ❌ | ✅ Pflicht |
| `<Ruegegruende>` | ✅ | ❌ |
| `<Entscheid>` (Block) | ❌ | ✅ |
| `<Postfix>` | ✅ | ❌ |
| `<Attachments>` | ✅ | ❌ |
| `ref`-Attribute auf `<Absatz>` | ❌ (Quelle) | ✅ (verweist auf Rechtsschrift) |

### tag-Attribut auf `<Absatz>`

| Wert | Bedeutung |
|------|-----------|
| `facts` | Sachverhaltsdarstellung, prozessuale Geschichte |
| `legal` | Rechtliche Ausführungen, Normzitate, Erwägungen |
| *(weggelassen)* | Nicht eindeutig klassifizierbar |

---

## Schritt 5: ref-Analyse

Dieser Schritt läuft **nur wenn zwei Dokumente** übergeben wurden.

### Grundregeln (nicht verhandelbar)

1. `ref`-Attribute erscheinen **ausschliesslich in Dok 2** (Entscheid)
2. `ref`-Werte dürfen **ausschliesslich IDs aus `reg["doc1_absaetze"]`** enthalten — niemals IDs aus Dok 2 oder andere Werte
3. Validierung mit `make_ref()` aus dem Registry-Skript ist **Pflicht** — ungültige IDs werden abgefangen
4. **Kein Report** — setze refs direkt nach bestem Ermessen

### Analysemethodik

Für jeden Absatz in Dok 2:
1. Extrahiere die **Kernaussage** (Rechtsfrage, Normzitate, Sachverhaltsbehauptung, Beträge, Daten)
2. Vergleiche mit **allen** Absätzen in Dok 1
3. Bewerte nach diesen Kriterien:

| Kriterium | Gewichtung | Beispiel |
|-----------|-----------|---------|
| Identische Normzitate | Hoch (0.35) | Beide zitieren Art. 135 Abs. 3 StPO |
| Gleiche Rechtsfrage | Hoch (0.30) | Beide behandeln Kognition der Vorinstanz |
| Gleiche Sachverhaltsbehauptung | Mittel (0.20) | Beide nennen denselben Betrag / dasselbe Datum |
| Gleicher Beschwerdeführer-Vortrag | Tief (0.10) | Entscheid gibt Parteibegehren wieder |
| Semantische Ähnlichkeit | Variabel (0.05) | Ähnliche Formulierung ohne direkten Normzitat-Match |

**Score** = gewichtete Summe (0.0 – 1.0). Setze `ref` wenn Score ≥ 0.50.

### Mehrfachbezüge

- Ein Absatz in Dok 2 kann auf **mehrere** Absätze in Dok 1 verweisen → kommagetrennte UUIDs: `ref="uuid1,uuid2,uuid3"`
- Derselbe Absatz in Dok 1 kann von **mehreren** Absätzen in Dok 2 referenziert werden — das ist korrekt und erwünscht
- Sei **präzise**: Setze nur refs, die inhaltlich tatsächlich begründet sind. Lieber weniger als zu viele.

### ref-Attribut-Format

```xml
<!-- Einzelner Bezug -->
<Absatz id="[dok2-uuid]" ref="[dok1-uuid]">...</Absatz>

<!-- Mehrere Bezüge (kommagetrennt, keine Leerzeichen) -->
<Absatz id="[dok2-uuid]" ref="[dok1-uuid-1],[dok1-uuid-2]">...</Absatz>
```

### Validierungsschritt vor XML-Ausgabe

```python
# Vor dem Schreiben der Entscheid-XML: alle geplanten refs validieren
planned_refs = {
    reg["doc2_absaetze"][2]: [reg["doc1_absaetze"][0], reg["doc1_absaetze"][3]],
    reg["doc2_absaetze"][4]: [reg["doc1_absaetze"][1]],
    # ... etc.
}
for doc2_id, doc1_ids in planned_refs.items():
    ref_str = make_ref(doc1_ids, reg)  # wirft ValueError bei ungültiger ID
    print(f"OK: {doc2_id} → {ref_str}")
```

---

## Schritt 6: Output erstellen

### Datei 1 & 2: XML-Dateien

- Dateiname: `[aktenzeichen]_rechtsschrift.xml` und `[aktenzeichen]_entscheid.xml`
- Encoding: UTF-8
- Wohlgeformtes XML (valide öffnende/schliessende Tags)
- Alle Kommentare aus Quelldokumenten weglassen
- Kein separater Report — refs werden direkt und nach bestem Ermessen gesetzt

---

## Wichtige Hinweise

- **Anonymisierung**: Namen wie `B.________` oder `■■■■■■` im Quelldokument werden unverändert übernommen
- **Leerelemente**: Elemente ohne Inhalt (`<Anschrift/>`) werden als leere Tags ausgegeben, nicht weggelassen
- **Zwischentitel** (`<b>...</b>`, `<br/>`) in Quelldokumenten werden als Fliesstext in den umliegenden `<Absatz>` integriert oder als eigener `<Absatz>` ohne ID aufgenommen – sie verändern die Hierarchie nicht
- **Mehrfachbezüge**: Ein `<Absatz>` in Dok 2 kann mehrere Absätze in Dok 1 referenzieren (kommagetrennt, keine Leerzeichen). Derselbe Dok-1-Absatz darf von mehreren Dok-2-Absätzen referenziert werden.
- **Richtung**: `ref` zeigt **immer** vom Entscheid (Dok 2) zur Rechtsschrift (Dok 1) — niemals umgekehrt, niemals auf eigene IDs
- **Referenzvalidierung**: Jede ID in einem `ref`-Attribut muss in `reg["valid_ref_targets"]` vorhanden sein. Die `make_ref()`-Funktion erzwingt dies. Phantomreferenzen (IDs, die nirgends existieren) sind ein kritischer Fehler.
- **Präzision**: Setze refs nur wenn ein echter inhaltlicher Bezug besteht. Zu viele refs sind schlimmer als zu wenige.
