# Priority guides

## Vista princial

  * Display text: Alerta si el servicio no está disponible

  * Search bar: Barra de búsqueda con el formato de búsqueda
    * Action: Realiza la consulta al servidor

  * Display text: Texto para ofrecer otra alternativa
  
  * Scroll window: Contiene la lista de intervalos y opciones para ordenarla
    * Sort buttons: Indican intervalo mayor o menor
      * Action: Ordena la lista

    * Radio button: Marca si el intervalo seleccionado es ascendente o descendente

    * Button: Uno por cada intervalo, con el nombre y abreviatura del mismo
      * Action: Realiza la consulta al servidor del intervalo seleccionado


## Vista resultado de la búsqueda

  * Return button: Vuelve a la vista inicial

  * Search bar: Barra de búsqueda con el input del usuario
    * Action: Realiza la consulta al servidor

  * Display text: Confirma la búsqueda realizada

  * Result tabs: Contiene la información devuelta por el servidor
    * Display text: Notas de ejemplo
      * Display text: Distancia del intervalo en tonos + semitonos
      * Display text: 2 notas de ejemplo que cumplan el intervalo

    * Display text: Canción representativa
      * Display text: "Título" + Título de la canción favorita
      * Display text: URL
      * Link text: Hiperenlace al sitio donde se aloja el vídeo
      
      * More button: Mostrar más canciones
        * Action: Despliega el resto de canciones, con el mismo formato que la primera
      * Separator: Separa cada canción
  

# Decisiones

  * El usuario puede buscar por abreviatura, o en caso de no conocerla, elegir de la lista de la pantalla inicial el intervalo deseado.
  * Para una búsqueda rápida en la lista de intervalos, podrá ordenarse ascendente o descendentemente por longitud del mismo.
  * La canción representativa de un intervalo es la canción favorita de la lista, o el primer resultado si no existe favorita.
  * Si el servidor no está disponible o tarda demasiado en responder, se indicará que no está disponible en la vista inicial tras intentar la consulta.
  * No añadimos ninguna pantalla de carga porque la respuesta del servidor es muy rápida como para que tenga sentido que exista.
