
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


class textos:
    def textos():
        t1 = rf'''
              Generado con sss
              
              Script:                    {os.path.basename(__file__)[:-3]} 
              clase                         {__class__.__name__}
                '''

        t2 = rf''' 
                                $\mathbf{{ T E X T O S\ \ de\ \  E J E M P L O}}$
                                    https://matplotlib.org/2.0.2/users/mathtext.html
        
        * variables                  {s.s['FV']['meta']['vv']['bb']} $a=2/3$ 
        * math !!! con variables                   $a=\frac{{{s.s['FV']['meta']['vv']['bb']} }}{{\alpha}}$
        '''
        t3 = rf''' 

        Ver otros simbolos:
                $\beta 	\chi 	\delta 	\digamma \backsimeq$  
                                    $\Downarrow 	\Leftarrow   \Leftrightarrow 	\Lleftarrow    \bigcap  \widehat{{xyz}} $ 
                                                    y todas la lineas que se queira con salto depagina automatico
            $\mathcal{{calligraphic}}$  $\mathbf{{negrita}}   $   $\mathit{{italic}}   $
            $\mathcal{{CALLIGRAPHY}}$
            $\mathbb{{blackboard}}$
   
X << este punto es el origen de los ejes anadidos. Se da anchura y altura cero
        '''
        return t1, t2, t3


class contenido:
    ''' contenidos'''

    def p11(fig):
        ax = fig.add_axes([.5, .5, 0.5, 0.5], frameon=False)
        #
        ax.axis("off")

    def p12(fig):
        ax = fig.add_axes([.1, .5, 0.5, 0.5], frameon=False)
        ax.text(0, 0, 'boo', color='k', family='monospace', fontsize=8, va='top',
                style='normal', wrap=True, bbox=dict(boxstyle='round', facecolor='w',
                                                     edgecolor='r', alpha=0.29))
        ax.axis("off")

    def p21(fig):
        ax = fig.add_axes([.5, .5, 0.5, 0.5], frameon=False)
        #
        ax.axis("off")

    def p22(fig):
        ax = fig.add_axes([.5, .5, 0.5, 0.5], frameon=False)
        #
        ax.axis("off")

    def p22(fig):
        '''
        .
        '''
        ax = fig.add_axes([0.2, .90, 0, 0], frameon=False)

        ax.text(0, 0, textos.textos()[1], color='k', family='monospace', fontsize=8, va='top',
                style='normal', wrap=True, bbox=dict(boxstyle='round', facecolor='w',
                                                     edgecolor='w', alpha=0.29))
        ax.axis('off')


class doc:
    '''
        documento
        '''

    def doc():

        with PdfPages(f"docs/Expediente/pdfs/{os.path.basename(__file__)[:-3]}.pdf") as pdf:
            doc.Pag01(pdf)
            # doc.Pag02(pdf)

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

    def Pag01(pdf):

        fig, axx = plt.subplots(figsize=(21/2.54*2, 29.7/2.54))
        cajetin = axx.get_position()
        axx.set_position([cajetin.x0-.05,
                          cajetin.y0-.08,
                          cajetin.x1+0.0,
                          cajetin.y1+0.055])
        ##########################
        contenido.p11(fig)
        contenido.p12(fig)
        contenido.p21(fig)
        contenido.p22(fig)
        ##########################
        # axx.axis('off')
        pdf.savefig()
        plt.close()

    def Pag02(pdf):

        fig, axx = plt.subplots(figsize=(21/2.54*2, 29.7/2.54))
        cajetin = axx.get_position()
        axx.set_position([cajetin.x0-.05,
                          cajetin.y0-.08,
                          cajetin.x1+0.0,
                          cajetin.y1+0.055])
        ##########################
        contenido.p11(fig)
        contenido.p12(fig)
        contenido.p21(fig)
        contenido.p22(fig)
        ##########################
        # axx.axis('off')
        pdf.savefig()
        plt.close()


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

        mkdocs.xxxxx_md()
        mkdocs.index_md()
        mkdocs.mkdocs_yml()
        # mkdocs.contacto_md()

    def xxxxx_md():
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

    def index_md():
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

    def mkdocs_yml():

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
  - attr_list
  - admonition
  - pymdownx.details
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
