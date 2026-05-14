se debe de tener el python 3.10 instalar streamlit y librerias como pandas reportlab etc 

# Devimulator – Simulación Monte Carlo para Evaluación de Proyectos de Inversión

Devimulator es una aplicación desarrollada en Python que permite realizar simulaciones Monte Carlo para evaluar proyectos de inversión bajo condiciones de riesgo e incertidumbre financiera.

El sistema calcula indicadores financieros como:

- VAN (Valor Actual Neto)
- TIR (Tasa Interna de Retorno)
- Flujos de caja simulados
- Escenarios optimistas y pesimistas
- Validación estadística de variables aleatorias

Además, el proyecto incluye:

- Generación automática de reportes PDF
- Visualización interactiva mediante Streamlit
- Almacenamiento de resultados en SQL Server
- Gráficas y análisis estadístico

---

# Tecnologías utilizadas

- Python 3.10
- Streamlit
- Pandas
- NumPy
- Matplotlib
- ReportLab
- PyODBC
- SQL Server

---

# Estructura del proyecto

```bash
TeoriaSimulacion/
│
├── assets/
├── reports/
├── simulador/
│   ├── datos.py
│   ├── escenarios.py
│   ├── finanzas.py
│   ├── flujo_caja.py
│   ├── generadores.py
│   ├── main_engine.py
│   ├── pdf_report.py
│   ├── reportes.py
│   ├── simulacion.py
│   ├── validacion.py
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```
---

# ¿Cómo funciona el sistema?

El sistema utiliza simulación Monte Carlo para generar múltiples escenarios financieros posibles utilizando variables aleatorias.

Las variables principales son:

- Demanda del producto
- Precio de venta
- Costos variables
- Costos fijos

Cada simulación genera:

- Flujos de caja proyectados
- Cálculo del VAN
- Cálculo de la TIR
- Estadísticas generales

El sistema repite el proceso cientos o miles de veces para analizar el comportamiento financiero del proyecto bajo incertidumbre.

---

# Distribuciones utilizadas

## Demanda
Distribución uniforme.

## Precio de venta
Distribución normal.

## Costos variables
Distribución uniforme.

## Costos fijos
Distribución discreta.

---

# Funcionalidades principales

## Simulación Monte Carlo

Permite ejecutar cientos o miles de iteraciones para analizar el comportamiento del VAN del proyecto.

## Comparación de escenarios

Incluye:

- Escenario base
- Escenario optimista
- Escenario pesimista

## Validación estadística

Se aplican pruebas como:

- Chi-cuadrado
- Kolmogorov-Smirnov

para validar que las variables aleatorias cumplen con la distribución teórica esperada.

## Reportes PDF

El sistema genera automáticamente informes PDF con:

- Resumen estadístico
- Resultados del VAN
- Resultados de validación

## Base de datos SQL Server

Los resultados de las simulaciones son almacenados en SQL Server.

---

# Requisitos previos

Antes de ejecutar el proyecto debe tener instalado:

## 1. Python 3.10

Descargar desde:

https://www.python.org/downloads/release/python-3100/

Verificar instalación:

```bash
python --version
```

---

## 2. SQL Server

Debe tener instalado:

- SQL Server
- SQL Server Management Studio (SSMS)

Y crear una base de datos llamada:

```sql
DevimulatorDB
```

---

# Instalación del proyecto

## 1. Clonar el repositorio

```bash
git clone https://github.com/LitzyCastellanos/TeoriaSimulacion.git
```

## 2. Entrar al proyecto

```bash
cd TeoriaSimulacion
```

## 3. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
```

Activar entorno virtual:

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no funciona el requirements.txt instalar manualmente:

```bash
pip install streamlit pandas numpy matplotlib reportlab pyodbc scipy
```

---

# Configuración de SQL Server

En el archivo `app.py` modificar la conexión según su servidor:

```python
SERVER=KAREN-CASTELLAN\\SQLEXPRESS
DATABASE=DevimulatorDB
```

Cambiar el nombre del servidor si es necesario.

---

# Ejecución del proyecto

## Ejecutar interfaz Streamlit

```bash
streamlit run app.py
```

Luego abrir en el navegador:

```text
http://localhost:8501
```

---

# Ejecución de pruebas desde main.py

El archivo `main.py` permite ejecutar una simulación de prueba y generar automáticamente un PDF.

Ejecutar:

```bash
python main.py
```

El sistema:

- Ejecutará la simulación
- Generará VANs
- Mostrará estadísticas
- Creará un PDF automáticamente

---

# Módulos principales

## main_engine.py

Motor principal de simulación.

## pdf_report.py

Generación de reportes PDF.

## validacion.py

Pruebas estadísticas para validación de distribuciones.

## generadores.py

Generación de números aleatorios.

## flujo_caja.py

Cálculo de flujos de caja.

## finanzas.py

Cálculo financiero de VAN y TIR.

---

# Autora

**Litzy Castellanos**  
Estudiante de Ingeniería en Sistemas  
Universidad Nacional Autónoma de Honduras (UNAH)
