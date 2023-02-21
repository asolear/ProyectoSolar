# pdf_merging.py
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import streamlit as st

# extract_doc_info.py


def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    ## Information about {pdf_path}: 
    - Author: {information.author}
    - Creator: {information.creator}
    - Producer: {information.producer}
    - Subject: {information.subject}
    - Title: {information.title}
    - Number of pages: {number_of_pages}
    """
    st.write(txt)
    print(txt)
    return information

if __name__ == '__main__':

    d='./docs/Expediente/pdfs'
    files = sorted([lista for lista in os.listdir(d)])
    files = [array for array in files if not "encrypt" in array]
    files=[os.path.join(d, f) for f in files]

    for file in files:
        extract_information(file)



