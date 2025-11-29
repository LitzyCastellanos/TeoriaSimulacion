import numpy as np
from scipy.stats import chisquare, shapiro

# PRUEBA PARA UNIFORME
def prueba_uniforme(datos, a, b, k=10):
    bins = np.linspace(a, b, k + 1)
    obs, _ = np.histogram(datos, bins=bins)

    esp = np.ones(k) * (len(datos) / k)
    chi2, p = chisquare(obs, esp)

    return {
        "prueba": "Chi-cuadrado",
        "estadistico": float(chi2),
        "p_valor": float(p),
        "acepta": p > 0.05
    }


# PRUEBA PARA NORMAL
def prueba_normal(datos):
    stat, p = shapiro(datos)

    return {
        "prueba": "Shapiro-Wilk",
        "estadistico": float(stat),
        "p_valor": float(p),
        "acepta": p > 0.05
    }


# PRUEBA PARA DISCRETA
def prueba_discreta(datos, valores, probs):
    obs = [np.sum(datos == v) for v in valores]
    esp = [len(datos) * p for p in probs]

    chi2, p = chisquare(obs, esp)

    return {
        "prueba": "Chi-cuadrado",
        "estadistico": float(chi2),
        "p_valor": float(p),
        "acepta": p > 0.05
    }
