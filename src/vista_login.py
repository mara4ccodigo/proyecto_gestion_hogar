#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha: 26/08/2026
# Archivo: vista_login.py
# Descripción:
#   Ventana de login para acceso al sistema de gestión hogareña.
#   Permite ingresar usuario y contraseña con opción de registro,
#   validación de datos y comunicación con el controlador principal.
#=============================================================================

import tkinter as tk
from tkinter import messagebox

from modelo_usuario import Usuario

class VentanaLogin(tk.Tk):
    """
    Ventana de login para que el usuario ingrese al sistema.

    Permite ingresar usuario y contraseña, con opciones de ingreso y registro.
    """

    def __init__(self, controlapp):
        """
        Inicializa la ventana de login.

        Args:
            controlapp (AppGestion): Instancia del controlador principal.
        """
        super().__init__()
        self.controlapp = controlapp
        self.title("Ingreso al Sistema")
        self.geometry("350x260")
        self.configure(bg="#0606A0")
        self.resizable(False, False)
        self._crear_widgets()

    def _crear_widgets(self):
        """
        Crea los widgets de la ventana de login: entradas, labels y botones.
        """
        tk.Label(self, text="Usuario (4-10 caracteres):", bg="#ef0b0b",
                 fg="white", font=("Arial", 10, "bold")).pack(pady=(20, 5))

        self.entrada_usuario = tk.Entry(
            self, font=("Arial", 10), justify="center"
            )
        self.entrada_usuario.pack(pady=5, ipady=2)

        tk.Label(self, text="Contraseña:", bg="#0606A0", fg="white",
                 font=("Arial", 10, "bold")).pack(pady=(10, 5))

        self.entrada_password = tk.Entry(
            self, show="*", font=("Arial", 10), justify="center"
            )
        self.entrada_password.pack(pady=5, ipady=2)

        frame_botones = tk.Frame(self, bg="#0606A0")
        frame_botones.pack(pady=20)

        btn_ingresar = tk.Button(
            frame_botones, text="Ingresar", bg="#10b981", fg="white",
                                 relief="flat", width=12, 
                                 font=("Arial", 9, "bold"),
                                 command=self._procesar_ingreso
                                 )
        btn_ingresar.pack(side=tk.LEFT, padx=10)

        btn_registrar = tk.Button(
            frame_botones, text="Registrarse", bg="#3b82f6", fg="white",
                                  relief="flat", width=12, font=("Arial", 9, "bold"),
                                  command=self._procesar_registro
                                  )
        btn_registrar.pack(side=tk.LEFT, padx=10)

    def _procesar_ingreso(self):
        """
        Procesa los datos ingresados para validar login y permitir acceso.
        """
        usuario = self.entrada_usuario.get()
        clave = self.entrada_password.get()
        user = Usuario(usuario, clave)
        if user.validar():
            if user.existe_en_bd():
                self.controlapp.login_correcto()
            else:
                messagebox.showerror("Error", "Usuario no registrado.")

    def _procesar_registro(self):
        """
        Procesa el registro de un usuario nuevo con los datos ingresados.
        """
        usuario = self.entrada_usuario.get()
        clave = self.entrada_password.get()
        user = Usuario(usuario, clave)
        user.registrar()
