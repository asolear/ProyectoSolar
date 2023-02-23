#
???+ Info "PS reduce los Plazos"
    ``` mermaid
    gantt
        title       ☀️ Instalacion FV con  PS
        excludes    weekends
        %% (`excludes` accepts specific dates in YYYY-MM-DD format, days of the week ("sunday") or "weekends", but not the word "weekdays".)
        title       ☀️ Instalacion FV  sin / con  PS
        section ❌ Sin PS
        Oferta                  :crit,    Oferta, 2023-02-10, 1w
        Contratacion          : milestone,1d
        T. Permisos :crit,2w
        Instalacion: 4w
        section ✔️ Con PS
        Oferta  :crit,milestone,    des1, 2023-02-10, 0d
        Contratacion         :milestone,1d
        T. Permisos :crit,milestone,0d
        Instalacion: 4w
    
    ```
            
??? Success "Flujo de DOCUMENTOS"
    ``` mermaid
    sequenceDiagram
    autonumber
      
            Instalador->>🧑 Cliente:🧑⬜ Oferta.  
            Instalador->>🧑 Cliente:🧑⬜ formularioUnico.  
            Instalador->>🧑 Cliente:🧑⬜ Contrato.  
            Instalador->>🏦 Ayuntamiento:🏦⬜ Representación ante la GMU.  
            Instalador->>🏦 Ayuntamiento:🏦⬜ DECLARACIÓN RESPONSABLE PARA EJECUCIÓN DE OBRAS.  
            Instalador->>🏦 Ayuntamiento:🏦⬜ Declaración Responsable de Obras.  
            Instalador->>🏦 Ayuntamiento:🏦⬜ Certificado técnico de colegiación y habilitación.  
            Instalador->>🏦 Ayuntamiento:🏦⬜ Formulario normalizado Licencias de Obras.  
            Instalador->>🏦 Ayuntamiento:🏦⬜ Panel o cartel informativo.  
            Instalador->>📐 Proyecto:📐⬜ Memoria Técnica de Diseño.  
            Instalador->>📐 Proyecto:📐⬜ Memoria.  
            Instalador->>📐 Proyecto:📐⬜ Planos.  
            Instalador->>📐 Proyecto:📐⬜ Mediciones y presupuesto.  
            Instalador->>📐 Proyecto:📐⬜ Certificado de instalación eléctrica.  
            Instalador->>🇪🇺 NextGenerationEU:🇪🇺⬜  DECLARACIÓN RESPONSABLE relativa a la estimación del consumoxx.  
            Instalador->>🇪🇺 NextGenerationEU:🇪🇺⬜  INFORME JUSTIFICATIVO de la previsión del consumo anual.  
            Instalador->>🇪🇺 NextGenerationEU:🇪🇺⬜  OTORGAMIENTO DE LA REPRESENTACIÓN A LA EMPRESA ADHERIDA .  
            Instalador->>🇪🇺 NextGenerationEU:🇪🇺⬜ DATOS TÉCNICOS Y ECONÓMICOS REQUERIDOS PARA CADA PROGRAMA DE INCENTIVOS.  
            Instalador->>🇪🇺 NextGenerationEU:🇪🇺⬜autoconsumo declaracion sistema almacenamiento.  
            Instalador->>🇪🇺 NextGenerationEU:🇪🇺⬜autoconsumo solicitud declaracion responsable 80.  
            Instalador->>🧪 Blog:🧪⬜ Admissions Application.  
            Instalador->>🧪 Blog:🧪⬜ DECLARACION PROVEEDOR ALMACENAMIENTO Autoconsumo y termicas.  
            Instalador->>🧪 Blog:🧪⬜ Estudio Básico de Seguridad y Salud, telegramv1.  
            Instalador->>🧪 Blog:🧪⬜NO  AFECCION  A OBJETIVOS MEDIOAMBIENTALES.
    ```
                
