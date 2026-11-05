#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha: 26/08/2026
# Archivo: movimiento.py
# Descripción:
#   Este módulo representa la evolución a POO en la app de gestión que 
#   realice en el curso de Python Inicial,
#   con la clase Movimiento que encapsula datos 
#   y comportamientos relacionados
#   a movimientos financieros del hogar.
#   Se incluyen validaciones, manejo con excepciones,
#   y operaciones de base de datos integradas.
#   Última actualización: 
#=============================================================================

import re
from tkinter import messagebox
from datetime import datetime
from db_manager import DBManager
from constantes import PATRON_IMPORTE, PATRON_FECHA
from observador import Observable  # Importo la clase Observable


class Movimiento(Observable): # Movimiento hereda de Observable
    """
    Modelo que representa un movimiento financiero del hogar.

    Atributos:
        propiedad (str): Propiedad relacionada.
        categoria (str): Categoría del movimiento.
        subcategoria (str): Subcategoría del movimiento.
        importe (float/str): Importe del movimiento.
        fecha_vencimiento (str): Fecha de vencimiento (opcional).
        fecha_pago (str): Fecha de pago (opcional).
        comentarios (str): Comentarios adicionales.
    """

    def __init__(self, propiedad, categoria, subcategoria, importe,
                 fecha_vencimiento="", fecha_pago="", comentarios=""):
        """
        Inicializa un objeto Movimiento.

        Args:
            propiedad (str): Propiedad asociada.
            categoria (str): Categoría principal.
            subcategoria (str): Subcategoría.
            importe (float/str): Valor monetario.
            fecha_vencimiento (str, optional): Fecha de vencimiento.
            fecha_pago (str, optional): Fecha de pago.
            comentarios (str, optional): Comentarios adicionales.
        """
        super().__init__()  # Inicializo Observable para manejar observadores
        self.propiedad = propiedad
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.importe = importe
        self.fecha_vencimiento = fecha_vencimiento
        self.fecha_pago = fecha_pago
        self.comentarios = comentarios
        self.db = DBManager()

    def validar_importe(self, valor_importe=None):
        """
        Valida el formato del importe.

        Args:
            valor_importe (str, optional): Importe a validar. 
                Si no se proporciona, valida el atributo self.importe.

        Returns:
            bool: True si el formato es válido, False en caso contrario.
        """
        texto = str(
            valor_importe if valor_importe is not None else self.importe
            ).replace(",", ".")
        return bool(PATRON_IMPORTE.match(texto))


    def validar_fecha(self, fecha_texto):
        """
        Valida que una fecha tenga formato correcto dd/mm/aa(aa).

        Args:
            fecha_texto (str): Cadena con la fecha.

        Returns:
            bool: True si la fecha es válida o está vacía (opcional), 
            False si es inválida.
        """
        if not fecha_texto:
            return True  # campo opcional vacío
        if not PATRON_FECHA.match(fecha_texto):
            return False
        try:
            dia, mes, anio = fecha_texto.split("/")
            if len(anio) == 2:
                anio = "20" + anio
            datetime.strptime(f"{dia}/{mes}/{anio}", "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def validar(self):
        """
        Valida todas las propiedades del movimiento.

        Returns:
            bool: True si todas las validaciones son correctas, 
            False en caso contrario.

        Ejemplo:
        >>> mov = Movimiento("Avellaneda 250 (MG)", "Servicios", 
        >>> "Edesur", "300.50", "01/09/2026", "05/09/2026")
        >>> mov.validar()
        True
        """
        if self.propiedad == "----DESPLEGAR----":
            messagebox.showerror("Error", "Seleccione una propiedad válida.")
            return False
        if self.categoria == "----DESPLEGAR----":
            messagebox.showerror("Error", "Seleccione una categoría válida.")
            return False
        if not self.validar_importe():
            messagebox.showerror("Error", "Formato de importe inválido.")
            return False
        if self.categoria == "Servicios":
            if not (
                self.validar_fecha(
                    self.fecha_vencimiento) and self.validar_fecha(
                    self.fecha_pago)
                    ):
                messagebox.showerror("Error", "Formato de fechas inválidas.")
                return False
        return True

    def guardar(self):
        """
        Guarda el movimiento en la base de datos si es válido.

        Returns:
            bool: True si se guardó correctamente, False de lo contrario.
        
        Ejemplo:
        >>> mov = Movimiento("Avellaneda 266 (MG)", "Alimentos y Bebidas", 
        "Chino", "150.75")
        >>> mov.guardar()
        True
        """
        if not self.validar():
            return False
        importe_num = float(
            str(self.importe).replace(".", "").replace(",", ".")
            )
        fv = self.fecha_vencimiento if self.categoria == "Servicios" else ""
        fp = self.fecha_pago if self.categoria == "Servicios" else ""
        try:
            self.db.insertar_movimiento(
                self.propiedad, self.categoria, self.subcategoria,
                importe_num, fv, fp, self.comentarios
            )
            messagebox.showinfo("Éxito", "Movimiento guardado correctamente.")
            self.notificar(
                f"Movimiento guardado: {self.propiedad}, {self.categoria}, "
                f"{self.subcategoria}, importe: {importe_num}"
            ) # Notificar el evento
            return True
        except Exception as e:
            messagebox.showerror("Error BD", 
                                 f"No se pudo guardar el movimiento: {e}")
            return False

    def obtener_todos(self):
        """
        Obtiene todos los movimientos de la base de datos.

        Returns:
            list: Lista de movimientos.
        """
        return self.db.obtener_movimientos()

    def eliminar(self, id_movimiento):
        """
        Elimina un movimiento por su ID.

        Args:
            id_movimiento (int): Identificador del movimiento a eliminar.
        """
        try:
            self.db.eliminar_movimiento(id_movimiento)
            messagebox.showinfo("Éxito", 
                                "Movimiento eliminado correctamente.")

        except Exception as e:
            messagebox.showerror("Error BD", 
                                 f"No se pudo eliminar el movimiento: {e}")

    def actualizar_importe(self, id_movimiento, nuevo_importe):
        """
        Actualiza el importe de un movimiento dado su ID.

        Args:
            id_movimiento (int): ID del movimiento.
            nuevo_importe (float): Nuevo importe para actualizar.
        """
        try:
            self.db.actualizar_importe(id_movimiento, nuevo_importe)
            messagebox.showinfo("Éxito", "Importe modificado correctamente.")
            self.notificar(
                f"Importe actualizado id: {id_movimiento} "
                f"nuevo importe: {nuevo_importe}"
            )

        except Exception as e:
            messagebox.showerror("Error BD", 
                                 f"No se pudo modificar el importe: {e}")
# Mi primer ejemplo para documentar
def ejemplo_docstring():
    """
    Esta es una función de ejemplo para demostrar docstrings.

    Returns:
        str: Mensaje de éxito.
    """
    return "Docstring generado correctamente"

