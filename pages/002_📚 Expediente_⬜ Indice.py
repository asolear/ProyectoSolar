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
import streamlit.components.v1 as components  # Import Streamlit

st.set_page_config(layout="wide")

warnings.filterwarnings('ignore')
font = {'family': 'monospace', 'size': '6'}
plt.rc('font', **font)



class doc:
    '''
        documento
        '''
    def doc():

        with PdfPages(f"docs/Expediente/pdfs/{os.path.basename(__file__)[:-3]}.pdf") as pdf:
            doc.Pag01.Pag01(pdf)

            # doc.Pag02.Pag02(pdf)
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

            doc.Pag01.Pag0101(fig, .15, .95)
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

            def fnavs():
                '''
                - embeber jpg del pdf con los resultados
                - https://github.com/asolear/fv01/blob/master/app_GUI.py
                '''
                navs = []

                files = sorted(
                    [lista for lista in os.listdir('docs/Expediente/pdfs')])[:]
                grupos = [x.split("_")[1] for x in files]
                grupos=list(dict.fromkeys(grupos))
                # grupos=["0"]

                for grupo in grupos:
                    files_grupo = [lista for lista in files if grupo in lista]
                    navs.append(f'''
                    
{grupo[2:]}''')
                    for file in files_grupo:
                        navs.append(f'''
    - {file.split("_")[2][2:-4]}.                    ''')
                navs = ' '.join(navs)
                    
                return navs


            texto = f'''

{fnavs()}
            









                        En Malaga a {datetime.datetime.today()}

                        
                                                 Proyecto.Solar

            '''

            ax.text(0, 0, texto, va="top", color='k', family='monospace', fontsize=9,
                    style='normal', wrap=True, bbox=dict(boxstyle='round', facecolor='w',
                                                         edgecolor='w', alpha=0.29))
            ax.axis('off')
class mkdocs:
    '''

    '''

    def mkdocs():
        '''
        arranca el servidor mkdocs
        '''

        mkdocs.CreaMds()
        mkdocs.creaIndexmd()
        mkdocs.creaMkdocsYml()

    def CreaMds():
        '''
        crea el mkdocs y lo arranca y lo incrusta en el st si esta disponible
        '''
        import os

        d = './docs/Expediente/pdfs'
        files = sorted([lista for lista in os.listdir(d)])
        files = [array for array in files if not "encrypt" in array]
        # print(files)
        for file in files:
            f = open(f"docs/Expediente/{file[:-4]}.md", "w")
            f.write(f'''#   {file.split("_")[2][:-4]}
# [🔙 ](../../)
<embed src="../../Expediente/pdfs/{file}"width=100% height="9999" type="application/pdf">'
    ''')
            f.close()

    def creaIndexmd():
        '''
        crea el index.md
        '''
        import os

        d = './docs/Expediente/pdfs'
        files = sorted([lista for lista in os.listdir(d)])
        files = [array for array in files if not "encrypt" in array]
        # print(files)

        f = open(f"docs/index.md", "w")
# <img src="figs/Screenshot from 2023-02-13 13-59-43.png"  width="100%" height="30%">

        f.write(f'''#
{mkdocs.fnavsmd()}
            ''')

        f.close()

    def creaMkdocsYml():

        # st.write(fnavs())
        f = open(f"mkdocs.yml", "w")
# <img src="figs/Screenshot from 2023-02-13 13-59-43.png"  width="100%" height="30%">

        f.write(f'''# 
site_name: 01_▫️📚_Proyecto.solar
theme:
  name: material
  palette:
    primary: white
  features:
    - toc.integrate
    - content.code.annotate
plugins:
  - mkdocstrings
  - search

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
  
nav:
{mkdocs.fnavsyml()}
            ''')
        f.close()

    def fnavsmd():
        '''
        - crea el indice en format md
        '''
        navs = []

        files = sorted(
            [lista for lista in os.listdir('docs/Expediente/pdfs')])[:]

        grupos = [x.split("_")[1] for x in files]
        grupos = list(dict.fromkeys(grupos))
        # grupos=["0"]

        for grupo in grupos:
            files_grupo = [lista for lista in files if grupo in lista]
            navs.append(f'''
## {grupo}:''')
            for file in files_grupo:
                navs.append(f'''
- [{file.split("_")[2][:-4]}.](Expediente/{file[:-4]}.md)''')
        navs = ' '.join(navs)

        return navs

    def fnavsyml():
        '''
        - crea el indice en formato yml
        '''
        navs = []

        files = sorted(
            [lista for lista in os.listdir('docs/Expediente/pdfs')])[:]
        grupos = [x.split("_")[1] for x in files]
        grupos = list(dict.fromkeys(grupos))
        # grupos=["0"]

        for grupo in grupos:
            files_grupo = [lista for lista in files if grupo in lista]
            navs.append(f'''
    - {grupo}:''')
            for file in files_grupo:
                navs.append(f'''
        - {file.split("_")[2][:-4]}: Expediente/{file[:-4]}.md''')
        navs = ' '.join(navs)

        return navs


def app():
    '''
    visualiza docuentos con los valors del estado tomados del json
    '''
    doc.doc()
    mkdocs.mkdocs()
    components.iframe("http://127.0.0.1:8000",  height=11002)

if __name__ == "__main__":
    # s = _estado.json2_estado()
    app()
