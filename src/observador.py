#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha: 02/11/2026
# Archivo: observador.py
# Descripción:
#   Implementación del patrón observador para registro de logs.
#   Observable permite añadir y notificar observadores.
#   ObserverLog registra eventos en un archivo con timestamp.
#=============================================================================

from datetime import datetime
import os

class Observable:
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def eliminar_observador(self, observador):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar(self, evento):
        for obs in self._observadores:
            obs.actualizar(evento)


class ObserverLog:
    RUTA_LOG = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'logs', 
                     'log_observador.txt')
    )

    def actualizar(self, evento):
        ahora = datetime.now().isoformat(sep=' ', timespec='seconds')
        linea = f"{ahora} - Evento: {evento}\n"
        try:
            with open(self.RUTA_LOG, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except Exception:
            # Ignorar errores para no interrumpir ejecución
            pass
