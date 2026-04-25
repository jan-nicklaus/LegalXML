"""Generiert xml-vorteile.pdf — eine Drittpräsentation der Vorteile
strukturierter XML-Rechtsdokumente gegenüber PDF/DOCX."""
from pathlib import Path
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, ListFlowable, ListItem,
)
from reportlab.pdfgen import canvas

OUT = Path(__file__).parent / "xml-vorteile.pdf"

# --- Farben (zurückhaltend, professionell) ----------------------------
INK = HexColor("#1a1a1a")
MUTED = HexColor("#555555")
ACCENT = HexColor("#0b3d6b")        # tiefes Blau
ACCENT_LIGHT = HexColor("#e8eef5")
RULE = HexColor("#cccccc")

# --- Styles -----------------------------------------------------------
ss = getSampleStyleSheet()

H1 = ParagraphStyle(
    "H1", parent=ss["Heading1"],
    fontName="Helvetica-Bold", fontSize=22, leading=28,
    textColor=ACCENT, spaceAfter=4, spaceBefore=0,
)
H2 = ParagraphStyle(
    "H2", parent=ss["Heading2"],
    fontName="Helvetica-Bold", fontSize=14, leading=18,
    textColor=ACCENT, spaceAfter=6, spaceBefore=14,
)
H3 = ParagraphStyle(
    "H3", parent=ss["Heading3"],
    fontName="Helvetica-Bold", fontSize=11, leading=15,
    textColor=INK, spaceAfter=2, spaceBefore=8,
)
LEAD = ParagraphStyle(
    "Lead", parent=ss["BodyText"],
    fontName="Helvetica", fontSize=11, leading=16,
    textColor=MUTED, spaceAfter=8, alignment=TA_LEFT,
)
BODY = ParagraphStyle(
    "Body", parent=ss["BodyText"],
    fontName="Helvetica", fontSize=10, leading=14,
    textColor=INK, spaceAfter=6, alignment=TA_JUSTIFY,
)
BULLET = ParagraphStyle(
    "Bullet", parent=BODY,
    leftIndent=12, bulletIndent=0, spaceAfter=3,
)
SMALL = ParagraphStyle(
    "Small", parent=BODY, fontSize=9, leading=12, textColor=MUTED,
)
CALLOUT = ParagraphStyle(
    "Callout", parent=BODY, fontName="Helvetica-Bold",
    fontSize=11, leading=15, textColor=ACCENT,
    backColor=ACCENT_LIGHT, borderPadding=10,
    spaceBefore=8, spaceAfter=8, alignment=TA_LEFT,
)

# --- Header / Footer --------------------------------------------------
def page_decoration(canv: canvas.Canvas, doc):
    canv.saveState()
    width, height = A4

    # Header
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.4)
    canv.line(2*cm, height - 2*cm, width - 2*cm, height - 2*cm)
    canv.setFont("Helvetica", 8)
    canv.setFillColor(MUTED)
    canv.drawString(2*cm, height - 1.7*cm, "Strukturierte Rechtsdokumente — Argumentarium")
    canv.drawRightString(width - 2*cm, height - 1.7*cm, "Lorentzo")

    # Footer
    canv.line(2*cm, 2*cm, width - 2*cm, 2*cm)
    canv.setFont("Helvetica", 8)
    canv.setFillColor(MUTED)
    canv.drawString(2*cm, 1.6*cm, date.today().strftime("%-d. %B %Y"))
    canv.drawRightString(width - 2*cm, 1.6*cm, f"Seite {doc.page}")
    canv.restoreState()


# --- Inhalt -----------------------------------------------------------
story = []

# Titelblock
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("XML statt PDF/DOCX", H1))
story.append(Paragraph("Wieso strukturierte Rechtsdokumente?", LEAD))
story.append(Spacer(1, 4))

