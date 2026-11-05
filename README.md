# Proyecto Gestión Hogar

El proyecto funciona como un panel administrativo mediante una **aplicación de escritorio**.
El código está estructurado siguiendo el patrón de diseño **Modelo-Vista-Controlador (MVC)**:

* **Modelo:** Gestiona la persistencia de datos utilizando **SQLite3**.
* **Controlador:** Centraliza las validaciones de negocio, incluyendo expresiones regulares para importes y fechas.
* **Vista:** Interfaz gráfica de usuario construida con **Tkinter**.
* **Registro de Logs:** Implementa decorador y patrón observador para trazabilidad de acciones.
* **Servidor y Cliente:** Implementa un servidor TCP para recepción centralizada de logs y cliente que envía registros remotos.

---

## 📁 Estructura del Proyecto

Organización principal de los directorios y archivos del sistema:

```text
proyecto_gestion_hogar/
├── docs/               # Documentación técnica generada con Sphinx
├── src/                # Código fuente de la aplicación (MVC y utilidades)
│   ├── db_manager.py       # Modelo: Conexión y gestión de la base de datos SQLite3
│   ├── movimiento.py       # Modelo: Lógica y estructura de movimientos financieros
│   ├── modelo_usuario.py   # Modelo: Gestión y validación de usuarios
│   ├── vista_login.py      # Vista: Interfaz para inicio de sesión (Tkinter)
│   ├── vista_principal.py  # Vista: Panel principal e interfaz (Tkinter)
│   ├── app_gestion2.py     # Controlador: Lógica principal y orquestación
│   ├── logger_decorator.py # Decorador para registro local y remoto de logs
│   ├── observador.py       # Implementación del patrón observador para logs
│   ├── servidor_logs.py    # Servidor TCP multi-hilo para registro centralizado
│   ├── cliente_logs.py     # Cliente para envío de logs al servidor remoto
│   └── ...                 # Otros archivos de utilidad o configuración
├── venv/               # Entorno virtual Python (no versionado)
├── README.md           # Documentación general y guía rápida
├── requirements.txt    # Dependencias Python del proyecto
└── registro_operaciones.txt # Logs locales generados por el decorador (no versionado)
```

---

## 🛠️ Requisitos

Antes de comenzar, asegurar  tener instalado lo siguiente:
* **Python 3.8** o superior
* **pip** (administrador de paquetes de Python)
* **Entorno virtual Python** recomendado para aislar dependencias

---

## 📦 Instalación y Configuración

Sigue estos pasos en tu terminal para configurar el entorno localmente:

1. **Clona el repositorio:**
   ```
   git clone https://github.com/mara4ccodigo/proyecto_gestion_hogar.git
   cd proyecto_gestion_hogar
   ```

2. **Crea y activa el entorno virtual (venv):**
   * En Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * En macOS / Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. **Instala las dependencias necesarias:**
   Instalar los paquetes requeridos, registrados en el archivo de configuración:
   ```
   pip install -r requirements.txt
   ```

---

## 🚀 Ejecución

Para iniciar la aplicación de escritorio, ejecuta el archivo principal desde la raíz con el entorno virtual activo:
```
python src/app_gestion2.py
```

Para levantar el servidor TCP que recibe los logs remotos
```
python src/servidor_logs.py
```

---

## 📖 Documentación (Sphinx)

El proyecto cuenta con documentación técnica automatizada utilizando **Sphinx**. Para generarla y visualizarla localmente:

1. Ingresa al directorio de documentación:
   ```
   cd docs
   ```
2. Genera los archivos HTML de la documentación:
   * En Windows:
     ```
     .\make.bat html
     ```
   * En macOS / Linux:
     ```
     make html
     ```
3. Abre el archivo generado `docs/_build/html/index.html` en cualquier navegador web para consultar la guía técnica.

## 🔍 Registro de Logs

El sistema genera registros de las operaciones clave a nivel local y los envía a un servidor central por TCP.

* Se usa un decorador para capturar llamadas a funciones importantes.
* Se aplica el patrón observador para notificar eventos de forma desacoplada.
* Logs locales se guardan en registro_operaciones.txt.
* Logs remotos se reciben en log_servidor_remoto.txt gestionado por servidor_logs.py.
* Para enviar logs remotos se usa el cliente cliente_logs.py.

## 🧪 Pruebas (Tests)
Actualmente en planificación. Se realizarán con la librería nativa unittest de Python y otros frameworks compatibles.

---

## 👩‍💻 Autor
Mara D. Leveroni C.
Curso Python Avanzado - UTN - 2026


