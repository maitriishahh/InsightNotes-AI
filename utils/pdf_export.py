from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib.pagesizes import A4
import os


def export_notes_to_pdf(title: str, notes: str, output_path: str):
    """
    Export structured notes to PDF.
    """

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    # Add Title
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Split notes into paragraphs
    lines = notes.split("\n")

    for line in lines:
        if line.strip() == "":
            elements.append(Spacer(1, 0.2 * inch))
        else:
            elements.append(Paragraph(line, normal_style))
            elements.append(Spacer(1, 0.1 * inch))

    doc.build(elements)