# Kurzes Lead
story.append(Paragraph(
    "Die Frage ist nicht «XML ja oder nein» — DOCX ist intern ebenfalls XML "
    "(ein ZIP-Container mit Office Open XML), und auch PDF lässt sich mit "
    "XML-Beilagen anreichern. Die Frage ist, <b>welches XML / welches "
    "Datenmodell</b> zur Aufgabe passt.",
    BODY,
))
story.append(Paragraph(
    "PDF beschreibt Pixel und Glyphen auf einer Seite. DOCX beschreibt "
    "Textverarbeitungs-Layout (Absatz, Stilvorlage, Schriftart). Ein "
    "<i>domänenspezifisches XML</i> für Rechtsdokumente beschreibt die Sache "
    "selbst: Geschäftsnummer ist eine Geschäftsnummer, eine Erwägung ist eine "
    "Erwägung, ein Verweis auf <i>Art. 18 OR</i> ist eine Norm-Referenz.",
    BODY,
))
story.append(Paragraph(
    "Erst dieses domänenspezifische Modell ermöglicht die Vorteile, die in der "
    "Kanzlei wie in der Justizverwaltung unmittelbar wirken — von der "
    "Qualitätssicherung über die Statistik bis zur Langzeitarchivierung.",
    BODY,
))

# Sinn und Zweck (Motivation)
story.append(Paragraph("Sinn und Zweck", H2))
story.append(Paragraph(
    "Rechtsschriften und Urteile bestehen mehrheitlich aus Text. Im Verlauf "
    "eines Verfahrens werden diese Texte zwischen den Beteiligten ausgetauscht; "
    "es wird wechselseitig auf sie Bezug genommen — und zwar nicht auf "
    "beliebige Stellen, sondern auf solche, die einen engeren inhaltlichen "
    "Bezug haben. Sachverhaltselemente korrespondieren mit anderen "
    "Sachverhaltselementen, rechtliche Argumente werden gegenüber anderen "
    "rechtlichen Argumenten erwidert.",
    BODY,
))
story.append(Paragraph(
    "Für diesen Austausch eignen sich strukturierte Daten. Dabei ist "
    "unerheblich, ob die Daten originär strukturiert entstehen oder ob sie "
    "aus anderen Formaten wie PDF abgeleitet werden. Entscheidend ist, dass "
    "die typischen Bezüge maschinell nachvollziehbar werden — und damit auch, "
    "dass die Strukturierung <b>bewusst minimal</b> ausgestaltet wird: gerade "
    "so präzise wie nötig, nicht so detailliert wie möglich.",
    BODY,
))
story.append(Paragraph(
    "Hinzu kommt, dass Rechtsschriften regelmässig auf <i>externe Ressourcen</i> "
    "verweisen — Beweismittel, Akten, Urkunden, Gutachten —, die ihrerseits in "
    "unterschiedlichen Formaten vorliegen. Auch solche Verweise müssen "
    "strukturiert abgebildet werden, damit sie sich automatisch auflösen lassen.",
    BODY,
))

# Vergleich-Tabelle
story.append(Spacer(1, 8))
story.append(Paragraph("Drei Formate auf einen Blick", H2))

tbl_data = [
    ["", "PDF", "DOCX", "Domänen-XML"],
    ["Modelliert",            "Pixel / Glyphen",    "Textverarbeitung (XML)",  "Juristische Inhalte"],
    ["Schema",                "—",                  "OOXML (Layout)",          "Eigen (Geschäftsnummer, Erwägung, …)"],
    ["Was validierbar ist",   "—",                  "Layout-Struktur",         "Pflichtfelder, Formate"],
    ["Maschinell auswertbar", "Nur über OCR",       "Über Stilvorlagen",       "Direkt, eindeutig"],
    ["Versionssichtbar",      "Nein",               "Binär (ZIP)",             "Zeile für Zeile"],
    ["Langzeitlesbar",        "Versionsabhängig",   "OOXML offen, breit",      "Offen, schmal"],
]
tbl = Table(tbl_data, colWidths=[3.8*cm, 3.4*cm, 4.2*cm, 4.8*cm])
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
    ("TEXTCOLOR",  (0, 0), (-1, 0), white),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME",   (0, 1), (0, -1), "Helvetica-Bold"),
    ("FONTNAME",   (-1, 1), (-1, -1), "Helvetica-Bold"),  # XML-Spalte hervorheben
    ("TEXTCOLOR",  (-1, 1), (-1, -1), ACCENT),
    ("FONTSIZE",   (0, 0), (-1, -1), 9),
    ("LEADING",    (0, 0), (-1, -1), 12),
    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN",      (1, 1), (-1, -1), "LEFT"),
    ("LEFTPADDING",  (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING",   (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f7f7f7")]),
    ("LINEBELOW", (0, 0), (-1, 0), 0.6, ACCENT),
    ("BOX",       (0, 0), (-1, -1), 0.4, RULE),
]))
story.append(tbl)
story.append(Spacer(1, 6))

