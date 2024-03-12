import traceback
import psycopg2

# Logger
from src.utils.Logger import Logger

def get_connection():
        conn_params = {
            "host": "localhost",
            "database": "db_permisos",
            "user": "postgres",
            "password": "1234",
            "port": "5432"
        }

        try:
            conn = psycopg2.connect(**conn_params)
            print("Conexión exitosa a la base de datos PostgreSQL")
            return conn
            # conn.close()  # No olvides cerrar la conexión cuando hayas terminado
        except psycopg2.Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())