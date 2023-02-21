

def bbestado2json():
    '''
    al inicio se cargan los datos del json y al final se guardan de nuevo
    '''
    s.s['_fecha'] = datetime.datetime.now().strftime(
        " %d / %m / %Y - %H:%M")
    # guardar estado
    # json.dumps(s.s),mm.json
    with open("assets/json/mm.json", "w") as outfile:
        outfile.write(json.dumps(s.s))
    return

def bbnrel():
    '''
    para la simulacion con sam de NREL
    '''
    import PySAM.Pvwattsv8 as PV
    import PySAM.Grid as GRID
    import PySAM.Utilityrate5 as UR
    import PySAM.Cashloan as CL
    # variables glbales pero no estan ejecutada no tienen los outputs
    pv = PV.default("PVWattsResidential")
    grid = GRID.from_existing(pv, "PVWattsResidential")
    ur = UR.from_existing(pv, "PVWattsResidential")
    cl = CL.from_existing(pv, "PVWattsResidential")


def bbdxf2parametros():
    '''
    como entrada al programa se usa un dxf, el primero de la lista de los que haya en este directorio
    '''
    try:
        ifile = [x for x in list(os.listdir('assets/DXFs')) if (("dxf"  in x) & ("#" not in x) & ("_OUT" not in x) & ("~" not in x))][0]
        print(f''' \n\n\n DXF MFUENTE ........{ifile}\n\n''')
        # exit()
    except:
        print('\n\n\n\n!!!!!!!!!!!!!!  pon el DXF en este directorio \n\n\n\n\n')
        # exit()
        # ifile = "modelo/pp.dxf"
    return ifile


def bbjson2estado():
    '''
    al final de la funcion principal, se guarda el estado modificado con la funcion 
    'estado2json'.
    '''
    with open("assets/json/mm.json", "r") as f:
        s = json.load(f)
    s = SimpleNamespace(s=s)
    return s



