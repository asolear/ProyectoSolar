
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
import contextily as ctx

st.set_page_config(layout="wide")

warnings.filterwarnings('ignore')
font = {'family': 'monospace', 'size': '6'}
plt.rc('font', **font)


class textos:
    def textos():
        geo_df = gpd.GeoDataFrame.from_file(
            s.s['FV']['outputs']['vv']['CUBIERTA'])

        t1 = rf'''geo_df.crs {geo_df.crs}'''
        # geo_df = geo_df.to_crs(epsg=2062 )
        t1 += rf'''     {geo_df.crs}'''
        # t1 += rf'''     {geo_df.to_string()}'''
        t1 += rf'''     {pd.DataFrame(list(ctx.providers.keys()))
}'''

        return t1


class contenido:
    ''' contenidos'''

    def contenido(fig):
        contenido.Alzado_Modificado(fig)
        contenido.Alzado_Actual(fig)
        contenido.Planta_Actual(fig)
        contenido.Planta_Modificado(fig)
        contenido.qr(fig)


    def qr(fig):
        '''
        - codigo QR que con el enlace a un oferta
            - parametros
                - url.- direccion de la oferta
                - x,y posicion en el folio 
        '''
        import qrcode
        ax = fig.add_axes([.77, .081, .05, .05], frameon=False)
        qr = qrcode.QRCode()
        qr.add_data('https://proyecto.solar/')
        ax.imshow(qr.make_image().convert("RGB"),
                  extent=[0, 22, 0, 22], cmap='Greys')
        ax.axis("off")


    def Alzado_Actual(fig):
        ax = fig.add_axes([.1, .6, 0.3, 0.3], frameon=False)


        ax.axis("off")

    def Alzado_Modificado(fig):
        ax = fig.add_axes([.5, .6, 0.3, 0.3], frameon=False)
        ax.axis("off")


    def Planta_Actual(fig):
        ax = fig.add_axes([.1, .3, 0.3, 0.3], frameon=False)

        # gpd.GeoDataFrame.from_file(
        #     s.s['FV']['outputs']['vv']['PANELES']).boundary.plot(ax=ax, aspect=1, cmap='tab20')
        gpd.GeoDataFrame.from_file(
            s.s['FV']['outputs']['vv']['CUBIERTA']).boundary.plot(ax=ax, aspect=1, cmap='tab20')
        ax.set_title('Planta_Actual', y=-.15)

        gg = gpd.GeoDataFrame.from_file(
            s.s['FV']['outputs']['vv']['SOMBRAS'])

        ggg = gg[gg['Layer'] == 'S0']
        ggg.plot(
            ax=ax, aspect=1, color='lightgrey')

        ax.axis("off")

    def Planta_Modificado(fig):
        ax = fig.add_axes([.5, .3, 0.3, 0.3], frameon=False)

        gpd.GeoDataFrame.from_file(
            s.s['FV']['outputs']['vv']['PANELES']).boundary.plot(ax=ax, aspect=1,color='b')
        print(gpd.GeoDataFrame.from_file(
            s.s['FV']['outputs']['vv']['PANELES']))
        gpd.GeoDataFrame.from_file(
            s.s['FV']['outputs']['vv']['CUBIERTA']).boundary.plot(ax=ax, aspect=1, cmap='tab20')
        ax.set_title('Planta_Modificado', y=-.15)

        gg = gpd.GeoDataFrame.from_file(
            s.s['FV']['outputs']['vv']['SOMBRAS'])

        ggg = gg[gg['Layer'] == 'S0']
        ggg.plot(
            ax=ax, aspect=1, color='lightgrey')


        ax.axis("off")


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
                          cajetin.x1+0.00,
                          cajetin.y1+0.06])

        yy=0.003
        xx=1*yy/1.2

        # hline
        plt.axhline(y=(36)*yy, xmin=1-(180)*xx, xmax=1.00, color='k', linewidth=.2)
        plt.axhline(y=(36-6-6-6)*yy, xmin=1-(180)*xx, xmax=1.00, color='k', linewidth=.2)
        plt.axhline(y=(36-6)*yy, xmin=1-(180)*xx, xmax=1+(-180+20+18+22+30)*xx, color='k', linewidth=.2)
        plt.axhline(y=(36-6-6)*yy, xmin=1-(180)*xx, xmax=1+(-180+20+18+22)*xx, color='k', linewidth=.2)
        plt.axhline(y=12*yy, xmin=1+(-60)*xx, xmax=1.00, color='k', linewidth=.2)
        plt.axhline(y=6*yy, xmin=1+(-60)*xx, xmax=1.00, color='k', linewidth=.2)
        # vline
        plt.axvline(x=1+(-180)*xx, ymin=0.00, ymax=(36)*yy, color='k', linewidth=.2)
        plt.axvline(x=1+(-180+20+18+22+30)*xx, ymin=(36-6-6-6)*yy, ymax=(36)*yy, color='k', linewidth=.2)
        plt.axvline(x=1+(-180+20+18+22)*xx, ymin=(36-6-6-6)*yy, ymax=(36)*yy, color='k', linewidth=.2)
        plt.axvline(x=1+(-180+20+18)*xx, ymin=(36-6-6-6)*yy, ymax=(36)*yy, color='k', linewidth=.2)
        plt.axvline(x=1+(-180+20)*xx, ymin=(36-36)*yy, ymax=(36)*yy, color='k', linewidth=.2)
        plt.axvline(x=1+(-60)*xx, ymin=(36-36)*yy, ymax=((36-6-6-6))*yy, color='k', linewidth=.2)
        #
        axx.text(1+(-180+20+1)*xx,(36-6+1)*yy,'Fecha',fontsize=8)
        axx.text(1+(-180+20+18+1)*xx,(36-6+1)*yy,'Nombre',fontsize=8)
        axx.text(1+(-180+20+18+22+1)*xx,(36-6+1)*yy,'Firmas',fontsize=8)
        #
        axx.text(1+(-180+1)*xx,(36-6+1)*yy,'')
        axx.text(1+(-180+1)*xx,(36-6-6+1)*yy,'Dibujado',fontsize=8)
        axx.text(1+(-180+20+18+1)*xx,(36-6-6+1)*yy,'M.Ruiz',fontsize=8)
        axx.text(1+(-180+20+1)*xx,(36-6-6+1)*yy,datetime.datetime.now().strftime("%d/%m/%Y"),fontsize=7)
        axx.text(1+(-180+1)*xx,(36-6-6-6+1)*yy,'Comprobado',fontsize=8)
        axx.text(1+(-180+20+18+1)*xx,(36-6-6-6+1)*yy,'F.Roman',fontsize=8)
        axx.text(1+(-180+20+1)*xx,(36-6-6-6+1)*yy,datetime.datetime.now().strftime("%d/%m/%Y"),fontsize=7)
        axx.text(1+(-180+1)*xx,(36-6-6-6-6+1)*yy,'Escala',fontsize=8)
        #
        axx.text(1+(-60+1)*xx,(0+1)*yy,'Sustituido por',fontsize=8)
        axx.text(1+(-60+1)*xx,(6+1)*yy,'Sustituye a',fontsize=8)
        axx.text(1+(-60+1)*xx,(6+6+1)*yy,'Número',fontsize=8)
        axx.text(1+(-60+33+1)*xx,(6+6+1)*yy,'1',fontsize=8)
        #
        axx.text(1+(-60+1)*xx,(10+6+6+1)*yy,'Proyecto.Solar',fontsize=14)
        axx.text(1+(-150+1)*xx,(6+1)*yy,f'{os.path.basename(__file__)[20:-3]}',fontsize=14)


        ##########################
        contenido.contenido(fig)
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
