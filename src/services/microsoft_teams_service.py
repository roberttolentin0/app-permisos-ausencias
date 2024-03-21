import threading
import time
import requests
import psycopg2
import json

# Variable global para controlar el cron
cron_activo = False

# Clase para manejar la conexión y consultas a la base de datos
class DatabaseManager:
    def __init__(self):
        # Conectarse a la base de datos
        self.conn = psycopg2.connect(
            dbname="db_permisos",
            user="postgres",
            password="1234",
            host="localhost"
        )

    def connection(self):
        return self.conn

    # Método para obtener empleados con estado de permiso "ACTIVADO"
    def obtener_permisos_aceptados(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT name, return_time, reason, status, observation
	                FROM public.view_permissions WHERE status = 'ACEPTADO'""")
        permisos = cur.fetchall()
        cur.close()
        permisos_json = []
        for row in permisos:
            permiso = {}
            permiso['name'] = row[0]
            permiso['return_time'] = row[1]
            permisos_json.append(permiso)
        return permisos_json

def send_notification_to_teams(data):
    # Añadir la lógica para enviar la notificación
    url_webhook = "https://mistrperu.webhook.office.com/webhookb2/a4eae717-ded2-402a-8dd6-071d5ab0b3cd@ceb88b8e-4e6a-4561-a112-5cf771712517/IncomingWebhook/8f66bb8e4f644abeaf4f0461daa1caa7/f17e9692-d4c9-4514-906e-286f3f4245bd"
    payload_notificacion = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "Notificación",
        "sections": [
            {
                "activityTitle": "Notificacion del App permisos de salida",
                "activityImage": "https://1.bp.blogspot.com/-z6LMrSwx_XA/XbhhKRAfMZI/AAAAAAAAoFs/CCSm0SMIq-47MjxmjGvnmcZd4DN3GG63QCLcBGAsYHQ/s1600/email-4539382_1280.jpg",
                "facts": [
                    {"name": "Empleado : ", "value": data["empleado_datos"]},
                    {"name": "Descripción: ", "value": data["descripcion"]},
                ],
                "potentialAction": [],
            }
        ],
    }
    print('payload_notificacion', payload_notificacion)
    headers_notificacion = {"Content-Type": "application/json"}
    response_notificacion = requests.post(
        url_webhook, headers=headers_notificacion, data=json.dumps(payload_notificacion)
    )
    # Enviar la respuesta de la notificación al cliente
    if response_notificacion.status_code == 200:
        print( "Notificación enviada correctamente")
    else:
        print( "Error al enviar la notificación")

# Función para verificar la hora de salida de un empleado
def verificar_hora_de_retorno_empleado(permiso):
    curr_time = time.strftime("%H:%M")
    return_time_str = permiso["return_time"].strftime('%H:%M')
    return_time = time.strptime(return_time_str, "%H:%M")
    tiempo_espera = (return_time.tm_hour - time.strptime(curr_time, "%H:%M").tm_hour) * 3600 + (return_time.tm_min - time.strptime(curr_time, "%H:%M").tm_min) * 60
    print(tiempo_espera)
    if 0 < tiempo_espera <= 900:  # Si faltan 15 minutos o menos para la hora de retorno
        msg = f"¡Está por Retornar! Su hora de Retorno es a las {return_time_str}"
        data = {
                'empleado_datos' : permiso['name'],
                'descripcion' : msg,
                }
        send_notification_to_teams(data)

def programar_verificacion_hora_retorno_empleados_aceptados(permisos_aceptados):
    for permiso in permisos_aceptados:
        verificar_hora_de_retorno_empleado(permiso)

def verificar_permisos_aceptados_cada_media_hora(db_manager):
    global cron_activo

    while cron_activo:
        print('-----cron_activo-----', cron_activo)
        permisos_aceptados = db_manager.obtener_permisos_aceptados()
        print('Cantidad de permisos ACEPTADOS', len(permisos_aceptados))
        if len(permisos_aceptados) == 0:
            cron_send_notification_teams('END')
            break
        programar_verificacion_hora_retorno_empleados_aceptados(permisos_aceptados)
        time.sleep(300)  # Esperar 5 minuto antes de volver a verificar la hora de retorno
    print("Hilo de verificación de estado detenido.")
    db_manager.connection().close()

def main():
    db_manager = DatabaseManager()
    verificar_permisos_aceptados_cada_media_hora(db_manager)

def cron_send_notification_teams(estado):
    global cron_activo
    if estado == 'INIT':
        if cron_activo == False:
            # Iniciar el cron si no está activo
            cron_activo = True
            threading.Thread(target=main).start()
    else:
        # Detener el cron si está activo
        cron_activo = False
    # Obtener el número de hilos activos
    num_hilos_activos = threading.active_count()
    print(f"Número de hilos activos: {num_hilos_activos}")

# cambiar_estado('ACEPTADO')
# time.sleep(30)
# cambiar_estado('')