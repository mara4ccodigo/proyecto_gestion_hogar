#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha: 26/08/2026
# Archivo: vista_principal.py
# Descripción:
#   Ventana principal de la aplicación de Gestión.
#   Presenta formulario para ingresar movimientos, tabla para histórico,
#   filtros, y botones para eliminar/modificar movimientos.
#   Se implementan validaciones y llamadas al controlador para operaciones.
#=============================================================================

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class VentanaPrincipal(tk.Tk):
    """
    Ventana principal de la aplicación de gestión.

    Presenta formulario para ingreso de movimientos, tabla histórica,
    filtros y botones para eliminar o modificar movimientos.
    """
    def __init__(self, controlapp=None):
        """
        Inicializa la ventana principal.

        Args:
            controlapp (AppGestion, optional): Controlador principal.
        """
        super().__init__()
        self.controlapp = controlapp
        self.title("Sistema de Gestión de Importes - Hogar")
        self.geometry("830x710")
        self._crear_widgets()

    def _crear_widgets(self):
        """
        Crea los widgets, combos, tabla, botones y bindings de la interfaz.
        """
        frame_form = tk.LabelFrame(self, text=" Registrar Movimiento ")
        frame_form.pack(fill="x", padx=15, pady=10, ipady=5)

        # Propiedad
        tk.Label(frame_form, text="Propiedad:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.combo_propiedad = ttk.Combobox(
            frame_form,
            values=self.controlapp.obtener_propiedades(),
            state="readonly",
            width=18,
        )
        self.combo_propiedad.grid(row=0, column=1, padx=5, pady=5)
        self.combo_propiedad.current(0)

        # Categoría
        tk.Label(frame_form, text="Categoría:").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        self.combo_categoria = ttk.Combobox(
            frame_form,
            values=self.controlapp.obtener_categorias(),
            state="readonly",
            width=18,
        )
        self.combo_categoria.grid(row=0, column=3, padx=5, pady=5)
        self.combo_categoria.current(0)

        # Subcategoría
        tk.Label(frame_form, text="Subcategoría:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.combo_subcategoria = ttk.Combobox(
            frame_form, state="readonly", width=18
        )
        self.combo_subcategoria.grid(row=1, column=1, padx=5, pady=5)

        # Sub-subcategoría
        tk.Label(frame_form, text="Sub-Subcategoría:").grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )
        self.combo_subsubcategoria = ttk.Combobox(
            frame_form, state="disabled", width=18
        )
        self.combo_subsubcategoria.grid(row=1, column=3, padx=5, pady=5)
        self.combo_subsubcategoria.set("No aplica")

        # Importe
        tk.Label(frame_form, text="Importe ($):").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.entrada_importe = tk.Entry(frame_form, width=20)
        self.entrada_importe.grid(row=2, column=1, padx=5, pady=5)

        # Fecha vencimiento
        tk.Label(frame_form, text="F. Vencimiento:").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        self.entrada_vencimiento = tk.Entry(frame_form, width=20)
        self.entrada_vencimiento.grid(row=3, column=1, padx=5, pady=5)
        self.entrada_vencimiento.bind(
            "<KeyRelease>",
            lambda e: self.controlapp.autoformatear_fecha_entry(
                e, self.entrada_vencimiento
            ),
        )

        # Fecha pago
        tk.Label(frame_form, text="F. Pago:").grid(
            row=3, column=2, sticky="w", padx=5, pady=5
        )
        self.entrada_pago = tk.Entry(frame_form, width=20)
        self.entrada_pago.grid(row=3, column=3, padx=5, pady=5)
        self.entrada_pago.bind(
            "<KeyRelease>", lambda e: self.controlapp.autoformatear_fecha_entry(e, self.entrada_pago)
        )

        # Comentarios
        tk.Label(frame_form, text="Comentarios:").grid(
            row=4, column=0, sticky="nw", padx=5, pady=5
        )
        self.entrada_comentarios = tk.Text(frame_form, width=50, height=4)
        self.entrada_comentarios.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

        # Botones: Limpiar y Guardar
        btn_limpiar = tk.Button(
            frame_form,
            text="Limpiar Campos",
            bg="#f5f5f5",
            width=14,
            command=lambda: self.controlapp.ejecutar_limpieza_formulario(
                self.combo_propiedad,
                self.combo_categoria,
                self.combo_subcategoria,
                self.combo_subsubcategoria,
                self.entrada_importe,
                self.entrada_vencimiento,
                self.entrada_pago,
                self.entrada_comentarios,
            ),
        )
        btn_limpiar.grid(row=2, column=4, padx=5, pady=5)

        btn_guardar = tk.Button(
            frame_form,
            text="Guardar Registro",
            bg="#e1e1e1",
            width=14,
            command=lambda: self.controlapp.ejecutar_guardado_seguro(
                self.combo_propiedad,
                self.combo_categoria,
                self.combo_subcategoria,
                self.combo_subsubcategoria,
                self.entrada_importe,
                self.entrada_vencimiento,
                self.entrada_pago,
                self.entrada_comentarios,
                self.combo_filtro_propiedad,
                self.tabla_movimientos,
                self.etiqueta_balance_total,
                self.etiqueta_gasto_mensual,
            ),
        )
        btn_guardar.grid(row=3, column=4, padx=5, pady=5)

        # Filtro por propiedad
        frame_filtros = tk.Frame(self)
        frame_filtros.pack(fill="x", padx=15, pady=5)

        tk.Label(
            frame_filtros, text="Filtrar por Propiedad:", font=("Arial", 10, "bold")
        ).pack(side="left", padx=5)

        self.combo_filtro_propiedad = ttk.Combobox(
            frame_filtros,
            values=["TODAS"] + self.controlapp.obtener_propiedades()[1:],
            state="readonly",
            width=20,
        )
        self.combo_filtro_propiedad.pack(side="left", padx=5)
        self.combo_filtro_propiedad.current(0)

        # Tabla de movimientos
        frame_tabla = tk.LabelFrame(self, text=" Historial ")
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        columnas = (
            "id",
            "propiedad",
            "categoria",
            "subcategoria",
            "importe",
            "vencimiento",
            "pago",
            "comentarios",
        )
        self.tabla_movimientos = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        for col in columnas:
            self.tabla_movimientos.heading(col, text=col.capitalize())
        self.tabla_movimientos.column("id", width=40, anchor="center")
        self.tabla_movimientos.column("propiedad", width=140)
        self.tabla_movimientos.column("categoria", width=130)
        self.tabla_movimientos.column("subcategoria", width=120)
        self.tabla_movimientos.column("importe", width=90, anchor="e")
        self.tabla_movimientos.column("vencimiento", width=120, anchor="center")
        self.tabla_movimientos.column("pago", width=120, anchor="center")
        self.tabla_movimientos.column("comentarios", width=200, anchor="w")
        self.tabla_movimientos.pack(fill="both", expand=True, padx=5, pady=5)

        # Botones de acciones: eliminar, modificar, logout
        frame_acciones = tk.Frame(self)
        frame_acciones.pack(fill="x", padx=15, pady=10)

        btn_eliminar = tk.Button(
            frame_acciones,
            text="Eliminar Seleccionado",
            bg="#ffcccc",
            fg="#cc0000",
            command=lambda: self.controlapp.ejecutar_eliminacion_seguro(
                self.tabla_movimientos,
                self.combo_filtro_propiedad,
                self.etiqueta_balance_total,
                self.etiqueta_gasto_mensual,
            ),
        )
        btn_eliminar.pack(side="left", padx=5, pady=5)

        btn_modificar = tk.Button(
            frame_acciones,
            text="Modificar Importe",
            command=lambda: (
                self.cargar_datos_seleccionados_en_formulario() and
                self.controlapp.ejecutar_modificacion_importe_seguro(
                    self.tabla_movimientos,
                    self.entrada_importe,
                    self.combo_filtro_propiedad,
                    self.etiqueta_balance_total,
                    self.etiqueta_gasto_mensual,
                    self.combo_propiedad,
                    self.combo_categoria,
                    self.combo_subcategoria,
                    self.combo_subsubcategoria,
                    self.entrada_vencimiento,
                    self.entrada_pago,
                )
            ),
        )


        btn_modificar.pack(side="left", padx=5, pady=5)

        btn_logout = tk.Button(
            frame_acciones,
            text="Cerrar Sesión",
            bg="#e1e1e1",
            command=lambda: self.controlapp.ejecutar_cerrar_sesion(self),
        )
        btn_logout.pack(side="left", padx=5, pady=5)

        self.etiqueta_balance_total = tk.Label(
            frame_acciones, text="Total Acumulado: $ 0.00", font=("Arial", 11, "bold")
        )
        self.etiqueta_balance_total.pack(side="right", pady=5)

        self.etiqueta_gasto_mensual = tk.Label(
            self,
            text="Gasto Mes Actual: $ 0.00",
            font=("Arial", 11, "bold"),
            fg="#1e293b",
            anchor="e",
        )
        self.etiqueta_gasto_mensual.pack(fill="x", padx=20, pady=(0, 10))

        # Bindings para actualización en cascada y refresco de tabla
        self.combo_categoria.bind(
            "<<ComboboxSelected>>",
            lambda e: [
                self.controlapp.controlar_evento_categoria(
                    self.combo_categoria,
                    self.combo_subcategoria,
                    self.combo_subsubcategoria,
                    self.entrada_vencimiento,
                    self.entrada_pago,
                ),
                self.combo_subsubcategoria.set("No aplica"),
                self.combo_subsubcategoria.configure(state="disabled"),
            ],
        )

        self.combo_subcategoria.bind(
            "<<ComboboxSelected>>",
            lambda e: self.controlapp.controlar_evento_subcategoria(
                self.combo_categoria,
                self.combo_subcategoria,
                self.combo_subsubcategoria,
                self.entrada_vencimiento,
                self.entrada_pago,
            ),
        )

        self.combo_filtro_propiedad.bind(
            "<<ComboboxSelected>>",
            lambda e: self.controlapp.refrescar_tabla_interfaz(
                self.combo_filtro_propiedad,
                self.tabla_movimientos,
                self.etiqueta_balance_total,
                self.etiqueta_gasto_mensual,
            ),
        )

        # Inicializar combos y tabla al cargar la ventana
        self.controlapp.controlar_evento_categoria(
            self.combo_categoria,
            self.combo_subcategoria,
            self.combo_subsubcategoria,
            self.entrada_vencimiento,
            self.entrada_pago,
        )
        self.controlapp.refrescar_tabla_interfaz(
            self.combo_filtro_propiedad,
            self.tabla_movimientos,
            self.etiqueta_balance_total,
            self.etiqueta_gasto_mensual,
        )

    def refrescar_tabla(self):
        """
        Refresca la tabla de movimientos con los datos más actuales.
        """
        self.controlapp.refrescar_tabla_interfaz(
            self.combo_filtro_propiedad,
            self.tabla_movimientos,
            self.etiqueta_balance_total,
            self.etiqueta_gasto_mensual,
        )
    # Se modifica 
    def cargar_importe_seleccionado_en_campo(self):
        """
        Carga el valor de importe del movimiento seleccionado en el campo
        de entrada de importe para facilitar su edición.

        Returns:
            bool: True si se pudo cargar importe, False si no hay selección.
        """
        seleccion = self.tabla_movimientos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un movimiento para modificar.")
            return False
        item = self.tabla_movimientos.item(seleccion[0])
        importe_actual = item['values'][4]  # columna importe en la tabla
        self.entrada_importe.delete(0, tk.END)
        self.entrada_importe.insert(0, f"{importe_actual:,.2f}")
        return True

    def _limpiar_formulario(self):
        """
        Limpia todos los campos del formulario para un nuevo ingreso.
        """
        self.controlapp.ejecutar_limpieza_formulario(
            self.combo_propiedad,
            self.combo_categoria,
            self.combo_subcategoria,
            self.combo_subsubcategoria,
            self.entrada_importe,
            self.entrada_vencimiento,
            self.entrada_pago,
            self.entrada_comentarios,
        )

    def cargar_datos_seleccionados_en_formulario(self):
        """
        Carga todos los datos del movimiento seleccionado en el formulario.

        Retorna:
            bool: True si se cargaron correctamente, False si no hay selección.
        """
        seleccion = self.tabla_movimientos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un movimiento para modificar.")
            return False
        item = self.tabla_movimientos.item(seleccion[0])
        valores = item['values']

        # Propiedad
        propiedad = valores[1]
        opciones_prop = list(self.combo_propiedad['values'])
        if propiedad not in opciones_prop:
            opciones_prop.append(propiedad)
            self.combo_propiedad.config(values=opciones_prop)
        self.combo_propiedad.set(propiedad)

        # Categoría
        categoria = valores[2]
        opciones_cat = list(self.combo_categoria['values'])
        if categoria not in opciones_cat:
            opciones_cat.append(categoria)
            self.combo_categoria.config(values=opciones_cat)
        self.combo_categoria.set(categoria)

        # Subcategoría
        subcategoria = valores[3]
        opciones_subcat = list(self.combo_subcategoria['values'])
        if subcategoria not in opciones_subcat:
            opciones_subcat.append(subcategoria)
            self.combo_subcategoria.config(values=opciones_subcat)
        self.combo_subcategoria.set(subcategoria)

        # Importe (sin formato para evitar errores en validación)
        self.entrada_importe.delete(0, tk.END)
        importe_limpio = str(valores[4]).replace(".", "").replace(",", ".")
        self.entrada_importe.insert(0, importe_limpio)

        # Fecha Vencimiento
        self.entrada_vencimiento.delete(0, tk.END)
        self.entrada_vencimiento.insert(0, valores[5] if valores[5] else "")

        # Fecha Pago
        self.entrada_pago.delete(0, tk.END)
        self.entrada_pago.insert(0, valores[6] if valores[6] else "")

        # Comentarios
        self.entrada_comentarios.delete("1.0", tk.END)
        self.entrada_comentarios.insert(tk.END, valores[7] if valores[7] else "")

        return True


