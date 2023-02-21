
import streamlit as st

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from types import SimpleNamespace
#
import os
import json
import inspect
import datetime
import pandas as pd
import numpy as np
#
import geopandas as gpd
from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import *
import tomli
import sys
from math import *
from pvlib import solarposition
import requests
from time import time
import warnings
import io
import base64
import shutil
st.set_page_config(layout="wide")

warnings.filterwarnings('ignore')
font = {'family': 'monospace', 'size': '6'}
plt.rc('font', **font)


class _estado:
    '''
    memoria
    '''
    def json2_estado():
        '''
        Leo el JSON en memoria  s.s['xxxxx'] y si no hay lo creo

        '''

        with open("_estado.json", "r") as f:
            s = json.load(f)
        s = SimpleNamespace(s=s)

        '''
        slo para inicializar algunas variables string vector y panadas
        tiene que estar el fichero 'assets/json/_estado.json' al meos solo con {}
        '''
        return s

    def _estado2json():
        '''
        Escribo el JSON en disco como datos 'json' s.s['xxxxx']
        '''

        with open("_estado.json", "w") as f:
            f.write(json.dumps(s.s))
        return


class displayPDF:
    def displayPDF():
        '''
        para visualizar el pdf generado
        '''
        file = f"docs/Expediente/pdfs/{os.path.basename(__file__)[:-3]}.pdf"
        with open(file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width=100% height="1000" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)


class doc:
    '''
        documento
        '''
    def doc():

        with PdfPages(f"docs/Expediente/pdfs/{os.path.basename(__file__)[:-3]}.pdf") as pdf:
            doc.Pag01.Pag01(pdf)

            doc.Pag02.Pag02(pdf)
            # doc.Pag01.Pag0103.Pag0103(pdf)

            d = pdf.infodict()
            d['Title'] = ''
            d['Creator'] = ''
            d['Producer'] = ''
            d['Author'] = 'Proyecto.Solar'
            d['Subject'] = ''
            d['Keywords'] = ''
            d['CreationDate'] = datetime.datetime.today()
            d['ModDate'] = datetime.datetime.today()
            return pdf

    class Pag01:
        '''
            pagina del documento (los nombres del metodo y clase de la pagina deben ser los del documento y 2 cifras del numero de pagina por el fig.savefig)
            '''
        def Pag01(pdf):

            fig, axx = plt.subplots(figsize=(21/2.54*1, 29.7/2.54))

            doc.Pag01.Pag0101(fig, .05, .8)
            # guardo primero un imagen par ala web, y luego elpdf con el cabecero y pie de pag
            axx.axis('off')
            pdf.savefig()
            plt.close()
            plt.show()

        def Pag0101(fig, x, y):
            '''
            .
            '''
            ax = fig.add_axes([x, y, 0, 0], frameon=False)

            ax.axis('off')

    class Pag02:
        '''
        pagina del documento (los nombres del metodo y clase de la pagina deben ser los del documento y 2 cifras del numero de pagina por el fig.savefig)
        '''

        def Pag02(pdf):

            fig, axx = plt.subplots(figsize=(21/2.54*1, 29.7/2.54))

            doc.Pag02.Pag0201(fig, .05, .6)
            # guardo primero un imagen par ala web, y luego elpdf con el cabecero y pie de pag
            axx.axis('off')
            pdf.savefig()
            plt.close()
            plt.show()

        def Pag0201(fig, x, y):
            '''
            .
            '''
            ax = fig.add_axes([x, y, 0, 0], frameon=False)


            ax.axis('off')


def app():
    '''
    visualiza docuentos con los valors del estado tomados del json
    '''

    doc.doc()
    displayPDF.displayPDF()


if __name__ == "__main__":
    s = _estado.json2_estado()
    app()
