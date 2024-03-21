import os
import traceback
import psycopg2

# Logger
from src.utils.Logger import Logger
from dotenv import load_dotenv

load_dotenv()


class DBConnection:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn = None

    def connect(self):
        try:
            conn_params = {
                "host": self.host,
                "database": self.database,
                "user": self.user,
                "password": self.password,
                "port": self.port
            }
            self.conn = psycopg2.connect(**conn_params)
            print("Conexión exitosa a la base de datos PostgreSQL")
            return self.conn
        except psycopg2.Error as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

    def close(self):
        if self.conn is not None:
            self.conn.close()
            print("Conexión cerrada")


class PGConnection(DBConnection):
    def __init__(self):
        host = os.getenv('DB_HOST')
        database = os.getenv('DB_DATABASE')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        port = os.getenv('DB_PORT')
        super().__init__(host, database, user, password, port)


class RhDBConnection(DBConnection):
    def __init__(self):
        host = "40.86.9.189"
        database = "RhDB2"
        user = "sqladmin"
        password = "Slayer20fer.."
        port = "5433"
        super().__init__(host, database, user, password, port)


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