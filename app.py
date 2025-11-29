# app.py – Devimulator con VAN, TIR, flujos y guardado en SQL Server

import os
import io
import copy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pyodbc

from simulador.main_engine import ejecutar_simulacion, generar_reporte
from simulador.reportes import tabla_frecuencias
from simulador.validacion import validar_aleatorios
from simulador.generadores import generar_uniforme, generar_normal, generar_discreta


# =========================================================
#   CONEXIÓN A SQL SERVER
# =========================================================

def conectar():
    """Devuelve una conexión a SQL Server."""
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=KAREN-CASTELLAN\\SQLEXPRESS;'
        'DATABASE=DevimulatorDB;'
        'Trusted_Connection=yes;'
    )


# =========================================================
#   FUNCIONES PARA GUARDAR EN BD
# =========================================================

def guardar_parametros(params: dict, iteraciones: int) -> int:
    """
    Inserta los parámetros de simulación y devuelve el id (simulacion_id).
    Debe existir la tabla ParametrosSimulacion en DevimulatorDB.
    """
    conn = conectar()
    cur = conn.cursor()

    query = """
    INSERT INTO ParametrosSimulacion
    (demanda_min, demanda_max, precio_mu, precio_sigma,
     cv_min, cv_max, cf_28k_prob, cf_30k_prob, cf_32k_prob,
     tasa_impuesto, tasa_descuento, vida, depreciacion, valor_desecho,
     inversion_inicial, iteraciones)
    OUTPUT INSERTED.id
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    simulacion_id = cur.execute(
        query,
        params["demanda_min"], params["demanda_max"],
        params["precio_mu"], params["precio_sigma"],
        params["cv_min"], params["cv_max"],
        params["cf_probs"][0], params["cf_probs"][1], params["cf_probs"][2],
        params["tasa_impuesto"], params["tasa_descuento"],
        params["vida"], params["depreciacion"], params["valor_desecho"],
        params["inversion_inicial"], iteraciones
    ).fetchone()[0]

    conn.commit()
    conn.close()
    return simulacion_id


def guardar_resumen_van(simulacion_id: int, resumen: dict) -> None:
    """Guarda el resumen estadístico del VAN en ResultadosVAN."""
    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO ResultadosVAN
        (simulacion_id, media, mediana, desviacion, minimo, maximo)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        simulacion_id,
        float(resumen["media"]),
        float(resumen["mediana"]),
        float(resumen["desviacion"]),
        float(resumen["minimo"]),
        float(resumen["maximo"]),
    )

    conn.commit()
    conn.close()


def guardar_iteraciones_van(simulacion_id: int, lista_van) -> None:
    """Guarda TODAS las iteraciones del VAN (una fila por simulación)."""
    conn = conectar()
    cur = conn.cursor()

    for v in lista_van:
        cur.execute(
            "INSERT INTO IteracionesVAN (simulacion_id, van) VALUES (?, ?)",
            simulacion_id,
            float(v),
        )

    conn.commit()
    conn.close()


def guardar_valores_aleatorios(simulacion_id: int,
                               dem, cv, prec, cf) -> None:
    """
    Guarda los valores aleatorios usados en la validación (opcional).
    Debe existir la tabla VariablesAleatorias.
    """
    conn = conectar()
    cur = conn.cursor()

    for i in range(len(dem)):
        cur.execute(
            """
            INSERT INTO VariablesAleatorias
            (simulacion_id, demanda, costo_variable, precio, costo_fijo)
            VALUES (?, ?, ?, ?, ?)
            """,
            simulacion_id,
            float(dem[i]),
            float(cv[i]),
            float(prec[i]),
            float(cf[i]),
        )

    conn.commit()
    conn.close()


def guardar_archivo(simulacion_id: int, tipo: str, ruta: str) -> None:
    """
    Registra en BD la ruta de un archivo generado (PDF, gráfica, etc.).
    Tabla: ArchivosGenerados.
    """
    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO ArchivosGenerados (simulacion_id, tipo, ruta)
        VALUES (?, ?, ?)
        """,
        simulacion_id, tipo, ruta
    )

    conn.commit()
    conn.close()


# =========================================================
#   ESTILO CORPORATIVO UNAH – STREAMLIT
# =========================================================

COLOR_PRIMARIO = "#002B5B"
COLOR_SECUNDARIO = "#F2A900"
COLOR_FONDO = "#FFFFFF"
COLOR_GRIS = "#F5F5F5"

