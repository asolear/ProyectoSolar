
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


class calculos:
    '''
    calculos
    '''
    def calculos():
        tt = time()
        ttt(tt)
        calculos.pvgis.pvgis()
        ttt(tt)
        calculos.calculos_PVcalc()
        ttt(tt)
        calculos.sam()
        ttt(tt)

    def calculos_PVcalc():
        '''
        ini calculos
        '''

        calculos.ini()
        calculos.perfil_sombras.perfilXpanel()

    def ini():
        '''
        en la termial se indica la funcion que se ha ejecutado y su tiempo de ejecucino de cada funcion
        '''
        clc_edificio

        s.s['FV']['meta']['vv']['fecha'] = datetime.datetime.now().strftime(
            " %d / %m / %Y - %H:%M")
        s.s['FV']['meta']['vv']['carpeta'] = os.path.realpath(
            os.path.dirname(__file__))

    class perfil_sombras:
        def perfilXpanel():
            '''
            para cada panel calculo el perfil de horizone que luego se pasara a la api de pvgis
            '''
            for ip, rp in gpd.GeoDataFrame.from_file(s.s['FV']['outputs']['vv']['PANELES']).iterrows():
                # #print(ip)
                s.s['FV']['meta']['vv']['ip'] = ip
                calculos.perfil_sombras.perfil(
                    calculos.perfil_sombras.coordenadas())

        def perfil(coordenadas):
            ''' 
            a partir de las coordenadas crea las geometrias de los obstaculos
            '''
            clc_edificio
            ss = []
            for io, ro in coordenadas.groupby(level=0):

                # para eleimnar los obstaculos que se crucen justo al norte, porque distorsiona el perfil_sombras
                if max(ro.az)-min(ro.az) < 250:
                    pp = Polygon(list(map(tuple, np.asarray(ro[['az', 'el']])))).union(
                        LineString([(min(ro.az)-1e-4, 0), (max(ro.az)+1e-4, 0)])).convex_hull

                    ss.append(
                        {
                            "geometry": pp,
                            "Layer": "obstaculos",
                        }
                    )

            gff = gpd.GeoDataFrame(ss)
            s.s['FV']['meta']['vv']['global1'] = gff.to_json()
            #  esta globalizacion de la variable es para poder depurar aparte
            gff = gpd.GeoDataFrame.from_file(
                s.s['FV']['meta']['vv']['global1'])
            # el poigono pp es un artificio para que funcione bien el unary union de todos los bstaculos, no funciona si hay separacion
            pp = Polygon(
                [[-180, 0], [180, 0], [180, .1], [-180, .1], [-180, 0]])
            gg = gpd.GeoDataFrame(
                {'id': 999, 'Layer': 'obstaculos', 'geometry': [pp]})
            gff = pd.concat([gff, gg], ignore_index=True)
            #
            gf = gff['geometry'].unary_union.buffer(1e-4).buffer(-1e-4)
            hh = pd.DataFrame(
                sorted(pd.DataFrame(mapping(gf)['coordinates']).T[0])).set_index(0)
            hh = hh[~hh.index.duplicated(keep='first')]
            horizonte = pd.DataFrame(s.s["PVGIS_printhorizon"]["outputs"]
                                     ["horizon_profile"]).set_index('A')
            # con la misma resolucion que pvgis
            hh_resampled = hh.reindex(hh.index.union(horizonte.index)).interpolate(
                "values").fillna(0)[1].loc[horizonte.index]
            # los mismos decimales que vienen de pvgis
            horizonte['obstaculo'] = np.around(
                np.array(hh_resampled.values), 1)
            # el maximo entre el horizonte de pvgis  y los obstaculos cercanos
            horizonte['perfil'] = horizonte.max(axis=1)
            # para pasarlo al formato que admite la api de pvgis
            userhorizon = ','.join([str(x)
                                   for x in horizonte['perfil'].values])

            paneles = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['PANELES'])

            paneles.loc[s.s['FV']['meta']['vv']
                        ['ip'], 'userhorizon'] = userhorizon

            s.s['FV']['outputs']['vv']['PANELES'] = paneles.to_json()
            # s.s['FV']['inputs']['vv']['PANELES'] = 'fgdsfgkkk'

            #

            return

        def asSpherical(xyz):
            '''
            para pasar de cartesioano a esfrica
            el truco es que x=-este, y=-norte
            '''
            x = xyz[0]
            y = xyz[1]
            z = float(xyz[2])
            r = sqrt(x*x + y*y + z*z)
            theta = asin(z/r)*180 / pi  # to degrees
            phi = (atan2(-x, -y)*180 / pi)
            return theta, phi

        def coordenadas():
            '''
            - a partir de las coordendas catesianas de cada uno de los vertices obtiene las esfericas
            '''
            clc_edificio
            paneles = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['PANELES'])
            rc = paneles.iloc[[s.s['FV']['meta']['vv']['ip']]]

            p0 = rc.geometry.centroid
            # para cada cubierta por encima del nivel del panel
            gf = gpd.read_file("assets/geojson/mm.geojson")
            xy = gf[(gf['Layer'] == 'CUBIERTA')]
            xy = xy[(xy['zz'].astype(float) > rc.zz.values[0])]
            coordenadas = pd.DataFrame()
            for ic, rc in xy.iterrows():
                # # #print(rc.zz-zz_paneles)
                dfn = pd.DataFrame(
                    list(rc.geometry.exterior.coords)[:-1], columns=['x', 'y'])
                dfn.index = dfn.index.rename('V')
                dfn['B'] = ic
                dfn = dfn.set_index(['B', dfn.index])
                dfn['z'] = rc.zz
                coordenadas = pd.concat(
                    [coordenadas, dfn], ignore_index=False)
            # y las paso a coordenadas esfericas
            for i, r in coordenadas.iterrows():
                coordenadas.loc[i, ['el', 'az']] = calculos.perfil_sombras.asSpherical(
                    [r.x-p0.x, r.y-p0.y, r.z])
            s.s['FV']['meta']['vv']['_coordenadas'] = coordenadas.to_json()

            return coordenadas

    class pvgis:
        '''
        - de PVGis me descargo la radiacion horaria de un anio
            - [PVGIS](https://joint-research-centre.ec.europa.eu/pvgis-online-tool/getting-started-pvgis/api-non-interactive-service_en)
            - como la llamada API es lenta intento no repetirla
                - primero con un try para ver si esta algun valor (lo hara la primera vez)
                - Si las coordendas de la finca no coinciden con las de la radiacion , se descaragaa la nueva
        '''
        def pvgis():
            '''
            APIs a PVgis
            '''

            try:  # prueba si enla base de datos hay
                s.s['PVGIS_PVcalcOpt']['inputs']['location']['longitude']

            except:
                calculos.pvgis.PVcalcOpt()
                calculos.pvgis.seriescalc()
                calculos.pvgis.tmy()
                calculos.pvgis.printhorizon()

            if (s.s['FV']['inputs']['Ubicacion']['_lng'] != s.s['PVGIS_PVcalcOpt']['inputs']['location']['longitude']) | (s.s['FV']['inputs']['Ubicacion']['_lat'] != s.s['PVGIS_PVcalcOpt']['inputs']['location']['latitude']):

                # #print(
                # ''' ... Cambada Ubicacion  ... descargando de PVGIS ra raciadilon de la nueva''')
                calculos.pvgis.PVcalcOpt()
                calculos.pvgis.seriescalc()
                calculos.pvgis.tmy()
                calculos.pvgis.printhorizon()

            else:
                None

        def PVcalc():
            '''
            - https://re.jrc.ec.europa.eu/api/PVcalc?lat=45&lon=8&peakpower=0.5&loss=14
            - Grid-connected & Tracking PV systems
            '''
            clc_edificio
            url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?outputformat=json"
            url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?outputformat=json"
            url = url + "&lat=" + \
                str(s.s['FV']['inputs']['Ubicacion']['_lat'])
            url = url + "&lon=" + \
                str(s.s['FV']['inputs']['Ubicacion']['_lng'])
            # !!! ojo que el 2020 es bisiesto
            url = url + "&peakpower=0.5"
            url = url + "&loss=14"
            url = url + "&angle=0.0"
            url = url + "&aspect=0.0"
            # url = url + "&userhorizon=0"
            s.s['PVGIS_PVcalc'] = requests.get(url).json()

        def PVcalcOpt():
            '''
            - https://re.jrc.ec.europa.eu/api/PVcalc?lat=45&lon=8&peakpower=0.5&loss=14
            - HOURLY RADIATION DATA
            '''
            clc_edificio
            url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?outputformat=json"
            url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?outputformat=json"
            url = url + "&lat=" + \
                str(s.s['FV']['inputs']['Ubicacion']['_lat'])
            url = url + "&lon=" + \
                str(s.s['FV']['inputs']['Ubicacion']['_lng'])
            # !!! ojo que el 2020 es bisiesto
            url = url + "&peakpower=0.5"
            url = url + "&loss=14"
            url = url + "&optimalangles=1"
            s.s['PVGIS_PVcalcOpt'] = requests.get(url).json()

        def seriescalc():
            '''
            - HOURLY RADIATION DATA
            '''
            clc_edificio
            url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?outputformat=json"
            url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?outputformat=json"
            url = url + "&lat=" + \
                str(s.s['FV']['inputs']['Ubicacion']['_lat'])
            url = url + "&lon=" + \
                str(s.s['FV']['inputs']['Ubicacion']['_lng'])
            # !!! ojo que el 2020 es bisiesto
            url = url + "&startyear=" + str(2019)
            url = url + "&endyear=" + str(2019)
            s.s['PVGIS_seriescalc'] = requests.get(url).json()

        def tmy():
            '''
            - TMY
            - [https://re.jrc.ec.europa.eu/api/tmy?outputformat=json&lat=45&lon=8](https://re.jrc.ec.europa.eu/api/tmy?outputformat=json&lat=45&lon=8)
            '''
            clc_edificio
            url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?outputformat=json"
            url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?outputformat=json"
            url = "https://re.jrc.ec.europa.eu/api/v5_2/tmy?outputformat=json"
            url = url + "&lat=" + \
                str(s.s['FV']['inputs']['Ubicacion']['_lat'])
            url = url + "&lon=" + \
                str(s.s['FV']['inputs']['Ubicacion']['_lng'])

            s.s['PVGIS_tmy'] = requests.get(url).json()

        def printhorizon():
            '''
            - printhorizon
            - [https://re.jrc.ec.europa.eu/api/printhorizon?outputformat=json&lat=45&lon=8](https://re.jrc.ec.europa.eu/api/printhorizon?outputformat=json&lat=45&lon=8)
            '''
            clc_edificio
            url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?outputformat=json"
            url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?outputformat=json"
            url = "https://re.jrc.ec.europa.eu/api/v5_2/tmy?outputformat=json"
            url = "https://re.jrc.ec.europa.eu/api/v5_2/printhorizon?outputformat=json"
            url = url + "&lat=" + \
                str(s.s['FV']['inputs']['Ubicacion']['_lat'])
            url = url + "&lon=" + \
                str(s.s['FV']['inputs']['Ubicacion']['_lng'])

            s.s['PVGIS_printhorizon'] = requests.get(url).json()

    def sam():
        print(os.path.basename(__file__))
        import PySAM.MhkTidal as MT
        import PySAM.Pvwattsv8 as PV
        import PySAM.Grid as GRID
        import PySAM.Utilityrate5 as UR
        import PySAM.Cashloan as CL

        pv = PV.default("PVWattsResidential")
        grid = GRID.from_existing(pv, "PVWattsResidential")
        ur = UR.from_existing(pv, "PVWattsResidential")
        cl = CL.from_existing(pv, "PVWattsResidential")
        #

        pv.SolarResource.solar_resource_file = "assets/sam/tmy0.epw"
        #
        pv.execute(0)
        grid.execute(0)
        # parar la simulacion y meterle las penalizaciones por exceso Pc ( demanda=carga-generacion )
        ur.execute(0)
        cl.execute(0)

        # st.write(pv.export())
        s.s['sam'] = {}
        s.s['sam']["pv"] = pv.export()
        s.s['sam']["grid"] = grid.export()
        s.s['sam']["ur"] = ur.export()
        s.s['sam']["cl"] = cl.export()


