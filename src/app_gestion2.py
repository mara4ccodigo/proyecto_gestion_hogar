#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha: 30/08/2026
# Archivo: app_gestion2.py
# Descripción:
#   Módulo controlador principal de la app de gestión.
#   Integra modelo, vista y acceso a base de datos, manejando validaciones,
#   operaciones CRUD y flujos de inicio y cierre de sesión.
#   Paso del paradigma estructural al POO,
#   centralizando lógica para facilitar mantenimiento y escalabilidad.
#   Última actualización: importo decorador con 4 @registro_log antes de las
#   funciones
#=============================================================================


import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from observador import ObserverLog # Agrego import
from movimiento import Movimiento # Agrego import
from logger_decorator import registro_log # Agrego import


from db_manager import DBManager
from constantes import (
    PATRON_USUARIO, CONTRASENIA_SISTEMA, PATRON_IMPORTE, PATRON_FECHA
) # Para mantener los 79 caracteres


OPCIONES_PROPIEDADES = [
    "----DESPLEGAR----",
    "Avellaneda 250 (MG)",
    "Avellaneda 266 (MG)",
    "Laprida 301 (MG)",
    "Almafuerte (SV)"
]

CATEGORIAS_SISTEMA = {
    "----DESPLEGAR----": [],
    "Alimentos y Bebidas": [
        "Cercania",
        ["Chino", "Josimar", "Carrefour", "Coto", "Día %",
         "Vea", "Disco", "Jumbo", "ChangoMás"],
        "Mayoristas",
        ["Maxiconsumo", "Vital", "Diarco", "Trappal", "Makro", "Tornado"],
        "Delivery",
        ["PedidosYa", "Rappi"],
        "Otros"
    ],
    "Servicios": [
        "Edesur", "MetroGas", "Aysa", "Internet y TV", "Telefonía Celular",
        ["Claro", "Movistar", "Tuenti"]
    ],
    "Impuestos": [
        "Nacionales", "Provinciales", "Municipales", "Patente", "ARBA"
    ],
    "Bancos": [
        "Galicia", "BBVA", "Santander", "Patagonia", "Macro", "Nación"
    ],
    "Billeteras Virtuales": [
        "Cuenta DNI", "Modo", "MercadoPago", "Brubank", "TarjetaNaranja"
    ],
    "Vivienda": ["Expensas", "Mantenimiento Hogar"],
    "Turismo": ["Pasajes", "Alojamiento", "Alquileres", "Gastos corrientes"],
    "Salud": ["Obra Social", "Profesional", "Farmacia"],
    "Movilidad": ["Combustible", "SUBE", "Uber / Cabify", "Peajes", "Taller"],
    "Finanzas": ["Gastos caja chica", "Ahorro", "Inversión"]
}