st.set_page_config(
    page_title="Devimulator – Simulación de Proyectos de Inversión",
    layout="wide",
    page_icon="📘",
)

st.markdown(
    f"""
    <style>
    .main {{
        background-color: {COLOR_FONDO};
    }}
    .titulo-principal {{
        font-size: 30px;
        font-weight: 800;
        color: {COLOR_PRIMARIO};
    }}
    .subtitulo {{
        font-size: 17px;
        color: #444444;
        margin-bottom: 20px;
    }}
    .card {{
        background-color: {COLOR_GRIS};
        padding: 1rem 1.5rem;
        border-radius: 6px;
        border-left: 6px solid {COLOR_SECUNDARIO};
        margin-bottom: 1rem;
    }}
    .metric-box {{
        background-color: {COLOR_GRIS};
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #DDDDDD;
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
#   PARÁMETROS – ESCENARIO BASE
# =========================================================

parametros_base = {
    # Demanda anual (Uniforme)
    "demanda_min": 9061,
    "demanda_max": 11915,

    # Precio de venta (Normal)
    "precio_mu": 26.48,
    "precio_sigma": 0.83,

    # Costo variable unitario (Uniforme)
    "cv_min": 9.01,
    "cv_max": 10.71,

    # Costo fijo mensual (Discreta)
    "cf_valores": [28000, 30000, 32000],
    "cf_probs": [0.30, 0.3667, 0.3333],

    # Impuesto y descuento
    "tasa_impuesto": 0.10,
    "tasa_descuento": 0.20,

    # Horizonte del proyecto
    "vida": 10,

    # Depreciación anual
    "depreciacion": 14000,

    # Valor de desecho
    "valor_desecho": 524000,

    # Inversión inicial
    "inversion_inicial": -812500,
}


# =========================================================
#   ESCENARIOS (Optimista / Pesimista)
# =========================================================

def construir_escenario_A_optimista(base: dict) -> dict:
    esc = copy.deepcopy(base)
    esc["demanda_min"] = base["demanda_min"] * 1.10
    esc["demanda_max"] = base["demanda_max"] * 1.10
    esc["cv_min"] = base["cv_min"] * 0.90
    esc["cv_max"] = base["cv_max"] * 0.90
    esc["cf_valores"] = [v * 0.95 for v in base["cf_valores"]]
    return esc


def construir_escenario_B_pesimista(base: dict) -> dict:
    esc = copy.deepcopy(base)
    esc["demanda_min"] = base["demanda_min"] * 0.90
    esc["demanda_max"] = base["demanda_max"] * 0.90
    esc["cv_min"] = base["cv_min"] * 1.10
    esc["cv_max"] = base["cv_max"] * 1.10
    esc["cf_valores"] = [v * 1.05 for v in base["cf_valores"]]
    return esc


# =========================================================
#   INTERVALOS DE CONFIANZA
# =========================================================

def calcular_intervalos_confianza(media: float, sigma: float) -> dict:
    ic_68_inf = media - sigma
    ic_68_sup = media + sigma
    ic_95_inf = media - 1.96 * sigma
    ic_95_sup = media + 1.96 * sigma
    return {
        "68_inf": ic_68_inf,
        "68_sup": ic_68_sup,
        "95_inf": ic_95_inf,
        "95_sup": ic_95_sup,
    }


# =========================================================
#   GRÁFICAS
# =========================================================

def grafica_campana_normal(lista_van):
    """Devuelve una figura con histograma + curva normal teórica."""
    mu = np.mean(lista_van)
    sigma = np.std(lista_van)

    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 500)
    y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

    fig, ax = plt.subplots(figsize=(6, 3))

    ax.hist(lista_van, bins=30, density=True, alpha=0.4, label="Histograma del VAN")
    ax.plot(x, y, 'r-', linewidth=2, label="Curva Normal teórica")

    ax.axvline(mu, color='blue', linestyle='--', label="Media μ")
    ax.axvline(mu + sigma, color='green', linestyle='--', label="μ + σ")
    ax.axvline(mu - sigma, color='green', linestyle='--')
    ax.axvline(mu + 2 * sigma, color='purple', linestyle='--', label="μ + 2σ")
    ax.axvline(mu - 2 * sigma, color='purple', linestyle='--')

    ax.set_title("Distribución del VAN (Histograma + Curva Normal)")
    ax.set_xlabel("VAN")
    ax.set_ylabel("Densidad")
    ax.legend()

    return fig


def guardar_figura_temporal(fig, filename="grafica_van.png"):
    """Guarda una figura en PNG y devuelve la ruta."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=200)
    buf.seek(0)

    with open(filename, "wb") as f:
        f.write(buf.getbuffer())

    return filename


# =========================================================
#   SIDEBAR
# =========================================================

st.sidebar.image("assets/logo_unah.png", width=120)

opcion = st.sidebar.radio(
    "Seleccione una sección:",
    [
        "Descripción del modelo",
        "Simulación Monte Carlo",
        "Comparación de escenarios",
        "Validación estadística",
        "Informe PDF",
    ],
)

iteraciones_sidebar = st.sidebar.slider(
    "Número de iteraciones de la simulación",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100,
)

# CABECERA PRINCIPAL
st.markdown(
    """
    <div class="titulo-principal">
        Devimulator – Sistema de Simulación de Proyectos de Inversión
    </div>
    <div class="subtitulo">
        Herramienta académica para evaluar proyectos bajo riesgo e incertidumbre
        mediante simulación Monte Carlo.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
#   1. DESCRIPCIÓN DEL MODELO
# =========================================================

if opcion == "Descripción del modelo":
    st.markdown("## Estructura general del modelo de simulación")

    col1, col2 = st.columns([1.2, 1.0])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Variables aleatorias del modelo")

        st.markdown("**Demanda (unidades) – Distribución uniforme**")
        st.write(
            f"- Rango: {parametros_base['demanda_min']:,} a {parametros_base['demanda_max']:,}\n"
            f"- Fórmula generadora: demanda = a + R · (b − a)"
        )

        st.markdown("**Precio de venta – Distribución normal**")
        st.write(
            f"- Media μ = {parametros_base['precio_mu']:.2f}\n"
            f"- Desviación estándar σ = {parametros_base['precio_sigma']:.2f}"
        )

        st.markdown("**Costo variable unitario – Distribución uniforme**")
        st.write(
            f"- Rango: {parametros_base['cv_min']:.2f} a {parametros_base['cv_max']:.2f}"
        )

        st.markdown("**Costo fijo mensual – Distribución discreta**")
        cf_df = pd.DataFrame(
            {
                "Costo fijo (L)": parametros_base["cf_valores"],
                "Probabilidad": parametros_base["cf_probs"],
            }
        )
        st.dataframe(cf_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Parámetros financieros del proyecto")

        st.write(
            f"- Tasa de impuesto: {parametros_base['tasa_impuesto']*100:.1f}%\n"
            f"- Tasa de descuento: {parametros_base['tasa_descuento']*100:.1f}%\n"
            f"- Horizonte de evaluación: {parametros_base['vida']} años\n"
            f"- Depreciación anual: L {parametros_base['depreciacion']:,.2f}\n"
            f"- Valor de desecho económico: L {parametros_base['valor_desecho']:,.2f}\n"
            f"- Inversión inicial: L {parametros_base['inversion_inicial']:,.2f}"
        )
        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
#   2. SIMULACIÓN MONTE CARLO
# =========================================================

elif opcion == "Simulación Monte Carlo":
    st.markdown("## Simulación Monte Carlo del VAN del proyecto")

    if st.button("Ejecutar simulación"):

        with st.spinner("Guardando parámetros de la simulación en la base de datos..."):
            simulacion_id = guardar_parametros(parametros_base, iteraciones_sidebar)

        with st.spinner("Ejecutando simulación Monte Carlo..."):
            vans, tirs, flujos, resumen = ejecutar_simulacion(
                parametros_base, iteraciones_sidebar
            )

        # Mostrar flujos de una iteración
        st.markdown("### Flujos de caja – Ejemplo de una iteración")
        df_flujos = pd.DataFrame({
            "Año": list(range(1, parametros_base["vida"] + 1)),
            "Flujo de caja": flujos[0]
        })
        st.dataframe(df_flujos, use_container_width=True)

        # Guardar resultados (USANDO LLAVES REALES)
        with st.spinner("Guardando resultados en la base de datos..."):
            guardar_resumen_van(simulacion_id, resumen)
            guardar_iteraciones_van(simulacion_id, vans)

        st.success("Simulación finalizada y almacenada en SQL Server.")

        # MÉTRICAS DE VAN
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-box">Media del VAN<br><b>L {resumen["media"]:,.2f}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-box">Mediana del VAN<br><b>L {resumen["mediana"]:,.2f}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-box">VAN mínimo<br><b>L {resumen["minimo"]:,.2f}</b></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-box">VAN máximo<br><b>L {resumen["maximo"]:,.2f}</b></div>', unsafe_allow_html=True)

        # TIR
        st.markdown("### Comportamiento de la TIR")
        st.write(
            f"- TIR promedio: {resumen.get('media_tir', 0)*100:.2f}%\n"
            f"- TIR mínima: {resumen.get('minimo_tir', 0)*100:.2f}%\n"
            f"- TIR máxima: {resumen.get('maximo_tir', 0)*100:.2f}%"
        )

        # HISTOGRAMA
        st.markdown("### Histograma del VAN")
        hist = tabla_frecuencias(vans, bins=10)
        hist["centro"] = (hist["lim_inf"] + hist["lim_sup"]) / 2
        st.bar_chart(hist.set_index("centro")["frecuencia"])

        # CURVA NORMAL
        fig = grafica_campana_normal(vans)
        st.pyplot(fig)

        ruta_img = guardar_figura_temporal(fig, "grafica_van.png")
        guardar_archivo(simulacion_id, "grafica_van", ruta_img)

        # INTERVALOS DE CONFIANZA
        ic = calcular_intervalos_confianza(resumen["media"], resumen["desviacion"])
        ic_df = pd.DataFrame({
            "Intervalo": ["68%", "95%"],
            "Límite inferior": [ic["68_inf"], ic["95_inf"]],
            "Límite superior": [ic["68_sup"], ic["95_sup"]],
        })
        st.dataframe(ic_df, use_container_width=True)


# =========================================================
#   3. COMPARACIÓN DE ESCENARIOS
# =========================================================

elif opcion == "Comparación de escenarios":
    st.markdown("## Comparación de escenarios: Base, A (optimista) y B (pesimista)")

    if st.button("Ejecutar comparación de escenarios"):

        # === ESCENARIO BASE ===
        with st.spinner("Simulando escenario base..."):
            vans_base, tirs_base, flujos_base, resumen_base = ejecutar_simulacion(
                parametros_base, iteraciones_sidebar
            )

        # === ESCENARIO A ===
        esc_A = construir_escenario_A_optimista(parametros_base)
        with st.spinner("Simulando escenario A (optimista)..."):
            vans_A, tirs_A, flujos_A, resumen_A = ejecutar_simulacion(
                esc_A, iteraciones_sidebar
            )

        # === ESCENARIO B ===
        esc_B = construir_escenario_B_pesimista(parametros_base)
        with st.spinner("Simulando escenario B (pesimista)..."):
            vans_B, tirs_B, flujos_B, resumen_B = ejecutar_simulacion(
                esc_B, iteraciones_sidebar
            )

        st.success("Comparación completada.")

        # === TABLA DE RESULTADOS (VAN + TIR) ===
        df_comp = pd.DataFrame(
            {
                "Indicador": [
                    "Media del VAN",
                    "Mediana del VAN",
                    "Desviación estándar del VAN",
                    "VAN mínimo",
                    "VAN máximo",
                    "TIR promedio",
                    "TIR mínima",
                    "TIR máxima",
                ],
                "Base": [
                    resumen_base["media"],
                    resumen_base["mediana"],
                    resumen_base["desviacion"],
                    resumen_base["minimo"],
                    resumen_base["maximo"],
                    resumen_base.get("media_tir", 0),
                    resumen_base.get("minimo_tir", 0),
                    resumen_base.get("maximo_tir", 0),
                ],
                "Escenario A (optimista)": [
                    resumen_A["media"],
                    resumen_A["mediana"],
                    resumen_A["desviacion"],
                    resumen_A["minimo"],
                    resumen_A["maximo"],
                    resumen_A.get("media_tir", 0),
                    resumen_A.get("minimo_tir", 0),
                    resumen_A.get("maximo_tir", 0),
                ],
                "Escenario B (pesimista)": [
                    resumen_B["media"],
                    resumen_B["mediana"],
                    resumen_B["desviacion"],
                    resumen_B["minimo"],
                    resumen_B["maximo"],
                    resumen_B.get("media_tir", 0),
                    resumen_B.get("minimo_tir", 0),
                    resumen_B.get("maximo_tir", 0),
                ],
            }
        )

        st.dataframe(df_comp, use_container_width=True)


# =========================================================
#   4. VALIDACIÓN ESTADÍSTICA
# =========================================================

elif opcion == "Validación estadística":
    st.markdown("## Validación estadística de los generadores aleatorios")

    st.write(
        """
        En esta sección se validan estadísticamente los números aleatorios que usa el modelo
        para cada variable:
        - Demanda y Costo variable: prueba Chi-cuadrado para distribución uniforme.  
        - Precio: prueba de Kolmogorov–Smirnov para distribución normal.  
        - Costo fijo: prueba Chi-cuadrado para distribución discreta.  
        Nivel de confianza: 95% (α = 0.05).
        """
    )

    if st.button("Ejecutar validación estadística"):
        with st.spinner("Calculando pruebas..."):
            resultados = validar_aleatorios(parametros_base)

        st.success("Pruebas completadas.")

        filas = []
        for var, res in resultados.items():
            filas.append(
                [
                    var,
                    res["prueba"],
                    f"{res['estadistico']:.4f}",
                    f"{res['valor_critico']:.4f}",
                    "Sí" if res["acepta"] else "No",
                ]
            )

        df = pd.DataFrame(
            filas,
            columns=["Variable", "Prueba", "Estadístico", "Valor crítico 5%", "¿Acepta H₀?"],
        )
        st.dataframe(df, use_container_width=True)

        # Valores aleatorios generados
        st.markdown("## Valores aleatorios generados")

        muestra_demanda = [
            generar_uniforme(parametros_base["demanda_min"], parametros_base["demanda_max"])
            for _ in range(200)
        ]
        muestra_cv = [
            generar_uniforme(parametros_base["cv_min"], parametros_base["cv_max"])
            for _ in range(200)
        ]
        muestra_precio = [
            generar_normal(parametros_base["precio_mu"], parametros_base["precio_sigma"])
            for _ in range(200)
        ]
        muestra_cf = [
            generar_discreta(parametros_base["cf_valores"], parametros_base["cf_probs"])
            for _ in range(200)
        ]

        df_aleatorios = pd.DataFrame(
            {
                "Demanda": muestra_demanda,
                "Costo variable": muestra_cv,
                "Precio": muestra_precio,
                "Costo fijo": muestra_cf,
            }
        )

        st.dataframe(df_aleatorios.head(30), use_container_width=True)
        st.info("Mostrando solo los primeros 30 valores.")

        # Histogramas
        st.markdown("## Histogramas de las variables aleatorias")

        fig, axes = plt.subplots(2, 2, figsize=(10, 7))

        axes[0, 0].hist(muestra_demanda, bins=10, color="#2D74DA")
        axes[0, 0].set_title("Demanda (Uniforme)")

        axes[0, 1].hist(muestra_cv, bins=10, color="#F2A900")
        axes[0, 1].set_title("Costo variable (Uniforme)")

        axes[1, 0].hist(muestra_precio, bins=10, color="#00916E")
        axes[1, 0].set_title("Precio (Normal)")

        axes[1, 1].hist(
            muestra_cf, bins=len(parametros_base["cf_valores"]), color="#D00000"
        )
        axes[1, 1].set_title("Costo fijo (Discreta)")

        st.pyplot(fig)
        fig.savefig("assets/hist_variables.png", dpi=200)

        st.markdown(
            """
            ## Explicación del ajuste estadístico

            Para validar que los números aleatorios generados siguen realmente la distribución 
            que definimos teóricamente, aplicamos:

            - **Chi-cuadrado** para distribuciones uniformes y discretas.  
            - **Kolmogorov–Smirnov** para la distribución normal.  

            **¿Qué significa “aceptar H₀”?**

            Si el estadístico es menor que el valor crítico al 5%, significa:

            - ✔ Los aleatorios caen bajo la distribución teórica asumida  
            - ✔ El generador funciona correctamente  
            - ✔ Podemos usar la variable en la simulación Monte Carlo con confianza  
            """
        )


# =========================================================
#   5. INFORME PDF
# =========================================================

elif opcion == "Informe PDF":
    st.markdown("## Generación del informe PDF")

    st.write(
        """
        Esta opción ejecuta una simulación con los parámetros del escenario base
        y genera un informe en PDF que incluye:
        - Resumen estadístico del VAN del proyecto.  
        - Resumen de las pruebas estadísticas aplicadas a las variables aleatorias.  
        """
    )

    if st.button("Generar y descargar informe PDF"):
        with st.spinner("Generando informe..."):
            ruta = generar_reporte(parametros_base, iteraciones_sidebar)

        st.success("Informe generado correctamente.")

        with open(ruta, "rb") as f:
            st.download_button(
                label="Descargar informe PDF",
                data=f,
                file_name="Reporte_Devimulator.pdf",
                mime="application/pdf",
            )
