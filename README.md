# awto_test
Resolucion de problema para cargo Ingeniero de Datos
----------------------------------------------------

Tome la decision de crear 2 tablas para cargar los datos que se obtienen del archivo CSV (trip.csv):
  - Tabla awto_user : Tabla con información del usuario/cliente que contrató el servicio de Awto. Contiene 3 columnas:
    - user_id : campo numérico que contiene el identificador interno del usuario
    - name_user: campo de texto que contiene el nombre del usuario
    - rut_user: campo de texto (para que pueda almacenar los rut con dígito verificador 'K') que contiene el Rut del usuario
  - Tabla awto_trip : Tabla con información de cada viaje. Contiene 17 columnas:
    - trip_id: campo numérico que contiene el identificador interno de cada viaje
    - vehicle_id: campo numérico que contiene el identificador interno del vehículo utilizado en el viaje
    - booking_time: campo de fecha que contiene la información de la fecha y hora cuando se realizó la reserva del vehículo
    - start_time: campo de fecha que contiene la información de la fecha y hora cuando se inició el viaje
    - end_time: campo de fecha que contiene la información de la fecha y hora cuando se terminó el viaje
    - status_id: campo numérico que contiene el identificador interno equivalente al estado del viaje
    - travel_dist: campo numérico que contiene la distancia que recorrió el vehículo durante el viaje. *Nota*: se debe normalizar la unidad usada (Kilómetros o metros) para evitar problemas de consistencia en la generación del resumen diario
    - membership_id: campo numérico que contiene el identificador de membresía que posee el usuario al momento de realizar el viaje. *Nota*: No lo incluí en la tabla de usuario, debido a que un usuario puede cambiar de tipo de membresía entre un viaje y otro
    - price_amount: campo numérico (decimal) que contiene el valor del viaje sin impuestos
    - price_tax: campo numérico (decimal) que contiene el valor de los impuestos asociados al viaje
    - price_total: campo numérico (decimal) que contiene el valor total del viaje (incluyendo impuestos)
    - start_lat: campo de punto flotante que contiene el valor de la latitud de la coordenada donde se inició el viaje
    - start_lon: campo de punto flotante que contiene el valor de la longitud de la coordenada donde se inició el viaje
    - end_lat: campo de punto flotante que contiene el valor de la latitud de la coordenada donde se finalizó el viaje
    - end_lon: campo de punto flotante que contiene el valor de la longitud de la coordenada donde se finalizó el viaje
    - start_coords: campo geométrico de tipo *point* que almacena la coordenada completa del punto donde se inició el viaje. Puede utilizarse para cruzar la información con capas de información como los perímetros de cada comuna o áreas donde el vehículo no debería transitar (sólo por mostrar un par de ejemplos de su posible aplicación a futuro)
    - end_coords: campo geométrico de tipo *point* que almacena la coordenada completa del punto donde se finalizó el viaje

Para la carga de los resumenes diarios, creé la tabla awto_resumen_diario que contiene 8 campos:
  - resumen_id: campo numérico que contiene un identificador único por día (se crea al formatear la fecha como 'YYYYMMDD'). Puede servir para ordenar más rápidamente que por la fecha
  - fecha_resumen: campo de fecha que contiene el día al que corresponde la fila
  - total_viajes: campo numérico que contiene el total de viajes que se encuentran en la tabla awto_trip. Se debería filtrar la información de los registros que se consideran como "válidos" según el status_id. Dado que no se entrega la información sobre el significado de cada valor, trabajé con el supuesto de que los estados válidos eran 1, 2, 3 y 4 (esto también aparece explicado en el código del script *cargaResumen.py*)
  - suma_ingresos_neto: campo numérico (decimal) que contiene la suma de los valores sin impuesto de los viajes correspondientes a la fecha procesada
  - suma_ingresos_bruto: campo numérico (decimal) que contiene la suma de los valores totales (incluyendo impuestos) de los viajes correspondientes a la fecha procesada
  - promedio_ingresos_neto: campo numérico (decimal) que contiene el promedio de los valores sin impuesto de los viajes correspondientes a la fecha procesada
  - promedio_ingresos_bruto: campo numérico (decimal) que contiene el promedio de los valores totales (incluyendo impuestos) de los viajes correspondientes a la fecha procesada
  - total_metros_recorridos: campo numérico (decimal) que contiene la suma de los valores del campo *travel_dist* de la tabla awto_trip. Como se menciona más arriba, es necesario estar seguros de la unidad que se utiliza (metros o kilómetros) para evitar valores inconsistentes

