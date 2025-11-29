import numpy as np
import pandas as pd

def resumen_van(resultados_van):
    """
    Devuelve estadísticas del VAN: media, mediana, desviación std y percentiles.
    """
    arr = np.array(resultados_van)   # ← ESTA es la variable que sí existe

    return {
        "media": float(np.mean(arr)),
        "mediana": float(np.median(arr)),
        "desviacion": float(np.std(arr)),
        "percentil_5": float(np.percentile(arr, 5)),
        "percentil_25": float(np.percentile(arr, 25)),
        "percentil_75": float(np.percentile(arr, 75)),
        "percentil_95": float(np.percentile(arr, 95)),
        "minimo": float(np.min(arr)),
        "maximo": float(np.max(arr)),
    }


def tabla_frecuencias(resultados_van, bins=10):
    """
    Igual al histograma de Excel, devuelve una tabla con:
    - rango inferior
    - rango superior
    - frecuencia
    - frecuencia relativa
    """
    freq, limites = np.histogram(resultados_van, bins=bins)
    total = len(resultados_van)

    data = []
    for i in range(len(freq)):
        data.append({
            "lim_inf": limites[i],
            "lim_sup": limites[i+1],
            "frecuencia": freq[i],
            "frecuencia_relativa": freq[i] / total
        })

    return pd.DataFrame(data)
