# pdf_merging.py
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import streamlit as st

def merge_pdfs(paths, output):
    texto=f'''

    # How to Work With a PDF in Python
    https://realpython.com/pdf-python/
    
    
    '''
    st.write(texto)


    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

if __name__ == '__main__':
    d='./docs/Expediente/pdfs'
    files = sorted([lista for lista in os.listdir(d)])
    files = [array for array in files if not "encrypt" in array]
    files=[os.path.join(d, f) for f in files]
    # paths = ['document1.pdf', 'document2.pdf']
    merge_pdfs(files, output=d+'/merged.pdf')
