
import pydeck as pdk
import numpy as np
import pandas as pd
import geopandas as gpd
import json
from types import SimpleNamespace
import streamlit as st
st.set_page_config(layout="wide")


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


def app():
    chart_data = pd.DataFrame(
        np.random.randn(2000, 2) / [5, 5] + [36.76, -4.4],
        columns=['lat', 'lon'])
    st.write(chart_data)

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=36.76,
            longitude=-4.4,
            zoom=7,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=chart_data,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=chart_data,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))


if __name__ == "__main__":
    s = _estado.json2_estado()
    app()
