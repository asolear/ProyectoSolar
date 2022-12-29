# Coordenadas

<form action="https://formsubmit.co/admin@asolear.es" method="POST" enctype="multipart/form-data">
  <!-- comandos -->
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_autoresponse" value="Muchas gracias, en breve le contactaremos.">
  <input class="form-control" type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_next" value="https://asolear.es/index.html">
  <input type="hidden" name="_subject" value="COLABORADOR">
  <input type="hidden" name="_autoresponse" value="Gracias, en breve le contactaremos.">
  <input type="hidden" name='lat' class="form-control" id="lat">
  <input type="hidden" name='lng' class="form-control" id="lng">
  <div class="col-sm-7">
    <div class="row">
      <div class="column">
      </div>
      <div class="column"></div>
      <label for="email">Email</label>
      <input name='email' type="email" class="form-control" id="email" placeholder="Enter email" required>
      <br>
      <label >Marque en el mapa la ubicacion de la instalacion</label>
      <br>
      <!-- <label for="exampleFormControlInput1" class="form-label">Adjuntar DXF:</label>
      <input type="file" id="myfile" name="cv" multiple><br><br> -->
      <label><input type="checkbox" class="agree" required> Acepto la</label> <a
        href="https://asolear.es/politicaprivacidad.html">Política
        de Privacidad.</a>
      <br>
      <input type="submit" value="Enviar">
      <div class="row">
        <div class="col-sm-5">
          <p><span class="glyphicon glyphicon-map-marker"></span> </p>
        </div>
      </div>
    </div>
  </div>
</form>
<div id="map" style="width: 100%; height: 400px;"></div>
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
