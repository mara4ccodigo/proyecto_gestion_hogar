#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha: 02/11/2026
# Archivo: logger_decorator.py
# Descripción:
#   Última actualización: Modifico mi archvo logger_decorator.py para
#   guardar el log localmente en registro_operaciones.txt
#   Ahora el decorador registra las llamadas a funciones en el archivo local 
#   y envia logs al servidor remoto vía socket TCP.
#=============================================================================

from datetime import datetime
import functools
import os
import socket

RUTA_LOG = os.path.join(os.path.dirname(__file__), "registro_operaciones.txt")
RUTA_LOG_ERRORES = os.path.join(os.path.dirname(__file__), "errores_log.txt")

# Configuración conexión servidor remoto de logs
REMOTE_HOST = "192.168.1.53"  # Reemplazo por IP real de mi PC servidor
REMOTE_PORT = 9999             # Puerto configurado en servidor_logs.py

def enviar_log_remoto(mensaje):
    """
    Envía un mensaje al servidor remoto TCP para registro de log.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((REMOTE_HOST, REMOTE_PORT))
        s.sendall(mensaje.encode("utf-8"))

def registro_log(func):
    """
    Decorador que registra la llamada de una función con timestamp,
    guarda en archivo local, envía mensaje al servidor remoto y maneja
    errores para no interrumpir flujo principal.
    Args:
        func (function): Función a decorar.
    Returns:
        function: Función decorada.
    """
    @functools.wraps(func)
    def envoltura(*args, **kwargs):
        ahora = datetime.now().isoformat(sep=' ', timespec='seconds')
        nombre_func = func.__name__
        linea_log = f"{ahora} - Llamada a función: {nombre_func}"
        try:
            with open(RUTA_LOG, "a", encoding="utf-8") as archivo_log:
                archivo_log.write(linea_log + "\n")
        except Exception as e:
            try:
                with open(RUTA_LOG_ERRORES, "a", encoding="utf-8") as archivo_err:
                    archivo_err.write(f"{ahora} - Error escribiendo log: {e}\n")
            except Exception:
                pass
        try:
            enviar_log_remoto(linea_log)
        except Exception:
            # Ignora errores de conexión para no afectar 
            pass
        return func(*args, **kwargs)
    return envoltura
