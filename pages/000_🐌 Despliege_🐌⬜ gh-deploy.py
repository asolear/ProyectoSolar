
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
from pdf2image import convert_from_path

st.set_page_config(layout="wide")

warnings.filterwarnings('ignore')
font = {'family': 'monospace', 'size': '6'}
plt.rc('font', **font)


class mkdocs_jpgs:
    '''
    - como alternativa a la clase mkdocs_jpgs en la que me lio mucho para ordenar los archivos anadiendoles un indice
    - aqui simplemente meto un nav en el kmdocs yml
    '''
    def mkdocs_jpgs():
        files = sorted(
            [lista for lista in os.listdir('docs/Expediente/pdfs')])[:]

        mkdocs_jpgs.crea_jpgs(files)
        mkdocs_jpgs.xxxxxx_md(files)
        mkdocs_jpgs.index_md(files)
        mkdocs_jpgs.mkdocs_yml(files)
        mkdocs_jpgs.contacto_md()

    def crea_jpgs(files):
        '''
        crea el mkdocs y lo arranca y lo incrusta en el st si esta disponible
        '''

        for ii in range(len(files)):
            file = files[ii]
            in_pdf_file = f'docs/Expediente/pdfs/{file}'
            print(in_pdf_file)

            try:
                os.mkdir(f'docs_jpg/')
            except:
                None
            try:
                os.mkdir(f'docs_jpg/Expediente')
            except:
                None
            try:
                os.mkdir(f'docs_jpg/Expediente/{file[:-4]}')
            except:
                None
            # Store Pdf with convert_from_path function
            images = convert_from_path(in_pdf_file)

            for i in range(len(images)):

                # Save pages as images in the pdf
                images[i].save(
                    f'docs_jpg/Expediente/{file[:-4]}/page{str(i)}.jpg', 'JPEG')

    def xxxxxx_md(files):
        '''
        crea el mkdocs y lo arranca y lo incrusta en el st si esta disponible
        '''
        import os

        def html_png():
            '''
            - embeber jpg del pdf con los resultados
            - https://github.com/asolear/fv01/blob/master/app_GUI.py
            '''
            html = []

            PNGs = sorted(os.listdir(f'docs_jpg/Expediente/{file[:-4]}'))
            PNGs = [array for array in PNGs if ".jpg" in array]
            for i in PNGs:
                print(i)
                html.append(f''' <img src="{i}"> ''')
            html = ' '.join(html)
            return html



        for ii in range(len(files)):
            file = files[ii]
            f = open(f"docs_jpg/Expediente/{file[:-4]}.md", "w")

            f.write(f'''#
# [🔙 ](../../)    <a href="../pdfs/{file}">📥</a>
{html_png()}

            
                ''')
            f.close()

    def index_md(files):
        '''
        crea el index.md
        '''
        import os


# <img src="figs/Screenshot from 2023-02-13 13-59-43.png"  width="100%" height="30%">

        indice = f'''{mkdocs_jpgs.fnavsmd(files)}'''

        boton_whatsap = '''
<script src="https://kit.fontawesome.com/1cf483120b.js" crossorigin="anonymous"></script>
<style>
.whatsapp-button {
  position: fixed;
  top: 222px;
  right: 15px;
  z-index: 99;
  background-color: #25d366;
  border-radius: 50px;
  color: #ffffff;
  text-decoration: none;
  width: 50px;
  height: 50px;
  font-size: 30px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  -webkit-box-shadow: 0px 0px 25px -6px rgba(0, 0, 0, 1);
  -moz-box-shadow: 0px 0px 25px -6px rgba(0, 0, 0, 1);
  box-shadow: 0px 0px 25px -6px rgba(0, 0, 0, 1);
  animation: effect 5s infinite ease-in;
}
@keyframes effect {
  20%,
  100% {
    width: 50px;
    height: 50px;
    font-size: 30px;
  }
  0%,
  10% {
    width: 55px;
    height: 55px;
    font-size: 35px;
  }
  5% {
    width: 50px;
    height: 50px;
    font-size: 30px;
  }
}
</style>
<a target="_blank" href="https://api.whatsapp.com/send?phone=600366211&text=Informacion sobre Black Roof Style" class="whatsapp-button"><i class="fab fa-whatsapp"></i></a>
'''
        f = open(f"docs_jpg/index.md", "w")
        f.write('''# [🏬 FV para comunidades](Contacto){ .md-button }''')
        f.write(boton_whatsap)
        f.write(indice)
        f.close()

    def mkdocs_yml(files):

        # st.write(fnavs())
        f = open(f"docs_jpg/mkdocs.yml", "w")
