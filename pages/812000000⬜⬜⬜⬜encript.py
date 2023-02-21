# pdf_merging.py
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import streamlit as st
# pdf_encrypt.py


def add_encryption(input_pdf, output_pdf, password):
    texto=f'''

    # How to Work With a PDF in Python
    https://realpython.com/pdf-python/
    
    
    '''
    st.write(texto)

    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_pdf)

    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))

    pdf_writer.encrypt(user_pwd=password, owner_pwd=None, 
                       use_128bit=True)

    with open(output_pdf, 'wb') as fh:
        pdf_writer.write(fh)

if __name__ == '__main__':
    d='./docs/Expediente/pdfs'
    add_encryption(input_pdf=d+'/merged.pdf',
                   output_pdf=d+'/merged-encrypted.pdf',
                   password='pk')


