# simulador/validacion.py

import math
import numpy as np

from simulador.generadores import (
    generar_uniforme,
    generar_normal,
    generar_discreta,
)


def _chi_cuadrado_uniforme(muestra, a, b, k=5):
    """
    Prueba Chi-cuadrado para variable uniforme [a,b].
    Nivel de significancia 5%, usamos valor crítico tabulado.
    """
    n = len(muestra)
    limites = np.linspace(a, b, k + 1)
    freq_obs, _ = np.histogram(muestra, bins=limites)
    freq_esp = np.ones(k) * (n / k)

    estadistico = np.sum((freq_obs - freq_esp) ** 2 / freq_esp)

    # gl = k - 1 → para k=5 → gl=4 → chi2_crit ~ 9.49
    gl = k - 1
    chi_criticos = {4: 9.49, 5: 11.07, 6: 12.59}
    valor_critico = chi_criticos.get(gl, 9.49)

    acepta = estadistico < valor_critico

    return estadistico, valor_critico, acepta


def _chi_cuadrado_discreta(muestra, valores, probs):
    """
    Prueba Chi-cuadrado para distribución discreta (costo fijo).
    valores: lista de valores posibles
    probs:   lista de probabilidades teóricas
    """
    n = len(muestra)
    valores = np.array(valores)
    probs = np.array(probs)

    freq_obs = []
    freq_esp = []
    for v, p in zip(valores, probs):
        freq_obs.append(np.sum(np.array(muestra) == v))
        freq_esp.append(n * p)

    freq_obs = np.array(freq_obs)
    freq_esp = np.array(freq_esp)

    estadistico = np.sum((freq_obs - freq_esp) ** 2 / freq_esp)

    # gl = k-1 → aquí k = número de categorías
    gl = len(valores) - 1
    chi_criticos = {2: 5.99, 3: 7.81, 4: 9.49}
    valor_critico = chi_criticos.get(gl, 5.99)

    acepta = estadistico < valor_critico

    return estadistico, valor_critico, acepta


def _kolmogorov_smirnov_normal(muestra, mu, sigma):
    """
    Prueba de Kolmogorov–Smirnov para normal N(mu, sigma).
    Usamos nivel de significancia 5% → D_crit ≈ 1.36 / sqrt(n)
    """
    n = len(muestra)
    datos = np.sort(np.array(muestra))

    # CDF teórica normal usando erf
    def cdf_norm(x):
        z = (x - mu) / (sigma * math.sqrt(2))
        return 0.5 * (1 + math.erf(z))

    F_teo = np.array([cdf_norm(x) for x in datos])
    F_emp = np.arange(1, n + 1) / n

    D = np.max(np.abs(F_emp - F_teo))
    D_crit = 1.36 / math.sqrt(n)
    acepta = D < D_crit

    return D, D_crit, acepta


def validar_aleatorios(parametros, n=200):
    """
    Genera muestras de números aleatorios para cada variable
    y aplica la prueba correspondiente:

    - Demanda (Uniforme)        → Chi-cuadrado
    - Costo variable (Uniforme) → Chi-cuadrado
    - Precio (Normal)           → Kolmogorov–Smirnov
    - Costo fijo (Discreta)     → Chi-cuadrado

    Devuelve un diccionario con resultados.
    """
    resultados = {}

    #Demanda (Uniforme)
    muestra_demanda = [
        generar_uniforme(parametros["demanda_min"], parametros["demanda_max"])
        for _ in range(n)
    ]
    estad, crit, acepta = _chi_cuadrado_uniforme(
        muestra_demanda,
        parametros["demanda_min"],
        parametros["demanda_max"],
    )
    resultados["Demanda"] = {
        "prueba": "Chi-cuadrado (Uniforme)",
        "estadistico": float(estad),
        "valor_critico": float(crit),
        "acepta": bool(acepta),
    }

    #Costo variable (Uniforme)
    muestra_cv = [
        generar_uniforme(parametros["cv_min"], parametros["cv_max"])
        for _ in range(n)
    ]
    estad, crit, acepta = _chi_cuadrado_uniforme(
        muestra_cv,
        parametros["cv_min"],
        parametros["cv_max"],
    )
    resultados["Costo variable unitario"] = {
        "prueba": "Chi-cuadrado (Uniforme)",
        "estadistico": float(estad),
        "valor_critico": float(crit),
        "acepta": bool(acepta),
    }

    #Precio (Normal)
    muestra_precio = [
        generar_normal(parametros["precio_mu"], parametros["precio_sigma"])
        for _ in range(n)
    ]
    estad, crit, acepta = _kolmogorov_smirnov_normal(
        muestra_precio,
        parametros["precio_mu"],
        parametros["precio_sigma"],
    )
    resultados["Precio de venta"] = {
        "prueba": "Kolmogorov–Smirnov (Normal)",
        "estadistico": float(estad),
        "valor_critico": float(crit),
        "acepta": bool(acepta),
    }

    #Costo fijo (Discreta)
    muestra_cf = [
        generar_discreta(
            parametros["cf_valores"],
            parametros["cf_probs"],
        )
        for _ in range(n)
    ]
    estad, crit, acepta = _chi_cuadrado_discreta(
        muestra_cf,
        parametros["cf_valores"],
        parametros["cf_probs"],
    )
    resultados["Costo fijo mensual"] = {
        "prueba": "Chi-cuadrado (Discreta)",
        "estadistico": float(estad),
        "valor_critico": float(crit),
        "acepta": bool(acepta),
    }

    return resultados
