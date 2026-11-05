#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha: 26/08/2026
# Archivo: modelo_usuario.py
# Descripción:
#   Modelo para gestionar usuarios, incluyendo validación, registro y consulta
#   en la base de datos. Adaptado para evitar importación circular.
#=============================================================================

import re
from tkinter import messagebox
from db_manager import DBManager
from constantes import PATRON_USUARIO, CONTRASENIA_SISTEMA

class Usuario:
    """
    Modelo Usuario: maneja validación, registro y consulta de usuarios.

    Atributos:
        nombre_usuario (str): Nombre del usuario del sistema.
        clave (str): Contraseña ingresada por el usuario.

    """

    def __init__(self, nombre_usuario, clave):
        """
        Inicializa un objeto Usuario.

        Args:
            nombre_usuario (str): Nombre del usuario a validar o registrar.
            clave (str): Contraseña del usuario (se convierte a mayúsculas).

        """    
        self.nombre_usuario = nombre_usuario
        self.clave = clave.upper()
        self.db = DBManager()

    def validar(self):
        """
        Valida el formato del nombre de usuario y contraseña.
        
        Returns:
            bool: True si la validación es correcta, False en caso contrario.

        """
        if not PATRON_USUARIO.match(self.nombre_usuario):
            messagebox.showerror(
                "Error de Validación",
                "El usuario debe tener entre 4 y 10 caracteres alfanuméricos."
                )
            return False
        if self.clave != CONTRASENIA_SISTEMA:
            messagebox.showerror("Error de Acceso", "Contraseña incorrecta.")
            return False
        return True

    def existe_en_bd(self):
        """
        Verifica si el usuario ya está registrado en la base de datos.

        Returns:
            bool: True si el usuario existe, False si no o error.

        """
        try:
            usuario = self.db.obtener_usuario(self.nombre_usuario)
            return usuario is not None
        except Exception as e:
            messagebox.showerror(
                "Error Base de Datos", f"Error consultando usuario: {e}"
                )
            return False

    def registrar(self):
        """
        Registra un nuevo usuario en la base de datos.

        Returns:
            bool: True si el registro fue exitoso,
            False si el usuario ya existe o ocurre un error.

            
        Ejemplo:

            >>> usuario = Usuario("mara123", "HOGAR")
            >>> usuario.registrar()
            True 

        """

        if self.existe_en_bd():
            messagebox.showwarning(
                "Advertencia", 
                f"El usuario '{self.nombre_usuario}' ya está registrado."
                )
            return False
        try:
            self.db.insertar_usuario(self.nombre_usuario, self.clave)
            messagebox.showinfo(
                "Éxito", 
                f"Usuario '{self.nombre_usuario}' registrado correctamente."
                )
            return True
        except Exception as e:
            messagebox.showerror(
                "Error Base de Datos", f"Error registrando usuario: {e}"
                )
            return False
