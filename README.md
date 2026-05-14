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