def app():
    if 1:
        a = 1

        def SOLPOS_DIA():
            tz = 'Europe/Madrid'
            tz = 'Etc/Greenwich'
            lat, lon = 40.416673, -3.703770
            #!!!!  poner los minutos p[ara desplazar los analemas no a las horas en punto sino para que sea vrtical el del medio dia, como en el diagrama del IDAE]
            times = pd.date_range('2020-01-01 00:15:00',
                                  '2021-01-01 00:15:00', closed='left', freq='10min', tz=tz)
            solpos = solarposition.get_solarposition(times, lat, lon)
            solpos["coords"] = solpos[["azimuth",
                                       "apparent_elevation"]].values.tolist()
            solpos['geometry'] = solpos["coords"].apply(lambda x: Point(*x, ))
            return solpos

        solpos = SOLPOS_DIA()

        def pvgis_Hourly_radiation():
            '''
            Si las coordendas de la finca no coinciden con las de la radiacion , se descaragaa la nueva
            '''
            if (s.s['GEN']['Ubicacion']['_lng'] != s.s['PVGIS_seriescalc']['inputs']['location']['longitude']) | (s.s['GEN']['Ubicacion']['_lat'] != s.s['PVGIS_seriescalc']['inputs']['location']['latitude']):
                print(
                    ''' ... Cambada Ubicacion  ... descargando de PVGIS ra raciadilon de la nueva''')

                # meter bien los parametros para pvgis
                url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?outputformat=json"
                url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?outputformat=json"

                url = url + "&lat=" + str(s.s['GEN']['Ubicacion']['_lat'])
                url = url + "&lon=" + str(s.s['GEN']['Ubicacion']['_lng'])
                url = url + "&startyear=" + str(2020)
                url = url + "&endyear=" + str(2020)

                radiacion = requests.get(url).json()
                s.s['PVGIS_seriescalc'] = radiacion
            else:
                radiacion = s.s['PVGIS_seriescalc']

            return radiacion
        radiacion = pvgis_Hourly_radiation()

        def indicesolpos2indicepvgis():
            '''
            interpola mas valores de pvgis (horarios) al indice de solpos
            1 le pongo el indice de tiempo
            2 se le cambia la frecuencia 
            '''

            times = pd.date_range('2020-01-01 00:15:00',
                                  '2021-01-01 00:15:00', closed='left', freq='1h')
            radiacion_resampled = pd.DataFrame(radiacion['outputs']['hourly'])
            radiacion_resampled = radiacion_resampled.set_index(times)
            radiacion_resampled = radiacion_resampled.asfreq(
                freq='10min', method='ffill')
            return radiacion_resampled
        radiacion = indicesolpos2indicepvgis()
        # gdf['rad']=pd.DataFrame(radiacion['outputs']['hourly'])['H_sun'].to_list()

        def radiacion2solpos():
            '''
            los anade al geopandas para ahora hacer la interseccion con los obstaculos y ver cuanto cae la
            suma de la columna, sera el porcentaje de perdida por sombras ???
            '''
            solpos['radiacion'] = radiacion['G(i)']
            a = 1
            return solpos
        solpos = radiacion2solpos()

        def perdida_por_sombras():
            perdidas=0
            obstaculo=1
            return perdidas
        perdidas=perdida_por_sombras()

    texto = f'''
 ssidea usar la interseccion entre los geodataframe de obstaculos y posicion del sol
1.- df solpos con las posiciones del sol como geometry Point, puedo hacerlo con la resolucion que quiera inicialmente cada
hora 8784

2.- df bajado de pvgis con los datos de irradiacion para coo maxima frecuencia de 1 h, lo suyo seria poder inerpolar otros
a 6 valores para poner mas puntos


                '''


    if 0:
        a = 1
        ##########################   VISUALIZACION   #################################################

    def visualizacion():
        with PdfPages(os.path.abspath(__file__)[:-3]+".pdf") as pdf:
            fig, axx = plt.subplots(figsize=(21/2.54*2, 29.7/2.54))

            def notas():

                ax = fig.add_axes([.16, .88, 0, 0], frameon=False)
                ax.text(0, 1, texto, va="top",   wrap=True, fontsize=6)
                ax.axis("off")
            notas()

            def grafico2():
                ax = fig.add_axes([.16, .4, .4, .4], frameon=False)
                gpd.GeoDataFrame(solpos.geometry).plot(ax=ax, markersize=.051)
                # ax.axis("off")
            grafico2()

            def grafico():
                ax = fig.add_axes([.16, .1, .3, .3], frameon=False)


                ax.axis("off")
            grafico()




            axx.axis('off')
            pdf.savefig()
            plt.close()

    visualizacion()

    def estado2json():
        '''
        al inicio se cargan los datos del json y al final se guardan de nuevo
        '''
        s.s['_fecha'] = datetime.datetime.now().strftime(
            " %d / %m / %Y - %H:%M")
        # guardar estado
        # json.dumps(s.s),mm.json
        with open("assets/json/mm.json", "w") as outfile:
            outfile.write(json.dumps(s.s))
        return
    estado2json()


if __name__ == "__main__":

    import matplotlib
    import datetime
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
    import matplotlib.image as image
    from matplotlib.transforms import IdentityTransform
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import *
    from shapely.affinity import *
    from shapely.ops import *

    import os
    from shapely import affinity
    from PIL import Image
    from io import BytesIO
    # Librerías y módulos necesarios
    import matplotlib.pyplot as plt
    import qrcode
    # estado
    import json
    from types import SimpleNamespace
    # NREL
    import PySAM.Pvwattsv8 as PV
    import PySAM.Grid as GRID
    import PySAM.Utilityrate5 as UR
    import PySAM.Cashloan as CL
    import math
    import utm
    import numpy as np
    import sys
    import tomli
    import pathlib
    import glob
    from pvlib import solarposition
    import requests

    import contextily as cx
    import rasterio
    from rasterio.plot import show as rioshow
    import geopandas
    import contextily as cx
    import time

    bbnrel()
    s = bbjson2estado()
    ifile = bbdxf2parametros()
    app()
    bbestado2json()
