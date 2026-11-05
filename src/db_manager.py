#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha:26/08/2026
# Archivo: db_manager.py
# Descripción:
#   Módulo que contiene la clase DBManager para gestionar la conexión y 
#   operaciones en la base de datos SQLite3, incluyendo creación de tablas 
#   y CRUD que comence en el curso de Python Inicial.
#=============================================================================

import sqlite3
from contextlib import contextmanager

class DBManager:
    """
    Clase para gestionar la conexión y operaciones en la base de datos.

    Métodos:
        configurar_base_datos(): Crea las tablas necesarias si no existen.
        insertar_usuario(nombre_usuario, clave): Inserta usuario en la tabla.
        obtener_usuario(nombre_usuario): Consulta usuario por nombre.
        insertar_movimiento(...): Inserta un movimiento financiero.
        obtener_movimientos(): Recupera todos los movimientos.
        eliminar_movimiento(id_movimiento): Elimina movimiento por id.
        actualizar_importe(id_movimiento, nuevo_importe): Actualiza importe.
    """
    def __init__(self, ruta_db="gestion_hogar_v3.db"):
        """
        Inicializa el manejador de base de datos.

        Args:
            ruta_db (str): Ruta del archivo de la base de datos SQLite.
        """
        self.ruta_db = ruta_db

    @contextmanager
    def gestionar_conexion(self):
        """
        Context manager para abrir y cerrar conexión con la base de datos.

        Permite realizar operaciones con commit o rollback automático.

        Yields:
            sqlite3.Connection: Objeto de conexión activo.
        """
        conexion = sqlite3.connect(self.ruta_db)
        try:
            yield conexion
            conexion.commit()
        except sqlite3.Error as e:
            conexion.rollback()
            raise e
        finally:
            conexion.close()

    def configurar_base_datos(self):
        """
        Crea tablas necesarias para usuarios y movimientos, si no existen.
        """
        with self.gestionar_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_usuario TEXT NOT NULL UNIQUE,
                    clave TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS movimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    propiedad TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    subcategoria TEXT NOT NULL,
                    importe REAL NOT NULL,
                    fecha_vencimiento TEXT,
                    fecha_pago TEXT,
                    comentarios TEXT
                )
            """)

    def insertar_usuario(self, nombre_usuario, clave):
        """
        Inserta un nuevo usuario en la tabla de usuarios.

        Args:
            nombre_usuario (str): Nombre del usuario.
            clave (str): Contraseña del usuario.

        Ejemplo:
        >>> db = DBManager()
        >>> db.insertar_usuario("mara123", "HOGAR")
        """
        with self.gestionar_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre_usuario, clave) VALUES (?, ?)",
                (nombre_usuario, clave)
            )

    def obtener_usuario(self, nombre_usuario):
        """
        Recupera un usuario por su nombre.

        Args:
            nombre_usuario (str): Nombre del usuario a buscar.

        Returns:
            tuple: Registro del usuario o None si no existe
        """
        with self.gestionar_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre_usuario, clave FROM usuarios WHERE nombre_usuario = ?",
                (nombre_usuario,)
            )
            return cursor.fetchone()

    def insertar_movimiento(self, propiedad, categoria, subcategoria, importe,
                            fecha_vencimiento="", fecha_pago="", comentarios=""):
        with self.gestionar_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO movimientos (
                    propiedad, categoria, subcategoria,
                    importe, fecha_vencimiento, fecha_pago, comentarios
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (propiedad, categoria, subcategoria, importe,
                  fecha_vencimiento, fecha_pago, comentarios))

    def obtener_movimientos(self):
        with self.gestionar_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id, propiedad, categoria, subcategoria,
                    importe, fecha_vencimiento, fecha_pago, comentarios
                FROM movimientos ORDER BY id DESC
            """)
            return cursor.fetchall()

    def eliminar_movimiento(self, id_movimiento):
        with self.gestionar_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM movimientos WHERE id = ?", (id_movimiento,))

    def actualizar_importe(self, id_movimiento, nuevo_importe):
        with self.gestionar_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE movimientos SET importe = ? WHERE id = ?",
                (nuevo_importe, id_movimiento)
            )