??? Info "DOCUMENTOS"
                
    ???+ Abstract "🧑 Cliente"  
        - 1 [🧑⬜ Oferta.](Expediente/110_🧑 Cliente_🧑⬜ Oferta.md)  
        - 2 [🧑⬜ formularioUnico.](Expediente/110_🧑 Cliente_🧑⬜ formularioUnico.md)  
        - 3 [🧑⬜ Contrato.](Expediente/120_🧑 Cliente_🧑⬜ Contrato.md)
    ???+ Abstract "🏦 Ayuntamiento"  
        - 4 [🏦⬜ Representación ante la GMU.](Expediente/220_🏦 Ayuntamiento_🏦⬜ Representación ante la GMU.md)  
        - 5 [🏦⬜ DECLARACIÓN RESPONSABLE PARA EJECUCIÓN DE OBRAS.](Expediente/221_🏦 Ayuntamiento_🏦⬜ DECLARACIÓN RESPONSABLE PARA EJECUCIÓN DE OBRAS.md)  
        - 6 [🏦⬜ Declaración Responsable de Obras.](Expediente/221_🏦 Ayuntamiento_🏦⬜ Declaración Responsable de Obras.md)  
        - 7 [🏦⬜ Certificado técnico de colegiación y habilitación.](Expediente/222_🏦 Ayuntamiento_🏦⬜ Certificado técnico de colegiación y habilitación.md)  
        - 8 [🏦⬜ Formulario normalizado Licencias de Obras.](Expediente/225_🏦 Ayuntamiento_🏦⬜ Formulario normalizado Licencias de Obras.md)  
        - 9 [🏦⬜ Panel o cartel informativo.](Expediente/227_🏦 Ayuntamiento_🏦⬜ Panel o cartel informativo.md)
    ???+ Abstract "📐 Proyecto"  
        - 10 [📐⬜ Memoria Técnica de Diseño.](Expediente/230_📐 Proyecto_📐⬜ Memoria Técnica de Diseño.md)  
        - 11 [📐⬜ Memoria.](Expediente/240_📐 Proyecto_📐⬜ Memoria.md)  
        - 12 [📐⬜ Planos.](Expediente/260_📐 Proyecto_📐⬜ Planos.md)  
        - 13 [📐⬜ Mediciones y presupuesto.](Expediente/270_📐 Proyecto_📐⬜ Mediciones y presupuesto.md)  
        - 14 [📐⬜ Certificado de instalación eléctrica.](Expediente/290_📐 Proyecto_📐⬜ Certificado de instalación eléctrica.md)
    ???+ Abstract "🇪🇺 NextGenerationEU"  
        - 15 [🇪🇺⬜  DECLARACIÓN RESPONSABLE relativa a la estimación del consumoxx.](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜  DECLARACIÓN RESPONSABLE relativa a la estimación del consumoxx.md)  
        - 16 [🇪🇺⬜  INFORME JUSTIFICATIVO de la previsión del consumo anual.](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜  INFORME JUSTIFICATIVO de la previsión del consumo anual.md)  
        - 17 [🇪🇺⬜  OTORGAMIENTO DE LA REPRESENTACIÓN A LA EMPRESA ADHERIDA .](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜  OTORGAMIENTO DE LA REPRESENTACIÓN A LA EMPRESA ADHERIDA .md)  
        - 18 [🇪🇺⬜ DATOS TÉCNICOS Y ECONÓMICOS REQUERIDOS PARA CADA PROGRAMA DE INCENTIVOS.](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜ DATOS TÉCNICOS Y ECONÓMICOS REQUERIDOS PARA CADA PROGRAMA DE INCENTIVOS.md)  
        - 19 [🇪🇺⬜autoconsumo declaracion sistema almacenamiento.](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜autoconsumo declaracion sistema almacenamiento.md)  
        - 20 [🇪🇺⬜autoconsumo solicitud declaracion responsable 80.](Expediente/320_🇪🇺 NextGenerationEU_🇪🇺⬜autoconsumo solicitud declaracion responsable 80.md)
    ???+ Abstract "🧪 Blog"  
        - 21 [🧪⬜ Admissions Application.](Expediente/999_🧪 Blog_🧪⬜ Admissions Application.md)  
        - 22 [🧪⬜ DECLARACION PROVEEDOR ALMACENAMIENTO Autoconsumo y termicas.](Expediente/999_🧪 Blog_🧪⬜ DECLARACION PROVEEDOR ALMACENAMIENTO Autoconsumo y termicas.md)  
        - 23 [🧪⬜ Estudio Básico de Seguridad y Salud, telegramv1.](Expediente/999_🧪 Blog_🧪⬜ Estudio Básico de Seguridad y Salud, telegramv1.md)  
        - 24 [🧪⬜NO  AFECCION  A OBJETIVOS MEDIOAMBIENTALES.](Expediente/999_🧪 Blog_🧪⬜NO  AFECCION  A OBJETIVOS MEDIOAMBIENTALES.md)
<script src="https://kit.fontawesome.com/1cf483120b.js" crossorigin="anonymous"></script>
<style>
.whatsapp-button {
  position: fixed;
  top:333px;
  right: 66px;
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
