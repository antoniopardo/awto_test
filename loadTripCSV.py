import pandas as pd
import psycopg2 as pg
import psycopg2.extras as extras

######################################################
##
##  Bloques de codigo
##
## 1 .- Crear Tablas
## 2 .- Cargar DataFrame con Csv
## 3 .- Separar Datos para cada tabla
## 4 .- Insertar Datos en cada tabla
## 5 .- Cerrar conexiones
##
######################################################

def carga_valores(conexion, cursor, df, tabla, valida):

    tuplas = [tuple(x) for x in df.to_numpy()]
    
    if (valida):
        valores_unicos = list(set(tuplas))
        lista_salida = []
        for registro in valores_unicos:
           query = "SELECT 1 FROM %s WHERE %s = %s" % (tabla, df.columns[0], registro[0])
           cursor.execute(query)
           reg_temporal = cursor.fetchall()
           if (len(reg_temporal) == 0):
            lista_salida.append(registro)
        tuplas = lista_salida
        
    cols = ','.join(list(df.columns))

    query = "INSERT INTO %s(%s) VALUES %%s" % (tabla, cols)

    try:
        extras.execute_values(cursor, query, tuplas)
        conexion.commit()
    except (Exception, pg.DatabaseError) as error:
        print("Error: %s" % error)
        conexion.rollback()
        return 1
    print(" *** Datos cargados en tabla ",tabla)

###############
## Punto 1
###############

scripts_iniciales = ("""
        CREATE TABLE IF NOT EXISTS public.awto_user (
            user_id int NOT NULL,
            name_user varchar NOT NULL,
            rut_user varchar NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS public.awto_trip (
            trip_id integer NOT NULL,
            vehicle_id integer NOT NULL,
            booking_time date NULL,
            start_time date NULL,
            end_time date NULL,
            status_id integer NOT NULL,
            travel_dist numeric NULL,
            membership_id integer NULL,
            price_amount numeric NULL,
            price_tax numeric NULL,
            price_total numeric NULL,
            start_lat float NULL,
            start_lon float NULL,
            end_lat float NULL,
            end_lon float NULL,
            start_coords point NULL,
            end_coords point NULL
        )
        """,
        """
        TRUNCATE TABLE public.awto_trip, public.awto_user
        """
        )
conn = pg.connect(host="localhost",database="awto",user="awto",password="4wt0")
cur = conn.cursor()
for comando in scripts_iniciales:
    cur.execute(comando)
conn.commit()

###############
## Punto 2
###############

viajes = pd.read_csv(r"C:\Users\jotap\Documents\Temporales\dataengineer.test-main\trips.csv")

###############
## Punto 3
###############

datos_usuario = viajes[["user_id", "name_user", "rut_user"]]
datos_viaje = viajes[["trip_id", "vehicle_id", "booking_time", "start_time", "end_time", "status_id", "travel_dist", "membership_id", "price_amount", "price_tax", "price_total", "start_lat", "start_lon", "end_lat", "end_lon"]]

###############
## Punto 4
###############

carga_valores(conn, cur, datos_usuario, 'awto_user', 1)
carga_valores(conn, cur, datos_viaje, 'awto_trip', 0)
query = "update awto_trip set start_coords = (point(start_lon, start_lat)), end_coords = (point(end_lon, end_lat));"
cur.execute(query)
conn.commit()

###############
## Punto 5
###############

conn.close()