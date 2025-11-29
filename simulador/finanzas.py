import numpy as np


# Cálculo de VAN igual que Excel

def calcular_van(inversion_inicial, tasa_descuento, flujo):
    """
    flujo = lista con los flujos de caja de cada año.
    VAN = -inversión inicial + Σ (FC_t / (1+r)^t)
    """

    van = -inversion_inicial

    for t, fc in enumerate(flujo, start=1):
        van += fc / ((1 + tasa_descuento) ** t)

    return van



# Resumen estadístico del VAN

def resumen_van(lista_vanes):

    return {
        "van_promedio": float(np.mean(lista_vanes)),
        "van_min": float(np.min(lista_vanes)),
        "van_max": float(np.max(lista_vanes)),
        "desviacion": float(np.std(lista_vanes)),
        "mediana": float(np.median(lista_vanes))
    }
