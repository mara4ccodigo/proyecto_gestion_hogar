#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha: 31/10/2026
# Archivo: servidor_logs.py
# Descripción:
#   Servidor TCP multihilo para la recepción y almacenamiento
#   centralizado de trazas de los logs enviados por los clientes 
#   (en mi caso, se utiliza la notebook como cliente) de la app.
#   Última actualización: Incorporo el registro también eventos de conexión
#   y desconexión en el archivo
#=============================================================================

import os
import socket
import threading

# Configuración del servidor de logs
# Trabajo con mi pc y notebook 
# (Para escuchar las peticiones de cualquier dispositivo de mi red. )
# Cambiar de: HOST = "xxx" a:

HOST = "0.0.0.0"
PORT = 9999
RUTA_LOG_SERV = os.path.join(
    os.path.dirname(__file__), "log_servidor_remoto.txt"
)


def manejar_cliente(conn, addr):
    """
    Atiende la conexión de un cliente en un hilo, recibe mensajes
    de log  y se escribe en el archivo centralizado.
    También registra la conexión y desconexión en el archivo.
    """
    print(f"[SERVIDOR] Conexión establecida desde {addr}")
    # Registrar conexión en archivo
    try:
        with open(RUTA_LOG_SERV, "a", encoding="utf-8") as f:
            f.write(f"[INFO] Conexión establecida con {addr}\n")
    except Exception:
        pass
    activo = True
    try:
        while activo:
            datos = conn.recv(1024)
            if not datos:
                activo = False
            else:
                mensaje = datos.decode("utf-8").strip()
                print(f"[SERVIDOR] Log recibido: {mensaje}")
                with open(RUTA_LOG_SERV, "a", encoding="utf-8") as f:
                    f.write(mensaje + "\n")
    except Exception as e:
        print(f"[SERVIDOR] Error manejando cliente {addr}: {e}")
    finally:
        conn.close()
        print(f"[SERVIDOR] Conexión cerrada con {addr}")
        # Registrar desconexión en archivo
        try:
            with open(RUTA_LOG_SERV, "a", encoding="utf-8") as f:
                f.write(f"[INFO] Conexión cerrada con {addr}\n")
        except Exception:
            pass
def iniciar_servidor():
    """
    Inicializa el socket del servidor, se enlaza al puerto configurado
    y queda en escucha activa delegando conexiones a nuevos hilos.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reutilizar el puerto si queda en espera en el sistema operativo
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}...")
        while True:
            conn, addr = server.accept()
            # Crear un hilo secundario por cada conexión entrante
            hilo = threading.Thread(
                target=manejar_cliente, args=(conn, addr)
            )
            hilo.daemon = True
            hilo.start()
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Apagando el servidor de logs...")
    except Exception as e:
        print(f"[SERVIDOR] Error crítico en el servidor: {e}")
    finally:
        server.close()

# Chequeo y pruebo
if __name__ == "__main__":
    iniciar_servidor()
