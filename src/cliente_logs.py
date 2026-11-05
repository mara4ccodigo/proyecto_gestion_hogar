#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha: 02/11/2026
# Archivo: cliente_logs.py
# Descripción:
#   Cliente TCP básico para enviar mensajes de log al servidor de logs.
#   Última actualizacion: Realizo prueba 4/11/2026
#=============================================================================

import socket

# Cambio la IP por la dirección de mi PC servidor en la red local
HOST = "192.168.1.53"  # ReemplazO con la IP real de mi PC
PORT = 9999             # El mismo puerto del servidor


def enviar_log(mensaje):
    """
    Se conecta al servidor y envía un mensaje de log.

    Args:
        mensaje (str): Texto del log a enviar.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(mensaje.encode("utf-8"))
            # No espera respuesta, solo envía y cierra
    except Exception as e:
        print(f"[CLIENTE] Error enviando log: {e}")


if __name__ == "__main__":
    # Ejemplo de envío de log de prueba
    texto_log = "Mensaje de log enviado desde cliente de prueba."
    enviar_log(texto_log)
    print("[CLIENTE] Mensaje enviado al servidor.")
