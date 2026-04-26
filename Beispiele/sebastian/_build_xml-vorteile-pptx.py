"""Generiert xml-vorteile.pptx — PowerPoint-Argumentarium auf Basis
der Kanzlei-Vorlage 'Standard PowerPoint.potx'.

Ausführen:
    uv run --no-project --with python-pptx \\
        python3 Beispiele/sebastian/_build_xml-vorteile-pptx.py
"""
from pathlib import Path
import zipfile, tempfile, os

from pptx import Presentation
from pptx.util import Pt, Cm
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

REPO = Path(__file__).resolve().parents[2]
TEMPLATE = REPO / "Standard PowerPoint.potx"
OUT = Path(__file__).parent / "xml-vorteile.pptx"

ACCENT = RGBColor(0x38, 0xB0, 0x7D)        # Kanzlei-Grün aus dem Theme
INK    = RGBColor(0x21, 0x21, 0x21)
MUTED  = RGBColor(0x55, 0x55, 0x55)


# --- Vorlage potx → pptx konvertieren (nur content-type ändern) -------
def potx_to_pptx_bytes(potx_path: Path) -> bytes:
    """Konvertiert .potx zu .pptx, indem der Content-Type umgeschrieben
    wird. Inhalt sonst identisch."""
    import io
    buf = io.BytesIO()
    with zipfile.ZipFile(potx_path, 'r') as zin, \
         zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.namelist():
            data = zin.read(item)
            if item == '[Content_Types].xml':
                data = data.replace(
                    b'application/vnd.openxmlformats-officedocument.'
                    b'presentationml.template.main+xml',
                    b'application/vnd.openxmlformats-officedocument.'
                    b'presentationml.presentation.main+xml')
            zout.writestr(item, data)
    return buf.getvalue()


# --- Helper -----------------------------------------------------------
def remove_all_slides(prs):
    sldIdLst = prs.slides._sldIdLst
    rId_to_drop = []
    for sldId in list(sldIdLst):
        rId_to_drop.append(sldId.attrib[
            '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'])
        sldIdLst.remove(sldId)
    for rId in rId_to_drop:
        try:
            prs.part.drop_rel(rId)
        except Exception:
            pass


def find_placeholder(slide, idx):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == idx:
            return ph
    return None


def set_text(placeholder, text, *, size=18, bold=False, color=INK, align=PP_ALIGN.LEFT):
    placeholder.text_frame.text = ""
    p = placeholder.text_frame.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color


def add_bullets(placeholder, items, *, size=14, level_size_step=2):
    tf = placeholder.text_frame
    tf.text = ""
    tf.word_wrap = True
    first = True
    for item in items:
        if isinstance(item, tuple):
            text, level = item
        else:
            text, level = item, 0
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.level = level
        p.text = text
        for run in p.runs:
            run.font.size = Pt(size - level * level_size_step)
            run.font.color.rgb = INK


