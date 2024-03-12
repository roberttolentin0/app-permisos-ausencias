import psycopg2

conn_params = {
    "host": "40.86.9.189",
    "database": "RhDB2",
    "user": "sqladmin",
    "password": "Slayer20fer..",
    "port": "5433"
}
# RhDB = PostgreSql(
#                 host="40.86.9.189",
#                 db="RhDB2",
#                 user="sqladmin",
#                 password="Slayer20fer.."
#                 ,port="5433")
try:
    conn = psycopg2.connect(**conn_params)
    print("Conexión exitosa a la base de datos PostgreSQL")
    # Aquí puedes realizar operaciones en la base de datos utilizando la conexión 'conn'
    cur = conn.cursor()
    cur.execute("select dni, fullname, lastname, surname, cellphone, email, salary from employee")
    # Retrieve query results
    records = cur.fetchall()
    print('records', records)
    # Recorremos los resultados y los mostramos
    for element in cur :
        print(element)
    conn.close()  # No olvides cerrar la conexión cuando hayas terminado
except psycopg2.Error as e:
    print("Error al conectar a la base de datos PostgreSQL:", e)

# # conn_params = {
# #             "host": "localhost",
# #             "database": "db_permisos",
# #             "user": "postgres",
# #             "password": "1234",
# #             "port": "5432"
# #         }

# # try:
# #     conn = psycopg2.connect(**conn_params)
# #     print("Conexión exitosa a la base de datos PostgreSQL")
# #     # Aquí puedes realizar operaciones en la base de datos utilizando la conexión 'conn'
# #     cur = conn.cursor()
# #     cur.execute("select * from permissions")
# #     # Retrieve query results
# #     records = cur.fetchall()
# #     print('records', records)
# #     # Recorremos los resultados y los mostramos
# #     for element in cur :
# #         print(element)
# #     conn.close()  # No olvides cerrar la conexión cuando hayas terminado
# # except psycopg2.Error as e:
# #     print("Error al conectar a la base de datos PostgreSQL:", e)

