

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
        ifile = [x for x in list(os.listdir('assets/dxf')) if (("dxf"  in x) & ("#" not in x) & ("_OUT" not in x) & ("~" not in x))][0]
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

        tz = 'Europe/Madrid'
        tz = 'Etc/Greenwich'
        lat, lon = 40.416673, -3.703770
        #!!!!  poner los minutos p[ara desplazar los analemas no a las horas en punto sino para que sea vrtical el del medio dia, como en el diagrama del IDAE]
        times = pd.date_range('2022-01-01 00:15:00',
                            '2023-01-01 00:15:00', closed='left', freq='H', tz=tz)

        # remove nighttime
        fig, ax = plt.subplots(figsize=(22, 11))
        fechas=[ '2022-06-21', '2022-08-21', '2022-10-21', '2022-12-21']
        dias = []
        for date in pd.to_datetime(fechas):
            times = pd.date_range(date, date+pd.Timedelta('24h'), freq='1h', tz=tz)
            solpos = solarposition.get_solarposition(times, lat, lon)
            # solpos = solpos.loc[solpos['apparent_elevation'] > -40, :]
            if 1:
                solpos["geometry"] = solpos[["azimuth",
                                            "apparent_elevation"]].values.tolist()
                dia = LineString(solpos["geometry"].apply(lambda x: (*x, )))
                dias.append(dia)


        gdf = gpd.GeoDataFrame(geometry=dias)
        # gdf.plot(ax=ax)

        # 
        fechas=[ '2022-06-21',  '2022-12-21']

        aee = pd.Series()
        for date in pd.to_datetime(fechas):
            times = pd.date_range(date, date+pd.Timedelta('24h'), freq='1h', tz=tz)
            solpos = solarposition.get_solarposition(times, lat, lon)

            # solpos = solpos.loc[solpos['apparent_elevation'] > -40, :]
            if 1:
                solpos["geometry"] = solpos[["azimuth",
                                            "apparent_elevation"]].values.tolist()
                aee=pd.concat([aee,solpos["geometry"] ])      


        df=aee.copy().to_frame(name='geometry')
        # print(df[df.index.hour==8])

        hh=[]
        for hora in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
            h=LineString(df[(df.index.hour==hora)]["geometry"].apply(lambda x: (*x, )))
            hh.append(h)
        hh.append(LineString([(0, 0),( 360, 0)]))
        gdfh = gpd.GeoDataFrame(geometry=hh)
        gdf=pd.concat([gdf,gdfh])

        # 

        # poligonizando los sectores
        polygons = list(polygonize(unary_union(gdf.geometry)))
        gdfP=gpd.GeoDataFrame(geometry=polygons)
        





    if 0:
        a = 1
        ##########################   VISUALIZACION   #################################################

    def visualizacion():
        with PdfPages(os.path.abspath(__file__)[:-3]+".pdf") as pdf:
            fig, axx = plt.subplots(figsize=(21/2.54*2, 29.7/2.54))

            def cabecera():
                texto = f'''
                        Latitud     {s.s["GEN"]["Ubicacion"]["_lat"]}
                        Longitud    {s.s["GEN"]["Ubicacion"]["_lng"]}
                '''

                ax = fig.add_axes([.16, .99, 0, 0], frameon=False)
                ax.text(0, 1, texto, va="top",   wrap=True,
                        fontfamily="monospace", fontsize=6)
                ax.axis("off")
            cabecera()

            def notas():
                texto = f'''
este es muy buen ejemplo para crear poligonos de los cruces delineas de una forma muy simple


                '''

                ax = fig.add_axes([.16, .88, 0, 0], frameon=False)
                ax.text(0, 1, texto, va="top",   wrap=True,
                        fontfamily="monospace", fontsize=6)
                ax.axis("off")
            notas()

            def grafico2():
                ax = fig.add_axes([.16, .4, .4, .4], frameon=False)
                gdfP.boundary.plot(ax=ax,cmap='tab20')
                
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
