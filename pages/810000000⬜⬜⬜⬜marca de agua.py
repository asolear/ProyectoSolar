# pdf_watermarker.py
# https://realpython.com/pdf-python/#pdfrw-an-alternative
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import streamlit as st

def create_watermark(input_pdf, output, watermark):
    texto=f'''

    # How to Work With a PDF in Python
    https://realpython.com/pdf-python/
    
    
    '''
    st.write(texto)


    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.merge_page(watermark_page)
        pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)

if __name__ == '__main__':
    create_watermark(
        input_pdf='Expediente/pdfs/33_⚪_📔_Plantilla.pdf', 
        output='watermarked_notebook.pdf',
        watermark='Expediente/pdfs/035_⚪_📗_PVcalc.pdf')