# <img src="figs/Screenshot from 2023-02-13 13-59-43.png"  width="100%" height="30%">

        f.write(f'''# 
site_name: 01_▫️📚_Proyecto.solar
docs_dir: 'docs_jpg'
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
{mkdocs_jpgs.fnavsyml(files)}
            ''')
        f.close()

    def fnavsmd(files):
        '''
        - crea el indice en format md
        '''
        navs = []

        grupos = [x.split("_")[1] for x in files]
        grupos = list(dict.fromkeys(grupos))
        # grupos=["0"]

        for grupo in grupos:
            files_grupo = [lista for lista in files if grupo in lista]
            navs.append(f'''
## {grupo}:''')
            for file in files_grupo:
                navs.append(f'''
- [{file.split("_")[2][:-4]}.](Expediente/{file[:-4]}.md)''')
        navs = ' '.join(navs)

        return navs

    def fnavsyml(files):
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

    def contacto_md():

        contenido = '''---
hide:
  - footer
  - toc
  # - navigation
---

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
# 
<div id="map" style="width: 100%; height: 400px;"></div>
<label >Marque la ubicacion </label>

<form action="https://formsubmit.co/admin@asolear.es" method="POST" enctype="multipart/form-data">
  <!-- comandos -->
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_autoresponse" value="Muchas gracias, en breve le contactaremos.">
  <input class="form-control" type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_next" value="https://proyecto.solar">
  <input type="hidden" name="_subject" value="PROYECTO_SOLAR">
  <input type="hidden" name="_autoresponse" value="Gracias, en breve le contactaremos.">
  <input type="hidden" name='lat' class="form-control" id="lat">
  <input type="hidden" name='lng' class="form-control" id="lng">
  <div class="col-sm-7">
    <div class="row">
      <div class="column">
      </div>
      <div class="column"></div>
      <br>
      <label for="email">Email</label>
        <input type="email" class="form-control" name='email' id="email"  aria-describedby="emailHelp" placeholder="Enter email" required>
      <br>
      <br>
      <!-- <label for="exampleFormControlInput1" class="form-label">Adjuntar DXF:</label>
      <input type="file" id="myfile" name="cv" multiple><br><br> -->
      <label><input type="checkbox" class="agree" required> Acepto la Política
        de Privacidad.
      <br>
      <br>
      <button type="submit" class="btn btn-primary" onclick="document.getElementById('modal').click()">Submit</button>
      <div class="row">
        <div class="col-sm-5">
          <p><span class="glyphicon glyphicon-map-marker"></span> </p>
        </div>
      </div>
    </div>
  </div>
</form>

<!-- Button trigger modal -->
<button hidden type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal" id="modal">
  Launch demo modal
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Gracias por contactarnos</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <!-- <button type="button" class="btn btn-primary">Save changes</button> -->
      </div>
    </div>
  </div>
</div>


??? warning "Politica de Privacidad "

    En Proyecto Solar cumplimos con el RGPD (Reglamento General de Protección de Datos):

    - Responsable: Proyecto Solar SL.
    - Finalidad: responder a tu mensaje enviado desde este formulario de contacto.
    - Legitimación: tu consentimiento.
    - Destinatarios: tus datos se guardarán en nuestro proveedor de email que también cumple con el RGPD.
    - Derechos: tienes derecho a acceder, rectificar, limitar y suprimir tus datos en cualquier momento.

<script data-require="leaflet@0.7.3" data-semver="0.7.3"
    src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js">
</script>
<link data-require="leaflet@0.7.3" data-semver="0.7.3" rel="stylesheet"
    href="//cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css" />`
<script>
  var tileLayer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    'attribution': 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
  });
  var map = new L.Map('map', {
    'center': [36.664, -4.458],
    'zoom': 8,
    'layers': [tileLayer]
  });
var marker = L.marker([36.664, -4.458]).addTo(map)
		.bindPopup('INSTALACION FOTOVOLTAICA').openPopup();
map.on('click', function (e) {
    if (marker) {
      map.removeLayer(marker);
    }
    marker = new L.Marker(e.latlng).addTo(map).bindPopup('INSTALACION FOTOVOLTAICA').openPopup();
    document.getElementById('lat').value = e.latlng.lat;
    document.getElementById('lng').value = e.latlng.lng;
  });
</script>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
    crossorigin="anonymous">   
</script>
        
        
        
        '''

        f = open(f"docs/Contacto.md", "w")
        f.write(contenido)
        f.close()


def app():
    ''' 
    - mkdocs gh-deploy
    - para subirlo a  github usando figuras e lugar de iframes de los pdf
    - inclustar imagenes para el despliegue de mkdocs, pero el proceso de crear las imagenes es mas llllleeeeennnnttooo


    '''

    mkdocs_jpgs.mkdocs_jpgs()

    components.iframe("http://127.0.0.1:8000",  height=11002)


if __name__ == "__main__":
    app()