class AppGestion:

    """
    Clase principal que controla la aplicación de gestión.
    Gestiona la interfaz de usuario, la conexión con la base de datos,
    operacione CRUD y el flujo de inicio y cierre de sesión.

    Atributos:
        ventana_login (tk.Tk): Ventana de login.
        ventana_principal (tk.Tk): Ventana principal de la aplicación.
        db (DBManager): Instancia para manejo de la base de datos.
    """


    def __init__(self):
        """
        Inicializa la aplicación y configura la base de datos.
        """

        self.ventana_login = None
        self.ventana_principal = None
        self.logger_observador = ObserverLog() # Instancia de Observador
        self.db = DBManager()
        self.db.configurar_base_datos()  # Configuración inicial

    def _crear_movimiento_con_observador(self, datos):
        mov = Movimiento(*datos)
        mov.agregar_observador(self.logger_observador)
        return mov

    def iniciar(self):
        """
        Inicia el flujo principal de la aplicación mostrando 
        la ventana de login.
        """
        from vista_login import VentanaLogin
        self.ventana_login = VentanaLogin(self)
        self.ventana_login.mainloop()

    def login_correcto(self):
        """
        Lógica a ejecutar cuando el login es exitoso.
        
        Cierra ventana de login y abre ventana principal.
        """
        if self.ventana_login:
            self.ventana_login.destroy()
            self.ventana_login = None
        self.mostrar_principal()

    def mostrar_principal(self):
        """
        Muestra la ventana principal de la aplicación.
        """
        from vista_principal import VentanaPrincipal
        self.ventana_principal = VentanaPrincipal(self)
        self.ventana_principal.mainloop()

    def cerrar_sesion(self):
        """
        Cierra la sesión actual y vuelve a mostrar la ventana de login.
        """
        if self.ventana_principal:
            self.ventana_principal.destroy()
            self.ventana_principal = None
        self.iniciar()

    def obtener_propiedades(self):
        """
        Obtiene las opciones de las propiedades disponibles

        Returns: Lista de propiedades.
        """
        return OPCIONES_PROPIEDADES

    def obtener_categorias(self):
        """
        Obtiene la lista de categorías disponibles.

        Returns:
            list: Lista de categorías.
        """
        return list(CATEGORIAS_SISTEMA.keys())

    def obtener_subcategorias(self, categoria):
        """
        Obtiene las subcategorías correspondientes a una categoría.

        Args:
            categoria (str): Nombre de la categoría seleccionada.

        Returns:
            list: Lista de subcategorías.
        """
        arr = CATEGORIAS_SISTEMA.get(categoria, [])
        return [item for item in arr if not isinstance(item, list)]

    def obtener_subsubcategorias(self, categoria, subcategoria):
        """
        Obtiene las sub-subcategorías para una combinación de categoría
        y subcategoría.

        Args:
            categoria (str): Categoría seleccionada.
            subcategoria (str): Subcategoría seleccionada.
            
        Returns:
            list: Lista de sub-subcategorías.
        """
        arr = CATEGORIAS_SISTEMA.get(categoria, [])
        for i in range(len(arr)):
            if (
                arr[i] == subcategoria and
                i + 1 < len(arr) and
                isinstance(arr[i + 1], list)
            ):
                return arr[i + 1]
        return []

    def controlar_evento_categoria(self, combo_categoria, combo_subcategoria,
                                   combo_subsubcategoria,
                                   entrada_vencimiento, entrada_pago):
        categoria_seleccionada = combo_categoria.get()
        subcats = self.obtener_subcategorias(categoria_seleccionada)
        if subcats:
            combo_subcategoria.config(values=subcats, state="readonly")
            combo_subcategoria.current(0)

            subsubcats = self.obtener_subsubcategorias(
                categoria_seleccionada, subcats[0])
            if subsubcats:
                combo_subsubcategoria.config(values=subsubcats, 
                                             state="readonly")
                combo_subsubcategoria.current(0)
            else:
                combo_subsubcategoria.set("No aplica")
                combo_subsubcategoria.config(state="disabled")
        else:
            combo_subcategoria.set("")
            combo_subcategoria.config(values=[], state="disabled")
            combo_subsubcategoria.set("No aplica")
            combo_subsubcategoria.config(state="disabled")

        if categoria_seleccionada == "Servicios":
            entrada_vencimiento.config(state="normal")
            entrada_pago.config(state="normal")
        else:
            entrada_vencimiento.delete(0, 'end')
            entrada_pago.delete(0, 'end')
            entrada_vencimiento.config(state="disabled")
            entrada_pago.config(state="disabled")

    def controlar_evento_subcategoria(self, combo_categoria, 
                                      combo_subcategoria,
                                      combo_subsubcategoria,
                                      entrada_vencimiento, entrada_pago):
        categoria_val = combo_categoria.get()
        subcategoria_val = combo_subcategoria.get()

        subsubcats = self.obtener_subsubcategorias(
            categoria_val, subcategoria_val)
        if subsubcats:
            combo_subsubcategoria.config(values=subsubcats, state="readonly")
            combo_subsubcategoria.current(0)
        else:
            combo_subsubcategoria.set("No aplica")
            combo_subsubcategoria.config(state="disabled")

    @registro_log # Modifico primer método
    def procesar_ingreso(self, usuario, contraseña):
        """
        Procesa el ingreso del usuario comprobando validación y 
        existencia en base de datos.

        Args:
            usuario (str): Nombre de usuario ingresado.
            contraseña (str): Contraseña ingresada.

        Ejemplo:
        >>> app = AppGestion()
        >>> app.procesar_ingreso("mara123", "HOGAR")
        (procesa login según lógica interna)
         """
        from modelo_usuario import Usuario
        user = Usuario(usuario, contraseña)
        if user.validar():
            if user.existe_en_bd():
                self.login_correcto()
            else:
                messagebox.showerror("Error", "Usuario no registrado.")

    def procesar_registro(self, usuario, contraseña):
        from modelo_usuario import Usuario
        user = Usuario(usuario, contraseña)
        user.registrar()

    @registro_log
    def guardar_movimiento(self, datos):
        mov = self._crear_movimiento_con_observador(datos)
        if mov.guardar():
            self.ventana_principal._limpiar_formulario()
            self.ventana_principal.refrescar_tabla()  
            """
            Refresca la tabla después de guardar
            """

    @registro_log
    def eliminar_movimiento(self, id_mov):
        mov = Movimiento("", "", "", "")
        mov.agregar_observador(self.logger_observador)
        mov.eliminar(id_mov)
        self.ventana_principal.refrescar_tabla()


    @registro_log
    def modificar_importe(self, id_mov, nuevo_importe):
        mov = Movimiento("", "", "", "")
        mov.agregar_observador(self.logger_observador)
        importe_clean = str(nuevo_importe).replace(".", "").replace(",", ".")
        if not mov.validar_importe():
            messagebox.showerror("Error", "Formato de importe inválido.")
            return
        mov.actualizar_importe(id_mov, float(importe_clean))
        self.ventana_principal.refrescar_tabla()


    def obtener_lista_movimientos(self):
        from movimiento import Movimiento
        return Movimiento("", "", "", "").obtener_todos()

    # Funciones auxiliares para la interfaz

    def autoformatear_fecha_entry(self, event, entrada):
        """
        Autoformatea
        
        Ejemplo:
            >>> # Al teclear en la entrada, se insertan automáticamente
            los '/' en posiciones correctas.
        """
        if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Tab"):
            return
        texto = entrada.get().strip()
        largo = len(texto)
        if largo > 0 and not texto[-1].isdigit() and texto[-1] != "/":
            entrada.delete(largo - 1, tk.END)
            return
        if largo == 2 and "/" not in texto:
            entrada.insert(tk.END, "/")
        elif largo == 5 and texto.count("/") == 1:
            entrada.insert(tk.END, "/")
        elif largo > 10:
            entrada.delete(10, tk.END)

    def refrescar_tabla_interfaz(self, combo_filtro_propiedad, tabla,
                                 etiqueta_balance, etiqueta_gasto):
        """
        Refresca la tabla de movimientos .

        Args:
            combo_filtro_propiedad (ttk.Combobox): Combo para filtrar por propiedad.
            tabla (ttk.Treeview): Tabla donde se muestran los movimientos.
            etiqueta_balance (tk.Label): Etiqueta para mostrar total acumulado.
            etiqueta_gasto (tk.Label): Etiqueta para mostrar gasto mensual.

        Returns:
            None

        """
        
        
        lista_movs = self.obtener_lista_movimientos()
        filtro = combo_filtro_propiedad.get()
        tabla.delete(*tabla.get_children())
        total = 0
        gasto_mes = 0
        mes_actual = datetime.now().month
        for movimiento in lista_movs:
            if filtro != "TODAS" and movimiento[1] != filtro:
                continue
            tabla.insert("", "end", values=movimiento)
            total += movimiento[4]
            try:
                f_pago_obj = datetime.strptime(movimiento[6], "%d/%m/%Y")
                if f_pago_obj.month == mes_actual:
                    gasto_mes += movimiento[4]
            except Exception:
                pass
        etiqueta_balance.config(text=f"Total Acumulado: $ {total:,.2f}")
        etiqueta_gasto.config(text=f"Gasto Mes Actual: $ {gasto_mes:,.2f}")

    def ejecutar_limpieza_formulario(self, combo_propiedad, combo_categoria, 
                                     combo_subcategoria,
                                     combo_subsubcategoria, entrada_importe,
                                     entrada_vencimiento, entrada_pago, 
                                     entrada_comentarios):
        combo_propiedad.current(0)
        combo_categoria.current(0)
        self.controlar_evento_categoria(combo_categoria, combo_subcategoria,
                                        combo_subsubcategoria,
                                        entrada_vencimiento, entrada_pago)
        combo_subsubcategoria.set("No aplica")
        combo_subsubcategoria.config(state="disabled")
        entrada_importe.delete(0, tk.END)
        entrada_vencimiento.delete(0, tk.END)
        entrada_vencimiento.config(state="disabled")
        entrada_pago.delete(0, tk.END)
        entrada_pago.config(state="disabled")
        entrada_comentarios.delete("1.0", tk.END)

    def ejecutar_guardado_seguro(self, combo_propiedad, combo_categoria, 
                                 combo_subcategoria,
                                 combo_subsubcategoria, entrada_importe,
                                 entrada_vencimiento, entrada_pago, 
                                 entrada_comentarios,
                                 combo_filtro_propiedad, tabla, 
                                 etiqueta_balance, etiqueta_gasto):
        """
        Recopila datos desde la interfaz y 
        guarda un nuevo movimiento de forma segura, 
        refrescando la tabla y totales

        Args:
            combo_propiedad (ttk.Combobox): Campo propiedad.
            combo_categoria (ttk.Combobox): Campo categoría.
            combo_subcategoria (ttk.Combobox): Campo subcategoría.
            combo_subsubcategoria (ttk.Combobox): Campo sub-subcategoría.
            entrada_importe (tk.Entry): Campo importe.
            entrada_vencimiento (tk.Entry): Campo fecha vencimiento.
            entrada_pago (tk.Entry): Campo fecha pago
            entrada_comentarios (tk.Text): Campo comentarios.
            combo_filtro_propiedad (ttk.Combobox): 
            Combo de filtro para refrescar tabla.
            tabla (ttk.Treeview): Tabla de movimientos.
            etiqueta_balance (tk.Label): Etiqueta de total acumulado.
            etiqueta_gasto (tk.Label): Etiqueta de gasto mensual.

        Ejemplo:
            >>> app.ejecutar_guardado_seguro(combo_propiedad, combo_categoria,
            combo_subcategoria, combo_subsubcategoria, entrada_importe,
            entrada_vencimiento, entrada_pago, entrada_comentarios
            combo_filtro_propiedad, tabla, etiqueta_balance, etiqueta_gasto)
        """
        datos = (
            combo_propiedad.get(),
            combo_categoria.get(),
            combo_subsubcategoria.get()
            if combo_subsubcategoria['state'] == "readonly"
            else combo_subcategoria.get(),
            entrada_importe.get(),
            entrada_vencimiento.get(),
            entrada_pago.get(),
            entrada_comentarios.get("1.0", tk.END).strip()
        )
        self.guardar_movimiento(datos)
        self.refrescar_tabla_interfaz(combo_filtro_propiedad, tabla, 
                                      etiqueta_balance, etiqueta_gasto)

    def ejecutar_eliminacion_seguro(self, tabla, combo_filtro_propiedad, 
                                    etiqueta_balance, etiqueta_gasto):
        """
        Elimina un movimiento seleccionado tras confirmar 
        con el usuario y refresca la tabla.

        Args:
            tabla (ttk.Treeview): Tabla donde se selecciona el movimiento.
            combo_filtro_propiedad (ttk.Combobox): 
            Combo filtro para refrescar tabla.
            etiqueta_balance (tk.Label): Etiqueta de total acumulado.
            etiqueta_gasto (tk.Label): Etiqueta de gasto mensual

        Ejemplo:
            >>> app.ejecutar_eliminacion_seguro
            (tabla, combo_filtro, label_balance, label_gasto)
        """
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", 
                                   "Seleccione un movimiento para eliminar.")
            return
        confirmado = messagebox.askyesno(
            "Confirmar", 
            "¿Está seguro que desea eliminar el movimiento seleccionado?")
        if confirmado:
            id_mov = tabla.item(seleccion[0])["values"][0]
            self.eliminar_movimiento(id_mov)
            self.refrescar_tabla_interfaz(combo_filtro_propiedad, tabla, 
                                          etiqueta_balance, etiqueta_gasto)

    def ejecutar_modificacion_importe_seguro(
        self, tabla, entrada_importe,
        combo_filtro_propiedad, etiqueta_balance,
        etiqueta_gasto, combo_propiedad, combo_categoria,
        combo_subcategoria, combo_subsubcategoria,
        entrada_vencimiento, entrada_pago
    ):
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia", "Seleccione un movimiento para modificar."
            )
            return

        nuevo_importe = entrada_importe.get().strip()
        if not nuevo_importe:
            messagebox.showerror("Error", "Debe ingresar un nuevo importe.")
            return

        import re
        patron_importe = re.compile(r"^\d{1,3}(\.\d{3})*([.,]\d{1,2})?$")
        if not patron_importe.match(nuevo_importe):
            messagebox.showerror("Error", "Formato de importe inválido.")
            return

        id_mov = tabla.item(seleccion[0])["values"][0]

        confirmado = messagebox.askyesno(
        "Confirmar Edición",
        f"¿Cambiar el importe del ID {id_mov} a $ {nuevo_importe}?"
        )
        if not confirmado:
            return

        try:
            importe_limpio = nuevo_importe.replace(".", "").replace(",", ".")
            nuevo_importe_num = float(importe_limpio)
        except ValueError:
            messagebox.showerror(
            "Error", "No se pudo convertir el importe a número válido."
            )
            return

        try:
            from movimiento import Movimiento
            mov = Movimiento("", "", "", "")
            mov.actualizar_importe(id_mov, nuevo_importe_num)
            messagebox.showinfo("Éxito", "Importe modificado correctamente.")
            entrada_importe.delete(0, "end")
            self.ventana_principal.refrescar_tabla()
        except Exception as e:
            messagebox.showerror(
                "Error BD", f"No se pudo modificar el importe: {e}"
            )

    
    def ejecutar_cerrar_sesion(self, ventana):
        confirmado = messagebox.askyesno(
            "Confirmar", "¿Está seguro que desea cerrar sesión?")
        if confirmado:
            ventana.destroy()
            self.cerrar_sesion()


if __name__ == "__main__":
    app = AppGestion()
    app.iniciar()