# Kernaussage
story.append(Paragraph(
    "Wer Rechtsdokumente nicht nur drucken, sondern auch <i>auswerten, "
    "wiederverwenden und maschinell prüfen</i> möchte, braucht ein "
    "domänenspezifisches Datenformat — nicht nur ein Layout- oder "
    "Textverarbeitungs-Format.",
    CALLOUT,
))

# Warum PDF und DOCX nicht reichen
story.append(Paragraph("Warum PDF und DOCX nicht reichen", H2))
story.append(Paragraph(
    "PDF ist das Standardformat für die Übergabe von Rechtsschriften und "
    "Urteilen, DOCX das Standardformat für ihre Erstellung. Beide haben für "
    "die maschinelle Weiterverarbeitung systematische Schwächen — wenn auch "
    "unterschiedliche.",
    BODY,
))

story.append(Paragraph("PDF — Layout statt Inhalt", H3))
pdf_schwaechen = [
    ("Doppelte Schichten — Textlayer und Bildlayer",
     "Sogenannte «Sandwich-PDFs» enthalten ein Bild des Originals und eine "
     "darunterliegende, automatisch erkannte Textschicht. Die Qualität dieser "
     "Textschicht hängt vom OCR-Verfahren ab; Diskrepanzen zwischen sichtbarem "
     "Bild und auswertbarem Text bleiben in der Regel unbemerkt."),
    ("Darstellung im Vordergrund, Inhalt im Hintergrund",
     "PDF beschreibt, wo Glyphen auf der Seite stehen — nicht, was sie "
     "bedeuten. Die Information «das ist Erwägung Nr. 3» ergibt sich nur aus "
     "visuellen Hinweisen wie Einrückung und Nummerierung. Diese Hinweise "
     "müssen maschinell rekonstruiert werden und variieren je nach Verfasserin."),
    ("Unschärfe in der Spezifikation",
     "PDF ist ein umfangreicher Standard, in dem dieselbe Information auf "
     "vielfältige Weise dargestellt werden kann. Eine inhaltliche Validierung — "
     "stimmt das Format der Geschäftsnummer, ist die Rechtsmittelbelehrung "
     "vorhanden — ist nicht vorgesehen."),
    ("Hoher Metadaten-Anteil",
     "PDF bringt eigene Metadaten mit (eingebettete Schriftarten, Formularfelder, "
     "Sicherheitseinstellungen, Rendering-Hinweise), die für die juristische "
     "Auswertung irrelevant sind, aber beim Verarbeiten mitgeführt werden müssen."),
]
for titel, text in pdf_schwaechen:
    story.append(KeepTogether([
        Paragraph("• " + titel, BULLET),
        Paragraph(text, BODY),
    ]))

story.append(Spacer(1, 4))
story.append(Paragraph("DOCX — XML, aber das falsche", H3))
story.append(Paragraph(
    "DOCX ist seit Office 2007 ein ZIP-Container mit XML-Dateien (Office Open "
    "XML, ECMA-376). Es ist also bereits ein XML-Format — aber eines, das die "
    "<i>Textverarbeitung</i> beschreibt, nicht die <i>Sache</i>:",
    BODY,
))

docx_schwaechen = [
    ("Generisches Layout-Modell",
     "Das DOCX-Schema kennt Konzepte wie «Absatz», «Stilvorlage», «Tabelle» — "
     "nicht aber «Erwägung», «Geschäftsnummer» oder «Rechtsbegehren». Die "
     "juristische Bedeutung muss über Stilvorlagen-Konventionen hilfsweise "
     "annotiert werden, was selten konsequent gelingt."),
    ("Validierung greift zu kurz",
     "Das OOXML-Schema validiert die Textverarbeitungs-Struktur (existieren "
     "alle Tags korrekt?), nicht den juristischen Inhalt (hat der Schriftsatz "
     "ein Rechtsbegehren? entspricht die Geschäftsnummer dem BGer-Format?)."),
    ("ZIP-Container — nicht direkt diff-bar",
     "Eine .docx ist ein gepacktes Archiv. Versionskontrollsysteme zeigen nur, "
     "dass sich «irgendetwas geändert hat», nicht <i>was</i>. Erst nach dem "
     "Entpacken liesse sich der Unterschied auf XML-Ebene lesen."),
]
for titel, text in docx_schwaechen:
    story.append(KeepTogether([
        Paragraph("• " + titel, BULLET),
        Paragraph(text, BODY),
    ]))

