# [🏬 Empiece mañana su instalacion FV](Contacto){ .md-button }
<script src="https://kit.fontawesome.com/1cf483120b.js" crossorigin="anonymous"></script>
<style>
.whatsapp-button {
  position: fixed;
  top: 55px;
  right: 111px;
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

???+ Info "PS prepara y gestiona toda la documentacion para que empiece a instalar mañana. "
    ``` mermaid
    gantt
        title       ☀️ Instalacion FV con  PS
        excludes    weekends
        %% (`excludes` accepts specific dates in YYYY-MM-DD format, days of the week ("sunday") or "weekends", but not the word "weekdays".)
        title       ☀️ Instalacion FV  sin / con  PS
        section ❌ Sin PS
        Oferta                  :crit,    Oferta, 2023-02-08, 1w
        Contratacion          : milestone,1d
        T. Permisos :crit,2w
        Instalacion: 4w

        section ✔️ Con PS
        Oferta  :crit,milestone,    des1, 2023-02-08, 0d
        Contratacion         :milestone,1d
        T. Permisos :crit,milestone,0d
        Instalacion: 4w
    
    ```
    
???+ Success "DOCUMENTACION de ejemplo"
    ``` mermaid
    sequenceDiagram

    autonumber
    Instalador->>Cliente: Oferta
    Cliente->>Instalador:  Contrato
    Instalador-->>Ayuntamiento: Declaracion Responsable De Obras
    Instalador->>Industria: Solicitud Incentivos
    Instalador-->>Industria: Legalizacion
    Instalador-->>Cliente:  Certificado de la instalacion 

    ```
        
    ??? Abstract "👷 Tecnico"  
        - [⬜ formularioUnico.](Expediente/109_👷 Tecnico_⬜ formularioUnico.md)
    ??? Abstract "🧑 Cliente"  
        - [🧑⬜ Oferta.](Expediente/110_🧑 Cliente_🧑⬜ Oferta.md)  
        - [🧑⬜ formularioUnico.](Expediente/110_🧑 Cliente_🧑⬜ formularioUnico.md)  
        - [🧑⬜ Contrato.](Expediente/120_🧑 Cliente_🧑⬜ Contrato.md)  
        - [🧑⬜ SolicitudRegistrada.](Expediente/120_🧑 Cliente_🧑⬜ SolicitudRegistrada.md)
    ??? Abstract "🏦 Ayuntamiento"  
        - [🏦⬜ Representación ante la GMU.](Expediente/220_🏦 Ayuntamiento_🏦⬜ Representación ante la GMU.md)  
        - [🏦⬜ DECLARACIÓN RESPONSABLE PARA EJECUCIÓN DE OBRAS.](Expediente/221_🏦 Ayuntamiento_🏦⬜ DECLARACIÓN RESPONSABLE PARA EJECUCIÓN DE OBRAS.md)  
        - [🏦⬜ Declaración Responsable de Obras.](Expediente/221_🏦 Ayuntamiento_🏦⬜ Declaración Responsable de Obras.md)  
        - [🏦⬜ Certificado técnico de colegiación y habilitación.](Expediente/222_🏦 Ayuntamiento_🏦⬜ Certificado técnico de colegiación y habilitación.md)  
        - [🏦⬜ Formulario normalizado Licencias de Obras.](Expediente/225_🏦 Ayuntamiento_🏦⬜ Formulario normalizado Licencias de Obras.md)  
        - [🏦⬜ Panel o cartel informativo.](Expediente/227_🏦 Ayuntamiento_🏦⬜ Panel o cartel informativo.md)
    ??? Abstract "📐 Proyecto"  
        - [📐⬜ Memoria Técnica de Diseño.](Expediente/230_📐 Proyecto_📐⬜ Memoria Técnica de Diseño.md)  
        - [📐⬜ Memoria.](Expediente/240_📐 Proyecto_📐⬜ Memoria.md)  
        - [📐⬜ Planos.](Expediente/260_📐 Proyecto_📐⬜ Planos.md)  
        - [📐⬜ Mediciones y presupuesto.](Expediente/270_📐 Proyecto_📐⬜ Mediciones y presupuesto.md)  
        - [📐⬜ Certificado de instalación eléctrica.](Expediente/290_📐 Proyecto_📐⬜ Certificado de instalación eléctrica.md)
    ??? Abstract "🇪🇺 NextGenerationEU"  
        - [🇪🇺⬜  DECLARACIÓN RESPONSABLE relativa a la estimación del consumoxx.](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜  DECLARACIÓN RESPONSABLE relativa a la estimación del consumoxx.md)  
        - [🇪🇺⬜  INFORME JUSTIFICATIVO de la previsión del consumo anual.](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜  INFORME JUSTIFICATIVO de la previsión del consumo anual.md)  
        - [🇪🇺⬜  OTORGAMIENTO DE LA REPRESENTACIÓN A LA EMPRESA ADHERIDA .](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜  OTORGAMIENTO DE LA REPRESENTACIÓN A LA EMPRESA ADHERIDA .md)  
        - [🇪🇺⬜ DATOS TÉCNICOS Y ECONÓMICOS REQUERIDOS PARA CADA PROGRAMA DE INCENTIVOS.](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜ DATOS TÉCNICOS Y ECONÓMICOS REQUERIDOS PARA CADA PROGRAMA DE INCENTIVOS.md)  
        - [🇪🇺⬜autoconsumo declaracion sistema almacenamiento.](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜autoconsumo declaracion sistema almacenamiento.md)  
        - [🇪🇺⬜autoconsumo solicitud declaracion responsable 80.](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜autoconsumo solicitud declaracion responsable 80.md)
    ??? Abstract "🧪 Blog"  
        - [🧪⬜ Admissions Application.](Expediente/999_🧪 Blog_🧪⬜ Admissions Application.md)  
        - [🧪⬜ DECLARACION PROVEEDOR ALMACENAMIENTO Autoconsumo y termicas.](Expediente/999_🧪 Blog_🧪⬜ DECLARACION PROVEEDOR ALMACENAMIENTO Autoconsumo y termicas.md)  
        - [🧪⬜ Estudio Básico de Seguridad y Salud, telegramv1.](Expediente/999_🧪 Blog_🧪⬜ Estudio Básico de Seguridad y Salud, telegramv1.md)  
        - [🧪⬜NO  AFECCION  A OBJETIVOS MEDIOAMBIENTALES.](Expediente/999_🧪 Blog_🧪⬜NO  AFECCION  A OBJETIVOS MEDIOAMBIENTALES.md)