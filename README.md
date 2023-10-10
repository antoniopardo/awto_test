# awto_test
Resolucion de problema para cargo Ingeniero de Datos
----------------------------------------------------

Tome la decision de crear 2 tablas para cargar los datos que se obtienen del archivo CSV (trip.csv):
- Tabla awto_user : Tabla con información del usuario/cliente que contrató el servicio de Awto. Contiene 3 columnas:
  - user_id : campo numérico que contiene el identificador interno del usuario
  - name_user: campo de texto que contiene el nombre del usuario
  - rut_user: campo de texto (para que pueda almacenar los rut con dígito verificador 'K') que contiene el Rut del usuario
  2.- Tabla awto_trip : Tabla con información de cada viaje. Contiene 17 columnas:
      a.- trip_id: campo numérico que contiene el identificador interno de cada viaje
      b.- vehicle_id: campo numérico que contiene el identificador interno del vehículo utilizado en el viaje
      c.- booking_time: campo de fecha que contiene la información de la fecha y hora cuando se realizó la reserva del vehículo
      d.- start_time: campo de fecha que contiene la información de la fecha y hora cuando se inició el viaje
      e.- end_time: campo de fecha que contiene la información de la fecha y hora cuando se terminó el viaje
      f.- status_id: campo numérico que contiene el identificador interno equivalente al estado del viaje
      g.- travel_dist: campo numérico que contiene la distancia que recorrió el vehículo durante el viaje. *Nota* se debe normalizar la unidad usada (Kilómetros o metros) para evitar problemas de consistencia en la generación del resumen diario
      h.- membership_id: campo numérico que contiene el identificador de membresía que posee el usuario al momento de realizar el viaje. *Nota* No lo incluí en la tabla de usuario, debido a que un usuario puede cambiar de tipo de membresía entre un viaje y otro
      i.- price_amount: campo numérico (decimal) que contiene el valor del viaje sin impuestos
      j.- price_tax: campo numérico (decimal) que contiene el valor de los impuestos asociados al viaje
      k.- price_total: campo numérico (decimal) que contiene el valor total del viaje (incluyendo impuestos)
      l.- start_lat: campo de punto flotante que contiene el valor de la latitud de la coordenada donde se inició el viaje
      m.- start_lon: campo de punto flotante que contiene el valor de la longitud de la coordenada donde se inició el viaje
      n.- end_lat: campo de punto flotante que contiene el valor de la latitud de la coordenada donde se finalizó el viaje
      o.- end_lon: campo de punto flotante que contiene el valor de la longitud de la coordenada donde se finalizó el viaje
      p.- start_coords: campo geométrico de tipo *point* que almacena la coordenada completa del punto donde se inició el viaje. Puede utilizarse para cruzar la información con capas de información como los perímetros de cada comuna o áreas donde el vehículo no debería transitar (sólo por mostrar un par de ejemplos de su posible aplicación a futuro)
      q.- end_coords: campo geométrico de tipo *point* que almacena la coordenada completa del punto donde se finalizó el viaje

Para la carga de los resumenes diarios, creé la tabla awto_resumen_diario que contiene 8 campos:
    a.- resumen_id: campo numérico que contiene un identificador único por día (se crea al formatear la fecha como 'YYYYMMDD'). Puede servir para ordenar más rápidamente que por la fecha
    b.- fecha_resumen: campo de fecha que contiene el día al que corresponde la fila
    c.- total_viajes: campo numérico que contiene el total de viajes que se encuentran en la tabla awto_trip. Se debería filtrar la información de los registros que se consideran como "válidos" según el status_id. Dado que no se entrega la información sobre el significado de cada valor, trabajé con el supuesto de que los estados válidos eran 1, 2, 3 y 4 (esto también aparece explicado en el código del script *cargaResumen.py*)
    d.- suma_ingresos_neto: campo numérico (decimal) que contiene la suma de los valores sin impuesto de los viajes correspondientes a la fecha procesada
    e.- suma_ingresos_bruto: campo numérico (decimal) que contiene la suma de los valores totales (incluyendo impuestos) de los viajes correspondientes a la fecha procesada
    f.- promedio_ingresos_neto: campo numérico (decimal) que contiene el promedio de los valores sin impuesto de los viajes correspondientes a la fecha procesada
    g.- promedio_ingresos_bruto: campo numérico (decimal) que contiene el promedio de los valores totales (incluyendo impuestos) de los viajes correspondientes a la fecha procesada
    h.- total_metros_recorridos: campo numérico (decimal) que contiene la suma de los valores del campo *travel_dist* de la tabla awto_trip. Como se menciona más arriba, es necesario estar seguros de la unidad que se utiliza (metros o kilómetros) para evitar valores inconsistentes

  Para asegurar la consistencia de los datos, se puede incorporar una lista de procesos que vayan validando los datos a medida que se leen desde el origen de datos (para efectos de este ejercicio, son los que se obtienen desde el archivo CSV):
  1.- Validar que cada valor corresponde al tipo de dato que se definió al crear la tabla. A modo de ejemplo, los campos numéricos no deberían incluir caracteres
  2.- Validar que cada valor se encuentra dentro de un rango "permitido". Se debería definir el intervalo de valores que se pueden almacenar en cada campo (por ejemplo, que el precio de un viaje no sea negativo) y chequear que el valor que se está recibiendo se encuentra dentro de los valores permitidos
  3.- Validar que los campos de identificadores (como el identificador de usuario, vehículo, etc) tengan valores y no vengan en blanco
  Si se detectan inconsistencias al realizar estas validaciones, se debe separar el registro completo y marcarlo para una revisión posterior, sin insertarlo en la tabla awto_trip hasta que se resuelvan las inconsistencias.
  Se puede utilizar alguna herramienta como Informatica Data Quality o IBM Databand (por mencionar sólo 2) para descubrir y luego corregir inconsistencias y errores en los datos, y así, una vez que se resuelven los errores existentes, crear un proceso de validación de integridad de los datos que revise los datos de manera periódica mediante un proceso batch que ejecute un script de análisis y envíe un reporte final con el estado de los registros (en el caso que las inconsistencias no se puedan resolver de manera automática).