# Sieben Hauptvorteile
story.append(Paragraph("Sieben praktische Vorteile", H2))

vorteile = [
    ("Maschinelle Auswertbarkeit ohne Heuristik",
     "Ein einziger Such-Ausdruck genügt für Anfragen wie: <i>«Alle Strafurteile "
     "der I. Strafkammer 2024 mit Streitwert über 100 000 CHF, in denen Art. 18 OR "
     "zitiert wird»</i>. Bei PDF braucht es OCR und Mustererkennung — bei DOCX "
     "diszipliniert verwendete Stilvorlagen, was selten gegeben ist."),

    ("Verlustfreie semantische Beziehungen",
     "Vorinstanz, Weiterzug, BGE-Zitate, Aktenreferenzen — all das sind im XML "
     "explizite Relationen. Daraus lassen sich Instanzenzüge nachzeichnen, "
     "Zitiernetzwerke aufbauen und Präjudizien-Karten erstellen. PDF kennt nur "
     "Text «BGE 145 III 365» — ohne Verknüpfung zu einer Datenbank."),

    ("Validierung vor dem Versand",
     "Ein XML-Schema prüft beim Erstellen: Stimmt das Format der "
     "Geschäftsnummer? Hat das Dispositiv eine Ziffer? Ist die Rechtsmittel"
     "belehrung vollständig? Fehler werden im Anwaltsbüro entdeckt — nicht "
     "vom Gericht zurückgewiesen."),

    ("Mehrere Darstellungen aus einer Quelle",
     "Eine XML-Datei lässt sich in beliebige Ausgabeformate transformieren: "
     "PDF für die Akte, HTML für die Webansicht, JSON für die Suchmaschine, "
     "Klartext für die E-Mail. Bei PDF/DOCX als Quelle ist jede Konvertierung "
     "Datenverlust und manuelles Re-Layout."),

    ("Versionierung mit Diff-Sinn",
     "Eine Änderung im XML zeigt klar: «Erwägung 3.2 wurde umformuliert». "
     "DOCX-Versionsvergleiche zeigen Binärdaten oder unbrauchbare Markups; "
     "PDFs sind in der Regel gar nicht versioniert."),

    ("Anonymisierung als Datenfeld",
     "Im XML ist Anonymisierung ein Attribut: <i>partei anonymisiert=\"true\"</i>. "
     "Das ist gezielt steuerbar — etwa: Vornamen ausblenden, Geschäftsnummer "
     "anzeigen. Bei PDF-Schwärzungstools sind Datenpannen mit unsichtbar "
     "gemachtem, aber technisch noch lesbarem Text bekannt geworden."),

    ("Stabile Anker für Querverweise",
     "Jede Erwägung kann eine eindeutige ID tragen. Verweise und Deep-Links "
     "überleben jede Textänderung. PDF-Anker basieren auf Seitennummern und "
     "brechen, sobald das Dokument neu umgebrochen wird."),
]

for i, (titel, text) in enumerate(vorteile, 1):
    story.append(KeepTogether([
        Paragraph(f"{i}. {titel}", H3),
        Paragraph(text, BODY),
    ]))

# Seitenumbruch vor weiteren Argumenten
story.append(PageBreak())

# Strategischer Mehrwert
story.append(Paragraph("Strategischer Mehrwert", H2))

story.append(Paragraph(
    "Die genannten Vorteile sind operativ. Die strategischen Vorteile gehen weiter:",
    BODY,
))