Para asegurar la consistencia de los datos, se puede incorporar una lista de procesos que vayan validando los datos a medida que se leen desde el origen de datos (para efectos de este ejercicio, son los que se obtienen desde el archivo CSV):
  - Validar que cada valor corresponde al tipo de dato que se definió al crear la tabla. A modo de ejemplo, los campos numéricos no deberían incluir caracteres
  - Validar que cada valor se encuentra dentro de un rango "permitido". Se debería definir el intervalo de valores que se pueden almacenar en cada campo (por ejemplo, que el precio de un viaje no sea negativo) y chequear que el valor que se está recibiendo se encuentra dentro de los valores permitidos
  - Validar que los campos de identificadores (como el identificador de usuario, vehículo, etc) tengan valores y no vengan en blanco

Si se detectan inconsistencias al realizar estas validaciones, se debe separar el registro completo y marcarlo para una revisión posterior, sin insertarlo en la tabla awto_trip hasta que se resuelvan las inconsistencias.

Se puede utilizar alguna herramienta como Informatica Data Quality o IBM Databand (por mencionar sólo 2) para descubrir y luego corregir inconsistencias y errores en los datos, y así, una vez que se resuelven los errores existentes, crear un proceso de validación de integridad de los datos que revise los datos de manera periódica mediante un proceso batch que ejecute un script de análisis y envíe un reporte final con el estado de los registros (en el caso que las inconsistencias no se puedan resolver de manera automática).

Para incorporar un sistema de descuentos mediante cupones, yo agregaría 2 nuevas tablas:
  - awto_cupon: Tabla que contiene una lista de cupones de descuento. Al menos debe tener 5 campos:
    - cupon_id: campo numérico que contiene un identificador único para el cupón
    - valor_descuento: campo numérico (decimal) con el valor que se descontará si se utiliza este cupón
    - fecha_inicio: campo de tipo fecha que almacena el valor del día cuando desde cuando se puede utilizar este cupón
    - fecha_termino: campo de tipo fecha que almacena el valor del día cuando hasta cuando se puede utilizar este cupón
    - status: campo numérico que indica si el cupón está vigente para ser utilizado
  - awto_cupon_usuario: Tabla que contiene la relación entre la tabla awto_cupon y la tabla awto_user. Al menos debe tener 3 campos:
    - cupon_usuario_id: campo numérico que contiene un identificador único para cada registro
    - cupon_id: campo numérico que se obtiene desde la tabla awto_cupon
    - user_id: campo numérico que se obtiene desde la tabla awto_user
    - trip_id: campo numérico que se obtiene desde la tabla awto_trip y que indica el viaje en que el cupón fue utilizado por el usuario
Además, modificaría la tabla awto_trip agregando el siguiente campo:
  - total_discount: campo numérico (decimal) que contiene la suma de los valores de descuento de los cupones utilizados en el viaje

Esta estrategia permitiría mantener ordenada la información relacionada con el uso del cupón, ya que relaciona la información del viaje con el usuario (con lo que se puede obtener la fecha cuando un usuario usó el cupón, mirando la fecha del viaje) y permite también registrar los cupones que ha ido acumulando un usuario en la tabla awto_cupon_usuario. Suponiendo que la forma de conceder cupones a los usuarios se basa en su comportamiento (cantidad de viajes totales, total de kilómetros, antigüedad del usuario, etc), se debería implementar un script automático que realice un barrido completo del historial de cada usuario y a medida que encuentre un usuario que cumple con algún criterio que le hace merecer un cupón, se va agregando la información de ese cupón para ese usuario en la tabla awto_cupon_usuario para que sea utilizado posteriormente.
