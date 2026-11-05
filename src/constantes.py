#=============================================================================
# Autor/a: Mara D. Leveroni C.
# Fecha: 28/08/2026
# Archivo: constantes.py
# Descripción:
#   Módulo que contiene constantes globales y patrones de validación
#   usados en múltiples módulos para evitar importaciones circulares
#   y centralizar la configuración del proyecto.
#=============================================================================

import re


CONTRASENIA_SISTEMA = "HOGAR" 
"""
Contraseña fija, momentanea.
"""

# Patrón regex para validar usuarios: 4-10 caracteres alfanuméricos
PATRON_USUARIO = re.compile(r"^[a-zA-Z0-9]{4,10}$")

# Patrón regex para validar formato de importes monetarios
PATRON_IMPORTE = re.compile(r"^\d{1,3}(\.\d{3})*([.,]\d{1,2})?$")

# Patrón regex para validar fechas dd/mm/aa(aa)
PATRON_FECHA = re.compile(r"^\d{2}/\d{2}/(\d{2}|\d{4})$")

