"""Generiert xml-vorteile.pdf — Argumentarium für ein strukturiertes
Scharnierformat zum Abgleich von Rechtsdokumenten."""
from pathlib import Path
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfgen import canvas

OUT = Path(__file__).parent / "xml-vorteile.pdf"

# --- Farben -----------------------------------------------------------
INK = HexColor("#1a1a1a")
MUTED = HexColor("#555555")
ACCENT = HexColor("#0b3d6b")
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
LEAD = ParagraphStyle(
    "Lead", parent=ss["BodyText"],
    fontName="Helvetica", fontSize=11, leading=16,
    textColor=MUTED, spaceAfter=8, alignment=TA_LEFT,
)
BODY = ParagraphStyle(
    "Body", parent=ss["BodyText"],
    fontName="Helvetica", fontSize=10.5, leading=15,
    textColor=INK, spaceAfter=8, alignment=TA_JUSTIFY,
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

    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.4)
    canv.line(2*cm, height - 2*cm, width - 2*cm, height - 2*cm)
    canv.setFont("Helvetica", 8)
    canv.setFillColor(MUTED)
    canv.drawString(2*cm, height - 1.7*cm, "Strukturierte Rechtsdokumente — Argumentarium")
    canv.drawRightString(width - 2*cm, height - 1.7*cm, "Lorentzo")

    canv.line(2*cm, 2*cm, width - 2*cm, 2*cm)
    canv.setFont("Helvetica", 8)
    canv.setFillColor(MUTED)
    canv.drawString(2*cm, 1.6*cm, date.today().strftime("%-d. %B %Y"))
    canv.drawRightString(width - 2*cm, 1.6*cm, f"Seite {doc.page}")
    canv.restoreState()


# --- Inhalt -----------------------------------------------------------
story = []

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Strukturierte Rechtsdokumente", H1))
story.append(Paragraph(
    "XML als Scharnier für den Abgleich von Rechtsdokumenten "
    "(Entscheide und Rechtsschriften)",
    LEAD,
))

story.append(Paragraph("Sinn und Zweck — wieso ein strukturiertes Scharnierformat?", H2))

story.append(Paragraph(
    "Rechtsschriften und Urteile bestehen mehrheitlich aus Text. Im Verlauf "
    "eines Verfahrens werden diese Texte zwischen den Beteiligten ausgetauscht; "
    "es wird wechselseitig auf Textteile Bezug genommen — und zwar nicht auf "
    "beliebige Stellen, sondern auf solche, die einen engeren inhaltlichen "
    "Bezug haben. Sachverhaltselemente korrespondieren mit anderen "
    "Sachverhaltselementen, rechtliche Argumente werden gegenüber anderen "
    "rechtlichen Argumenten erwidert.",
    BODY,
))

story.append(Paragraph(
    "Für diesen Austausch und den damit verbundenen Abgleich wird ein Mapping "
    "benötigt; für das Mapping wäre eine minimale Struktur hilfreich. Dabei "
    "ist unerheblich, ob die Texte bzw. Textteile originär strukturiert "
    "entstehen oder ob sie aus anderen Dateiformaten wie PDF abgeleitet "
    "werden. Entscheidend ist, dass die typischen Bezüge maschinell "
    "nachvollziehbar werden — und damit auch, dass die Strukturierung "
    "<b>bewusst minimal</b> ausgestaltet wird: gerade so präzise wie nötig, "
    "nicht so detailliert wie möglich.",
    BODY,
))

story.append(Paragraph(
    "Das Ziel ist nicht, Rechtsschriften und Entscheide vollständig in "
    "strukturierter Form abzubilden — sondern jene Anker zu setzen, an denen "
    "sich der Abgleich festmachen lässt.",
    CALLOUT,
))


# --- Build ------------------------------------------------------------
doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.6*cm, bottomMargin=2.4*cm,
    title="Strukturierte Rechtsdokumente — Argumentarium",
    author="Lorentzo",
    subject="XML als Scharnier für den Abgleich von Rechtsdokumenten",
)

doc.build(story, onFirstPage=page_decoration, onLaterPages=page_decoration)
print(f"Geschrieben: {OUT}")
