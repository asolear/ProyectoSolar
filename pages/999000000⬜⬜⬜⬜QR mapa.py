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
#
import matplotlib
import contextily as cx
import qrcode
font = {'family': 'monospace', 'size': '6'}
plt.rc('font', **font)
'''
- a destacar las librerias
    - SimpleNamespace  que usare a modo de memoria diccionario en la variable 
        - s.s['key']= value
    -
'''


def e_CabPag(fig, N):
    '''
    - cabecera de pagina
        - el numero de pagina se cofe del ultimo caracter del nombre de la funcion
    '''
    ax = fig.add_axes([.16, .99, 0, 0], frameon=False)
    txt = f''' {os.path.abspath(__file__)[:-3]}.pdf    {datetime.datetime.now().strftime(" %d / %m / %Y - %H:%M")}   Pag.: {N}  '''
    ax.text(0, 1, txt, va="top",   wrap=True, fontsize=6)
    ax.axis("off")


class mm:
    '''
    fsafasdf
    '''
    def json2estado():
        '''
        Leo la Pseudo Base de Datos en memoria como dato 'json' s.s['xxxxx']
        '''
        with open("_estado.json", "r") as f:
            s = json.load(f)
        s = SimpleNamespace(s=s)
        return s

    def estado2json():
        '''
        Escribo la Pseudo Base de Datos en disco como datos 'json' s.s['xxxxx']
        '''

        with open("assets/json/mm.json", "w") as f:
            f.write(json.dumps(s.s))
        return


class calculos():
    '''
    - CALCULOS      x = s.s['x'] ;    y = f(x) ;    s.s['_y'] = y
    - se debe ejecutar antes de la visulaizacion de pagnas
        - hacer siempre el orden
            - x = s.s['x']  
            - y = f(x) 
            - s.s['_y'] = y
        - basicamente se toman los valores del dxf se actualiza el estado s cargado antes de llamar a app,
        ojo !!!! que no funciona si se llama despues
        - con los valores importados en la memoria s hace  operaciones los modifica Y LOS VUELVE A GUARDAR 
    '''

    def ini():
        '''
        slo para inicializar algunas variables string vector y panadas
        '''
        # para mantener los valores anteriores en el json
        try:
            s.s['02_Ampliado']['meta']
        except:
            s.s['02_Ampliado'] = {'meta': {}, 'inputs': {}, 'outputs': {}}
            s.s['02_Ampliado']['meta']['_fecha'] = datetime.datetime.now().strftime(
            " %d / %m / %Y - %H:%M")
        

        s.s['02_Ampliado']['inputs']['x1'] = "Nuestras vivividas son los rios que van a dar a la mar"
        s.s['02_Ampliado']['inputs']['x2'] = [22, 33, 44]
        s.s['02_Ampliado']['inputs']['df'] = pd.DataFrame(
            np.random.rand(2, 3)).to_json()

        s.s['02_Ampliado']['inputs']['gf'] = gpd.GeoDataFrame({'geometry': gpd.GeoSeries(
            [
                Polygon([(0, 0), (3, 4), (1, 4)]),
                Polygon([(2, 0), (5, 2), (1, 3)]),
            ])}).to_json()

    def mod():
        '''
        calculos de preuba, con textos, pandas
        '''
        def ff():
            #  por ejm modificar un texto
            s.s['02_Ampliado']['outputs']['y'] = s.s['02_Ampliado']['inputs']['x1'] + \
                ' Modificacion al texto hecha en el programa'
        ff()

        def ff():
            # por ejemplo cncatenar la df del json con un nueva
            df = pd.concat([pd.read_json(s.s['02_Ampliado']['inputs']['df'], orient='index'),
                            pd.DataFrame(np.random.rand(2, 4))], ignore_index=True)

            s.s['02_Ampliado']['outputs']['df'] = df.to_json()
        ff()

        def ff():
            gf0 = gpd.GeoDataFrame.from_file(
                s.s['02_Ampliado']['inputs']['gf'])

            gf1 = gpd.GeoDataFrame({'geometry': gpd.GeoSeries(
                [
                    Polygon([(5, 0), (6, 5),  (1, 0)]),
                ])})
            gf = pd.concat([gf0, gf1])
            # por ejemplo cncatenar la df del json con un nueva

            s.s['02_Ampliado']['outputs']['gf'] = gf.to_json()
        ff()

        return


