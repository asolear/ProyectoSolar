
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


class doc:
    '''
        documento
        '''
    def doc():
        with PdfPages(f"docs/Expediente/pdfs/{os.path.basename(__file__)[:-3]}.pdf") as pdf:
            for ip, rp in gpd.GeoDataFrame.from_file(s.s['FV']['outputs']['vv']['PANELES']).iloc[[1, 5,3]].iterrows():
                print(rp.userhorizon)
                st.write(ip)
                s.s['FV']['meta']['vv']['ip']=ip
                doc.Pag01.Pag01(pdf)

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

            doc.Pag01.TablaInput_____(fig, .70, .75)
            doc.Pag01.mapaGeoJson____(fig, .65, .70)
            doc.Pag01.energy_________(fig, .10, .20)
            doc.Pag01.perfilSombras__(fig, .10, .35)
            doc.Pag01.cubierta_______(fig, .10, .55)
            # PDFs.Pagina_0.objetos__(fig, .10, .85)

            axx.axis('off')
            pdf.savefig()
            plt.close()
            plt.show()

        def objetos__(fig, x, y):
            ax = fig.add_axes([x, y, .4, .10], frameon=False)
            # print(pd.DataFrame(s.s['_temPagina_2']))
            gpd.GeoDataFrame.from_file(
                s.s['obstaculos']).boundary.plot(ax=ax, cmap='tab20')
            ax.set_xlim(-180, 180)
            ax.set_ylim(0, 90)
            ax.set_title('obstaculos geometry ')
            plt.grid(True)

        def cubierta_______(fig, x, y):

            ax = fig.add_axes([x, y, .3, .3], frameon=False)
            # ax.arrow(p0.x, p0.y, 0.0, 0.0, head_width=0.4,
            #          head_length=0.2, fc='r', ec='r')

            # xy = gpd.read_file("assets/geojson/mm.geojson")
            gpd.GeoDataFrame.from_file(s.s['FV']['outputs']['vv']['CUBIERTA']).boundary.plot(
                ax=ax, cmap='tab20', aspect=1)
            gpd.GeoDataFrame.from_file(s.s['FV']['outputs']['vv']['PANELES']).boundary.plot(
                ax=ax, aspect=1)
            sombras = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['SOMBRAS'])
            sombras[sombras['Layer'] == 'S0'].plot(
                ax=ax, color='grey', alpha=.5, aspect=1)

            gpd.GeoDataFrame.from_file(s.s['FV']['outputs']['vv']['PANELES']).iloc[[
                s.s['FV']['meta']['vv']['ip']]].geometry.centroid.plot(ax=ax, color='r', aspect=1)

            ax.axis('off')

        def perfilSombras__(fig, x, y):
            '''
            Dibuja el cielo, solsticios y terreno
            '''
            ax = fig.add_axes([x, y, .4, .1], frameon=False)
            df = pd.DataFrame(s.s["PVGIS_printhorizon"]["outputs"]
                              ["summer_solstice"]).set_index('A_sun(s)').plot(ax=ax)
            pd.DataFrame(s.s["PVGIS_printhorizon"]["outputs"]
                         ["winter_solstice"]).set_index('A_sun(w)').plot(ax=ax)

            df = pd.DataFrame(s.s["PVGIS_printhorizon"]["outputs"]
                              ["horizon_profile"]).set_index('A')
            df['H_shading'] = [float(x) for x in gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['PANELES']).loc[s.s['FV']['meta']['vv']['ip'], 'userhorizon'].split(',')]
            df = df[['H_shading', 'H_hor']]
            df.plot(ax=ax)

            ax.set_title('Horizon profile ')

            plt.grid(True)

            # ax.axis('off')

        def TablaInput_____(fig, x, y):
            '''
            radiacion
            '''
            ax = fig.add_axes([x, y, .3, .1], frameon=False)
            texto = f'''
    * Provided inputs:
    {json.dumps(s.s['PVGIS_PVcalcOpt']['inputs'], indent=2).replace("{", "").replace("}", "").replace(",", "").replace('"', "")}












    * Simulation outputs:
    {json.dumps(s.s['PVGIS_PVcalcOpt']['outputs']['totals']['fixed'], indent=2).replace("{", "").replace("}", "").replace(",", "").replace('"', "")}









            '''
            ax.text(0, 0, texto, va="top",  bbox=dict(
                boxstyle='round', facecolor='w', edgecolor='k'))
            ax.axis("off")

        def energy_________(fig, x, y):
            ax = fig.add_axes([x, y, .4, .1], frameon=False)
            pd.DataFrame(s.s['PVGIS_PVcalcOpt']['outputs']['monthly']
                         ['fixed']).set_index('month')[['E_m', 'H(i)_m']].plot.bar(ax=ax)

            ax.set_title(
                'Average monthly energy (kWh/mo) & global irradiation (kWh/m2/mo)')

            plt.grid(True)

        def mapaGeoJson____(fig, x, y):
            '''
            - [mapa geojson](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/countries)
            - dibuja en matplotlib un mapa facilmente
            '''
            lat, lon = 37.0, -4.2
            ax = fig.add_axes([x, y, .3, .3], frameon=False)
            mapa = gpd.read_file('assets/geojson/europe.geojson')
            # mapa = gpd.read_file('assets/geojson/georef-spain-municipio-millesime_andalucia.geojson')
            mapa.boundary.plot(ax=ax, linewidth=.5, alpha=.5)

            ax.plot([lon], [lat], 'ro')
            ax.set_title(
                f''' lat.:{round(lat, 2) },  lon.: {round(lon, 2)}  ''')
            ax.axis("off")


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
