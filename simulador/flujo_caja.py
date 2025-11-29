import numpy as np


def flujo_caja_anual(demanda, precio, costo_variable, costo_fijo,
                     depreciacion_anual, tasa_impuesto, valor_desecho=0, ultimo_anio=False):
    """
    Calcula el flujo de caja anual igual que en Excel.

    Fórmulas Excel equivalentes:
        Ingresos = Demanda * Precio
        CV = Demanda * CostoVariable
        Utilidad antes de impuestos = Ingresos - CV - CF - Depreciación
        Impuesto = Utilidad * tasa
        Utilidad neta = Utilidad - Impuesto
        Flujo = Utilidad neta + Depreciación + Valor de desecho (solo último año)
    """

    ingresos = demanda * precio
    cv = demanda * costo_variable

    utilidad = ingresos - cv - costo_fijo - depreciacion_anual
    impuesto_total = utilidad * tasa_impuesto

    utilidad_neta = utilidad - impuesto_total

    flujo = utilidad_neta + depreciacion_anual

    # Valor de desecho si es último año
    if ultimo_anio:
        flujo += valor_desecho

    return flujo, {
        "ingresos": ingresos,
        "cv": cv,
        "utilidad": utilidad,
        "impuesto": impuesto_total,
        "utilidad_neta": utilidad_neta,
        "flujo": flujo,
        "valor_desecho": valor_desecho if ultimo_anio else 0
    }
def calcular_flujo_proyecto(parametros, ultimo_anio=False):
    """
    Wrapper para conectar con simulacion.py
    Parámetros esperados:
        parametros = {
            "demanda": ...,
            "precio": ...,
            "costo_variable": ...,
            "costo_fijo": ...,
            "depreciacion": ...,
            "tasa_impuesto": ...,
            "valor_desecho": ...
        }
    """

    return flujo_caja_anual(
        demanda=parametros["demanda"],
        precio=parametros["precio"],
        costo_variable=parametros["costo_variable"],
        costo_fijo=parametros["costo_fijo"],
        depreciacion_anual=parametros["depreciacion"],
        tasa_impuesto=parametros["tasa_impuesto"],
        valor_desecho=parametros.get("valor_desecho", 0),
        ultimo_anio=ultimo_anio
    )