# --- Build ------------------------------------------------------------
def build():
    pptx_bytes = potx_to_pptx_bytes(TEMPLATE)
    tmp = tempfile.NamedTemporaryFile(suffix=".pptx", delete=False)
    tmp.write(pptx_bytes)
    tmp.close()

    prs = Presentation(tmp.name)
    remove_all_slides(prs)
    layouts = list(prs.slide_layouts)

    # 0 Titelfolie | 1 Abschnittsüberschrift | 4 Nur Text
    # 8 Danke | 9 Inhalt mit Überschrift
    L_TITEL    = layouts[0]
    L_ABSCHN   = layouts[1]
    L_NUR_TEXT = layouts[4]
    L_INHALT   = layouts[9]
    L_DANKE    = layouts[8]

    # ------------------------------------------------------------------
    # 1 — Titelfolie
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(L_TITEL)
    ph10 = find_placeholder(s, 10)
    ph14 = find_placeholder(s, 14)
    if ph10:
        set_text(ph10, "Strukturierte Rechtsdokumente",
                 size=40, bold=True, color=ACCENT)
    if ph14:
        set_text(ph14,
                 "XML als Scharnier für den Abgleich von Rechtsdokumenten "
                 "(Entscheide und Rechtsschriften)",
                 size=20, color=INK)

    # ------------------------------------------------------------------
    # 2 — Abschnittsüberschrift: Sinn und Zweck
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(L_ABSCHN)
    ph0 = find_placeholder(s, 0)
    if ph0:
        set_text(ph0,
                 "Sinn und Zweck — wieso ein strukturiertes Scharnierformat?",
                 size=36, bold=True, color=ACCENT)

    # ------------------------------------------------------------------
    # 3 — Texte und ihre Bezüge
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(L_INHALT)
    title = find_placeholder(s, 0)
    body  = find_placeholder(s, 2) or find_placeholder(s, 1)
    if title:
        set_text(title, "Texte und ihre Bezüge", size=28, bold=True, color=ACCENT)
    if body:
        add_bullets(body, [
            "Rechtsschriften und Urteile bestehen mehrheitlich aus Text.",
            "Im Verfahren werden diese Texte ausgetauscht; es wird wechselseitig "
            "auf Textteile Bezug genommen.",
            "Bezug nicht auf beliebige Stellen, sondern auf inhaltlich verwandte:",
            ("Sachverhaltselemente korrespondieren mit Sachverhaltselementen,", 1),
            ("rechtliche Argumente werden gegen rechtliche Argumente erwidert.", 1),
        ], size=18)

    # ------------------------------------------------------------------
    # 4 — Mapping braucht minimale Struktur
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(L_INHALT)
    title = find_placeholder(s, 0)
    body  = find_placeholder(s, 2) or find_placeholder(s, 1)
    if title:
        set_text(title, "Mapping braucht minimale Struktur",
                 size=28, bold=True, color=ACCENT)
    if body:
        add_bullets(body, [
            "Für den Austausch und Abgleich wird ein Mapping benötigt.",
            "Für das Mapping ist eine minimale Struktur hilfreich.",
            "Unerheblich, ob Texte originär strukturiert entstehen oder "
            "aus PDF abgeleitet werden.",
            "Entscheidend: typische Bezüge maschinell nachvollziehbar.",
            "Strukturierung bewusst minimal — gerade so präzise wie nötig, "
            "nicht so detailliert wie möglich.",
        ], size=18)

    # ------------------------------------------------------------------
    # 5 — Kernaussage
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(L_NUR_TEXT)
    ph14 = find_placeholder(s, 14)
    if ph14:
        tf = ph14.text_frame
        tf.text = ""
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = "Nicht Vollabbildung,"
        run.font.size = Pt(32)
        run.font.bold = True
        run.font.color.rgb = ACCENT

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = "sondern Anker für den Abgleich."
        r2.font.size = Pt(32)
        r2.font.bold = True
        r2.font.color.rgb = ACCENT

        p3 = tf.add_paragraph()
        p3.alignment = PP_ALIGN.CENTER
        r3 = p3.add_run()
        r3.text = ""
        r3.font.size = Pt(8)

        p4 = tf.add_paragraph()
        p4.alignment = PP_ALIGN.CENTER
        r4 = p4.add_run()
        r4.text = ("Ziel ist nicht, Rechtsschriften und Entscheide vollständig "
                   "in strukturierter Form abzubilden.")
        r4.font.size = Pt(16)
        r4.font.color.rgb = MUTED

    # ------------------------------------------------------------------
    # 6 — Danke
    # ------------------------------------------------------------------
    prs.slides.add_slide(L_DANKE)

    prs.save(str(OUT))
    os.unlink(tmp.name)
    print(f"Geschrieben: {OUT}  ({OUT.stat().st_size:,} Bytes, "
          f"{len(prs.slides)} Folien)")


if __name__ == "__main__":
    build()