class clc_edificio:
    def clc_edificio():
        clc_edificio.clc1()
        clc_edificio.edificio.a_dxf2gpd()                    # lee el dxf de entrada
        clc_edificio.edificio.b_parametrosDXF2ss()           # lee los paramtros
        clc_edificio.edificio.c_DXF2polygonize()
        # asociar las alguraa a los poligonos
        clc_edificio.edificio.d_ZZ()
        # calcula las sombras para el SI
        clc_edificio.edificio.e_SOMBRAS()
        clc_edificio.edificio.f_ENVELOPES()
        clc_edificio.edificio.g_PANELES_ENVOLVENTE()
        clc_edificio.edificio.h_PANELES()

    def clc1():
        '''
                en la termial se indica la funcion que se ha ejecutado y su tiempo de ejecucino de cada funcion
                '''
        clc_edificio

        # s.s['FV']['meta']['vv']['fecha'] = datetime.datetime.now().strftime(
        #     " %d / %m / %Y - %H:%M")
        # s.s['FV']['meta']['vv']['carpeta'] = os.path.realpath(
        #     os.path.dirname(__file__))

    class edificio():

        def a_dxf2gpd():
            '''
            ### 1./ Paso de dxf a geopandas
            - lee el primer dxf que haya en el assets/DXFs
            - se deben haber incluido las capas
                - FV identificando las superficies donde iran las placas
                - PARAMETROS indicando los modelos de los componentes del generador como en el ejm

                        [inversor]
                        Modelo=" Fronius Symo 5.0-3-M Trif"
                        Pdco= 10000.0
                        Cantidad_MPPTs= 2
                        Vdco= 380
                        Vdcmax= 480
                        Idcmax= 16.0
                        Iccmax= 24.0
                        Mppt_low= 150
                        Mppt_high= 800
                        Paco= 5000
                        Iac= 230


                        [panel]
                        Modelo= "Jiiiiimko 400"
                        Pmp= 400
                        Largo= 2
                        Ancho= 1.5
                        Peso= 25
                        Voc= 49.6
                        Vmp= 41.2
                        Isc= 11.1
                        Imp= 10.56
                        Asc= 0.05
                        Boc= -0.28
                        Gmp= -0.36



                        [estructura]      
                        # variable=7777
                        Modelo= "cemntako"
                        Inclinacion= 10.0 # 10,12,14
                        Peso= 405.0
                        Lastre= 49.6


                        [Ubicacion]
                        Parcela1= "9989703UF6598N"
                        Parcela= "prueba"
                        Parcela3= "dxf_00"
                        _Nvecinos= 44
                        _lat= 36.730368543107275
                        _lng= -4.46829098578932
                        Az_max= 20.0
                        _Az= 0.0
                        _kwp= 39.29
                        Sombra_max= 0
                        AlturaXplanta= 3.0
                        _Npaneles= 97
                        _ddy= 1.2575425430070026
                        _pyi= 0.9820728078915534
                        _h= 0.5669999999999998
                        _horas_azimut= [4, 3, 2, 1, 0]


            '''
            try:
                ifile = [x for x in list(os.listdir('assets/DXFs'))]
                ifile = [lista for lista in ifile if "dxf" in lista]
                ifile = [lista for lista in ifile if not "_OUT" in lista]
                ifile = [lista for lista in ifile if not "~" in lista][0]
                # if (("dxf" in x) & ("#" not in x) & ("_OUT" not in x) & ("~" not in x))][0]
                print(f''' \n\n\n DXF MFUENTE ........{ifile}\n\n''')

                s.s['FV']['outputs']['vv']['gf_dxf'] = gpd.read_file(
                    'assets/DXFs/'+ifile).to_json()

            except:
                print(
                    '\n\n\n\n!!!!!!!!!!!!!!  no hay ningun DXF en el presente directorio \n\n\n\n\n')

        def b_parametrosDXF2ss():
            '''
            ### dxf.PARAMETROS.txt >>> pd
            primero ha cargado los parametros del json, pero si se han pasado por el dxf, prevaleceran estos
            los parametros introducidos como texto en el dxf
            ['inversores','paneles','soportes']
            '''
            # #print('------------------------'+sys._getframe().f_code.co_name)
            try:
                gg = gpd.GeoDataFrame.from_file(
                    s.s['FV']['outputs']['vv']['gf_dxf'])
                parametros = gg[gg["Layer"] == 'PARAMETROS']["Text"].to_list()[
                    0]
                s.s['FV']['inputs'] = tomli.loads(parametros)
                s.s['FV']['inputs']['Ubicacion']['lat'] = 6.730368543107275
                s.s['FV']['inputs']['Ubicacion']['lng'] = -4.46829098578932
            except:
                parametros = ''
                # #print('No se han podido cargar los parametros del DXF')
            return parametros

        def c_DXF2polygonize():
            '''
            ### paso polilineas a poligonos cerrados
            - hago las interseccion con los textos y 
                - asigno zz a cada poligono
                - asigno las cubiertas usadas para paneles
            '''
            # #print('------------------------'+sys._getframe().f_code.co_name)
            gg = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['gf_dxf'])
            gg_dxf_polygon, dangles, cuts, invalids = polygonize_full(
                gg["geometry"])
            gg_dxf_polygon_explode = gpd.GeoDataFrame(geometry=[gg_dxf_polygon]).explode(
                index_parts=True
            )
            gg_dxf_polygon_explode = gg_dxf_polygon_explode.droplevel(level=0)
            gg_dxf_polygon_explode["Layer"] = "CUBIERTA"
            gg = pd.concat([gg_dxf_polygon_explode, gg], ignore_index=True)
            #  Y ASOCIO A CADA POLIGONO SU TEXTO
            for i, r in gg[gg["Layer"] == "CUBIERTA"].iterrows():
                for i_ee, r_ee in gg[gg["Layer"] == "PG-AA"].iterrows():
                    if r_ee.geometry.intersection(r.geometry):
                        gg.loc[i, "Text"] = r_ee.Text

            #  Y ASOCIO A CADA POLIGONO la insalacion FV
            gg['FV'] = 0
            for i, r in gg[gg["Layer"] == "CUBIERTA"].iterrows():
                for i_ee, r_ee in gg[gg["Layer"] == "FV"].iterrows():
                    if r_ee.geometry.intersection(r.geometry):
                        gg.loc[i, "FV"] = 1

            gg = gg[['Layer', 'geometry', 'Text', 'FV']]
            gg = gg[gg['Layer'].isin(['CUBIERTA'])]

            gg = gg.fillna("")

            s.s['FV']['outputs']['vv']['CUBIERTA'] = gg.to_json()

        def d_ZZ():
            '''
            ### paso las alturas de pisos en numeros romanos a metos, 
            - si el codigo no es un numero decimal veo si es un numero romano y si no asigno cero
            '''
            # #print('------------------------'+sys._getframe().f_code.co_name)
            gg = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['CUBIERTA'])
            # https://www.catastro.meh.es/documentos/formatos_intercambio/FICCcodigosUnificado07.pdf
            r2d = dict(zip(["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"], [
                i for i in range(11)][1:]))

            # el ultim elemento de la cadena es la altura, expresada en numeros romanos o metros o tambien TZA
            gg['planta'] = gg.Text.apply(
                lambda x: x.split("+")[-1])
            gg["zz"] = gg["planta"].map(
                r2d) * s.s['FV']['inputs']["Ubicacion"]["AlturaXplanta"]
            # el resto lopongo a cero
            gg["planta"] = pd.to_numeric(gg["planta"], errors="coerce")
            # anado la altura de la cubierta a la del obstaculo
            for i, r in gg[gg["planta"].notnull()].iterrows():
                # compruebo en que poligono esta
                for ic, rc in gg[gg["planta"].isnull()].iterrows():
                    if not r["geometry"].intersection(rc["geometry"]).is_empty:
                        # gg.loc[i, "zz"] = r.zz + rc.planta
                        gg.loc[i, "zz"] = rc.zz+r.planta

            gg = gg.fillna(0)
            gg = gg[['Layer', 'geometry', 'Text', 'zz', 'FV']]
            s.s['FV']['outputs']['vv']['CUBIERTA'] = gg.to_json()

        def e_SOMBRAS():
            '''
            ### para 2 h +- del medio dia
            para calcular las sombras uso el convexhull del poligono su proyectado para cada azimut y zz
            creo la capa
            SOMBRA_<azimut> ee=<indice de la cubierta> zz=<altura>
            '''
            # #print('------------------------'+sys._getframe().f_code.co_name)
            gg = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['CUBIERTA'])

            sombras = []
            zzs = (
                gg[(gg["Layer"] == "CUBIERTA")]
                .drop_duplicates(subset="zz", keep="first")["zz"]
                .tolist()
            )
            for zz in zzs:
                for i, r in gg[(gg["Layer"] == "CUBIERTA") & (gg["zz"] > zz)].iterrows():
                    CUBIERTAS = unary_union(
                        list(gg[(gg["Layer"] == "CUBIERTA") &
                                (gg["zz"] > zz)]["geometry"])
                    )
                    for azimut in s.s['FV']['inputs']["Ubicacion"]["_horas_azimut"]:
                        # for azimut in [0]:

                        yoff = round(
                            (r.zz - zz)
                            * (1 / np.tan(np.pi * (63 - abs(azimut * 2) -
                                                   s.s['FV']['inputs']['Ubicacion']['lat']) / 180)),
                            2,
                        )
                        xoff = yoff * np.sin(np.pi * (azimut * 20 / 180))
                        # tarde
                        sombrat = translate(
                            r["geometry"], xoff=xoff, yoff=yoff)
                        sombrat = (
                            r["geometry"].union(
                                sombrat).convex_hull.difference(CUBIERTAS)
                        )
                        # manana
                        sombram = translate(
                            r["geometry"], xoff=-xoff, yoff=yoff)
                        sombram = (
                            r["geometry"].union(
                                sombram).convex_hull.difference(CUBIERTAS)
                        )

                        sombra = sombrat.union(sombram)

                        sombras.append(
                            {
                                "Layer": "SOMBRAS"+str(azimut),
                                "geometry": sombra,
                                "zz": zz,
                                # "Text": i,
                            }
                        )
            df = gpd.GeoDataFrame(sombras)

            gg = pd.concat([gg, df], ignore_index=True)
            # gg.drop(['Text', 'zz'], axis=1)

            '''
            para unificar todas las sombras por hora
            '''
            # #print('------------------------'+sys._getframe().f_code.co_name)
            # para unir todas las sombras por hora

            dfS = gpd.GeoDataFrame()
            for azimut in s.s['FV']['inputs']["Ubicacion"]["_horas_azimut"]:

                ss = gg[(gg['Layer'].isin(['SOMBRAS'+str(azimut)]))].unary_union
                df = gpd.GeoDataFrame(geometry=[ss])
                df['Layer'] = 'S'+str(azimut)
                dfS = pd.concat([dfS, df], ignore_index=True)

                # borrarlas
                gg.drop(
                    gg[(gg['Layer'].isin(['SOMBRAS'+str(azimut)]))].index, inplace=True)
            # # #print(gg)
            s.s['FV']['outputs']['vv']['SOMBRAS'] = dfS.to_json()

        def f_ENVELOPES():
            '''
            ### poligono rectangular que contiene la superfice a poner paneles
            los envolventes de los poligonos donde iran la placas
            '''
            # #print('------------------------'+sys._getframe().f_code.co_name)
            gg = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['CUBIERTA'])

            pps = []
            # for i, r in gg[gg["Layer"] == "fv"].iterrows():
            for i, r in gg[gg["FV"] == 1].iterrows():
                #############   CUBIERTAICIE #######################
                # funcion para mover el orden de los vertices de la envolvente
                def rl(a, b):
                    return a[b: len(a)] + a[0:b]

                # _estado inicial
                pw = r.geometry.minimum_rotated_rectangle
                x, y = pw.exterior.coords.xy
                angulo = degrees(
                    atan2(list(y)[1] - list(y)[0],
                          list(x)[1] - list(x)[0])
                )
                while (angulo > 45) or (angulo < -45):
                    pw = Polygon(
                        list(zip(rl(x.tolist(), 1), rl(y.tolist(), 1))))
                    x, y = pw.exterior.coords.xy
                    angulo = degrees(
                        atan2(list(y)[1] - list(y)[0],
                              list(x)[1] - list(x)[0])
                    )

                if s.s['FV']['inputs']["estructura"]["Inclinacion"] == 0:
                    desorientacion_max = 45
                else:
                    desorientacion_max = s.s['FV']['inputs']["Ubicacion"]["Az_max"]

                if (angulo > desorientacion_max) or (angulo < -desorientacion_max):
                    pw = r.geometry.envelope
                    x, y = pw.exterior.coords.xy
                    angulo = degrees(
                        atan2(list(y)[1] - list(y)[0],
                              list(x)[1] - list(x)[0])
                    )

                pps.append(
                    {
                        "geometry": pw,
                        "Layer": "ENVELOPES",
                        "zz": r.zz
                    }
                )
            df = gpd.GeoDataFrame(pps)
            # gg = pd.concat([gg, df], ignore_index=True)
            df = df.fillna("")
            s.s['FV']['outputs']['vv']['ENVELOPES'] = df.to_json()
            return

        def g_PANELES_ENVOLVENTE():
            '''
            ### llena la envolvente de pane
            pone una maya de panaeles en cada envolvente
            '''
            # #print('------------------------'+sys._getframe().f_code.co_name)
            if 1:  # valores previos
                py, px, garra = (
                    float(s.s['FV']['inputs']["panel"]["Ancho"]),
                    float(s.s['FV']['inputs']["panel"]["Largo"]),
                    float(s.s['FV']['inputs']["estructura"]["garra"]),
                )
                inclinacion = float(s.s['FV']['inputs']
                                    ["estructura"]["Inclinacion"])
                pyi = py * np.cos(inclinacion * np.pi / 180)
                panel_modelo = Polygon([(0, 0), (px, 0), (px, pyi), (0, pyi)])

                # para situar los paneles
                #         con la inclinacion
                # separacione entre modulos
                lat = float(s.s['FV']['inputs']["Ubicacion"]["_lat"])
                h = py * np.sin(inclinacion * np.pi / 180)
                ddy = h * (1 / np.tan((61 - lat) * np.pi / 180))

            #
            pps = []
            gg = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['ENVELOPES'])
            for i, r in gg.iterrows():
                x, y = r.geometry.exterior.coords.xy

                angulo = degrees(
                    atan2(list(y)[1] - list(y)[0],
                          list(x)[1] - list(x)[0])
                )
                #  para rellenar la plantilla de paneles
                lados = (
                    Point(x[0], y[0]).distance(Point(x[1], y[1])),
                    Point(x[0], y[0]).distance(Point(x[-2], y[-2])),
                )
                # cuantos paneles caben en cada direccion de paneles por cada lado
                ppx = int(lados[0] // (px + garra))
                ppy = int(lados[1] // (pyi + ddy))
                # para centrarlos, se incrementa el origen en el resto/2
                offset = ((lados[0] % (px + garra))/2,
                          (lados[1] % (pyi + ddy))/2)
                # Origen del plano de los paneles
                x0 = list(x)[0]+offset[0]
                # en el eje y hago que la distancia etre filas quede tambien al principio
                y0 = list(y)[0]+offset[1]+ddy
                for iiy in range(ppy):
                    if iiy % 2 == 0:
                        fila = reversed(range(ppx))
                    else:
                        fila = range(ppx)
                    for iix in fila:
                        #
                        pp = translate(
                            panel_modelo,
                            xoff=x0 + px * iix,
                            yoff=y0 + (ddy + pyi) * iiy,
                        )
                        pp = rotate(
                            pp, angulo, origin=(list(x)[0], list(y)[0]))
                        pps.append(
                            {
                                "geometry": pp,
                                "Layer": "PANELES_MATRIZ",
                                "zz": r.zz,
                                "iix": iix,
                                "iiy": iiy,
                                "azimut": angulo,
                            }
                        )
            df = gpd.GeoDataFrame(pps)

            s.s['FV']['outputs']['vv']['PANELES_MATRIZ'] = df.to_json()

        def h_PANELES():
            '''
            ### paneles de la matriz, dentro de la cubierta 
            '''
            PANELES_MATRIZ = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['PANELES_MATRIZ'])
            # gg=gpd.GeoDataFrame({'geometry':Point(1.1,2.2)})
            gg = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['CUBIERTA'])
            gg = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['CUBIERTA'])
            cubierta = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['CUBIERTA'])
            # para cada cubierta donde vayan paneles se vogen los que caen dentro completamente
            paneles_matriz = gpd.GeoDataFrame.from_file(
                s.s['FV']['outputs']['vv']['PANELES_MATRIZ'])
            ppcc = gpd.GeoDataFrame()
            for i, r in cubierta[cubierta['FV'] == 1].iterrows():
                # #print(r)
                mask = paneles_matriz.within(r.geometry)
                paneles = paneles_matriz.loc[mask].copy()
                paneles['iic'] = i
                paneles['inversor'] = 11
                paneles['string'] = 1
                paneles['peakpower'] = 0.5
                paneles['angle'] = 0
                paneles['aspect'] = 0
                paneles['userhorizon'] = ','.join([str(x) for x in [0]*49])
                paneles['E_m'] = ','.join([str(x) for x in [0]*12])

                ppcc = pd.concat([ppcc, paneles], ignore_index=True)

            s.s['FV']['outputs']['vv']['PANELES'] = ppcc.to_json()


class forms:
    def forms():
        '''
        formularioUnico 2 *formularios
        '''

        forms.actualizaFormularios()

    def actualizaFormularios():
        s.s['formularios']['outputs'] = s.s['formularios']['inputs']



def ttt(tt):
    '''
    - PARA MEDIR LOS TEIMPOS DE EJECUCION
    '''
    print(f">>> {inspect.currentframe().f_code.co_name} {time() - tt}")
    tt = time()
    return tt


def app():
    '''

    '''

    if  st.checkbox('marcarlo solo para desarrollo mas rapido  solo los formularios '):
        clc_edificio.clc_edificio()
        calculos.calculos()
    else:
        # mkdocs_jpgs.mkdocs_jpgs()
        None

    forms.forms()
    _estado._estado2json()


if __name__ == "__main__":
    s = _estado.json2_estado()
    app()
