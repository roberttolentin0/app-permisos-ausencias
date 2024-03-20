from flask import request, jsonify
import requests
import json
import time

def send_notification_to_teams(data):
    # Añadir la lógica para enviar la notificación
    url_webhook = "https://mistrperu.webhook.office.com/webhookb2/a4eae717-ded2-402a-8dd6-071d5ab0b3cd@ceb88b8e-4e6a-4561-a112-5cf771712517/IncomingWebhook/8f66bb8e4f644abeaf4f0461daa1caa7/f17e9692-d4c9-4514-906e-286f3f4245bd"
    payload_notificacion = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "Notificación",
        "sections": [
            {
                "activityTitle": "Notificaciones del aplicativo",
                "activityImage": "https://1.bp.blogspot.com/-z6LMrSwx_XA/XbhhKRAfMZI/AAAAAAAAoFs/CCSm0SMIq-47MjxmjGvnmcZd4DN3GG63QCLcBGAsYHQ/s1600/email-4539382_1280.jpg",
                "facts": [
                    {"name": "Descripción del inconveniente : ", "value": data["descripcion"]},
                    {"name": "Empleado : ", "value": data["empleado_datos"]},
                    {"name": "DNI : ", "value": data["empleado_dni"]},
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
    # print(response_notificacion)
    # Enviar la respuesta de la notificación al cliente
    if response_notificacion.status_code == 200:
        print( "Notificación enviada correctamente")
    else:
        print( "Error al enviar la notificación")


def is_return_time_expire(empleado):
    hora_actual = time.strftime("%H:%M")
    return_time= empleado["return_time"]
    print(hora_actual, return_time)
    tiempo_espera = (time.strptime(return_time, "%H:%M").tm_hour - time.strptime(hora_actual, "%H:%M").tm_hour) * 3600 + (time.strptime(return_time, "%H:%M").tm_min - time.strptime(hora_actual, "%H:%M").tm_min) * 60
    print('tiempo_espera', tiempo_espera)
    if tiempo_espera > 0 and tiempo_espera <= 600:  # Si faltan 10 minutos o menos para la hora de salida
        return True

# Ejemplo de empleados (pueden ser obtenidos de la base de datos)
empleados = [
    {"nombre": "Empleado 1", "return_time": "23:24", "webhook_url": "URL_DEL_WEBHOOK_DE_EMPLEADO_1"},
    {"nombre": "Empleado 2", "return_time": "23:35", "webhook_url": "URL_DEL_WEBHOOK_DE_EMPLEADO_2"}
]

def main():
    while True:
        for empleado in empleados:
            if is_return_time_expire(empleado):
                mensaje = f"¡{empleado['nombre']} está por cumplir! Su hora de retorno a las {empleado['return_time']}."
                print(mensaje)
                data = {
                'empleado_datos' : 'Robert Carlos Tolentino Mendoza',
                'empleado_dni' : '47518568',
                'descripcion' : mensaje,
                }
                send_notification_to_teams(data)
        time.sleep(60)  # Verificar cada minuto
main()