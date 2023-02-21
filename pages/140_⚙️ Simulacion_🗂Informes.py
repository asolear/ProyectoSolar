
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from types import SimpleNamespace
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
import utm
import os
st.set_page_config(layout="wide")

warnings.filterwarnings('ignore')
font = {'family': 'monospace', 'size': '6'}
plt.rc('font', **font)


class doc:
    def doc():
        '''
        # FILTRADO DE LOS DOCUMENTOS PARA EL EXPEDIENTE 
        - rellenado de los formularios con los datos del estado
        '''
        from fillpdf import fillpdfs

        files = sorted(
            [lista for lista in os.listdir('docs/Expediente/pdfs')])
        files = [lista for lista in files if not "index" in lista]
        files = [lista for lista in files if ".pdf" in lista]

        for file in files:
            in_pdf_file = f'docs/Expediente/pdfs/{file}'
            out_pdf_file = f'docs/Expediente/pdfs/{file}'
            try:
                diccionario = s.s['formularios']['outputs'][file]
                fillpdfs.write_fillable_pdf(
                    in_pdf_file, out_pdf_file, diccionario)
            except:
                shutil.copy(in_pdf_file, out_pdf_file)



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
    import streamlit.components.v1 as components  # Import Streamlit
    doc.doc()
    mkdocs.mkdocs()
    components.iframe("http://127.0.0.1:8000",  height=11002)


if __name__ == "__main__":
    s = _estado.json2_estado()
    app()
