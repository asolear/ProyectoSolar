

import streamlit as st
import streamlit.components.v1 as components

# bootstrap 4 collapse example
components.html(
    """

    
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
<label >Marque su ubicacion </label>

    <div id="map" style="width: 100%; height: 400px;"></div>

<form action="https://formsubmit.co/admin@asolear.es" method="POST" enctype="multipart/form-data">
  <!-- comandos -->
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_autoresponse" value="Muchas gracias, en breve le contactaremos.">
  <input class="form-control" type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_next" value="">
  <input type="hidden" name="_subject" value="TEJADO_SOLAR">
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





    """,
    height=600,
)
# import streamlit as st
# import numpy as np
# import pandas as pd
# from pathlib import Path

# def app():

#     # Use local CSS
#     def local_css(file_name):
#         with open(file_name) as f:
#             st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


#     local_css("style/style.css")

#     # ---- CONTACT ----
#     with st.container():
#         st.write("---")
#         st.header("Hola, soy  Lucía  :wave:, contacta conmigo")
#         st.write("##")

#         # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
#         contact_form = """
#         <form action="https://formsubmit.co/admin@asolear.es" method="POST">
#             <input type="hidden" name="_captcha" value="false">
#             <input type="text" name="name" placeholder="Tu nombre" required>
#             <input type="text" name="Telefono" placeholder="Tu Telefono" required>
#             <input type="email" name="email" placeholder="Tu email" required>
#             <textarea name="message" placeholder="Tu mensaje " required></textarea>
#             <button type="submit">Enviar</button>
#         </form>
#         """
#         left_column, right_column = st.columns(2)
#         with left_column:
#             st.markdown(contact_form, unsafe_allow_html=True)
#         with right_column:
#             st.empty()

# if __name__ == "__main__":
#     app()
