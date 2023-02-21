
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
        # #print(os.path.realpath(os.path.dirname(__file__)))
        with open("_estado.json", "r") as f:
            s = json.load(f)
        s = SimpleNamespace(s=s)

        return s

    def _estado2json():
        '''
        Escribo el JSON en disco como datos 'json' s.s['xxxxx']
        '''

        with open("_estado.json", "w") as f:
            f.write(json.dumps(s.s))
        return



class GRAFICOS:
    def Draw(Draw):
        ff = Draw.selectbox("Draws", list(
            s.s['FV']['outputs']['vv'].keys()))
        gf = gpd.GeoDataFrame.from_file(s.s['FV']['outputs']['vv'][ff])
        geo, Table = Draw.tabs(['geo', 'Table'])
        geo.write(gf.crs)
        try:
            fig, axx = plt.subplots(figsize=(21/2.54*1, 29.7/2.54))
            gf.boundary.plot(ax=axx, cmap='tab20', aspect=1)
            axx.axis('off')
            geo.pyplot(fig)
        except:
            fig, axx = plt.subplots(figsize=(21/2.54*1, 29.7/2.54))
            gf.plot(ax=axx, cmap='tab20', aspect=1)
            axx.axis('off')
            geo.pyplot(fig)
        #


        Table.write(gf)

    def pvgis(pvgis):

        kk = s.s.keys()
        kk = [lista for lista in kk if "PVGIS" in lista]

        ff = pvgis.selectbox("pvgis", list(kk))
        fig, axx = plt.subplots(figsize=(21/2.54*1, 29.7/2.54))
        try:
            data = s.s[ff]['outputs']['monthly']['fixed']
            pd.DataFrame(data).plot(ax=axx, cmap='tab20')
            pvgis.pyplot(fig)
        except:
            try:
                data = (s.s[ff]['outputs']['months_selected'])
                pd.DataFrame(data).plot(ax=axx, cmap='tab20')
                pvgis.pyplot(fig)
            except:
                try:
                    data = (s.s[ff]['outputs']['horizon_profile'])
                    pd.DataFrame(data).plot(ax=axx, cmap='tab20')
                    pvgis.pyplot(fig)
                except:
                    try:
                        data = (s.s[ff]['outputs']['hourly'])
                        pd.DataFrame(data).plot(ax=axx, cmap='tab20')
                        pvgis.pyplot(fig)
                    except:
                        None

    def sam(sam):

        g1s = s.s['sam'].keys()
        g1 = sam.selectbox("sam", list(g1s))

        g2s = s.s['sam'][g1]['Outputs'].keys()
        # g2s = [lista for lista in g2s if "monthly" in lista]
        g2 = sam.selectbox("sam", list(g2s))
        fig, axx = plt.subplots(figsize=(21/2.54*1, 29.7/2.54))

        try:
            data = [s.s['sam'][g1]['Outputs'][g2]]
            pd.DataFrame(data).T.plot(ax=axx)
            sam.pyplot(fig)
            # sam.DataFrame(pd.DataFrame(data).T)
        except:
            None


def app():
    '''

    '''
    Draw, pvgis, sam = st.tabs(['Draws', 'pvgis', 'sam'])

    # EDITAR_JSON.json(Parameters)
    GRAFICOS.Draw(Draw)
    GRAFICOS.pvgis(pvgis)
    GRAFICOS.sam(sam)


if __name__ == "__main__":
    s = _estado.json2_estado()
    app()
