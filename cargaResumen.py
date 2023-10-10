import psycopg2 as pg

######################################################
##
##  Bloques de codigo
##
## 1 .- Crear Tabla
## 2 .- Obtener fechas desde tabla awto_trip
## 3 .- Iterar sobre las fechas y realizar la carga en tabla awto_resumen_diario
## 4 .- Cerrar conexiones
##
######################################################

conn = pg.connect(host="localhost",database="awto",user="awto",password="4wt0")
cur = conn.cursor()

###############
##
## Lista de status_id que son relevantes para el resumen (No se debería considerar los viajes cancelados, por ejemplo)
## Para efectos de este ejercicio, supondre que existen 4 estados validos: 1,2,3 y 4
##
###############

estados_validos = "1,2,3,4"

###############
## Punto 1
###############

crea_tabla = """CREATE TABLE IF NOT EXISTS public.awto_resumen_diario (
	resumen_id int4 NOT NULL,
	fecha_resumen date NOT NULL,
	total_viajes int4 NOT NULL DEFAULT 0,
	suma_ingresos_neto numeric NOT NULL DEFAULT 0,
	suma_ingresos_bruto numeric NOT NULL DEFAULT 0,
	promedio_ingresos_neto numeric NOT NULL DEFAULT 0,
	promedio_ingresos_bruto numeric NOT NULL DEFAULT 0,
	total_metros_recorridos numeric NOT NULL DEFAULT 0
    )"""
cur.execute(crea_tabla)

###############
## Punto 2
###############

query = "select distinct to_char(date(start_time), 'YYYY-MM-DD') as fecha from awto_trip order by fecha"
cur.execute(query)

fechas = cur.fetchall()

###############
## Punto 3
###############

query_carga = "insert into awto_resumen_diario select '%%s', '%%s', count(*) as total_viajes, sum(price_amount) as suma_ingresos_neto, sum(price_total) as suma_ingresos_bruto, avg(price_amount) as promedio_ingresos_neto, avg(price_total) as promedio_ingresos_bruto, sum(travel_dist) as metros_recorridos from awto_trip where date(start_time) = '%%s' and status_id in (%s)" % estados_validos;

for fecha in fechas:
    valor_fecha = str(fecha[0])
    fecha_id = valor_fecha.replace('-','')
    cur.execute(query_carga % (fecha_id, valor_fecha, valor_fecha))
	
conn.commit()

###############
## Punto 4
###############

conn.close()