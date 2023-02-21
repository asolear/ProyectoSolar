
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

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


class parameters:
    def parameters():
        # st.write(s.s['formularios']['outputs']['110_🧑 Cliente_⬜ formularioUnico.pdf'])
        parameters.json()

    def json():
        '''
        - para modificar el json
        '''
        Parameters,  = st.tabs(['Parameters'])
        # para insertar pruebas

        #
        col1, col2, col3 = Parameters.columns([1, 1, 4])
        g1s = list(s.s.keys())
        g1s = [lista for lista in g1s if not "__" in lista]
        g1s = [lista for lista in g1s if not lista[0] == '_']
        g1s = [lista for lista in g1s if not lista[0] == '_']
        g1 = col1.selectbox(" ", g1s,)

        g2s = list(s.s[g1].keys())
        g2s = [lista for lista in g2s if not "__" in lista]
        g2s = [lista for lista in g2s if not "outputs" in lista]
        g2s = [lista for lista in g2s if not "meta" in lista]
        g2 = col2.selectbox(" ", g2s,)

        g3s = list(s.s[g1][g2].keys())
        # g3s = [lista for lista in g3s if not "outputs" in lista]
        g3s = [lista for lista in g3s if not "Outputs" in lista]
        g3s = [lista for lista in g3s if not "__" in lista]
        g3s = [lista for lista in g3s if not lista[0] == '_']
        g3 = col3.selectbox(" ", g3s,)

        Edit, Visualizar = Parameters.tabs(['🖍  Edit', '👁 Visualize'])

        with Edit.form("aamy_form"):
            g4s = list(s.s[g1][g2][g3].keys())
            for i, g4 in enumerate(g4s):
                # st.write(type(s.s[g1][g2][g3][g4]))
                try:
                    globals()[g1+g2+g3+g4] = st.slider(
                        g4, 0.0, s.s[g1][g2][g3][g4] *
                        2.0+.01, s.s[g1][g2][g3][g4]
                    )
                except:
                    try:
                        globals()[g1+g2+g3+g4] = st.slider(
                            g4, 0, s.s[g1][g2][g3][g4]*2+1, s.s[g1][g2][g3][g4]
                        )
                    except:
                        try:
                            globals()[g1+g2+g3+g4] = st.text_input(
                                g4, s.s[g1][g2][g3][g4]
                            )
                        except:
                            None
            submitted = st.form_submit_button("Actualizar")
            if submitted:
                # actualiza los parametros
                for i, g1 in enumerate(g1s):
                    for i, g2 in enumerate(g2s):
                        for i, g3 in enumerate(g3s):
                            for i, g4 in enumerate(g4s):
                                try:
                                    s.s[g1][g2][g3][g4] = globals()[
                                        g1+g2+g3+g4]
                                except:
                                    None
                
                _estado._estado2json()
                # switch_page('Documentacion')
                st.experimental_rerun()
        Visualizar.json(s.s[g1][g2][g3], expanded=True)


def app():
    '''

    '''
    parameters.parameters()


if __name__ == "__main__":
    s = _estado.json2_estado()
    app()
