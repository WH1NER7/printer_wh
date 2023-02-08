import os

from io import BytesIO
from PyPDF2 import PdfWriter, PdfReader

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from barcode import EAN13
from barcode.writer import SVGWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from miscellaneous.path import PathManager


def barcode_generating(brand, name, model, color, size, country, batch, factory, barcode):
    # rv = BytesIO()
    # EAN13(str("100000902922"), writer=SVGWriter()).write(rv)

    # Or to an actual file:
    with open(PathManager.get("svgs/somefile.svg"), "wb") as f:
        EAN13(str(barcode), writer=SVGWriter()).write(f)

    drawing = svg2rlg(PathManager.get("svgs/somefile.svg"))

    drawing.scale(1.3, 1)
    drawing.height = 113.5
    drawing.width = 164

    renderPDF.drawToFile(drawing, PathManager.get("barcodes_data_print/file.pdf"))
    space = ' '
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'miscellaneous/DejaVuSans.ttf'))

    can.setFont('DejaVuSans', 14)
    can.drawString(15, 100, f"{brand}{space * (15 - len(brand))}EAC")
    can.setFont('DejaVuSans', 6)

    can.drawString(15, 83, name)
    can.setFont('DejaVuSans', 5)
    can.drawString(15, 67,
                   f"Размер [{size}] {space * (15 - len(color))} {color} {space * (20 - len(brand))} {country} {batch} {factory}")
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    # read your existing PDF
    existing_pdf = PdfReader(open(PathManager.get("barcodes_data_print/file.pdf"), "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    # finally, write "output" to a real file
    output_stream = open(PathManager.get(f'barcodes_data_print/destination.pdf'), "wb")
    output.write(output_stream)
    output_stream.close()
    os.startfile(PathManager.get(f'barcodes_data_print/destination.pdf'), 'print')


if __name__ == '__main__':
    barcode_generating('MissYourKiss', 'Деван-дерьеры + красные подвязки', 'model', 'Красный', 'L', 'Россия', 'A1XX',
                       'RKXX', 100000011111)