strategisch = [
    ("Statistische Auswertbarkeit über Korpora",
     "Wer seine Urteile als XML hat, kann Fragen beantworten wie «Wie hat sich das "
     "durchschnittliche Strafmass für Tatbestand X von 2018 bis 2024 entwickelt?» — "
     "ohne Zukauf von Heuristik-Tools, die heute kommerzielle Anbieter auf "
     "PDF-Stapel anwenden."),

    ("KI-Tauglichkeit",
     "Ein gut strukturiertes XML-Korpus ist hochwertige Trainingsgrundlage für "
     "anwaltliche und gerichtliche KI-Anwendungen. Eine PDF-Sammlung ist Rohmaterial "
     "mit hohem Aufbereitungsaufwand."),

    ("Anschluss an eJustiz-Standards",
     "Das Bundesgericht und internationale Initiativen (Akoma Ntoso, LegalDocML) "
     "arbeiten an XML-basierten Austauschformaten. Wer seine Dokumente bereits "
     "strukturiert führt, ist bei jeder zukünftigen Schnittstelle anschlussfähig."),

    ("Langzeitarchivierung",
     "XML ist offen, textbasiert und in 30 Jahren noch lesbar — ohne proprietäre "
     "Software. DOCX-Dokumente sind an Microsoft-Versionen gebunden, PDFs "
     "an die Spezifikation des jeweiligen Erstellungsjahres."),

    ("Konsistente Formvorlagen kanzleiweit",
     "Ein Schema erzwingt Pflichtfelder. Damit gibt es keine «vergessene "
     "Rechtsmittelbelehrung» und keine «falsch zitierte Geschäftsnummer» mehr — "
     "weder bei Junior-Mitarbeitenden noch unter Zeitdruck."),
]

for titel, text in strategisch:
    story.append(KeepTogether([
        Paragraph(titel, H3),
        Paragraph(text, BODY),
    ]))

# Was XML nicht ist
story.append(Spacer(1, 8))
story.append(Paragraph("Was XML nicht ist", H2))

story.append(Paragraph(
    "XML ersetzt PDF und DOCX nicht in jedem Anwendungsfall. Realistische "
    "Einschränkungen:",
    BODY,
))

einschr = [
    "<b>Kein Lesedokument.</b> Roh-XML liest niemand gern. Es braucht einen Viewer "
    "oder eine generierte HTML/PDF-Ansicht.",
    "<b>Kein Schreibwerkzeug.</b> Anwälte tippen nicht in Tags. Es braucht einen "
    "Editor, der XML im Hintergrund erzeugt — vergleichbar zu Word, das DOCX "
    "schreibt, ohne dass die Verfasserin den XML-Inhalt sieht.",
    "<b>Kein Layout-Format.</b> Für die endgültige Akte und den Briefkopf wird "
    "weiterhin PDF gebraucht — aber <i>generiert aus XML</i>, nicht als Quelle.",
    "<b>Kein Allheilmittel für bildhafte Beilagen.</b> Pläne, Fotos, "
    "Bildgutachten bleiben PDF-Anhänge.",
]
for s in einschr:
    story.append(Paragraph("• " + s, BULLET))

# Faustregel
story.append(Spacer(1, 6))
story.append(Paragraph("Faustregel", H2))
story.append(Paragraph(
    "XML ist das <b>Quellformat</b>. PDF und DOCX sind <b>Ausgabeformate</b>, "
    "die aus dem Quellformat generiert werden.",
    CALLOUT,
))
story.append(Paragraph(
    "Damit hat man strukturierte Daten für alle maschinellen Anwendungsfälle "
    "(Suche, Statistik, KI, Archivierung, Validierung) — und gewohntes Layout "
    "für die Akte und den Anwaltsbrief.",
    BODY,
))

# Schluss / Kontakt
story.append(Spacer(1, 14))
story.append(Paragraph(
    "Eine vertiefte technische Darstellung sowie konkrete Schema-Vorschläge "
    "für Bundesgericht, Obergerichte (Zürich, Bern), Kantonsgericht Luzern und "
    "Appellationsgericht Basel-Stadt liegen im LegalXML-Repository auf Anfrage vor.",
    SMALL,
))


# --- Build ------------------------------------------------------------
doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.6*cm, bottomMargin=2.4*cm,
    title="Strukturierte Rechtsdokumente — Argumentarium",
    author="Lorentzo",
    subject="Vorteile von XML gegenüber PDF/DOCX bei Rechtsdokumenten",
)

doc.build(story, onFirstPage=page_decoration, onLaterPages=page_decoration)
print(f"Geschrieben: {OUT}")
