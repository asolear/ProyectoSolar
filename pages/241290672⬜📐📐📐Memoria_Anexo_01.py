
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
        print(os.path.realpath(os.path.dirname(__file__)))
        try:
            with open("_estado.json", "r") as f:
                s = json.load(f)
            s = SimpleNamespace(s=s)
        except:
            # lo creo
            f = open("_estado.json", "w")
            f.write("{}")
            f.close()
            # y lopaso a memoria
            with open("_estado.json", "r") as f:
                s = json.load(f)
            s = SimpleNamespace(s=s)

        '''
        slo para inicializar algunas variables string vector y panadas
        tiene que estar el fichero 'assets/json/_estado.json' al meos solo con {}
        '''
        # para mantener los valores anteriores en el json
        try:
            s.s['FV']
        except:
            s.s = {'a': {'meta': {}, 'inputs': {}, 'outputs': {}}}

        return s

    def _estado2json():
        '''
        Escribo el JSON en disco como datos 'json' s.s['xxxxx']
        '''

        with open("_estado.json", "w") as f:
            f.write(json.dumps(s.s))
        return


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

    class Pag01:
        '''
            pagina del documento (los nombres del metodo y clase de la pagina deben ser los del documento y 2 cifras del numero de pagina por el fig.savefig)
            '''
        def Pag01(pdf):

            fig, axx = plt.subplots(figsize=(21/2.54*1, 29.7/2.54))

            def ff():
                ax = fig.add_axes([.16, .77, 0.2, 0.2], frameon=False)
                gpd.GeoDataFrame.from_file(
                    s.s['FV']['outputs']['vv']['gf_dxf']).plot(ax=ax, aspect=1, cmap='tab20')
                # ax.axis("off")
                ax.set_title('fig. dxf', y=-.15)
            ff()

            def ff():
                ax = fig.add_axes([.16, .55, 0.2, 0.2], frameon=False)
                gpd.GeoDataFrame.from_file(
                    s.s['FV']['outputs']['vv']['CUBIERTA']).boundary.plot(ax=ax, aspect=1, cmap='tab20')
                ax.set_title('fig. gf', y=-.15)

                # ax.axis("off")
            ff()

            def ff():
                ax = fig.add_axes([.16, .35, 0.2, 0.2], frameon=False)
                gpd.GeoDataFrame.from_file(
                    s.s['FV']['outputs']['vv']['SOMBRAS']).boundary.plot(ax=ax, aspect=1, cmap='tab20')
                ax.set_title('fig. SOMBRAS', y=-.15)

                # ax.axis("off")
            ff()

            def ff():
                ax = fig.add_axes([.16, .2, 0.2, 0.2], frameon=False)

                gg = s.s['FV']['outputs']['vv']['ENVELOPES']
                gpd.GeoDataFrame.from_file(gg).boundary.plot(
                    ax=ax, aspect=1, cmap='tab20')

                gg = s.s['FV']['outputs']['vv']['PANELES_MATRIZ']
                gpd.GeoDataFrame.from_file(gg).boundary.plot(
                    ax=ax, aspect=1, cmap='tab20')

                ax.set_title('fig. PANELES_MATRIZ', y=-.15)

                # ax.axis("off")
            ff()

            def ff():
                ax = fig.add_axes([.46, .2, 0.2, 0.2], frameon=False)

                gpd.GeoDataFrame.from_file(
                    s.s['FV']['outputs']['vv']['PANELES']).boundary.plot(ax=ax, aspect=1, cmap='tab20')
                gpd.GeoDataFrame.from_file(
                    s.s['FV']['outputs']['vv']['CUBIERTA']).boundary.plot(ax=ax, aspect=1, cmap='tab20')
                ax.set_title('fig. h_PANELES', y=-.15)

                gg = gpd.GeoDataFrame.from_file(
                    s.s['FV']['outputs']['vv']['SOMBRAS'])

                ggg = gg[gg['Layer'] == 'S0']
                ggg.plot(
                    ax=ax, aspect=1, color='lightgrey')

                # ax.axis("off")
            ff()

            def ff():
                ax = fig.add_axes([.46, .85, 0, 0], frameon=False)
                ax.text(0, 0, pd.Series(
                    s.s['FV']['inputs']['inversor']).to_string())

                ax = fig.add_axes([.46, .73, 0, 0], frameon=False)
                ax.text(0, 0, pd.Series(
                    s.s['FV']['inputs']['panel']).to_string())

                ax = fig.add_axes([.46, .6, 0, 0], frameon=False)
                ax.text(0, 0, pd.Series(
                    s.s['FV']['inputs']['inversor']).to_string())

                # ax.text(0, 1, ''+parametrosDXF, va="top",   wrap=True,
                # fontfamily="monospace", fontsize=6)
                # ax.axis("off")
            ff()

            def ff():
                gg = gpd.GeoDataFrame.from_file(
                    s.s['FV']['outputs']['vv']['CUBIERTA'])
                print(gg.head())
                gg = gpd.GeoDataFrame.from_file(
                    s.s['FV']['outputs']['vv']['ENVELOPES'])
                print(gg.head())
            ff()

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

            texto = f'''
                  Generado con el script:
                    {os.path.basename(__file__)[:-3]} 

                  en la clase
                    {__class__.__name__}

                  el

                  {s.s['FV']['meta']['vv']['fecha']}
                    '''

            ax.text(0, 0, texto, color='green', family='monospace', fontsize=11,
                    style='normal', wrap=True, bbox=dict(boxstyle='round', facecolor='w',
                                                         edgecolor='w', alpha=0.29))
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

            texto = f'''
                  Generado con el script:
                    {os.path.basename(__file__)[:-3]} 

                  en la clase
                    {__class__.__name__}

                    fffff ok makei
                    '''

            ax.text(0, 0, texto, color='red', family='monospace', fontsize=11,
                    style='normal', wrap=True, bbox=dict(boxstyle='round', facecolor='w',
                                                         edgecolor='w', alpha=0.29))
            ax.axis('off')


def displayPDF():
    '''
    para visualizar el pdf generado
    '''
    file = f"docs/Expediente/pdfs/{os.path.basename(__file__)[:-3]}.pdf"
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width=100% height="1000" type="application/pdf">'
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


def app():
    '''

    '''
    # mkdocs.mkdocs()

    # clc_edificio.clc_edificio()
    doc.doc()
    displayPDF()


if __name__ == "__main__":

    s = _estado.json2_estado()
    app()