class ff:
    '''
    funciones para crear elementos basicos basicas
    https://github.com/asolear/pdfpy_fv/blob/master/docs/FV/_plantilla_funciones.pdf
    '''
    def qr(fig, url='https://asolear.es/p/9989703UF6598N.pdf', x=.4, y=.8):
        '''
        - codigo QR que con el enlace a un oferta
            - parametros
                - url.- direccion de la oferta
                - x,y posicion en el folio 
        '''
        ax = fig.add_axes([x, y, .1, .1], frameon=False)
        qr = qrcode.QRCode()
        qr.add_data(url)
        ax.imshow(qr.make_image().convert("RGB"),
                  extent=[0, 22, 0, 22], cmap='Greys')
        ax.set_title('ff.qr')
        ax.axis("off")

    def poligonizar(fig, x=.2, y=.6, gf=gpd.GeoDataFrame({'geometry': gpd.GeoSeries(
            [Polygon([(0, 0), (2, 1), (0, 1)]), Polygon([(3, 0), (2, 1), (1, 1)])])})):
        '''
        - poligonizar cruce de lineas
            - funciona si se pasa por dxf
            - parametros
                - x,y posicion en el folio 
        '''

        ax = fig.add_axes([x, y, .1, .1], frameon=False)

        gf.boundary.to_file(f'fooo.dxf', driver='DXF')
        #
        gf = gpd.read_file('fooo.dxf')

        gpd.GeoDataFrame(
            {'geometry': list(polygonize(unary_union(gf.geometry)))}).boundary.plot(ax=ax, cmap='tab20')
        ax.set_title('ff.poligonizar')
        ax.axis("off")

    def graphviz(fig):
        '''
        diagrama de bloques con grapviz
        '''
        ax = fig.add_axes([.16, .8, .2, .2], frameon=False)
        import graphviz
        dot = graphviz.Digraph(
            graph_attr={
                "bgcolor": "transparent",
                "splines": "ortho",
            },
        )
        for i in range(3):
            dot.node(
                'FV'+str(i),
                color="blue",
                shape="box",
            )
            dot.edge(
                'FV'+str(i),
                'inveAAArsor',)
        dot.format = "png"
        ax.imshow(matplotlib.image.imread(dot.render()))
        ax.set_title('ff.graphviz')
        ax.axis("off")

    def imagen(fig, img='assets/figs/asolear.png'):
        '''
        imporytar una imagen cualquiera
        '''
        ax = fig.add_axes([.3, .71, .1, .1], frameon=False)
        ax.imshow(matplotlib.image.imread(img),
                  extent=[0, 22, 0, 22])
        ax.set_title('ff.imagen')
        ax.axis("off")

    def mapabn(fig):
        '''
        dibuja el mapa en blanco y negro, en teoria deberia de de hacerlo mas chico y superponerle las placas
        '''
        ax = fig.add_axes([.16, .2, .1, .1], frameon=False)
        south, west, north,  east = (
            36.663994, -4.459781,
            36.763757, -4.351741
        )
        ghent_img, ghent_ext = cx.bounds2img(west,
                                             south,
                                             east,
                                             north,
                                             ll=True,
                                             source=cx.providers.Stamen.Toner
                                             )
        ax.imshow(ghent_img, extent=ghent_ext)
        ax.set_title('ff.mapabn')
        ax.axis("off")

    def mapa(fig):
        '''
        https://contextily.readthedocs.io/en/latest/intro_guide.html
        dibuja en matplotlib un mapa facilmente
        '''
        ax = fig.add_axes([.16, .4, .2, .2], frameon=False)
        mapa = gpd.read_file(
            "https://ndownloader.figshare.com/files/20232174")
        mapa.plot(color="red", ax=ax)
        cx.add_basemap(ax, crs=mapa.crs.to_string())
        ax.set_title('ff.mapa')
        ax.axis("off")


class doc:
    '''
    Documento
    '''
    def pag_codigo(pdf):
        '''
        - como todo el texto no cabe en un A4
            - se puede hacer una 'A4 alargado' cambiando CUANTOS_A4_PEGADOS
                -     fig, axx = plt.subplots(figsize=(21/2.54, 29.7/2.54*CUANTOS_A4_PEGADOS))
            - se puede hacer mu chiquitita la letra
            - se 'podria ' ir dividiendo el texto e N lineas por pagina !!?
        -suele haber una separacion con la parte alta del folio que si se intenta bajar demasiado, se puede distorsinar tordo el texto
        '''
        fig, axx = plt.subplots(figsize=(21/2.54, 29.7/2.54*10))
        e_CabPag(fig, inspect.stack()[0][3].split("_")[-1])

        def ff():
            ax = fig.add_axes([.16, .9, 0, 0], frameon=False)
            with open(os.path.abspath(__file__), 'r') as file:
                txt = file.read()
            ax.text(0, 1, txt, va="top",   wrap=True,
                    fontfamily="monospace", fontsize=6)
            ax.axis("off")
        ff()
        axx.axis('off')
        pdf.savefig()

    def pag_1(pdf):
        '''
        - PAGINA DE MUESTRA
            - pagina_???????  CAMBIAR EN EL NOMBRE DE LA FUNCION  EL NUMERO DE PAGINA
                - pagina de muestra, el ultimo numero marcara el numero de pagina
        '''
        fig, axx = plt.subplots(figsize=(21/2.54*1, 29.7/2.54))
        e_CabPag(fig, inspect.stack()[0][3].split("_")[-1])

        ff.qr(fig, x=.8, url='j')
        ff.poligonizar(fig, gf=gpd.GeoDataFrame.from_file(
            s.s['02_Ampliado']['outputs']['gf']))
        ff.graphviz(fig)
        ff.imagen(fig, img='assets/figs/asolear.png')
        ff.mapabn(fig)
        ff.mapa(fig)

        axx.axis('off')
        pdf.savefig()
        return


def app():
    ''' 
    - Matplotlib a pdf

        Plantilla para crear documentos pdf desde matplotlib
        con cualquier numero de paginas y formato (incluso mezclado), las funciones se organiza como:

        - modelo
            - parametros del (dxf / json )
            - resultados al json
        - c__paginas
            - with PdfPages
                - pagN
                    - f_p_ (todas se llaman igula solo para ordenar)
                    - el numero de pagina se cofe del ultimo caracter del nombre de la funcion
    '''

    calculos.ini()
    calculos.mod()

    with PdfPages(os.path.abspath(__file__)[:-3]+".pdf") as pdf:

        doc.pag_1(pdf)
        doc.pag_codigo(pdf)
        plt.show()
        plt.close()

    mm.estado2json()


if __name__ == "__main__":

    s = mm.json2estado()
    app()
